# Held-out agreement, deberta at target precision 0.40 (threshold 0.9616)

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/calibration/predictions/deberta-0.40.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.182 | [0.101, 0.262] |
| Exact span F1 | 0.193 | [0.103, 0.280] |
| Exact span precision | 0.472 | [0.290, 0.625] |
| Exact span recall | 0.121 | [0.062, 0.184] |
| Role macro-F1 (roles with gold support) | 0.054 | [0.031, 0.083] |
| Category macro-F1 | 0.110 | [0.061, 0.152] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.035 | [0.000, 0.107] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.333 | [0.200, 0.487] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 0.941 | [0.842, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.472 | 0.142 | 0.218 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 18 |
| USAGE | 0.370 | 0.185 | 0.247 | 54 |
| ACCESS | 0.750 | 0.111 | 0.194 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.997 | 0.250 | 0.007 |
| 19% | 0.995 | 0.143 | 0.007 |
| 31% | 0.994 | 0.273 | 0.021 |
| 39% | 0.992 | 0.357 | 0.036 |
| 50% | 0.989 | 0.500 | 0.064 |
| 61% | 0.985 | 0.545 | 0.086 |
| 69% | 0.979 | 0.520 | 0.093 |
| 81% | 0.974 | 0.483 | 0.100 |
| 89% | 0.970 | 0.469 | 0.107 |
| 100% | 0.964 | 0.444 | 0.114 |
