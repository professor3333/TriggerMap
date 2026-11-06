# Agreement with model drafts (held-out half): distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed0.jsonl` (distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.045 | [0.018, 0.078] |
| Exact span F1 | 0.059 | [0.027, 0.091] |
| Exact span precision | 0.043 | [0.020, 0.069] |
| Exact span recall | 0.093 | [0.045, 0.143] |
| Role macro-F1 (roles with gold support) | 0.045 | [0.010, 0.089] |
| Category macro-F1 | 0.041 | [0.016, 0.064] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.750 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.589 | [0.494, 0.657] |
| Reversed meaning rate (lower is better) | 0.032 | [0.000, 0.076] |
| Category accuracy on exactly matched spans | 0.846 | [0.667, 1.000] |
| Role accuracy on exactly matched spans | 0.923 | [0.769, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.038 | 0.083 | 0.052 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.095 | 0.200 | 0.129 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.045 | 0.056 | 0.050 | 18 |
| USAGE | 0.029 | 0.093 | 0.044 | 54 |
| ACCESS | 0.055 | 0.093 | 0.069 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.593 | 0.067 | 0.014 |
| 20% | 0.552 | 0.082 | 0.036 |
| 30% | 0.534 | 0.066 | 0.043 |
| 40% | 0.514 | 0.049 | 0.043 |
| 50% | 0.500 | 0.046 | 0.050 |
| 60% | 0.488 | 0.044 | 0.057 |
| 70% | 0.465 | 0.042 | 0.064 |
| 80% | 0.431 | 0.041 | 0.071 |
| 90% | 0.362 | 0.036 | 0.071 |
| 100% | 0.186 | 0.033 | 0.071 |
