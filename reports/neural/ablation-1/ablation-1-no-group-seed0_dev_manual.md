# Hand-labelled dev: ablation-1-no-group-seed0

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-no-group-seed0.jsonl` (ablation-1-no-group-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.355 | [0.207, 0.545] |
| Exact span F1 | 0.387 | [0.250, 0.593] |
| Exact span precision | 0.267 | [0.167, 0.438] |
| Exact span recall | 0.706 | [0.471, 1.000] |
| Role macro-F1 (roles with gold support) | 0.216 | [0.137, 0.571] |
| Category macro-F1 | 0.442 | [0.319, 0.781] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.514 | [0.333, 0.667] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 0.917 | [0.667, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.314 | 0.688 | 0.431 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.167 | 1.000 | 0.286 | 1 |
| USAGE | 0.200 | 0.667 | 0.308 | 9 |
| ACCESS | 1.000 | 0.800 | 0.889 | 5 |
| PLATFORM | 0.200 | 0.500 | 0.286 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 9% | 0.984 | 0.750 | 0.176 |
| 20% | 0.943 | 0.667 | 0.353 |
| 31% | 0.930 | 0.643 | 0.529 |
| 40% | 0.883 | 0.500 | 0.529 |
| 49% | 0.804 | 0.409 | 0.529 |
| 60% | 0.747 | 0.333 | 0.529 |
| 71% | 0.622 | 0.344 | 0.647 |
| 80% | 0.558 | 0.306 | 0.647 |
| 89% | 0.497 | 0.275 | 0.647 |
| 100% | 0.276 | 0.244 | 0.647 |
