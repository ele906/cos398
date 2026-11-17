# Fine-tuned mid.0 stability: 20 seeds per prompt group

**69,600 image conditions**: ten fixed SAE features × twelve demographic prompt groups × twenty seeds (30–49) × 29 saved multipliers. This extends the original five-seed evaluation with fifteen disjoint seeds per group. The original five-seed report is preserved.

Only the face-fine-tuned SAE at `unet.mid_block.attentions.0` is used. Checkpoint SHA-256: `cbb3a0a2d0c43c822c7ba97a494de38ae56ea25401a8d31484ffa32e7cc329a6`. The original feature selection and multiplier grid are unchanged. Combining checks seed disjointness, full condition coverage, checkpoint, software versions, generation settings, and detector definitions; no old-environment sweeps are pooled.

## Generated image examples

You are right that the aggregate graphs do not show what the generated faces look like. [Saved-image contact sheets](face_examples/README.md) now show the α=1 reference and neighboring multipliers around representative MediaPipe detection misses. They include 143 examples across feature, prompt group, seed, and intervention direction. The [complete miss counts](face_examples/failure_counts.csv) cover all 877 missed detections among 69,600 conditions. These examples are illustrative rather than a blinded human quality assessment: MediaPipe misses do not prove visible facial distortion.

## Figures and data

- [All 94 figure sets and methods](figures/README.md), each as PNG, PDF, and aggregated CSV.
- [Feature × prompt-group heatmaps and sampled crossing brackets](figures/heatmaps/).
- [Ten per-feature plots](figures/per_feature/) and [twelve per-category plots](figures/per_category/).
- [Measured perturbation-magnitude panels](figures/magnitude/).
- [Per-image records](data/per_image.csv), [detection summary](data/detection_summary.csv), and [sampled boundaries](data/sampled_boundaries.csv).
- [Condition and provenance audit](figures/audit.json), [source merge audit](data/source_audit.csv), and [experiment configuration](data/experiment.json).
- [Fixed fine-tuned feature ranking](ranking.json) and [plotting code](code/plot_context_stability.py).

The existing `all`, `active`, and `active baseline detected` definitions are preserved. Figures report eligible sample counts, pointwise 95% Wilson intervals, missing cohorts, and the explicit n<5 exploratory flag. Twenty available seeds do not guarantee twenty eligible active-feature samples. Sampled crossing brackets are not continuous threshold estimates.

MediaPipe landmark detection is **not facial quality**. Prompt groups are generation conditions, not measured demographic identities. A three-reviewer pilot on 100 selected paired cases is now available in [human-review results](human_review_results/README.md); it is limited and does not validate all 69,600 outcomes. More seeds improve precision; these descriptive figures do not establish a causal feature–prompt interaction or demographic vulnerability. See the [integrated results](../INTEGRATED_RESULTS.md) for the current synthesis.

Original source hashes are retained in figures/audit.json. Published per-image paths are converted to workspace-relative references; published_data_hashes.json records the exported CSV/JSON hashes. Raw images, model weights, and detector caches are not uploaded.

From this report directory, reproduce the plots with the saved CSVs:

```bash
python code/plot_context_stability.py --source data --output figures_v2
```

Existing output directories are refused. The plotting script requires Python, NumPy, pandas, and Matplotlib and does not rerun diffusion or MediaPipe.
