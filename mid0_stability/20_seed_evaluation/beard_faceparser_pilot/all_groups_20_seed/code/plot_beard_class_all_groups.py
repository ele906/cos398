#!/usr/bin/env python3
"""Plot Beard-class prediction curves across all prompt groups."""

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

GROUP_ORDER = (
    "black_man", "black_woman", "east_asian_man", "east_asian_woman",
    "hispanic_man", "hispanic_woman", "indian_man", "indian_woman",
    "middle_eastern_man", "middle_eastern_woman", "white_man", "white_woman",
)
ALPHAS = (-7, 1, 7)


def read_rows(path: Path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, required=True)
    args = parser.parse_args()
    rows = read_rows(args.results_dir / "beard_class_metrics.csv")
    summaries = read_rows(args.results_dir / "group_alpha_summary.csv")
    present = {row["prompt_group"] for row in rows}
    groups = [group for group in GROUP_ORDER if group in present]
    if not groups:
        raise ValueError("No recognized prompt groups found in metrics CSV")
    ncols = 3
    nrows = int(np.ceil(len(groups) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(13.2, 3.05 * nrows), sharex=True, sharey=True, squeeze=False)
    x = np.arange(len(ALPHAS))
    group_summary = {(r["prompt_group"], int(float(r["alpha"]))): r for r in summaries}
    color_by_gender = {"man": "#2468a2", "woman": "#aa3f81"}
    for ax, group in zip(axes.flat, groups):
        group_rows = [r for r in rows if r["prompt_group"] == group]
        seeds = sorted({int(r["seed"]) for r in group_rows})
        by_seed = {
            seed: {int(float(r["alpha"])): 100 * float(r["beard_fraction_image"])
                   for r in group_rows if int(r["seed"]) == seed}
            for seed in seeds
        }
        for seed in seeds:
            ax.plot(x, [by_seed[seed][alpha] for alpha in ALPHAS], color="#7b7b7b", alpha=0.2, linewidth=0.7, zorder=1)
        means, lows, highs = [], [], []
        for alpha in ALPHAS:
            record = group_summary[(group, alpha)]
            means.append(100 * float(record["mean_beard_fraction_image"]))
            lows.append(100 * float(record["mean_ci95_low_percentile_bootstrap"]))
            highs.append(100 * float(record["mean_ci95_high_percentile_bootstrap"]))
        gender = group.rsplit("_", 1)[-1]
        color = color_by_gender[gender]
        ax.errorbar(x, means, yerr=[np.array(means)-np.array(lows), np.array(highs)-np.array(means)],
                    color=color, marker="o", markersize=4.5, capsize=2.5, linewidth=1.7, zorder=3)
        ax.set_title(group.replace("_", " ").title(), fontsize=10, pad=5)
        ax.set_xticks(x, [f"{alpha:+d}" for alpha in ALPHAS])
        ax.grid(axis="y", color="#dddddd", linewidth=0.6)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=8)
    for ax in axes.flat[len(groups):]:
        ax.set_visible(False)
    fig.supxlabel("SAE multiplier α", fontsize=10)
    fig.supylabel("Predicted Beard-class area (% of full image)", fontsize=10)
    fig.suptitle(f"Feature 4228 · Beard-class predictions across {len(groups)} prompt groups", fontsize=13, y=0.995)
    legend = [
        Line2D([0], [0], color="#7b7b7b", alpha=0.4, linewidth=1, label="Individual seed"),
        Line2D([0], [0], color="#2468a2", marker="o", linewidth=1.7, label="Men: mean, 95% bootstrap CI"),
        Line2D([0], [0], color="#aa3f81", marker="o", linewidth=1.7, label="Women: mean, 95% bootstrap CI"),
    ]
    fig.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, 0.977), ncol=3, frameon=False, fontsize=8)
    fig.tight_layout(rect=(0.03, 0.025, 1, 0.955))
    suffix = "all_groups" if len(groups) > 2 else "by_multiplier"
    fig.savefig(args.results_dir / f"beard_area_{suffix}.png", dpi=260, bbox_inches="tight")
    fig.savefig(args.results_dir / f"beard_area_{suffix}.pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"Saved plots for {len(groups)} groups to {args.results_dir}")


if __name__ == "__main__":
    main()
