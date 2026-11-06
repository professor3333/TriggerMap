# Agreement with model drafts: deberta-2-base-bio_weightingnone-learning_rate2e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Predictions: `reports/neural/predictions/deberta-2-base-bio_weightingnone-learning_rate2e-05-seed2.jsonl` (deberta-2-base-bio_weightingnone-learning_rate2e-05-seed2)
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
| Complete-document exact match, documents without conditions | 0.294 | [0.000, 0.542] |
| False prerequisite rate (lower is better) | 0.959 | [0.934, 0.978] |
| Reversed meaning rate (lower is better) | 0.472 | [0.294, 0.657] |
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
| 10% | 0.252 | 0.000 | 0.000 |
| 20% | 0.227 | 0.000 | 0.000 |
| 30% | 0.210 | 0.000 | 0.000 |
| 40% | 0.194 | 0.000 | 0.000 |
| 50% | 0.181 | 0.000 | 0.000 |
| 60% | 0.172 | 0.000 | 0.000 |
| 70% | 0.164 | 0.000 | 0.000 |
| 80% | 0.151 | 0.000 | 0.000 |
| 90% | 0.137 | 0.000 | 0.000 |
| 100% | 0.104 | 0.000 | 0.000 |
