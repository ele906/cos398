# Feature 3884: biased dataset alpha sweep

This run uses the original biased race/gender dataset and its saved simple prompts (`a picture of a {race} {gender}`). It covers all 12 prompt groups, using seeds 0–19 from each group (20 images per group; 240 source images total).

For each source image, the intervention uses alpha values `-75, -50, -30, -20, -15, -10, -7, -5, -3, 0, 3, 5, 7, 10, 15, 20, 30, 50, 75`. Each 5×4 grid contains the original image followed by all 19 alpha variants in ascending order. Alpha `+1` is the no-op reference and is not included in the grid.

## Preliminary visual note

In a spot-check of alpha `+75` across seeds 0–19, U.S. flag backgrounds recur in many White men, Hispanic men, and Hispanic women outputs. The seed 000 source portraits do not show the same flags. This suggests feature 3884 may be associated with U.S.-flag imagery in these generated portraits; calling it “patriotic” is an interpretation, and the strongest settings also distort some images.

## Results by race and gender

Each group has its own folder with an activation graph, 20 plain-image sheets, and signed-coefficient, post-re-encoded-activation, and intervention-footprint overlays for all 20 seeds. The graph is shown smaller; image and overlay grids are shown larger in each group report.

| Group | Report |
|---|---|
| Black men | [black_man](black_man/README.md) |
| Black women | [black_woman](black_woman/README.md) |
| White men | [white_man](white_man/README.md) |
| White women | [white_woman](white_woman/README.md) |
| East Asian men | [east_asian_man](east_asian_man/README.md) |
| East Asian women | [east_asian_woman](east_asian_woman/README.md) |
| Middle Eastern men | [middle_eastern_man](middle_eastern_man/README.md) |
| Middle Eastern women | [middle_eastern_woman](middle_eastern_woman/README.md) |
| Indian men | [indian_man](indian_man/README.md) |
| Indian women | [indian_woman](indian_woman/README.md) |
| Hispanic men | [hispanic_man](hispanic_man/README.md) |
| Hispanic women | [hispanic_woman](hispanic_woman/README.md) |

The combined [mean metrics by group and alpha](mean_metrics_by_group_alpha.csv) has 228 rows, one for each group/alpha pair. It reports the mean post-re-encoded activation of feature 3884, active spatial fraction, mean pixel MAE versus the source image (RGB 0–255), and coefficient-change magnitudes, averaged across 20 seeds. The full [per-image metrics](metrics.csv), [activation maps](activation_maps.npz), [visual review template](visual_review.csv), and [run settings](settings.json) are also included. Each group README contains its own 19-row metric table. Coefficient overlays use transparent zero, green through blue to purple for negative values, and yellow through orange to red for positive values. Each tile is normalized individually for visibility, so use metrics and graphs to compare magnitudes.

The runnable [notebook](feature_3884_biased_dataset_alpha_sweep.ipynb), [sweep script](run_feature_3884_biased_sweep.py), [renderer](render_feature_3884.py), and [metric report generator](summarize_feature_3884.py) are also available in the [SAE demo notebook repository](https://github.com/ele906/sae-demo-notebooks/tree/main/sae-activation/activation_tuning).
