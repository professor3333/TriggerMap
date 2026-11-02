# Pilot dev: rules, gold origin all

- Gold: `annotations/pilot/pilot-1.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 38 documents)
- Predictions: `reports/pilot/predictions/rules-2.jsonl` (rules-2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 38 (34 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.144 | [0.040, 0.276] |
| Exact span F1 | 0.235 | [0.109, 0.348] |
| Exact span precision | 0.486 | [0.250, 0.686] |
| Exact span recall | 0.155 | [0.068, 0.241] |
| Role macro-F1 (roles with gold support) | 0.082 | [0.040, 0.159] |
| Category macro-F1 | 0.188 | [0.027, 0.340] |
| Group exact-match F1 | 0.105 | [0.000, 0.353] |
| Complete-document exact match, documents with conditions | 0.029 | [0.000, 0.091] |
| Complete-document exact match, documents without conditions | 1.000 | [1.000, 1.000] |
| False prerequisite rate (lower is better) | 0.135 | [0.030, 0.270] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 0.611 | [0.250, 0.938] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.486 | 0.164 | 0.245 | 110 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 3 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 3 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.286 | 0.154 | 0.200 | 13 |
| USAGE | 0.263 | 0.075 | 0.116 | 67 |
| ACCESS | 0.333 | 0.097 | 0.150 | 31 |
| PLATFORM | 0.500 | 0.200 | 0.286 | 5 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.750 | 0.750 | 0.026 |
| 19% | 0.750 | 0.714 | 0.043 |
| 30% | 0.750 | 0.455 | 0.043 |
| 41% | 0.600 | 0.400 | 0.052 |
| 49% | 0.600 | 0.444 | 0.069 |
| 59% | 0.550 | 0.364 | 0.069 |
| 70% | 0.550 | 0.346 | 0.078 |
| 81% | 0.550 | 0.300 | 0.078 |
| 89% | 0.550 | 0.303 | 0.086 |
| 100% | 0.550 | 0.297 | 0.095 |
