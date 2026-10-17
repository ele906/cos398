# Activation tuning

This folder contains feature intervention experiments on images from the original biased race/gender dataset. Each feature gets its own folder with the sweep script, notebook, run metadata, metrics, charts, and image sheets.

## Feature 138

The first run uses the 100 Middle Eastern women images because feature 138 had its largest mean activation in that group. Prompts and seeds come from `backprop/manifest.csv` and use the original template, `a picture of a {race} {gender}`. The intervention varies alpha across `-100, -80, -60, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 60, 80, 100`; each seed sheet contains the original and all 19 alpha variants, ordered ascending.

The earlier scarf/no-scarf prompt experiment remains in `../race_gender_feature_interventions/feature_138/` as a separate prompt-controlled exploration. It is not used for the biased-dataset results here.

## Feature 3279

[Feature 3279 report](feature_3279/feature_report.md): biased-dataset intervention sweep across 12 race/gender groups, seeds 0–19, and 23 signed alpha values. Each source seed has an original plus 23 variants in ascending alpha order on 4×6 grids. Per-alpha mean activation, active fraction, pixel MAE, and coefficient metrics are reported by group.

## Features 452 and 527

[Feature 452 report](feature_452/feature_report.md) and [feature 527 report](feature_527/feature_report.md): both were run across all 12 biased race/gender groups, seeds 0–19, and 23 signed alpha values. Each report includes the per-alpha activation and pixel-MAE tables, 4×6 per-seed grids, and per-group post-activation galleries.

## Feature 3884

The follow-up run covers all 12 biased race/gender groups, with 20 original seeds per group. The symmetric alpha set is `-75, -50, -30, -20, -15, -10, -7, -5, -3, 0, 3, 5, 7, 10, 15, 20, 30, 50, 75`. Browse the results in [feature 3884](feature_3884/README.md), organized by group with a 5×4 grid per seed.

Feature 3884 post-activation overlays have dedicated per-group pages, such as [Black men, all 20 seeds](feature_3884/black_man/post_activation_overlays.md). The runnable notebooks and reusable scripts are also included in the public [cos398 `tuning_activations` folder](https://github.com/ele906/cos398/tree/main/tuning_activations) and the [SAE demo notebook repository](https://github.com/ele906/sae-demo-notebooks/tree/main/sae-activation/activation_tuning).
