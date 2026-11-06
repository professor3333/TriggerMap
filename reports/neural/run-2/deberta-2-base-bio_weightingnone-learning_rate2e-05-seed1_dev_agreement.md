# Agreement with model drafts: deberta-2-base-bio_weightingnone-learning_rate2e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/deberta-2-base-bio_weightingnone-learning_rate2e-05-seed1.jsonl` (deberta-2-base-bio_weightingnone-learning_rate2e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 172 (155 with gold conditions, 17 without)

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
| False prerequisite rate (lower is better) | 0.937 | [0.883, 0.980] |
| Reversed meaning rate (lower is better) | 0.090 | [0.016, 0.191] |
| Category accuracy on exactly matched spans | 0.000 | [0.000, 0.000] |
| Role accuracy on exactly matched spans | 0.000 | [0.000, 0.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.000 | 0.000 | 0.000 | 323 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 17 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 18 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 28 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 36 |
| USAGE | 0.000 | 0.000 | 0.000 | 186 |
| ACCESS | 0.000 | 0.000 | 0.000 | 134 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 30 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.309 | 0.000 | 0.000 |
| 20% | 0.273 | 0.000 | 0.000 |
| 30% | 0.249 | 0.000 | 0.000 |
| 40% | 0.231 | 0.000 | 0.000 |
| 50% | 0.212 | 0.000 | 0.000 |
| 60% | 0.197 | 0.000 | 0.000 |
| 70% | 0.183 | 0.000 | 0.000 |
| 80% | 0.169 | 0.000 | 0.000 |
| 90% | 0.154 | 0.000 | 0.000 |
| 100% | 0.101 | 0.000 | 0.000 |
