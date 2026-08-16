#!/usr/bin/env python3
"""
Does handing a model the market price change its forecast, and its score?

ForecastBench runs its own baseline models twice on identical question sets:
    run-variant-NN-zero-shot                        (no market price in prompt)
    run-variant-NN-zero-shot-with-freeze-values     (market price in prompt)

That is a controlled experiment, already run, in public data. This script measures
the paired difference, and separately measures how closely every entry on the board
tracks the market price.

Input: extracted processed_forecast_sets.tar.gz
    https://www.forecastbench.org/assets/data/processed-forecast-sets/processed_forecast_sets.tar.gz

Usage:
    python analyse_freeze_values.py /path/to/forecastbench-processed-forecast-sets

Outputs:
    freeze_value_effect.csv   paired within-model comparison
    market_tracking.csv       market-tracking stats for every entry
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

MARKET_SOURCES = {"infer", "manifold", "metaculus", "polymarket"}
EXACT_TOL = 0.005          # "copied": within 0.5 percentage points, per FRI's own framing


def load(root: Path) -> pd.DataFrame:
    rows = []
    files = sorted(root.rglob("*.json"))
    print(f"reading {len(files)} forecast set files ...")

    for i, fp in enumerate(files, 1):
        if i % 250 == 0:
            print(f"  {i}/{len(files)}")
        try:
            d = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict) or "forecasts" not in d:
            continue

        meta = dict(
            model=d.get("model"),
            model_org=d.get("model_organization"),
            org=d.get("organization"),
            due=d.get("forecast_due_date"),
            eligible=d.get("leaderboard_eligible"),
            run_key=d.get("model_run_key"),
            variant=d.get("forecast_variant_key"),
        )

        for f in d["forecasts"]:
            if f.get("source") not in MARKET_SOURCES:
                continue
            if not f.get("resolved"):
                continue
            mv = f.get("market_value_on_due_date")
            fc = f.get("forecast")
            rt = f.get("resolved_to")
            if mv is None or fc is None or rt is None:
                continue
            rows.append(
                dict(**meta, qid=f.get("id"), source=f.get("source"),
                     forecast=float(fc), market=float(mv),
                     resolved_to=float(rt), imputed=bool(f.get("imputed", False)))
            )

    df = pd.DataFrame(rows)
    print(f"market-question rows, resolved: {len(df):,}")
    return df


def tracking_stats(g: pd.DataFrame) -> pd.Series:
    real = g[~g.imputed]
    n = len(real)
    if n < 20:
        return pd.Series(dtype="float64")
    d = (real.forecast - real.market).abs()
    return pd.Series(dict(
        n=n,
        pct_imputed=100 * g.imputed.mean(),
        corr=real.forecast.corr(real.market),
        pct_within_0p5pp=100 * (d < EXACT_TOL).mean(),
        pct_within_2pp=100 * (d < 0.02).mean(),
        median_abs_dev=d.median(),
        brier=((real.forecast - real.resolved_to) ** 2).mean(),
        brier_market=((real.market - real.resolved_to) ** 2).mean(),
    ))


def main(root: Path) -> None:
    df = load(root)
    if df.empty:
        sys.exit("No usable rows.")

    # ---------- every entry, how closely does it track the market ----------
    print("\n" + "=" * 78)
    print("MARKET TRACKING — all entries, resolved market questions, all rounds")
    print("=" * 78)
    recs = []
    for (mdl, morg), g in df.groupby(["model", "model_org"], dropna=False):
        s = tracking_stats(g)
        if s.empty or pd.isna(s.get("corr")):
            continue
        recs.append(dict(model=mdl, model_org=morg, **s.to_dict()))
    t = pd.DataFrame(recs)
    t = t[t["n"] >= 50].sort_values("corr", ascending=False)
    t["brier_vs_market"] = t.brier - t.brier_market
    t.to_csv("market_tracking.csv", index=False)

    show = ["model", "n", "corr", "pct_within_0p5pp", "median_abs_dev", "brier", "brier_market"]
    print("\nTOP 15 BY CORRELATION WITH THE MARKET PRICE")
    print(t.head(15)[show].to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    print("\nBOTTOM 10")
    print(t.tail(10)[show].to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    print(f"\nentries with corr > 0.95: {(t['corr'] > 0.95).sum()} of {len(t)}")
    print(f"entries with corr > 0.99: {(t['corr'] > 0.99).sum()} of {len(t)}")
    print(f"median correlation across all entries: {t['corr'].median():.3f}")

    # ---------- the paired experiment ----------
    print("\n" + "=" * 78)
    print("PAIRED: same model, same questions, price shown vs price withheld")
    print("=" * 78)
    pair = df[df.run_key.notna() & df.variant.notna()].copy()
    if pair.empty:
        print("no variant-tagged runs found")
        return
    pair["shown"] = pair.variant.str.contains("with-freeze-values")

    key = ["run_key", "due", "qid"]
    a = pair[pair.shown].set_index(key)
    b = pair[~pair.shown].set_index(key)
    common = a.index.intersection(b.index)
    print(f"matched question-level pairs: {len(common):,}")
    if len(common) == 0:
        return

    m = pd.DataFrame({
        "run_key": [i[0] for i in common],
        "fc_shown": a.loc[common, "forecast"].values,
        "fc_hidden": b.loc[common, "forecast"].values,
        "market": a.loc[common, "market"].values,
        "resolved_to": a.loc[common, "resolved_to"].values,
    })

    def paired(g):
        return pd.Series(dict(
            n=len(g),
            corr_shown=g.fc_shown.corr(g.market),
            corr_hidden=g.fc_hidden.corr(g.market),
            copy_rate_shown=100 * ((g.fc_shown - g.market).abs() < EXACT_TOL).mean(),
            copy_rate_hidden=100 * ((g.fc_hidden - g.market).abs() < EXACT_TOL).mean(),
            brier_shown=((g.fc_shown - g.resolved_to) ** 2).mean(),
            brier_hidden=((g.fc_hidden - g.resolved_to) ** 2).mean(),
        ))

    precs = []
    for rk, g in m.groupby("run_key"):
        s = paired(g)
        precs.append(dict(run_key=rk, **s.to_dict()))
    p = pd.DataFrame(precs)
    p = p[p["n"] >= 50]
    p["d_corr"] = p.corr_shown - p.corr_hidden
    p["d_brier"] = p.brier_shown - p.brier_hidden      # negative = showing price helped
    p = p.sort_values("d_brier")
    p.to_csv("freeze_value_effect.csv", index=False)

    print()
    print(p[["run_key", "n", "corr_hidden", "corr_shown", "copy_rate_hidden",
             "copy_rate_shown", "brier_hidden", "brier_shown", "d_brier"]]
          .to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    print("\n" + "-" * 78)
    print(f"models where showing the price improved Brier: "
          f"{(p.d_brier < 0).sum()} of {len(p)}")
    print(f"median Brier change when price shown: {p.d_brier.median():+.4f}")
    print(f"median correlation with market — price hidden: {p.corr_hidden.median():.3f}")
    print(f"median correlation with market — price shown:  {p.corr_shown.median():.3f}")
    print(f"median copy rate (within 0.5pp) — price shown: {p.copy_rate_shown.median():.1f}%")

    print("\nwrote market_tracking.csv, freeze_value_effect.csv")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(Path(sys.argv[1]))
