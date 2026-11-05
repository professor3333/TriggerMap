# Agreement with model drafts: deberta-1-base-learning_rate5e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/deberta-1-base-learning_rate5e-05-seed0.jsonl` (deberta-1-base-learning_rate5e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.020 | [0.014, 0.027] |
| Exact span F1 | 0.028 | [0.022, 0.037] |
| Exact span precision | 0.015 | [0.012, 0.020] |
| Exact span recall | 0.228 | [0.189, 0.275] |
| Role macro-F1 (roles with gold support) | 0.017 | [0.010, 0.027] |
| Category macro-F1 | 0.020 | [0.016, 0.026] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.832 | [0.812, 0.850] |
| Reversed meaning rate (lower is better) | 0.054 | [0.021, 0.094] |
| Category accuracy on exactly matched spans | 0.852 | [0.769, 0.924] |
| Role accuracy on exactly matched spans | 0.852 | [0.770, 0.931] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.017 | 0.214 | 0.031 | 323 |
| EXCEPTION | 0.006 | 0.059 | 0.010 | 17 |
| NOT_REQUIRED | 0.014 | 0.222 | 0.026 | 18 |
| UNCERTAIN | 0.001 | 0.036 | 0.002 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.005 | 0.111 | 0.010 | 36 |
| USAGE | 0.014 | 0.226 | 0.026 | 186 |
| ACCESS | 0.021 | 0.194 | 0.038 | 134 |
| PLATFORM | 0.004 | 0.100 | 0.008 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.629 | 0.029 | 0.044 |
| 20% | 0.536 | 0.025 | 0.075 |
| 30% | 0.480 | 0.024 | 0.109 |
| 40% | 0.437 | 0.023 | 0.137 |
| 50% | 0.397 | 0.020 | 0.150 |
| 60% | 0.358 | 0.017 | 0.153 |
| 70% | 0.322 | 0.015 | 0.155 |
| 80% | 0.285 | 0.013 | 0.158 |
| 90% | 0.244 | 0.012 | 0.161 |
| 100% | 0.119 | 0.011 | 0.161 |
