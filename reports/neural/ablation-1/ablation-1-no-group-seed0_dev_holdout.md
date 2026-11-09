# Agreement with model drafts (held-out half): ablation-1-no-group-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-no-group-seed0.jsonl` (ablation-1-no-group-seed0)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 61 (57 with gold conditions, 4 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.193 | [0.139, 0.258] |
| Exact span F1 | 0.224 | [0.170, 0.291] |
| Exact span precision | 0.162 | [0.121, 0.216] |
| Exact span recall | 0.364 | [0.288, 0.449] |
| Role macro-F1 (roles with gold support) | 0.121 | [0.078, 0.199] |
| Category macro-F1 | 0.166 | [0.117, 0.218] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.053 | [0.000, 0.131] |
| Complete-document exact match, documents without conditions | 0.250 | [0.000, 0.500] |
| False prerequisite rate (lower is better) | 0.459 | [0.391, 0.526] |
| Reversed meaning rate (lower is better) | 0.047 | [0.015, 0.085] |
| Category accuracy on exactly matched spans | 0.882 | [0.761, 0.971] |
| Role accuracy on exactly matched spans | 0.980 | [0.933, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.193 | 0.375 | 0.255 | 120 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 2 |
| NOT_REQUIRED | 0.147 | 0.500 | 0.227 | 10 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 8 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.146 | 0.389 | 0.212 | 18 |
| USAGE | 0.122 | 0.333 | 0.179 | 54 |
| ACCESS | 0.215 | 0.370 | 0.272 | 54 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 14 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.986 | 0.469 | 0.107 |
| 20% | 0.946 | 0.381 | 0.171 |
| 30% | 0.892 | 0.319 | 0.214 |
| 40% | 0.782 | 0.278 | 0.250 |
| 50% | 0.704 | 0.234 | 0.264 |
| 60% | 0.646 | 0.222 | 0.300 |
| 70% | 0.579 | 0.195 | 0.307 |
| 80% | 0.537 | 0.171 | 0.307 |
| 90% | 0.466 | 0.151 | 0.307 |
| 100% | 0.179 | 0.140 | 0.314 |
