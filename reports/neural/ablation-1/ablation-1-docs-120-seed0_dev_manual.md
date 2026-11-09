# Hand-labelled dev: ablation-1-docs-120-seed0

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-docs-120-seed0.jsonl` (ablation-1-docs-120-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.148 | [0.000, 0.346] |
| Exact span F1 | 0.173 | [0.038, 0.367] |
| Exact span precision | 0.109 | [0.023, 0.250] |
| Exact span recall | 0.412 | [0.091, 0.714] |
| Role macro-F1 (roles with gold support) | 0.096 | [0.021, 0.340] |
| Category macro-F1 | 0.105 | [0.000, 0.333] |
| Group exact-match F1 | 0.100 | [0.000, 0.353] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.333] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.632 | [0.425, 0.768] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 0.857 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.123 | 0.438 | 0.192 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.105 | 0.444 | 0.170 | 9 |
| ACCESS | 0.182 | 0.400 | 0.250 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 9% | 0.611 | 0.000 | 0.000 |
| 20% | 0.565 | 0.077 | 0.059 |
| 30% | 0.530 | 0.158 | 0.176 |
| 41% | 0.497 | 0.192 | 0.294 |
| 50% | 0.488 | 0.156 | 0.294 |
| 59% | 0.452 | 0.132 | 0.294 |
| 70% | 0.405 | 0.111 | 0.294 |
| 80% | 0.381 | 0.098 | 0.294 |
| 91% | 0.313 | 0.103 | 0.353 |
| 100% | 0.163 | 0.094 | 0.353 |
