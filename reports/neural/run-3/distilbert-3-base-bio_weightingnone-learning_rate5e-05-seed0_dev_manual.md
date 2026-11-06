# Hand-labelled dev: distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed0

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed0.jsonl` (distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.143 | [0.000, 0.278] |
| Exact span F1 | 0.143 | [0.000, 0.278] |
| Exact span precision | 0.103 | [0.000, 0.209] |
| Exact span recall | 0.235 | [0.000, 0.500] |
| Role macro-F1 (roles with gold support) | 0.078 | [0.000, 0.264] |
| Category macro-F1 | 0.079 | [0.000, 0.234] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.629 | [0.485, 0.811] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.114 | 0.250 | 0.157 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.115 | 0.333 | 0.171 | 9 |
| ACCESS | 0.111 | 0.200 | 0.143 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.632 | 0.750 | 0.176 |
| 21% | 0.608 | 0.375 | 0.176 |
| 31% | 0.552 | 0.250 | 0.176 |
| 41% | 0.528 | 0.188 | 0.176 |
| 51% | 0.513 | 0.150 | 0.176 |
| 59% | 0.505 | 0.174 | 0.235 |
| 69% | 0.491 | 0.148 | 0.235 |
| 79% | 0.475 | 0.129 | 0.235 |
| 90% | 0.457 | 0.114 | 0.235 |
| 100% | 0.411 | 0.103 | 0.235 |
