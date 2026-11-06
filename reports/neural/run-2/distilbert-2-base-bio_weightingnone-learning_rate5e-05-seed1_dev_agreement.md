# Agreement with model drafts: distilbert-2-base-bio_weightingnone-learning_rate5e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/distilbert-2-base-bio_weightingnone-learning_rate5e-05-seed1.jsonl` (distilbert-2-base-bio_weightingnone-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.064 | [0.048, 0.081] |
| Exact span F1 | 0.086 | [0.064, 0.105] |
| Exact span precision | 0.073 | [0.056, 0.091] |
| Exact span recall | 0.104 | [0.072, 0.134] |
| Role macro-F1 (roles with gold support) | 0.042 | [0.020, 0.079] |
| Category macro-F1 | 0.046 | [0.034, 0.056] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.006 | [0.000, 0.020] |
| Complete-document exact match, documents without conditions | 0.824 | [0.615, 1.000] |
| False prerequisite rate (lower is better) | 0.510 | [0.429, 0.573] |
| Reversed meaning rate (lower is better) | 0.042 | [0.013, 0.075] |
| Category accuracy on exactly matched spans | 0.875 | [0.750, 0.976] |
| Role accuracy on exactly matched spans | 0.850 | [0.746, 0.971] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.066 | 0.099 | 0.079 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.077 | 0.111 | 0.091 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 36 |
| USAGE | 0.054 | 0.097 | 0.069 | 186 |
| ACCESS | 0.104 | 0.127 | 0.114 | 134 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.696 | 0.164 | 0.023 |
| 20% | 0.630 | 0.118 | 0.034 |
| 30% | 0.589 | 0.098 | 0.041 |
| 40% | 0.553 | 0.087 | 0.049 |
| 50% | 0.522 | 0.073 | 0.052 |
| 60% | 0.505 | 0.061 | 0.052 |
| 70% | 0.490 | 0.057 | 0.057 |
| 80% | 0.461 | 0.050 | 0.057 |
| 90% | 0.402 | 0.055 | 0.070 |
| 100% | 0.220 | 0.055 | 0.078 |
