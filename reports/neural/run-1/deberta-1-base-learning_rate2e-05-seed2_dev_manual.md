# Hand-labelled dev: deberta-1-base-learning_rate2e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-1-base-learning_rate2e-05-seed2.jsonl` (deberta-1-base-learning_rate2e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.010 | [0.000, 0.028] |
| Exact span F1 | 0.010 | [0.000, 0.028] |
| Exact span precision | 0.005 | [0.000, 0.015] |
| Exact span recall | 0.118 | [0.000, 0.235] |
| Role macro-F1 (roles with gold support) | 0.006 | [0.000, 0.029] |
| Category macro-F1 | 0.005 | [0.000, 0.017] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.865 | [0.809, 0.902] |
| Reversed meaning rate (lower is better) | 0.022 | [0.000, 0.061] |
| Category accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.007 | 0.125 | 0.013 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.010 | 0.222 | 0.019 | 9 |
| ACCESS | 0.000 | 0.000 | 0.000 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.448 | 0.026 | 0.059 |
| 20% | 0.373 | 0.013 | 0.059 |
| 30% | 0.341 | 0.008 | 0.059 |
| 40% | 0.308 | 0.006 | 0.059 |
| 50% | 0.281 | 0.010 | 0.118 |
| 60% | 0.252 | 0.008 | 0.118 |
| 70% | 0.223 | 0.007 | 0.118 |
| 80% | 0.200 | 0.006 | 0.118 |
| 90% | 0.173 | 0.006 | 0.118 |
| 100% | 0.133 | 0.005 | 0.118 |
