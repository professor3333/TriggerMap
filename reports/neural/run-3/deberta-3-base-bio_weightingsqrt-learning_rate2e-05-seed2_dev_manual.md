# Hand-labelled dev: deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Predictions: `reports/neural/predictions/deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed2.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed2)
- Bootstrap: 1000 resamples, project clusters, seed 0
- Documents: 10 (9 with gold conditions, 1 without)

## Headline metrics (95% bootstrap intervals)

| Metric | Estimate | 95% CI |
|---|---:|:---:|
| Typed condition micro-F1 (span + category + role) | 0.237 | [0.127, 0.379] |
| Exact span F1 | 0.316 | [0.190, 0.485] |
| Exact span precision | 0.203 | [0.114, 0.353] |
| Exact span recall | 0.706 | [0.538, 0.864] |
| Role macro-F1 (roles with gold support) | 0.172 | [0.102, 0.500] |
| Category macro-F1 | 0.251 | [0.113, 0.486] |
| Group exact-match F1 | 0.167 | [0.000, 0.462] |
| Complete-document exact match, documents with conditions | 0.111 | [0.000, 0.300] |
| Complete-document exact match, documents without conditions | 0.000 | [0.000, 0.000] |
| False prerequisite rate (lower is better) | 0.667 | [0.526, 0.767] |
| Reversed meaning rate (lower is better) | 0.000 | [0.000, 0.000] |
| Category accuracy on exactly matched spans | 0.833 | [0.545, 1.000] |
| Role accuracy on exactly matched spans | 0.917 | [0.692, 1.000] |

## Per-role results (exact span + role)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| REQUIRED | 0.229 | 0.688 | 0.344 | 16 |
| EXCEPTION | 0.000 | 0.000 | 0.000 | 0 |
| NOT_REQUIRED | 0.000 | 0.000 | 0.000 | 0 |
| UNCERTAIN | 0.000 | 0.000 | 0.000 | 1 |

## Per-category results (exact span + category)

| Label | Precision | Recall | F1 | Gold support |
|---|---:|---:|---:|---:|
| CONFIGURATION | 0.333 | 1.000 | 0.500 | 1 |
| USAGE | 0.163 | 0.778 | 0.269 | 9 |
| ACCESS | 0.167 | 0.400 | 0.235 | 5 |
| PLATFORM | 0.000 | 0.000 | 0.000 | 2 |

## Precision versus coverage

| Coverage | Confidence ≥ | Typed precision | Retained recall |
|---:|---:|---:|---:|
| 10% | 0.742 | 0.500 | 0.176 |
| 20% | 0.643 | 0.333 | 0.235 |
| 31% | 0.551 | 0.278 | 0.294 |
| 41% | 0.521 | 0.208 | 0.294 |
| 51% | 0.507 | 0.167 | 0.294 |
| 59% | 0.481 | 0.171 | 0.353 |
| 69% | 0.423 | 0.171 | 0.412 |
| 80% | 0.382 | 0.191 | 0.529 |
| 90% | 0.327 | 0.170 | 0.529 |
| 100% | 0.218 | 0.153 | 0.529 |
