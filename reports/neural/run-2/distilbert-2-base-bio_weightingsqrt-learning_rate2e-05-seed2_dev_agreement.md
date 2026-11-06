# Agreement with model drafts: distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed2.jsonl` (distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.033 | [0.022, 0.045] |
| Exact span F1 | 0.044 | [0.031, 0.059] |
| Exact span precision | 0.027 | [0.019, 0.037] |
| Exact span recall | 0.111 | [0.078, 0.144] |
| Role macro-F1 (roles with gold support) | 0.025 | [0.011, 0.043] |
| Category macro-F1 | 0.026 | [0.018, 0.034] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.412 | [0.200, 0.667] |
| False prerequisite rate (lower is better) | 0.667 | [0.628, 0.701] |
| Reversed meaning rate (lower is better) | 0.038 | [0.014, 0.063] |
| Category accuracy on exactly matched spans | 0.814 | [0.703, 0.929] |
| Role accuracy on exactly matched spans | 0.930 | [0.833, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.032 | 0.118 | 0.050 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.032 | 0.111 | 0.049 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.007 | 0.028 | 0.012 | 36 |
| USAGE | 0.018 | 0.086 | 0.030 | 186 |
| ACCESS | 0.041 | 0.134 | 0.063 | 134 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.521 | 0.026 | 0.010 |
| 20% | 0.480 | 0.029 | 0.023 |
| 30% | 0.449 | 0.028 | 0.034 |
| 40% | 0.424 | 0.027 | 0.044 |
| 50% | 0.397 | 0.023 | 0.047 |
| 60% | 0.371 | 0.021 | 0.052 |
| 70% | 0.340 | 0.022 | 0.062 |
| 80% | 0.304 | 0.022 | 0.070 |
| 90% | 0.257 | 0.022 | 0.080 |
| 100% | 0.122 | 0.020 | 0.083 |
