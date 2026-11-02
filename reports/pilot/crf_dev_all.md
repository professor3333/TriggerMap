# Pilot-2 dev: crf, gold origin all

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 38 documents)
- Predictions: `reports/pilot/predictions/crf-pilot-2.jsonl` (crf-pilot-2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 38 (35 with gold conditions, 3 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.093 | [0.029, 0.185] |
| Exact span F1 | 0.119 | [0.041, 0.210] |
| Exact span precision | 0.250 | [0.107, 0.407] |
| Exact span recall | 0.078 | [0.025, 0.144] |
| Role macro-F1 (roles with gold support) | 0.041 | [0.015, 0.093] |
| Category macro-F1 | 0.083 | [0.019, 0.166] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.057 | [0.000, 0.176] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.361 | [0.231, 0.479] |
| Reversed meaning rate (lower is better) | 0.043 | [0.000, 0.143] |
| Category accuracy on exactly matched spans | 0.778 | [0.500, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.250 | 0.083 | 0.124 | 109 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 3 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 3 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.500 | 0.083 | 0.143 | 12 |
| USAGE | 0.167 | 0.060 | 0.088 | 67 |
| ACCESS | 0.250 | 0.065 | 0.103 | 31 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 5 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.882 | 0.000 | 0.000 |
| 19% | 0.826 | 0.286 | 0.017 |
| 31% | 0.649 | 0.273 | 0.026 |
| 39% | 0.615 | 0.214 | 0.026 |
| 50% | 0.571 | 0.222 | 0.035 |
| 61% | 0.544 | 0.273 | 0.052 |
| 69% | 0.523 | 0.240 | 0.052 |
| 81% | 0.488 | 0.207 | 0.052 |
| 89% | 0.458 | 0.219 | 0.061 |
| 100% | 0.203 | 0.194 | 0.061 |
