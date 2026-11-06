# Hand-labelled dev: deberta-3-base-bio_weightingnone-learning_rate5e-05-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingnone-learning_rate5e-05-seed1.jsonl` (deberta-3-base-bio_weightingnone-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.298 | [0.065, 0.585] |
| Exact span F1 | 0.298 | [0.065, 0.585] |
| Exact span precision | 0.233 | [0.050, 0.500] |
| Exact span recall | 0.412 | [0.091, 0.789] |
| Role macro-F1 (roles with gold support) | 0.167 | [0.043, 0.560] |
| Category macro-F1 | 0.187 | [0.062, 0.481] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.222 | [0.000, 0.455] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.538 | [0.294, 0.778] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.269 | 0.438 | 0.333 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.294 | 0.556 | 0.385 | 9 |
| ACCESS | 0.333 | 0.400 | 0.364 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.846 | 1.000 | 0.176 |
| 20% | 0.782 | 0.667 | 0.235 |
| 30% | 0.671 | 0.556 | 0.294 |
| 40% | 0.649 | 0.500 | 0.353 |
| 50% | 0.621 | 0.400 | 0.353 |
| 60% | 0.576 | 0.333 | 0.353 |
| 70% | 0.519 | 0.333 | 0.412 |
| 80% | 0.447 | 0.292 | 0.412 |
| 90% | 0.395 | 0.259 | 0.412 |
| 100% | 0.225 | 0.233 | 0.412 |
