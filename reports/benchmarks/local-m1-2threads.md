# CPU inference benchmark: Apple M1, 2 inference threads (local proxy)

- Measured 2026-10-21T02:59:31+00:00 at commit `bed2183`
- Hardware: Apple M1 (arm64), 8 CPUs, 8.0 GB, Darwin, Python 3.12.6
- **Local proxy run, not the documented 2 vCPU / 4 GB x86-64 target host.** Numbers indicate relative cost; targets are not judged here.
- Workload `workload-v1`: train and dev pools of splits/pool-v1.json; lengths in `distilbert/distilbert-base-cased` subword tokens. Natural-sample distribution: max 5772, p10 59, p50 234, p90 1775, p99 3112
- Transformer bundles are latency-only: pretrained encoders with untrained heads. Latency and memory do not depend on head weights; accuracy is not measured here.
- In-process on an 8 GB Apple M1 (arm64) with inference limited to 2 threads; the target host is a 2 vCPU / 4 GB x86-64 server, so absolute numbers will differ.
- Load tests: uvicorn with 1 worker; the DeBERTa run allowed 2 concurrent extractions and a 30 s queue timeout. Its 148 failures are the 300-condition safety limit firing on untrained-head output (about 78 spurious spans per document); its 8 failures are overload responses (503 with Retry-After).

## Warm latency, memory and throughput (in process, one request at a time)

| Configuration | Model | p50 ~512 | p95 ~512 | p50 ~2000 | p95 ~2000 | Natural docs/s | Peak RSS (MB) |
|---|---|---:|---:|---:|---:|---:|---:|
| rules | `rules-2` | 0.0029 | 0.0279 | 0.0072 | 0.0379 | 195.214 | 69.1 |
| distilbert-torch-t2-b4 | `distilbert-base-cased-untrained-latency` | 0.1706 | 0.32 | 0.5601 | 0.9152 | 6.008 | 474.5 |
| distilbert-onnx-t2-b1 | `distilbert-base-cased-untrained-latency` | 0.3788 | 0.5198 | 1.5516 | 2.7369 | 2.039 | 536.4 |
| distilbert-onnx-t2-b4 | `distilbert-base-cased-untrained-latency` | 0.6207 | 0.7394 | 1.8062 | 2.5479 | 1.702 | 522.1 |
| distilbert-onnx-t2-b8 | `distilbert-base-cased-untrained-latency` | 0.7909 | 2.5553 | 1.9194 | 2.2902 | 1.745 | 523.8 |
| distilbert-onnx-t1-b4 | `distilbert-base-cased-untrained-latency` | 1.1203 | 1.4394 | 3.1076 | 4.0011 | 1.04 | 420 |
| distilbert-int8-t2-b4 | `distilbert-base-cased-untrained-latency-int8` | 0.2658 | 0.3944 | 0.5787 | 0.7531 | 5.294 | 417.5 |
| deberta-int8-t2-b4 | `deberta-v3-small-untrained-latency-int8` | 0.2587 | 0.5377 | 0.9481 | 1.4051 | 2.864 | 538.4 |
| deberta-onnx-t2-b4 | `deberta-v3-small-untrained-latency` | 0.4649 | 1.1856 | 2.5113 | 3.4969 | 1.387 | 595.9 |
| deberta-torch-t2-b1 | `deberta-v3-small-untrained-latency` | 0.1426 | 0.1951 | 0.6424 | 0.7623 | 4.499 | 700.7 |
| *Target (documented host)* | | | ≤ 2.5 | | ≤ 8.0 | ≥ 0.25 | ≤ 3072 |

Latencies are seconds per document, including preprocessing, windowing, inference and decoding; p95 over all documents and repeats in the bucket.

## Cold start (fresh process)

| Configuration | Imports (s) | Model load (s) | First extraction (s) | Total (s) |
|---|---:|---:|---:|---:|
| rules | 0.59 | 0.017 | 0.049 | 0.656 |
| distilbert-torch-t2-b4 | 5.223 | 14.409 | 0.182 | 19.813 |
| distilbert-onnx-t2-b1 | 0.335 | 6.067 | 0.217 | 6.619 |
| distilbert-onnx-t2-b4 | 0.254 | 6.854 | 0.406 | 7.515 |
| distilbert-onnx-t2-b8 | 0.249 | 5.427 | 0.223 | 5.899 |
| distilbert-onnx-t1-b4 | 0.356 | 6.94 | 0.612 | 7.909 |
| distilbert-int8-t2-b4 | 0.265 | 5.297 | 0.125 | 5.688 |
| deberta-int8-t2-b4 | 0.272 | 7.402 | 0.194 | 7.868 |
| deberta-onnx-t2-b4 | 0.24 | 13.921 | 0.857 | 15.018 |
| deberta-torch-t2-b1 | 2.016 | 11.9 | 0.308 | 14.224 |

## HTTP load test

| Service | Requests | Concurrency | Success | p50 (s) | p95 (s) | p99 (s) | Throughput (req/s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| rules-2 (uvicorn, 1 worker) | 1000 | 4 | 100.00% | 0.0084 | 0.0254 | 0.0371 | 373.08 |
| deberta-v3-small INT8 ONNX, latency-only (uvicorn, 1 worker, 2 concurrent extractions) | 1000 | 4 | 84.40% | 0.3594 | 2.6046 | 6.5876 | 3.6 |

Target: ≥ 99.5% successful requests at the supported load.
