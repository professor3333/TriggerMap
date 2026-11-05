# Agreement with model drafts: distilbert-1-base-learning_rate5e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/distilbert-1-base-learning_rate5e-05-seed2.jsonl` (distilbert-1-base-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.019 | [0.014, 0.027] |
| Exact span F1 | 0.026 | [0.019, 0.034] |
| Exact span precision | 0.014 | [0.010, 0.018] |
| Exact span recall | 0.238 | [0.194, 0.287] |
| Role macro-F1 (roles with gold support) | 0.012 | [0.008, 0.019] |
| Category macro-F1 | 0.018 | [0.013, 0.025] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.845 | [0.828, 0.862] |
| Reversed meaning rate (lower is better) | 0.072 | [0.034, 0.116] |
| Category accuracy on exactly matched spans | 0.870 | [0.779, 0.948] |
| Role accuracy on exactly matched spans | 0.848 | [0.769, 0.920] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.019 | 0.232 | 0.035 | 323 |
| EXCEPTION | 0.004 | 0.059 | 0.008 | 17 |
| NOT_REQUIRED | 0.004 | 0.111 | 0.007 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.003 | 0.111 | 0.006 | 36 |
| USAGE | 0.015 | 0.247 | 0.028 | 186 |
| ACCESS | 0.015 | 0.201 | 0.027 | 134 |
| PLATFORM | 0.006 | 0.100 | 0.011 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.586 | 0.040 | 0.070 |
| 20% | 0.499 | 0.028 | 0.096 |
| 30% | 0.448 | 0.022 | 0.114 |
| 40% | 0.408 | 0.018 | 0.127 |
| 50% | 0.372 | 0.016 | 0.142 |
| 60% | 0.338 | 0.014 | 0.145 |
| 70% | 0.305 | 0.013 | 0.161 |
| 80% | 0.270 | 0.012 | 0.166 |
| 90% | 0.234 | 0.011 | 0.168 |
| 100% | 0.107 | 0.010 | 0.176 |
