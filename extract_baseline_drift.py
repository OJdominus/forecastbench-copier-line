#!/usr/bin/env python3
"""
Reconstruct the ForecastBench tournament leaderboard from git history.

Measures how the superforecaster human baseline moved over time, against how many
additional questions actually resolved. The superforecasters submitted forecasts once,
on 2024-07-21; that forecast set has never changed.

Run from inside a full (non-shallow) clone of
    https://github.com/forecastingresearch/forecastbench-datasets

    git clone https://github.com/forecastingresearch/forecastbench-datasets.git
    cd forecastbench-datasets
    python extract_baseline_drift.py

Outputs
    baseline_drift.csv   one row per leaderboard revision
    baseline_drift.png   figure

Requires: pandas, matplotlib

Data: CC BY-SA 4.0, Forecasting Research Institute.
"""

import io
import subprocess
import sys

import pandas as pd

LEADERBOARD = "leaderboards/csv/leaderboard_tournament.csv"
HUMAN_ROW = "Superforecaster median forecast"

# The leaderboard reported raw Brier scores (lower is better, ~0.04) until the Brier
# Index (0-100, higher is better) was introduced. The switch appears in this file on
# 2026-03-04. Series that cross this date are not comparable.
BRIER_INDEX_FROM = "2026-03-04"


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def check_repo() -> None:
    try:
        git("rev-parse", "--git-dir")
    except Exception:
        sys.exit("Not a git repository. Run this inside the forecastbench-datasets clone.")
    if git("rev-parse", "--is-shallow-repository").strip() == "true":
        sys.exit("Shallow clone: history is truncated. Run `git fetch --unshallow` first.")


def revisions() -> list[tuple[str, str]]:
    """(sha, iso_date) for every commit touching the tournament leaderboard, oldest first."""
    out = git("log", "--format=%H|%ci", "--", LEADERBOARD).strip().splitlines()
    return [tuple(line.split("|")) for line in out if "|" in line][::-1]


def extract() -> pd.DataFrame:
    rows = []
    revs = revisions()
    print(f"revisions of {LEADERBOARD}: {len(revs)}")

    for sha, date in revs:
        day = date[:10]
        try:
            text = git("show", f"{sha}:{LEADERBOARD}")
        except Exception:
            continue
        if not text.strip():
            continue
        try:
            df = pd.read_csv(io.StringIO(text))
        except Exception:
            continue
        if "Model" not in df.columns or "Market" not in df.columns:
            continue

        human = df[df["Model"] == HUMAN_ROW]
        if human.empty:
            continue
        h = human.iloc[0]

        ai = df[~df["Team"].astype(str).eq("ForecastBench")]
        if ai.empty or ai["Market"].isna().all():
            continue
        best = ai.loc[ai["Market"].idxmax()]

        rows.append(
            dict(
                date=day,
                sha=sha[:10],
                human_market=h["Market"],
                human_market_n=h["N market"],
                human_dataset=h["Dataset"],
                human_dataset_n=h["N dataset"],
                human_overall=h["Overall"],
                human_rank=h["Rank"],
                best_ai_market=best["Market"],
                best_ai_market_n=best["N market"],
                best_ai_model=str(best["Model"]),
                n_entries=len(df),
                n_ai_above_human=int((ai["Market"] > h["Market"]).sum()),
            )
        )

    out = (
        pd.DataFrame(rows)
        .drop_duplicates(subset="date", keep="last")
        .sort_values("date")
        .reset_index(drop=True)
    )
    out["brier_index_era"] = out["date"] >= BRIER_INDEX_FROM
    return out


def report(df: pd.DataFrame) -> None:
    era = df[df.brier_index_era]
    if era.empty:
        print("No revisions in the Brier Index era.")
        return

    peak = era.loc[era.human_market.idxmax()]
    last = era.iloc[-1]

    print()
    print("=" * 72)
    print("HUMAN BASELINE DRIFT  (Brier Index era only)")
    print("=" * 72)
    print(f"revisions analysed: {len(era)}  ({era.date.iloc[0]} to {last.date})")
    print()
    print(f"peak    {peak.date}   market {peak.human_market:5.1f}   "
          f"n_market {int(peak.human_market_n)}   n_dataset {int(peak.human_dataset_n)}")
    print(f"latest  {last.date}   market {last.human_market:5.1f}   "
          f"n_market {int(last.human_market_n)}   n_dataset {int(last.human_dataset_n)}")
    print()
    print(f"  market score moved      {last.human_market - peak.human_market:+.1f} points")
    print(f"  market questions added  {int(last.human_market_n - peak.human_market_n)}")
    print(f"  dataset questions added {int(last.human_dataset_n - peak.human_dataset_n)}")
    print()
    print("  Superforecaster forecasts were submitted once, on 2024-07-21,")
    print("  and have not changed.")

    cross = era[era.best_ai_market > era.human_market]
    if not cross.empty:
        c = cross.iloc[0]
        print()
        print(f"first revision where an AI entry exceeds the human market score: {c.date}")
        print(f"  {c.best_ai_model} {c.best_ai_market:.1f} (n={int(c.best_ai_market_n)}) "
              f"vs humans {c.human_market:.1f} (n={int(c.human_market_n)})")


def plot(df: pd.DataFrame, path: str = "baseline_drift.png") -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    era = df[df.brier_index_era].copy()
    era["d"] = pd.to_datetime(era["date"])

    INK, HUMAN, AI, GRID = "#1a1a1a", "#B4443A", "#2E6E8E", "#E2E2E2"

    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    peak = era.loc[era.human_market.idxmax()]
    last = era.iloc[-1]

    # headroom so annotations never collide with the title or the axis
    lo = min(era.human_market.min(), era.best_ai_market.min())
    hi = max(era.human_market.max(), era.best_ai_market.max())
    pad = (hi - lo) * 0.18
    ax.set_ylim(lo - pad, hi + pad)

    cross = era[era.best_ai_market > era.human_market]
    if not cross.empty:
        c = cross.iloc[0]
        ax.axvline(c.d, color=INK, lw=0.8, ls=(0, (4, 3)), alpha=0.5, zorder=1)
        ax.annotate("AI entries overtake\nthe human baseline",
                    xy=(c.d, lo - pad * 0.55), xytext=(7, 0),
                    textcoords="offset points", fontsize=8.5, color=INK,
                    alpha=0.7, linespacing=1.4, va="center")

    ax.plot(era.d, era.human_market, color=HUMAN, lw=2.4, zorder=3,
            label="Superforecaster median  (forecasts fixed 2024-07-21)")
    ax.plot(era.d, era.best_ai_market, color=AI, lw=2.4, zorder=3,
            label="Best AI entry on market questions")

    ax.scatter([peak.d, last.d], [peak.human_market, last.human_market],
               s=26, color=HUMAN, zorder=4)
    ax.annotate(f"{peak.human_market:.1f}   n = {int(peak.human_market_n)}",
                xy=(peak.d, peak.human_market), xytext=(9, 9),
                textcoords="offset points", ha="left", fontsize=9.5,
                color=HUMAN, fontweight="600")
    ax.annotate(f"{last.human_market:.1f}   n = {int(last.human_market_n)}",
                xy=(last.d, last.human_market), xytext=(-9, -18),
                textcoords="offset points", ha="right", fontsize=9.5,
                color=HUMAN, fontweight="600")

    ax.set_ylabel("Brier Index, market questions  (higher is better)", fontsize=10)
    ax.set_title(
        "ForecastBench's human baseline fell "
        f"{abs(last.human_market - peak.human_market):.1f} points in four months\n"
        "while one additional question resolved",
        fontsize=14, fontweight="600", color=INK, loc="left", pad=16,
    )

    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors="#555", labelsize=9)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())

    ax.legend(frameon=False, fontsize=9.5, loc="upper right",
              bbox_to_anchor=(1.0, 1.0), handlelength=1.8, borderaxespad=0.4)

    fig.text(0.008, 0.012,
             f"Reconstructed from {len(era)} git revisions of leaderboards/csv/"
             "leaderboard_tournament.csv, forecastingresearch/forecastbench-datasets. "
             "CC BY-SA 4.0.\nBrier Index era only; the metric changed on 2026-03-04.",
             fontsize=7.2, color="#8A8A8A", linespacing=1.5)

    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.savefig(path, facecolor="white")
    print(f"\nwrote {path}")


if __name__ == "__main__":
    check_repo()
    data = extract()
    data.to_csv("baseline_drift.csv", index=False)
    print(f"wrote baseline_drift.csv  ({len(data)} revisions)")
    report(data)
    plot(data)
