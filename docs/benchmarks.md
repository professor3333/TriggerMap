# CPU inference benchmarks

How serving cost is measured, and what has been measured so far. Generated reports live in
[`reports/benchmarks/`](../reports/benchmarks/); this page explains them.

## Targets (engineering targets, not results)

For the documented host: **2 vCPU, 4 GB, x86-64 Linux**.

| Metric | Target |
|---|---|
| Warm p95 latency, ~512-token advisory | ≤ 2.5 s |
| Warm p95 latency, ~2,000-token advisory | ≤ 8 s |
| Peak application memory | ≤ 3 GB |
| Sustained throughput, natural workload | ≥ 0.25 documents/s |
| Successful requests over 1,000 at the supported load | ≥ 99.5% |
| Typed-condition F1 lost through optimization (ONNX/INT8) | ≤ 1 point |

A report judges targets (✅/❌) **only when it was measured on the documented host**. Every
other run is labelled a *local proxy*: useful for comparing configurations, not for claims.

## Workload (`reports/benchmarks/workload-v1.json`)

Real advisories from the **train and dev pools only** (no test text), with lengths counted in
`distilbert/distilbert-base-cased` subword tokens so the workload is the same for every model:

| Bucket | Selection | Documents |
|---|---|---:|
| `~512` | 448–576 tokens | 20 |
| `~2000` | 1,750–2,250 tokens | 20 |
| `natural` | uniform sample (throughput, length distribution) | 100 |

The natural sample's length distribution: p10 59, median 234, p90 1,775, p99 3,112, max 5,772
tokens. One advisory in ten is longer than the ~2,000-token target bucket, so long-document
behaviour matters.

## Method

- Each configuration runs **in a fresh process** (`python -m triggermap.bench.worker`), so
  cold start (imports, model load, first extraction) and peak RSS are measured per
  configuration.
- Warm latency is per document and includes preprocessing, windowing, inference and
  decoding, one request at a time. p95 is taken over all documents and repeats in a bucket,
  after one warm-up extraction per bucket.
- Throughput is a sequential pass over the natural sample.
- The HTTP load test (`triggermap bench load`) sends *N* extraction requests at fixed
  concurrency against a running service. Each request's raw text gets a unique HTML comment,
  so the prediction cache always misses while the canonical text, and therefore the work, is
  unchanged.
- Transformer configurations vary the runtime (PyTorch, ONNX Runtime FP32, ONNX Runtime
  dynamic INT8), CPU threads and windows per batch (dynamic padding to the longest window in
  the batch).

## ONNX and INT8

`triggermap export onnx --bundle B --out O --int8 O8` exports the encoder and BIO head to
ONNX (dynamic batch and sequence axes, eager attention for a clean trace) and writes a
dynamically quantized INT8 copy. The small category, role and group heads run in NumPy in
both runtimes, so PyTorch and ONNX share one decoding path, and an ONNX serving image needs no
PyTorch.

Parity measured on the real pretrained backbones over 18 workload advisories, including
three of about 2,000 tokens:

| Backbone | FP32 max logit difference | FP32 identical predictions | INT8 max logit difference |
|---|---:|---:|---:|
| DistilBERT (cased) | 3.0e-6 | 18/18 | 0.36 |
| DeBERTa-v3-small | 5.4e-6 | 18/18 | 1.54 |

FP32 ONNX is numerically exact. INT8 moves the logits, and DeBERTa much more than
DistilBERT. With untrained heads the INT8 *predictions* are not meaningful, so whether INT8
is usable is decided only by the ≤ 1-point typed-F1 gate on a trained model.

## Results so far: local proxy (Apple M1, 2 inference threads)

Full tables: [`reports/benchmarks/local-m1-2threads.md`](../reports/benchmarks/local-m1-2threads.md)
(raw JSON next to it). Measured on 2026-10-21, in process on an 8 GB Apple M1 with inference
limited to 2 threads. **This is not the target host. The transformer bundles have untrained
heads**, so latency and memory are real but accuracy is not measured.

| Configuration | p95 ~512 (s) | p95 ~2000 (s) | Natural docs/s | Peak RSS (MB) | Cold start (s) |
|---|---:|---:|---:|---:|---:|
| rules-2 | 0.03 | 0.04 | 195 | 69 | 0.7 |
| DistilBERT, PyTorch, batch 4 | 0.32 | 0.92 | 6.0 | 475 | 19.8 |
| DistilBERT, ONNX FP32, batch 4 | 0.74 | 2.55 | 1.7 | 522 | 7.5 |
| DistilBERT, ONNX INT8, batch 4 | 0.39 | 0.75 | 5.3 | 418 | 5.7 |
| DeBERTa-v3-small, PyTorch, batch 1 | 0.20 | 0.76 | 4.5 | 701 | 14.2 |
| DeBERTa-v3-small, ONNX FP32, batch 4 | 1.19 | 3.50 | 1.4 | 596 | 15.0 |
| DeBERTa-v3-small, ONNX INT8, batch 4 | 0.54 | 1.41 | 2.9 | 538 | 7.9 |

What this does and does not show:

- Every configuration is far inside the latency and memory targets **on this machine**. On
  the target x86 host they still have to be measured: absolute numbers will differ.
- **On Apple Silicon, PyTorch beats ONNX Runtime FP32.** PyTorch uses Apple's optimized math
  libraries, while ONNX Runtime's ARM FP32 kernels are slower. On x86, ONNX Runtime is
  usually faster. The runtime choice must therefore be made on the target host, not here.
- INT8 roughly halves FP32 ONNX latency and memory, but it is only usable if a trained model
  stays within 1 point of typed F1 (see the parity table above: DeBERTa's logits move more).
- ONNX Runtime cold starts are 3 to 4 times faster than PyTorch's (no PyTorch import), which
  matters for restarts and rollbacks.
- Batch size (windows per forward pass) had a small and inconsistent effect at this scale.
  Most advisories fit in one window, so there is little to batch.
- Repeated runs on a shared laptop vary by up to about 3×. Treat differences under that as
  noise.

HTTP load test, 1,000 requests at concurrency 4, cache bypassed:

| Service | Success | p50 (s) | p95 (s) | Throughput (req/s) |
|---|---:|---:|---:|---:|
| rules-2 | 100.0% | 0.008 | 0.025 | 373 |
| DeBERTa-v3-small INT8 ONNX, latency-only | 84.4% | 0.36 | 2.60 | 3.6 |

The rules service meets the ≥ 99.5% target. The transformer service result is **not a
pass** and **not representative**:

- 148 failures are the service's 300-condition safety limit rejecting untrained-head output
  (about 78 spurious spans per document);
- 8 failures are `overloaded` responses: with 2 extraction slots and 4 concurrent clients,
  long advisories waited longer than the 30-second queue timeout. That is the overload
  protection working as designed (503 with `Retry-After`, no unbounded queue), and it shows
  that a transformer deployment needs a declared supported concurrency.

It will be repeated with a trained model on the target host.

## Lessons from running the benchmarks

- An earlier attempt ran the matrix in a 4 GB Docker container on this 8 GB laptop, alongside
  other running containers. The host swapped heavily (about 15 GB of swap in use), the Docker
  engine stopped responding, and the run was discarded: swapped timings measure the disk,
  not the model. Runs are now **checkpointed and resumable**
  (`reports/benchmarks/*.partial.jsonl`), so an interruption loses no finished
  configuration.
- On a small machine, run heavy configurations alone and watch swap. On the target host,
  run the matrix inside the 2 vCPU / 4 GB VM itself.

## Reproduce

```bash
uv sync --extra neural --extra onnx --extra export
uv run triggermap bench workload                                   # reports/benchmarks/workload-v1.json
uv run triggermap bench latency-bundle --base microsoft/deberta-v3-small \
    --revision a36c739020e01763fe789b4b85e2df55d6180012 --out artifacts/latency/deberta
uv run triggermap export onnx --bundle artifacts/latency/deberta \
    --out artifacts/latency/deberta-onnx --int8 artifacts/latency/deberta-int8
uv run triggermap bench run --repeats 2 \
    --config kind=onnx,dir=artifacts/latency/deberta-int8,threads=2,batch=4 \
    --out reports/benchmarks/<host>.md
uv run triggermap bench load --url http://127.0.0.1:8000 --requests 1000 --concurrency 4 \
    --out reports/benchmarks/load-<host>.json
```

Latency-only bundles are refused by `triggermap release create`, so they can never be
deployed.
