# Agreement with model drafts (held-out half): ablation-1-no-group-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-no-group-seed2.jsonl` (ablation-1-no-group-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.134 | [0.100, 0.181] |
| Exact span F1 | 0.170 | [0.132, 0.221] |
| Exact span precision | 0.108 | [0.081, 0.147] |
| Exact span recall | 0.400 | [0.331, 0.486] |
| Role macro-F1 (roles with gold support) | 0.091 | [0.057, 0.179] |
| Category macro-F1 | 0.106 | [0.081, 0.139] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.667 | [0.600, 0.722] |
| Reversed meaning rate (lower is better) | 0.044 | [0.016, 0.074] |
| Category accuracy on exactly matched spans | 0.804 | [0.702, 0.909] |
| Role accuracy on exactly matched spans | 0.964 | [0.911, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.124 | 0.408 | 0.190 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.087 | 0.400 | 0.143 | 10 |
| UNCERTAIN | 0.018 | 0.125 | 0.031 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.050 | 0.222 | 0.082 | 18 |
| USAGE | 0.092 | 0.426 | 0.152 | 54 |
| ACCESS | 0.134 | 0.333 | 0.191 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.713 | 0.250 | 0.093 |
| 20% | 0.627 | 0.173 | 0.129 |
| 30% | 0.567 | 0.142 | 0.157 |
| 40% | 0.519 | 0.135 | 0.200 |
| 50% | 0.492 | 0.131 | 0.243 |
| 60% | 0.461 | 0.116 | 0.257 |
| 70% | 0.417 | 0.107 | 0.279 |
| 80% | 0.373 | 0.094 | 0.279 |
| 90% | 0.323 | 0.090 | 0.300 |
| 100% | 0.162 | 0.085 | 0.314 |
