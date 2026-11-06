# Held-out agreement, crf at target precision 0.30 (threshold 0.4839)

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/calibration/predictions/crf-0.30.jsonl` (crf-batches-01-02)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.107 | [0.041, 0.169] |
| Exact span F1 | 0.130 | [0.060, 0.192] |
| Exact span precision | 0.379 | [0.179, 0.607] |
| Exact span recall | 0.079 | [0.035, 0.120] |
| Role macro-F1 (roles with gold support) | 0.076 | [0.022, 0.157] |
| Category macro-F1 | 0.092 | [0.032, 0.139] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.035 | [0.000, 0.078] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.280 | [0.111, 0.500] |
| Reversed meaning rate (lower is better) | 0.100 | [0.000, 0.286] |
| Category accuracy on exactly matched spans | 0.818 | [0.500, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.400 | 0.083 | 0.138 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.500 | 0.100 | 0.167 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 18 |
| USAGE | 0.143 | 0.037 | 0.059 | 54 |
| ACCESS | 0.545 | 0.111 | 0.185 | 54 |
| PLATFORM | 0.500 | 0.071 | 0.125 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.808 | 1.000 | 0.021 |
| 21% | 0.781 | 0.667 | 0.029 |
| 31% | 0.751 | 0.444 | 0.029 |
| 41% | 0.713 | 0.500 | 0.043 |
| 48% | 0.694 | 0.500 | 0.050 |
| 59% | 0.677 | 0.471 | 0.057 |
| 69% | 0.601 | 0.400 | 0.057 |
| 79% | 0.545 | 0.348 | 0.057 |
| 90% | 0.533 | 0.308 | 0.057 |
| 100% | 0.497 | 0.310 | 0.064 |
