# Agreement with model drafts (held-out half): distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/predictions/distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed1.jsonl` (distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.069 | [0.036, 0.112] |
| Exact span F1 | 0.079 | [0.044, 0.128] |
| Exact span precision | 0.063 | [0.035, 0.105] |
| Exact span recall | 0.107 | [0.060, 0.169] |
| Role macro-F1 (roles with gold support) | 0.021 | [0.012, 0.038] |
| Category macro-F1 | 0.060 | [0.029, 0.110] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.018 | [0.000, 0.052] |
| Complete-document exact match, documents without conditions | 0.500 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.548 | [0.482, 0.603] |
| Reversed meaning rate (lower is better) | 0.028 | [0.000, 0.068] |
| Category accuracy on exactly matched spans | 0.933 | [0.765, 1.000] |
| Role accuracy on exactly matched spans | 0.933 | [0.769, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.064 | 0.117 | 0.083 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.059 | 0.056 | 0.057 | 18 |
| USAGE | 0.038 | 0.111 | 0.056 | 54 |
| ACCESS | 0.125 | 0.130 | 0.127 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.704 | 0.125 | 0.021 |
| 20% | 0.637 | 0.125 | 0.043 |
| 30% | 0.594 | 0.085 | 0.043 |
| 40% | 0.559 | 0.074 | 0.050 |
| 50% | 0.538 | 0.067 | 0.057 |
| 60% | 0.514 | 0.063 | 0.064 |
| 70% | 0.499 | 0.054 | 0.064 |
| 80% | 0.483 | 0.053 | 0.071 |
| 90% | 0.454 | 0.051 | 0.079 |
| 100% | 0.273 | 0.055 | 0.093 |
