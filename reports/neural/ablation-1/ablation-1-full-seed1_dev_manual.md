# Hand-labelled dev: ablation-1-full-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-full-seed1.jsonl` (ablation-1-full-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.281 | [0.120, 0.500] |
| Exact span F1 | 0.351 | [0.233, 0.558] |
| Exact span precision | 0.250 | [0.150, 0.455] |
| Exact span recall | 0.588 | [0.450, 0.778] |
| Role macro-F1 (roles with gold support) | 0.188 | [0.130, 0.490] |
| Category macro-F1 | 0.294 | [0.170, 0.651] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.500 | [0.327, 0.692] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 0.900 | [0.625, 1.000] |
| Role accuracy on exactly matched spans | 0.900 | [0.667, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.281 | 0.562 | 0.375 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.250 | 1.000 | 0.400 | 1 |
| USAGE | 0.217 | 0.556 | 0.312 | 9 |
| ACCESS | 0.375 | 0.600 | 0.462 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.934 | 1.000 | 0.235 |
| 20% | 0.886 | 0.625 | 0.294 |
| 30% | 0.835 | 0.417 | 0.294 |
| 40% | 0.752 | 0.375 | 0.353 |
| 50% | 0.701 | 0.400 | 0.471 |
| 60% | 0.632 | 0.333 | 0.471 |
| 70% | 0.558 | 0.286 | 0.471 |
| 80% | 0.494 | 0.250 | 0.471 |
| 90% | 0.425 | 0.222 | 0.471 |
| 100% | 0.270 | 0.200 | 0.471 |
