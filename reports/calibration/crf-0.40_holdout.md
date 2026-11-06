# Held-out agreement, crf at target precision 0.40 (threshold 0.6599)

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/calibration/predictions/crf-0.40.jsonl` (crf-batches-01-02)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.102 | [0.042, 0.157] |
| Exact span F1 | 0.102 | [0.042, 0.157] |
| Exact span precision | 0.471 | [0.200, 0.750] |
| Exact span recall | 0.057 | [0.024, 0.090] |
| Role macro-F1 (roles with gold support) | 0.068 | [0.015, 0.149] |
| Category macro-F1 | 0.089 | [0.031, 0.136] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.018 | [0.000, 0.052] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.231 | [0.000, 0.545] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.538 | 0.058 | 0.105 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.500 | 0.100 | 0.167 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 18 |
| USAGE | 0.167 | 0.019 | 0.033 | 54 |
| ACCESS | 0.667 | 0.111 | 0.190 | 54 |
| PLATFORM | 1.000 | 0.071 | 0.133 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 12% | 0.880 | 1.000 | 0.014 |
| 18% | 0.808 | 1.000 | 0.021 |
| 29% | 0.789 | 0.800 | 0.029 |
| 41% | 0.771 | 0.571 | 0.029 |
| 47% | 0.754 | 0.500 | 0.029 |
| 59% | 0.725 | 0.400 | 0.029 |
| 71% | 0.713 | 0.500 | 0.043 |
| 82% | 0.694 | 0.500 | 0.050 |
| 88% | 0.683 | 0.467 | 0.050 |
| 100% | 0.677 | 0.471 | 0.057 |
