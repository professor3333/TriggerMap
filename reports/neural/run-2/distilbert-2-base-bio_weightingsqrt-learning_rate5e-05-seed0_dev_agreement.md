# Agreement with model drafts: distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed0.jsonl` (distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.074 | [0.051, 0.099] |
| Exact span F1 | 0.101 | [0.079, 0.129] |
| Exact span precision | 0.069 | [0.053, 0.092] |
| Exact span recall | 0.184 | [0.148, 0.225] |
| Role macro-F1 (roles with gold support) | 0.047 | [0.028, 0.067] |
| Category macro-F1 | 0.071 | [0.054, 0.092] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.019 | [0.000, 0.045] |
| Complete-document exact match, documents without conditions | 0.706 | [0.500, 0.909] |
| False prerequisite rate (lower is better) | 0.554 | [0.492, 0.606] |
| Reversed meaning rate (lower is better) | 0.044 | [0.018, 0.072] |
| Category accuracy on exactly matched spans | 0.845 | [0.757, 0.926] |
| Role accuracy on exactly matched spans | 0.859 | [0.736, 0.952] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.069 | 0.176 | 0.099 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.047 | 0.167 | 0.073 | 18 |
| UNCERTAIN | 0.009 | 0.036 | 0.014 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.042 | 0.111 | 0.061 | 36 |
| USAGE | 0.050 | 0.161 | 0.076 | 186 |
| ACCESS | 0.094 | 0.187 | 0.125 | 134 |
| PLATFORM | 0.017 | 0.033 | 0.022 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.806 | 0.157 | 0.041 |
| 20% | 0.712 | 0.127 | 0.067 |
| 30% | 0.649 | 0.101 | 0.080 |
| 40% | 0.602 | 0.088 | 0.093 |
| 50% | 0.558 | 0.076 | 0.101 |
| 60% | 0.527 | 0.070 | 0.111 |
| 70% | 0.500 | 0.064 | 0.119 |
| 80% | 0.457 | 0.061 | 0.130 |
| 90% | 0.384 | 0.056 | 0.135 |
| 100% | 0.185 | 0.051 | 0.135 |
