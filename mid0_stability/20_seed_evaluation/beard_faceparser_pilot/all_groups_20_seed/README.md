# Beard-class results across all prompt groups

**[Browse the compact 3×3 overlay pages](contact_sheets_3x3/README.md)** — three seeds per image, seven pages per group. [Indian-man gallery](contact_sheets_3x3/indian_man/README.md). Original long strips are preserved.

FaceParsing raw class 14 (listed as Beard in the model README) was evaluated on the existing canonical 512×512 Feature 4228 sweep images: 12 prompt groups × 20 seeds (30–49) × α ∈ {−7, +1, +7} = 720 images. All source conditions and files were checked. No diffusion model was run. The earlier Indian-man and Middle-Eastern-man results are reused from the full-resolution 20-seed analysis, not rerun from the smaller-crop pilot.

## Mean predicted Beard-class area

Percentage of full image; 95% percentile-bootstrap CI across 20 seeds.

| Prompt group | α = −7 | α = +1 | α = +7 |
|---|---:|---:|---:|
| Black Man | 0.36 [0.16, 0.61] | 0.49 [0.21, 0.82] | 0.71 [0.28, 1.23] |
| Black Woman | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| East Asian Man | 0.60 [0.42, 0.79] | 0.59 [0.41, 0.77] | 0.58 [0.41, 0.75] |
| East Asian Woman | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| Hispanic Man | 2.57 [2.14, 3.03] | 2.65 [2.17, 3.13] | 2.90 [2.28, 3.61] |
| Hispanic Woman | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| Indian Man | 1.87 [1.52, 2.24] | 3.94 [2.99, 5.05] | 7.96 [6.17, 9.87] |
| Indian Woman | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| Middle Eastern Man | 8.72 [7.90, 9.57] | 11.89 [10.40, 13.39] | 17.57 [15.49, 19.54] |
| Middle Eastern Woman | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| White Man | 0.05 [0.02, 0.09] | 0.08 [0.03, 0.15] | 0.27 [0.07, 0.52] |
| White Woman | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

## Paired changes versus α = +1

Mean paired change in percentage points; 95% percentile-bootstrap CI across seeds. Parentheses give seeds with a positive change.

| Prompt group | α = −7 vs +1 | α = +7 vs +1 |
|---|---:|---:|
| Black Man | -0.12 [-0.30, +0.03] (5/20 positive) | +0.23 [+0.01, +0.49] (10/20 positive) |
| Black Woman | +0.00 [+0.00, +0.00] (0/20 positive) | +0.00 [+0.00, +0.00] (0/20 positive) |
| East Asian Man | +0.01 [-0.01, +0.04] (6/20 positive) | -0.01 [-0.06, +0.02] (5/20 positive) |
| East Asian Woman | +0.00 [+0.00, +0.00] (0/20 positive) | +0.00 [+0.00, +0.00] (0/20 positive) |
| Hispanic Man | -0.07 [-0.17, +0.01] (7/20 positive) | +0.25 [+0.04, +0.54] (11/20 positive) |
| Hispanic Woman | +0.00 [+0.00, +0.00] (0/20 positive) | +0.00 [+0.00, +0.00] (0/20 positive) |
| Indian Man | -2.07 [-3.03, -1.23] (1/20 positive) | +4.02 [+2.77, +5.36] (18/20 positive) |
| Indian Woman | +0.00 [+0.00, +0.00] (1/20 positive) | +0.00 [+0.00, +0.00] (0/20 positive) |
| Middle Eastern Man | -3.17 [-3.97, -2.39] (0/20 positive) | +5.68 [+4.72, +6.61] (20/20 positive) |
| Middle Eastern Woman | +0.00 [+0.00, +0.00] (0/20 positive) | +0.00 [+0.00, +0.00] (0/20 positive) |
| White Man | -0.03 [-0.08, +0.00] (5/20 positive) | +0.18 [+0.01, +0.43] (8/20 positive) |
| White Woman | +0.00 [+0.00, +0.00] (0/20 positive) | +0.00 [+0.00, +0.00] (0/20 positive) |

## Files

- `contact_sheets/`: all 12 groups, each sheet arranged by 20 seeds and three multipliers; magenta is the predicted class-14 region.
- Individual masks are not duplicated in this repository; the twelve contact sheets show the predictions overlaid on each input image.
- `beard_class_metrics.csv`: all 720 per-image predictions and class pixel counts.
- `input_manifest.csv`: source identities, conditions, and SHA-256 hashes; source paths are portable run-relative paths.
- `paired_changes.csv` and `paired_summary.csv`: within-seed comparisons to α = +1.
- `group_alpha_summary.csv`: per-group/multiplier means and seed-bootstrap intervals.
- `run_metadata.json`: checkpoint/layer/run provenance.

## Interpretation

The women’s prompts provide a useful negative-control check, while the four additional men’s groups test how the measured response varies beyond the original Indian-man and Middle-Eastern-man focus. East Asian men show little paired change at either intervention compared with α=+1 in this parser output. These are measurements of an unvalidated parser output, not verified beard area. The class-14 label is defined in the parser README, but the repository visualization helper has a conflicting class list; overlays also show some edge spillover. Seed-level bootstrap intervals do not account for parser error. No claims about facial quality or human-perceived beard area should be made without a beard-mask validation set.

## Reproduction

The saved analysis used the existing `mid0_stability/combined20_results/per_image.csv` images; it did not run diffusion. `input_manifest.csv` lists the 720 source image paths relative to the existing Feature 4228 sweep and records their SHA-256 hashes. The model weights are not included. To rerun parsing on the research host, install the dependencies documented by the FaceParsing model repository and run:

```bash
python code/run_beard_class_faceparser_20seed.py \
  --source-csv /path/to/combined20_results/per_image.csv \
  --repo /path/to/face-parsing-beard-class \
  --output-dir /path/to/new_all_groups_output \
  --groups black_man black_woman east_asian_man east_asian_woman \
    hispanic_man hispanic_woman indian_man indian_woman \
    middle_eastern_man middle_eastern_woman white_man white_woman
python code/plot_beard_class_all_groups.py --results-dir /path/to/new_all_groups_output
```

The runner checks for the complete group × seed × multiplier grid and verifies the source images before inference. It refuses to overwrite a nonempty output directory. `code/run_beard_class_faceparser.py` contains the shared model-loading and preprocessing helpers. The checked-in PNG/PDF and CSV files are the outputs used for this report.
