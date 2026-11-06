# Agreement with model drafts (held-out half): deberta-3-base-bio_weightingnone-learning_rate2e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingnone-learning_rate2e-05-seed2.jsonl` (deberta-3-base-bio_weightingnone-learning_rate2e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.000 | [0.000, 0.000] |
| Exact span F1 | 0.005 | [0.000, 0.011] |
| Exact span precision | 0.003 | [0.000, 0.006] |
| Exact span recall | 0.021 | [0.000, 0.048] |
| Role macro-F1 (roles with gold support) | 0.001 | [0.000, 0.002] |
| Category macro-F1 | 0.001 | [0.000, 0.005] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.948 | [0.924, 0.966] |
| Reversed meaning rate (lower is better) | 0.522 | [0.393, 0.629] |
| Category accuracy on exactly matched spans | 0.333 | [0.000, 1.000] |
| Role accuracy on exactly matched spans | 0.333 | [0.000, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.002 | 0.008 | 0.003 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.000 | 0.000 | 0.000 | 18 |
| USAGE | 0.000 | 0.000 | 0.000 | 54 |
| ACCESS | 0.003 | 0.019 | 0.005 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.262 | 0.000 | 0.000 |
| 20% | 0.235 | 0.000 | 0.000 |
| 30% | 0.214 | 0.000 | 0.000 |
| 40% | 0.200 | 0.000 | 0.000 |
| 50% | 0.189 | 0.000 | 0.000 |
| 60% | 0.178 | 0.000 | 0.000 |
| 70% | 0.169 | 0.000 | 0.000 |
| 80% | 0.157 | 0.000 | 0.000 |
| 90% | 0.144 | 0.000 | 0.000 |
| 100% | 0.097 | 0.000 | 0.000 |
