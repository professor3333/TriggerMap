# Agreement with model drafts: rules-2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/agreement/predictions/rules-2.jsonl` (rules-2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.107 | [0.058, 0.154] |
| Exact span F1 | 0.142 | [0.085, 0.195] |
| Exact span precision | 0.272 | [0.182, 0.340] |
| Exact span recall | 0.096 | [0.055, 0.141] |
| Role macro-F1 (roles with gold support) | 0.116 | [0.023, 0.161] |
| Category macro-F1 | 0.098 | [0.052, 0.133] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.019 | [0.000, 0.040] |
| Complete-document exact match, documents without conditions | 0.941 | [0.840, 1.000] |
| False prerequisite rate (lower is better) | 0.330 | [0.165, 0.467] |
| Reversed meaning rate (lower is better) | 0.060 | [0.011, 0.132] |
| Category accuracy on exactly matched spans | 0.865 | [0.704, 0.966] |
| Role accuracy on exactly matched spans | 0.892 | [0.760, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.252 | 0.090 | 0.132 | 323 |
| EXCEPTION | 0.571 | 0.235 | 0.333 | 17 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.147 | 0.139 | 0.143 | 36 |
| USAGE | 0.333 | 0.102 | 0.156 | 186 |
| ACCESS | 0.190 | 0.060 | 0.091 | 134 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.750 | 0.286 | 0.010 |
| 20% | 0.750 | 0.333 | 0.023 |
| 30% | 0.600 | 0.293 | 0.031 |
| 40% | 0.600 | 0.296 | 0.041 |
| 50% | 0.550 | 0.265 | 0.047 |
| 60% | 0.550 | 0.232 | 0.049 |
| 70% | 0.550 | 0.232 | 0.057 |
| 80% | 0.550 | 0.239 | 0.067 |
| 90% | 0.350 | 0.230 | 0.073 |
| 100% | 0.350 | 0.206 | 0.073 |
