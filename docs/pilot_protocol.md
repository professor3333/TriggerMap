# Pilot annotation protocol

The pilot is the Phase 1 decision gate. It answers three questions before large-scale
labelling starts:

1. **Is the label scheme understandable?** Can the guidelines be applied consistently, and
   which rules cause hesitation?
2. **Are there enough examples?** How often does each category, role and group operator
   occur, and which are too rare to support?
3. **What does annotation cost?** Measured minutes per document, which replaces the
   5–8 minute estimate in the plan.

## The sample

`annotations/pilot/pilot_manifest.json` (committed) lists 100 advisories from snapshot
`1912cbd6`, chosen by `triggermap corpus sample-pilot` (seed 20261020):

| Stratum | n | Selection | Later use |
|---|---:|---|---|
| `random` | 50 | Uniform over PyPI advisories, at most 2 per project group | Evaluation candidates |
| `enriched` | 50 | Top quartile of condition-cue score, at most 800 words | Training only |

At most one advisory per duplicate group is included. Tasks are shown in a shuffled order
that mixes the strata, so you cannot tell which stratum a document came from. **Annotate in
task order** and do not look up strata while annotating.

## Setup (once)

```bash
uv run triggermap annotate tasks          # writes data/label_studio/pilot_tasks.json
uvx --python 3.12 --from label-studio==1.23.2 label-studio start --data-dir data/label_studio/ls --port 8080
```

In Label Studio (http://localhost:8080):

1. Create a project named `TriggerMap pilot`.
2. **Labeling setup → Code**: paste `configs/label_studio/condition_annotation.xml`, then save.
3. **Import**: upload `data/label_studio/pilot_tasks.json`.
4. In the data manager, sort by the `order` column so tasks appear in task order.

## Annotating

- Keep `docs/annotation_guidelines.md` open, and follow the guideline version stated at its top.
- For each condition: select its text, choose a category (hotkeys `c u a p`), then choose a
  role (`1 2 3 4`).
- Link grouped conditions with relations (`ALL` / `ANY` / `UNRESOLVED`).
- Choose a document status for every task, including `NO_EXPLICIT_CONDITION` tasks.
- Write a note whenever you hesitate.
- Work in sessions of at most an hour. Label Studio measures time per task, so pause
  rather than leaving a task open while away.

## Import and check

Export from Label Studio as **JSON** (not JSON-MIN) to `data/label_studio/export.json`, then:

```bash
uv run triggermap annotate import data/label_studio/export.json --annotator A1
```

This writes `annotations/pilot/pilot-1.jsonl` (clean records only) and
`annotations/pilot/pilot-1_report.md`, which contains label counts, pace, and every issue to
fix. Fix issues in Label Studio, export again, and re-run until the report shows none. The
command exits non-zero while issues remain.

## Self-consistency (after a gap of at least one week)

Re-annotate a random 10% of the pilot without looking at your earlier labels. The agreement
between the two passes is reported as **self-consistency**, never as inter-annotator
agreement.

## Decision gate

These are proposed criteria for review together after the pilot:

- **Pace.** The measured median minutes per document sets the realistic size of the gold set
  within the 80–130 hour budget.
- **Support.** For each role and group operator, project the count at 800 documents from
  the pilot rates (strata reported separately). A class projected below about 50 examples is
  marked **unsupported** until targeted sampling finds more. It is never filled with
  invented examples.
- **Guidelines.** Every note and every issue category is reviewed. Rules that caused
  repeated hesitation are rewritten, and guideline version 0.2 is frozen before scaled
  annotation begins.
- **Targets.** Acceptance targets are written to `docs/targets.md` after the pilot and
  before any test-set results exist.
