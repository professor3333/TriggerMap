# Hand-labelled dev: deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed1.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.184 | [0.058, 0.343] |
| Exact span F1 | 0.184 | [0.058, 0.343] |
| Exact span precision | 0.119 | [0.035, 0.244] |
| Exact span recall | 0.412 | [0.167, 0.619] |
| Role macro-F1 (roles with gold support) | 0.109 | [0.039, 0.338] |
| Category macro-F1 | 0.134 | [0.048, 0.308] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.521 | [0.298, 0.727] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.146 | 0.438 | 0.219 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.161 | 0.556 | 0.250 | 9 |
| ACCESS | 0.222 | 0.400 | 0.286 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.638 | 0.167 | 0.059 |
| 20% | 0.584 | 0.250 | 0.176 |
| 31% | 0.537 | 0.222 | 0.235 |
| 41% | 0.514 | 0.208 | 0.294 |
| 51% | 0.502 | 0.200 | 0.353 |
| 59% | 0.494 | 0.171 | 0.353 |
| 69% | 0.459 | 0.146 | 0.353 |
| 80% | 0.435 | 0.128 | 0.353 |
| 90% | 0.370 | 0.132 | 0.412 |
| 100% | 0.227 | 0.119 | 0.412 |
