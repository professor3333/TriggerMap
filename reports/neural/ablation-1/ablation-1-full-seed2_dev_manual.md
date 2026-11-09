# Hand-labelled dev: ablation-1-full-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-full-seed2.jsonl` (ablation-1-full-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.340 | [0.167, 0.545] |
| Exact span F1 | 0.377 | [0.209, 0.615] |
| Exact span precision | 0.278 | [0.152, 0.481] |
| Exact span recall | 0.588 | [0.333, 0.895] |
| Role macro-F1 (roles with gold support) | 0.191 | [0.105, 0.535] |
| Category macro-F1 | 0.569 | [0.271, 0.758] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.484 | [0.261, 0.688] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 0.900 | [0.625, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.290 | 0.562 | 0.383 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 1.000 | 1.000 | 1.000 | 1 |
| USAGE | 0.185 | 0.556 | 0.278 | 9 |
| ACCESS | 0.600 | 0.600 | 0.600 | 5 |
| PLATFORM | 0.333 | 0.500 | 0.400 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.988 | 1.000 | 0.235 |
| 19% | 0.971 | 0.714 | 0.294 |
| 31% | 0.919 | 0.636 | 0.412 |
| 39% | 0.860 | 0.500 | 0.412 |
| 50% | 0.802 | 0.389 | 0.412 |
| 61% | 0.739 | 0.364 | 0.471 |
| 69% | 0.711 | 0.320 | 0.471 |
| 81% | 0.608 | 0.276 | 0.471 |
| 89% | 0.503 | 0.281 | 0.529 |
| 100% | 0.342 | 0.250 | 0.529 |
