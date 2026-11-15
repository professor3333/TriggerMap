# Held-out test evaluation (declared release evaluation, 2026-11-15)

This is the one declared evaluation on the locked test split of `splits/pool-v1.json`. The owner
declared it on 2026-11-15 with the reason: *"Final held-out evaluation of v0.1.0 (CRF) and the
run-3 DeBERTa candidate; no hand labels will come."* Every scoring run is logged in
[`docs/test-access-log.md`](../../docs/test-access-log.md). Nothing was tuned on these results,
and no system changes because of them. The test split holds the newest project groups
(published 2024-04 → 2026-10), so the results measure **temporal and project shift**.

## Systems (frozen)

| System | Source | Conditions predicted (146 docs) |
|---|---|---:|
| `rules-2` | deterministic rules | 188 (1.3 per document) |
| CRF `crf-batches-01-02` (default) | release [v0.1.0](https://github.com/professor3333/TriggerMap/releases/tag/v0.1.0) | 297 (2.0 per document) |
| DeBERTa-v3-small `deberta-3-…sqrt…5e-05-seed2` | pre-release [model-deberta-3-run3](https://github.com/professor3333/TriggerMap/releases/tag/model-deberta-3-run3), downloaded and checked against its SHA-256 | 1,227 (8.4 per document) |

Before scoring, each system's predictions on the 88 pilot documents outside the test split
were confirmed identical to its committed dev predictions, so these are the same frozen
systems that the dev reports describe.

## Test data: two slices

| Slice | Documents | Gold conditions | What it measures |
|---|---:|---:|---|
| Model-drafted test records (138 `batch-04` + 8 `pilot-2`) | 146 (139 with conditions, 7 without) | 356 | **Agreement with the drafting model, not accuracy** |
| Hand-labelled test records (`pilot-2`, `origin: manual`) | 4 (3 with conditions, 1 without) | 7 | Accuracy, but far too few documents to conclude anything |

The `batch-04` labels were drafted by the same session and process as the first batch-07
draft (2026-11-09). That session read these test texts in order to draft them. No model was
developed, tuned or scored on them before this evaluation.

## Results: agreement, 146 model-drafted test records

95% project-group bootstrap intervals (1,000 resamples, seed 0).

| Metric | `rules-2` | CRF (default) | DeBERTa run 3 |
|---|---:|---:|---:|
| Typed-condition micro-F1 | 0.048 [0.021, 0.082] | **0.193 [0.154, 0.238]** | 0.154 [0.125, 0.186] |
| Exact span F1 | 0.070 [0.035, 0.110] | **0.239 [0.194, 0.288]** | 0.177 [0.146, 0.207] |
| Exact span precision | 0.101 [0.051, 0.168] | **0.263 [0.207, 0.335]** | 0.114 [0.092, 0.137] |
| Exact span recall | 0.053 [0.027, 0.081] | 0.219 [0.176, 0.266] | **0.393 [0.337, 0.444]** |
| Role macro-F1 | 0.017 [0.008, 0.028] | 0.132 [0.093, 0.179] | 0.125 [0.087, 0.171] |
| Group exact-match F1 | 0.000 | 0.000 | 0.000 |
| Document exact match, with conditions (139) | 0.000 | 0.058 [0.016, 0.101] | 0.043 [0.014, 0.075] |
| Document exact match, without conditions (7) | 0.857 [0.500, 1.000] | 0.857 [0.500, 1.000] | 0.571 [0.167, 1.000] |
| False-prerequisite rate (lower is better) | 0.646 [0.500, 0.762] | **0.482 [0.400, 0.556]** | 0.650 [0.605, 0.691] |
| Reversed-meaning rate (lower is better) | 0.043 [0.000, 0.102] | 0.037 [0.008, 0.073] | **0.005 [0.000, 0.014]** |

Per-role exact span + role F1, with gold support:

| Role (support) | CRF | DeBERTa run 3 |
|---|---:|---:|
| REQUIRED (299) | 0.240 | 0.202 |
| EXCEPTION (11) | 0.000 | 0.133 |
| NOT_REQUIRED (16) | 0.209 | 0.114 |
| UNCERTAIN (30) | 0.080 | 0.053 |

Per-category exact span + category F1, with gold support:

| Category (support) | CRF | DeBERTa run 3 |
|---|---:|---:|
| CONFIGURATION (57) | 0.188 | 0.188 |
| USAGE (166) | 0.203 | 0.149 |
| ACCESS (91) | 0.247 | 0.177 |
| PLATFORM (42) | 0.111 | 0.119 |

Paired differences (system minus CRF):

| Metric | DeBERTa run 3 − CRF | `rules-2` − CRF |
|---|---:|---:|
| Typed-condition micro-F1 | −0.039 [−0.080, −0.000] clearly worse (only just) | −0.145 [−0.190, −0.105] clearly worse |
| Exact span F1 | −0.062 [−0.106, −0.019] clearly worse | −0.169 [−0.221, −0.127] clearly worse |
| Exact span precision | −0.149 [−0.208, −0.101] clearly worse | −0.162 [−0.225, −0.111] clearly worse |
| Exact span recall | +0.174 [+0.119, +0.228] clearly better | −0.166 [−0.214, −0.125] clearly worse |
| False-prerequisite rate | +0.168 [+0.106, +0.239] clearly worse | +0.164 [+0.061, +0.268] clearly worse |
| Reversed-meaning rate | −0.032 [−0.067, −0.002] clearly better | +0.006 [−0.046, +0.066] not clear |

## Results: accuracy, 4 hand-labelled test records

| Metric | `rules-2` | CRF (default) | DeBERTa run 3 |
|---|---:|---:|---:|
| Typed-condition micro-F1 | 0.167 [0.000, 0.286] | 0.125 [0.000, 0.182] | 0.133 [0.000, 0.235] |
| Exact span F1 | 0.167 [0.000, 0.286] | 0.125 [0.000, 0.182] | 0.200 [0.000, 0.545] |
| False-prerequisite rate | 0.500 [0.000, 1.000] | 0.667 [0.000, 0.750] | 0.684 [0.500, 0.889] |

No paired difference on this slice is clear. Seven gold conditions in four documents cannot
separate these systems.

## Release targets

[`docs/targets.md`](../../docs/targets.md) judges the release gates on hand-labelled test
records only. With 4 such records, **the gates cannot be judged as declared**, and they are
reported as not judgeable. The targets were not changed after the fact.

## Reading

- **The CRF remains the right default.** On the 146 test records it agrees with the drafts
  better than DeBERTa (typed F1 0.193 against 0.154; the difference is clear but only just).
  It is far more precise (0.263 against 0.114) and invents clearly fewer prerequisites (0.482
  against 0.650). The pre-set rule kept the CRF before any test result was seen, and the test
  result supports that choice.
- **DeBERTa's dev lead did not transfer to the test drafts.** On dev it led the CRF without a
  clear difference (held-out typed F1 0.185 against 0.127). On test it trails. It predicts 8.4
  conditions per document where the test drafts mark 2.4, so its high recall (0.393) costs
  precision. This matches batch-07, where DeBERTa's lead was clear only against the denser
  second draft. Against drafts made the way `batch-04` was made, it had no clear lead there
  either.
- **DeBERTa is better at one of the two errors this project weighs most:** reversed meaning
  (0.005 against 0.037, clear). The CRF is better at the other: invented prerequisites.
- **Both systems remain weak in absolute terms.** No group is ever matched exactly, the CRF
  finds no EXCEPTION condition, and fewer than 6% of condition-bearing documents come out
  fully right. These are agreement scores against one drafting model on newer projects. They
  are not accuracy, and the 4 hand-labelled documents cannot settle accuracy.

## Reproduce

```bash
# predictions (frozen systems; DeBERTa from the model-deberta-3-run3 asset)
uv run triggermap predict --sample annotations/batches/batch-04.json annotations/pilot/pilot_manifest.json --out reports/test-evaluation/predictions/rules-2.jsonl
uv run triggermap predict --model crf --model-dir artifacts/crf-batches-01-02 --sample annotations/batches/batch-04.json annotations/pilot/pilot_manifest.json --out reports/test-evaluation/predictions/crf-batches-01-02.jsonl
uv run triggermap predict --model transformer --model-dir deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2 --sample annotations/batches/batch-04.json annotations/pilot/pilot_manifest.json --out reports/test-evaluation/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl
# scoring: a declared release evaluation only (it appends to docs/test-access-log.md)
bash scripts/experiments/test_evaluation.sh "<declared reason>"
```
