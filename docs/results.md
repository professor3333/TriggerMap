# Results

Every number here is measured. Scores against model-drafted records measure **agreement with
the drafting model, not accuracy**; only the hand-labelled records (22 in total: 10 in dev, 4 in
test) measure accuracy. Intervals are 95% project-group bootstrap intervals (1,000 resamples).
Metric definitions are in [`evaluation.md`](evaluation.md), release targets in
[`targets.md`](targets.md), and the known limits in the README's *Limitations* section.

**Contents:** [Held-out test](#held-out-test-results-declared-release-evaluation-2026-11-15) ·
[Development results](#development-results) · [Serving cost](#serving-cost)

## Held-out test results (declared release evaluation, 2026-11-15)

Run once, on the owner's declaration, on the locked test split (newest project groups, so it
measures temporal and project shift). It is logged in [`docs/test-access-log.md`](test-access-log.md).
The 146 model-drafted test records measure **agreement with the drafting model, not accuracy**.
95% project-group bootstrap intervals.

| Test split, 146 model-drafted records | Typed-condition micro-F1 | Exact span precision | Exact span recall | False-prerequisite rate | Reversed-meaning rate |
|---|---:|---:|---:|---:|---:|
| Rules (`rules-2`) | 0.048 [0.021, 0.082] | 0.101 | 0.053 | 0.646 | 0.043 |
| CRF (`crf-batches-01-02`, default) | **0.193 [0.154, 0.238]** | **0.263** | 0.219 | **0.482** | 0.037 |
| DeBERTa-v3-small (run 3) | 0.154 [0.125, 0.186] | 0.114 | **0.393** | 0.650 | **0.005** |

The CRF agrees with the drafts better than DeBERTa (−0.039 typed F1 for DeBERTa, 95% CI
[−0.080, −0.000], clear but only just). It is clearly more precise and invents clearly fewer
prerequisites. DeBERTa has clearly higher recall and clearly fewer reversed meanings. It predicts
8.4 conditions per document where the test drafts mark 2.4. Its dev lead did not transfer. On the
4 hand-labelled test records (7 conditions), typed F1 is 0.125 (CRF), 0.133 (DeBERTa) and 0.167
(rules), and no difference is clear. The release gates in [`docs/targets.md`](targets.md)
are judged on hand-labelled test records only, so they **cannot be judged** with 4. Full report,
with per-class support: [`reports/test-evaluation/`](../reports/test-evaluation/README.md).

**Prospective check (259 advisories published after the snapshot, behaviour only).** These
have no labels, so there is no accuracy or agreement. The input has shifted: new advisories
have a median of 515 words (dev: 79). 71% need more than one 512-token transformer window
(dev: 13%), and median length in the corpus has risen steadily through 2026. On them the CRF
suggests 4.4 conditions per advisory (dev: 1.1) and reports "no explicit conditions found"
for 7.7% (dev: 43.8%). NOT_REQUIRED, EXCEPTION and negation-flagged items are more common, which
is where both models are weakest. See [`reports/prospective/`](../reports/prospective/README.md).

## Development results

### Preliminary pilot results (hand-labelled dev documents)

Measured on the **10 hand-labelled pilot documents in the dev split** (17 gold conditions,
`pilot-2`). These are early, small-sample baselines, not final results: the intervals are wide,
the CRF was trained on only 39 pilot documents (32 of them from model drafts), and they were
measured before the test split was evaluated.

| System | Typed-condition micro-F1 | Exact span F1 | False-prerequisite rate |
|---|---:|---:|---:|
| Rules (`rules-2`) | 0.095 [0.000, 0.333] | 0.095 [0.000, 0.333] | 0.750 [0.000, 1.000] |
| CRF (`crf-pilot-2`, pilot train split) | 0.231 [0.062, 0.417] | 0.231 [0.062, 0.417] | 0.444 [0.000, 0.667] |
| CRF (`crf-pilot-2-batch-01`, + 100 model-drafted `batch-01` records) | 0.444 [0.133, 0.667] | 0.444 [0.133, 0.667] | 0.300 [0.000, 0.750] |

**Label source.** Every annotation batch after the pilot (710 advisories annotated, 22 by hand)
was submitted from model drafts, by the owner's decision. Accuracy is therefore measured only on
the 10 hand-labelled dev documents above. Later results are reported as *agreement with the
drafting model*, never as accuracy, and the release gates in [`docs/targets.md`](targets.md)
cannot be judged as declared.

| Agreement with model drafts (172 dev records, not accuracy) | Typed-condition micro-F1 | Exact span F1 | False-prerequisite rate |
|---|---:|---:|---:|
| Rules (`rules-2`) | 0.107 [0.058, 0.154] | 0.142 [0.085, 0.195] | 0.330 [0.165, 0.467] |
| CRF (`crf-pilot-2-batch-01`) | 0.128 [0.095, 0.168] | 0.174 [0.134, 0.215] | 0.416 [0.294, 0.493] |
| CRF (`crf-batches-01-02`, + 100 model-drafted `batch-02` records) | 0.145 [0.105, 0.185] | 0.221 [0.171, 0.268] | 0.353 [0.260, 0.416] |

Adding `batch-02` clearly improves exact-span agreement (+0.047, 95% CI [+0.004, +0.086]), but not
typed agreement. On the 10 hand-labelled documents, `crf-batches-01-02` scores 0.370 typed F1
[0.000, 0.640], and the difference from `crf-pilot-2-batch-01` is not clear; see
[`reports/agreement/`](../reports/agreement/README.md). Its disagreements with the drafts, by error
type, are in [`docs/error_catalogue.md`](error_catalogue.md). The drafts themselves are
unstable: two
model drafting runs of the 100 `batch-07` documents agree with each other at only 0.375 typed F1
[0.309, 0.444] (0.431 span F1), so low agreement scores partly reflect noisy reference labels; see
[`reports/drafter-consistency/`](../reports/drafter-consistency/README.md).

**Two references (batch-07, 100 dev documents, agreement only).** Scored against both drafts,
the CRF beats `rules-2` clearly under each one (typed F1 +0.099 and +0.082). The run-3 DeBERTa
candidate leads the CRF under both drafts (+0.028, not clear; +0.109, clear). It finds 0.426 of the
94 conditions both drafts agree on (CRF 0.181), and its invented-prerequisite rate against both
drafts is not clearly different (0.327 against 0.380). The pre-set switching rule needs a clear gain
in precision or invention, so the CRF stays the default. A run-3-recipe bundle without the group
objective gives nearly the same result; DeBERTa run 2 changes direction between the drafts and
invents clearly more (0.504). See
[`reports/batch-07-comparison/`](../reports/batch-07-comparison/README.md).

**Transformers.** DistilBERT and DeBERTa-v3-small were fine-tuned on one T4 GPU with the same
training data. Early stopping and the choice of each grid's best run (of 12) used only a
selection half of these model-drafted dev records. The comparison below is on the other,
held-out half (61 documents in 46 project groups, `splits/selection-v1/`):

| Agreement, held-out half (61 dev records, not accuracy) | Typed-condition micro-F1 | Exact span F1 | False-prerequisite rate |
|---|---:|---:|---:|
| CRF (`crf-batches-01-02`) | 0.127 [0.054, 0.201] | 0.176 [0.100, 0.261] | 0.412 [0.288, 0.538] |
| DistilBERT (`distilbert-3`) | 0.099 [0.064, 0.142] | 0.118 [0.074, 0.177] | 0.463 [0.375, 0.545] |
| DeBERTa-v3-small (`deberta-3`) | 0.185 [0.145, 0.235] | 0.221 [0.174, 0.277] | 0.483 [0.418, 0.544] |

DeBERTa leads the CRF on typed agreement, but not clearly (+0.058, 95% CI [−0.008, +0.134]).
Its false-prerequisite rate is not clearly different (+0.072 [−0.070, +0.196]). On the 10
hand-labelled documents no difference is clear. See [`reports/neural/run-3/`](../reports/neural/run-3/README.md);
earlier runs are in [`run-2/`](../reports/neural/run-2/README.md) and the failed first
configuration in [`run-1/`](../reports/neural/run-1/README.md).

**Calibration and review thresholds.** Platt scaling fitted on the selection half cuts the
held-out calibration error from 0.305 to 0.101 (CRF) and from 0.548 to 0.059 (DeBERTa). With
review thresholds chosen on the selection half for the same target precision, DeBERTa keeps two
to three times as many agreeing conditions. Its held-out typed F1 is clearly higher at targets
0.30 and 0.35 (+0.100 [+0.034, +0.172] and +0.100 [+0.024, +0.171]), but its precision is not
clearly different, and its false-prerequisite rate is higher at every target (not clearly).
The CRF therefore stays the default model; see [`reports/calibration/`](../reports/calibration/README.md).

**Ablations and learning curve (CRF).** On the 172 agreement records, removing the heading/list
context features (−0.006 typed F1 [−0.027, +0.020]) or the part-of-speech features (+0.002
[−0.025, +0.032]) makes no clear difference. Typed agreement rises from 0.054 with 30 training
documents to 0.143 with 120, then stays flat (0.145 with all 239); span agreement keeps rising
slowly. See [`reports/crf-ablations/`](../reports/crf-ablations/README.md).

**Ablations and learning curve (DeBERTa, held-out half, three seeds each).** DeBERTa needs far
more data than the CRF: typed agreement is 0.075 with 60 training documents, 0.097 with 120 and
0.197 with all 239, and every reduced-data seed is clearly worse than the full model. Removing
heading/list context or the group objective makes no clear difference to held-out typed
agreement. Without context, the false-prerequisite rate is higher for all three seeds, and
hand-labelled typed F1 is lower for all three (clear for one seed each). See
[`reports/neural/ablation-1/`](../reports/neural/ablation-1/README.md).

95% project-group bootstrap intervals (1,000 resamples). Full reports, including scores against
the 28 model-made dev records (which measure agreement with the drafting model, not accuracy),
are in [`reports/pilot/`](../reports/pilot/README.md). The paired difference from adding `batch-01` (+0.214 typed F1,
95% CI [−0.026, +0.457]) is not clear; see [`reports/training-origin/`](../reports/training-origin/README.md). Release targets, declared before any test
result, are in [`docs/targets.md`](targets.md).

## Serving cost

**On the target host (2 vCPU / 4 GB x86-64, AWS EC2, 2026-11-09)**, the released CRF
(`crf-batches-01-02`, v0.1.0) meets every serving target:

| Measure | CRF v0.1.0 | Target |
|---|---:|---:|
| Warm p95 latency, ~512-token advisory | 0.06 s | ≤ 2.5 s |
| Warm p95 latency, ~2,000-token advisory | 0.14 s | ≤ 8 s |
| Throughput, natural workload (in process) | 23.6 docs/s | ≥ 0.25 docs/s |
| Peak memory (in process) | 276 MB | ≤ 3 GB |
| HTTP load test, 1,000 requests at concurrency 4 (Compose stack) | 100% succeeded, p95 0.61 s, 18.6 req/s | ≥ 99.5% |

Full report: [`reports/benchmarks/target-host-crf.md`](../reports/benchmarks/target-host-crf.md).
The transformer models have not been measured on this host.

**Local proxy for the transformers.** Measured on an 8 GB Apple M1 with inference limited to 2 threads. This is **not the target
host**, and the transformer bundles have untrained heads, so latency and memory are real but
accuracy is not measured. Details and caveats: [`docs/benchmarks.md`](benchmarks.md).

| Configuration | p95, ~512 tokens | p95, ~2,000 tokens | Peak memory |
|---|---:|---:|---:|
| rules-2 | 0.03 s | 0.04 s | 69 MB |
| DistilBERT, PyTorch | 0.32 s | 0.92 s | 475 MB |
| DeBERTa-v3-small, PyTorch | 0.20 s | 0.76 s | 701 MB |
| DeBERTa-v3-small, ONNX INT8 (fails the accuracy gate, see below) | 0.54 s | 1.41 s | 538 MB |

ONNX export is numerically exact against PyTorch (maximum logit difference ≈ 5 × 10⁻⁶). On the
trained run-3 DeBERTa, FP32 ONNX reproduces PyTorch on all 372 dev documents, but dynamic INT8
fails the ≤ 1-point typed-F1 gate: −2.1 points on the hand-labelled dev documents, −7.4 points of
agreement on 172 dev records, and only 51 of 372 documents unchanged
([`reports/onnx-int8/`](../reports/onnx-int8/README.md)). The
rules service handled 1,000 of 1,000 load-test requests. The plan's targets (p95 ≤ 2.5 s and
≤ 8 s, ≤ 3 GB) will be judged only on the documented 2 vCPU / 4 GB x86-64 host.
