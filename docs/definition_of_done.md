# Definition of Done: final audit (2026-11-15, v0.2.0)

Each item of the project's Definition of Done, with its status and the evidence for it.
✅ done · 🟨 done within a stated limit · ⛔ out of scope (the reason is given).

| # | Item | Status | Evidence |
|---|---|:---:|---|
| 1 | A pinned public-data snapshot can be reconstructed | ✅ | Snapshot commit and output SHA-256 in [`data/manifests/snapshot.json`](../data/manifests/snapshot.json). The fresh-clone check rebuilds it byte for byte on macOS arm64 and Linux x86-64 ([`reproducibility.md`](reproducibility.md)). |
| 2 | Dataset licensing, attribution, filtering and counts are documented | ✅ | [`dataset_card.md`](dataset_card.md) (36,910 scanned → 6,350 PyPI kept, withdrawn and quarantine counts), [`corpus_stats.md`](corpus_stats.md), CC BY 4.0 layering in [`../annotations/README.md`](../annotations/README.md). |
| 3 | Annotation guidelines and quality checks are published | ✅ | [`annotation_guidelines.md`](annotation_guidelines.md) (v0.2 frozen). Deterministic validator and CI checks over every committed record ([`../tests/test_committed_annotations.py`](../tests/test_committed_annotations.py)). Import reports with origin and drift, and drafter consistency ([`../reports/drafter-consistency/`](../reports/drafter-consistency/README.md)). |
| 4 | ≈ 800 advisories labelled, with actual counts and exclusions reported | 🟨 | 710 advisories annotated, plus a second draft of 100. Only **22 are hand-labelled**; the rest are model drafts, by the owner's decision, and no more hand labels will come. Counts by origin and split are in [`dataset_card.md`](dataset_card.md). |
| 5 | Duplicate-, alias- and project-aware split manifests are reproducible | ✅ | [`../splits/pool-v1.json`](../splits/pool-v1.json) (frozen, with SHA-256), [`splits.md`](splits.md), and leakage and assignment tests in [`../tests/test_splits.py`](../tests/test_splits.py). |
| 6 | Rules, traditional supervised and transformer experiments run from scripts | ✅ | `triggermap predict / train / experiment`, [`../configs/experiments/`](../configs/experiments), [`../scripts/gpu/run_neural.sh`](../scripts/gpu/run_neural.sh), `scripts/experiments/*.sh`. |
| 7 | Fine-tuned weights, tokenizer, labels, calibration and provenance are downloadable | ✅ | CRF in releases v0.1.0 and v0.2.0; run-3 DeBERTa in the pre-release `model-deberta-3-run3`. Checksums in the [model card](model_card.md#downloads). |
| 8 | Held-out results include per-class support, uncertainty and difficult slices | 🟨 | Declared test evaluation, run once ([`../reports/test-evaluation/`](../reports/test-evaluation/README.md)): per-role and per-category support, project-group bootstrap intervals, and paired comparisons. It measures **agreement** on 146 model-drafted records; accuracy rests on only 4 hand-labelled records, so the release gates are not judgeable. |
| 9 | Every predicted condition is linked to source evidence | ✅ | Every condition is an exact `[start, end)` span of the canonical text, with an offset map back to the raw text. Every system ends in the deterministic validator ([`model_card.md`](model_card.md)). The API checks each extraction again and returns `invalid_prediction` instead of showing or caching an item without valid evidence (`src/triggermap/serve/app.py`; test `test_invalid_prediction_is_rejected_not_shown`). |
| 10 | Ambiguous structures and unsupported inputs produce visible review states | ✅ | [`../configs/review_policy.yaml`](../configs/review_policy.yaml) routes uncertain, unresolved and unsupported output, and low-confidence items, to *Review required*. "No explicit conditions found" is shown as distinct from "not affected" (the demo's abstention page). |
| 11 | A user can import an advisory, inspect predictions, correct them, record answers and export | ✅ | The review app and API ([`deployment.md`](deployment.md)). `app verify` checks extraction → review → export end to end. |
| 12 | Authenticated saved reviews survive a service restart | ✅ | `test_reviews_survive_restart_and_detect_advisory_change` in `tests/test_app.py`. Reviews kept across the rollback drills. |
| 13 | The API and interface run locally through Docker and on a hosted CPU deployment | ✅ | Local Docker Compose. Hosted on a 2 vCPU / 4 GiB x86-64 AWS EC2 instance on 2026-11-09, with `app verify` passing ([`deployment.md`](deployment.md#hosted-deployment-record)). The instance was temporary, and there is no permanent server. |
| 14 | Load tests, optimization comparisons, monitoring and rollback are demonstrated | 🟨 | CRF on the target host: p95 0.062 s / 0.145 s, 1,000 of 1,000 load-test requests ([`benchmarks.md`](benchmarks.md)). ONNX FP32 is exact; INT8 fails its gate on the trained DeBERTa ([`../reports/onnx-int8/`](../reports/onnx-int8/README.md)). Prometheus metrics, and a rollback drill v0.1.0 → v0.2.0 → v0.1.0. The transformers were not measured on the target host. |
| 15 | A fresh checkout reproduces evaluation within documented tolerances | ✅ | [`reproducibility.md`](reproducibility.md): byte-identical corpus, rules, retrained CRF and reports, on macOS arm64 (208 s) and Linux x86-64 (245 s). |
| 16 | The public demo shows a successful extraction, a difficult linguistic case and a failure or abstention | ✅ | <https://professor3333.github.io/TriggerMap/>: aiohttp, Flask and Django pages, built by `scripts/demo/build_site.sh`. |
| 17 | Resume claims contain measured results only | ✅ | Kept outside the repository. Every figure is taken from the reports linked here, with its caveat (agreement vs accuracy). |

## Roadmap items outside the checklist

| Item | Status | Evidence |
|---|:---:|---|
| Prospective batch | 🟨 | 259 advisories published after the snapshot, behaviour only, with no labels ([`../reports/prospective/`](../reports/prospective/README.md)). |
| Constructed challenge set | ⛔ | Its labels would need human adjudication. Writing them without it would fabricate gold labels, so the set stays empty (`challenge/`). |
| Preliminary usability study | ⛔ | No developer participants are available, now or later. Walkthroughs by AI models are not reported as usability evidence (README, *Limitations*). |
