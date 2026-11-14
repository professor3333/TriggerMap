# Consistency between two model drafting runs (batch-07, dev)

The 100 `batch-07` dev documents have been drafted twice. Both drafts were made by a model
under guidelines v0.2 and submitted unchanged. Neither one is hand-labelled.

| | Draft 1 | Draft 2 |
|---|---|---|
| File | `annotations/batches/batch-07.jsonl` | `annotations/second-drafts/batch-07.jsonl` |
| Label Studio project | 7 | 9 |
| Draft model version | `model-batch-07-guidelines-0.2` | `model-project9-guidelines-0.2` |
| Submitted | 2026-11-09 | 2026-11-12 → 2026-11-14, one task at a time |
| Origin | 100 `model_draft_accepted` | 100 `model_draft_accepted` |
| Conditions | 182 | 319 |
| Groups | 5 | 39 |
| Documents with no conditions | 13 | 14 |

Each draft-2 annotation is an unchanged copy of its pre-annotation. The pre-annotation was
created 8 to 80 seconds before the annotation was submitted, with a recorded annotation time of
0.9 s on average (23 s at most). Draft 2 was imported from the Label Studio export
`project-9-at-2026-11-14-08-43` (SHA-256 `f23f25a0…0c62`; not committed). The import report is
[`annotations/second-drafts/batch-07_report.md`](../../annotations/second-drafts/batch-07_report.md).

**What this measures.** The table shows how closely two model drafting runs agree with each
other. It is not accuracy, it is not inter-annotator agreement, and it is not human
self-consistency. Draft 2 is not used for training or model selection. The single-reference agreement results
still use draft 1. Systems are scored against both drafts in
[`../batch-07-comparison/`](../batch-07-comparison/README.md).

## Result

Draft 2 is scored with draft 1 as the reference
([`batch-07.md`](batch-07.md), reproduced by `bash scripts/experiments/drafter_consistency.sh`).
F1 is symmetric, so swapping the two drafts only swaps precision and recall. The intervals are
95% project-group bootstrap intervals, 1,000 resamples, seed 0.

| Metric | Draft 2 vs draft 1 |
|---|---:|
| Typed-condition micro-F1 (span + category + role) | 0.375 [0.309, 0.444] |
| Exact span F1 | 0.431 [0.366, 0.503] |
| Exact span precision / recall | 0.339 / 0.593 |
| Role macro-F1 | 0.377 [0.244, 0.495] |
| Category / role accuracy on spans both drafts mark | 0.935 / 0.935 |
| Group exact-match F1 | 0.091 [0.000, 0.200] |
| Whole document identical, documents with conditions (87) | 0.207 [0.122, 0.300] |
| Whole document identical, documents with no conditions (13) | 0.692 [0.417, 1.000] |
| Draft-2 conditions that draft 1 does not have (the "false prerequisite rate" row) | 0.395 [0.323, 0.462] |
| Role reversed between the drafts on the same span | 0.000 |

The report's precision–coverage table is meaningless here, because model drafts carry no
confidences.

## Reading

- **The two drafts mostly disagree on which spans are conditions, not on their labels.** When
  both drafts mark the same span, they give the same category and the same role 93.5% of the
  time, and no role is reversed. But draft 2 marks 1.75 times as many conditions (319 against
  182), and exact span F1 is only 0.431. Draft 2 also forms 39 groups where draft 1 forms 5, so
  groups almost never match (F1 0.091).
- **This puts the agreement scores in context.** Against the 172 model-drafted dev records of
  `batch-03` and `batch-06`, the CRF reaches 0.145 typed F1, and DeBERTa about 0.19 on their
  held-out half ([`reports/agreement/`](../agreement/README.md),
  [`reports/neural/run-3/`](../neural/run-3/README.md)). Two model drafting runs under the same
  guidelines agree with each other at only 0.375. A low agreement score therefore reflects
  unstable reference labels as well as model error. This is measured on one batch of 100
  documents, so it is an indication, not a fixed ceiling for the other batches.
- **It does not say which draft is right.** Only hand-labelled records can tell. There are 22,
  of which 10 are in dev and none are in batch-07.
