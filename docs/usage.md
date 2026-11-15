# Usage

Every command below was rerun against the project on 2026-11-15 (release v0.2.0), except the GPU
scripts, which ran on a Kaggle T4 for the training runs. Run them from the repository root.
`uv run` syncs the environment first; add `--no-sync` to skip that.

## Set up

Requires [uv](https://docs.astral.sh/uv/) and Git.

```bash
git clone https://github.com/professor3333/TriggerMap.git && cd TriggerMap
uv sync                                    # Python 3.12 environment from uv.lock
uv run pytest -m "not slow"                # offline test suite
```

**Rebuild the corpus** from the pinned snapshot:

```bash
uv run triggermap ingest fetch --commit 1912cbd6ce9d4cb141636adc4abafb4eb77a93e6   # sparse clone, ~360 MB
uv run triggermap ingest build             # PyPI filter, withdrawn excluded, malformed quarantined
uv run triggermap corpus stats             # writes docs/corpus_stats.md
```

`ingest build` writes `data/processed/advisories.jsonl` (not committed) and the committed
[`data/manifests/snapshot.json`](../data/manifests/snapshot.json). The manifest records the source
commit, every filtering count, each quarantined file with its reason, and the SHA-256 of the
output. Rebuilding from the same commit reproduces it byte for byte.

A full fresh-clone check (`bash scripts/reproduce/clean_clone.sh EMPTY_DIR`) rebuilds the corpus,
retrains the CRF and regenerates the rules, CRF and agreement reports. On 2026-11-14 every
regenerated file was byte-identical to the commit on macOS arm64 and on Linux x86-64 (Docker). Tolerances and what is not
covered (transformer retraining) are in [`docs/reproducibility.md`](reproducibility.md).

**Extract and review** (rules baseline; no labels needed):

```bash
uv sync --extra baselines                  # adds CRF, scikit-learn and spaCy for the trained baseline
uv run triggermap view GHSA-m2qf-hxjv-5gpq --out review.html          # evidence-linked review page
uv run triggermap view --text-file advisory.md --out review.html      # any pasted advisory text
uv run triggermap predict --out data/predictions/rules-2.jsonl        # whole corpus, validated output
```

**Train and evaluate** (once gold labels exist):

```bash
uv run triggermap train --gold annotations/pilot/pilot-1.jsonl --out artifacts/crf-1   # --origin manual: hand-made labels only
uv run triggermap predict --model crf --model-dir artifacts/crf-1 --out data/predictions/crf-1.jsonl
uv run triggermap evaluate annotations/pilot/pilot-1.jsonl data/predictions/crf-1.jsonl --out reports/crf-1.md
uv run triggermap compare annotations/pilot/pilot-2.jsonl reports/pilot/predictions/rules-2.jsonl \
    reports/pilot/predictions/crf-pilot-2.jsonl --gold-origin manual   # paired bootstrap, B - A
uv run triggermap evaluate annotations/batches/batch-03.jsonl reports/agreement/predictions/crf-batches-01-02.jsonl \
    --add-gold annotations/batches/batch-06.jsonl --split dev   # agreement with model drafts, not accuracy
uv run triggermap multiref annotations/batches/batch-07.jsonl annotations/second-drafts/batch-07.jsonl \
    reports/batch-07-comparison/predictions/crf-batches-01-02.jsonl reports/batch-07-comparison/predictions/rules-2.jsonl
```

**Transformers** (DistilBERT, DeBERTa-v3-small; needs a CUDA GPU, see
[`docs/training_on_gpu.md`](training_on_gpu.md)):

```bash
bash scripts/gpu/run_neural.sh                       # on the GPU machine: both grids, packed results
bash scripts/gpu/score_neural.sh triggermap-neural-results.tgz   # back here: reports/neural/
uv run triggermap experiment --config configs/experiments/deberta.toml --dry-run      # planned runs
uv run triggermap predict --model transformer --model-dir artifacts/experiments/<run> --out preds.jsonl
```

Each run records the pinned base-checkpoint revision, the training-data and split hashes,
hyperparameters, seed, per-epoch dev metrics, training time and peak GPU memory (and logs
them to MLflow). Reports carry leakage-group bootstrap intervals and mean ± SD across seeds.

**Run the review application** (FastAPI + SQLite):

```bash
uv sync --extra serve
uv run triggermap app sync                    # load the advisory snapshot (6,350 advisories)
uv run triggermap app create-user alice       # prints an API token once
uv run triggermap app run                     # http://127.0.0.1:8000 (--port to change)
```

Look up an advisory by GHSA, CVE or PYSEC id, paste advisory text, or upload an OSV-Scanner
JSON report. The same features are available as a JSON API: `POST /v1/extractions`,
`POST /v1/imports/osv`, `POST /v1/reviews` (bearer token and `Idempotency-Key`), plus
`/healthz`, `/readyz` and `/metrics`. Interactive API docs are served at `/docs`.

**Annotate** with [Label Studio](https://labelstud.io/):

```bash
uv run triggermap corpus sample-pilot      # reproduce the pilot sample (seed 20261020)
uv run triggermap annotate tasks           # Label Studio tasks for the sample
uv run triggermap annotate import data/label_studio/export.json --annotator A1   # rewrites pilot-1 (labels identical; schema version updated)
uv run triggermap annotate gate --gold annotations/pilot/pilot-2.jsonl --export data/label_studio/export.json   # docs/pilot_gate.md
```

The importer validates every exported annotation (offsets, labels, groups, document status),
records its origin (manual, or a model draft accepted or edited), writes only clean records, and
reports problems, label counts, origins and annotation pace. The procedure
is in [`docs/pilot_protocol.md`](pilot_protocol.md), and the labelling rules are in
[`docs/annotation_guidelines.md`](annotation_guidelines.md). The gate projects each role
and group operator to 800 documents from the non-test pilot records and marks classes below 50
as unsupported.
