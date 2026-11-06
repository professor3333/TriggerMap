# Hand-labelled dev: distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed0

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed0.jsonl` (distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.135 | [0.079, 0.205] |
| Exact span F1 | 0.135 | [0.079, 0.205] |
| Exact span precision | 0.080 | [0.045, 0.127] |
| Exact span recall | 0.412 | [0.222, 0.636] |
| Role macro-F1 (roles with gold support) | 0.078 | [0.046, 0.215] |
| Category macro-F1 | 0.101 | [0.062, 0.224] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.743 | [0.649, 0.851] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.095 | 0.438 | 0.156 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.056 | 0.333 | 0.095 | 9 |
| ACCESS | 0.190 | 0.800 | 0.308 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.510 | 0.000 | 0.000 |
| 20% | 0.476 | 0.118 | 0.118 |
| 30% | 0.426 | 0.077 | 0.118 |
| 40% | 0.406 | 0.114 | 0.235 |
| 51% | 0.368 | 0.091 | 0.235 |
| 60% | 0.352 | 0.115 | 0.353 |
| 70% | 0.329 | 0.115 | 0.412 |
| 80% | 0.282 | 0.100 | 0.412 |
| 90% | 0.245 | 0.090 | 0.412 |
| 100% | 0.169 | 0.080 | 0.412 |
