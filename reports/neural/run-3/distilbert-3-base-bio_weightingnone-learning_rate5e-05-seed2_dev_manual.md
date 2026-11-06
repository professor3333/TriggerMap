# Hand-labelled dev: distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed2.jsonl` (distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.286 | [0.071, 0.474] |
| Exact span F1 | 0.286 | [0.071, 0.474] |
| Exact span precision | 0.278 | [0.077, 0.500] |
| Exact span recall | 0.294 | [0.067, 0.526] |
| Role macro-F1 (roles with gold support) | 0.152 | [0.042, 0.424] |
| Category macro-F1 | 0.233 | [0.087, 0.441] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.471 | [0.286, 0.619] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.294 | 0.312 | 0.303 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.154 | 0.222 | 0.182 | 9 |
| ACCESS | 1.000 | 0.600 | 0.750 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.604 | 0.500 | 0.059 |
| 22% | 0.535 | 0.500 | 0.118 |
| 28% | 0.526 | 0.400 | 0.118 |
| 39% | 0.480 | 0.429 | 0.176 |
| 50% | 0.450 | 0.444 | 0.235 |
| 61% | 0.446 | 0.364 | 0.235 |
| 72% | 0.398 | 0.385 | 0.294 |
| 78% | 0.396 | 0.357 | 0.294 |
| 89% | 0.366 | 0.312 | 0.294 |
| 100% | 0.338 | 0.278 | 0.294 |
