# Feature 527 — biased dataset alpha sweep

Feature 527 ranked fourth in the biased dataset one-vs-many scan: Black women had mean spatial-max activation 58.09, versus 13.98 averaged across the other 11 groups (gap 44.11). This is a descriptive association, not an interpretation of the feature or evidence that changing it controls a particular attribute.

## Run design

- Dataset: original biased/simple-prompt portraits; prompt and seed replay from the saved manifest.
- Groups: all 12 race/gender categories; seeds 0–19 (20 source images per group).
- Alpha values: −120, −100, −75, −50, −30, −20, −15, −10, −7, −5, −3, 0, 3, 5, 7, 10, 15, 20, 30, 50, 75, 100, 120.
- Per seed: original plus 23 alpha variants in ascending alpha order, arranged in a 4×6 grid.
- Each group has plain-image, signed-coefficient, post-re-encoded activation, and intervention-footprint grids.
- Pixel MAE is mean absolute RGB pixel difference from the original on a 0–255 scale; tables average across the 20 source seeds.
- Signed coefficient overlays use translucent colors: green near-zero negative → blue → purple for stronger negative; yellow near-zero positive → orange → red for stronger positive; zero is transparent.

## Reports by group

| Group | Per-alpha table and representative grids | All post-activation grids |
|---|---|---|
| Black Man | [Black Man feature summary](black_man/feature_summary.md) | [20-seed gallery](black_man/post_activation_overlays.md) |
| Black Woman | [Black Woman feature summary](black_woman/feature_summary.md) | [20-seed gallery](black_woman/post_activation_overlays.md) |
| White Man | [White Man feature summary](white_man/feature_summary.md) | [20-seed gallery](white_man/post_activation_overlays.md) |
| White Woman | [White Woman feature summary](white_woman/feature_summary.md) | [20-seed gallery](white_woman/post_activation_overlays.md) |
| East Asian Man | [East Asian Man feature summary](east_asian_man/feature_summary.md) | [20-seed gallery](east_asian_man/post_activation_overlays.md) |
| East Asian Woman | [East Asian Woman feature summary](east_asian_woman/feature_summary.md) | [20-seed gallery](east_asian_woman/post_activation_overlays.md) |
| Middle Eastern Man | [Middle Eastern Man feature summary](middle_eastern_man/feature_summary.md) | [20-seed gallery](middle_eastern_man/post_activation_overlays.md) |
| Middle Eastern Woman | [Middle Eastern Woman feature summary](middle_eastern_woman/feature_summary.md) | [20-seed gallery](middle_eastern_woman/post_activation_overlays.md) |
| Indian Man | [Indian Man feature summary](indian_man/feature_summary.md) | [20-seed gallery](indian_man/post_activation_overlays.md) |
| Indian Woman | [Indian Woman feature summary](indian_woman/feature_summary.md) | [20-seed gallery](indian_woman/post_activation_overlays.md) |
| Hispanic Man | [Hispanic Man feature summary](hispanic_man/feature_summary.md) | [20-seed gallery](hispanic_man/post_activation_overlays.md) |
| Hispanic Woman | [Hispanic Woman feature summary](hispanic_woman/feature_summary.md) | [20-seed gallery](hispanic_woman/post_activation_overlays.md) |

## Files

- [Mean metrics by group and alpha](mean_metrics_by_group_alpha.csv) (276 rows).
- [Run settings](settings.json).
- Runnable [notebook](feature_527_biased_dataset_alpha_sweep.ipynb), [generation script](run_feature_527_biased_sweep.py), [renderer](render_feature_527.py), and [summary generator](summarize_feature_527.py).
