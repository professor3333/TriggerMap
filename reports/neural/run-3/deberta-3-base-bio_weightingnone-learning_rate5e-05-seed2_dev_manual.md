# Hand-labelled dev: deberta-3-base-bio_weightingnone-learning_rate5e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingnone-learning_rate5e-05-seed2.jsonl` (deberta-3-base-bio_weightingnone-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.320 | [0.105, 0.622] |
| Exact span F1 | 0.360 | [0.152, 0.718] |
| Exact span precision | 0.273 | [0.106, 0.591] |
| Exact span recall | 0.529 | [0.250, 0.867] |
| Role macro-F1 (roles with gold support) | 0.182 | [0.073, 0.571] |
| Category macro-F1 | 0.399 | [0.191, 0.756] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.464 | [0.333, 0.639] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 0.889 | [0.571, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.286 | 0.500 | 0.364 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.250 | 1.000 | 0.400 | 1 |
| USAGE | 0.238 | 0.556 | 0.333 | 9 |
| ACCESS | 0.333 | 0.400 | 0.364 | 5 |
| PLATFORM | 0.500 | 0.500 | 0.500 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 9% | 0.795 | 0.667 | 0.118 |
| 21% | 0.708 | 0.714 | 0.294 |
| 30% | 0.686 | 0.500 | 0.294 |
| 39% | 0.622 | 0.462 | 0.353 |
| 48% | 0.581 | 0.375 | 0.353 |
| 61% | 0.522 | 0.350 | 0.412 |
| 70% | 0.487 | 0.304 | 0.412 |
| 79% | 0.462 | 0.269 | 0.412 |
| 91% | 0.402 | 0.233 | 0.412 |
| 100% | 0.330 | 0.242 | 0.471 |
