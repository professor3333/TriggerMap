# Hand-labelled dev: deberta-1-base-learning_rate5e-05-seed0

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-1-base-learning_rate5e-05-seed0.jsonl` (deberta-1-base-learning_rate5e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.030 | [0.000, 0.080] |
| Exact span F1 | 0.030 | [0.000, 0.080] |
| Exact span precision | 0.016 | [0.000, 0.045] |
| Exact span recall | 0.235 | [0.000, 0.444] |
| Role macro-F1 (roles with gold support) | 0.019 | [0.000, 0.086] |
| Category macro-F1 | 0.027 | [0.000, 0.079] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.839 | [0.754, 0.903] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.021 | 0.250 | 0.038 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.013 | 0.222 | 0.024 | 9 |
| ACCESS | 0.047 | 0.400 | 0.083 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.652 | 0.040 | 0.059 |
| 20% | 0.560 | 0.060 | 0.176 |
| 30% | 0.504 | 0.039 | 0.176 |
| 40% | 0.457 | 0.030 | 0.176 |
| 50% | 0.432 | 0.024 | 0.176 |
| 60% | 0.388 | 0.020 | 0.176 |
| 70% | 0.360 | 0.023 | 0.235 |
| 80% | 0.316 | 0.020 | 0.235 |
| 90% | 0.272 | 0.018 | 0.235 |
| 100% | 0.149 | 0.016 | 0.235 |
