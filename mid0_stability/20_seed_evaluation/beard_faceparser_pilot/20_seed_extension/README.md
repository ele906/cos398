# Beard-class results across 20 saved seeds

This extension runs FaceParsing output class 14 on the existing canonical 512 × 512 Feature 4228 images for `indian_man` and `middle_eastern_man`, seeds 30–49, and α ∈ {−7, +1, +7}. The full 120-condition grid was checked for duplicates and missing files before inference. **No diffusion images were generated.** Seed 30 was re-evaluated from the canonical sweep images because the earlier six-image pilot used smaller crops; this makes all 20 seeds comparable and leaves the earlier pilot untouched.

## Results

Mean predicted Beard-class area as a percentage of the full image (95% percentile-bootstrap CI across seeds):

| Prompt group | α = −7 | α = +1 | α = +7 |
|---|---:|---:|---:|
| Indian man | 1.87 [1.52, 2.24] | 3.94 [3.00, 5.03] | 7.96 [6.14, 9.82] |
| Middle-Eastern man | 8.72 [7.89, 9.55] | 11.89 [10.40, 13.41] | 17.57 [15.56, 19.51] |

Paired seed-level mean change versus α = +1, in percentage points (95% percentile-bootstrap CI):

| Prompt group | α = −7 vs +1 | α = +7 vs +1 |
|---|---:|---:|
| Indian man | −2.07 [−3.02, −1.22] | +4.02 [+2.78, +5.33] (18/20 seeds increased) |
| Middle-Eastern man | −3.17 [−3.99, −2.40] | +5.68 [+4.73, +6.63] (20/20 seeds increased) |

The parser’s predicted Beard-class area increases from α = +1 to +7 across nearly all seeds in both prompt groups. This is a consistent change in the model output, not yet a validated change in true beard area.

## Files

- `contact_sheets/`: one 20-row × 3-column overlay sheet per prompt group. Magenta marks the predicted Beard class.
- `masks/`: 120 full-resolution binary class-14 masks.
- `beard_class_metrics.csv`: per-image class pixel counts and predicted Beard area.
- `input_manifest.csv`: all source identities, condition metadata, and image SHA-256 hashes. Source paths are run-relative; the full source sweep is not duplicated here.
- `paired_changes.csv` and `paired_summary.csv`: seed-paired changes against α = +1 and bootstrap summaries.
- `group_alpha_summary.csv`: per-group, per-multiplier means, medians, SDs, and bootstrap intervals.
- `beard_area_by_multiplier.png` / `.pdf`: individual seed trajectories and group means with 95% seed-bootstrap intervals.
- `provenance.json`: feature/layer, source run, model and checkpoint hashes.
- `code/`: inference and plotting scripts.

## Interpretation and limitations

FaceParsing’s README identifies class index 14 as Beard. Its visualization helper lists a conflicting class order, so these masks use the raw class-14 output and the conflict is documented. Overlays look beard-like in many examples, with some edge spillover. The model has not been validated against human beard masks; area numbers are exploratory model measurements, not ground truth or a face-quality judgment. The seed bootstrap reflects variation across these generated seeds and does not account for parser error.

The source image conditions and SHA-256 hashes are preserved in `input_manifest.csv`. The contact sheets show all 120 predictions; full-resolution source images and model weights are not included in this extension. DINOv3 weights require accepting Meta’s DINOv3 license and are not redistributed here.

## Reproduce

Use the source evaluation CSV and its saved images, the parser and checkpoints described in the parent [`README.md`](../README.md), and the goose PyTorch environment. From the repository root:

```bash
PYTHONNOUSERSITE=1 /n/fs/goose/el8403/conda-envs/goose/bin/python \
  mid0_stability/20_seed_evaluation/beard_faceparser_pilot/20_seed_extension/code/run_beard_class_faceparser_20seed.py \
  --source-csv /n/fs/goose/layers/mid0_stability/combined20_results/per_image.csv \
  --repo /n/fs/goose/face-parsing-beard-class \
  --output-dir /tmp/faceparser_beard_20seed_rerun
```

The inference script requires the complete 120-image grid and refuses to overwrite a non-empty output directory. It never loads or calls the diffusion model. Generate the PNG/PDF summary using the base Python with Matplotlib:

```bash
PYTHONNOUSERSITE=1 /usr/local/anaconda3/2024.02/bin/python \
  mid0_stability/20_seed_evaluation/beard_faceparser_pilot/20_seed_extension/code/plot_beard_class_20seed.py \
  --results-dir /tmp/faceparser_beard_20seed_rerun
```
