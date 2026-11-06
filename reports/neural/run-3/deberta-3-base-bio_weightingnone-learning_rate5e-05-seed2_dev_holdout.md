# Agreement with model drafts (held-out half): deberta-3-base-bio_weightingnone-learning_rate5e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingnone-learning_rate5e-05-seed2.jsonl` (deberta-3-base-bio_weightingnone-learning_rate5e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.129 | [0.086, 0.183] |
| Exact span F1 | 0.165 | [0.118, 0.221] |
| Exact span precision | 0.129 | [0.091, 0.181] |
| Exact span recall | 0.229 | [0.161, 0.297] |
| Role macro-F1 (roles with gold support) | 0.094 | [0.045, 0.171] |
| Category macro-F1 | 0.109 | [0.076, 0.143] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.500 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.430 | [0.358, 0.498] |
| Reversed meaning rate (lower is better) | 0.044 | [0.016, 0.074] |
| Category accuracy on exactly matched spans | 0.906 | [0.805, 1.000] |
| Role accuracy on exactly matched spans | 0.875 | [0.758, 0.971] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.121 | 0.208 | 0.153 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.176 | 0.300 | 0.222 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.044 | 0.111 | 0.063 | 18 |
| USAGE | 0.128 | 0.259 | 0.172 | 54 |
| ACCESS | 0.173 | 0.241 | 0.202 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.756 | 0.080 | 0.014 |
| 20% | 0.664 | 0.160 | 0.057 |
| 30% | 0.625 | 0.160 | 0.086 |
| 40% | 0.576 | 0.140 | 0.100 |
| 50% | 0.549 | 0.129 | 0.114 |
| 60% | 0.519 | 0.114 | 0.121 |
| 70% | 0.500 | 0.121 | 0.150 |
| 80% | 0.464 | 0.116 | 0.164 |
| 90% | 0.391 | 0.112 | 0.179 |
| 100% | 0.206 | 0.100 | 0.179 |
