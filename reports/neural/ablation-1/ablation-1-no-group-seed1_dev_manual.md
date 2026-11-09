# Hand-labelled dev: ablation-1-no-group-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-no-group-seed1.jsonl` (ablation-1-no-group-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.310 | [0.140, 0.576] |
| Exact span F1 | 0.310 | [0.140, 0.576] |
| Exact span precision | 0.220 | [0.098, 0.457] |
| Exact span recall | 0.529 | [0.238, 0.818] |
| Role macro-F1 (roles with gold support) | 0.176 | [0.093, 0.538] |
| Category macro-F1 | 0.251 | [0.142, 0.537] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.222 | [0.000, 0.455] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.571 | [0.250, 0.750] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.257 | 0.562 | 0.353 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.185 | 0.556 | 0.278 | 9 |
| ACCESS | 0.667 | 0.800 | 0.727 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.991 | 1.000 | 0.235 |
| 20% | 0.986 | 0.875 | 0.412 |
| 29% | 0.969 | 0.667 | 0.471 |
| 39% | 0.877 | 0.500 | 0.471 |
| 49% | 0.811 | 0.450 | 0.529 |
| 61% | 0.672 | 0.360 | 0.529 |
| 71% | 0.625 | 0.310 | 0.529 |
| 80% | 0.584 | 0.273 | 0.529 |
| 90% | 0.502 | 0.243 | 0.529 |
| 100% | 0.389 | 0.220 | 0.529 |
