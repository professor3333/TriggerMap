# Held-out agreement, deberta at target precision 0.35 (threshold 0.8956)

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/calibration/predictions/deberta-0.35.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.201 | [0.129, 0.271] |
| Exact span F1 | 0.221 | [0.140, 0.295] |
| Exact span precision | 0.373 | [0.259, 0.473] |
| Exact span recall | 0.157 | [0.095, 0.222] |
| Role macro-F1 (roles with gold support) | 0.062 | [0.042, 0.092] |
| Category macro-F1 | 0.123 | [0.079, 0.162] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.035 | [0.000, 0.107] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.379 | [0.264, 0.500] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 0.909 | [0.778, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.379 | 0.183 | 0.247 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 18 |
| USAGE | 0.262 | 0.204 | 0.229 | 54 |
| ACCESS | 0.643 | 0.167 | 0.265 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.995 | 0.167 | 0.007 |
| 20% | 0.993 | 0.333 | 0.029 |
| 31% | 0.989 | 0.500 | 0.064 |
| 41% | 0.982 | 0.542 | 0.093 |
| 51% | 0.973 | 0.500 | 0.107 |
| 59% | 0.966 | 0.457 | 0.114 |
| 69% | 0.953 | 0.415 | 0.121 |
| 80% | 0.935 | 0.362 | 0.121 |
| 90% | 0.921 | 0.358 | 0.136 |
| 100% | 0.899 | 0.339 | 0.143 |
