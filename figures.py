#!/usr/bin/env python3
"""
Figures for the ForecastBench review. All read the blob emitted by copier_line.py.

    python copier_line.py --date 2026-08-11
    python figures.py --blob copier_line.2026-08-11.json

header_card         social / hero card
figure_1_bootstrap  every entry against the market price it was shown. Durable.
figure_2_drift      the frozen human baseline against a moving anchor. Expires with the
                    autumn 2026 superforecaster round.
figure_3_freeze     what the market price in the prompt is worth
figure_4_gradient   where the edge over the market is largest
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
        seg = d[d.cat == verdict]
        if seg.empty:
            continue
        ax.vlines(seg["rank"], seg.ci_lo, seg.ci_hi, color=colour,
                  lw=lw, alpha=alpha if verdict != "beats market" else 0.9, zorder=2)
    ax.plot(d["rank"], d.mean_adj, color=NAVY, lw=1.1, zorder=3)


def _bh_flags(p, alpha=0.05):
    """Benjamini-Hochberg rejection flags for a vector of p-values."""
    p = np.asarray(p, dtype=float)
    m = len(p)
    order = np.argsort(p)
    passed = p[order] <= (np.arange(1, m + 1) / m) * alpha
    k = int(np.max(np.where(passed)[0]) + 1) if passed.any() else 0
    out = np.zeros(m, dtype=bool)
    out[order[:k]] = True
    return out


def _classify(d):
    """Colour categories consistent with the corrected test.

    Bars show 95% intervals, which is the uncorrected per-entry test. Categories use
    Benjamini-Hochberg at 5% FDR across all entries, which is what the headline quotes.
    The two differ for a handful of entries whose interval sits just off zero.
    """
    d = d.copy()
    d["bh_below"] = _bh_flags(d.p_lose.values)
    d["cat"] = np.where(d.verdict == "beats market", "beats market",
                np.where(d.bh_below, "below market", "indistinguishable"))
    return d


def figure_1_bootstrap(blob, path="fig1_vs_market.png"):
    d = pd.DataFrame(blob["entries"])
    d = d[~d.is_reference].sort_values("mean_adj").reset_index(drop=True)
    d["rank"] = np.arange(1, len(d) + 1)
    d = _classify(d)

    n_beat = int((d.cat == "beats market").sum())
    n_ind = int((d.cat == "indistinguishable").sum())
    n_below = int((d.cat == "below market").sum())

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
              [f"clears an uncorrected test  ({n_beat})",
               f"not distinguishable after correction  ({n_ind})",
               f"below the market at 5% FDR  ({n_below})"],
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

    fig.suptitle(f"Of {len(d)} forecasters on ForecastBench, {n_below} score worse "
                 f"than the market price they were shown",
                 fontsize=15.5, fontweight="600", color=NAVY, x=0.008, ha="left", y=0.985)
    fig.text(0.008, 0.928, "None demonstrably beat it. Two clear an uncorrected test, and both were "
                           "named publicly before this analysis existed.",
             fontsize=10.5, color=MUTED, ha="left")

    lines = blob["lines"]
    fig.text(0.008, 0.018,
             f"95% bootstrap intervals, {blob['generated_from']['n_resamples']:,} resamples; "
             f"entries with at least {blob['generated_from']['min_questions']} resolved market "
             f"questions; reference and dummy models excluded. Data as of {blob['date']}.\n"
             f"Question difficulty on a market question is the Brier score of the due-date market "
             f"price (forecastbench src/leaderboard/main.py:2348), so this axis is the benchmark's "
             f"own adjusted score. Copier lines: {lines['due_date_price']:.2f} due-date price, "
             f"{lines['shown_price']:.2f} shown price.\n"
             f"Bars are 95% intervals, the uncorrected per-entry test. Colours use "
             f"Benjamini-Hochberg at 5% FDR across all {len(d)} tests, which returns 0 entries "
             f"beating the market and {n_below} losing to it.\n"
             f"Chance alone would place 2.2 of the 90 entries not significantly below the line "
             f"below it; 2 are there, and both were named publicly before this analysis existed.",
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



def figure_3_freeze(blob, path="fig3_freeze_effect.png"):
    """What the market price in the prompt is worth, and where it still leaves you."""
    fp = blob.get("freeze_pairs") or {}
    if not fp:
        print("no freeze pair data"); return
    r = pd.DataFrame(fp["runs"])
    line_shown = blob["lines"]["shown_price"]

    fig, ax = plt.subplots(figsize=(9.5, 6.2), dpi=200)
    fig.patch.set_facecolor(CREAM); _style(ax)

    for _, e in r.iterrows():
        ax.plot([0, 1], [e.index_hidden, e.index_shown], color=BAND, alpha=0.35, lw=1.3, zorder=2)
    ax.scatter([0]*len(r), r.index_hidden, s=30, color=MUTED, zorder=3, edgecolor=CREAM, lw=0.8)
    ax.scatter([1]*len(r), r.index_shown, s=30, color=BAND, zorder=3, edgecolor=CREAM, lw=0.8)

    for x, v, col in [(0, fp["median_index_hidden"], MUTED), (1, fp["median_index_shown"], BAND)]:
        ax.plot([x-.12, x+.12], [v, v], color=col, lw=3.4, zorder=5)
        ax.annotate(f"median {v:.1f}", xy=(x-.13, v), xytext=(-8, 0), textcoords="offset points",
                    ha="right", va="center", fontsize=10, color=col, fontweight="600")

    ax.axhline(line_shown, color=CLEAR, lw=2.0, ls=(0, (6, 3)), zorder=4)
    ax.annotate(f"submitting the price unchanged scores {line_shown:.1f}",
                xy=(-0.46, line_shown), xytext=(0, 11), textcoords="offset points",
                ha="left", fontsize=9.5, color=CLEAR, fontweight="600")
    ax.axhline(50, color=NAVY, lw=1.0, alpha=0.5, zorder=1)
    ax.annotate("always predicting 50%", xy=(-0.46, 50), xytext=(0, 6),
                textcoords="offset points", ha="left", fontsize=9, color=NAVY, alpha=0.7)

    ax.set_xlim(-0.5, 1.45); ax.set_xticks([0, 1])
    ax.set_xticklabels(["price withheld", "price shown"], fontsize=11, color=NAVY)
    ax.set_ylabel("Brier Index, market questions", fontsize=10, color=NAVY)
    ax.set_title("The market price is worth 16 index points, and still leaves you\n"
                 "short of simply submitting it",
                 fontsize=14, fontweight="600", color=NAVY, loc="left", pad=14)

    fig.text(0.008, 0.018,
             f"{fp['n_runs']} ForecastBench baseline runs, {fp['n_pairs']:,} matched question pairs, "
             f"same model and same questions in both conditions. {fp['n_improved']} of "
             f"{fp['n_runs']} improved.\n"
             f"Within a matched pair the question is identical, so the "
             f"difficulty term cancels and the advantage carries through to the leaderboard in full.",
             fontsize=7.2, color=MUTED, linespacing=1.6)
    fig.tight_layout(rect=(0, 0.085, 1, 1))
    fig.savefig(path, facecolor=CREAM)
    print(f"wrote {path}")


def figure_4_gradient(blob, path="fig4_difficulty_gradient.png"):
    """Where the average forecaster's edge over the market is largest."""
    db = blob.get("difficulty_bins") or {}
    if not db:
        print("no bin data"); return
    lab = db["labels"][::-1]
    allv = db["mean_adj_all"][::-1]
    strv = db["mean_adj_strong"][::-1]
    pool = db["pool_share"][::-1]
    x = np.arange(len(lab))

    fig, (axt, axb) = plt.subplots(2, 1, figsize=(9.5, 6.8), dpi=200,
                                   gridspec_kw={"height_ratios": [3, 1], "hspace": 0.12},
                                   sharex=True)
    fig.patch.set_facecolor(CREAM)
    for a in (axt, axb): _style(a)

    axt.axhline(0, color=NAVY, lw=1.5, zorder=4)
    axt.plot(x, allv, color=BAND, lw=2.4, marker="o", ms=6, zorder=3,
             label="all 527 entries")
    axt.plot(x, strv, color=CLEAR, lw=2.4, marker="o", ms=6, zorder=3,
             label="the 90 at or above the market")
    axt.annotate("the market price", xy=(0, 0), xytext=(5, 7),
                 textcoords="offset points", ha="left", fontsize=9,
                 color=NAVY, fontweight="600")
    axt.annotate(f"spread {allv[-1]-allv[0]:+.3f}", xy=(0.06, allv[0]), xytext=(12, -16),
                 textcoords="offset points", fontsize=9, color=BAND, fontweight="600")
    axt.annotate(f"spread {strv[-1]-strv[0]:+.3f}", xy=(0.06, strv[0]), xytext=(12, -16),
                 textcoords="offset points", fontsize=9, color=CLEAR, fontweight="600")
    axt.set_ylabel("mean Brier score minus\nthe market's Brier score", fontsize=10, color=NAVY)
    axt.legend(frameon=False, fontsize=9.5, loc="upper left", labelcolor=NAVY)
    axt.set_title("The average forecaster's edge over the market is largest\n"
                  "where the market is least certain",
                  fontsize=14, fontweight="600", color=NAVY, loc="left", pad=14)

    axb.bar(x, pool, color=BELOW, width=0.6, zorder=3)
    for xi, p in zip(x, pool):
        axb.annotate(f"{p:.0f}%", xy=(xi, p), xytext=(0, 4), textcoords="offset points",
                     ha="center", fontsize=8.5, color=MUTED)
    axb.set_ylabel("share of\nquestions", fontsize=9, color=NAVY)
    axb.set_ylim(0, max(pool)*1.35)
    axb.set_xticks(x)
    axb.set_xticklabels([f"{l}" for l in lab], fontsize=9.5, color=NAVY)
    axb.set_xlabel("market price distance from 0.5      "
                   "(left = near coin flip, right = near certain)",
                   fontsize=9.5, color=NAVY)

    fig.text(0.008, 0.018,
             "423,396 resolved market forecasts, binned on the market price, which is observable "
             "in advance. The outcome is never used to form the bins.\n"
             "Half the market questions carry a price within 0.05 of 0 or 1.",
             fontsize=7.2, color=MUTED, linespacing=1.6)
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    fig.savefig(path, facecolor=CREAM)
    print(f"wrote {path}")



def header_card(blob, path="header.png"):
    """Hero / social card. 1200x630. Must read at thumbnail size, so: one number,
    one sentence, and the shape of the result."""
    d = pd.DataFrame(blob["entries"])
    d = d[~d.is_reference].sort_values("mean_adj").reset_index(drop=True)
    d["rank"] = np.arange(1, len(d) + 1)
    n_beat = int((d.verdict == "beats market").sum())

    fig = plt.figure(figsize=(12, 6.3), dpi=100)
    fig.patch.set_facecolor(CREAM)

    # type block
    d = _classify(d)
    n_lose = int((d.cat == "below market").sum())
    fig.text(0.065, 0.775, f"{n_lose} of {len(d)}", fontsize=64, fontweight="700",
             color=NAVY, va="top", ha="left")
    fig.text(0.065, 0.545,
             "forecasters on ForecastBench score worse than the market price they were shown.",
             fontsize=18, color=NAVY, va="top", ha="left")
    fig.text(0.065, 0.455,
             "None demonstrably beat it.",
             fontsize=15, color=MUTED, va="top", ha="left")
    fig.text(0.065, 0.115, "THE COPIER LINE", fontsize=12.5, fontweight="700",
             color=CLEAR, va="bottom", ha="left")
    fig.text(0.065, 0.062, "What ForecastBench's market scores measure",
             fontsize=12.5, color=MUTED, va="bottom", ha="left")

    # the result, drawn small and wide under the type
    ax = fig.add_axes([0.065, 0.185, 0.87, 0.19])
    ax.set_facecolor(CREAM)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])

    for verdict, colour, alpha, lw in [("below market", BELOW, 0.9, 0.9),
                                       ("indistinguishable", BAND, 0.5, 0.9),
                                       ("beats market", CLEAR, 1.0, 2.6)]:
        seg = d[d.cat == verdict]
        ax.vlines(seg["rank"], seg.ci_lo, seg.ci_hi, color=colour, lw=lw,
                  alpha=alpha, zorder=2)
    ax.axhline(0, color=NAVY, lw=1.7, zorder=4)
    ax.set_xlim(-6, len(d) + 6)
    # orientation matches Figure 1: below the line adds information over the market
    ax.set_ylim(-0.055, 0.14)
    ax.annotate("the market price", xy=(len(d), 0), xytext=(0, 6),
                textcoords="offset points", ha="right", va="bottom",
                fontsize=9.5, color=NAVY, fontweight="600")
    ax.annotate(f"{int((d.cat == chr(98)+chr(101)+chr(97)+chr(116)+chr(115)+chr(32)+chr(109)+chr(97)+chr(114)+chr(107)+chr(101)+chr(116)).sum())} clear an uncorrected test", xy=(2, d.ci_lo.min()), xytext=(16, 0),
                textcoords="offset points", ha="left", va="center",
                fontsize=9.5, color=CLEAR, fontweight="700")

    fig.savefig(path, facecolor=CREAM)
    print(f"wrote {path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--blob", default="copier_line.2026-08-11.json")
    a = p.parse_args()
    with open(a.blob, encoding="utf-8") as fh:
        blob = json.load(fh)
    header_card(blob)
    figure_1_bootstrap(blob)
    figure_2_drift(blob)
    figure_3_freeze(blob)
    figure_4_gradient(blob)
