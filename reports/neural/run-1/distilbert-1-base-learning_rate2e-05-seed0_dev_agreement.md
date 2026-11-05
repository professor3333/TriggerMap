# Agreement with model drafts: distilbert-1-base-learning_rate2e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/distilbert-1-base-learning_rate2e-05-seed0.jsonl` (distilbert-1-base-learning_rate2e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.007 | [0.004, 0.010] |
| Exact span F1 | 0.010 | [0.007, 0.014] |
| Exact span precision | 0.005 | [0.004, 0.007] |
| Exact span recall | 0.132 | [0.098, 0.171] |
| Role macro-F1 (roles with gold support) | 0.006 | [0.003, 0.009] |
| Category macro-F1 | 0.007 | [0.004, 0.009] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.859 | [0.842, 0.875] |
| Reversed meaning rate (lower is better) | 0.081 | [0.052, 0.113] |
| Category accuracy on exactly matched spans | 0.784 | [0.638, 0.905] |
| Role accuracy on exactly matched spans | 0.824 | [0.712, 0.923] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.008 | 0.121 | 0.014 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.004 | 0.167 | 0.008 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.002 | 0.083 | 0.003 | 36 |
| USAGE | 0.005 | 0.118 | 0.010 | 186 |
| ACCESS | 0.005 | 0.097 | 0.009 | 134 |
| PLATFORM | 0.002 | 0.067 | 0.004 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.376 | 0.010 | 0.026 |
| 20% | 0.321 | 0.008 | 0.041 |
| 30% | 0.286 | 0.006 | 0.047 |
| 40% | 0.259 | 0.006 | 0.060 |
| 50% | 0.236 | 0.005 | 0.062 |
| 60% | 0.216 | 0.005 | 0.073 |
| 70% | 0.199 | 0.005 | 0.083 |
| 80% | 0.180 | 0.004 | 0.083 |
| 90% | 0.159 | 0.004 | 0.085 |
| 100% | 0.104 | 0.003 | 0.085 |
