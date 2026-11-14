# batch-07: draft 2 (project 9) scored against draft 1 (project 7)

- Gold: `annotations/batches/batch-07.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 100 documents)
- Predictions: `reports/drafter-consistency/predictions/batch-07-draft-2.jsonl` (model-project9-guidelines-0.2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 100 (87 with gold conditions, 13 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.375 | [0.309, 0.444] |
| Exact span F1 | 0.431 | [0.366, 0.503] |
| Exact span precision | 0.339 | [0.277, 0.410] |
| Exact span recall | 0.593 | [0.517, 0.671] |
| Role macro-F1 (roles with gold support) | 0.377 | [0.244, 0.495] |
| Category macro-F1 | 0.384 | [0.301, 0.455] |
| Group exact-match F1 | 0.091 | [0.000, 0.200] |
| Complete-document exact match, documents with conditions | 0.207 | [0.122, 0.300] |
| Complete-document exact match, documents without conditions | 0.692 | [0.417, 1.000] |
| False prerequisite rate (lower is better) | 0.395 | [0.323, 0.462] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 0.935 | [0.888, 0.975] |
| Role accuracy on exactly matched spans | 0.935 | [0.867, 0.989] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.341 | 0.553 | 0.422 | 161 |
| EXCEPTION | 0.214 | 0.429 | 0.286 | 7 |
| NOT_REQUIRED | 0.400 | 1.000 | 0.571 | 4 |
| UNCERTAIN | 0.147 | 0.500 | 0.227 | 10 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.424 | 0.609 | 0.500 | 23 |
| USAGE | 0.319 | 0.619 | 0.421 | 84 |
| ACCESS | 0.313 | 0.477 | 0.378 | 65 |
| PLATFORM | 0.167 | 0.400 | 0.235 | 10 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 1.000 | 0.281 | 0.049 |
| 20% | 1.000 | 0.266 | 0.093 |
| 30% | 1.000 | 0.240 | 0.126 |
| 40% | 1.000 | 0.266 | 0.187 |
| 50% | 1.000 | 0.287 | 0.253 |
| 60% | 1.000 | 0.272 | 0.286 |
| 70% | 1.000 | 0.274 | 0.335 |
| 80% | 1.000 | 0.278 | 0.390 |
| 90% | 1.000 | 0.279 | 0.440 |
| 100% | 1.000 | 0.295 | 0.516 |
