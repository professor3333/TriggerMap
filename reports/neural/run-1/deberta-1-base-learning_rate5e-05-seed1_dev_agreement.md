# Agreement with model drafts: deberta-1-base-learning_rate5e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/deberta-1-base-learning_rate5e-05-seed1.jsonl` (deberta-1-base-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.023 | [0.017, 0.031] |
| Exact span F1 | 0.034 | [0.026, 0.043] |
| Exact span precision | 0.018 | [0.014, 0.023] |
| Exact span recall | 0.264 | [0.222, 0.315] |
| Role macro-F1 (roles with gold support) | 0.015 | [0.010, 0.021] |
| Category macro-F1 | 0.023 | [0.017, 0.030] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.839 | [0.820, 0.855] |
| Reversed meaning rate (lower is better) | 0.055 | [0.021, 0.097] |
| Category accuracy on exactly matched spans | 0.804 | [0.718, 0.879] |
| Role accuracy on exactly matched spans | 0.853 | [0.775, 0.930] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.020 | 0.257 | 0.037 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.010 | 0.167 | 0.019 | 18 |
| UNCERTAIN | 0.001 | 0.036 | 0.002 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.011 | 0.194 | 0.020 | 36 |
| USAGE | 0.016 | 0.253 | 0.029 | 186 |
| ACCESS | 0.018 | 0.187 | 0.033 | 134 |
| PLATFORM | 0.005 | 0.100 | 0.009 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.586 | 0.037 | 0.054 |
| 20% | 0.513 | 0.026 | 0.078 |
| 30% | 0.465 | 0.022 | 0.096 |
| 40% | 0.424 | 0.021 | 0.122 |
| 50% | 0.388 | 0.019 | 0.142 |
| 60% | 0.351 | 0.018 | 0.155 |
| 70% | 0.314 | 0.017 | 0.171 |
| 80% | 0.279 | 0.015 | 0.174 |
| 90% | 0.230 | 0.013 | 0.176 |
| 100% | 0.113 | 0.012 | 0.181 |
