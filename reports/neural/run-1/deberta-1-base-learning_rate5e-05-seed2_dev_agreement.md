# Agreement with model drafts: deberta-1-base-learning_rate5e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/deberta-1-base-learning_rate5e-05-seed2.jsonl` (deberta-1-base-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.020 | [0.014, 0.027] |
| Exact span F1 | 0.030 | [0.023, 0.039] |
| Exact span precision | 0.016 | [0.012, 0.021] |
| Exact span recall | 0.244 | [0.202, 0.291] |
| Role macro-F1 (roles with gold support) | 0.014 | [0.009, 0.022] |
| Category macro-F1 | 0.022 | [0.017, 0.030] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.834 | [0.814, 0.850] |
| Reversed meaning rate (lower is better) | 0.058 | [0.024, 0.104] |
| Category accuracy on exactly matched spans | 0.840 | [0.757, 0.909] |
| Role accuracy on exactly matched spans | 0.819 | [0.729, 0.905] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.017 | 0.223 | 0.032 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.013 | 0.278 | 0.025 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.009 | 0.222 | 0.017 | 36 |
| USAGE | 0.015 | 0.215 | 0.028 | 186 |
| ACCESS | 0.016 | 0.187 | 0.029 | 134 |
| PLATFORM | 0.008 | 0.200 | 0.015 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.636 | 0.037 | 0.057 |
| 20% | 0.540 | 0.029 | 0.088 |
| 30% | 0.481 | 0.024 | 0.111 |
| 40% | 0.436 | 0.021 | 0.130 |
| 50% | 0.395 | 0.018 | 0.140 |
| 60% | 0.356 | 0.015 | 0.142 |
| 70% | 0.319 | 0.014 | 0.150 |
| 80% | 0.278 | 0.012 | 0.153 |
| 90% | 0.232 | 0.012 | 0.161 |
| 100% | 0.117 | 0.011 | 0.163 |
