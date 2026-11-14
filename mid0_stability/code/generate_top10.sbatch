#!/bin/bash
#SBATCH --job-name=mid0-ft-top10
#SBATCH --partition=all
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
#SBATCH --gres=gpu:l40:1
#SBATCH --time=08:00:00
#SBATCH --array=0-9%10
#SBATCH --output=/n/fs/goose/layers/mid0_stability/logs/top10-%A_%a.out
set -euo pipefail
cd /n/fs/goose
export OMP_NUM_THREADS=4 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 PYTHONNOUSERSITE=1
export PYTHONPATH=/n/fs/goose/layers/mid0_stability/generation_deps
PY=/n/fs/goose/el8403/conda-envs/goose/bin/python
FEATURE=$($PY -c 'import json,os; print(json.load(open("layers/mid0_stability/finetuned_ranking/top10.json"))["features"][int(os.environ["SLURM_ARRAY_TASK_ID"])])')
OUT="layers/runs/mid0_sae_face_001/interventions/stability_top10_${SLURM_ARRAY_JOB_ID}/feature_${FEATURE}"
$PY -u layers/mid0_stability/generate_sweep.py \
  --feature "$FEATURE" --block unet.mid_block.attentions.0 \
  --checkpoint layers/runs/mid0_sae_face_001/sae \
  --alphas -100 -70 -50 -40 -30 -20 -15 -12 -10 -7 -5 -3 -2 -1 0 1 2 3 5 7 10 12 15 20 30 40 50 70 100 \
  --samples-per-group 5 --seed-start 30 --output "$OUT" \
  --reuse-images-from /n/fs/goose/layers/runs/mid0_sae_face_001/interventions/stability_wider_4243070
