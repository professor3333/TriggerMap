# Agreement with model drafts: deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed2.jsonl` (deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.070 | [0.051, 0.096] |
| Exact span F1 | 0.090 | [0.071, 0.116] |
| Exact span precision | 0.054 | [0.042, 0.071] |
| Exact span recall | 0.269 | [0.225, 0.321] |
| Role macro-F1 (roles with gold support) | 0.040 | [0.023, 0.065] |
| Category macro-F1 | 0.071 | [0.054, 0.095] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.013 | [0.000, 0.033] |
| Complete-document exact match, documents without conditions | 0.235 | [0.056, 0.500] |
| False prerequisite rate (lower is better) | 0.701 | [0.668, 0.733] |
| Reversed meaning rate (lower is better) | 0.066 | [0.019, 0.128] |
| Category accuracy on exactly matched spans | 0.885 | [0.809, 0.957] |
| Role accuracy on exactly matched spans | 0.885 | [0.795, 0.959] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.059 | 0.276 | 0.098 | 323 |
| EXCEPTION | 0.019 | 0.059 | 0.028 | 17 |
| NOT_REQUIRED | 0.020 | 0.111 | 0.034 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.058 | 0.306 | 0.098 | 36 |
| USAGE | 0.047 | 0.269 | 0.079 | 186 |
| ACCESS | 0.063 | 0.224 | 0.098 | 134 |
| PLATFORM | 0.006 | 0.033 | 0.010 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.546 | 0.037 | 0.018 |
| 20% | 0.496 | 0.070 | 0.070 |
| 30% | 0.462 | 0.070 | 0.104 |
| 40% | 0.433 | 0.060 | 0.119 |
| 50% | 0.405 | 0.055 | 0.137 |
| 60% | 0.377 | 0.059 | 0.176 |
| 70% | 0.344 | 0.054 | 0.187 |
| 80% | 0.307 | 0.049 | 0.194 |
| 90% | 0.256 | 0.045 | 0.202 |
| 100% | 0.134 | 0.042 | 0.207 |
