# Beard-class face parser pilot

This pilot applies the Beard output class from [jseobyun/FaceParsing](https://github.com/jseobyun/FaceParsing) to six already-generated Feature 4228 images: Indian-man and Middle-Eastern-man prompt groups, seed 30, at α = −7, +1, and +7. **No diffusion generation was run.** The six inputs are already in [`../beard_sam_pilot/input_crops/`](../beard_sam_pilot/input_crops/).

## Results

Predicted Beard-class area as a fraction of the full 512 × 512 image:

| Prompt group | α = −7 | α = +1 | α = +7 |
|---|---:|---:|---:|
| Indian man | 5.6% | 26.7% | 40.1% |
| Middle-Eastern man | 22.4% | 31.1% | 40.0% |

These are exploratory model outputs from one seed per prompt-group/multiplier cell. They do not establish a reliable intervention effect or model accuracy.

## Visuals and data

- [`beard_class_contact_sheet.jpg`](beard_class_contact_sheet.jpg): all six Beard-class overlays.
- [`masks/`](masks/): binary masks for class index 14.
- [`overlays/`](overlays/): magenta Beard-class overlays on the inputs.
- [`beard_class_metrics.csv`](beard_class_metrics.csv): pixel counts for every predicted class and per-image area fractions.
- [`code/run_beard_class_faceparser.py`](code/run_beard_class_faceparser.py): inference script for these same six inputs.

## Model provenance

- Face parser: `jseobyun/FaceParsing`, source commit `bb649e99424ea988ca2bec8b5a3c8e8ca33f3f2e`.
- Decoder: the repository's published `experiments/checkpoints/decoder.ckpt`; SHA-256 `ad5266f61eaf540f120e15c47315bef3e2302c720c1c7135d0a3e9f9de55af39`.
- Backbone: official Meta DINOv3 ViT-B/16 LVD-1689M, `dinov3_vitb16_pretrain_lvd1689m-73cec8be.pth`; SHA-256 `73cec8be7427c8655ceced13ce62f6e20a1fa90d1b4d4a550df17a1144081a7c`.
- Class mapping: index 14 is named **Beard** in the FaceParsing README. Model weights are not committed; the DINOv3 license requires accepting Meta's terms before downloading them.

The upstream visualization helper lists a conflicting class order (where index 14 is named `neck`). For this pilot, inference extracts raw class index 14, matching the upstream README's FaceSynthetics label table; the visualization helper was not used to generate these masks. The overlays look beard-like in these examples but include some spillover around the edges. Treat these as unvalidated model predictions, not ground-truth beard annotations.

## Reproduce

First obtain the DINOv3 ViT-B/16 weights under Meta's DINOv3 license, then clone the parser at the recorded source commit and place its decoder checkpoint at the paths expected by the parser:

```bash
git clone https://github.com/jseobyun/FaceParsing.git /n/fs/goose/face-parsing-beard-class
git -C /n/fs/goose/face-parsing-beard-class checkout bb649e99424ea988ca2bec8b5a3c8e8ca33f3f2e
# Put the licensed DINOv3 ViT-B/16 checkpoint at:
# /n/fs/goose/face-parsing-beard-class/checkpoints/dinov3_vitb16_pretrain_lvd1689m-73cec8be.pth
# Download the decoder checkpoint linked in the upstream FaceParsing README to:
# /n/fs/goose/face-parsing-beard-class/experiments/checkpoints/decoder.ckpt

PYTHONNOUSERSITE=1 /n/fs/goose/el8403/conda-envs/goose/bin/python \
  mid0_stability/20_seed_evaluation/beard_faceparser_pilot/code/run_beard_class_faceparser.py \
  --repo /n/fs/goose/face-parsing-beard-class
```

By default, rerun outputs go to `/tmp/faceparser_beard_pilot_rerun`; set `--input-dir` or `--output-dir` to use different locations. The script reads the six saved crops from the neighboring SAM pilot directory and does not call the diffusion model.

## 20-seed extension

The separate [20-seed FaceParsing Beard-class extension](20_seed_extension/README.md) evaluates raw class-14 predictions on the full-resolution saved Feature 4228 sweep images for seeds 30–49. It includes contact sheets, masks, per-image metrics, paired changes, and uncertainty intervals. It does not replace the SAM proposals or validate the parser against ground-truth beard masks.
