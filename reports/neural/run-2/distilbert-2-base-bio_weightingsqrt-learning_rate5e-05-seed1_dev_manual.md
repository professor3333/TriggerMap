# Hand-labelled dev: distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed1.jsonl` (distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.052 | [0.012, 0.094] |
| Exact span F1 | 0.052 | [0.012, 0.094] |
| Exact span precision | 0.029 | [0.007, 0.053] |
| Exact span recall | 0.235 | [0.043, 0.500] |
| Role macro-F1 (roles with gold support) | 0.030 | [0.007, 0.098] |
| Category macro-F1 | 0.035 | [0.010, 0.083] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.765 | [0.653, 0.841] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.034 | 0.250 | 0.059 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.028 | 0.222 | 0.050 | 9 |
| ACCESS | 0.050 | 0.400 | 0.089 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.466 | 0.143 | 0.118 |
| 20% | 0.430 | 0.111 | 0.176 |
| 30% | 0.408 | 0.073 | 0.176 |
| 40% | 0.376 | 0.073 | 0.235 |
| 50% | 0.358 | 0.059 | 0.235 |
| 60% | 0.321 | 0.049 | 0.235 |
| 70% | 0.293 | 0.042 | 0.235 |
| 80% | 0.278 | 0.036 | 0.235 |
| 90% | 0.245 | 0.033 | 0.235 |
| 100% | 0.157 | 0.029 | 0.235 |
