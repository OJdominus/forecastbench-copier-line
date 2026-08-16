#!/usr/bin/env python3
"""
Two figures for the ForecastBench review. Both read the blob from copier_line.py.

    python copier_line.py --date 2026-08-11
    python figures.py --blob copier_line.2026-08-11.json

figure_1_bootstrap  every entry against the market price it was shown. Durable.
figure_2_drift      the frozen human baseline against a moving anchor. Expires with the
                    fall 2026 superforecaster round.
"""

import argparse
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle

CREAM = "#FAF6EE"
NAVY = "#16283C"
CLEAR = "#B4443A"      # the entries that beat the market
BAND = "#4E86A5"       # indistinguishable from the market
BELOW = "#C6CDD4"      # significantly below the market
GRID = "#E4DFD4"
MUTED = "#8A8579"

ANNOTATE = ["Cassi-2026-05-10", "Superforecaster median forecast", "Public median forecast"]


def _style(ax):
    ax.set_facecolor(CREAM)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8.5)


def _ribbon(ax, d, lw=0.9, alpha=0.55):
    """One thin vertical interval per entry. At article width these merge into a band
    without the false edges a filled polygon draws between non-monotone bounds."""
    for verdict, colour in [("below market", BELOW),
                            ("indistinguishable", BAND),
                            ("beats market", CLEAR)]:
        seg = d[d.verdict == verdict]
        if seg.empty:
            continue
        ax.vlines(seg["rank"], seg.ci_lo, seg.ci_hi, color=colour,
                  lw=lw, alpha=alpha if verdict != "beats market" else 0.9, zorder=2)
    ax.plot(d["rank"], d.mean_adj, color=NAVY, lw=1.1, zorder=3)


def figure_1_bootstrap(blob, path="fig1_vs_market.png"):
    d = pd.DataFrame(blob["entries"])
    d = d[~d.is_reference].sort_values("mean_adj").reset_index(drop=True)
    d["rank"] = np.arange(1, len(d) + 1)

    n_beat = int((d.verdict == "beats market").sum())
    n_ind = int((d.verdict == "indistinguishable").sum())
    n_below = int((d.verdict == "below market").sum())

    fig, (ax, axz) = plt.subplots(
        1, 2, figsize=(13.5, 6.4), dpi=200,
        gridspec_kw={"width_ratios": [1, 1.25], "wspace": 0.20})
    fig.patch.set_facecolor(CREAM)
    for a in (ax, axz):
        _style(a)

    # ---------------- panel A: all entries ----------------
    _ribbon(ax, d, lw=0.7, alpha=0.45)
    ax.axhline(0, color=NAVY, lw=1.6, zorder=4)
    ax.set_xlim(-4, len(d) + 4)
    ax.set_ylim(-0.055, d.ci_hi.max() * 1.04)
    ax.set_xlabel("all entries, ranked", fontsize=9.5, color=NAVY)
    ax.set_ylabel("Brier score minus the market's Brier score\n(below zero = adds information)",
                  fontsize=10, color=NAVY)
    ax.annotate("the market price\nit was shown", xy=(len(d) * 0.99, 0),
                xytext=(0, 9), textcoords="offset points", ha="right",
                fontsize=9, color=NAVY, fontweight="600", linespacing=1.35)

    handles = [Rectangle((0, 0), 1, 1, color=CLEAR),
               Rectangle((0, 0), 1, 1, color=BAND, alpha=0.55),
               Rectangle((0, 0), 1, 1, color=BELOW)]
    ax.legend(handles,
              [f"beats the market  ({n_beat})",
               f"indistinguishable  ({n_ind})",
               f"below the market  ({n_below})"],
              frameon=False, fontsize=9, loc="upper left",
              bbox_to_anchor=(0.02, 0.99), labelcolor=NAVY)

    # ---------------- panel B: the decisive region ----------------
    ZOOM = 120
    top = d[d["rank"] <= ZOOM]
    _ribbon(axz, top, lw=1.6, alpha=0.5)
    axz.axhline(0, color=NAVY, lw=1.6, zorder=4)
    axz.set_xlim(-1, ZOOM + 1)
    axz.set_ylim(-0.048, 0.062)
    axz.set_xlabel(f"top {ZOOM} entries", fontsize=9.5, color=NAVY)
    axz.set_title("where every entry that clears the market sits",
                  fontsize=10.5, color=MUTED, loc="left", pad=8)

    bnd = int(d[d.verdict == "indistinguishable"]["rank"].max())
    if bnd <= ZOOM:
        axz.axvline(bnd, color=MUTED, lw=0.9, ls=(0, (3, 3)), zorder=5)
        axz.annotate(f"beyond rank {bnd}, every\nentry is below the market",
                     xy=(bnd, 0.056), xytext=(8, 0), textcoords="offset points",
                     fontsize=8.4, color=MUTED, va="top", linespacing=1.4)
    else:
        axz.annotate(f"the indistinguishable band runs to rank {bnd};\n"
                     f"beyond it every entry is below the market",
                     xy=(0.985, 0.03), xycoords="axes fraction", ha="right", va="bottom",
                     fontsize=8.4, color=MUTED, linespacing=1.4)

    # annotations: the two that clear, then the public median wherever it lands
    offsets = {"Cassi-2026-05-10": (24, -30),
               "Superforecaster median forecast": (30, 18),
               "Public median forecast": (14, 16)}
    labels = {"Cassi-2026-05-10": "Cassi-2026-05-10",
              "Superforecaster median forecast": "Superforecaster median",
              "Public median forecast": "Public median"}
    for name in ANNOTATE:
        row = d[d.model == name]
        if row.empty:
            continue
        r = row.iloc[0]
        tgt = axz if r["rank"] <= ZOOM else ax
        beats = r.verdict == "beats market"
        col = CLEAR if beats else NAVY
        tgt.scatter([r["rank"]], [r.mean_adj], s=38, color=col, zorder=6,
                    edgecolor=CREAM, lw=1.0)
        tgt.annotate(f"{labels[name]}\n{r.mean_adj:+.4f}",
                     xy=(r["rank"], r.mean_adj), xytext=offsets[name],
                     textcoords="offset points", fontsize=8.8, color=col,
                     fontweight="600" if beats else "normal", linespacing=1.4,
                     arrowprops=dict(arrowstyle="-", color=col, lw=0.9, alpha=0.6))

    fig.suptitle(f"Of {len(d)} forecasters on ForecastBench, {n_beat} beat the market price",
                 fontsize=15.5, fontweight="600", color=NAVY, x=0.008, ha="left", y=0.985)

    lines = blob["lines"]
    fig.text(0.008, 0.018,
             f"95% bootstrap intervals, {blob['generated_from']['n_resamples']:,} resamples; "
             f"entries with at least {blob['generated_from']['min_questions']} resolved market "
             f"questions; reference and dummy models excluded. Data as of {blob['date']}.\n"
             f"Question difficulty on a market question is the Brier score of the due-date market "
             f"price (forecastbench src/leaderboard/main.py:2348), so this axis is the benchmark's "
             f"own adjusted score. Copier lines: {lines['due_date_price']:.2f} due-date price, "
             f"{lines['shown_price']:.2f} shown price.",
             fontsize=7.2, color=MUTED, linespacing=1.6)

    fig.tight_layout(rect=(0, 0.10, 1, 0.945))
    fig.subplots_adjust(bottom=0.20)
    fig.savefig(path, facecolor=CREAM)
    print(f"wrote {path}   ({n_beat} beat / {n_ind} indistinguishable / {n_below} below)")


def figure_2_drift(blob, drift_csv="baseline_drift.csv", path="fig2_drift.png"):
    h = pd.read_csv(drift_csv)
    h = h[h.brier_index_era].copy()
    h["d"] = pd.to_datetime(h.date)
    adj = -0.0173
    h["C"] = (1 - h.human_market / 100) ** 2 - adj
    h["copier"] = (1 - np.sqrt(h.C)) * 100

    fig, ax = plt.subplots(figsize=(10.5, 5.8), dpi=200)
    fig.patch.set_facecolor(CREAM)
    _style(ax)

    ax.fill_between(h.d, h.copier, h.human_market, color=CLEAR, alpha=0.16, zorder=2)
    ax.plot(h.d, h.human_market, color=CLEAR, lw=2.4, zorder=3,
            label="Superforecaster median, as published")
    ax.plot(h.d, h.copier, color=NAVY, lw=1.8, ls=(0, (5, 3)), zorder=3,
            label="Copier line, recomputed daily")

    f, l = h.iloc[0], h.iloc[-1]
    pk = h.loc[h.human_market.idxmax()]
    for r in (pk, l):
        ax.scatter([r.d], [r.human_market], s=28, color=CLEAR, zorder=5)
    ax.annotate(f"{pk.human_market:.1f}", xy=(pk.d, pk.human_market), xytext=(8, 6),
                textcoords="offset points", fontsize=9.5, color=CLEAR, fontweight="600")
    ax.annotate(f"{l.human_market:.1f}", xy=(l.d, l.human_market), xytext=(-8, -18),
                textcoords="offset points", ha="right", fontsize=9.5,
                color=CLEAR, fontweight="600")

    mid = h.iloc[len(h) // 2]
    ax.annotate(f"gap = {adj:+.4f} adjusted score,\nunchanged since July 2024",
                xy=(mid.d, (mid.human_market + mid.copier) / 2),
                xytext=(0, 0), textcoords="offset points", ha="center", va="center",
                fontsize=9, color=NAVY, linespacing=1.4)

    ax.set_ylabel("Brier Index, market questions", fontsize=10, color=NAVY)
    ax.set_title("The superforecaster score fell 4.7 points. Their forecasts never changed.",
                 fontsize=14, fontweight="600", color=NAVY, loc="left", pad=14)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.legend(frameon=False, fontsize=9.5, loc="lower left", labelcolor=NAVY)

    fig.text(0.008, 0.012,
             "Superforecasters forecast once, on 2024-07-21. Their difficulty-adjusted market "
             "score is fixed at -0.0173: raw Brier 0.0830 against the market's 0.1003 on the same "
             "57 questions.\nThe published index moves because the rescaling anchor does. "
             "Brier Index era only; the metric changed on 2026-03-04.",
             fontsize=7, color=MUTED, linespacing=1.55)

    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(path, facecolor=CREAM)
    print(f"wrote {path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--blob", default="copier_line.2026-08-11.json")
    a = p.parse_args()
    with open(a.blob, encoding="utf-8") as fh:
        blob = json.load(fh)
    figure_1_bootstrap(blob)
    figure_2_drift(blob)
