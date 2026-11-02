# Pilot-2 dev: crf, gold origin manual

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/pilot/predictions/crf-pilot-2.jsonl` (crf-pilot-2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.231 | [0.062, 0.417] |
| Exact span F1 | 0.231 | [0.062, 0.417] |
| Exact span precision | 0.333 | [0.111, 1.000] |
| Exact span recall | 0.176 | [0.043, 0.375] |
| Role macro-F1 (roles with gold support) | 0.120 | [0.033, 0.378] |
| Category macro-F1 | 0.176 | [0.022, 0.360] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.375] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.444 | [0.000, 0.667] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.333 | 0.188 | 0.240 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.167 | 0.111 | 0.133 | 9 |
| ACCESS | 1.000 | 0.400 | 0.571 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.955 | 0.000 | 0.000 |
| 22% | 0.843 | 0.500 | 0.059 |
| 33% | 0.697 | 0.333 | 0.059 |
| 44% | 0.575 | 0.250 | 0.059 |
| 44% | 0.575 | 0.250 | 0.059 |
| 56% | 0.552 | 0.400 | 0.118 |
| 67% | 0.544 | 0.500 | 0.176 |
| 78% | 0.497 | 0.429 | 0.176 |
| 89% | 0.488 | 0.375 | 0.176 |
| 100% | 0.458 | 0.333 | 0.176 |
