# Held-out agreement, crf at target precision 0.35 (threshold 0.6149)

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/calibration/predictions/crf-0.35.jsonl` (crf-batches-01-02)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.101 | [0.042, 0.157] |
| Exact span F1 | 0.101 | [0.042, 0.157] |
| Exact span precision | 0.444 | [0.188, 0.733] |
| Exact span recall | 0.057 | [0.024, 0.090] |
| Role macro-F1 (roles with gold support) | 0.068 | [0.015, 0.149] |
| Category macro-F1 | 0.089 | [0.031, 0.136] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.018 | [0.000, 0.052] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.214 | [0.000, 0.500] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.500 | 0.058 | 0.104 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.500 | 0.100 | 0.167 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 18 |
| USAGE | 0.143 | 0.019 | 0.033 | 54 |
| ACCESS | 0.667 | 0.111 | 0.190 | 54 |
| PLATFORM | 1.000 | 0.071 | 0.133 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.880 | 1.000 | 0.014 |
| 22% | 0.795 | 0.750 | 0.021 |
| 28% | 0.789 | 0.800 | 0.029 |
| 39% | 0.771 | 0.571 | 0.029 |
| 50% | 0.751 | 0.444 | 0.029 |
| 61% | 0.719 | 0.455 | 0.036 |
| 72% | 0.696 | 0.462 | 0.043 |
| 78% | 0.694 | 0.500 | 0.050 |
| 89% | 0.682 | 0.500 | 0.057 |
| 100% | 0.622 | 0.444 | 0.057 |
