# Hand-labelled dev: deberta-1-base-learning_rate2e-05-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-1-base-learning_rate2e-05-seed1.jsonl` (deberta-1-base-learning_rate2e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.005 | [0.000, 0.016] |
| Exact span F1 | 0.010 | [0.000, 0.022] |
| Exact span precision | 0.005 | [0.000, 0.012] |
| Exact span recall | 0.118 | [0.000, 0.267] |
| Role macro-F1 (roles with gold support) | 0.004 | [0.000, 0.019] |
| Category macro-F1 | 0.007 | [0.000, 0.018] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.856 | [0.790, 0.903] |
| Reversed meaning rate (lower is better) | 0.070 | [0.000, 0.200] |
| Category accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 0.500 | [0.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.004 | 0.062 | 0.007 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.005 | 0.111 | 0.009 | 9 |
| ACCESS | 0.010 | 0.200 | 0.019 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.382 | 0.000 | 0.000 |
| 20% | 0.321 | 0.000 | 0.000 |
| 30% | 0.289 | 0.000 | 0.000 |
| 40% | 0.268 | 0.000 | 0.000 |
| 50% | 0.244 | 0.000 | 0.000 |
| 60% | 0.222 | 0.000 | 0.000 |
| 70% | 0.203 | 0.000 | 0.000 |
| 80% | 0.185 | 0.000 | 0.000 |
| 90% | 0.165 | 0.000 | 0.000 |
| 100% | 0.117 | 0.003 | 0.059 |
