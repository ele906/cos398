#!/usr/bin/env python3
"""Apply the published FaceParsing Beard class to saved Feature 4228 images.

Uses only existing images from the combined 20-seed evaluation CSV. No diffusion
model is loaded or run. The complete 2 groups x 20 seeds x 3 alpha grid is
required; missing or duplicate conditions are errors, not silently omitted.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_beard_class_faceparser as parser_helpers


SOURCE_CSV = Path("/n/fs/goose/layers/mid0_stability/combined20_results/per_image.csv")
DEFAULT_REPO = Path("/n/fs/goose/face-parsing-beard-class")
DEFAULT_OUT = Path("/n/fs/goose/experiments/mid0_sae_selectivity/faceparser_beard_20seed")
GROUPS = ("indian_man", "middle_eastern_man")
ALL_GROUPS = (
    "black_man", "black_woman", "east_asian_man", "east_asian_woman",
    "hispanic_man", "hispanic_woman", "indian_man", "indian_woman",
    "middle_eastern_man", "middle_eastern_woman", "white_man", "white_woman",
)
SEEDS = tuple(range(30, 50))
ALPHAS = (-7.0, 1.0, 7.0)
FEATURE = "4228"
CLASS_ID = 14


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def alpha_label(alpha: float) -> str:
    value = int(alpha)
    return f"m{abs(value)}" if value < 0 else f"p{value}"


def load_manifest(source_csv: Path, groups: tuple[str, ...] = GROUPS) -> list[dict[str, object]]:
    with source_csv.open(newline="") as handle:
        source_rows = list(csv.DictReader(handle))
    selected = [
        row for row in source_rows
        if row["feature"] == FEATURE
        and row["group"] in groups
        and int(row["seed"]) in SEEDS
        and float(row["alpha"]) in ALPHAS
    ]
    expected = len(groups) * len(SEEDS) * len(ALPHAS)
    keys = [(r["group"], int(r["seed"]), float(r["alpha"])) for r in selected]
    counts = Counter(keys)
    duplicates = [key for key, count in counts.items() if count != 1]
    expected_keys = {
        (group, seed, alpha)
        for group in groups for seed in SEEDS for alpha in ALPHAS
    }
    missing_keys = sorted(expected_keys - set(keys))
    if len(selected) != expected or duplicates or missing_keys:
        raise RuntimeError(
            f"Incomplete/duplicate source grid: rows={len(selected)} expected={expected}; "
            f"duplicates={duplicates[:5]}, missing={missing_keys[:5]}"
        )

    records: list[dict[str, object]] = []
    for row in selected:
        image_path = Path(row["image"])
        if not image_path.is_file():
            raise FileNotFoundError(
                f"Source evaluation row exists but its image is missing: {image_path}"
            )
        with Image.open(image_path) as image:
            width, height = image.size
        if (width, height) != (512, 512):
            raise ValueError(f"Expected canonical 512x512 sweep image, got {(width, height)}: {image_path}")
        record: dict[str, object] = {
            "feature": int(row["feature"]),
            "prompt_group": row["group"],
            "seed": int(row["seed"]),
            "alpha": float(row["alpha"]),
            "alpha_label": alpha_label(float(row["alpha"])),
            "image": image_path.name,
            "source_path": str(image_path),
            "source_sha256": sha256_file(image_path),
            "source_face_detected": row.get("face_detected", ""),
            "source_baseline_detected": row.get("baseline_detected", ""),
            "source_initially_active": row.get("initially_active", ""),
            "source_relative_delta_fro": row.get("relative_delta_fro", ""),
        }
        records.append(record)
    records.sort(key=lambda r: (str(r["prompt_group"]), int(r["seed"]), float(r["alpha"])))
    return records


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def contact_sheet(rows: list[dict[str, object]], out: Path, group: str) -> None:
    group_rows = [r for r in rows if r["prompt_group"] == group]
    tile = 256
    label_h = 28
    sheet = Image.new("RGB", (3 * tile, len(SEEDS) * (tile + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for row in group_rows:
        col = ALPHAS.index(float(row["alpha"]))
        yrow = int(row["seed"]) - SEEDS[0]
        x, y = col * tile, yrow * (tile + label_h)
        source = Image.open(str(row["source_path"])).convert("RGB").resize((tile, tile), Image.Resampling.BILINEAR)
        source = Image.open(str(row["source_path"])).convert("RGB")
        binary = np.asarray(Image.open(out / "masks" / f"{row['output_stem']}_class14_beard.png")) > 0
        class_mask = np.where(binary, CLASS_ID, 0).astype(np.uint8)
        overlay = parser_helpers.make_overlay(source, class_mask).resize((tile, tile), Image.Resampling.BILINEAR)
        draw.text((x + 4, y + 5), f"seed {row['seed']}   α={row['alpha']:g}", fill="black", font=font)
        sheet.paste(overlay, (x, y + label_h))
    sheet.save(out / "contact_sheets" / f"{group}.jpg", quality=94)


def make_paired_summaries(rows: list[dict[str, object]], out: Path, groups: tuple[str, ...] = GROUPS) -> None:
    indexed = {(r["prompt_group"], int(r["seed"]), float(r["alpha"])): r for r in rows}
    paired: list[dict[str, object]] = []
    for group in groups:
        for seed in SEEDS:
            control = indexed[(group, seed, 1.0)]
            for alpha in (-7.0, 7.0):
                treatment = indexed[(group, seed, alpha)]
                paired.append({
                    "prompt_group": group,
                    "seed": seed,
                    "alpha": int(alpha),
                    "control_alpha": 1,
                    "beard_fraction_image_control": control["beard_fraction_image"],
                    "beard_fraction_image_treatment": treatment["beard_fraction_image"],
                    "paired_delta_beard_fraction_image": float(treatment["beard_fraction_image"]) - float(control["beard_fraction_image"]),
                    "beard_fraction_face_classes_control": control["beard_fraction_face_classes_1_to_14"],
                    "beard_fraction_face_classes_treatment": treatment["beard_fraction_face_classes_1_to_14"],
                    "paired_delta_beard_fraction_face_classes": float(treatment["beard_fraction_face_classes_1_to_14"]) - float(control["beard_fraction_face_classes_1_to_14"]),
                })
    write_csv(out / "paired_changes.csv", paired)

    paired_rng = np.random.default_rng(4229)
    paired_summary: list[dict[str, object]] = []
    for group in groups:
        for alpha in (-7.0, 7.0):
            values = np.array([
                float(r["paired_delta_beard_fraction_image"])
                for r in paired
                if r["prompt_group"] == group and int(r["alpha"]) == int(alpha)
            ])
            boot = np.array([
                paired_rng.choice(values, size=len(values), replace=True).mean()
                for _ in range(10000)
            ])
            paired_summary.append({
                "prompt_group": group,
                "alpha": int(alpha),
                "control_alpha": 1,
                "n_paired_seeds": len(values),
                "mean_paired_delta_beard_fraction_image": values.mean(),
                "mean_delta_ci95_low_percentile_bootstrap": np.quantile(boot, 0.025),
                "mean_delta_ci95_high_percentile_bootstrap": np.quantile(boot, 0.975),
                "median_paired_delta_beard_fraction_image": np.median(values),
                "seeds_with_positive_delta": int((values > 0).sum()),
                "seeds_with_negative_delta": int((values < 0).sum()),
            })
    write_csv(out / "paired_summary.csv", paired_summary)

    rng = np.random.default_rng(4228)
    summary: list[dict[str, object]] = []
    for group in groups:
        for alpha in ALPHAS:
            values = np.array([
                float(indexed[(group, seed, alpha)]["beard_fraction_image"])
                for seed in SEEDS
            ])
            boot = np.array([
                rng.choice(values, size=len(values), replace=True).mean()
                for _ in range(10000)
            ])
            summary.append({
                "prompt_group": group,
                "alpha": int(alpha),
                "n_seeds": len(values),
                "mean_beard_fraction_image": values.mean(),
                "mean_ci95_low_percentile_bootstrap": np.quantile(boot, 0.025),
                "mean_ci95_high_percentile_bootstrap": np.quantile(boot, 0.975),
                "median_beard_fraction_image": np.median(values),
                "sd_beard_fraction_image": values.std(ddof=1),
            })
    write_csv(out / "group_alpha_summary.csv", summary)



def main() -> None:
    argp = argparse.ArgumentParser()
    argp.add_argument("--source-csv", type=Path, default=SOURCE_CSV)
    argp.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    argp.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    argp.add_argument("--device", default="cuda:0" if torch.cuda.is_available() else "cpu")
    argp.add_argument("--groups", nargs="+", choices=ALL_GROUPS, default=list(GROUPS))
    argp.add_argument("--save-individual-overlays", action="store_true")
    args = argp.parse_args()
    groups = tuple(args.groups)
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        raise FileExistsError(f"Refusing to overwrite non-empty output directory: {args.output_dir}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "masks").mkdir()
    if args.save_individual_overlays:
        (args.output_dir / "overlays").mkdir()
    (args.output_dir / "contact_sheets").mkdir()

    records = load_manifest(args.source_csv, groups)
    print(f"Verified complete input grid: {len(records)} images from {args.source_csv}")
    manifest_rows = [{k: v for k, v in r.items() if k != "output_stem"} for r in records]
    write_csv(args.output_dir / "input_manifest.csv", manifest_rows)

    device = torch.device(args.device)
    model = parser_helpers.load_model(args.repo, device)
    results: list[dict[str, object]] = []
    for i, record in enumerate(records, 1):
        source = Image.open(str(record["source_path"])).convert("RGB")
        with torch.inference_mode():
            output = model(parser_helpers.preprocess(source, device))
            mask = output["probabilities"][0].argmax(dim=0).cpu().numpy().astype(np.uint8)
        counts = np.bincount(mask.ravel(), minlength=19)
        beard_pixels = int(counts[CLASS_ID])
        face_pixels = int(counts[1:15].sum())
        stem = f"{record['prompt_group']}__seed{int(record['seed']):03d}__alpha_{record['alpha_label']}"
        record["output_stem"] = stem
        Image.fromarray((mask == CLASS_ID).astype(np.uint8) * 255).save(
            args.output_dir / "masks" / f"{stem}_class14_beard.png"
        )
        if args.save_individual_overlays:
            parser_helpers.make_overlay(source, mask).save(
                args.output_dir / "overlays" / f"{stem}_class14_beard_overlay.png"
            )
        result = {
            **{k: v for k, v in record.items() if k != "output_stem"},
            "beard_class_id": CLASS_ID,
            "width": mask.shape[1],
            "height": mask.shape[0],
            "beard_pixels": beard_pixels,
            "image_pixels": int(mask.size),
            "beard_fraction_image": beard_pixels / int(mask.size),
            "face_classes_1_to_14_pixels": face_pixels,
            "beard_fraction_face_classes_1_to_14": beard_pixels / face_pixels if face_pixels else float("nan"),
        }
        result.update({f"class_{j}_pixels": int(n) for j, n in enumerate(counts)})
        results.append(result)
        if i == 1 or i % 10 == 0 or i == len(records):
            print(f"Completed {i}/{len(records)}: {stem}; Beard={100 * beard_pixels / mask.size:.2f}% image")

    write_csv(args.output_dir / "beard_class_metrics.csv", results)
    for group in groups:
        contact_sheet(records, args.output_dir, group)
    make_paired_summaries(results, args.output_dir, groups)
    metadata = {
        "feature": 4228,
        "layer": "unet.mid_block.attentions.0",
        "groups": groups,
        "seeds": SEEDS,
        "alphas": ALPHAS,
        "n_images": len(results),
        "source_csv": str(args.source_csv),
        "source_csv_sha256": sha256_file(args.source_csv),
        "no_diffusion_generation": True,
        "beard_class_id": CLASS_ID,
        "model": "jseobyun/FaceParsing decoder + official DINOv3 ViT-B/16 LVD-1689M",
    }
    import json
    (args.output_dir / "run_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    group_summary = list(csv.DictReader((args.output_dir / "group_alpha_summary.csv").open(newline="")))
    paired_summary = list(csv.DictReader((args.output_dir / "paired_summary.csv").open(newline="")))
    group_lookup = {(r["prompt_group"], int(float(r["alpha"]))): r for r in group_summary}
    paired_lookup = {(r["prompt_group"], int(float(r["alpha"]))): r for r in paired_summary}
    area_table = [
        "| Prompt group | α = −7 | α = +1 | α = +7 |",
        "|---|---:|---:|---:|",
    ]
    paired_table = [
        "| Prompt group | α = −7 vs +1 | α = +7 vs +1 |",
        "|---|---:|---:|",
    ]
    for group in groups:
        area_cells = []
        for alpha in ALPHAS:
            row = group_lookup[(group, int(alpha))]
            mean = 100 * float(row["mean_beard_fraction_image"])
            low = 100 * float(row["mean_ci95_low_percentile_bootstrap"])
            high = 100 * float(row["mean_ci95_high_percentile_bootstrap"])
            area_cells.append(f"{mean:.2f} [{low:.2f}, {high:.2f}]")
        area_table.append(f"| {group.replace('_', ' ').title()} | " + " | ".join(area_cells) + " |")
        paired_cells = []
        for alpha in (-7, 7):
            row = paired_lookup[(group, alpha)]
            mean = 100 * float(row["mean_paired_delta_beard_fraction_image"])
            low = 100 * float(row["mean_delta_ci95_low_percentile_bootstrap"])
            high = 100 * float(row["mean_delta_ci95_high_percentile_bootstrap"])
            positive = int(row["seeds_with_positive_delta"])
            paired_cells.append(f"{mean:+.2f} [{low:+.2f}, {high:+.2f}] pp ({positive}/20 increased)")
        paired_table.append(f"| {group.replace('_', ' ').title()} | " + " | ".join(paired_cells) + " |")
    (args.output_dir / "README.md").write_text(
        "# 20-seed Beard-class extension\n\n"
        f"FaceParsing class 14 was run on canonical existing 512×512 Feature 4228 images for {len(groups)} selected prompt group(s), seeds 30–49, at α = −7, +1, +7. The source grid was checked for all {len(records)} unique conditions and all source files were present before inference. No diffusion model was loaded or run.\n\n"
        "The earlier six-image pilot used smaller face crops; this run uses full-size canonical sweep images for every seed, including seed 30, so measurements are comparable across the 20 seeds. This new run does not overwrite the earlier pilot.\n\n"
        "## Results\n\n"
        "Mean predicted Beard-class area as a percentage of the full image (95% percentile-bootstrap CI across seeds):\n\n"
        + "\n".join(area_table) + "\n\n"
        "Paired seed-level mean area change versus α = +1, in percentage points (95% percentile-bootstrap CI):\n\n"
        + "\n".join(paired_table) + "\n\n"
        "These are consistent changes in the model's Beard-class predictions, not validated changes in true beard area.\n\n"
        "`input_manifest.csv` records every input path and SHA-256, along with source detector/activity fields. `beard_class_metrics.csv` records all class pixel counts and Beard-class area per image. `paired_changes.csv` contains seed-level paired deltas; `paired_summary.csv` gives their means, percentile-bootstrap intervals, and directional counts. `group_alpha_summary.csv` reports group/multiplier means, medians, SDs, and percentile bootstrap intervals across 20 seeds. `contact_sheets/` contains overlays arranged by seed and multiplier.\n\n"
        "Caution: these are unvalidated predictions from class index 14, identified as Beard in the model README. The model repository's visualization helper has a conflicting class list. Inspect masks and overlays; do not treat these measurements as ground truth or facial-quality judgments. Seed-level intervals do not validate the parser.\n"
    )
    print(f"Saved all outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
