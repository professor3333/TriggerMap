# Neural run 1 (2026-11-05): failed configuration

The first GPU run of `scripts/gpu/run_neural.sh` (Kaggle, one Tesla T4, torch 2.14.1+cu130):
the `distilbert-1` and `deberta-1` grids, 2 learning rates × 3 seeds, up to 6 epochs, patience
2, inverse-frequency (balanced) class weights on the span tags. Training used the train split
of `pilot-2`, `batch-01` and `batch-02` (239 documents). Early stopping used only the
model-drafted dev batches `batch-03` and `batch-06`. The test split was not touched.

**Result: every run over-predicts spans.** Typed F1 against the 172 model-drafted dev records
is at most 0.023, against 0.145 for `crf-batches-01-02` on the same records. The runs predict
39–47 conditions per document (the CRF predicts 1.8), mostly short fragments (median 8–9
characters).

| Run | Best epoch | Dev typed F1 (agreement) | Span precision, last epoch | Span recall, last epoch | Seconds | Peak GPU MB |
|---|---:|---:|---:|---:|---:|---:|
| `deberta-1-base-learning_rate2e-05-seed0` | 6 | 0.006 | 0.005 | 0.122 | 115 | 4787 |
| `deberta-1-base-learning_rate2e-05-seed1` | 6 | 0.006 | 0.005 | 0.127 | 113 | 5340 |
| `deberta-1-base-learning_rate2e-05-seed2` | 6 | 0.008 | 0.007 | 0.168 | 112 | 5341 |
| `deberta-1-base-learning_rate5e-05-seed0` | 6 | 0.020 | 0.015 | 0.228 | 110 | 5334 |
| `deberta-1-base-learning_rate5e-05-seed1` | 6 | 0.023 | 0.018 | 0.264 | 110 | 5343 |
| `deberta-1-base-learning_rate5e-05-seed2` | 6 | 0.020 | 0.016 | 0.244 | 109 | 5344 |
| `distilbert-1-base-learning_rate2e-05-seed0` | 5 | 0.007 | 0.005 | 0.130 | 61 | 1956 |
| `distilbert-1-base-learning_rate2e-05-seed1` | 5 | 0.007 | 0.005 | 0.130 | 64 | 2202 |
| `distilbert-1-base-learning_rate2e-05-seed2` | 6 | 0.006 | 0.005 | 0.132 | 69 | 2204 |
| `distilbert-1-base-learning_rate5e-05-seed0` | 6 | 0.019 | 0.013 | 0.215 | 62 | 2221 |
| `distilbert-1-base-learning_rate5e-05-seed1` | 6 | 0.018 | 0.014 | 0.231 | 63 | 2210 |
| `distilbert-1-base-learning_rate5e-05-seed2` | 6 | 0.019 | 0.014 | 0.238 | 64 | 2205 |

Paired comparisons of each grid's best run (by early-stopping score) against
`crf-batches-01-02`:

| Comparison | Slice | Typed F1, B − A | False-prerequisite rate, B − A |
|---|---|---:|---:|
| CRF → `deberta-1-…5e-05-seed1` | agreement (172) | **−0.122 [−0.160, −0.081]** | **+0.486 [+0.420, +0.574]** |
| CRF → `distilbert-1-…5e-05-seed2` | agreement (172) | **−0.126 [−0.165, −0.084]** | **+0.492 [+0.431, +0.579]** |
| CRF → `deberta-1-…5e-05-seed1` | hand-labelled (10) | −0.324 [−0.587, +0.032] | +0.514 [−0.141, +0.849] |
| CRF → `distilbert-1-…5e-05-seed2` | hand-labelled (10) | −0.344 [−0.625, +0.023] | +0.546 [−0.087, +0.875] |

Bold marks a clear difference. Full reports are in this directory.

## Diagnosis

- **Span-tag weighting.** About 95% of training tokens are tagged `O`. Balanced
  (inverse-frequency) weights then make a missed `B` about 65 times as costly as a wrong one,
  so the tagger marks any token with a small chance of starting a condition. High recall with
  precision near 0.01 is the expected symptom.
- **Too few updates.** 493–543 training windows at an effective batch of 16 give about 31
  optimizer steps per epoch. Most runs were still improving at their last epoch (best epoch 6
  of 6), and 5e-5 beat 2e-5 in every pair.

## Change for run 2

- `TrainConfig.bio_weighting`: `inverse` (run 1), `sqrt` (default) or `none`. Both new values
  are in the grid.
- Up to 15 epochs with patience 3.
- New run names (`distilbert-2`, `deberta-2`), so resumed runs never reuse run-1 bundles.

## Provenance

- Results archive: `triggermap-neural-results.tgz`, SHA-256
  `9bf7cf81442d9fc353f4f8ea374f49cd53ad638f8649b2a1f65024ec81130915`.
- Per-run `metadata.json` (configuration, base revision, training hash and origins, per-epoch
  losses and dev scores) is in `metadata/`. The predictions (24 MB) and the bundles are not
  committed.
