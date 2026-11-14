# Interpreting the context-stability extension

The main question is whether feature interventions have different detectable-face
outcomes across prompt contexts at comparable measured perturbation magnitudes.
The figures are descriptive evidence for this question, not proof of a
feature-by-context interaction or of demographic vulnerability.

## Why the original 17,400 conditions need cautious interpretation

There are only five distinct noise seeds per prompt group, repeated across ten
features and 29 multipliers. There are 164 failed landmark detections, and these
are correlated across the same seed and neighboring interventions. The repeated
conditions cannot be treated as 17,400 independent demographic observations.

Among the 120 feature–prompt-group combinations in the initially active,
baseline-detected cohort, 25 have no eligible original seed and only 42 retain
all five. An absent active-cohort curve is not evidence of stability: the feature
was not active in those original samples. The all-sample cohort retains them.

Even five detections in five seeds yield a Wilson lower confidence limit near
0.566. At the exploratory 0.95 crossing criterion, one failure among five gives
0.80; one among twenty gives 0.95 and does not cross a strict below-0.95 rule.
Therefore sampled brackets may move simply because the denominator changes.
Prioritize complete detection curves, counts, and intervals over one cliff number.
Do not interpolate a precise threshold between saved multipliers.

## What the 20-seed extension can resolve

Keep feature selection, checkpoint, prompts, detector settings, multiplier grid,
and filtering fixed. Add disjoint seeds 35–49 to the original 30–34; evaluate the
additional seeds separately before combining same-environment detections.
This yields 69,600 conditions across twenty seed values. Inspect the new-fifteen
subset as a check on whether patterns seen in the initial five repeat, before
emphasizing the pooled estimate. More seeds help precision but do not create
independent human validation or remove sparse-feature eligibility issues.

## Priorities after the descriptive plots

1. Inspect whether failures recur across seeds or are driven by one sample.
2. Blindly annotate a stratified subset of detection failures and successes,
   including near-crossing, extreme-strength, and detector-recovery cases.
   Distinguish coherent face, visible distortion, plausible pose/occlusion,
   face replaced by texture/other content, and uncertain. The existing selected
   review sheets display detection outcomes and are not a blinded evaluation set.
3. Compare feature and prompt contexts where measured perturbation magnitudes
   overlap. Median-norm plots are descriptive; they do not accomplish matching or
   adjust confounding by themselves. Do not extrapolate into unsupported ranges.
4. Only then consider a regularized predictive model, evaluated by held-out seed
   clusters shared across all prompt groups and features. With twenty seeds,
   a large unregularized feature-by-group interaction remains vulnerable to
   separation, sparse failures, and overfitting. Compare simpler models first;
   make any modeling choices before examining held-out outcomes.

The paper can focus on context-dependent stability if replicated differences
remain after these checks. If they disappear after magnitude adjustment or
human validation, that is an informative limitation of raw multiplier-based
stability measurements. MediaPipe landmark detection is never itself facial
quality, and demographic prompt groups are not measured identities.
