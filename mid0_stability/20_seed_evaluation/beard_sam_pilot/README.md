# Targeted SAM beard-mask pilot: two prompt groups

## Scope

This release contains candidate masks for the already-saved Feature 4228 crops for `indian_man` and `middle_eastern_man`, seed 30 at α = −7, +1, and +7. It contains six source crops and 12 SAM proposals (two prompt sets per crop). No diffusion images were generated.

## What the outputs show

The `broad_lower_face` and `tight_beard_box` prompts produce lower-face proposals, but visual inspection shows spillover onto skin, neck, and in some cases clothing. The proposal masks cover roughly 26–52% of these lower-face crops. These are **not beard-area measurements**. `sam_proposal_score` is SAM's internal proposal score, not beard segmentation accuracy.

## Files

- `input_crops/`: the six crops provided to SAM.
- `masks/`: raw binary candidate proposals.
- `overlays/`: red overlays for visual inspection.
- `two_category_visual_check.jpg`: all six inputs and both prompt outputs in one sheet.
- `candidate_mask_metrics.csv`: proposal extent and SAM-internal score, with fields named to avoid implying beard accuracy.

Use these proposals only as a starting point for hand-corrected annotations. Correct every mask against the visible beard boundary before comparing area with the same-category, same-seed α=1 reference.
