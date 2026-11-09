# Agreement with model drafts (held-out half): ablation-1-no-context-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-no-context-seed2.jsonl` (ablation-1-no-context-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.173 | [0.129, 0.230] |
| Exact span F1 | 0.208 | [0.160, 0.267] |
| Exact span precision | 0.149 | [0.111, 0.197] |
| Exact span recall | 0.343 | [0.271, 0.427] |
| Role macro-F1 (roles with gold support) | 0.080 | [0.055, 0.137] |
| Category macro-F1 | 0.138 | [0.101, 0.179] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.053 | [0.000, 0.111] |
| Complete-document exact match, documents without conditions | 0.250 | [0.000, 0.500] |
| False prerequisite rate (lower is better) | 0.506 | [0.432, 0.579] |
| Reversed meaning rate (lower is better) | 0.053 | [0.014, 0.095] |
| Category accuracy on exactly matched spans | 0.896 | [0.816, 0.973] |
| Role accuracy on exactly matched spans | 0.938 | [0.860, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.170 | 0.358 | 0.231 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.057 | 0.200 | 0.089 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.067 | 0.167 | 0.095 | 18 |
| USAGE | 0.121 | 0.352 | 0.180 | 54 |
| ACCESS | 0.216 | 0.389 | 0.278 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.956 | 0.312 | 0.071 |
| 20% | 0.864 | 0.359 | 0.164 |
| 30% | 0.750 | 0.309 | 0.214 |
| 40% | 0.687 | 0.240 | 0.221 |
| 50% | 0.621 | 0.224 | 0.257 |
| 60% | 0.575 | 0.187 | 0.257 |
| 70% | 0.530 | 0.164 | 0.264 |
| 80% | 0.488 | 0.155 | 0.286 |
| 90% | 0.427 | 0.138 | 0.286 |
| 100% | 0.224 | 0.124 | 0.286 |
