# Hand-labelled dev: ablation-1-no-context-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-no-context-seed1.jsonl` (ablation-1-no-context-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.254 | [0.118, 0.448] |
| Exact span F1 | 0.286 | [0.152, 0.500] |
| Exact span precision | 0.196 | [0.098, 0.389] |
| Exact span recall | 0.529 | [0.300, 0.778] |
| Role macro-F1 (roles with gold support) | 0.148 | [0.074, 0.440] |
| Category macro-F1 | 0.265 | [0.179, 0.567] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.553 | [0.323, 0.744] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 0.889 | [0.600, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.211 | 0.500 | 0.296 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.143 | 1.000 | 0.250 | 1 |
| USAGE | 0.172 | 0.556 | 0.263 | 9 |
| ACCESS | 0.500 | 0.600 | 0.545 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.964 | 0.800 | 0.235 |
| 20% | 0.932 | 0.556 | 0.294 |
| 30% | 0.887 | 0.429 | 0.353 |
| 39% | 0.805 | 0.389 | 0.412 |
| 50% | 0.728 | 0.304 | 0.412 |
| 61% | 0.656 | 0.250 | 0.412 |
| 70% | 0.627 | 0.219 | 0.412 |
| 80% | 0.533 | 0.216 | 0.471 |
| 89% | 0.463 | 0.195 | 0.471 |
| 100% | 0.384 | 0.174 | 0.471 |
