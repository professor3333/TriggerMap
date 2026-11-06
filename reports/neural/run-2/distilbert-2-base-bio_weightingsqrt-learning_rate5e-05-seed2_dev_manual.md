# Hand-labelled dev: distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.192 | [0.043, 0.364] |
| Exact span F1 | 0.192 | [0.043, 0.364] |
| Exact span precision | 0.143 | [0.033, 0.333] |
| Exact span recall | 0.294 | [0.067, 0.526] |
| Role macro-F1 (roles with gold support) | 0.132 | [0.038, 0.381] |
| Category macro-F1 | 0.154 | [0.056, 0.341] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.591 | [0.200, 0.812] |
| Reversed meaning rate (lower is better) | 0.231 | [0.000, 0.600] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.227 | 0.312 | 0.263 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.077 | 0.222 | 0.114 | 9 |
| ACCESS | 0.429 | 0.600 | 0.500 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.890 | 0.750 | 0.176 |
| 20% | 0.762 | 0.429 | 0.176 |
| 29% | 0.736 | 0.400 | 0.235 |
| 40% | 0.667 | 0.357 | 0.294 |
| 51% | 0.589 | 0.278 | 0.294 |
| 60% | 0.556 | 0.238 | 0.294 |
| 69% | 0.498 | 0.208 | 0.294 |
| 80% | 0.417 | 0.179 | 0.294 |
| 91% | 0.337 | 0.156 | 0.294 |
| 100% | 0.244 | 0.143 | 0.294 |
