# Agreement with model drafts (held-out half): distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed1.jsonl` (distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.030 | [0.014, 0.049] |
| Exact span F1 | 0.046 | [0.026, 0.068] |
| Exact span precision | 0.029 | [0.016, 0.043] |
| Exact span recall | 0.121 | [0.065, 0.177] |
| Role macro-F1 (roles with gold support) | 0.019 | [0.007, 0.044] |
| Category macro-F1 | 0.023 | [0.012, 0.036] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.250 | [0.000, 0.500] |
| False prerequisite rate (lower is better) | 0.699 | [0.632, 0.747] |
| Reversed meaning rate (lower is better) | 0.040 | [0.012, 0.074] |
| Category accuracy on exactly matched spans | 0.765 | [0.550, 1.000] |
| Role accuracy on exactly matched spans | 0.824 | [0.588, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.030 | 0.108 | 0.047 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.017 | 0.100 | 0.029 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 18 |
| USAGE | 0.013 | 0.074 | 0.022 | 54 |
| ACCESS | 0.043 | 0.167 | 0.069 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.496 | 0.034 | 0.014 |
| 20% | 0.461 | 0.017 | 0.014 |
| 30% | 0.432 | 0.011 | 0.014 |
| 40% | 0.409 | 0.021 | 0.036 |
| 50% | 0.384 | 0.027 | 0.057 |
| 60% | 0.356 | 0.028 | 0.071 |
| 70% | 0.328 | 0.024 | 0.071 |
| 80% | 0.287 | 0.023 | 0.079 |
| 90% | 0.246 | 0.021 | 0.079 |
| 100% | 0.169 | 0.019 | 0.079 |
