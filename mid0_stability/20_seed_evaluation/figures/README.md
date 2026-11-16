# Fine-tuned mid.0 context-stability visualizations

Generated exclusively from the saved CSVs in `combined20_results`; no images generated, diffusion replayed, detector run, or old-environment sweeps pooled. Checkpoint SHA-256: `cbb3a0a2d0c43c822c7ba97a494de38ae56ea25401a8d31484ffa32e7cc329a6`. All 69,600 saved conditions are accounted for; 877 failed detections remain in their denominators. Missing or duplicate conditions and missing detection flags cause an explicit error, rather than an inferred value or silent exclusion. Full audit: [audit.json](audit.json).

## Cohorts and uncertainty

- **all**: every saved condition.
- **active**: initially_active is True.
- **active baseline detected**: initially_active AND baseline_detected are True.

Each feature–group–alpha point reports n independent seeds, k detections, k/n, and a pointwise 95% Wilson interval, exactly matching the existing category-level summary. These intervals are descriptive; they are not simultaneous bounds or a repeated-measures hypothesis test. No independence is claimed between alphas/features or prompt groups sharing a noise seed. Saved pooled ALL rows are also audited against the CSV; they are not plotted here.

The default insufficient-observation flag is n < 5, an explicit exploratory display rule rather than a power calculation. Low-n data remain displayed with †/× or hatching; n=0 has a missing rate/interval and ∅. Even n=5 with 5/5 detections has a wide interval and does not establish 95% population validity. With only 20 seed values, interaction-model and demographic-vulnerability claims are unsupported by these figures alone.

## Figures

Each of the 94 figures has a PNG at 300 dpi, a vector PDF with embedded fonts, and a same-stem CSV containing its aggregated plotting data (including n, k, confidence limits, and low-n flags).

1. **heatmaps/alpha_*.png**: rows are the ten fixed feature IDs in rank order, columns are twelve demographic prompt groups. Selected saved alphas: [-100, -70, -40, -20, 1, 20, 40, 70, 100]. For each cohort, paired panels show detection rate and Wilson interval width, both with fixed 0–1 color scales. Rate cells print percentage and n. Grey missing cells are not zeros.
2. **heatmaps/crossing_brackets_*.png**: separate negative reversal and positive amplification branches, per cohort. Cells print last passing → first failing sampled alpha under the saved exploratory 0.95 detection criterion. NR means not reached, B means baseline already below criterion, ∅ unavailable, † low n, and * any nonmonotonic recovery. Low-n observed brackets are explicitly flagged, not established boundaries. No continuous interpolation or precise threshold is estimated. Alpha=0 ablation and 0<alpha<1 attenuation are excluded from these branch crossings, matching the old code. Confidence intervals for both bracket endpoints are in the figure CSVs.
3. **per_feature/**: ten figures, one per feature, with three cohort panels and twelve consistently colored prompt-group curves. Legends report n. Error bars and translucent bands show Wilson intervals. Symmetric-log alpha axes retain every saved grid point, including 0 and no-op 1; lines only connect sampled observations.
4. **per_category/**: twelve figures, one per prompt group, with the same cohort panels and ten consistently colored feature curves. Every plot uses identical alpha and detection axes.
5. **magnitude/**: for each feature, cohort, and measured metric, twelve prompt-group panels show median magnitude versus detection rate at each sampled alpha. The relative metric is the saved applied perturbation norm divided by original block norm; the absolute metric is saved delta_fro_applied. Negative reversal, positive amplification, and attenuation/ablation use consistent branch colors/styles. The alpha=1 baseline is present in the CSV but excluded from magnitude branch curves. Symmetric-log magnitude axes include zero and share the same metric-specific limits across all features, prompt groups, and cohorts. No magnitude bins, smoothers, or pooled repeated-image denominators are used. Magnitude medians summarize different seeds at the same alpha; they do not match individual magnitudes or control for confounding. Wilson bands quantify detection uncertainty, not uncertainty in median magnitude.

The original coefficient_bins.csv describes scaled coefficients, not actual perturbation norms. Its counts were audited against per_image.csv; it is not relabeled as a perturbation measurement.

## Data and reproducibility

[Aggregated detection data](aggregated_detection.csv), [crossing brackets](sampled_crossing_brackets.csv), and [insufficient-observation cells](insufficient_observations.csv) retain all cohorts, groups, and saved multipliers. Input hashes and dependency versions are in audit.json. Source script: ../code/plot_context_stability.py. Run:

```bash
python code/plot_context_stability.py --source data --output figures_v2
```

Existing output directories are refused. Existing report files are untouched. Exact multiplier grid: `[-100, -70, -50, -40, -30, -20, -15, -12, -10, -7, -5, -3, -2, -1, 0, 1, 2, 3, 5, 7, 10, 12, 15, 20, 30, 40, 50, 70, 100]`. The source experiment configuration preserves the checkpoint and feature IDs. MediaPipe landmark detection is not facial quality; prompt groups are prompt conditions, not inferred demographic identities. Human validation remains necessary.

## Gallery

### heatmaps

- [alpha_m020](heatmaps/alpha_m020.png) · [PDF](heatmaps/alpha_m020.pdf) · [data](heatmaps/alpha_m020.csv)
- [alpha_m040](heatmaps/alpha_m040.png) · [PDF](heatmaps/alpha_m040.pdf) · [data](heatmaps/alpha_m040.csv)
- [alpha_m070](heatmaps/alpha_m070.png) · [PDF](heatmaps/alpha_m070.pdf) · [data](heatmaps/alpha_m070.csv)
- [alpha_m100](heatmaps/alpha_m100.png) · [PDF](heatmaps/alpha_m100.pdf) · [data](heatmaps/alpha_m100.csv)
- [alpha_p001](heatmaps/alpha_p001.png) · [PDF](heatmaps/alpha_p001.pdf) · [data](heatmaps/alpha_p001.csv)
- [alpha_p020](heatmaps/alpha_p020.png) · [PDF](heatmaps/alpha_p020.pdf) · [data](heatmaps/alpha_p020.csv)
- [alpha_p040](heatmaps/alpha_p040.png) · [PDF](heatmaps/alpha_p040.pdf) · [data](heatmaps/alpha_p040.csv)
- [alpha_p070](heatmaps/alpha_p070.png) · [PDF](heatmaps/alpha_p070.pdf) · [data](heatmaps/alpha_p070.csv)
- [alpha_p100](heatmaps/alpha_p100.png) · [PDF](heatmaps/alpha_p100.pdf) · [data](heatmaps/alpha_p100.csv)
- [crossing_brackets_active](heatmaps/crossing_brackets_active.png) · [PDF](heatmaps/crossing_brackets_active.pdf) · [data](heatmaps/crossing_brackets_active.csv)
- [crossing_brackets_active_baseline_detected](heatmaps/crossing_brackets_active_baseline_detected.png) · [PDF](heatmaps/crossing_brackets_active_baseline_detected.pdf) · [data](heatmaps/crossing_brackets_active_baseline_detected.csv)
- [crossing_brackets_all](heatmaps/crossing_brackets_all.png) · [PDF](heatmaps/crossing_brackets_all.pdf) · [data](heatmaps/crossing_brackets_all.csv)

### per_feature

- [feature_1074](per_feature/feature_1074.png) · [PDF](per_feature/feature_1074.pdf) · [data](per_feature/feature_1074.csv)
- [feature_1650](per_feature/feature_1650.png) · [PDF](per_feature/feature_1650.pdf) · [data](per_feature/feature_1650.csv)
- [feature_2023](per_feature/feature_2023.png) · [PDF](per_feature/feature_2023.pdf) · [data](per_feature/feature_2023.csv)
- [feature_2361](per_feature/feature_2361.png) · [PDF](per_feature/feature_2361.pdf) · [data](per_feature/feature_2361.csv)
- [feature_4228](per_feature/feature_4228.png) · [PDF](per_feature/feature_4228.pdf) · [data](per_feature/feature_4228.csv)
- [feature_4338](per_feature/feature_4338.png) · [PDF](per_feature/feature_4338.pdf) · [data](per_feature/feature_4338.csv)
- [feature_4399](per_feature/feature_4399.png) · [PDF](per_feature/feature_4399.pdf) · [data](per_feature/feature_4399.csv)
- [feature_4554](per_feature/feature_4554.png) · [PDF](per_feature/feature_4554.pdf) · [data](per_feature/feature_4554.csv)
- [feature_4586](per_feature/feature_4586.png) · [PDF](per_feature/feature_4586.pdf) · [data](per_feature/feature_4586.csv)
- [feature_5094](per_feature/feature_5094.png) · [PDF](per_feature/feature_5094.pdf) · [data](per_feature/feature_5094.csv)

### per_category

- [category_black_man](per_category/category_black_man.png) · [PDF](per_category/category_black_man.pdf) · [data](per_category/category_black_man.csv)
- [category_black_woman](per_category/category_black_woman.png) · [PDF](per_category/category_black_woman.pdf) · [data](per_category/category_black_woman.csv)
- [category_east_asian_man](per_category/category_east_asian_man.png) · [PDF](per_category/category_east_asian_man.pdf) · [data](per_category/category_east_asian_man.csv)
- [category_east_asian_woman](per_category/category_east_asian_woman.png) · [PDF](per_category/category_east_asian_woman.pdf) · [data](per_category/category_east_asian_woman.csv)
- [category_hispanic_man](per_category/category_hispanic_man.png) · [PDF](per_category/category_hispanic_man.pdf) · [data](per_category/category_hispanic_man.csv)
- [category_hispanic_woman](per_category/category_hispanic_woman.png) · [PDF](per_category/category_hispanic_woman.pdf) · [data](per_category/category_hispanic_woman.csv)
- [category_indian_man](per_category/category_indian_man.png) · [PDF](per_category/category_indian_man.pdf) · [data](per_category/category_indian_man.csv)
- [category_indian_woman](per_category/category_indian_woman.png) · [PDF](per_category/category_indian_woman.pdf) · [data](per_category/category_indian_woman.csv)
- [category_middle_eastern_man](per_category/category_middle_eastern_man.png) · [PDF](per_category/category_middle_eastern_man.pdf) · [data](per_category/category_middle_eastern_man.csv)
- [category_middle_eastern_woman](per_category/category_middle_eastern_woman.png) · [PDF](per_category/category_middle_eastern_woman.pdf) · [data](per_category/category_middle_eastern_woman.csv)
- [category_white_man](per_category/category_white_man.png) · [PDF](per_category/category_white_man.pdf) · [data](per_category/category_white_man.csv)
- [category_white_woman](per_category/category_white_woman.png) · [PDF](per_category/category_white_woman.pdf) · [data](per_category/category_white_woman.csv)

### magnitude

- [feature_1074_median_delta_fro_applied_active](magnitude/feature_1074_median_delta_fro_applied_active.png) · [PDF](magnitude/feature_1074_median_delta_fro_applied_active.pdf) · [data](magnitude/feature_1074_median_delta_fro_applied_active.csv)
- [feature_1074_median_delta_fro_applied_active_baseline_detected](magnitude/feature_1074_median_delta_fro_applied_active_baseline_detected.png) · [PDF](magnitude/feature_1074_median_delta_fro_applied_active_baseline_detected.pdf) · [data](magnitude/feature_1074_median_delta_fro_applied_active_baseline_detected.csv)
- [feature_1074_median_delta_fro_applied_all](magnitude/feature_1074_median_delta_fro_applied_all.png) · [PDF](magnitude/feature_1074_median_delta_fro_applied_all.pdf) · [data](magnitude/feature_1074_median_delta_fro_applied_all.csv)
- [feature_1074_median_relative_delta_fro_active](magnitude/feature_1074_median_relative_delta_fro_active.png) · [PDF](magnitude/feature_1074_median_relative_delta_fro_active.pdf) · [data](magnitude/feature_1074_median_relative_delta_fro_active.csv)
- [feature_1074_median_relative_delta_fro_active_baseline_detected](magnitude/feature_1074_median_relative_delta_fro_active_baseline_detected.png) · [PDF](magnitude/feature_1074_median_relative_delta_fro_active_baseline_detected.pdf) · [data](magnitude/feature_1074_median_relative_delta_fro_active_baseline_detected.csv)
- [feature_1074_median_relative_delta_fro_all](magnitude/feature_1074_median_relative_delta_fro_all.png) · [PDF](magnitude/feature_1074_median_relative_delta_fro_all.pdf) · [data](magnitude/feature_1074_median_relative_delta_fro_all.csv)
- [feature_1650_median_delta_fro_applied_active](magnitude/feature_1650_median_delta_fro_applied_active.png) · [PDF](magnitude/feature_1650_median_delta_fro_applied_active.pdf) · [data](magnitude/feature_1650_median_delta_fro_applied_active.csv)
- [feature_1650_median_delta_fro_applied_active_baseline_detected](magnitude/feature_1650_median_delta_fro_applied_active_baseline_detected.png) · [PDF](magnitude/feature_1650_median_delta_fro_applied_active_baseline_detected.pdf) · [data](magnitude/feature_1650_median_delta_fro_applied_active_baseline_detected.csv)
- [feature_1650_median_delta_fro_applied_all](magnitude/feature_1650_median_delta_fro_applied_all.png) · [PDF](magnitude/feature_1650_median_delta_fro_applied_all.pdf) · [data](magnitude/feature_1650_median_delta_fro_applied_all.csv)
- [feature_1650_median_relative_delta_fro_active](magnitude/feature_1650_median_relative_delta_fro_active.png) · [PDF](magnitude/feature_1650_median_relative_delta_fro_active.pdf) · [data](magnitude/feature_1650_median_relative_delta_fro_active.csv)
- [feature_1650_median_relative_delta_fro_active_baseline_detected](magnitude/feature_1650_median_relative_delta_fro_active_baseline_detected.png) · [PDF](magnitude/feature_1650_median_relative_delta_fro_active_baseline_detected.pdf) · [data](magnitude/feature_1650_median_relative_delta_fro_active_baseline_detected.csv)
- [feature_1650_median_relative_delta_fro_all](magnitude/feature_1650_median_relative_delta_fro_all.png) · [PDF](magnitude/feature_1650_median_relative_delta_fro_all.pdf) · [data](magnitude/feature_1650_median_relative_delta_fro_all.csv)
- [feature_2023_median_delta_fro_applied_active](magnitude/feature_2023_median_delta_fro_applied_active.png) · [PDF](magnitude/feature_2023_median_delta_fro_applied_active.pdf) · [data](magnitude/feature_2023_median_delta_fro_applied_active.csv)
- [feature_2023_median_delta_fro_applied_active_baseline_detected](magnitude/feature_2023_median_delta_fro_applied_active_baseline_detected.png) · [PDF](magnitude/feature_2023_median_delta_fro_applied_active_baseline_detected.pdf) · [data](magnitude/feature_2023_median_delta_fro_applied_active_baseline_detected.csv)
- [feature_2023_median_delta_fro_applied_all](magnitude/feature_2023_median_delta_fro_applied_all.png) · [PDF](magnitude/feature_2023_median_delta_fro_applied_all.pdf) · [data](magnitude/feature_2023_median_delta_fro_applied_all.csv)
- [feature_2023_median_relative_delta_fro_active](magnitude/feature_2023_median_relative_delta_fro_active.png) · [PDF](magnitude/feature_2023_median_relative_delta_fro_active.pdf) · [data](magnitude/feature_2023_median_relative_delta_fro_active.csv)
- [feature_2023_median_relative_delta_fro_active_baseline_detected](magnitude/feature_2023_median_relative_delta_fro_active_baseline_detected.png) · [PDF](magnitude/feature_2023_median_relative_delta_fro_active_baseline_detected.pdf) · [data](magnitude/feature_2023_median_relative_delta_fro_active_baseline_detected.csv)
- [feature_2023_median_relative_delta_fro_all](magnitude/feature_2023_median_relative_delta_fro_all.png) · [PDF](magnitude/feature_2023_median_relative_delta_fro_all.pdf) · [data](magnitude/feature_2023_median_relative_delta_fro_all.csv)
- [feature_2361_median_delta_fro_applied_active](magnitude/feature_2361_median_delta_fro_applied_active.png) · [PDF](magnitude/feature_2361_median_delta_fro_applied_active.pdf) · [data](magnitude/feature_2361_median_delta_fro_applied_active.csv)
- [feature_2361_median_delta_fro_applied_active_baseline_detected](magnitude/feature_2361_median_delta_fro_applied_active_baseline_detected.png) · [PDF](magnitude/feature_2361_median_delta_fro_applied_active_baseline_detected.pdf) · [data](magnitude/feature_2361_median_delta_fro_applied_active_baseline_detected.csv)
- [feature_2361_median_delta_fro_applied_all](magnitude/feature_2361_median_delta_fro_applied_all.png) · [PDF](magnitude/feature_2361_median_delta_fro_applied_all.pdf) · [data](magnitude/feature_2361_median_delta_fro_applied_all.csv)
- [feature_2361_median_relative_delta_fro_active](magnitude/feature_2361_median_relative_delta_fro_active.png) · [PDF](magnitude/feature_2361_median_relative_delta_fro_active.pdf) · [data](magnitude/feature_2361_median_relative_delta_fro_active.csv)
- [feature_2361_median_relative_delta_fro_active_baseline_detected](magnitude/feature_2361_median_relative_delta_fro_active_baseline_detected.png) · [PDF](magnitude/feature_2361_median_relative_delta_fro_active_baseline_detected.pdf) · [data](magnitude/feature_2361_median_relative_delta_fro_active_baseline_detected.csv)
- [feature_2361_median_relative_delta_fro_all](magnitude/feature_2361_median_relative_delta_fro_all.png) · [PDF](magnitude/feature_2361_median_relative_delta_fro_all.pdf) · [data](magnitude/feature_2361_median_relative_delta_fro_all.csv)
- [feature_4228_median_delta_fro_applied_active](magnitude/feature_4228_median_delta_fro_applied_active.png) · [PDF](magnitude/feature_4228_median_delta_fro_applied_active.pdf) · [data](magnitude/feature_4228_median_delta_fro_applied_active.csv)
- [feature_4228_median_delta_fro_applied_active_baseline_detected](magnitude/feature_4228_median_delta_fro_applied_active_baseline_detected.png) · [PDF](magnitude/feature_4228_median_delta_fro_applied_active_baseline_detected.pdf) · [data](magnitude/feature_4228_median_delta_fro_applied_active_baseline_detected.csv)
- [feature_4228_median_delta_fro_applied_all](magnitude/feature_4228_median_delta_fro_applied_all.png) · [PDF](magnitude/feature_4228_median_delta_fro_applied_all.pdf) · [data](magnitude/feature_4228_median_delta_fro_applied_all.csv)
- [feature_4228_median_relative_delta_fro_active](magnitude/feature_4228_median_relative_delta_fro_active.png) · [PDF](magnitude/feature_4228_median_relative_delta_fro_active.pdf) · [data](magnitude/feature_4228_median_relative_delta_fro_active.csv)
- [feature_4228_median_relative_delta_fro_active_baseline_detected](magnitude/feature_4228_median_relative_delta_fro_active_baseline_detected.png) · [PDF](magnitude/feature_4228_median_relative_delta_fro_active_baseline_detected.pdf) · [data](magnitude/feature_4228_median_relative_delta_fro_active_baseline_detected.csv)
- [feature_4228_median_relative_delta_fro_all](magnitude/feature_4228_median_relative_delta_fro_all.png) · [PDF](magnitude/feature_4228_median_relative_delta_fro_all.pdf) · [data](magnitude/feature_4228_median_relative_delta_fro_all.csv)
- [feature_4338_median_delta_fro_applied_active](magnitude/feature_4338_median_delta_fro_applied_active.png) · [PDF](magnitude/feature_4338_median_delta_fro_applied_active.pdf) · [data](magnitude/feature_4338_median_delta_fro_applied_active.csv)
- [feature_4338_median_delta_fro_applied_active_baseline_detected](magnitude/feature_4338_median_delta_fro_applied_active_baseline_detected.png) · [PDF](magnitude/feature_4338_median_delta_fro_applied_active_baseline_detected.pdf) · [data](magnitude/feature_4338_median_delta_fro_applied_active_baseline_detected.csv)
- [feature_4338_median_delta_fro_applied_all](magnitude/feature_4338_median_delta_fro_applied_all.png) · [PDF](magnitude/feature_4338_median_delta_fro_applied_all.pdf) · [data](magnitude/feature_4338_median_delta_fro_applied_all.csv)
- [feature_4338_median_relative_delta_fro_active](magnitude/feature_4338_median_relative_delta_fro_active.png) · [PDF](magnitude/feature_4338_median_relative_delta_fro_active.pdf) · [data](magnitude/feature_4338_median_relative_delta_fro_active.csv)
- [feature_4338_median_relative_delta_fro_active_baseline_detected](magnitude/feature_4338_median_relative_delta_fro_active_baseline_detected.png) · [PDF](magnitude/feature_4338_median_relative_delta_fro_active_baseline_detected.pdf) · [data](magnitude/feature_4338_median_relative_delta_fro_active_baseline_detected.csv)
- [feature_4338_median_relative_delta_fro_all](magnitude/feature_4338_median_relative_delta_fro_all.png) · [PDF](magnitude/feature_4338_median_relative_delta_fro_all.pdf) · [data](magnitude/feature_4338_median_relative_delta_fro_all.csv)
- [feature_4399_median_delta_fro_applied_active](magnitude/feature_4399_median_delta_fro_applied_active.png) · [PDF](magnitude/feature_4399_median_delta_fro_applied_active.pdf) · [data](magnitude/feature_4399_median_delta_fro_applied_active.csv)
- [feature_4399_median_delta_fro_applied_active_baseline_detected](magnitude/feature_4399_median_delta_fro_applied_active_baseline_detected.png) · [PDF](magnitude/feature_4399_median_delta_fro_applied_active_baseline_detected.pdf) · [data](magnitude/feature_4399_median_delta_fro_applied_active_baseline_detected.csv)
- [feature_4399_median_delta_fro_applied_all](magnitude/feature_4399_median_delta_fro_applied_all.png) · [PDF](magnitude/feature_4399_median_delta_fro_applied_all.pdf) · [data](magnitude/feature_4399_median_delta_fro_applied_all.csv)
- [feature_4399_median_relative_delta_fro_active](magnitude/feature_4399_median_relative_delta_fro_active.png) · [PDF](magnitude/feature_4399_median_relative_delta_fro_active.pdf) · [data](magnitude/feature_4399_median_relative_delta_fro_active.csv)
- [feature_4399_median_relative_delta_fro_active_baseline_detected](magnitude/feature_4399_median_relative_delta_fro_active_baseline_detected.png) · [PDF](magnitude/feature_4399_median_relative_delta_fro_active_baseline_detected.pdf) · [data](magnitude/feature_4399_median_relative_delta_fro_active_baseline_detected.csv)
- [feature_4399_median_relative_delta_fro_all](magnitude/feature_4399_median_relative_delta_fro_all.png) · [PDF](magnitude/feature_4399_median_relative_delta_fro_all.pdf) · [data](magnitude/feature_4399_median_relative_delta_fro_all.csv)
- [feature_4554_median_delta_fro_applied_active](magnitude/feature_4554_median_delta_fro_applied_active.png) · [PDF](magnitude/feature_4554_median_delta_fro_applied_active.pdf) · [data](magnitude/feature_4554_median_delta_fro_applied_active.csv)
- [feature_4554_median_delta_fro_applied_active_baseline_detected](magnitude/feature_4554_median_delta_fro_applied_active_baseline_detected.png) · [PDF](magnitude/feature_4554_median_delta_fro_applied_active_baseline_detected.pdf) · [data](magnitude/feature_4554_median_delta_fro_applied_active_baseline_detected.csv)
- [feature_4554_median_delta_fro_applied_all](magnitude/feature_4554_median_delta_fro_applied_all.png) · [PDF](magnitude/feature_4554_median_delta_fro_applied_all.pdf) · [data](magnitude/feature_4554_median_delta_fro_applied_all.csv)
- [feature_4554_median_relative_delta_fro_active](magnitude/feature_4554_median_relative_delta_fro_active.png) · [PDF](magnitude/feature_4554_median_relative_delta_fro_active.pdf) · [data](magnitude/feature_4554_median_relative_delta_fro_active.csv)
- [feature_4554_median_relative_delta_fro_active_baseline_detected](magnitude/feature_4554_median_relative_delta_fro_active_baseline_detected.png) · [PDF](magnitude/feature_4554_median_relative_delta_fro_active_baseline_detected.pdf) · [data](magnitude/feature_4554_median_relative_delta_fro_active_baseline_detected.csv)
- [feature_4554_median_relative_delta_fro_all](magnitude/feature_4554_median_relative_delta_fro_all.png) · [PDF](magnitude/feature_4554_median_relative_delta_fro_all.pdf) · [data](magnitude/feature_4554_median_relative_delta_fro_all.csv)
- [feature_4586_median_delta_fro_applied_active](magnitude/feature_4586_median_delta_fro_applied_active.png) · [PDF](magnitude/feature_4586_median_delta_fro_applied_active.pdf) · [data](magnitude/feature_4586_median_delta_fro_applied_active.csv)
- [feature_4586_median_delta_fro_applied_active_baseline_detected](magnitude/feature_4586_median_delta_fro_applied_active_baseline_detected.png) · [PDF](magnitude/feature_4586_median_delta_fro_applied_active_baseline_detected.pdf) · [data](magnitude/feature_4586_median_delta_fro_applied_active_baseline_detected.csv)
- [feature_4586_median_delta_fro_applied_all](magnitude/feature_4586_median_delta_fro_applied_all.png) · [PDF](magnitude/feature_4586_median_delta_fro_applied_all.pdf) · [data](magnitude/feature_4586_median_delta_fro_applied_all.csv)
- [feature_4586_median_relative_delta_fro_active](magnitude/feature_4586_median_relative_delta_fro_active.png) · [PDF](magnitude/feature_4586_median_relative_delta_fro_active.pdf) · [data](magnitude/feature_4586_median_relative_delta_fro_active.csv)
- [feature_4586_median_relative_delta_fro_active_baseline_detected](magnitude/feature_4586_median_relative_delta_fro_active_baseline_detected.png) · [PDF](magnitude/feature_4586_median_relative_delta_fro_active_baseline_detected.pdf) · [data](magnitude/feature_4586_median_relative_delta_fro_active_baseline_detected.csv)
- [feature_4586_median_relative_delta_fro_all](magnitude/feature_4586_median_relative_delta_fro_all.png) · [PDF](magnitude/feature_4586_median_relative_delta_fro_all.pdf) · [data](magnitude/feature_4586_median_relative_delta_fro_all.csv)
- [feature_5094_median_delta_fro_applied_active](magnitude/feature_5094_median_delta_fro_applied_active.png) · [PDF](magnitude/feature_5094_median_delta_fro_applied_active.pdf) · [data](magnitude/feature_5094_median_delta_fro_applied_active.csv)
- [feature_5094_median_delta_fro_applied_active_baseline_detected](magnitude/feature_5094_median_delta_fro_applied_active_baseline_detected.png) · [PDF](magnitude/feature_5094_median_delta_fro_applied_active_baseline_detected.pdf) · [data](magnitude/feature_5094_median_delta_fro_applied_active_baseline_detected.csv)
- [feature_5094_median_delta_fro_applied_all](magnitude/feature_5094_median_delta_fro_applied_all.png) · [PDF](magnitude/feature_5094_median_delta_fro_applied_all.pdf) · [data](magnitude/feature_5094_median_delta_fro_applied_all.csv)
- [feature_5094_median_relative_delta_fro_active](magnitude/feature_5094_median_relative_delta_fro_active.png) · [PDF](magnitude/feature_5094_median_relative_delta_fro_active.pdf) · [data](magnitude/feature_5094_median_relative_delta_fro_active.csv)
- [feature_5094_median_relative_delta_fro_active_baseline_detected](magnitude/feature_5094_median_relative_delta_fro_active_baseline_detected.png) · [PDF](magnitude/feature_5094_median_relative_delta_fro_active_baseline_detected.pdf) · [data](magnitude/feature_5094_median_relative_delta_fro_active_baseline_detected.csv)
- [feature_5094_median_relative_delta_fro_all](magnitude/feature_5094_median_relative_delta_fro_all.png) · [PDF](magnitude/feature_5094_median_relative_delta_fro_all.pdf) · [data](magnitude/feature_5094_median_relative_delta_fro_all.csv)
