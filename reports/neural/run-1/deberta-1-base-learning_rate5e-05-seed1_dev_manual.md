# Hand-labelled dev: deberta-1-base-learning_rate5e-05-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-1-base-learning_rate5e-05-seed1.jsonl` (deberta-1-base-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.047 | [0.021, 0.066] |
| Exact span F1 | 0.054 | [0.027, 0.077] |
| Exact span precision | 0.029 | [0.014, 0.042] |
| Exact span recall | 0.412 | [0.214, 0.625] |
| Role macro-F1 (roles with gold support) | 0.030 | [0.015, 0.080] |
| Category macro-F1 | 0.036 | [0.013, 0.075] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.847 | [0.766, 0.911] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 0.857 | [0.625, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.033 | 0.375 | 0.060 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.036 | 0.556 | 0.068 | 9 |
| ACCESS | 0.042 | 0.400 | 0.075 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.562 | 0.083 | 0.118 |
| 20% | 0.499 | 0.062 | 0.176 |
| 30% | 0.451 | 0.069 | 0.294 |
| 40% | 0.422 | 0.062 | 0.353 |
| 50% | 0.394 | 0.050 | 0.353 |
| 60% | 0.358 | 0.041 | 0.353 |
| 70% | 0.307 | 0.036 | 0.353 |
| 80% | 0.273 | 0.031 | 0.353 |
| 90% | 0.228 | 0.028 | 0.353 |
| 100% | 0.158 | 0.025 | 0.353 |
