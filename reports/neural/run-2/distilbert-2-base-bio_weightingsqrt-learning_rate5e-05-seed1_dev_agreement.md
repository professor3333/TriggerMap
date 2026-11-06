# Agreement with model drafts: distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed1.jsonl` (distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.041 | [0.030, 0.055] |
| Exact span F1 | 0.052 | [0.040, 0.065] |
| Exact span precision | 0.030 | [0.023, 0.038] |
| Exact span recall | 0.194 | [0.153, 0.236] |
| Role macro-F1 (roles with gold support) | 0.035 | [0.017, 0.057] |
| Category macro-F1 | 0.039 | [0.029, 0.049] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.059 | [0.000, 0.200] |
| False prerequisite rate (lower is better) | 0.770 | [0.743, 0.793] |
| Reversed meaning rate (lower is better) | 0.052 | [0.023, 0.084] |
| Category accuracy on exactly matched spans | 0.867 | [0.770, 0.948] |
| Role accuracy on exactly matched spans | 0.933 | [0.840, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.030 | 0.201 | 0.052 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.052 | 0.278 | 0.088 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.007 | 0.056 | 0.013 | 36 |
| USAGE | 0.021 | 0.151 | 0.037 | 186 |
| ACCESS | 0.062 | 0.254 | 0.099 | 134 |
| PLATFORM | 0.003 | 0.033 | 0.005 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.473 | 0.056 | 0.036 |
| 20% | 0.435 | 0.051 | 0.067 |
| 30% | 0.406 | 0.042 | 0.083 |
| 40% | 0.382 | 0.043 | 0.111 |
| 50% | 0.357 | 0.037 | 0.122 |
| 60% | 0.332 | 0.034 | 0.135 |
| 70% | 0.302 | 0.030 | 0.137 |
| 80% | 0.270 | 0.027 | 0.142 |
| 90% | 0.229 | 0.026 | 0.153 |
| 100% | 0.122 | 0.024 | 0.155 |
