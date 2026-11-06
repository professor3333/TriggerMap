# Hand-labelled dev: distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed0

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed0.jsonl` (distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.107 | [0.041, 0.181] |
| Exact span F1 | 0.107 | [0.041, 0.181] |
| Exact span precision | 0.063 | [0.024, 0.109] |
| Exact span recall | 0.353 | [0.125, 0.611] |
| Role macro-F1 (roles with gold support) | 0.061 | [0.023, 0.184] |
| Category macro-F1 | 0.094 | [0.052, 0.230] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.756 | [0.677, 0.831] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.073 | 0.375 | 0.122 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.032 | 0.222 | 0.056 | 9 |
| ACCESS | 0.200 | 0.800 | 0.320 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.487 | 0.000 | 0.000 |
| 20% | 0.447 | 0.105 | 0.118 |
| 29% | 0.424 | 0.071 | 0.118 |
| 40% | 0.380 | 0.079 | 0.176 |
| 51% | 0.352 | 0.083 | 0.235 |
| 60% | 0.335 | 0.088 | 0.294 |
| 69% | 0.314 | 0.076 | 0.294 |
| 80% | 0.268 | 0.079 | 0.353 |
| 91% | 0.234 | 0.070 | 0.353 |
| 100% | 0.159 | 0.063 | 0.353 |
