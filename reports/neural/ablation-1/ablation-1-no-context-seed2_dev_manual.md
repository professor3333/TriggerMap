# Hand-labelled dev: ablation-1-no-context-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-no-context-seed2.jsonl` (ablation-1-no-context-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.222 | [0.038, 0.455] |
| Exact span F1 | 0.254 | [0.073, 0.500] |
| Exact span precision | 0.174 | [0.048, 0.375] |
| Exact span recall | 0.471 | [0.154, 0.812] |
| Role macro-F1 (roles with gold support) | 0.127 | [0.026, 0.423] |
| Category macro-F1 | 0.237 | [0.100, 0.564] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.462 | [0.300, 0.625] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 0.875 | [0.400, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.179 | 0.438 | 0.255 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.200 | 1.000 | 0.333 | 1 |
| USAGE | 0.161 | 0.556 | 0.250 | 9 |
| ACCESS | 0.333 | 0.400 | 0.364 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.970 | 1.000 | 0.294 |
| 20% | 0.927 | 0.556 | 0.294 |
| 30% | 0.832 | 0.429 | 0.353 |
| 39% | 0.787 | 0.389 | 0.412 |
| 50% | 0.709 | 0.304 | 0.412 |
| 61% | 0.606 | 0.250 | 0.412 |
| 70% | 0.564 | 0.219 | 0.412 |
| 80% | 0.508 | 0.189 | 0.412 |
| 89% | 0.358 | 0.171 | 0.412 |
| 100% | 0.249 | 0.152 | 0.412 |
