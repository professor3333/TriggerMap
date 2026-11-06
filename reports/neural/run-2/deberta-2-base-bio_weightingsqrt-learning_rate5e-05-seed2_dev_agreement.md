# Agreement with model drafts: deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.130 | [0.103, 0.162] |
| Exact span F1 | 0.152 | [0.125, 0.185] |
| Exact span precision | 0.100 | [0.080, 0.124] |
| Exact span recall | 0.319 | [0.271, 0.377] |
| Role macro-F1 (roles with gold support) | 0.093 | [0.057, 0.138] |
| Category macro-F1 | 0.121 | [0.089, 0.156] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.032 | [0.007, 0.062] |
| Complete-document exact match, documents without conditions | 0.353 | [0.133, 0.588] |
| False prerequisite rate (lower is better) | 0.577 | [0.532, 0.616] |
| Reversed meaning rate (lower is better) | 0.026 | [0.012, 0.043] |
| Category accuracy on exactly matched spans | 0.902 | [0.845, 0.958] |
| Role accuracy on exactly matched spans | 0.943 | [0.897, 0.982] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.107 | 0.334 | 0.162 | 323 |
| EXCEPTION | 0.061 | 0.118 | 0.080 | 17 |
| NOT_REQUIRED | 0.072 | 0.278 | 0.115 | 18 |
| UNCERTAIN | 0.008 | 0.036 | 0.014 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.089 | 0.250 | 0.131 | 36 |
| USAGE | 0.084 | 0.306 | 0.132 | 186 |
| ACCESS | 0.114 | 0.313 | 0.167 | 134 |
| PLATFORM | 0.036 | 0.100 | 0.053 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.763 | 0.179 | 0.057 |
| 20% | 0.665 | 0.159 | 0.101 |
| 30% | 0.602 | 0.154 | 0.148 |
| 40% | 0.565 | 0.146 | 0.187 |
| 50% | 0.527 | 0.128 | 0.205 |
| 60% | 0.498 | 0.114 | 0.218 |
| 70% | 0.463 | 0.102 | 0.228 |
| 80% | 0.419 | 0.095 | 0.244 |
| 90% | 0.354 | 0.094 | 0.269 |
| 100% | 0.167 | 0.085 | 0.272 |
