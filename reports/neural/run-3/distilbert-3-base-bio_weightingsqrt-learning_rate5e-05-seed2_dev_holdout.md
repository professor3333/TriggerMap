# Agreement with model drafts (held-out half): distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.108 | [0.067, 0.162] |
| Exact span F1 | 0.126 | [0.088, 0.177] |
| Exact span precision | 0.092 | [0.064, 0.135] |
| Exact span recall | 0.200 | [0.136, 0.270] |
| Role macro-F1 (roles with gold support) | 0.057 | [0.027, 0.105] |
| Category macro-F1 | 0.097 | [0.053, 0.157] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.035 | [0.000, 0.077] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.494 | [0.400, 0.569] |
| Reversed meaning rate (lower is better) | 0.042 | [0.009, 0.081] |
| Category accuracy on exactly matched spans | 0.893 | [0.727, 1.000] |
| Role accuracy on exactly matched spans | 0.929 | [0.828, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.097 | 0.200 | 0.131 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.062 | 0.200 | 0.095 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.048 | 0.111 | 0.067 | 18 |
| USAGE | 0.065 | 0.167 | 0.093 | 54 |
| ACCESS | 0.120 | 0.241 | 0.160 | 54 |
| PLATFORM | 0.067 | 0.071 | 0.069 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.901 | 0.267 | 0.057 |
| 20% | 0.793 | 0.148 | 0.064 |
| 30% | 0.725 | 0.121 | 0.079 |
| 40% | 0.647 | 0.098 | 0.086 |
| 50% | 0.595 | 0.105 | 0.114 |
| 60% | 0.547 | 0.099 | 0.129 |
| 70% | 0.511 | 0.094 | 0.143 |
| 80% | 0.472 | 0.086 | 0.150 |
| 90% | 0.420 | 0.084 | 0.164 |
| 100% | 0.151 | 0.079 | 0.171 |
