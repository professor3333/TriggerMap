# CRF ablations and learning curve (2026-11-07)

How much each feature group and each extra training document contributes to the CRF behind
the v0.1.0 preview (`crf-batches-01-02`). The runs are in
[`configs/experiments/crf-ablations.toml`](../../configs/experiments/crf-ablations.toml) and are
run by [`scripts/experiments/crf_ablations.sh`](../../scripts/experiments/crf_ablations.sh).

- **Training data:** the train split of `pilot-2`, `batch-01` and `batch-02` (239 documents: 7
  `manual`, 232 model drafts), the released model's training set.
- **Scored on:** the 172 model-drafted dev records (`batch-03` + `batch-06`). These scores are
  **agreement with the drafting model, not accuracy**. The CRF is not tuned or selected on
  them; every run here is a measurement.
- **Also scored on:** the 10 hand-labelled dev documents of `pilot-2`, for the ablations.
- **Untouched:** the test split.
- **Reproducible:** the full-data run reproduces the released model exactly. All 272 of its
  predictions equal those of `crf-batches-01-02` in
  [`reports/agreement/predictions/`](../agreement/predictions/), apart from the model id.

95% project-group bootstrap intervals, 1,000 resamples.

## Ablations

One factor removed at a time, on all 239 training documents:
- **`no-context`** drops the heading, list-level and lead-in features from the tagger and the
  attribute classifiers, and the list and lead-in features from the group classifier.
- **`no-pos`** drops the spaCy part-of-speech features.

| Run | Typed F1 | Exact span F1 | Role macro-F1 | False-prerequisite rate | Training seconds |
|---|---:|---:|---:|---:|---:|
| full | 0.145 [0.104, 0.186] | 0.221 [0.169, 0.268] | 0.115 [0.066, 0.161] | 0.353 [0.268, 0.417] | 22 |
| no-context | 0.139 [0.101, 0.178] | 0.203 [0.160, 0.242] | 0.114 [0.061, 0.172] | 0.377 [0.298, 0.436] | 19 |
| no-pos | 0.147 [0.110, 0.188] | 0.217 [0.168, 0.259] | 0.121 [0.069, 0.177] | 0.331 [0.228, 0.410] | 8 |

Paired differences against the full model (B − A):

| B | Slice | Typed F1 | Exact span F1 | False-prerequisite rate (lower is better) |
|---|---|---:|---:|---:|
| no-context | agreement (172) | −0.006 [−0.027, +0.020] | −0.018 [−0.044, +0.011] | +0.024 [−0.030, +0.073] |
| no-pos | agreement (172) | +0.002 [−0.025, +0.032] | −0.004 [−0.035, +0.031] | −0.022 [−0.089, +0.024] |
| no-context | hand-labelled (10) | +0.030 [+0.000, +0.095] | +0.030 [+0.000, +0.095] | −0.048 [−0.500, +0.068] |
| no-pos | hand-labelled (10) | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |

None of these differences is clear. Full reports: `compare_agreement_*.md` and
`compare_manual_*.md`.

## Learning curve

Seeded random subsets of the 239 training documents, three subsets per budget. Mean ± SD
across the three subsets. The CRF is deterministic for a fixed training set, so the
239-document point is a single run.

| Training documents | Typed F1 | Exact span F1 | Role macro-F1 | False-prerequisite rate |
|---:|---:|---:|---:|---:|
| 30 | 0.054 ± 0.006 | 0.099 ± 0.007 | 0.027 ± 0.009 | 0.465 ± 0.084 |
| 60 | 0.094 ± 0.017 | 0.143 ± 0.007 | 0.061 ± 0.028 | 0.386 ± 0.055 |
| 120 | 0.143 ± 0.008 | 0.194 ± 0.006 | 0.088 ± 0.023 | 0.375 ± 0.042 |
| 180 | 0.140 ± 0.010 | 0.209 ± 0.008 | 0.108 ± 0.006 | 0.364 ± 0.034 |
| 239 | 0.145 | 0.221 | 0.115 | 0.353 |

Every run, with intervals, is in [`experiment.md`](experiment.md).

## Reading

- **Heading and list context adds nothing measurable to the CRF.** Removing it lowers span
  agreement by 0.018, with an interval across zero. The group classifier, where list context
  should matter most, matches no model-drafted group in any run (group F1 0.000).
- **Part-of-speech features add nothing measurable either,** and they cost the most. Without
  them training is about three times faster and needs no spaCy model. On the 10 hand-labelled
  documents the two models' predictions score identically. This makes dropping spaCy from the
  CRF a candidate simplification. It is not applied here: the released model stays as it is.
- **Typed agreement stops rising at about 120 documents.** It climbs from 0.054 (30 documents)
  to 0.143 (120), then stays flat (0.140 at 180, 0.145 at 239). Span agreement and role
  macro-F1 keep rising slowly, and the false-prerequisite rate keeps falling slowly. More
  model-drafted documents of the same kind are therefore unlikely to move the CRF's typed
  agreement much. The limit is the attribute classifiers (category and role), not the number of
  spans.
- **The group-objective ablation does not apply to the CRF.** Its group classifier is separate
  and predicts no matching group. That ablation is planned for the transformer
  (`configs/experiments/ablations.toml`), which needs a GPU.

Every number here is agreement with model drafts or a 10-document slice; neither is a release
result.

## Reproduce

```bash
bash scripts/experiments/crf_ablations.sh   # 15 trainings, a few minutes on a laptop
```

Bundles go to `artifacts/experiments/crf-ablations/` (not committed). The predictions of the
three full-data runs are committed in `predictions/`.
