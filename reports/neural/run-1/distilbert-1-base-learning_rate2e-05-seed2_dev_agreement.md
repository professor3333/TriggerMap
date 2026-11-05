# Agreement with model drafts: distilbert-1-base-learning_rate2e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/distilbert-1-base-learning_rate2e-05-seed2.jsonl` (distilbert-1-base-learning_rate2e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.006 | [0.004, 0.009] |
| Exact span F1 | 0.010 | [0.007, 0.013] |
| Exact span precision | 0.005 | [0.003, 0.007] |
| Exact span recall | 0.132 | [0.098, 0.166] |
| Role macro-F1 (roles with gold support) | 0.005 | [0.002, 0.009] |
| Category macro-F1 | 0.007 | [0.004, 0.010] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.867 | [0.850, 0.882] |
| Reversed meaning rate (lower is better) | 0.073 | [0.042, 0.104] |
| Category accuracy on exactly matched spans | 0.824 | [0.707, 0.927] |
| Role accuracy on exactly matched spans | 0.745 | [0.636, 0.854] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.006 | 0.111 | 0.012 | 323 |
| EXCEPTION | 0.003 | 0.059 | 0.006 | 17 |
| NOT_REQUIRED | 0.001 | 0.056 | 0.002 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.001 | 0.056 | 0.003 | 36 |
| USAGE | 0.005 | 0.108 | 0.009 | 186 |
| ACCESS | 0.005 | 0.127 | 0.009 | 134 |
| PLATFORM | 0.003 | 0.100 | 0.006 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.373 | 0.009 | 0.023 |
| 20% | 0.320 | 0.005 | 0.028 |
| 30% | 0.287 | 0.005 | 0.041 |
| 40% | 0.262 | 0.005 | 0.052 |
| 50% | 0.241 | 0.005 | 0.070 |
| 60% | 0.223 | 0.005 | 0.073 |
| 70% | 0.205 | 0.004 | 0.075 |
| 80% | 0.186 | 0.004 | 0.078 |
| 90% | 0.166 | 0.003 | 0.080 |
| 100% | 0.101 | 0.003 | 0.083 |
