# Neural run 2 (2026-11-06)

The second GPU run of `scripts/gpu/run_neural.sh`, a Kaggle background version on one Tesla T4.
It covers the `distilbert-2` and `deberta-2` grids:
- two span-tag weightings (`sqrt`, `none`) × two learning rates (2e-5, 5e-5) × three seeds, 24
  runs;
- up to 15 epochs, with patience 3.

The other settings match run 1 ([`../run-1/`](../run-1/README.md)):
- **Training:** the train split of `pilot-2`, `batch-01` and `batch-02` (239 documents: 7
  `manual`, 232 model drafts).
- **Early stopping and run selection:** only the model-drafted dev batches `batch-03` and
  `batch-06`.
- **Untouched:** the 10 hand-labelled dev documents had no part in selection, and the test
  split was not touched.

All scores against model drafts measure **agreement with the drafting model, not accuracy**.

## All runs (agreement with 172 model-drafted dev records, at the selected epoch)

| Run | Best / last epoch | Typed F1 | Span precision | Span recall | False-prerequisite rate | Conditions per document | Seconds |
|---|---:|---:|---:|---:|---:|---:|---:|
| `deberta-2-base-bio_weightingnone-learning_rate2e-05-seed0` | 1/4 | 0.000 | 0.000 | 0.000 | 0.955 | 0.9 | 69 |
| `deberta-2-base-bio_weightingnone-learning_rate2e-05-seed1` | 1/4 | 0.000 | 0.000 | 0.000 | 0.937 | 8.6 | 69 |
| `deberta-2-base-bio_weightingnone-learning_rate2e-05-seed2` | 1/4 | 0.000 | 0.000 | 0.000 | 0.959 | 4.7 | 68 |
| `deberta-2-base-bio_weightingnone-learning_rate5e-05-seed0` | 1/4 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 68 |
| `deberta-2-base-bio_weightingnone-learning_rate5e-05-seed1` | 1/4 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 68 |
| `deberta-2-base-bio_weightingnone-learning_rate5e-05-seed2` | 1/4 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 68 |
| `deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed0` | 15/15 | 0.072 | 0.055 | 0.238 | 0.660 | 11.5 | 267 |
| `deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed1` | 15/15 | 0.077 | 0.062 | 0.244 | 0.658 | 10.9 | 265 |
| `deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed2` | 11/14 | 0.070 | 0.054 | 0.269 | 0.701 | 13.4 | 246 |
| `deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0` | 9/12 | **0.133** | 0.108 | 0.355 | 0.607 | 8.8 | 210 |
| `deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed1` | 15/15 | 0.132 | 0.108 | 0.319 | 0.596 | 7.7 | 263 |
| `deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed2` | 9/12 | 0.130 | 0.100 | 0.319 | 0.577 | 8.4 | 210 |
| `distilbert-2-base-bio_weightingnone-learning_rate2e-05-seed0` | 1/4 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 39 |
| `distilbert-2-base-bio_weightingnone-learning_rate2e-05-seed1` | 1/4 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 39 |
| `distilbert-2-base-bio_weightingnone-learning_rate2e-05-seed2` | 1/4 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 39 |
| `distilbert-2-base-bio_weightingnone-learning_rate5e-05-seed0` | 1/4 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 39 |
| `distilbert-2-base-bio_weightingnone-learning_rate5e-05-seed1` | 14/15 | 0.064 | 0.073 | 0.104 | 0.510 | 4.1 | 146 |
| `distilbert-2-base-bio_weightingnone-learning_rate5e-05-seed2` | 1/4 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 39 |
| `distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed0` | 8/11 | 0.039 | 0.034 | 0.168 | 0.724 | 13.2 | 101 |
| `distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed1` | 12/15 | 0.042 | 0.037 | 0.137 | 0.662 | 10.3 | 147 |
| `distilbert-2-base-bio_weightingsqrt-learning_rate2e-05-seed2` | 14/15 | 0.033 | 0.027 | 0.111 | 0.667 | 11.1 | 147 |
| `distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed0` | 13/15 | 0.074 | 0.069 | 0.184 | 0.554 | 7.3 | 147 |
| `distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed1` | 4/7 | 0.041 | 0.030 | 0.194 | 0.770 | 17.7 | 69 |
| `distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed2` | 15/15 | **0.075** | 0.072 | 0.171 | 0.541 | 6.9 | 148 |

Typed F1 across seeds (mean ± SD):

| Grid cell | 2e-5 | 5e-5 |
|---|---:|---:|
| DeBERTa, `sqrt` | 0.073 ± 0.004 | **0.131 ± 0.001** |
| DeBERTa, `none` | 0.000 ± 0.000 | 0.000 ± 0.000 |
| DistilBERT, `sqrt` | 0.038 ± 0.004 | 0.063 ± 0.019 |
| DistilBERT, `none` | 0.000 ± 0.000 | 0.021 ± 0.037 |

For reference, `crf-batches-01-02` scores 0.145 typed F1 on the same records
([`../../agreement/`](../../agreement/README.md)).

## Best run of each grid against the CRF

Paired project-group bootstrap, 1,000 resamples, B − A with A = `crf-batches-01-02`.

| B | Slice | Typed F1 | Exact span precision | False-prerequisite rate (lower is better) |
|---|---|---:|---:|---:|
| `deberta-2-…sqrt…5e-05-seed0` | agreement (172) | −0.013 [−0.063, +0.043] | **−0.224 [−0.288, −0.163]** | **+0.254 [+0.188, +0.343]** |
| `distilbert-2-…sqrt…5e-05-seed2` | agreement (172) | **−0.070 [−0.113, −0.020]** | **−0.260 [−0.320, −0.202]** | **+0.187 [+0.124, +0.252]** |
| `deberta-2-…sqrt…5e-05-seed0` | hand-labelled (10) | −0.106 [−0.313, +0.194] | −0.304 [−0.525, +0.150] | +0.350 [−0.233, +0.690] |
| `distilbert-2-…sqrt…5e-05-seed2` | hand-labelled (10) | −0.178 [−0.316, +0.040] | −0.357 [−0.583, +0.026] | +0.258 [−0.194, +0.500] |

Bold marks a clear difference. Full reports: `compare_*.md`, and `<run>_dev_agreement.md` /
`<run>_dev_manual.md` for every run.

## Reading

The transformer numbers are **optimistic**: early stopping and the choice of the best run used
these same 172 records, while the CRF was not tuned on them. A difference in the CRF's favour
is therefore conservative. A difference in a transformer's favour would need a separate
held-out slice.

- **The softer weighting fixed most of run 1's failure.** The best DeBERTa typed F1 rose from
  0.023 to 0.133, and all three DeBERTa `sqrt` 5e-5 seeds agree within 0.003.
- **DeBERTa is not clearly different from the CRF on typed agreement** (−0.013, interval
  across zero). It is clearly worse on precision and on the false-prerequisite rate: it still
  predicts about 8 conditions per document against 1.8 for the CRF, so it invents
  prerequisites more often. On the error that matters most, the CRF remains the better
  system.
- **DistilBERT is clearly worse than the CRF** on typed agreement (−0.070).
- **Uniform weights (`none`) were cut off by early stopping, not tested.** These runs predict
  no spans after epoch 1, score 0.000, and patience 3 stops them at epoch 4 before they can
  start tagging. The one that survived (DistilBERT, 5e-5, seed 1) climbed to 0.064 by epoch
  14. Run 3 needs a minimum number of epochs before patience applies.
- **Several runs were still improving at their last epoch** (best epoch 15 of 15).
- **On the 10 hand-labelled documents nothing is clear**, as with every other comparison on
  that slice.

## Provenance

- Results archive SHA-256 `7b760c8b52e7f5f69cd50a4f76ee9fee8b9ed540c78bc15a06f238941ba8aa85`.
- Bundles archive (best run of each grid, weights not committed): 661,598,084 bytes.
- Committed:
  - per-run `metadata.json` in `metadata/` (configuration, base revision, training hash and
    origins, span-tag weights, per-epoch losses and dev scores, peak GPU memory);
  - the predictions of the two best runs in `predictions/`.

To reproduce the comparisons from the committed predictions:

```bash
uv run triggermap compare annotations/batches/batch-03.jsonl reports/agreement/predictions/crf-batches-01-02.jsonl \
    reports/neural/run-2/predictions/deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0.jsonl \
    --add-gold annotations/batches/batch-06.jsonl --split dev
```
