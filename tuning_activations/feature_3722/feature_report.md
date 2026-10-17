# Feature 3722 — biased dataset sweep

This run replays seeds 0–19 from the original biased/simple-prompt dataset in all 12 race/gender groups. Each source image has the original plus 23 alpha variants, ordered from −120 to +120 on 4×6 grids. The saved metrics include post-re-encoded feature activation, active spatial fraction, RGB pixel MAE, and coefficient-change magnitudes.

The signed coefficient overlays use translucent colors: green near-zero negative, blue to purple for stronger negatives, yellow near-zero positive, and orange to red for stronger positives. Exact zero is transparent.

## Group reports and galleries

| Group | Metrics and representative grids | All 20 post-activation grids |
|---|---|---|
| Black Man | [Black Man summary](black_man/feature_summary.md) | [Post-activation gallery](black_man/post_activation_overlays.md) |
| Black Woman | [Black Woman summary](black_woman/feature_summary.md) | [Post-activation gallery](black_woman/post_activation_overlays.md) |
| White Man | [White Man summary](white_man/feature_summary.md) | [Post-activation gallery](white_man/post_activation_overlays.md) |
| White Woman | [White Woman summary](white_woman/feature_summary.md) | [Post-activation gallery](white_woman/post_activation_overlays.md) |
| East Asian Man | [East Asian Man summary](east_asian_man/feature_summary.md) | [Post-activation gallery](east_asian_man/post_activation_overlays.md) |
| East Asian Woman | [East Asian Woman summary](east_asian_woman/feature_summary.md) | [Post-activation gallery](east_asian_woman/post_activation_overlays.md) |
| Middle Eastern Man | [Middle Eastern Man summary](middle_eastern_man/feature_summary.md) | [Post-activation gallery](middle_eastern_man/post_activation_overlays.md) |
| Middle Eastern Woman | [Middle Eastern Woman summary](middle_eastern_woman/feature_summary.md) | [Post-activation gallery](middle_eastern_woman/post_activation_overlays.md) |
| Indian Man | [Indian Man summary](indian_man/feature_summary.md) | [Post-activation gallery](indian_man/post_activation_overlays.md) |
| Indian Woman | [Indian Woman summary](indian_woman/feature_summary.md) | [Post-activation gallery](indian_woman/post_activation_overlays.md) |
| Hispanic Man | [Hispanic Man summary](hispanic_man/feature_summary.md) | [Post-activation gallery](hispanic_man/post_activation_overlays.md) |
| Hispanic Woman | [Hispanic Woman summary](hispanic_woman/feature_summary.md) | [Post-activation gallery](hispanic_woman/post_activation_overlays.md) |

## Run files

- [Mean metrics by group and alpha](mean_metrics_by_group_alpha.csv)
- [Per-image metrics](metrics.csv)
- [Run settings](settings.json)
- [Saved activation maps](activation_maps.npz)
