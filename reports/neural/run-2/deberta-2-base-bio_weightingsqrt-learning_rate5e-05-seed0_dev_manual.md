# Hand-labelled dev: deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0.jsonl` (deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.265 | [0.174, 0.400] |
| Exact span F1 | 0.294 | [0.208, 0.462] |
| Exact span precision | 0.196 | [0.130, 0.342] |
| Exact span recall | 0.588 | [0.450, 0.778] |
| Role macro-F1 (roles with gold support) | 0.158 | [0.118, 0.417] |
| Category macro-F1 | 0.285 | [0.221, 0.563] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.683 | [0.500, 0.791] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 0.900 | [0.667, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.220 | 0.562 | 0.316 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.200 | 1.000 | 0.333 | 1 |
| USAGE | 0.162 | 0.667 | 0.261 | 9 |
| ACCESS | 0.500 | 0.600 | 0.545 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.831 | 0.600 | 0.176 |
| 20% | 0.733 | 0.500 | 0.294 |
| 29% | 0.648 | 0.400 | 0.353 |
| 39% | 0.609 | 0.350 | 0.412 |
| 51% | 0.527 | 0.308 | 0.471 |
| 61% | 0.512 | 0.290 | 0.529 |
| 71% | 0.470 | 0.250 | 0.529 |
| 80% | 0.411 | 0.220 | 0.529 |
| 90% | 0.318 | 0.196 | 0.529 |
| 100% | 0.209 | 0.176 | 0.529 |
