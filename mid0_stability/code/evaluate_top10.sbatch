#!/bin/bash
#SBATCH --job-name=mid0-ft-top10-eval
#SBATCH --partition=all
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --output=/n/fs/goose/layers/mid0_stability/logs/top10-eval-%j.out
set -euo pipefail
cd /n/fs/goose
export OMP_NUM_THREADS=4
mapfile -t FEATURES < <(/usr/local/anaconda3/2024.02/bin/python -c 'import json; print(*json.load(open("layers/mid0_stability/finetuned_ranking/top10.json"))["features"],sep="\n")')
/usr/local/anaconda3/2024.02/bin/python -u layers/mid0_stability/analyze_stability.py \
 --runs /n/fs/goose/layers/runs/mid0_sae_face_001/interventions/stability_top10_4243081 \
 --features "${FEATURES[@]}" \
 --output /n/fs/goose/layers/mid0_stability/top10_results
