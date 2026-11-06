# Agreement with model drafts (held-out half): distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed0.jsonl` (distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.037 | [0.020, 0.059] |
| Exact span F1 | 0.054 | [0.032, 0.083] |
| Exact span precision | 0.032 | [0.018, 0.050] |
| Exact span recall | 0.179 | [0.113, 0.256] |
| Role macro-F1 (roles with gold support) | 0.024 | [0.009, 0.059] |
| Category macro-F1 | 0.031 | [0.014, 0.050] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.736 | [0.675, 0.782] |
| Reversed meaning rate (lower is better) | 0.040 | [0.006, 0.082] |
| Category accuracy on exactly matched spans | 0.720 | [0.529, 0.889] |
| Role accuracy on exactly matched spans | 0.880 | [0.733, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.031 | 0.175 | 0.053 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.027 | 0.100 | 0.043 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 18 |
| USAGE | 0.018 | 0.148 | 0.033 | 54 |
| ACCESS | 0.035 | 0.167 | 0.058 | 54 |
| PLATFORM | 0.022 | 0.071 | 0.034 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.482 | 0.064 | 0.036 |
| 20% | 0.449 | 0.051 | 0.057 |
| 30% | 0.427 | 0.047 | 0.079 |
| 40% | 0.403 | 0.045 | 0.100 |
| 50% | 0.374 | 0.041 | 0.114 |
| 60% | 0.346 | 0.034 | 0.114 |
| 70% | 0.321 | 0.031 | 0.121 |
| 80% | 0.284 | 0.027 | 0.121 |
| 90% | 0.241 | 0.024 | 0.121 |
| 100% | 0.153 | 0.022 | 0.121 |
