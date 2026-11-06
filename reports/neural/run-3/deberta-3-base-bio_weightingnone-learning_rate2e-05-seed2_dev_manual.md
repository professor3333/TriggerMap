# Hand-labelled dev: deberta-3-base-bio_weightingnone-learning_rate2e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingnone-learning_rate2e-05-seed2.jsonl` (deberta-3-base-bio_weightingnone-learning_rate2e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.000 | [0.000, 0.000] |
| Exact span F1 | 0.000 | [0.000, 0.000] |
| Exact span precision | 0.000 | [0.000, 0.000] |
| Exact span recall | 0.000 | [0.000, 0.000] |
| Role macro-F1 (roles with gold support) | 0.000 | [0.000, 0.000] |
| Category macro-F1 | 0.000 | [0.000, 0.000] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.889 | [0.720, 0.969] |
| Reversed meaning rate (lower is better) | 0.438 | [0.154, 0.846] |
| Category accuracy on exactly matched spans | 0.000 | [0.000, 0.000] |
| Role accuracy on exactly matched spans | 0.000 | [0.000, 0.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.000 | 0.000 | 0.000 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.000 | 0.000 | 0.000 | 9 |
| ACCESS | 0.000 | 0.000 | 0.000 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.260 | 0.000 | 0.000 |
| 20% | 0.234 | 0.000 | 0.000 |
| 30% | 0.221 | 0.000 | 0.000 |
| 40% | 0.206 | 0.000 | 0.000 |
| 50% | 0.195 | 0.000 | 0.000 |
| 60% | 0.177 | 0.000 | 0.000 |
| 70% | 0.166 | 0.000 | 0.000 |
| 80% | 0.156 | 0.000 | 0.000 |
| 90% | 0.143 | 0.000 | 0.000 |
| 100% | 0.111 | 0.000 | 0.000 |
