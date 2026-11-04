# Annotation plan

Target: about 800 gold advisories (500 train, 150 dev, 150 test), drawn from the frozen pools
in `splits/pool-v1.json` (see [`splits.md`](splits.md)). Every batch is committed under
`annotations/` *before* it is annotated, and no advisory appears in two samples (checked in CI).

| Sample | Pool | n | Strategy | Usable for | When to annotate |
|---|---|---:|---|---|---|
| `pilot/pilot_manifest.json` | mixed | 100 | 50 natural + 50 enriched | 39 train, 38 dev, 12 test (11 excluded) | done under v0.1 (`pilot-1`, revised as `pilot-2`) |
| `batches/batch-01.json` | train | 100 | natural | train | done under v0.2 (`batch-01`; model drafts, no `manual` records) |
| `batches/batch-02.json` | train | 100 | enriched (cue top quartile, ≤ 800 words) | train | after guidelines v0.2 |
| `batches/batch-03.json` | dev | 112 | natural, ≤ 3 per leakage group | dev | after guidelines v0.2 |
| `batches/batch-04.json` | test | 138 | natural, ≤ 2 per leakage group | test | **last**, after guidelines are frozen |
| `batches/batch-05…` | train | ≈ 261 | uncertainty from the first CRF + 30% natural | train | after batches 01–03 |

Totals when complete: train 39 + 100 + 100 + ≈ 261 ≈ 500; dev 38 + 112 = 150;
test 12 + 138 = 150.

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
