# Agreement with model drafts (held-out half): ablation-1-no-context-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-no-context-seed0.jsonl` (ablation-1-no-context-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.227 | [0.177, 0.288] |
| Exact span F1 | 0.264 | [0.215, 0.329] |
| Exact span precision | 0.195 | [0.154, 0.255] |
| Exact span recall | 0.407 | [0.338, 0.489] |
| Role macro-F1 (roles with gold support) | 0.137 | [0.100, 0.211] |
| Category macro-F1 | 0.187 | [0.147, 0.244] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.070 | [0.000, 0.148] |
| Complete-document exact match, documents without conditions | 0.250 | [0.000, 0.500] |
| False prerequisite rate (lower is better) | 0.466 | [0.394, 0.535] |
| Reversed meaning rate (lower is better) | 0.065 | [0.020, 0.118] |
| Category accuracy on exactly matched spans | 0.912 | [0.820, 0.983] |
| Role accuracy on exactly matched spans | 0.947 | [0.875, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.231 | 0.400 | 0.293 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.139 | 0.500 | 0.217 | 10 |
| UNCERTAIN | 0.023 | 0.125 | 0.039 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.120 | 0.333 | 0.176 | 18 |
| USAGE | 0.172 | 0.407 | 0.242 | 54 |
| ACCESS | 0.264 | 0.444 | 0.331 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.970 | 0.379 | 0.079 |
| 20% | 0.909 | 0.431 | 0.179 |
| 30% | 0.819 | 0.409 | 0.257 |
| 40% | 0.721 | 0.333 | 0.279 |
| 50% | 0.646 | 0.281 | 0.293 |
| 60% | 0.587 | 0.251 | 0.314 |
| 70% | 0.542 | 0.230 | 0.336 |
| 80% | 0.506 | 0.205 | 0.343 |
| 90% | 0.446 | 0.183 | 0.343 |
| 100% | 0.202 | 0.168 | 0.350 |
