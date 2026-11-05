# Agreement with model drafts: distilbert-1-base-learning_rate5e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/distilbert-1-base-learning_rate5e-05-seed0.jsonl` (distilbert-1-base-learning_rate5e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.019 | [0.013, 0.026] |
| Exact span F1 | 0.025 | [0.019, 0.033] |
| Exact span precision | 0.013 | [0.010, 0.018] |
| Exact span recall | 0.215 | [0.179, 0.257] |
| Role macro-F1 (roles with gold support) | 0.012 | [0.007, 0.018] |
| Category macro-F1 | 0.019 | [0.014, 0.027] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.839 | [0.818, 0.857] |
| Reversed meaning rate (lower is better) | 0.064 | [0.034, 0.096] |
| Category accuracy on exactly matched spans | 0.916 | [0.852, 0.973] |
| Role accuracy on exactly matched spans | 0.807 | [0.724, 0.896] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.016 | 0.198 | 0.030 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.009 | 0.167 | 0.018 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.006 | 0.139 | 0.011 | 36 |
| USAGE | 0.013 | 0.220 | 0.024 | 186 |
| ACCESS | 0.015 | 0.194 | 0.029 | 134 |
| PLATFORM | 0.007 | 0.133 | 0.013 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.586 | 0.030 | 0.049 |
| 20% | 0.501 | 0.024 | 0.080 |
| 30% | 0.454 | 0.019 | 0.093 |
| 40% | 0.413 | 0.016 | 0.106 |
| 50% | 0.378 | 0.015 | 0.122 |
| 60% | 0.345 | 0.014 | 0.137 |
| 70% | 0.311 | 0.013 | 0.145 |
| 80% | 0.277 | 0.012 | 0.153 |
| 90% | 0.238 | 0.011 | 0.161 |
| 100% | 0.127 | 0.010 | 0.163 |
