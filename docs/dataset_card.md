# Dataset card: TriggerMap condition annotations

Condition-level annotations of English security advisories for Python (PyPI) packages. Each
annotation marks the *deployment conditions* that make a vulnerability reachable, as exact
character spans with a category, a role and optional logical groups.

**Status (2026-11-05): in progress.** 472 advisories are annotated (the 100-document pilot and
batches 01, 02, 03 and 06). Only 22 are hand-labelled: from batch-01 on, every batch was
submitted from model drafts, and the owner decided on 2026-11-05 to continue that way. Most of these labels were drafted by a model; see [Label origin](#label-origin). The
target is about 800 advisories ([`annotation_plan.md`](annotation_plan.md)).

## Source

| | |
|---|---|
| Database | [GitHub Advisory Database](https://github.com/github/advisory-database), `advisories/github-reviewed/` (OSV JSON) |
| Pinned commit | `1912cbd6ce9d4cb141636adc4abafb4eb77a93e6` (2026-10-20) |
| Snapshot manifest | [`data/manifests/snapshot.json`](../data/manifests/snapshot.json), SHA-256 `3e8c50779feb84006d35b9621973dcee45a33d410cf203615a7f1745ce27d66f` |
| Corpus file | `data/processed/advisories.jsonl` (not committed; rebuilt by `triggermap ingest build`), SHA-256 `734043ff982a337f6cc593745160e997f20ee62609183ff857edce3d47d2b655` |
| Preprocessing version | `1` |

Pages linked from an advisory's `references` are **not** ingested.

## Filtering

| Step | Files |
|---|---:|
| Scanned | 36,910 |
| Excluded: no PyPI package affected | 30,324 |
| Excluded: withdrawn | 236 |
| Quarantined (malformed) | 0 |
| **Kept** | **6,350** |

The kept advisories name 1,528 distinct PyPI packages. Their median length is 98 whitespace
tokens (p90 559), and 15.7% are longer than 384 whitespace tokens. Details are in
[`corpus_stats.md`](corpus_stats.md).

## Annotation scheme

The label inventory is defined in `src/triggermap/schema/models.py`, with rules in
[`annotation_guidelines.md`](annotation_guidelines.md) (v0.1 for the pilot, v0.2 frozen
2026-11-02 for batches).

- **Condition:** a half-open `[start, end)` span in the canonical text.
  - Category: `CONFIGURATION`, `USAGE`, `ACCESS` or `PLATFORM`.
  - Role: `REQUIRED`, `EXCEPTION`, `NOT_REQUIRED` or `UNCERTAIN`.
- **Group:** a flat `ALL`, `ANY` or `UNRESOLVED` group of at least two conditions in one sentence
  or list block. A condition belongs to at most one group.
- **Document status:** `HAS_CONDITIONS`, `NO_EXPLICIT_CONDITION` or `UNSUPPORTED_STRUCTURE`.

Not labelled as conditions:
- consequences and impact;
- workarounds;
- affected version ranges;
- background mentions of a feature;
- CVSS, CWE and package metadata.

Every record carries the advisory ID, the source commit, the SHA-256 of the annotated text,
the preprocessing, annotation and schema versions, the annotator's pseudonym and the label
origin.

Records are checked at two points:
- **At import** (`annotate import`), against the canonical text: spans are in bounds, do not
  overlap, and do not start or end in whitespace.
- **In CI**, on every committed record (`tests/test_committed_annotations.py`):
  - labels come from the inventory;
  - condition ids are unique and spans do not overlap;
  - group members exist and groups are valid;
  - the document status agrees with the conditions;
  - the text hash, snapshot commit and preprocessing version match the record's sample and
    the pinned snapshot.

CI has no corpus, so it cannot check span text. For records in the test split, CI checks
provenance only.

## Label origin

| Version | Records | `manual` | `model_draft_accepted` | `model_draft_revised` | Guidelines |
|---|---:|---:|---:|---:|---|
| `pilot-2` (supersedes `pilot-1`) | 100 | 22 | 52 | 26 | v0.1 |
| `batch-01` | 100 | 0 | 99 | 1 | v0.2 |
| `batch-02` | 100 | 0 | 99 | 1 | v0.2 |
| `batch-03` | 112 | 0 | 112 | 0 | v0.2 |
| `batch-06` | 60 | 0 | 60 | 0 | v0.2 |

- **`manual`:** labelled by hand in Label Studio, with working time recorded.
- **`model_draft_accepted`:** a model pre-annotation submitted unchanged.
- **`model_draft_revised`:** a pre-annotation changed with no working time recorded, so this is
  not evidence of human editing.

Only `manual` records measure accuracy. All 22 `manual` records are in `pilot-2` (10 of them in
dev), so every batch so far is model-drafted. Model-drafted records are used for training, and scores
against them measure agreement with the drafting model. No record has been adjudicated by a
second annotator.

## Splits

Before scaled annotation, every kept advisory was assigned to a pool
([`splits.md`](splits.md), frozen manifest `splits/pool-v1.json`). Advisories are grouped
before assignment when they share:
- a package;
- an upstream repository;
- an alias;
- identical text;
- near-duplicate details (MinHash, Jaccard ≥ 0.6).

| Pool | Advisories | Leakage groups | Published |
|---|---:|---:|---|
| train | 2,450 | 347 | 2018-07 → 2026-10 |
| dev | 2,703 | 423 | 2018-07 → 2026-10 |
| test | 1,197 | 558 | 2024-04 → 2026-10 |

Test holds the newest groups, so test results measure **temporal and project shift**.

Annotated so far, by split:

| | Train | Dev | Test | Excluded |
|---|---:|---:|---:|---:|
| `pilot-2` | 39 | 38 | 12 | 11 (enriched, sharing a group with a natural document) |
| `batch-01` | 100 | 0 | 0 | 0 |
| `batch-02` | 100 | 0 | 0 | 0 |
| `batch-03` | 0 | 112 | 0 | 0 |
| `batch-06` | 0 | 60 | 0 | 0 |

Test records are never read for development, and no test evaluation has been run ([`test-access-log.md`](test-access-log.md) has no entries).

## Sampling

- **Pilot:** 50 random documents and 50 keyword-enriched documents.
- **Batches:** natural samples from one pool each (batch-01 train, batch-03 dev, batch-04 test).
  Batch-02 is an enriched train sample, and batch-05 is an uncertainty-selected train sample.
  Evaluation pools take natural samples only, so their class proportions stay realistic.

## Known biases and limitations

- **One source, one ecosystem, one language:** GitHub-reviewed advisories, PyPI only, English
  only.
- **Leakage across records:** advisories are copied across packages, aliases and revisions.
  Grouping removes the duplicates it can detect, but full independence is not guaranteed.
- **Writing style varies strongly by project.** Large projects (the biggest leakage group,
  TensorFlow, has 433 advisories) can dominate a pool.
- **Most current labels come from model drafts.** The label mix also shifts between versions.
  Against `pilot-2`, `batch-01` has many more `UNCERTAIN` roles (23.2% against 1.1%) and
  `NOT_REQUIRED` roles (12.2% against 3.0%); see `annotations/batches/batch-01_report.md`.
  `batch-02` (enriched) has 23.2% `UNCERTAIN` against 13.2% in `pilot-2` plus `batch-01`
  (`annotations/batches/batch-02_report.md`).
- **Rare classes are unsupported.** `EXCEPTION`, `UNCERTAIN` and `UNRESOLVED` are rare, and the
  pilot gate marks `UNCERTAIN` and `UNRESOLVED` unsupported ([`pilot_gate.md`](pilot_gate.md)).
- **There is a single annotator.** Repeat annotation will be reported as self-consistency,
  never as inter-annotator agreement.

## License and attribution

Advisory text © its authors and GitHub, published under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The annotations are modified
material derived from that text and are released under CC BY 4.0 (see
[`annotations/README.md`](../annotations/README.md)). Each record links to its advisory through
`https://github.com/advisories/<advisory_id>`. The code is MIT.
