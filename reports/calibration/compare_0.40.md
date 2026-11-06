# Held-out agreement at target precision 0.40: CRF -> DeBERTa

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/calibration/predictions/crf-0.40.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/calibration/predictions/deberta-0.40.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.102 | 0.182 | +0.080 | [-0.003, +0.162] | no clear difference |
| Exact span F1 | 0.102 | 0.193 | +0.091 | [+0.004, +0.171] | B clearly better |
| Exact span precision | 0.471 | 0.472 | +0.002 | [-0.252, +0.232] | no clear difference |
| Exact span recall | 0.057 | 0.121 | +0.064 | [+0.007, +0.126] | B clearly better |
| Role macro-F1 (roles with gold support) | 0.068 | 0.054 | -0.013 | [-0.099, +0.048] | no clear difference |
| Category macro-F1 | 0.089 | 0.110 | +0.021 | [-0.035, +0.084] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.018 | 0.035 | +0.018 | [-0.046, +0.099] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.231 | 0.333 | +0.103 | [-0.178, +0.318] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 0.941 | -0.059 | [-0.158, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
