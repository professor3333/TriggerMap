# Hand-labelled dev: distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed2.jsonl` (distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.078 | [0.014, 0.161] |
| Exact span F1 | 0.078 | [0.014, 0.161] |
| Exact span precision | 0.047 | [0.008, 0.104] |
| Exact span recall | 0.235 | [0.043, 0.500] |
| Role macro-F1 (roles with gold support) | 0.045 | [0.008, 0.170] |
| Category macro-F1 | 0.065 | [0.014, 0.250] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.708 | [0.597, 0.829] |
| Reversed meaning rate (lower is better) | 0.083 | [0.000, 0.190] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.056 | 0.250 | 0.091 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.042 | 0.222 | 0.070 | 9 |
| ACCESS | 0.125 | 0.400 | 0.190 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.481 | 0.222 | 0.118 |
| 20% | 0.436 | 0.176 | 0.176 |
| 30% | 0.406 | 0.154 | 0.235 |
| 40% | 0.381 | 0.118 | 0.235 |
| 50% | 0.347 | 0.093 | 0.235 |
| 60% | 0.310 | 0.077 | 0.235 |
| 70% | 0.281 | 0.067 | 0.235 |
| 80% | 0.269 | 0.058 | 0.235 |
| 90% | 0.237 | 0.052 | 0.235 |
| 100% | 0.210 | 0.047 | 0.235 |
