# CPU inference benchmark: target host, CRF v0.1.0

- Measured 2026-11-09T03:34:45+00:00 at commit `55e1778`
- Hardware: Intel(R) Xeon(R) Platinum 8488C (x86_64), 2 CPUs, 3.72 GB, Linux, Python 3.12.16
- **This is the documented target host**: targets are judged below.
- Workload `workload-v1`: train and dev pools of splits/pool-v1.json; lengths in `distilbert/distilbert-base-cased` subword tokens. Natural-sample distribution: max 5772, p10 59, p50 234, p90 1775, p99 3112
- AWS EC2, 2 vCPU / 4 GiB x86-64 (Intel Xeon Platinum 8488C), Ubuntu 24.04, measured 2026-11-09.
- Model: released v0.1.0 bundle crf-batches-01-02 (SHA-256 65677a74…d29a), in process.
- Load test: the Docker Compose stack of release v0.1.0 (image sha256:0b9e2f30…adac), client on the same host against the app's loopback port, so the client shares the 2 vCPUs.

## Warm latency, memory and throughput (in process, one request at a time)

| Configuration | Model | p50 ~512 | p95 ~512 | p50 ~2000 | p95 ~2000 | Natural docs/s | Peak RSS (MB) |
|---|---|---:|---:|---:|---:|---:|---:|
| crf | `crf-batches-01-02` | 0.0395 | 0.0617 ✅ | 0.1227 | 0.1446 ✅ | 23.619 ✅ | 276.2 ✅ |
| *Target (documented host)* | | | ≤ 2.5 | | ≤ 8.0 | ≥ 0.25 | ≤ 3072 |

Latencies are seconds per document, including preprocessing, windowing, inference and decoding; p95 over all documents and repeats in the bucket.

## Cold start (fresh process)

| Configuration | Imports (s) | Model load (s) | First extraction (s) | Total (s) |
|---|---:|---:|---:|---:|
| crf | 0.22 | 2.501 | 1.4 | 4.121 |

## HTTP load test

| Service | Requests | Concurrency | Success | p50 (s) | p95 (s) | p99 (s) | Throughput (req/s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| crf | 1000 | 4 | 100.00% | 0.1403 | 0.6144 | 1.0167 | 18.6 |

Target: ≥ 99.5% successful requests at the supported load.
