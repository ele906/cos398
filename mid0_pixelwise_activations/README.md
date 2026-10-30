# Mid.0 pixelwise-standardized SAE activations

This analysis reruns the 1,200-image SDXL Turbo prompt set at `unet.mid_block.attentions.0`.
For every SAE feature and each 16×16 grid position, it uses all 12 prompt categories and all 100
seeds per category to calculate a reference mean and sample standard deviation. A category's 100-image
mean activation at each grid location is then standardized against that all-category reference:

`Z = (category pixel mean − all-category pixel mean) / all-category pixel SD`.

The rank-1 feature below maximizes the spatial mean of its finite pixelwise Z map for that category.
This scalar is only a ranking summary; inspect the map for spatial structure. Color scales are independently
bounded per panel at the 99th percentile of absolute Z, so color intensity should not be compared between panels.
SAE features with zero variance at all pixels were excluded. These results are descriptive associations in
generated prompt-conditioned images, not semantic labels or causal claims.

![Rank-1 pixelwise standardized maps](rank1_pixelwise_z_overview.png)

| Target prompt group | Rank-1 mid.0 feature | Mean pixelwise Z | Map |
|---|---:|---:|---|
| Black Man | 2138 | +0.605 | ![Z map](rank1_pixelwise_z_maps/black_man_feature_2138.png) |
| East Asian Man | 797 | +0.329 | ![Z map](rank1_pixelwise_z_maps/east_asian_man_feature_797.png) |
| Hispanic Man | 2809 | +0.338 | ![Z map](rank1_pixelwise_z_maps/hispanic_man_feature_2809.png) |
| Indian Man | 4228 | +0.543 | ![Z map](rank1_pixelwise_z_maps/indian_man_feature_4228.png) |
| Middle Eastern Man | 4228 | +1.171 | ![Z map](rank1_pixelwise_z_maps/middle_eastern_man_feature_4228.png) |
| White Man | 2068 | +0.786 | ![Z map](rank1_pixelwise_z_maps/white_man_feature_2068.png) |
| Black Woman | 1650 | +1.264 | ![Z map](rank1_pixelwise_z_maps/black_woman_feature_1650.png) |
| East Asian Woman | 1252 | +1.092 | ![Z map](rank1_pixelwise_z_maps/east_asian_woman_feature_1252.png) |
| Hispanic Woman | 2467 | +0.593 | ![Z map](rank1_pixelwise_z_maps/hispanic_woman_feature_2467.png) |
| Indian Woman | 2278 | +0.773 | ![Z map](rank1_pixelwise_z_maps/indian_woman_feature_2278.png) |
| Middle Eastern Woman | 3067 | +0.611 | ![Z map](rank1_pixelwise_z_maps/middle_eastern_woman_feature_3067.png) |
| White Woman | 5094 | +1.256 | ![Z map](rank1_pixelwise_z_maps/white_woman_feature_5094.png) |

See `rank1_features.csv` for the published selections and `settings.json` for the exact
model, checkpoint, seeds, and formula. The full ranking and raw standardized tensors remain
available in the experiment workspace rather than this GitHub report.
