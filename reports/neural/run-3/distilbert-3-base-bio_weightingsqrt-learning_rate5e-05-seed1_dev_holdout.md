# Agreement with model drafts (held-out half): distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed1.jsonl` (distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.085 | [0.049, 0.136] |
| Exact span F1 | 0.101 | [0.064, 0.152] |
| Exact span precision | 0.069 | [0.043, 0.110] |
| Exact span recall | 0.186 | [0.120, 0.266] |
| Role macro-F1 (roles with gold support) | 0.060 | [0.030, 0.109] |
| Category macro-F1 | 0.065 | [0.041, 0.106] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.053 | [0.000, 0.116] |
| Complete-document exact match, documents without conditions | 0.500 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.566 | [0.492, 0.638] |
| Reversed meaning rate (lower is better) | 0.040 | [0.014, 0.072] |
| Category accuracy on exactly matched spans | 0.923 | [0.833, 1.000] |
| Role accuracy on exactly matched spans | 0.885 | [0.696, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.072 | 0.158 | 0.099 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.070 | 0.300 | 0.113 | 10 |
| UNCERTAIN | 0.015 | 0.125 | 0.027 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.023 | 0.056 | 0.032 | 18 |
| USAGE | 0.052 | 0.167 | 0.079 | 54 |
| ACCESS | 0.105 | 0.259 | 0.150 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.742 | 0.105 | 0.029 |
| 20% | 0.663 | 0.080 | 0.043 |
| 30% | 0.612 | 0.071 | 0.057 |
| 40% | 0.561 | 0.073 | 0.079 |
| 50% | 0.522 | 0.074 | 0.100 |
| 60% | 0.499 | 0.066 | 0.107 |
| 70% | 0.459 | 0.068 | 0.129 |
| 80% | 0.413 | 0.063 | 0.136 |
| 90% | 0.355 | 0.065 | 0.157 |
| 100% | 0.171 | 0.058 | 0.157 |
