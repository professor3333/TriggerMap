# Hand-labelled dev: distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed1.jsonl` (distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.082 | [0.018, 0.158] |
| Exact span F1 | 0.082 | [0.018, 0.158] |
| Exact span precision | 0.049 | [0.011, 0.096] |
| Exact span recall | 0.235 | [0.043, 0.500] |
| Role macro-F1 (roles with gold support) | 0.053 | [0.011, 0.192] |
| Category macro-F1 | 0.061 | [0.011, 0.173] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.712 | [0.544, 0.857] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.068 | 0.250 | 0.107 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.036 | 0.222 | 0.062 | 9 |
| ACCESS | 0.118 | 0.400 | 0.182 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.495 | 0.125 | 0.059 |
| 20% | 0.458 | 0.062 | 0.059 |
| 30% | 0.430 | 0.125 | 0.176 |
| 40% | 0.406 | 0.125 | 0.235 |
| 49% | 0.382 | 0.100 | 0.235 |
| 60% | 0.329 | 0.082 | 0.235 |
| 70% | 0.301 | 0.070 | 0.235 |
| 80% | 0.274 | 0.062 | 0.235 |
| 90% | 0.235 | 0.055 | 0.235 |
| 100% | 0.162 | 0.049 | 0.235 |
