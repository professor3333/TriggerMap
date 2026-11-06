# Hand-labelled dev: distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.279 | [0.114, 0.471] |
| Exact span F1 | 0.279 | [0.114, 0.471] |
| Exact span precision | 0.231 | [0.095, 0.450] |
| Exact span recall | 0.353 | [0.125, 0.611] |
| Role macro-F1 (roles with gold support) | 0.158 | [0.069, 0.471] |
| Category macro-F1 | 0.220 | [0.135, 0.462] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.636 | [0.300, 0.826] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.273 | 0.375 | 0.316 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.118 | 0.222 | 0.154 | 9 |
| ACCESS | 0.667 | 0.800 | 0.727 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 12% | 0.969 | 0.667 | 0.118 |
| 19% | 0.944 | 0.800 | 0.235 |
| 31% | 0.830 | 0.625 | 0.294 |
| 38% | 0.727 | 0.600 | 0.353 |
| 50% | 0.639 | 0.462 | 0.353 |
| 62% | 0.521 | 0.375 | 0.353 |
| 69% | 0.494 | 0.333 | 0.353 |
| 81% | 0.448 | 0.286 | 0.353 |
| 88% | 0.299 | 0.261 | 0.353 |
| 100% | 0.267 | 0.231 | 0.353 |
