# Hand-labelled dev: ablation-1-docs-60-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-docs-60-seed1.jsonl` (ablation-1-docs-60-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.148 | [0.052, 0.247] |
| Exact span F1 | 0.148 | [0.052, 0.247] |
| Exact span precision | 0.094 | [0.032, 0.173] |
| Exact span recall | 0.353 | [0.150, 0.545] |
| Role macro-F1 (roles with gold support) | 0.078 | [0.028, 0.247] |
| Category macro-F1 | 0.115 | [0.037, 0.243] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.689 | [0.488, 0.826] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.098 | 0.375 | 0.156 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.093 | 0.444 | 0.154 | 9 |
| ACCESS | 0.250 | 0.400 | 0.308 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 9% | 0.589 | 0.167 | 0.059 |
| 20% | 0.539 | 0.231 | 0.176 |
| 30% | 0.505 | 0.158 | 0.176 |
| 41% | 0.468 | 0.115 | 0.176 |
| 50% | 0.442 | 0.156 | 0.294 |
| 59% | 0.417 | 0.132 | 0.294 |
| 70% | 0.386 | 0.111 | 0.294 |
| 80% | 0.364 | 0.118 | 0.353 |
| 91% | 0.312 | 0.103 | 0.353 |
| 100% | 0.231 | 0.094 | 0.353 |
