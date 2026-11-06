# Hand-labelled dev: deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.242 | [0.070, 0.435] |
| Exact span F1 | 0.273 | [0.105, 0.471] |
| Exact span precision | 0.184 | [0.069, 0.348] |
| Exact span recall | 0.529 | [0.235, 0.818] |
| Role macro-F1 (roles with gold support) | 0.138 | [0.042, 0.433] |
| Category macro-F1 | 0.283 | [0.111, 0.607] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.548 | [0.351, 0.735] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 0.889 | [0.500, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.190 | 0.500 | 0.276 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.333 | 1.000 | 0.500 | 1 |
| USAGE | 0.167 | 0.667 | 0.267 | 9 |
| ACCESS | 0.333 | 0.400 | 0.364 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.797 | 0.600 | 0.176 |
| 20% | 0.695 | 0.500 | 0.294 |
| 31% | 0.605 | 0.400 | 0.353 |
| 41% | 0.554 | 0.350 | 0.412 |
| 49% | 0.524 | 0.333 | 0.471 |
| 59% | 0.494 | 0.276 | 0.471 |
| 69% | 0.461 | 0.235 | 0.471 |
| 80% | 0.412 | 0.205 | 0.471 |
| 90% | 0.366 | 0.182 | 0.471 |
| 100% | 0.233 | 0.163 | 0.471 |
