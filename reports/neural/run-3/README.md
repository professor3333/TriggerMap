# Neural run 3 (2026-11-06)

The third GPU run of `scripts/gpu/run_neural.sh`, a Kaggle background version on one Tesla T4.
It covers the `distilbert-3` and `deberta-3` grids:
- span-tag weighting {`sqrt`, `none`} × learning rate {2e-5, 5e-5} × 3 seeds, 24 runs;
- up to 20 epochs, patience 3, and no early stop before epoch 6 (`min_epochs`).

Training data matches runs 1 and 2: the train split of `pilot-2`, `batch-01` and `batch-02` (239
documents: 7 `manual`, 232 model drafts).

**New in this run: selection and comparison use different documents.** The 172 model-drafted dev
records (`batch-03` + `batch-06`) were split once by leakage group (`splits/selection-v1/`):
- **Selection half:** 111 documents in 46 groups. It drove early stopping and the choice of
  each grid's best run.
- **Held-out half:** 61 documents in 46 other groups, used only for the comparisons below.

The 10 hand-labelled dev documents and the test split were not used for selection.

Every score against model drafts measures **agreement with the drafting model, not accuracy**.

## All runs

Held-out scores are on the 61 held-out documents.

| Run | Best / last epoch | Selection typed F1 | Held-out typed F1 | Held-out span precision | Held-out span recall | Held-out false-prerequisite rate | Conditions per document | Seconds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `deberta-3-base-bio_weightingnone-learning_rate2e-05-seed0` | 1/6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.940 | 7.8 | 88 |
| `deberta-3-base-bio_weightingnone-learning_rate2e-05-seed1` | 1/6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.892 | 22.6 | 88 |
| `deberta-3-base-bio_weightingnone-learning_rate2e-05-seed2` | 1/6 | 0.000 | 0.000 | 0.003 | 0.021 | 0.948 | 22.4 | 88 |
| `deberta-3-base-bio_weightingnone-learning_rate5e-05-seed0` | 16/19 | 0.154 | 0.156 | 0.151 | 0.236 | 0.408 | 4.2 | 282 |
| `deberta-3-base-bio_weightingnone-learning_rate5e-05-seed1` | 20/20 | 0.144 | 0.150 | 0.141 | 0.221 | 0.479 | 4.1 | 296 |
| `deberta-3-base-bio_weightingnone-learning_rate5e-05-seed2` | 15/18 | 0.133 | 0.129 | 0.129 | 0.229 | 0.430 | 4.8 | 266 |
| `deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed0` | 19/20 | 0.107 | 0.105 | 0.083 | 0.321 | 0.613 | 10.4 | 304 |
| `deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed1` | 20/20 | 0.089 | 0.103 | 0.077 | 0.286 | 0.649 | 9.5 | 301 |
| `deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed2` | 20/20 | 0.105 | 0.105 | 0.086 | 0.336 | 0.636 | 10.2 | 302 |
| `deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed0` | 18/20 | 0.167 | 0.207 | 0.178 | 0.386 | 0.431 | 5.3 | 298 |
| `deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed1` | 16/19 | 0.168 | 0.198 | 0.156 | 0.407 | 0.567 | 6.4 | 283 |
| `deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2` | 19/20 | **0.185** | 0.185 | 0.162 | 0.350 | 0.483 | 5.2 | 299 |
| `distilbert-3-base-bio_weightingnone-learning_rate2e-05-seed0` | 1/6 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 49 |
| `distilbert-3-base-bio_weightingnone-learning_rate2e-05-seed1` | 1/6 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.0 | 49 |
| `distilbert-3-base-bio_weightingnone-learning_rate2e-05-seed2` | 1/6 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.0 | 49 |
| `distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed0` | 8/11 | 0.052 | 0.045 | 0.043 | 0.093 | 0.589 | 5.2 | 90 |
| `distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed1` | 12/15 | 0.076 | 0.069 | 0.063 | 0.107 | 0.548 | 4.8 | 122 |
| `distilbert-3-base-bio_weightingnone-learning_rate5e-05-seed2` | 12/15 | 0.053 | 0.056 | 0.056 | 0.086 | 0.478 | 4.0 | 122 |
| `distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed0` | 8/11 | 0.042 | 0.037 | 0.032 | 0.179 | 0.736 | 12.6 | 86 |
| `distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed1` | 10/13 | 0.052 | 0.030 | 0.029 | 0.121 | 0.699 | 10.3 | 106 |
| `distilbert-3-base-bio_weightingsqrt-learning_rate2e-05-seed2` | 8/11 | 0.034 | 0.024 | 0.021 | 0.114 | 0.747 | 12.4 | 90 |
| `distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed0` | 18/20 | **0.096** | 0.099 | 0.088 | 0.179 | 0.463 | 5.2 | 164 |
| `distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed1` | 10/13 | 0.078 | 0.085 | 0.069 | 0.186 | 0.566 | 7.3 | 107 |
| `distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed2` | 15/18 | 0.083 | 0.108 | 0.092 | 0.200 | 0.494 | 5.8 | 148 |

Bold marks each grid's best run on the selection half, the run that is compared below.

Typed F1 across seeds (mean ± SD), selection / held-out:

| Grid cell | 2e-5 | 5e-5 |
|---|---:|---:|
| DeBERTa, `sqrt` | 0.100 ± 0.010 / 0.104 ± 0.001 | **0.173 ± 0.010 / 0.197 ± 0.011** |
| DeBERTa, `none` | 0.000 / 0.000 | 0.143 ± 0.011 / 0.145 ± 0.014 |
| DistilBERT, `sqrt` | 0.042 ± 0.009 / 0.030 ± 0.007 | 0.085 ± 0.009 / 0.097 ± 0.012 |
| DistilBERT, `none` | 0.000 / 0.000 | 0.060 ± 0.013 / 0.057 ± 0.012 |

## Held-out comparison

95% project-group bootstrap intervals, 1,000 resamples.

| System | Typed F1 | Exact span F1 | False-prerequisite rate (lower is better) |
|---|---:|---:|---:|
| CRF `crf-batches-01-02` | 0.127 [0.054, 0.201] | 0.176 [0.100, 0.261] | 0.412 [0.288, 0.538] |
| DeBERTa `deberta-3-…sqrt…5e-05-seed2` | 0.185 [0.145, 0.235] | 0.221 [0.174, 0.277] | 0.483 [0.418, 0.544] |
| DistilBERT `distilbert-3-…sqrt…5e-05-seed0` | 0.099 [0.064, 0.142] | 0.118 [0.074, 0.177] | 0.463 [0.375, 0.545] |

Paired differences against the CRF (B − A):

| B | Slice | Typed F1 | Exact span precision | False-prerequisite rate |
|---|---|---:|---:|---:|
| DeBERTa | held-out (61) | +0.058 [−0.008, +0.134] | −0.120 [−0.266, +0.002] | +0.072 [−0.070, +0.196] |
| DistilBERT | held-out (61) | −0.028 [−0.088, +0.031] | **−0.193 [−0.327, −0.090]** | +0.052 [−0.114, +0.189] |
| DeBERTa | hand-labelled (10) | −0.024 [−0.129, +0.185] | −0.214 [−0.433, +0.172] | +0.167 [−0.402, +0.462] |
| DistilBERT | hand-labelled (10) | −0.143 [−0.346, +0.077] | −0.315 [−0.607, +0.062] | +0.095 [−0.333, +0.375] |

Bold marks a clear difference. Full reports: `compare_*.md`, and `<run>_dev_holdout.md` /
`<run>_dev_manual.md` for every run (`crf-batches-01-02_dev_holdout.md` for the CRF).

## Reading

- **Longer training helped DeBERTa.** With `sqrt` weights at 5e-5, the seed mean rose from
  0.131 (run 2, all 172 documents) to 0.197 on the held-out half. It now predicts about 5
  conditions per document, down from 8.
- **DeBERTa leads the CRF on held-out typed agreement, but not clearly.** The difference is
  +0.058 with an interval of [−0.008, +0.134]. Its false-prerequisite rate is not clearly
  different either (+0.072 [−0.070, +0.196]). On 61 documents neither system is shown to be
  better.
- **Uniform weights now get a fair test at 5e-5.** DeBERTa `none` reaches 0.145 ± 0.014 with
  the lowest false-prerequisite rates of any transformer (0.41–0.48), though still below
  `sqrt`. At 2e-5 the uniform runs still predict nothing by epoch 6.
- **DistilBERT stays behind.** Its span precision is clearly worse than the CRF's.
- **Still training.** Several of the best runs peaked at epoch 18–20 of 20.
- **No difference is clear on the 10 hand-labelled documents.**

## Provenance

- Results archive SHA-256 `e8d505b4fa25cc879f7d06c11f93faa4684e4eeb38e4eb8ecf52749e690138f6`.
- Committed:
  - per-run `metadata.json` in `metadata/`;
  - the predictions of the two compared runs in `predictions/`.
- The CRF's held-out report is `crf-batches-01-02_dev_holdout.md`.

To reproduce the held-out comparison:

```bash
uv run triggermap compare annotations/batches/batch-03.jsonl reports/agreement/predictions/crf-batches-01-02.jsonl \
    reports/neural/run-3/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl \
    --add-gold annotations/batches/batch-06.jsonl --subset splits/selection-v1/holdout.json --split dev
```
