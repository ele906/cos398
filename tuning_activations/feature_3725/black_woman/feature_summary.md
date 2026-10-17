# Feature 3725 — Black Woman

Biased dataset; original prompt and seed replay for seeds 0–19. Values are means across 20 source images. The table reports the mean post-re-encoded activation of feature 3725, the active spatial fraction, mean RGB pixel MAE versus the original image (0–255 scale), and coefficient change magnitudes for each alpha.

## Activation graph

<img src="activation_graph.png" width="380" alt="Feature 3725 graph for Black Woman">

## Mean metrics by alpha

| Alpha | Mean post-reencoded feature 3725 activation | Active spatial fraction | Mean pixel change (MAE) | Mean absolute coefficient change | Mean absolute scaled coefficient |
|---:|---:|---:|---:|---:|---:|
| -120 | 0.000 | 0.000 | 0.562 | 0.251 | 0.249 |
| -100 | 0.000 | 0.000 | 0.481 | 0.210 | 0.208 |
| -75 | 0.000 | 0.000 | 0.413 | 0.158 | 0.156 |
| -50 | 0.000 | 0.000 | 0.328 | 0.106 | 0.104 |
| -30 | 0.000 | 0.000 | 0.179 | 0.064 | 0.062 |
| -20 | 0.000 | 0.000 | 0.103 | 0.044 | 0.042 |
| -15 | 0.000 | 0.000 | 0.075 | 0.033 | 0.031 |
| -10 | 0.000 | 0.000 | 0.051 | 0.023 | 0.021 |
| -7 | 0.000 | 0.000 | 0.039 | 0.017 | 0.015 |
| -5 | 0.000 | 0.000 | 0.034 | 0.012 | 0.010 |
| -3 | 0.000 | 0.000 | 0.026 | 0.008 | 0.006 |
| +0 | 0.000 | 0.000 | 0.019 | 0.002 | 0.000 |
| +3 | 0.006 | 0.000 | 0.022 | 0.004 | 0.006 |
| +5 | 0.010 | 0.000 | 0.028 | 0.008 | 0.010 |
| +7 | 0.013 | 0.000 | 0.035 | 0.012 | 0.015 |
| +10 | 0.019 | 0.000 | 0.048 | 0.019 | 0.021 |
| +15 | 0.029 | 0.000 | 0.090 | 0.029 | 0.031 |
| +20 | 0.038 | 0.000 | 0.150 | 0.039 | 0.042 |
| +30 | 0.057 | 0.000 | 0.274 | 0.060 | 0.062 |
| +50 | 0.095 | 0.000 | 0.346 | 0.102 | 0.104 |
| +75 | 0.142 | 0.000 | 0.390 | 0.154 | 0.156 |
| +100 | 0.189 | 0.000 | 0.388 | 0.206 | 0.208 |
| +120 | 0.227 | 0.000 | 0.406 | 0.247 | 0.249 |

## Per-seed grids

Each 4×6 sheet contains the original followed by the 23 alpha variants in ascending alpha order, from −120 through +120.

### Plain images

<img src="seed_sheets/black_woman_seed0.jpg" width="1100" alt="Black Woman seed 0, original and alpha variants">

[All 20 plain-image grids](seed_sheets/)

### Signed coefficient overlays

<img src="signed_coefficient_overlays/black_woman_seed0.jpg" width="1100" alt="Black Woman seed 0 signed coefficient overlays">

[All 20 signed coefficient grids](signed_coefficient_overlays/)

### Post-re-encoded activation overlays

<img src="post_activation_overlays/black_woman_seed0.jpg" width="1100" alt="Black Woman seed 0 post-activation overlays">

[All 20 post-activation grids](post_activation_overlays/)

### Intervention-footprint overlays

[All 20 intervention-footprint grids](intervention_footprint_overlays/)

Zero is transparent. Negative coefficient colors progress green through blue to purple; positive colors progress yellow through orange to red. Each map tile is normalized individually for visibility. The original and alpha-zero tiles show the pre-intervention feature map so its location remains visible.
