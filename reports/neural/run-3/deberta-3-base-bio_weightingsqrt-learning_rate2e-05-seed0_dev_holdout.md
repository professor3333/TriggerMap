# Agreement with model drafts (held-out half): deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed0.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.105 | [0.070, 0.151] |
| Exact span F1 | 0.132 | [0.094, 0.179] |
| Exact span precision | 0.083 | [0.057, 0.117] |
| Exact span recall | 0.321 | [0.257, 0.393] |
| Role macro-F1 (roles with gold support) | 0.072 | [0.043, 0.130] |
| Category macro-F1 | 0.093 | [0.065, 0.128] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.613 | [0.547, 0.669] |
| Reversed meaning rate (lower is better) | 0.043 | [0.020, 0.066] |
| Category accuracy on exactly matched spans | 0.844 | [0.732, 0.953] |
| Role accuracy on exactly matched spans | 0.933 | [0.852, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.097 | 0.317 | 0.149 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.083 | 0.400 | 0.138 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.049 | 0.222 | 0.081 | 18 |
| USAGE | 0.068 | 0.315 | 0.112 | 54 |
| ACCESS | 0.099 | 0.296 | 0.149 | 54 |
| PLATFORM | 0.019 | 0.071 | 0.030 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.658 | 0.204 | 0.079 |
| 20% | 0.595 | 0.165 | 0.129 |
| 30% | 0.541 | 0.129 | 0.150 |
| 40% | 0.502 | 0.115 | 0.179 |
| 50% | 0.476 | 0.110 | 0.214 |
| 60% | 0.440 | 0.095 | 0.221 |
| 70% | 0.407 | 0.084 | 0.229 |
| 80% | 0.363 | 0.078 | 0.243 |
| 90% | 0.297 | 0.073 | 0.257 |
| 100% | 0.155 | 0.066 | 0.257 |
