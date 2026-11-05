# Hand-labelled dev: distilbert-1-base-learning_rate5e-05-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/distilbert-1-base-learning_rate5e-05-seed1.jsonl` (distilbert-1-base-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.012 | [0.000, 0.039] |
| Exact span F1 | 0.012 | [0.000, 0.039] |
| Exact span precision | 0.006 | [0.000, 0.020] |
| Exact span recall | 0.118 | [0.000, 0.400] |
| Role macro-F1 (roles with gold support) | 0.010 | [0.000, 0.052] |
| Category macro-F1 | 0.010 | [0.000, 0.034] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.827 | [0.748, 0.881] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.011 | 0.125 | 0.021 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.000 | 0.000 | 0.000 | 9 |
| ACCESS | 0.022 | 0.400 | 0.041 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.623 | 0.032 | 0.059 |
| 20% | 0.519 | 0.016 | 0.059 |
| 30% | 0.461 | 0.011 | 0.059 |
| 40% | 0.408 | 0.008 | 0.059 |
| 50% | 0.378 | 0.006 | 0.059 |
| 60% | 0.346 | 0.005 | 0.059 |
| 70% | 0.301 | 0.005 | 0.059 |
| 80% | 0.278 | 0.004 | 0.059 |
| 90% | 0.233 | 0.004 | 0.059 |
| 100% | 0.148 | 0.006 | 0.118 |
