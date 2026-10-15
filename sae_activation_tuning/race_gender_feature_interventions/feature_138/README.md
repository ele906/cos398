# Feature 138: headscarf intervention sweep

Feature 138 ranked highly for Middle Eastern women in the biased race/gender dataset. A previous intervention at strengths 0–2 did not cleanly remove a headscarf in one image; the earlier prompt had not explicitly forbidden a head covering. This run asks a more specific question: **does scaling feature 138 make a headscarf appear or disappear in matched neutral portraits?**

## Setup

- SDXL Turbo portraits, one inference step, at `unet.down_blocks.2.attentions.1` with the same pretrained SAE.
- Two explicit prompt conditions: a Middle Eastern woman with uncovered dark hair, and a Middle Eastern woman wearing a plain dark navy hijab.
- Six paired seeds, 7000–7005.
- Alpha values: `-100, -75, -50, -25, -10, -5, -3, -2, -1, 0, 1, 2, 3, 5, 10, 25, 50, 75, 100`.
- The intervention is block output plus `(alpha - 1) × original feature coefficient × decoder direction`. Alpha `+1` is the no-op reference.

## Initial visual read

The hijab remained visible at moderate negative and positive values in the seed sheets inspected. Moderate changes affected face details and scarf folds, but did not consistently add or remove the headscarf. At the largest magnitudes, portraits became severely distorted or turned into unrelated fabric-like textures. The no-headscarf condition did not consistently acquire a hijab at moderate values. This does not show feature 138 is a reliable headscarf control.

The output makes a useful distinction between **post-activation overlays** and **intervention-footprint overlays**. Post-activation overlays can be blank after suppression because the SAE encoder clips negative coefficients to zero. Footprint overlays show the absolute coefficient change applied to the feature direction, including when the post-activation is zero. Both use `jet`, with blue/green for lower values and yellow/red for higher values.

## Graphs

| Prompt condition | Graph |
|---|---|
| No headscarf | ![Feature 138 alpha sweep without a headscarf](run_001/activation_graphs/no_headscarf.png) |
| Headscarf | ![Feature 138 alpha sweep with a headscarf](run_001/activation_graphs/headscarf.png) |

## Per-seed sheets

Each sheet contains the original followed by all 19 alpha values in a 4×5 grid.

| Condition | Plain image sweep | Post-activation overlay | Intervention-footprint overlay |
|---|---|---|---|
| No headscarf, seed 7000 | ![No-headscarf images](run_001/seed_sheets/no_headscarf_seed7000.jpg) | ![Post-activation overlay](run_001/post_activation_overlays/no_headscarf_seed7000.jpg) | ![Intervention footprint](run_001/intervention_footprint_overlays/no_headscarf_seed7000.jpg) |
| Headscarf, seed 7000 | ![Headscarf images](run_001/seed_sheets/headscarf_seed7000.jpg) | ![Post-activation overlay](run_001/post_activation_overlays/headscarf_seed7000.jpg) | ![Intervention footprint](run_001/intervention_footprint_overlays/headscarf_seed7000.jpg) |

All six seeds for both conditions are in the matching folders under [`run_001`](run_001/). The individual per-alpha JPEGs remain in the source workspace; this public repository includes the composite sheets. Saved activation maps and metrics are included for later graphing without rerunning diffusion. Each metric row links to its seed sheet and alpha tile.

## Selected diagnostics

Means below are across six seeds. Pixel MAE compares each image with its alpha `+1` reference on the 0–255 RGB scale; it is not a headscarf score.

| Prompt | Alpha | Mean post-reencoded activation | Mean active spatial fraction | Mean pixel MAE |
|---|---:|---:|---:|---:|
| No headscarf | -5 | 0.00 | 0.000 | 11.29 |
| No headscarf | +1 | 5.86 | 0.369 | 0.00 |
| No headscarf | +5 | 28.97 | 0.369 | 16.50 |
| No headscarf | +10 | 57.85 | 0.369 | 26.93 |
| Headscarf | -5 | 0.00 | 0.000 | 44.15 |
| Headscarf | +1 | 31.51 | 0.928 | 0.00 |
| Headscarf | +5 | 155.80 | 0.928 | 20.77 |
| Headscarf | +10 | 311.16 | 0.928 | 44.24 |

## Saved data

- [`metrics.csv`](run_001/metrics.csv) — per-seed activation and pixel-change metrics
- [`visual_review.csv`](run_001/visual_review.csv) — blank human annotation template
- [`activation_maps.npz`](run_001/activation_maps.npz) — pre-activation, post-re-encoded, coefficient-change footprint, and scaled-coefficient maps
- [`settings.json`](run_001/settings.json) — prompts, seeds, alpha values, and method

This is a prompt-controlled exploratory run, not a rerun on the original 12-group biased images. Prompt conditions are requested attributes, not verified image labels. The reported group association does not prove what feature 138 represents or why it activates.
