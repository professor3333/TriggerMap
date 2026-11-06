# Held-out agreement, deberta at target precision 0.30 (threshold 0.8575)

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/calibration/predictions/deberta-0.30.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.207 | [0.141, 0.275] |
| Exact span F1 | 0.225 | [0.151, 0.296] |
| Exact span precision | 0.329 | [0.232, 0.418] |
| Exact span recall | 0.171 | [0.110, 0.237] |
| Role macro-F1 (roles with gold support) | 0.063 | [0.045, 0.093] |
| Category macro-F1 | 0.145 | [0.093, 0.187] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.035 | [0.000, 0.107] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.391 | [0.284, 0.500] |
| Reversed meaning rate (lower is better) | 0.047 | [0.000, 0.132] |
| Category accuracy on exactly matched spans | 0.917 | [0.800, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.348 | 0.200 | 0.254 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.333 | 0.056 | 0.095 | 18 |
| USAGE | 0.255 | 0.222 | 0.238 | 54 |
| ACCESS | 0.474 | 0.167 | 0.247 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.995 | 0.143 | 0.007 |
| 21% | 0.992 | 0.400 | 0.043 |
| 30% | 0.985 | 0.545 | 0.086 |
| 40% | 0.974 | 0.483 | 0.100 |
| 49% | 0.964 | 0.444 | 0.114 |
| 60% | 0.942 | 0.386 | 0.121 |
| 70% | 0.923 | 0.353 | 0.129 |
| 79% | 0.900 | 0.328 | 0.136 |
| 90% | 0.877 | 0.333 | 0.157 |
| 100% | 0.858 | 0.301 | 0.157 |
