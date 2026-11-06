# Agreement with model drafts (held-out half): distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed2.jsonl` (distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.024 | [0.010, 0.044] |
| Exact span F1 | 0.035 | [0.016, 0.061] |
| Exact span precision | 0.021 | [0.010, 0.038] |
| Exact span recall | 0.114 | [0.056, 0.180] |
| Role macro-F1 (roles with gold support) | 0.010 | [0.005, 0.017] |
| Category macro-F1 | 0.018 | [0.007, 0.033] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.250 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.747 | [0.699, 0.787] |
| Reversed meaning rate (lower is better) | 0.040 | [0.013, 0.071] |
| Category accuracy on exactly matched spans | 0.750 | [0.571, 0.933] |
| Role accuracy on exactly matched spans | 0.938 | [0.765, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.025 | 0.125 | 0.041 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 18 |
| USAGE | 0.013 | 0.093 | 0.023 | 54 |
| ACCESS | 0.030 | 0.130 | 0.049 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.472 | 0.039 | 0.021 |
| 20% | 0.433 | 0.026 | 0.029 |
| 30% | 0.399 | 0.022 | 0.036 |
| 40% | 0.371 | 0.016 | 0.036 |
| 50% | 0.348 | 0.016 | 0.043 |
| 60% | 0.325 | 0.015 | 0.050 |
| 70% | 0.291 | 0.017 | 0.064 |
| 80% | 0.261 | 0.018 | 0.079 |
| 90% | 0.222 | 0.016 | 0.079 |
| 100% | 0.141 | 0.014 | 0.079 |
