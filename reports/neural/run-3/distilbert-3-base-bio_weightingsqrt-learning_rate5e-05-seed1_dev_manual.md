# Hand-labelled dev: distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed1.jsonl` (distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.214 | [0.057, 0.333] |
| Exact span F1 | 0.214 | [0.057, 0.333] |
| Exact span precision | 0.154 | [0.043, 0.241] |
| Exact span recall | 0.353 | [0.077, 0.611] |
| Role macro-F1 (roles with gold support) | 0.133 | [0.038, 0.370] |
| Category macro-F1 | 0.142 | [0.056, 0.265] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.552 | [0.280, 0.824] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.207 | 0.375 | 0.267 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.111 | 0.333 | 0.167 | 9 |
| ACCESS | 0.300 | 0.600 | 0.400 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.842 | 0.500 | 0.118 |
| 21% | 0.635 | 0.500 | 0.235 |
| 31% | 0.588 | 0.417 | 0.294 |
| 41% | 0.561 | 0.312 | 0.294 |
| 51% | 0.543 | 0.250 | 0.294 |
| 59% | 0.522 | 0.217 | 0.294 |
| 69% | 0.499 | 0.222 | 0.353 |
| 79% | 0.425 | 0.194 | 0.353 |
| 90% | 0.366 | 0.171 | 0.353 |
| 100% | 0.248 | 0.154 | 0.353 |
