#!/usr/bin/env python3
"""
Compute the ForecastBench copier lines and the per-entry bootstrap against the market price.

Data layer only. Emits a single JSON blob consumed by figures.py, and later by the live page.

    python copier_line.py --date 2026-08-11 \
        --processed /path/to/forecastbench-processed-forecast-sets \
        --out copier_line.2026-08-11.json

Inputs, all public:
  question_sets/          freeze values shown to forecasters   (forecastbench-datasets)
  fixed_effects/          FRI's published question difficulty  (forecastbench.org)
  processed forecast sets per-question forecasts and outcomes  (forecastbench.org)

Scoring rule, from forecastingresearch/forecastbench src/leaderboard/main.py:
  question difficulty on a market question is the Brier score of the market price on the
  forecast due date (line 2348); scores are shifted by 0.25 minus the Always 0.5 model's
  score, which equals mean difficulty C (line 2954); and
  Brier Index = (1 - sqrt(rescaled)) * 100 (line 2985).

A forecaster reproducing a price scores zero on the adjusted scale, so its index is
(1 - sqrt(C)) * 100. Two such lines exist because two prices exist: the due-date price the
benchmark scores against, and the older freeze value forecasters were actually shown.
"""

import argparse
import glob
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

MARKET_SOURCES = {"infer", "manifold", "metaculus", "polymarket"}
REFERENCE_MODELS = {
    "Always 0", "Always 0.5", "Always 1",
    "Random Uniform", "Imputed Forecaster", "Naive Forecaster",
}
MIN_QUESTIONS = 50
N_RESAMPLES = 2000
SEED = 11


def index_from(score: float) -> float:
    """Brier Index for a rescaled difficulty-adjusted score."""
    return (1.0 - np.sqrt(score)) * 100.0


def jload(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


def load_freeze_values(question_sets_dir: Path) -> dict:
    """The price shown to forecasters, keyed (due_date, source, id)."""
    out, skipped = {}, 0
    for f in glob.glob(str(question_sets_dir / "*-llm.json")):
        d = jload(f)
        if not isinstance(d, dict) or "questions" not in d:
            skipped += 1
            continue
        due = d["forecast_due_date"]
        for q in d["questions"]:
            if q.get("source") not in MARKET_SOURCES or isinstance(q.get("id"), list):
                continue
            v = pd.to_numeric(q.get("freeze_datetime_value"), errors="coerce")
            if pd.notna(v):
                out[(due, q["source"], str(q["id"]))] = float(v)
    print(f"  freeze values: {len(out):,}  (files skipped: {skipped})")
    return out


def load_forecasts(processed_dir: Path) -> pd.DataFrame:
    """Per-question forecasts for every entry, market questions, resolved, not imputed."""
    rows = []
    files = sorted(glob.glob(str(processed_dir / "*" / "*.json")))
    print(f"  reading {len(files):,} forecast set files")
    for i, f in enumerate(files, 1):
        if i % 500 == 0:
            print(f"    {i}/{len(files)}")
        d = jload(f)
        if not d or "forecasts" not in d:
            continue
        model, due = d.get("model"), d.get("forecast_due_date")
        for x in d["forecasts"]:
            if x.get("source") not in MARKET_SOURCES:
                continue
            if not x.get("resolved") or x.get("imputed"):
                continue
            mv, rt, fc = x.get("market_value_on_due_date"), x.get("resolved_to"), x.get("forecast")
            if mv is None or rt is None or fc is None:
                continue
            rows.append((model, due, x["source"], str(x["id"]),
                         float(fc), float(mv), float(rt)))
    df = pd.DataFrame(rows, columns=["model", "due", "source", "id",
                                     "forecast", "market", "outcome"])
    df["brier"] = (df.forecast - df.outcome) ** 2
    df["gamma"] = (df.market - df.outcome) ** 2      # question difficulty
    df["adj"] = df.brier - df.gamma                  # adjusted score, market-relative
    print(f"  per-question rows: {len(df):,} across {df.model.nunique()} entries")
    return df


def bootstrap(df: pd.DataFrame) -> pd.DataFrame:
    """Per entry, resample questions and test the mean adjusted score against zero."""
    rng = np.random.default_rng(SEED)
    out = []
    for model, g in df.groupby("model"):
        v = g.adj.values
        if len(v) < MIN_QUESTIONS:
            continue
        draws = rng.choice(v, size=(N_RESAMPLES, len(v)), replace=True).mean(axis=1)
        lo, hi = np.percentile(draws, [2.5, 97.5])
        verdict = ("beats market" if hi < 0
                   else "below market" if lo > 0
                   else "indistinguishable")
        out.append(dict(model=model, n=int(len(v)), mean_adj=float(v.mean()),
                        ci_lo=float(lo), ci_hi=float(hi), verdict=verdict,
                        is_reference=model in REFERENCE_MODELS))
    r = pd.DataFrame(out).sort_values("mean_adj").reset_index(drop=True)
    r["rank"] = np.arange(1, len(r) + 1)
    return r


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", default="2026-08-11")
    p.add_argument("--repo", default=".", help="forecastbench-datasets clone")
    p.add_argument("--processed", default="/tmp/fb/forecastbench-processed-forecast-sets")
    p.add_argument("--out", default=None)
    a = p.parse_args()

    repo = Path(a.repo)
    out_path = a.out or f"copier_line.{a.date}.json"

    print("loading inputs")
    freeze = load_freeze_values(repo / "datasets" / "question_sets")
    df = load_forecasts(Path(a.processed))

    # --- C, from FRI's published fixed effects for the requested date -----------
    fe_path = (repo / "fixed_effects" /
               f"question_fixed_effects.{a.date}.tournament_leaderboard.json")
    fe = jload(fe_path)
    if fe is None:
        raise SystemExit(f"missing {fe_path}. Run get_fixed_effects.ps1 first.")
    g = pd.DataFrame(fe)
    C_published = float(g[g.source.isin(MARKET_SOURCES)].question_fixed_effect.mean())

    # --- the two prices, over the questions where both are known ----------------
    q = (df.drop_duplicates(subset=["due", "source", "id"])
           [["due", "source", "id", "market", "outcome", "gamma"]].copy())
    q["freeze"] = [freeze.get(t) for t in zip(q.due, q.source, q.id)]
    q = q.dropna(subset=["freeze"])
    q["brier_freeze"] = (q.freeze - q.outcome) ** 2

    C_reconstructed = float(q.gamma.mean())
    B_freeze = float(q.brier_freeze.mean())

    print("\nbootstrapping")
    r = bootstrap(df)
    counts = r.verdict.value_counts().to_dict()

    blob = {
        "date": a.date,
        "generated_from": {
            "n_question_rows": int(len(df)),
            "n_entries_total": int(df.model.nunique()),
            "n_entries_tested": int(len(r)),
            "min_questions": MIN_QUESTIONS,
            "n_resamples": N_RESAMPLES,
            "seed": SEED,
            "n_questions_both_prices": int(len(q)),
        },
        "anchor": {
            "C_published": C_published,
            "C_reconstructed": C_reconstructed,
            "agreement": abs(C_published - C_reconstructed),
            "brier_freeze": B_freeze,
        },
        "lines": {
            "due_date_price": index_from(C_published),
            "shown_price": index_from(B_freeze),
            "penalty_index_points": index_from(B_freeze) - index_from(C_published),
        },
        "counts": {
            "beats_market": int(counts.get("beats market", 0)),
            "indistinguishable": int(counts.get("indistinguishable", 0)),
            "below_market": int(counts.get("below market", 0)),
        },
        "entries": r.to_dict(orient="records"),
    }

    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(blob, fh, indent=1)

    print(f"\nC published {C_published:.6f}  reconstructed {C_reconstructed:.6f}"
          f"  agree to {abs(C_published-C_reconstructed):.6f}")
    print(f"due-date line {index_from(C_published):.2f}   "
          f"shown-price line {index_from(B_freeze):.2f}")
    print(f"beats market {blob['counts']['beats_market']}   "
          f"indistinguishable {blob['counts']['indistinguishable']}   "
          f"below {blob['counts']['below_market']}")
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
