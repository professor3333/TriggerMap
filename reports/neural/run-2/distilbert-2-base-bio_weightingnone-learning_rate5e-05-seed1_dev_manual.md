# Hand-labelled dev: distilbert-2-base-bio_weightingnone-learning_rate5e-05-seed1

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/distilbert-2-base-bio_weightingnone-learning_rate5e-05-seed1.jsonl` (distilbert-2-base-bio_weightingnone-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.146 | [0.000, 0.303] |
| Exact span F1 | 0.146 | [0.000, 0.303] |
| Exact span precision | 0.125 | [0.000, 0.250] |
| Exact span recall | 0.176 | [0.000, 0.429] |
| Role macro-F1 (roles with gold support) | 0.079 | [0.000, 0.276] |
| Category macro-F1 | 0.101 | [0.000, 0.317] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.409 | [0.263, 0.600] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 1.000 | [0.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.136 | 0.188 | 0.158 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 1 |
| USAGE | 0.118 | 0.222 | 0.154 | 9 |
| ACCESS | 0.333 | 0.200 | 0.250 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 8% | 0.707 | 0.500 | 0.059 |
| 21% | 0.579 | 0.200 | 0.059 |
| 29% | 0.537 | 0.143 | 0.059 |
| 42% | 0.507 | 0.100 | 0.059 |
| 50% | 0.499 | 0.167 | 0.118 |
| 58% | 0.483 | 0.214 | 0.176 |
| 71% | 0.416 | 0.176 | 0.176 |
| 79% | 0.404 | 0.158 | 0.176 |
| 92% | 0.336 | 0.136 | 0.176 |
| 100% | 0.278 | 0.125 | 0.176 |
