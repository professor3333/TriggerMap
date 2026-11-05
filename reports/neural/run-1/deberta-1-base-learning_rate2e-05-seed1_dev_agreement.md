# Agreement with model drafts: deberta-1-base-learning_rate2e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/deberta-1-base-learning_rate2e-05-seed1.jsonl` (deberta-1-base-learning_rate2e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.006 | [0.004, 0.009] |
| Exact span F1 | 0.010 | [0.007, 0.013] |
| Exact span precision | 0.005 | [0.004, 0.007] |
| Exact span recall | 0.127 | [0.096, 0.160] |
| Role macro-F1 (roles with gold support) | 0.005 | [0.002, 0.008] |
| Category macro-F1 | 0.006 | [0.004, 0.010] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.868 | [0.850, 0.883] |
| Reversed meaning rate (lower is better) | 0.066 | [0.042, 0.096] |
| Category accuracy on exactly matched spans | 0.776 | [0.654, 0.886] |
| Role accuracy on exactly matched spans | 0.776 | [0.623, 0.938] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.006 | 0.111 | 0.011 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.004 | 0.111 | 0.008 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.004 | 0.139 | 0.008 | 36 |
| USAGE | 0.004 | 0.113 | 0.008 | 186 |
| ACCESS | 0.005 | 0.090 | 0.009 | 134 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.396 | 0.003 | 0.008 |
| 20% | 0.341 | 0.004 | 0.021 |
| 30% | 0.308 | 0.005 | 0.039 |
| 40% | 0.278 | 0.004 | 0.044 |
| 50% | 0.255 | 0.004 | 0.054 |
| 60% | 0.234 | 0.004 | 0.067 |
| 70% | 0.213 | 0.004 | 0.073 |
| 80% | 0.191 | 0.004 | 0.075 |
| 90% | 0.167 | 0.003 | 0.078 |
| 100% | 0.095 | 0.003 | 0.078 |
