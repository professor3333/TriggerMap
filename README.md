# TriggerMap

**Security advisories → evidence-linked exposure checklists.**

> Status: early development (Phase 1, feasibility). Nothing below the roadmap line is
> implemented yet; this README only describes features that exist.

A vulnerability alert tells you a dependency is affected. The advisory prose tells you *when*:
an optional feature must be enabled, a particular function used, the attacker already
authenticated, or several conditions must hold together. TriggerMap extracts those conditions
from English advisories for Python (PyPI) packages, classifies each one as a prerequisite,
an exception, or an explicitly unnecessary condition, keeps their ALL/ANY grouping, and links
every checklist item to the exact source text so a developer can verify it.

It complements dependency scanners such as
[OSV-Scanner](https://github.com/google/osv-scanner): the scanner says *which* dependency is
affected; TriggerMap surfaces the *conditions* stated in the advisory.

## Data

Advisories come from the public [GitHub Advisory Database](https://github.com/github/advisory-database)
(CC BY 4.0). The corpus is rebuilt from a pinned snapshot:

```bash
uv run triggermap ingest fetch --commit 1912cbd6ce9d4cb141636adc4abafb4eb77a93e6  # sparse clone, ~360 MB
uv run triggermap ingest build    # PyPI filter, withdrawn excluded, malformed quarantined
uv run triggermap corpus stats    # writes docs/corpus_stats.md
```

`ingest build` writes `data/processed/advisories.jsonl` (not committed) and the committed
manifest `data/manifests/snapshot.json`, which records the source commit, every filtering
count, quarantined files with reasons, and the SHA-256 of the output. Rebuilding from the same
commit reproduces the manifest byte for byte. Current counts are in
[`docs/corpus_stats.md`](docs/corpus_stats.md).

## Annotation

Gold labels are created by hand in [Label Studio](https://labelstud.io/) following
[`docs/annotation_guidelines.md`](docs/annotation_guidelines.md). Each condition is a span of the
canonical advisory text, with a category (`CONFIGURATION`, `USAGE`, `ACCESS`, `PLATFORM`), a
role (`REQUIRED`, `EXCEPTION`, `NOT_REQUIRED`, `UNCERTAIN`) and, where the text states it, an
`ALL`/`ANY`/`UNRESOLVED` group. The 100-document pilot sample is fixed in
[`annotations/pilot/pilot_manifest.json`](annotations/pilot/pilot_manifest.json); the procedure
is in [`docs/pilot_protocol.md`](docs/pilot_protocol.md).

```bash
uv run triggermap corpus sample-pilot     # reproduce the pilot sample (seed 20261020)
uv run triggermap annotate tasks          # Label Studio tasks for the sample
uv run triggermap annotate import data/label_studio/export.json --annotator A1
```

The importer validates every exported annotation (offsets, labels, groups, document status)
and writes only clean records, plus a report of problems, label counts and annotation pace.

## Development

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pytest
```
