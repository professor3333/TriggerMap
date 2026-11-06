# Hand-labelled dev: deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed2.jsonl` (deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.143 | [0.056, 0.239] |
| Exact span F1 | 0.163 | [0.091, 0.250] |
| Exact span precision | 0.099 | [0.053, 0.164] |
| Exact span recall | 0.471 | [0.308, 0.615] |
| Role macro-F1 (roles with gold support) | 0.104 | [0.056, 0.323] |
| Category macro-F1 | 0.087 | [0.034, 0.176] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.721 | [0.576, 0.810] |
| Reversed meaning rate (lower is better) | 0.056 | [0.000, 0.188] |
| Category accuracy on exactly matched spans | 0.875 | [0.500, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.131 | 0.500 | 0.208 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.093 | 0.556 | 0.159 | 9 |
| ACCESS | 0.125 | 0.400 | 0.190 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.552 | 0.125 | 0.059 |
| 20% | 0.518 | 0.125 | 0.118 |
| 30% | 0.475 | 0.125 | 0.176 |
| 40% | 0.452 | 0.156 | 0.294 |
| 49% | 0.442 | 0.125 | 0.294 |
| 60% | 0.402 | 0.122 | 0.353 |
| 70% | 0.370 | 0.123 | 0.412 |
| 80% | 0.328 | 0.108 | 0.412 |
| 90% | 0.256 | 0.096 | 0.412 |
| 100% | 0.176 | 0.086 | 0.412 |
