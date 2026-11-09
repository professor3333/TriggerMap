# Agreement with model drafts (held-out half): ablation-1-no-context-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-no-context-seed1.jsonl` (ablation-1-no-context-seed1)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.198 | [0.154, 0.253] |
| Exact span F1 | 0.233 | [0.192, 0.288] |
| Exact span precision | 0.160 | [0.128, 0.203] |
| Exact span recall | 0.429 | [0.358, 0.505] |
| Role macro-F1 (roles with gold support) | 0.107 | [0.072, 0.176] |
| Category macro-F1 | 0.179 | [0.135, 0.237] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.070 | [0.018, 0.137] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.610 | [0.528, 0.675] |
| Reversed meaning rate (lower is better) | 0.030 | [0.000, 0.075] |
| Category accuracy on exactly matched spans | 0.917 | [0.831, 0.984] |
| Role accuracy on exactly matched spans | 0.933 | [0.850, 0.986] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.165 | 0.433 | 0.239 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.125 | 0.400 | 0.190 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.091 | 0.278 | 0.137 | 18 |
| USAGE | 0.112 | 0.407 | 0.175 | 54 |
| ACCESS | 0.270 | 0.500 | 0.351 | 54 |
| PLATFORM | 0.042 | 0.071 | 0.053 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.936 | 0.368 | 0.100 |
| 20% | 0.850 | 0.347 | 0.186 |
| 30% | 0.758 | 0.283 | 0.229 |
| 40% | 0.709 | 0.253 | 0.271 |
| 50% | 0.631 | 0.223 | 0.300 |
| 60% | 0.586 | 0.199 | 0.321 |
| 70% | 0.550 | 0.175 | 0.329 |
| 80% | 0.503 | 0.163 | 0.350 |
| 90% | 0.428 | 0.151 | 0.364 |
| 100% | 0.217 | 0.136 | 0.364 |
