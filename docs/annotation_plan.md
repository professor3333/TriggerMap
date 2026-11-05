# Annotation plan

Target: about 800 gold advisories (500 train, 150 dev, 150 test), drawn from the frozen pools
in `splits/pool-v1.json` (see [`splits.md`](splits.md)). Every batch is committed under
`annotations/` *before* it is annotated, and no advisory appears in two samples (checked in CI).

| Sample | Pool | n | Strategy | Usable for | When to annotate |
|---|---|---:|---|---|---|
| `pilot/pilot_manifest.json` | mixed | 100 | 50 natural + 50 enriched | 39 train, 38 dev, 12 test (11 excluded) | done under v0.1 (`pilot-1`, revised as `pilot-2`) |
| `batches/batch-01.json` | train | 100 | natural | train | done under v0.2 (`batch-01`; model drafts, no `manual` records) |
| `batches/batch-02.json` | train | 100 | enriched (cue top quartile, ≤ 800 words) | train | done under v0.2 (`batch-02`; model drafts, no `manual` records) |
| `batches/batch-03.json` | dev | 112 | natural, ≤ 3 per leakage group | dev | done under v0.2 (`batch-03`; model drafts, no `manual` records) |
| `batches/batch-04.json` | test | 138 | natural, ≤ 2 per leakage group | test | **last**, after guidelines are frozen |
| `batches/batch-05.json` | train | 261 | 183 uncertainty from `crf-batches-01-02` + 78 natural, ≤ 3 per leakage group | train | next (drawn 2026-11-05) |
| `batches/batch-06.json` | dev | 60 | natural, ≤ 3 per leakage group | dev | done under v0.2 (`batch-06`; model drafts, no `manual` records) |

Totals when complete: train 39 + 100 + 100 + 261 = 500; dev 38 + 112 + 60 = 210;
test 12 + 138 = 150. Batch-06 was added to give dev hand-labelled documents, but it was
also submitted from model drafts; only 10 dev documents are `manual`.

## Rules

- **Evaluation pools are natural only.** Dev and test keep realistic class proportions;
  enriched and uncertainty sampling are used only in train (`sample-batch` refuses otherwise).
- **Test is annotated last.** Guidelines are frozen before anyone reads test documents, so
  rules are never adjusted to the test set.
- **Batches are immutable.** `sample-batch` refuses to overwrite a batch; a change means a new
  batch name.
- **Self-consistency:** after a gap of at least a week, re-annotate a random 10% of each batch
  blind. Report the result as self-consistency, never as inter-annotator agreement.

## Workflow per batch

```bash
uv run triggermap annotate tasks --sample annotations/batches/batch-01.json
# → data/label_studio/batch-01_tasks.json; import into a Label Studio project, annotate, export JSON
uv run triggermap annotate import data/label_studio/export-batch-01.json \
    --sample annotations/batches/batch-01.json --annotator A1 \
    --annotation-version batch-01 --out annotations/batches/batch-01.jsonl \
    --reference annotations/pilot/pilot-2.jsonl
```

`--reference` adds a *label mix* table to the import report. It compares the batch's role,
group-operator and document-status shares with earlier gold (test split excluded), and it
flags large shifts. A flag is a reason to check a sample of the batch against the guidelines
before training on it. It is not an error: batches are sampled differently, and guideline
versions differ.

Check the report's **Origin** table on every import. Records drafted by a model are training
data only. Only `manual` records count toward evaluation (see [`targets.md`](targets.md)).

## Label source decision (2026-11-05)

Batches 01, 02, 03 and 06 were all submitted from model drafts. The owner decided to continue
with model-drafted labels instead of hand labelling. Results against them are reported as
agreement with the drafting model, and the release gates in [`targets.md`](targets.md) cannot
be judged as declared. If hand labelling resumes, the procedure below still applies.

## Hand-labelled dev batch (batch-06)

Accuracy can only be measured against `manual` records, and every batch so far was submitted
from model drafts. Batch-06 is 60 natural dev documents for hand labelling. Its task file,
`data/label_studio/batch-06_tasks.json`, holds advisory text only, with no predictions.

1. In Label Studio, create a **new** project (for example "TriggerMap batch-06 (v0.2, manual)").
   Paste `configs/label_studio/condition_annotation.xml` as the labelling interface and import
   `data/label_studio/batch-06_tasks.json`.
2. Do not connect a model backend, and do not import or create predictions for this project.
3. Label each task in the interface and submit it there, so that Label Studio records working
   time. Use the frozen v0.2 guidelines and the notes field for doubts.
4. Export and import as usual, with `--annotation-version batch-06`. The Origin table must show
   `manual` for every record. Anything else means the batch does not add hand-labelled dev
   documents.

Smaller sittings are fine: a partial export can be imported, and each later import replaces
the earlier file.

## Batch-05 (uncertainty sample)

`batch-05` draws 261 unsampled train-pool documents: 183 where `crf-batches-01-02` is least
certain (confidences closest to 0.5) and a 78-document natural slice. The predictions that
chose them are committed at `reports/sampling/crf-batches-01-02_train_pool.jsonl`, and their
SHA-256 and model id are recorded in the manifest (`predictions`). Tasks:
`data/label_studio/batch-05_tasks.json` (no predictions).

The predictions cover the 2,211 train-pool documents that were in no earlier sample (no dev
or test text was predicted). The draw itself is deterministic:

```bash
uv run triggermap corpus sample-batch --name batch-05 --pool train --n 261 --strategy uncertainty \
    --predictions reports/sampling/crf-batches-01-02_train_pool.jsonl
```
