# Agreement with model drafts: deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed1.jsonl` (deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.132 | [0.110, 0.160] |
| Exact span F1 | 0.161 | [0.135, 0.188] |
| Exact span precision | 0.108 | [0.089, 0.129] |
| Exact span recall | 0.319 | [0.274, 0.365] |
| Role macro-F1 (roles with gold support) | 0.069 | [0.050, 0.090] |
| Category macro-F1 | 0.125 | [0.099, 0.156] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.039 | [0.013, 0.074] |
| Complete-document exact match, documents without conditions | 0.353 | [0.143, 0.600] |
| False prerequisite rate (lower is better) | 0.596 | [0.553, 0.634] |
| Reversed meaning rate (lower is better) | 0.034 | [0.013, 0.060] |
| Category accuracy on exactly matched spans | 0.894 | [0.829, 0.951] |
| Role accuracy on exactly matched spans | 0.919 | [0.858, 0.981] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.113 | 0.334 | 0.168 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.066 | 0.278 | 0.106 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.096 | 0.306 | 0.147 | 36 |
| USAGE | 0.100 | 0.339 | 0.154 | 186 |
| ACCESS | 0.112 | 0.246 | 0.154 | 134 |
| PLATFORM | 0.029 | 0.100 | 0.045 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.859 | 0.263 | 0.078 |
| 20% | 0.766 | 0.170 | 0.101 |
| 30% | 0.698 | 0.157 | 0.140 |
| 40% | 0.637 | 0.151 | 0.179 |
| 50% | 0.587 | 0.135 | 0.199 |
| 60% | 0.547 | 0.120 | 0.212 |
| 70% | 0.515 | 0.115 | 0.238 |
| 80% | 0.479 | 0.105 | 0.249 |
| 90% | 0.408 | 0.095 | 0.254 |
| 100% | 0.210 | 0.088 | 0.262 |
