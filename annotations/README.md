# Annotations

Condition-level annotations of security advisories from the
[GitHub Advisory Database](https://github.com/github/advisory-database).

## License and attribution

The advisory text is © its respective authors and GitHub, published in the GitHub Advisory
Database under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The annotations in this
directory are derived from that text. They are **modified material**: condition spans,
categories, roles, groups and document status were added by the TriggerMap project. They are
released under CC BY 4.0.

Each record carries its advisory ID (link: `https://github.com/advisories/<advisory_id>`), the
advisory-database commit it was taken from, and the SHA-256 of the annotated text.

## Contents

| Path | What |
|---|---|
| `pilot/pilot_manifest.json` | The 100-document pilot sample: IDs, strata, project groups, hashes. |
| `pilot/pilot-1.jsonl` | Pilot annotations as first submitted, 100 records. One `AdvisoryAnnotation` per line. |
| `pilot/pilot-2.jsonl` | Current pilot version: `pilot-1` after 43 model drafts were revised (see below). |
| `pilot/pilot-*_report.md` | Import reports: label counts, origins, annotation pace. |
| `batches/batch-NN.json` | Batch samples (IDs, pools, strategy), committed before annotation. |
| `batches/batch-01.jsonl` | Batch-01 annotations (train pool), 100 records, guidelines v0.2. |
| `batches/batch-02.jsonl` | Batch-02 annotations (train pool, enriched), 100 records, guidelines v0.2. |
| `batches/batch-03.jsonl` | Batch-03 annotations (dev pool, natural), 112 records, guidelines v0.2. |
| `batches/batch-06.jsonl` | Batch-06 annotations (dev pool, natural), 60 records, guidelines v0.2. |
| `batches/batch-07.jsonl` | Batch-07 annotations (dev pool, natural), 100 records, guidelines v0.2. |
| `batches/batch-04.jsonl` | Batch-04 annotations (test pool, natural), 138 records, guidelines v0.2. |
| `batches/batch-*_report.md` | Batch import reports. |
| `second-drafts/batch-07.jsonl` | A second model draft of the same 100 batch-07 documents (Label Studio project 9). Used to measure consistency between drafting runs and as a second reference next to draft 1; never training or selection data. |

## Origin

Each record's `origin` states how its labels were made, read from Label Studio's own fields:

| Origin | Meaning |
|---|---|
| `manual` | Submitted without a Label Studio pre-annotation (labelled by hand in the tool). |
| `model_draft_accepted` | A model pre-annotation submitted with its labels unchanged (`origin_model` names it). |
| `model_draft_edited` | A model pre-annotation changed in the Label Studio interface (working time recorded). |
| `model_draft_revised` | A model pre-annotation changed with no working time recorded (saved through the API or a script). Not evidence of human editing. |

In `pilot-1`, 22 records are `manual` and 78 are `model_draft_accepted`
(`model-pilot-draft-2026-11-01-v1`). In `pilot-2`, 22 are `manual`, 52 `model_draft_accepted`
and 26 `model_draft_revised`. Both versions follow guidelines v0.1. Evaluation reports score the two separately: a score against
an accepted model draft measures agreement with that model, not accuracy. `adjudicated` is
`false` for every pilot record (there is no second annotator yet).

`batch-01` (train pool, guidelines v0.2) has no `manual` records: 99 are `model_draft_accepted`
and 1 is `model_draft_revised` (`model-batch-01-guidelines-0.2`), with no annotation time
recorded. It is training data only. It does not count toward the hand-labelled gold target,
and a model trained on it learns from the drafting model's labels.

`batch-02` (train pool, enriched sample, guidelines v0.2) has no `manual` records either: 99 are
`model_draft_accepted` and 1 is `model_draft_revised`, with no annotation time recorded. Orders
0–49 come from `model-batch-02-guidelines-0.2`, and orders 50–99 from
`model-batch-02-predraft-guidelines-0.2`. Orders 50–99 were submitted through the Label Studio
API, so their export entries do not carry the parent prediction inline. For the import, each one
was filled in from Label Studio's own database by its `parent_prediction` id, and that model
version string and note prefix were normalised to the `model-…` / `MODEL PRE-ANNOTATION` form.
No label was changed. Batch-02 is training data only.

`batch-03` (dev pool, natural sample, guidelines v0.2) has no `manual` records: all 112 are
`model_draft_accepted` (`model-batch-03-guidelines-0.2`), with no annotation time recorded.
Scores against it measure agreement with the drafting model, not accuracy, so it does not add
hand-labelled dev documents. `evaluate --gold-origin manual` excludes it, and `calibrate` and
`errors` exclude it by default.

`batch-06` (dev pool, natural sample, guidelines v0.2) was drawn for hand labelling, but all
60 records are `model_draft_accepted` (`model-batch-06-guidelines-0.2`), with no annotation time
recorded. On 2026-11-05 the owner decided to continue with model-drafted labels, so results
against these batches are reported as agreement with the drafting model, not accuracy.

`batch-07` (dev pool, 100 records) and `batch-04` (test pool, 138 records), guidelines v0.2,
were also drawn for hand labelling and were submitted from model drafts on 2026-11-09, by the
owner's decision: every record is `model_draft_accepted` (`model-batch-07-guidelines-0.2`,
`model-batch-04-guidelines-0.2`), with no annotation time recorded. The drafting process read
the batch-04 test texts; no model was developed, tuned or scored on them. CI checks batch-04
records for provenance only.

`second-drafts/batch-07.jsonl` (annotation version `batch-07-draft-2`) redrafts the same
100 batch-07 documents. It was submitted one task at a time between 2026-11-12 and 2026-11-14,
and every record is `model_draft_accepted` (`model-project9-guidelines-0.2`): each one is an
unchanged copy of a pre-annotation made seconds earlier. It does not replace
`batches/batch-07.jsonl` and is not used for training or selection. Its consistency with
draft 1 is in [`reports/drafter-consistency/`](../reports/drafter-consistency/README.md), and
systems are scored against both drafts in
[`reports/batch-07-comparison/`](../reports/batch-07-comparison/README.md).

Records follow the schema in `src/triggermap/schema/models.py` and the rules in
`docs/annotation_guidelines.md`.
