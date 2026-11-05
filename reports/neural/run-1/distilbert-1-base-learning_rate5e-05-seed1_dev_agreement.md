# Agreement with model drafts: distilbert-1-base-learning_rate5e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/distilbert-1-base-learning_rate5e-05-seed1.jsonl` (distilbert-1-base-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.018 | [0.013, 0.026] |
| Exact span F1 | 0.026 | [0.020, 0.035] |
| Exact span precision | 0.014 | [0.010, 0.018] |
| Exact span recall | 0.231 | [0.188, 0.277] |
| Role macro-F1 (roles with gold support) | 0.012 | [0.008, 0.018] |
| Category macro-F1 | 0.018 | [0.013, 0.025] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.845 | [0.828, 0.862] |
| Reversed meaning rate (lower is better) | 0.072 | [0.032, 0.122] |
| Category accuracy on exactly matched spans | 0.809 | [0.704, 0.896] |
| Role accuracy on exactly matched spans | 0.854 | [0.766, 0.935] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.018 | 0.226 | 0.034 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.008 | 0.167 | 0.015 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.007 | 0.167 | 0.013 | 36 |
| USAGE | 0.011 | 0.194 | 0.021 | 186 |
| ACCESS | 0.019 | 0.216 | 0.035 | 134 |
| PLATFORM | 0.001 | 0.033 | 0.003 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.581 | 0.024 | 0.039 |
| 20% | 0.498 | 0.022 | 0.073 |
| 30% | 0.447 | 0.019 | 0.096 |
| 40% | 0.405 | 0.018 | 0.117 |
| 50% | 0.369 | 0.016 | 0.130 |
| 60% | 0.335 | 0.014 | 0.142 |
| 70% | 0.303 | 0.013 | 0.153 |
| 80% | 0.270 | 0.012 | 0.153 |
| 90% | 0.229 | 0.011 | 0.158 |
| 100% | 0.114 | 0.010 | 0.161 |
