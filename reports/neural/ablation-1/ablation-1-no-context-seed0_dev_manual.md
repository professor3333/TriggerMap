# Hand-labelled dev: ablation-1-no-context-seed0

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-no-context-seed0.jsonl` (ablation-1-no-context-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.291 | [0.091, 0.531] |
| Exact span F1 | 0.364 | [0.203, 0.596] |
| Exact span precision | 0.263 | [0.150, 0.457] |
| Exact span recall | 0.588 | [0.333, 0.895] |
| Role macro-F1 (roles with gold support) | 0.196 | [0.108, 0.556] |
| Category macro-F1 | 0.326 | [0.208, 0.673] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.222 | [0.000, 0.455] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.500 | [0.304, 0.655] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 0.900 | [0.600, 1.000] |
| Role accuracy on exactly matched spans | 0.900 | [0.625, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.300 | 0.562 | 0.391 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.250 | 1.000 | 0.400 | 1 |
| USAGE | 0.208 | 0.556 | 0.303 | 9 |
| ACCESS | 0.600 | 0.600 | 0.600 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.982 | 1.000 | 0.235 |
| 21% | 0.942 | 0.875 | 0.412 |
| 29% | 0.895 | 0.636 | 0.412 |
| 39% | 0.834 | 0.467 | 0.412 |
| 50% | 0.684 | 0.368 | 0.412 |
| 61% | 0.637 | 0.348 | 0.471 |
| 71% | 0.569 | 0.296 | 0.471 |
| 79% | 0.539 | 0.267 | 0.471 |
| 89% | 0.441 | 0.235 | 0.471 |
| 100% | 0.330 | 0.211 | 0.471 |
