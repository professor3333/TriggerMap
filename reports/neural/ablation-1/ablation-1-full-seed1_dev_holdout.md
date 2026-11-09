# Agreement with model drafts (held-out half): ablation-1-full-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-full-seed1.jsonl` (ablation-1-full-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.198 | [0.151, 0.259] |
| Exact span F1 | 0.225 | [0.177, 0.290] |
| Exact span precision | 0.156 | [0.117, 0.208] |
| Exact span recall | 0.407 | [0.328, 0.492] |
| Role macro-F1 (roles with gold support) | 0.121 | [0.082, 0.201] |
| Category macro-F1 | 0.171 | [0.130, 0.221] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.070 | [0.018, 0.137] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.567 | [0.490, 0.636] |
| Reversed meaning rate (lower is better) | 0.056 | [0.018, 0.101] |
| Category accuracy on exactly matched spans | 0.912 | [0.800, 1.000] |
| Role accuracy on exactly matched spans | 0.947 | [0.889, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.179 | 0.400 | 0.247 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.108 | 0.400 | 0.170 | 10 |
| UNCERTAIN | 0.037 | 0.250 | 0.065 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.120 | 0.333 | 0.176 | 18 |
| USAGE | 0.140 | 0.444 | 0.213 | 54 |
| ACCESS | 0.183 | 0.389 | 0.249 | 54 |
| PLATFORM | 0.033 | 0.071 | 0.045 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.935 | 0.405 | 0.107 |
| 20% | 0.853 | 0.288 | 0.150 |
| 30% | 0.762 | 0.300 | 0.236 |
| 40% | 0.704 | 0.260 | 0.271 |
| 50% | 0.618 | 0.219 | 0.286 |
| 60% | 0.567 | 0.195 | 0.307 |
| 70% | 0.512 | 0.172 | 0.314 |
| 80% | 0.477 | 0.160 | 0.336 |
| 90% | 0.412 | 0.149 | 0.350 |
| 100% | 0.226 | 0.137 | 0.357 |
