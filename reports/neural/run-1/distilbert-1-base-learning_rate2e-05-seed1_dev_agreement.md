# Agreement with model drafts: distilbert-1-base-learning_rate2e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/distilbert-1-base-learning_rate2e-05-seed1.jsonl` (distilbert-1-base-learning_rate2e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.007 | [0.005, 0.010] |
| Exact span F1 | 0.010 | [0.007, 0.014] |
| Exact span precision | 0.005 | [0.004, 0.007] |
| Exact span recall | 0.137 | [0.106, 0.169] |
| Role macro-F1 (roles with gold support) | 0.005 | [0.003, 0.008] |
| Category macro-F1 | 0.007 | [0.004, 0.010] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.865 | [0.848, 0.878] |
| Reversed meaning rate (lower is better) | 0.073 | [0.044, 0.100] |
| Category accuracy on exactly matched spans | 0.830 | [0.717, 0.929] |
| Role accuracy on exactly matched spans | 0.830 | [0.719, 0.938] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.007 | 0.127 | 0.013 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.004 | 0.167 | 0.008 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.004 | 0.139 | 0.008 | 36 |
| USAGE | 0.005 | 0.124 | 0.010 | 186 |
| ACCESS | 0.005 | 0.119 | 0.010 | 134 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.382 | 0.013 | 0.034 |
| 20% | 0.326 | 0.008 | 0.044 |
| 30% | 0.289 | 0.007 | 0.057 |
| 40% | 0.260 | 0.006 | 0.062 |
| 50% | 0.237 | 0.006 | 0.078 |
| 60% | 0.216 | 0.005 | 0.083 |
| 70% | 0.198 | 0.005 | 0.091 |
| 80% | 0.178 | 0.004 | 0.091 |
| 90% | 0.157 | 0.004 | 0.096 |
| 100% | 0.092 | 0.004 | 0.096 |
