# Agreement with model drafts (held-out half): deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed1.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.103 | [0.070, 0.145] |
| Exact span F1 | 0.121 | [0.087, 0.166] |
| Exact span precision | 0.077 | [0.055, 0.109] |
| Exact span recall | 0.286 | [0.205, 0.370] |
| Role macro-F1 (roles with gold support) | 0.043 | [0.027, 0.089] |
| Category macro-F1 | 0.090 | [0.057, 0.130] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.018 | [0.000, 0.054] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.649 | [0.580, 0.708] |
| Reversed meaning rate (lower is better) | 0.029 | [0.005, 0.062] |
| Category accuracy on exactly matched spans | 0.925 | [0.841, 1.000] |
| Role accuracy on exactly matched spans | 0.925 | [0.833, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.087 | 0.300 | 0.134 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.024 | 0.100 | 0.039 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.040 | 0.167 | 0.065 | 18 |
| USAGE | 0.080 | 0.370 | 0.132 | 54 |
| ACCESS | 0.079 | 0.241 | 0.119 | 54 |
| PLATFORM | 0.030 | 0.071 | 0.043 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.631 | 0.096 | 0.036 |
| 20% | 0.557 | 0.154 | 0.114 |
| 30% | 0.525 | 0.122 | 0.136 |
| 40% | 0.497 | 0.106 | 0.157 |
| 50% | 0.464 | 0.104 | 0.193 |
| 60% | 0.436 | 0.096 | 0.214 |
| 70% | 0.402 | 0.090 | 0.236 |
| 80% | 0.365 | 0.079 | 0.236 |
| 90% | 0.307 | 0.072 | 0.243 |
| 100% | 0.177 | 0.065 | 0.243 |
