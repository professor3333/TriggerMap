# Hand-labelled dev: deberta-1-base-learning_rate5e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-1-base-learning_rate5e-05-seed2.jsonl` (deberta-1-base-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.042 | [0.008, 0.092] |
| Exact span F1 | 0.049 | [0.017, 0.097] |
| Exact span precision | 0.026 | [0.009, 0.053] |
| Exact span recall | 0.412 | [0.211, 0.579] |
| Role macro-F1 (roles with gold support) | 0.034 | [0.014, 0.113] |
| Category macro-F1 | 0.031 | [0.007, 0.104] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.847 | [0.784, 0.897] |
| Reversed meaning rate (lower is better) | 0.031 | [0.000, 0.103] |
| Category accuracy on exactly matched spans | 0.857 | [0.400, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.037 | 0.438 | 0.068 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.029 | 0.444 | 0.054 | 9 |
| ACCESS | 0.039 | 0.400 | 0.071 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.625 | 0.037 | 0.059 |
| 20% | 0.538 | 0.037 | 0.118 |
| 30% | 0.486 | 0.037 | 0.176 |
| 40% | 0.454 | 0.037 | 0.235 |
| 50% | 0.407 | 0.037 | 0.294 |
| 60% | 0.382 | 0.037 | 0.353 |
| 70% | 0.339 | 0.032 | 0.353 |
| 80% | 0.295 | 0.028 | 0.353 |
| 90% | 0.245 | 0.025 | 0.353 |
| 100% | 0.121 | 0.022 | 0.353 |
