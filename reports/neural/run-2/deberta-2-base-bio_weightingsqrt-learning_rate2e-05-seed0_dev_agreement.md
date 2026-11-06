# Agreement with model drafts: deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed0.jsonl` (deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.072 | [0.055, 0.093] |
| Exact span F1 | 0.089 | [0.071, 0.111] |
| Exact span precision | 0.055 | [0.043, 0.070] |
| Exact span recall | 0.238 | [0.197, 0.281] |
| Role macro-F1 (roles with gold support) | 0.036 | [0.022, 0.058] |
| Category macro-F1 | 0.072 | [0.050, 0.098] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.353 | [0.125, 0.636] |
| False prerequisite rate (lower is better) | 0.661 | [0.624, 0.693] |
| Reversed meaning rate (lower is better) | 0.046 | [0.018, 0.083] |
| Category accuracy on exactly matched spans | 0.891 | [0.817, 0.952] |
| Role accuracy on exactly matched spans | 0.913 | [0.846, 0.974] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.060 | 0.251 | 0.097 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.021 | 0.111 | 0.035 | 18 |
| UNCERTAIN | 0.006 | 0.036 | 0.010 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.056 | 0.222 | 0.089 | 36 |
| USAGE | 0.047 | 0.237 | 0.079 | 186 |
| ACCESS | 0.067 | 0.209 | 0.101 | 134 |
| PLATFORM | 0.011 | 0.067 | 0.019 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.559 | 0.090 | 0.039 |
| 20% | 0.509 | 0.075 | 0.065 |
| 30% | 0.479 | 0.074 | 0.096 |
| 40% | 0.455 | 0.069 | 0.119 |
| 50% | 0.429 | 0.066 | 0.142 |
| 60% | 0.403 | 0.066 | 0.171 |
| 70% | 0.370 | 0.059 | 0.179 |
| 80% | 0.326 | 0.053 | 0.184 |
| 90% | 0.264 | 0.049 | 0.189 |
| 100% | 0.132 | 0.044 | 0.192 |
