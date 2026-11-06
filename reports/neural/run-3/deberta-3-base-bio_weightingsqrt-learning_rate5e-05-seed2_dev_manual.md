# Hand-labelled dev: deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.346 | [0.172, 0.545] |
| Exact span F1 | 0.385 | [0.214, 0.615] |
| Exact span precision | 0.286 | [0.156, 0.500] |
| Exact span recall | 0.588 | [0.333, 0.895] |
| Role macro-F1 (roles with gold support) | 0.196 | [0.111, 0.541] |
| Category macro-F1 | 0.571 | [0.271, 0.758] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 1.000 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.500 | [0.280, 0.690] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 0.900 | [0.625, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.300 | 0.562 | 0.391 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 1.000 | 1.000 | 1.000 | 1 |
| USAGE | 0.192 | 0.556 | 0.286 | 9 |
| ACCESS | 0.600 | 0.600 | 0.600 | 5 |
| PLATFORM | 0.333 | 0.500 | 0.400 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 11% | 0.989 | 1.000 | 0.235 |
| 20% | 0.970 | 0.714 | 0.294 |
| 29% | 0.942 | 0.700 | 0.412 |
| 40% | 0.855 | 0.500 | 0.412 |
| 51% | 0.802 | 0.389 | 0.412 |
| 60% | 0.747 | 0.381 | 0.471 |
| 69% | 0.714 | 0.333 | 0.471 |
| 80% | 0.646 | 0.286 | 0.471 |
| 91% | 0.500 | 0.281 | 0.529 |
| 100% | 0.338 | 0.257 | 0.529 |
