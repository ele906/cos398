# Largest mid.0 SAE group differences

This reproduces the structure of [`sae_group_activations`](../sae_group_activations/),
but uses the layer-specific SAE at `unet.mid_block.attentions.0`. Values are mean SAE
activation across the 16×16 spatial grid, averaged over the same 100 generated images
in each of the 12 race/gender prompt groups. They are raw activations, so they are directly
suited to the bar-chart comparisons below. The complementary
[`mid0_pixelwise_activations`](../mid0_pixelwise_activations/) report standardizes each
grid location before ranking spatial patterns.

## Section 1: one group vs. the other 11

Candidate features are the union of each group's top-10 raw-activation features (43 unique features). Features are ranked by their largest group mean minus the average of the other 11 group means.

| Rank | Feature | Peak group | Peak mean | Other 11 groups’ average | Difference | Chart |
|---:|---:|---|---:|---:|---:|---|
| 1 | 4228 | Middle Eastern men | 5.919 | 0.642 | 5.278 | <img src="one_vs_many/feature_4228.png" width="420" alt="Feature 4228 activation across 12 groups"> |
| 2 | 1650 | Black women | 4.355 | 0.309 | 4.046 | <img src="one_vs_many/feature_1650.png" width="420" alt="Feature 1650 activation across 12 groups"> |
| 3 | 4554 | White women | 4.899 | 0.951 | 3.948 | <img src="one_vs_many/feature_4554.png" width="420" alt="Feature 4554 activation across 12 groups"> |
| 4 | 4586 | White women | 3.830 | 0.288 | 3.542 | <img src="one_vs_many/feature_4586.png" width="420" alt="Feature 4586 activation across 12 groups"> |
| 5 | 5094 | White women | 3.585 | 0.249 | 3.335 | <img src="one_vs_many/feature_5094.png" width="420" alt="Feature 5094 activation across 12 groups"> |
| 6 | 1074 | White women | 3.422 | 0.323 | 3.100 | <img src="one_vs_many/feature_1074.png" width="420" alt="Feature 1074 activation across 12 groups"> |
| 7 | 2023 | Middle Eastern men | 3.896 | 0.983 | 2.913 | <img src="one_vs_many/feature_2023.png" width="420" alt="Feature 2023 activation across 12 groups"> |
| 8 | 4338 | White men | 4.926 | 2.133 | 2.794 | <img src="one_vs_many/feature_4338.png" width="420" alt="Feature 4338 activation across 12 groups"> |
| 9 | 2361 | White women | 3.078 | 0.616 | 2.462 | <img src="one_vs_many/feature_2361.png" width="420" alt="Feature 2361 activation across 12 groups"> |
| 10 | 509 | White men | 3.037 | 0.674 | 2.363 | <img src="one_vs_many/feature_509.png" width="420" alt="Feature 509 activation across 12 groups"> |

## Section 2: predefined many-group contrasts

This section uses the same seven predefined contrasts as the original report: all women versus
all men, plus each race's men and women versus the other five races. It scans all 5,120
mid.0 features and reports the three largest absolute raw-activation differences per contrast.

| Contrast | Feature | First side mean | Comparison side mean | Difference | 12-group chart |
|---|---:|---:|---:|---:|---|
| All women vs. All men | 4228 | 0.028 | 2.135 | -2.106 | <img src="many_vs_many/feature_4228.png" width="420" alt="Feature 4228 activation across 12 groups"> |
| All women vs. All men | 4554 | 2.214 | 0.347 | +1.867 | <img src="many_vs_many/feature_4554.png" width="420" alt="Feature 4554 activation across 12 groups"> |
| All women vs. All men | 4338 | 1.482 | 3.249 | -1.768 | <img src="many_vs_many/feature_4338.png" width="420" alt="Feature 4338 activation across 12 groups"> |
| Black men and women vs. The other five races | 1650 | 2.207 | 0.334 | +1.872 | <img src="many_vs_many/feature_1650.png" width="420" alt="Feature 1650 activation across 12 groups"> |
| Black men and women vs. The other five races | 4338 | 3.519 | 2.135 | +1.384 | <img src="many_vs_many/feature_4338.png" width="420" alt="Feature 4338 activation across 12 groups"> |
| Black men and women vs. The other five races | 2023 | 0.102 | 1.451 | -1.348 | <img src="many_vs_many/feature_2023.png" width="420" alt="Feature 2023 activation across 12 groups"> |
| White men and women vs. The other five races | 4586 | 1.922 | 0.316 | +1.606 | <img src="many_vs_many/feature_4586.png" width="420" alt="Feature 4586 activation across 12 groups"> |
| White men and women vs. The other five races | 5094 | 1.794 | 0.274 | +1.519 | <img src="many_vs_many/feature_5094.png" width="420" alt="Feature 5094 activation across 12 groups"> |
| White men and women vs. The other five races | 4554 | 2.516 | 1.033 | +1.483 | <img src="many_vs_many/feature_4554.png" width="420" alt="Feature 4554 activation across 12 groups"> |
| East Asian men and women vs. The other five races | 4554 | 0.194 | 1.497 | -1.304 | <img src="many_vs_many/feature_4554.png" width="420" alt="Feature 4554 activation across 12 groups"> |
| East Asian men and women vs. The other five races | 4228 | 0.019 | 1.294 | -1.275 | <img src="many_vs_many/feature_4228.png" width="420" alt="Feature 4228 activation across 12 groups"> |
| East Asian men and women vs. The other five races | 4601 | 1.000 | 2.083 | -1.083 | <img src="many_vs_many/feature_4601.png" width="420" alt="Feature 4601 activation across 12 groups"> |
| Middle Eastern men and women vs. The other five races | 2023 | 3.550 | 0.761 | +2.788 | <img src="many_vs_many/feature_2023.png" width="420" alt="Feature 2023 activation across 12 groups"> |
| Middle Eastern men and women vs. The other five races | 4228 | 3.038 | 0.690 | +2.348 | <img src="many_vs_many/feature_4228.png" width="420" alt="Feature 4228 activation across 12 groups"> |
| Middle Eastern men and women vs. The other five races | 4399 | 2.618 | 0.547 | +2.071 | <img src="many_vs_many/feature_4399.png" width="420" alt="Feature 4399 activation across 12 groups"> |
| Indian men and women vs. The other five races | 953 | 2.841 | 1.774 | +1.067 | <img src="many_vs_many/feature_953.png" width="420" alt="Feature 953 activation across 12 groups"> |
| Indian men and women vs. The other five races | 3018 | 2.769 | 1.829 | +0.939 | <img src="many_vs_many/feature_3018.png" width="420" alt="Feature 3018 activation across 12 groups"> |
| Indian men and women vs. The other five races | 3067 | 1.689 | 0.768 | +0.921 | <img src="many_vs_many/feature_3067.png" width="420" alt="Feature 3067 activation across 12 groups"> |
| Hispanic men and women vs. The other five races | 2244 | 1.233 | 0.471 | +0.761 | <img src="many_vs_many/feature_2244.png" width="420" alt="Feature 2244 activation across 12 groups"> |
| Hispanic men and women vs. The other five races | 3595 | 1.024 | 0.272 | +0.751 | <img src="many_vs_many/feature_3595.png" width="420" alt="Feature 3595 activation across 12 groups"> |
| Hispanic men and women vs. The other five races | 2497 | 0.220 | 0.948 | -0.728 | <img src="many_vs_many/feature_2497.png" width="420" alt="Feature 2497 activation across 12 groups"> |

Differences are descriptive associations in prompt-conditioned generated images. They do not
identify a feature's semantic meaning or establish causation. Feature IDs are SAE-specific
and should not be compared directly with the down.2.1 dictionary.
