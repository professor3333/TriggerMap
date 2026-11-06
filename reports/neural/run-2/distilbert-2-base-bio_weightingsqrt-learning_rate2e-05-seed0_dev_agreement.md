# Agreement with model drafts: distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed0.jsonl` (distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.039 | [0.029, 0.052] |
| Exact span F1 | 0.056 | [0.043, 0.073] |
| Exact span precision | 0.034 | [0.026, 0.045] |
| Exact span recall | 0.168 | [0.131, 0.210] |
| Role macro-F1 (roles with gold support) | 0.037 | [0.017, 0.057] |
| Category macro-F1 | 0.042 | [0.027, 0.058] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.006 | [0.000, 0.023] |
| Complete-document exact match, documents without conditions | 0.176 | [0.000, 0.417] |
| False prerequisite rate (lower is better) | 0.724 | [0.685, 0.755] |
| Reversed meaning rate (lower is better) | 0.039 | [0.013, 0.069] |
| Category accuracy on exactly matched spans | 0.800 | [0.689, 0.898] |
| Role accuracy on exactly matched spans | 0.862 | [0.769, 0.952] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.031 | 0.158 | 0.052 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.050 | 0.167 | 0.077 | 18 |
| UNCERTAIN | 0.010 | 0.071 | 0.018 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.027 | 0.083 | 0.041 | 36 |
| USAGE | 0.022 | 0.134 | 0.038 | 186 |
| ACCESS | 0.042 | 0.164 | 0.067 | 134 |
| PLATFORM | 0.013 | 0.067 | 0.021 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.472 | 0.052 | 0.026 |
| 20% | 0.437 | 0.034 | 0.034 |
| 30% | 0.413 | 0.034 | 0.052 |
| 40% | 0.389 | 0.035 | 0.070 |
| 50% | 0.363 | 0.035 | 0.088 |
| 60% | 0.337 | 0.030 | 0.091 |
| 70% | 0.305 | 0.028 | 0.098 |
| 80% | 0.274 | 0.026 | 0.106 |
| 90% | 0.233 | 0.025 | 0.111 |
| 100% | 0.135 | 0.023 | 0.117 |
