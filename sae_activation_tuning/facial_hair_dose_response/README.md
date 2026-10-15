# Facial hair feature intervention sweep

This is an exploratory SDXL Turbo intervention study for SAE feature 2893, a weak beard candidate, with feature 4544 as an activity-matched comparison. It asks whether changing one feature's coefficient can visibly add or suppress facial hair in matched generated portraits.

## Design

- Prompts use a neutral studio portrait, plain white T-shirt, and white background. The paired conditions request either a clean-shaven face or a clearly visible full beard and moustache.
- Six fixed seeds (7000–7005) are paired across conditions.
- The feature coefficient is multiplied by alpha in `-100, -75, -50, -25, -10, -5, -3, -2, -1, 0, 1, 2, 3, 5, 10, 25, 50, 75, 100`.
- The intervention is applied to the selected SAE direction at `unet.down_blocks.2.attentions.1`. Alpha `+1` is the unchanged reference. The `original` tiles use the saved baseline image.
- The original SAE coefficient maps and the edited residual's re-encoded feature maps are saved. The `jet` overlays use nearest-neighbor upsampling so the SAE spatial grid remains visible.

## Initial visual read

Across the inspected seed sheets, alpha values from roughly -10 to +10 do not consistently make facial hair appear or disappear. At +25 and above, facial hair and other face details can change, but face shape, age cues, and image quality also shift. At the most extreme magnitudes, images often contain severe distortions or unrelated objects. Negative values frequently suppress the post-intervention feature activation to zero without cleanly removing just facial hair.

This is not evidence that feature 2893 controls facial hair. Its earlier beard validation was weak (AUC 0.562), and the intervention has broad side effects. The prompts define the requested conditions but the generated images have not been independently labeled. Pixel MAE and post-re-encoded activation are diagnostics, not a facial-hair score.

For feature 2893, the following are means over six seeds. Pixel MAE compares each image with its alpha `+1` image on the 0–255 RGB scale:

| Alpha | Clean-shaven post-code mean | Bearded post-code mean | Mean pixel MAE across both conditions |
|---:|---:|---:|---:|
| -10 | 0.00 | 0.00 | 27.13 |
| -5 | 0.00 | 0.00 | 17.25 |
| 0 | 0.03 | 0.01 | 3.45 |
| +1 | 4.81 | 3.81 | 0.00 |
| +5 | 19.22 | 15.22 | 11.71 |
| +10 | 37.22 | 29.48 | 18.12 |
| +25 | 91.22 | 72.26 | 29.21 |

The activation statistics confirm the coefficient intervention is large, but cannot tell whether the visual change is specifically facial hair. The visual check above suggests changes become noticeable while other face details are shifting too.

## Results

All generated images and maps are under [`run_001`](run_001/). Each seed has a 4×5 contact sheet containing the original plus all 19 alpha values, and a matching activation overlay sheet:

- [`seed_sheets/`](run_001/seed_sheets/) — generated images
- [`seed_jet_overlay_sheets/`](run_001/seed_jet_overlay_sheets/) — post-intervention `jet` activation overlays (pre-intervention map on the original)
- [`activation_graphs/`](run_001/activation_graphs/) — per-condition, per-feature mean intervention/activation/pixel-change graphs, with `jet` bars
- [`metrics.csv`](run_001/metrics.csv) — per-seed diagnostics
- [`visual_review.csv`](run_001/visual_review.csv) — blank annotation template for human review
- [`activation_maps.npz`](run_001/activation_maps.npz) — saved pre-intervention, post-re-encoded, and scaled-coefficient 16×16 maps
- [`settings.json`](run_001/settings.json) — prompts, seeds, feature IDs, checkpoint, and method

The individual original and per-alpha images are retained in the source workspace; this public repository includes the finished contact sheets rather than duplicating every generated image. The saved maps and metrics are sufficient to replot the activation graphs without rerunning generation. Metric rows link to the seed sheet and identify the corresponding alpha tile.

The current set is a small prompt-controlled probe, not the earlier biased or unbiased 12-group dataset. A next useful step is to have a reviewer annotate visible beard amount and face/artifact damage for each seed sheet, then compare those ratings against alpha and the control feature.
