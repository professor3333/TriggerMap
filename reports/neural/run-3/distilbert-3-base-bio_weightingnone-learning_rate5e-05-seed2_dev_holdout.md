# Agreement with model drafts (held-out half): distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed2.jsonl` (distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.056 | [0.020, 0.102] |
| Exact span F1 | 0.067 | [0.030, 0.112] |
| Exact span precision | 0.056 | [0.026, 0.094] |
| Exact span recall | 0.086 | [0.037, 0.142] |
| Role macro-F1 (roles with gold support) | 0.050 | [0.011, 0.109] |
| Category macro-F1 | 0.046 | [0.015, 0.087] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.478 | [0.394, 0.556] |
| Reversed meaning rate (lower is better) | 0.037 | [0.007, 0.076] |
| Category accuracy on exactly matched spans | 0.833 | [0.538, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.056 | 0.083 | 0.067 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.100 | 0.200 | 0.133 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.050 | 0.056 | 0.053 | 18 |
| USAGE | 0.038 | 0.093 | 0.054 | 54 |
| ACCESS | 0.083 | 0.074 | 0.078 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.650 | 0.091 | 0.014 |
| 20% | 0.602 | 0.070 | 0.021 |
| 30% | 0.566 | 0.077 | 0.036 |
| 40% | 0.540 | 0.058 | 0.036 |
| 50% | 0.517 | 0.056 | 0.043 |
| 60% | 0.495 | 0.046 | 0.043 |
| 70% | 0.478 | 0.040 | 0.043 |
| 80% | 0.446 | 0.046 | 0.057 |
| 90% | 0.408 | 0.046 | 0.064 |
| 100% | 0.232 | 0.046 | 0.071 |
