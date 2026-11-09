# Hand-labelled dev: ablation-1-no-group-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/ablation-1/predictions/ablation-1-no-group-seed2.jsonl` (ablation-1-no-group-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.177 | [0.068, 0.304] |
| Exact span F1 | 0.203 | [0.100, 0.338] |
| Exact span precision | 0.129 | [0.063, 0.234] |
| Exact span recall | 0.471 | [0.222, 0.692] |
| Role macro-F1 (roles with gold support) | 0.115 | [0.047, 0.343] |
| Category macro-F1 | 0.212 | [0.084, 0.437] |
| Group exact-match F1 | 0.000 | [0.000, 0.000] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.622 | [0.424, 0.767] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 1.000 | [1.000, 1.000] |
| Role accuracy on exactly matched spans | 0.875 | [0.500, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.156 | 0.438 | 0.230 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.250 | 1.000 | 0.400 | 1 |
| USAGE | 0.119 | 0.556 | 0.196 | 9 |
| ACCESS | 0.182 | 0.400 | 0.250 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.773 | 0.500 | 0.176 |
| 19% | 0.719 | 0.333 | 0.235 |
| 31% | 0.627 | 0.263 | 0.294 |
| 40% | 0.562 | 0.240 | 0.353 |
| 50% | 0.531 | 0.226 | 0.412 |
| 60% | 0.505 | 0.189 | 0.412 |
| 69% | 0.454 | 0.163 | 0.412 |
| 81% | 0.388 | 0.140 | 0.412 |
| 90% | 0.323 | 0.125 | 0.412 |
| 100% | 0.271 | 0.113 | 0.412 |
