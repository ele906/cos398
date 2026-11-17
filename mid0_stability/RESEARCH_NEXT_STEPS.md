# Current research status and next steps

The previous version of this document described the 20-seed evaluation and human review as future work. Both have since been completed. Use [Integrated results](INTEGRATED_RESULTS.md) as the current project synthesis.

## Completed

- Fine-tuned mid.0 SAE evaluation: 10 features × 12 prompt groups × 20 seeds × 29 multipliers (69,600 conditions), with saved detection outcomes, uncertainty intervals, figures, and provenance.
- Three-reviewer distortion-rating pilot: 100 unique paired cases, 300 judgments, agreement statistics, and a comparison against MediaPipe detection.
- Feature-4228 beard-class analysis across all 12 prompt groups and two exploratory SAM feasibility studies. The segmentation endpoint has not been validated as ground-truth beard area.
- Separate exploratory additive, spatial-pattern, and support-expansion analyses. These use distinct designs and should not be pooled with the multiplicative stability sweep.

## Current paper focus

Lead with intervention-strength stability in the fine-tuned mid.0 SAE, using MediaPipe landmark detection as an operational endpoint. Present the human pilot as evidence that landmark detection is not equivalent to perceived facial distortion. Keep the beard and other feature-4228 studies exploratory unless their semantic measurements are validated.

The data support descriptive differences across sampled features and prompt groups; they do not establish demographic vulnerability, a precise instability threshold, or a causal feature-by-context interaction. Prompt groups are generation conditions. MediaPipe detection is not facial quality.

## Next work

No new broad image generation is needed to write the current Results and Limitations sections. Draft those sections from the completed analyses, state the sampling and endpoint limits, and preserve secondary pilots in a clearly labeled exploratory section or appendix. Revisit additional experiments only if the manuscript exposes a specific claim that the current data cannot answer.
