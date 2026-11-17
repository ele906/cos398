#!/usr/bin/env python3
"""Create publication-style curves from the saved 20-seed Beard-class CSVs."""

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


GROUPS = ("indian_man", "middle_eastern_man")
ALPHAS = (-7, 1, 7)


def read_rows(path: Path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=Path("/n/fs/goose/experiments/mid0_sae_selectivity/faceparser_beard_20seed"))
    args = parser.parse_args()
    metrics = read_rows(args.results_dir / "beard_class_metrics.csv")
    summaries = read_rows(args.results_dir / "group_alpha_summary.csv")

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.6), sharey=True)
    x = np.arange(len(ALPHAS))
    colors = {"indian_man": "#2468a2", "middle_eastern_man": "#aa3f81"}
    for ax, group in zip(axes, GROUPS):
        group_rows = [r for r in metrics if r["prompt_group"] == group]
        for seed in sorted({int(r["seed"]) for r in group_rows}):
            by_alpha = {int(float(r["alpha"])): float(r["beard_fraction_image"]) * 100 for r in group_rows if int(r["seed"]) == seed}
            ax.plot(x, [by_alpha[a] for a in ALPHAS], color="#777777", alpha=0.22, linewidth=0.8, zorder=1)
        summary_group = {int(float(r["alpha"])): r for r in summaries if r["prompt_group"] == group}
        means = np.array([float(summary_group[a]["mean_beard_fraction_image"]) * 100 for a in ALPHAS])
        low = np.array([float(summary_group[a]["mean_ci95_low_percentile_bootstrap"]) * 100 for a in ALPHAS])
        high = np.array([float(summary_group[a]["mean_ci95_high_percentile_bootstrap"]) * 100 for a in ALPHAS])
        ax.errorbar(x, means, yerr=[means - low, high - means], color=colors[group], marker="o", markersize=6, capsize=4, linewidth=2.2, label="Mean ± 95% seed bootstrap CI", zorder=3)
        ax.set_title(group.replace("_", " ").title(), fontsize=12)
        ax.set_xticks(x, [f"{a:+d}" for a in ALPHAS])
        ax.set_xlabel("SAE multiplier α")
        ax.grid(axis="y", color="#d9d9d9", linewidth=0.7)
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(frameon=False, fontsize=8, loc="best")
    axes[0].set_ylabel("Predicted Beard-class area (% of image)")
    fig.suptitle("Feature 4228 · Beard-class area across 20 saved seeds per group", fontsize=14, y=1.02)
    fig.tight_layout()
    fig.savefig(args.results_dir / "beard_area_by_multiplier.png", dpi=300, bbox_inches="tight")
    fig.savefig(args.results_dir / "beard_area_by_multiplier.pdf", bbox_inches="tight")
    plt.close(fig)
    print(f"Saved PNG and PDF curves under {args.results_dir}")


if __name__ == "__main__":
    main()
