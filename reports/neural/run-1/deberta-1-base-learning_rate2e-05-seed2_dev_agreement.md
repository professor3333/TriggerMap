# Agreement with model drafts: deberta-1-base-learning_rate2e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/deberta-1-base-learning_rate2e-05-seed2.jsonl` (deberta-1-base-learning_rate2e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.008 | [0.006, 0.012] |
| Exact span F1 | 0.013 | [0.010, 0.018] |
| Exact span precision | 0.007 | [0.005, 0.009] |
| Exact span recall | 0.168 | [0.134, 0.212] |
| Role macro-F1 (roles with gold support) | 0.005 | [0.003, 0.008] |
| Category macro-F1 | 0.009 | [0.006, 0.013] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.868 | [0.852, 0.884] |
| Reversed meaning rate (lower is better) | 0.075 | [0.032, 0.133] |
| Category accuracy on exactly matched spans | 0.754 | [0.646, 0.857] |
| Role accuracy on exactly matched spans | 0.862 | [0.768, 0.949] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.007 | 0.167 | 0.014 | 323 |
| EXCEPTION | 0.002 | 0.059 | 0.004 | 17 |
| NOT_REQUIRED | 0.002 | 0.056 | 0.003 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.004 | 0.139 | 0.008 | 36 |
| USAGE | 0.006 | 0.140 | 0.012 | 186 |
| ACCESS | 0.005 | 0.104 | 0.010 | 134 |
| PLATFORM | 0.003 | 0.133 | 0.007 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.457 | 0.003 | 0.008 |
| 20% | 0.389 | 0.009 | 0.044 |
| 30% | 0.344 | 0.009 | 0.067 |
| 40% | 0.311 | 0.008 | 0.078 |
| 50% | 0.283 | 0.007 | 0.080 |
| 60% | 0.256 | 0.006 | 0.083 |
| 70% | 0.230 | 0.005 | 0.085 |
| 80% | 0.205 | 0.005 | 0.093 |
| 90% | 0.176 | 0.005 | 0.101 |
| 100% | 0.101 | 0.004 | 0.106 |
