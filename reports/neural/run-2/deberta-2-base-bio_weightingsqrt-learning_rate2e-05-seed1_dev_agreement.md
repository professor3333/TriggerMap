# Agreement with model drafts: deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed1.jsonl` (deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.077 | [0.059, 0.100] |
| Exact span F1 | 0.098 | [0.078, 0.121] |
| Exact span precision | 0.062 | [0.048, 0.077] |
| Exact span recall | 0.244 | [0.200, 0.291] |
| Role macro-F1 (roles with gold support) | 0.041 | [0.027, 0.061] |
| Category macro-F1 | 0.071 | [0.051, 0.093] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.019 | [0.000, 0.042] |
| Complete-document exact match, documents without conditions | 0.235 | [0.056, 0.500] |
| False prerequisite rate (lower is better) | 0.658 | [0.614, 0.690] |
| Reversed meaning rate (lower is better) | 0.044 | [0.013, 0.085] |
| Category accuracy on exactly matched spans | 0.862 | [0.780, 0.938] |
| Role accuracy on exactly matched spans | 0.926 | [0.861, 0.979] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.067 | 0.260 | 0.106 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.033 | 0.111 | 0.051 | 18 |
| UNCERTAIN | 0.005 | 0.036 | 0.009 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.063 | 0.250 | 0.101 | 36 |
| USAGE | 0.056 | 0.242 | 0.090 | 186 |
| ACCESS | 0.059 | 0.201 | 0.091 | 134 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.530 | 0.065 | 0.026 |
| 20% | 0.488 | 0.079 | 0.062 |
| 30% | 0.460 | 0.072 | 0.085 |
| 40% | 0.436 | 0.077 | 0.122 |
| 50% | 0.408 | 0.076 | 0.150 |
| 60% | 0.383 | 0.068 | 0.161 |
| 70% | 0.352 | 0.063 | 0.174 |
| 80% | 0.320 | 0.057 | 0.181 |
| 90% | 0.269 | 0.053 | 0.189 |
| 100% | 0.114 | 0.048 | 0.192 |
