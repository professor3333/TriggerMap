# Agreement with model drafts (held-out half): ablation-1-docs-120-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-docs-120-seed1.jsonl` (ablation-1-docs-120-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.141 | [0.103, 0.198] |
| Exact span F1 | 0.163 | [0.119, 0.226] |
| Exact span precision | 0.110 | [0.078, 0.159] |
| Exact span recall | 0.314 | [0.237, 0.401] |
| Role macro-F1 (roles with gold support) | 0.056 | [0.039, 0.099] |
| Category macro-F1 | 0.102 | [0.073, 0.140] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.018 | [0.000, 0.052] |
| Complete-document exact match, documents without conditions | 0.750 | [0.000, 1.000] |
| False prerequisite rate (lower is better) | 0.629 | [0.546, 0.700] |
| Reversed meaning rate (lower is better) | 0.056 | [0.013, 0.109] |
| Category accuracy on exactly matched spans | 0.886 | [0.762, 0.978] |
| Role accuracy on exactly matched spans | 0.955 | [0.889, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.128 | 0.342 | 0.186 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 10 |
| UNCERTAIN | 0.022 | 0.125 | 0.037 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.034 | 0.111 | 0.052 | 18 |
| USAGE | 0.107 | 0.389 | 0.167 | 54 |
| ACCESS | 0.139 | 0.296 | 0.189 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.844 | 0.200 | 0.057 |
| 20% | 0.735 | 0.225 | 0.129 |
| 30% | 0.667 | 0.200 | 0.171 |
| 40% | 0.611 | 0.175 | 0.200 |
| 50% | 0.555 | 0.145 | 0.207 |
| 60% | 0.514 | 0.121 | 0.207 |
| 70% | 0.466 | 0.114 | 0.229 |
| 80% | 0.429 | 0.116 | 0.264 |
| 90% | 0.360 | 0.103 | 0.264 |
| 100% | 0.188 | 0.095 | 0.271 |
