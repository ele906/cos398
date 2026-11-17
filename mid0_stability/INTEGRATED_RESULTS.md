# Integrated results: fine-tuned mid.0 SAE interventions

## Research question and scope

This report brings together the completed mid.0 stability sweep, its human distortion-rating pilot, and the follow-up feature-4228 beard and spatial-pattern analyses. The strongest supported paper story is about **intervention stability and the limits of automated face detection as a proxy for visible distortion**. The beard analysis remains exploratory and should not carry the main claim.

All main stability results use the face-fine-tuned SAE at `unet.mid_block.attentions.0` (mid.0), checkpoint SHA-256 `cbb3a0a2d0c43c822c7ba97a494de38ae56ea25401a8d31484ffa32e7cc329a6`, with single-step SDXL-Turbo. The ten features were selected by group-difference ranking using discovery data; the 20-seed intervention evaluation used seeds 30–49. Prompt groups are text conditions; they are not measurements of participants’ identities or perceived identities.

The saved intervention is `h′ = h + (α − 1) zᵢ dᵢ`: α=1 is the no-op, α=0 removes the selected feature contribution, 0<α<1 attenuates it, α>1 amplifies it, and α<0 reverses its sign. “Ablation strength” should therefore not be used for every signed multiplier.

## Study 1: landmark-detection stability

The completed evaluation contains **69,600 conditions** (10 features × 12 prompt groups × 20 seeds × 29 multipliers). It has 877 MediaPipe landmark-detection failures overall (1.26%). The exact saved grid, filtering definitions, per-condition outcomes, and provenance are retained in the [20-seed evaluation report](20_seed_evaluation/README.md) and [figure documentation](20_seed_evaluation/figures/README.md).

### Pooled detection response

The table below is the `all` cohort: all 2,400 feature × prompt-group × seed observations at each multiplier. Intervals are percentile bootstrap intervals over the 20 shared seed IDs, resampling a seed together across all features and prompt groups. They are descriptive and do not make repeated images independent. At strengths with no observed misses, the interval is necessarily degenerate and should not be read as proof of 100% population detection.

| Multiplier α | Detected / n | Detection rate | 95% seed-cluster bootstrap interval |
|---:|---:|---:|---:|
| −100 | 2,064 / 2,400 | 86.0% | 84.0–88.0% |
| −50 | 2,354 / 2,400 | 98.1% | 97.4–98.8% |
| 0 (feature ablation) | 2,400 / 2,400 | 100.0% | 100–100% observed |
| +1 (no-op) | 2,400 / 2,400 | 100.0% | 100–100% observed |
| +50 | 2,376 / 2,400 | 99.0% | 98.6–99.4% |
| +100 | 2,188 / 2,400 | 91.2% | 89.5–92.9% |

Detection remained perfect at each sampled multiplier from −20 through +20. It decreased toward the extremes, with a larger decrease under negative reversal at −100 than positive amplification at +100. This is a result about **whether MediaPipe returned landmarks**, not image quality or face coherence.

The pooled curve masks substantial heterogeneity. At α=−100, 8/10 feature-pooled rates and 9/12 prompt-group rates were below 95%; at α=+100, 5/10 feature-pooled rates and 7/12 prompt-group rates were below 95%. For feature × prompt-group cells (20 seeds per cell), 35/120 were below 95% at −100 and 27/120 at +100. These are descriptive summaries; the figures show the cell counts and pointwise Wilson intervals.

### Sampled feature-level brackets

Using the saved exploratory 95% detection criterion on the **active baseline detected** cohort, the pooled-across-prompt-groups feature curves yielded the following last-passing → first-failing sampled multiplier pairs. “Not reached” means no failing sampled point through the end of the saved grid. These are brackets on the sampled detection curve, not precise instability thresholds and not thresholds for human-rated distortion.

| Feature | Negative reversal | Positive amplification |
|---:|:---:|:---:|
| 1074 | −70 → −100 | Not reached through +100 |
| 1650 | −50 → −70 | Not reached through +100 |
| 2023 | −50 → −70 | +70 → +100 |
| 2361 | −70 → −100 | Not reached through +100 |
| 4228 | −30 → −40 | +50 → +70 |
| 4338 | −40 → −50 | +30 → +40 |
| 4399 | −70 → −100 | +70 → +100 |
| 4554 | −50 → −70 | Not reached through +100 |
| 4586 | −70 → −100 | Not reached through +100 |
| 5094 | −70 → −100 | +70 → +100 |

The observed variation supports the narrower conclusion that **landmark-detection responses differ across the selected features and prompt contexts**. It does not, by itself, establish a semantic cause or a statistically confirmed feature-by-demographic interaction. Feature selection was based on group-difference activation statistics, and only one checkpoint, one layer, and one generator configuration were studied.

## Study 2: human distortion-rating pilot

Three reviewers independently rated the same 100 paired cases (300 judgments total). The sample was stratified across features and selected multiplier values, drawn from initially active features with detected α=1 references. It was not a random sample of the 69,600 images.

- Majority vote marked **28/100** candidates as visibly distorted (28%; descriptive Wilson interval 20–37%).
- Reviewers agreed on 19 yes and 53 no cases; 28 cases had a 2–1 split. Pairwise agreement was 80–83%; Fleiss’ κ was 0.566.
- MediaPipe returned landmarks for **98/100** cases. It still detected a face in **26/28** majority-yes distortion cases (92.9%).
- In the selected multiplier sample, majority-yes counts were 6/10 at −100, 7/10 at −50, 0/10 at the α=+1 no-op, 5/10 at +50, and 4/10 at +100. The pattern is not a monotonic threshold curve.
- Median relative perturbation was 1.922 in majority-yes cases and 0.119 in majority-no cases; the reported correlation is unadjusted and confounded by feature, prompt group, seed, and sampled strength.

The strongest measurement finding is the detector–human mismatch: **landmark detection is not a reliable stand-in for visible facial distortion in this reviewed subset**. The review supports treating the endpoints separately, but its selected 100 cases do not estimate the prevalence of distortion across the full sweep or calibrate a distortion threshold. See the [human-review report](20_seed_evaluation/human_review_results/README.md) for the protocol, full tables, and agreement statistics.

## Follow-up: feature 4228 beard measurements

The all-group FaceParsing analysis used 720 existing feature-4228 images (12 prompt groups × 20 seeds × α ∈ {−7, +1, +7}); it did not generate new images. Its output is the area assigned to parser class 14 (“Beard”), as a percentage of the full image. For Indian-man prompts, the mean predicted area was 3.94% at α=+1, 1.87% at −7, and 7.96% at +7. Paired changes versus +1 were −2.07 percentage points at −7 (95% seed-bootstrap interval −3.03 to −1.23) and +4.02 points at +7 (+2.77 to +5.36). For Middle-Eastern-man prompts, the corresponding baseline was 11.89%; paired changes were −3.17 points at −7 (−3.97 to −2.39) and +5.68 points at +7 (+4.72 to +6.61). East Asian men showed little paired change: +0.01 points at −7 (−0.01 to +0.04) and −0.01 at +7 (−0.06 to +0.02).

These are **parser predictions, not validated beard-area measurements**. The later SAM pilot found that the frozen prompt policy often selected chin/neck skin, lips, jewelry, or head-covering fabric, and SAM quality scores did not distinguish those mistakes. The two-group SAM follow-up had only five seeds and assistant-screened masks; its Middle-Eastern-man +50 proposal change is therefore exploratory, while the Indian-man screen retained only one paired seed. Do not claim 4228 is a confirmed beard controller or use the parser/SAM area changes as the main paper result. See the [all-group FaceParsing report](20_seed_evaluation/beard_faceparser_pilot/all_groups_20_seed/README.md). The SAM reports are on the research host at `experiments/mid0_sae_selectivity/sam_beard_all_groups_20261116_233008_010361/README.md` and `experiments/mid0_sae_selectivity/sam_beard_two_groups_20261117_003306_350126/README.md`.

## Other completed exploratory analyses

These answer narrower design questions and should remain separate from the main stability result unless the manuscript is explicitly broadened:

- **Spatial-pattern transfer, feature 4228:** 200 edited images plus controls at matched output norms, five recipient seeds, and two fixed donor maps. All 220 images were detected. For East-Asian-man prompts, natural-minus-shuffled lower-face change fraction at the larger target was 0.00784 (95% seed-bootstrap interval −0.01036 to 0.02715; exact sign-flip p=0.5). No clear localization advantage or validated beard effect was established. Full report on the research host: `experiments/mid0_sae_selectivity/spatial4228_20261114_183629_015130/results/research_summary.md`.
- **Support-expansion analysis:** On the same 200 edited conditions, intervention method explained 98.77% of balanced support variance; support was strongly determined by the layout construction. Selected-coordinate re-encoding discrepancy had some conditional associations, but support expansion was not independently identified as a cause of image instability. Pixel-change and lower-face concentration results did not support a general causal support-to-instability claim. Full report: `experiments/mid0_sae_selectivity/support_analysis_20261114_192821_021986/results/research_report.md`.
- **Additive interventions across ten features:** 4,200 existing edits were evaluated without new generation. Every image differed at the pixel level, but the analysis did not establish reliable semantic control. Addition is a different intervention operator from the multiplicative stability sweep; do not pool their strengths or outcomes. Full report: `experiments/mid0_sae_selectivity/ten_feature_review_20261116_230430_705065/README.md`.

## Paper-level conclusion supported now

> In a 20-seed evaluation of a face-fine-tuned mid.0 SAE in SDXL-Turbo, MediaPipe landmark detection was retained for nearly all sampled interventions at moderate multipliers and declined at extreme feature reversals or amplifications, with descriptive variation across features and prompt groups. A three-reviewer audit of 100 selected paired cases found that MediaPipe often continued to return landmarks for faces reviewers judged distorted, showing that detection and perceived distortion are distinct outcomes.

This is an empirical characterization of one model, SAE checkpoint, layer, feature-selection procedure, prompt set, and detector. It is not evidence that one demographic group is intrinsically more vulnerable, that landmark detection measures facial quality, or that any candidate feature selectively controls a semantic attribute.

## What to do next

No new broad image-generation experiment is needed to write the main results. The practical next step is to use this synthesis to draft the paper’s Results and Limitations sections, with the 20-seed curves as the main figures and the human-review mismatch as the measurement-validation result. Keep beard, spatial-layout, support, and additive analyses in a clearly labeled exploratory section or appendix. The older next-steps note has been replaced with a current status summary; the original five-seed report still contains its own blank annotation template, which is distinct from the completed 20-seed human-review pilot.
