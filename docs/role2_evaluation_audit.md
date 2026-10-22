# Audit note — supplied Role 2 evaluation artifacts

The supplied model package loads and returns entity predictions, but the supplied evaluation aggregation needs to be verified before presenting the metric table as final.

The JSON reports final-test overall TP=404, FP=21, FN=6, with precision ≈0.9506, recall ≈0.9854, and F1 ≈0.9677. The training notebook output says the manually reviewed test set contains 410 gold entities, so TP+FN=410 is plausible for the overall counts.

However, the per-label final-test section reports DATE TP=6,133, ORG TP=1,619, GPE TP=5,573, and PERSON TP=37. Those sum to 13,362 true positives, which cannot describe the same 410 gold entities. Baseline per-label counts show a similar discrepancy. Therefore, the per-label table is internally inconsistent with the overall counts and should be recomputed from a single exact-span comparison over (article_id, start, end, label).

For the presentation, demonstrate actual API predictions and tests. Do not say the API independently verifies F1=0.968. If mentioning the supplied overall score, identify it as the number in the provided Role 2 report and state that per-label aggregation is under review.
