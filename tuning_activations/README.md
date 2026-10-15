# Activation tuning

This folder contains feature intervention experiments on images from the original biased race/gender dataset. Each feature gets its own folder with the sweep script, notebook, run metadata, metrics, charts, and image sheets.

## Feature 138

The first run uses the 100 Middle Eastern women images because feature 138 had its largest mean activation in that group. Prompts and seeds come from `backprop/manifest.csv` and use the original template, `a picture of a {race} {gender}`. The intervention varies alpha across `-100, -80, -60, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 60, 80, 100`; each seed sheet contains the original and all 19 alpha variants, ordered ascending.

The earlier scarf/no-scarf prompt experiment remains in `../race_gender_feature_interventions/feature_138/` as a separate prompt-controlled exploration. It is not used for the biased-dataset results here.

The runnable notebook and reusable scripts are also included in the public [cos398 `tuning_activations` folder](https://github.com/ele906/cos398/tree/main/tuning_activations) and the [SAE demo notebook repository](https://github.com/ele906/sae-demo-notebooks/tree/main/sae-activation/activation_tuning).
