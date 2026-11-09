# Hand-labelled dev: ablation-1-docs-120-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-docs-120-seed1.jsonl` (ablation-1-docs-120-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.305 | [0.197, 0.455] |
| Exact span F1 | 0.339 | [0.233, 0.480] |
| Exact span precision | 0.238 | [0.151, 0.387] |
| Exact span recall | 0.588 | [0.444, 0.727] |
| Role macro-F1 (roles with gold support) | 0.204 | [0.164, 0.500] |
| Category macro-F1 | 0.199 | [0.130, 0.404] |
| Group exact-match F1 | 0.167 | [0.000, 0.421] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.545 | [0.360, 0.698] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 0.900 | [0.700, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.303 | 0.625 | 0.408 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.222 | 0.667 | 0.333 | 9 |
| ACCESS | 0.375 | 0.600 | 0.462 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.916 | 0.750 | 0.176 |
| 19% | 0.784 | 0.500 | 0.235 |
| 31% | 0.710 | 0.385 | 0.294 |
| 40% | 0.542 | 0.294 | 0.294 |
| 50% | 0.522 | 0.286 | 0.353 |
| 60% | 0.507 | 0.280 | 0.412 |
| 69% | 0.498 | 0.241 | 0.412 |
| 81% | 0.447 | 0.235 | 0.471 |
| 90% | 0.391 | 0.211 | 0.471 |
| 100% | 0.307 | 0.214 | 0.529 |
