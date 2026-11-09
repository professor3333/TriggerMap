# Transformer ablations and learning curve (ablation-1, 2026-11-08)

A Kaggle run (one Tesla T4) of
[`configs/experiments/ablations.toml`](../../../configs/experiments/ablations.toml).

**Recipe:** the best grid cell of neural run 3, with one factor changed at a time:
- DeBERTa-v3-small, `sqrt` span-tag weights, learning rate 5e-5;
- up to 20 epochs, patience 3, no early stop before epoch 6;
- three seeds for every variant.

**Data:**
- **Training:** the train split of `pilot-2`, `batch-01` and `batch-02` (239 documents), as in
  runs 1–3.
- **Early stopping:** the selection half of the model-drafted dev records
  (`splits/selection-v1/selection.json`, 111 documents). Nothing else was used for it.
- **Scored on:** the held-out half (61 documents in 46 other project groups) and the 10
  hand-labelled dev documents. Against model drafts, the scores measure **agreement with the
  drafting model, not accuracy**.
- **Untouched:** the test split.

**No run is selected:** every seed is reported, and each variant is compared with the full
model trained with the same seed.

**Variants:**

| Variant | Change |
|---|---|
| `full` | none |
| `no-context` | no heading or list context in the windows |
| `no-group` | group loss weight 0 |
| `docs-60`, `docs-120` | a seeded random subset of 60 or 120 training documents |

## Results (held-out half, 61 documents)

Mean ± SD across the three seeds. The last column is typed F1 on the 10 hand-labelled dev
documents.

| Variant | Typed F1 | Exact span F1 | Exact span precision | False-prerequisite rate | Hand-labelled typed F1 |
|---|---:|---:|---:|---:|---:|
| full | 0.197 ± 0.012 | 0.230 ± 0.012 | 0.166 ± 0.012 | 0.493 ± 0.070 | 0.328 ± 0.043 |
| no-context | 0.199 ± 0.027 | 0.235 ± 0.028 | 0.168 ± 0.024 | 0.527 ± 0.074 | 0.256 ± 0.035 |
| no-group | 0.185 ± 0.048 | 0.227 ± 0.059 | 0.163 ± 0.056 | 0.541 ± 0.111 | 0.281 ± 0.093 |
| docs-120 | 0.097 ± 0.041 | 0.119 ± 0.040 | 0.076 ± 0.031 | 0.697 ± 0.086 | 0.186 ± 0.105 |
| docs-60 | 0.075 ± 0.031 | 0.090 ± 0.040 | 0.060 ± 0.030 | 0.633 ± 0.047 | 0.104 ± 0.066 |

For reference, the CRF (`crf-batches-01-02`) scores 0.127 typed F1 and a 0.412
false-prerequisite rate on the same 61 documents ([`../run-3/`](../run-3/README.md)).

### Paired differences against the full model, same seed (B − A)

95% project-group bootstrap intervals, 1,000 resamples. Bold marks a clear difference.

| Variant | Seed | Typed F1, held-out | False-prerequisite rate, held-out | Typed F1, hand-labelled (10) |
|---|---:|---:|---:|---:|
| no-context | 0 | +0.019 [−0.021, +0.062] | +0.038 [−0.021, +0.091] | −0.073 [−0.190, +0.021] |
| no-context | 1 | +0.000 [−0.028, +0.027] | **+0.042 [+0.005, +0.078]** | −0.027 [−0.079, +0.009] |
| no-context | 2 | −0.012 [−0.044, +0.026] | +0.023 [−0.022, +0.064] | **−0.117 [−0.232, −0.034]** |
| no-group | 0 | −0.015 [−0.060, +0.028] | +0.031 [−0.024, +0.089] | −0.009 [−0.113, +0.101] |
| no-group | 1 | +0.030 [−0.003, +0.064] | **−0.070 [−0.117, −0.024]** | +0.030 [−0.054, +0.134] |
| no-group | 2 | **−0.051 [−0.081, −0.017]** | **+0.183 [+0.132, +0.238]** | **−0.162 [−0.325, −0.018]** |
| docs-120 | 0 | **−0.120 [−0.180, −0.063]** | **+0.240 [+0.160, +0.312]** | **−0.215 [−0.308, −0.110]** |
| docs-120 | 1 | **−0.057 [−0.092, −0.024]** | **+0.062 [+0.012, +0.108]** | +0.024 [−0.067, +0.104] |
| docs-120 | 2 | **−0.124 [−0.169, −0.083]** | **+0.310 [+0.256, +0.369]** | **−0.233 [−0.428, −0.064]** |
| docs-60 | 0 | **−0.162 [−0.219, −0.110]** | **+0.209 [+0.122, +0.293]** | **−0.335 [−0.565, −0.122]** |
| docs-60 | 1 | **−0.125 [−0.174, −0.083]** | **+0.110 [+0.060, +0.166]** | **−0.133 [−0.307, −0.036]** |
| docs-60 | 2 | **−0.078 [−0.123, −0.031]** | **+0.101 [+0.038, +0.170]** | **−0.204 [−0.431, −0.003]** |

Full reports: `compare_holdout_*.md`, `compare_manual_*.md`, and `<run>_dev_holdout.md` /
`<run>_dev_manual.md` for every run. Selection-half scores are in
[`experiment.md`](experiment.md).

## Reading

- **DeBERTa needs much more data than the CRF.** With 60 or 120 training documents, every seed
  is clearly worse than with all 239, on typed agreement and on invented prerequisites. Typed
  agreement roughly doubles from 120 to 239 documents (0.097 → 0.197). The CRF, by contrast,
  stops improving at about 120 documents ([`../../crf-ablations/`](../../crf-ablations/README.md);
  measured on all 172 agreement records). So more training documents would likely raise
  DeBERTa's agreement further. With model-drafted labels, though, that means agreement with the
  drafting model, not shown accuracy.
- **Heading and list context: no clear effect on held-out agreement,** but every sign points
  the same way. Without context, the false-prerequisite rate is higher for all three seeds
  (+0.023 to +0.042, clear for one), and hand-labelled typed F1 is lower for all three (0.328 →
  0.256 on average, clear for one seed). That is weak evidence that context helps; 61 and 10
  documents cannot settle it.
- **Group objective: not measurable here.** No run reproduces a single drafted group exactly
  (group F1 0.000 everywhere), so its own target cannot be scored. Its effect on spans is
  inconsistent: one seed is clearly better without it, and one is clearly worse.
- **Training is unstable at this data size.** The worse seeds stopped early: `no-group` seed 2
  peaked at epoch 6, and `docs-120` seeds 0 and 2 at epochs 9 and 7. Without the group loss,
  the spread across seeds is four times larger (SD 0.048 against 0.012). Single runs should
  not be trusted; seed means are the unit of comparison.
- **The recipe reproduces.** The three `full` seeds score 0.208, 0.198 and 0.185 held-out.
  Run 3 scored 0.207, 0.198 and 0.185 with the same settings.

## Provenance

- Results archive SHA-256 `34451e81108226bb1067b8a458b7b1491c9979aa4309e8e69237c5044a5f3240`.
- Per-run `metadata/` (configuration, base revision, training hash and origins, per-epoch
  losses and dev scores, peak GPU memory) and every run's `predictions/` are committed. The
  weights are not.

To rescore from the archive:

```bash
bash scripts/gpu/score_ablations.sh ~/Downloads/triggermap-neural-results.tgz
```
