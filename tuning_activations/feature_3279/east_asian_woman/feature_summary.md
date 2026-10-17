# Feature 3279 — East Asian Woman

Biased dataset; original prompt and seed replay for seeds 0–19. Values are means across 20 source images. The table reports the mean post-re-encoded activation of feature 3279, the active spatial fraction, mean RGB pixel MAE versus the original image (0–255 scale), and coefficient change magnitudes for each alpha.

## Activation graph

<img src="activation_graph.png" width="380" alt="Feature 3279 graph for East Asian Woman">

## Mean metrics by alpha

| Alpha | Mean post-reencoded feature 3279 activation | Active spatial fraction | Mean pixel change (MAE) | Mean absolute coefficient change | Mean absolute scaled coefficient |
|---:|---:|---:|---:|---:|---:|
| -120 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| -100 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| -75 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| -50 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| -30 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| -20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| -15 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| -10 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| -7 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| -5 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| -3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| +0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| +3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| +5 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| +7 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| +10 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| +15 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| +20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| +30 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| +50 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| +75 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| +100 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| +120 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Per-seed grids

Each 4×6 sheet contains the original followed by the 23 alpha variants in ascending alpha order, from −120 through +120.

### Plain images

<img src="seed_sheets/east_asian_woman_seed0.jpg" width="1100" alt="East Asian Woman seed 0, original and alpha variants">

[All 20 plain-image grids](seed_sheets/)

### Signed coefficient overlays

<img src="signed_coefficient_overlays/east_asian_woman_seed0.jpg" width="1100" alt="East Asian Woman seed 0 signed coefficient overlays">

[All 20 signed coefficient grids](signed_coefficient_overlays/)

### Post-re-encoded activation overlays

<img src="post_activation_overlays/east_asian_woman_seed0.jpg" width="1100" alt="East Asian Woman seed 0 post-activation overlays">

[All 20 post-activation grids](post_activation_overlays/)

### Intervention-footprint overlays

[All 20 intervention-footprint grids](intervention_footprint_overlays/)

Zero is transparent. Negative coefficient colors progress green through blue to purple; positive colors progress yellow through orange to red. Each map tile is normalized individually for visibility. The original and alpha-zero tiles show the pre-intervention feature map so its location remains visible.
