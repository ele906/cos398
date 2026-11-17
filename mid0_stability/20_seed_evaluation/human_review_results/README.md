# Human Review of Face Distortion Under mid.0 SAE Interventions

## Executive summary

Three reviewers independently rated the same 100 paired images. The majority judged 28/100 candidates as visibly distorted, while MediaPipe still detected a face in 26 of those 28 cases. The reviewer agreement was 80–83% pairwise (Cohen’s κ = 0.534–0.616; Fleiss’ κ = 0.566). These results support using human judgments as a separate endpoint from face detection. They are preliminary: this is a stratified 100-case pilot, not a population estimate or a validated multiplier threshold.

## Research question

When sparse feature activations in the fine-tuned SDXL SAE are intervened on at `unet.mid_block.attentions.0` (mid.0), how often do reviewers judge the resulting face to be visibly distorted, and how well does MediaPipe landmark detection track those judgments?

## Methods

### Experiment and image sample

The image pool comes from the existing 20-seed mid.0 sweep: 10 SAE feature IDs, 12 demographic prompt groups, 20 seeds, and 29 saved multipliers (69,600 conditions). The experiment configuration identifies the fine-tuned SAE checkpoint SHA-256 as `cbb3a0a2d0c43c822c7ba97a494de38ae56ea25401a8d31484ffa32e7cc329a6`; no new images were generated for this human review.

The review subset contains 100 cases: one case for each of 10 features × 10 selected multiplier values (`-100, -50, -20, -5, 0, 1, 5, 20, 50, 100`). Prompt groups are balanced as closely as available active examples allow (8–9 cases per group). Cases were selected from initially active features with an α=1 baseline where MediaPipe detected a face. Each candidate is shown beside the α=1 image from the same feature, prompt group, and seed. The α=1 multiplier cases are identical reference/candidate controls. Each of the three reviewers rated all 100 cases, giving 300 judgments but still only 100 unique cases.

### Human labels and agreement

Reviewers answered whether the candidate showed clear structural facial distortion compared with the paired reference. The provided files contain binary yes/no labels; there were no unsure ratings. The original file is assigned reviewer ID 001 as requested. The two new files had blank reviewer IDs, so IDs 002 and 003 were assigned from their filenames for this analysis.

Pairwise agreement is the fraction of cases with matching labels. Cohen’s κ is computed for each reviewer pair; Fleiss’ κ summarizes all three raters. Majority vote is used for case-level summaries. No adjudication was performed.

### Automated endpoint

MediaPipe Face Landmarker detection was read from the existing saved evaluation. It indicates whether the model returned face landmarks, not whether a face is visually coherent or high quality.

## Results

### Human labels and reviewer agreement

Reviewers 001, 002, and 003 labeled 29, 28, and 37 cases “yes,” respectively. There were 19 unanimous yes cases and 53 unanimous no cases; the other 28 cases had a 2–1 split. Overall majority-yes proportion was 28/100 (28%; Wilson interval 20%–37%, shown only as descriptive uncertainty for this selected sample).

| Reviewer pair | Raw agreement | Cohen’s κ |
|---|---:|---:|
| 001 vs 002 | 81% | 0.534 |
| 001 vs 003 | 80% | 0.551 |
| 002 vs 003 | 83% | 0.616 |

Fleiss’ κ across the three reviewers was 0.566.

### Results by sampled multiplier

| Multiplier α | Cases | Majority yes | Majority no | Yes rate |
|---:|---:|---:|---:|---:|
| -100 | 10 | 6 | 4 | 60% |
| -50 | 10 | 7 | 3 | 70% |
| -20 | 10 | 2 | 8 | 20% |
| -5 | 10 | 0 | 10 | 0% |
| +0 | 10 | 1 | 9 | 10% |
| +1 | 10 | 0 | 10 | 0% |
| +5 | 10 | 0 | 10 | 0% |
| +20 | 10 | 3 | 7 | 30% |
| +50 | 10 | 5 | 5 | 50% |
| +100 | 10 | 4 | 6 | 40% |

The α=1 identical-image control was rated “no” in all 10 cases. Majority distortion judgments were most frequent at −50 (7/10) and −100 (6/10), while the positive values ranged from 0/10 at +5 and +1 to 5/10 at +50. This is not a monotonic cliff curve: the sample is sparse, selected, and varies in prompt group and seed across cells. It does not justify interpolation of a threshold between multipliers.

### Feature-level descriptive results

| SAE feature | Majority yes / 10 | Yes rate |
|---:|---:|---:|
| 1074 | 2/10 | 20% |
| 1650 | 3/10 | 30% |
| 2023 | 3/10 | 30% |
| 2361 | 3/10 | 30% |
| 4228 | 3/10 | 30% |
| 4338 | 6/10 | 60% |
| 4399 | 2/10 | 20% |
| 4554 | 4/10 | 40% |
| 4586 | 1/10 | 10% |
| 5094 | 1/10 | 10% |

Feature 4338 had the highest sample count of majority-yes ratings (6/10). These feature comparisons are exploratory; ten cases per feature are insufficient to establish stable feature rankings, and prompt context and seed also vary.

### Comparison with MediaPipe

MediaPipe detected a face in 98/100 cases. Of the 28 majority-yes cases, 26 (92.9%) were still detected; only 2 majority-yes case(s) were also detector misses. Both detector misses were majority-rated “yes.” Thus, in this sample, face detection missed most cases that reviewers considered distorted. The detector answers whether landmarks can be returned, not whether their geometry corresponds to a visually coherent face.

### Perturbation magnitude (exploratory)

The median saved relative intervention magnitude was 1.922 among majority-yes cases and 0.119 among majority-no cases. Spearman correlations in this selected sample were ρ=0.47 between `|α|` and the majority-yes label and ρ=0.69 between saved `relative_delta_fro` and the label. These are unadjusted descriptive associations. Feature, prompt group, and seed are not controlled in these correlations; they should not be interpreted as causal effects or significance tests.

## Interpretation

The clearest result is the gap between landmark detection and human judgment: MediaPipe detected most faces that reviewers judged distorted. Detection rate remains a useful technical endpoint for whether a face mesh was produced, but it is not an adequate stand-in for visible facial coherence. The human labels provide a promising reference target for a future geometry-based score, but the present data do not calibrate or validate such a score.

Reviewer agreement is encouraging but imperfect. The κ values indicate that labels are not interchangeable across raters, so a future study should keep multiple raters and use a prespecified consensus/adjudication rule. The α=1 controls receiving unanimous “no” is a useful check that reviewers did not label every image distorted.

## Limitations

1. Only 100 unique cases were rated, with one selected case per feature × multiplier cell; this is a pilot sample, not a representative estimate of all 69,600 conditions.
2. The sample was restricted to initially active features and cases with a detected α=1 baseline. Intervention cases with no detected face could still be included, but baseline failures were excluded.
3. The multiplier sample is coarse and deliberately selected. No precise instability boundary or threshold is estimated.
4. The ratings are subjective binary judgments from three reviewers. No “unsure” labels were present, and the two new CSVs did not record reviewer IDs; IDs were inferred from filenames.
5. Prompt group is a generation condition, not a measured identity or appearance label. These results do not establish demographic differences in distortion.
6. Perturbation-magnitude correlations are unadjusted and descriptive; the study does not show that activation magnitude alone causes the perceived distortion.

## Recommended next steps

- Retain the three labels per case and, if feasible, collect two more independent ratings on the same 100 cases to improve agreement estimates. This would provide 500 ratings but still only 100 unique images.
- To support a threshold or train a landmark-based predictor, annotate more unique cases spanning weak, intermediate, and strong interventions, with held-out cases for evaluation.
- Extract landmark coordinates from the saved images, align candidate and α=1 landmarks for pose/scale, then assess whether geometric residuals predict the majority human label on held-out cases.
- Report the rating protocol, per-rater counts, agreement, and uncertainty; do not describe MediaPipe detection as facial quality.

## Public release and reproducibility

This folder publishes the report, aggregate counts, and figure. Individual reviewer rows and the case-to-experiment mapping are retained privately and are not included in this release.

- `human_review_by_multiplier.csv` and `human_review_by_feature.csv` — aggregate tables used above.
- `human_review_by_multiplier.png` / `.pdf` — majority and per-reviewer multiplier plot.

The underlying review set contains 100 unique images rated by three reviewers (300 labels). Reviewer identifiers are pseudonymous. The private per-case consensus table and answer key are intentionally excluded.
