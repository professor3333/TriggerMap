# Agreement with model drafts: distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed1.jsonl` (distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.042 | [0.029, 0.054] |
| Exact span F1 | 0.058 | [0.042, 0.072] |
| Exact span precision | 0.037 | [0.027, 0.046] |
| Exact span recall | 0.137 | [0.098, 0.174] |
| Role macro-F1 (roles with gold support) | 0.040 | [0.020, 0.067] |
| Category macro-F1 | 0.038 | [0.026, 0.050] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.013 | [0.000, 0.034] |
| Complete-document exact match, documents without conditions | 0.471 | [0.231, 0.727] |
| False prerequisite rate (lower is better) | 0.662 | [0.624, 0.694] |
| Reversed meaning rate (lower is better) | 0.053 | [0.025, 0.087] |
| Category accuracy on exactly matched spans | 0.887 | [0.804, 0.966] |
| Role accuracy on exactly matched spans | 0.830 | [0.702, 0.964] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.033 | 0.118 | 0.051 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.064 | 0.333 | 0.107 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.017 | 0.056 | 0.026 | 36 |
| USAGE | 0.028 | 0.118 | 0.045 | 186 |
| ACCESS | 0.051 | 0.172 | 0.079 | 134 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.510 | 0.021 | 0.008 |
| 20% | 0.474 | 0.024 | 0.018 |
| 30% | 0.449 | 0.028 | 0.031 |
| 40% | 0.425 | 0.033 | 0.049 |
| 50% | 0.396 | 0.032 | 0.060 |
| 60% | 0.369 | 0.035 | 0.078 |
| 70% | 0.337 | 0.035 | 0.091 |
| 80% | 0.293 | 0.031 | 0.093 |
| 90% | 0.246 | 0.029 | 0.098 |
| 100% | 0.126 | 0.026 | 0.098 |
