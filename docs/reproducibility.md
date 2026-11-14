# Reproducibility

The aim: a fresh checkout of the repository, together with the pinned advisory snapshot,
reproduces the committed results within the tolerances declared below.

## Declared tolerances

| What | Tolerance | Verified |
|---|---|---|
| Corpus build (`data/processed/advisories.jsonl`, `data/manifests/snapshot.json`) | byte-identical; corpus SHA-256 `734043ff…b655` | yes, 2026-11-14 |
| Rules (`rules-2`) predictions | byte-identical | yes, 2026-11-14 |
| CRF (`crf-batches-01-02`) retrained from the annotations: bundle files and predictions | byte-identical | yes, 2026-11-14 |
| Evaluation reports built from those predictions (point estimates and bootstrap intervals, seed 0) | byte-identical | yes, 2026-11-14 |
| Transformer predictions from a given bundle, on CPU | identical conditions, confidences to 3 decimal places | yes for the run-2 DeBERTa bundle: 60 of 60 `batch-06` documents (2026-11-14) |
| Transformer **retraining** on a GPU | GPU kernels are not bit-deterministic, so the target is the seed spread. A reproduced run should fall within the reported seed mean ± 2 SD (DeBERTa run 3, `sqrt` 5e-5: 0.197 ± 0.011 held-out typed F1). | no; this is a target, and it needs a GPU run |

The exact tolerances hold for the locked environment (`uv.lock`, Python 3.12), the pinned
snapshot commit and the committed annotations and split manifests. They were verified on macOS
arm64 and on Linux x86-64 (Debian bookworm in Docker). CI runs on Linux but never fetches the
advisory database.

## Fresh-clone check

```bash
bash scripts/reproduce/clean_clone.sh /path/to/empty/dir      # optional: REPO_URL REF
```

The script clones the repository, runs `uv sync --locked --extra baselines`, fetches the advisory
database at `1912cbd6ce9d4cb141636adc4abafb4eb77a93e6` and rebuilds the corpus. It checks the
corpus SHA-256, then regenerates these committed files in place:

- `data/manifests/snapshot.json`;
- the `rules-2` and `crf-batches-01-02` predictions, and the agreement and hand-labelled reports
  in [`reports/agreement/`](../reports/agreement/README.md). The CRF is retrained from
  `pilot-2`, `batch-01` and `batch-02`; nothing is downloaded from a release;
- the drafter-consistency report ([`reports/drafter-consistency/`](../reports/drafter-consistency/README.md));
- the CRF and rules predictions and the two-reference report in
  [`reports/batch-07-comparison/`](../reports/batch-07-comparison/README.md). The committed
  DeBERTa predictions are reused, because no weights are committed.

The check passes only if the clone's `git status` is clean afterwards, which means every
regenerated file is byte-identical to the commit. It needs network access to GitHub and PyPI
and about 1.5 GB of disk. It does not touch the test split.

## Recorded runs

| Date | Commit | Platform | Result | Time |
|---|---|---|---|---:|
| 2026-11-14 | `df1e3a3` | macOS 26 arm64, uv-managed Python 3.12 | reproduced: `git status` clean; retrained CRF bundle digests identical to the v0.1.0 bundle (`tagger.crfsuite` `d1f8cb5a…`, `classifiers.joblib` `e7360d77…`) | 208 s |
| 2026-11-14 | `17922e2` | Linux x86-64: `python:3.12-bookworm` (Python 3.12.16, git 2.39.5) under amd64 emulation, 2 CPUs, 2.5 GB | **not reproduced**: only `data/manifests/snapshot.json` differed (`commit_date` written as `+00:00` instead of `Z`); corpus, predictions and reports identical | 237 s |
| 2026-11-14 | `3e695be` | same Linux container | reproduced after the fix below: `git status` clean (bundle digests not recorded) | 245 s |

**Fixed:** `git log --format=%cI` prints a UTC offset as `Z` in git 2.45 and as `+00:00` in git 2.39,
so the manifest depended on the git version. The commit date is now formatted in UTC from the
commit's Unix timestamp; the committed value did not change.

The Linux runs used:

```bash
docker run --rm --platform linux/amd64 --memory 2500m --cpus 2 \
  -v "$PWD/scripts/reproduce/clean_clone.sh:/opt/clean_clone.sh:ro" python:3.12-bookworm bash -c \
  'pip install --quiet uv==0.12.5 && UV_PYTHON_PREFERENCE=only-system bash /opt/clean_clone.sh /work'
```

Filter counts in every run: 36,910 records scanned, 30,324 excluded as not PyPI, 236 withdrawn,
6,350 kept. These match [`data/manifests/snapshot.json`](../data/manifests/snapshot.json).

## Not covered

- Transformer training (needs a CUDA GPU; see [`training_on_gpu.md`](training_on_gpu.md)).
- Label Studio exports and annotation imports. The exports are not committed, and the imported
  JSONL files are the starting point.
- Benchmarks, which depend on the hardware (see [`benchmarks.md`](benchmarks.md)).
