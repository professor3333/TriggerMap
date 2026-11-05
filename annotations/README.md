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
| `batches/batch-*_report.md` | Batch import reports. |

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

Records follow the schema in `src/triggermap/schema/models.py` and the rules in
`docs/annotation_guidelines.md`.
