# Held-out agreement at target precision 0.30: CRF -> DeBERTa

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/calibration/predictions/crf-0.30.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/calibration/predictions/deberta-0.30.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.107 | 0.207 | +0.100 | [+0.034, +0.172] | B clearly better |
| Exact span F1 | 0.130 | 0.225 | +0.095 | [+0.027, +0.163] | B clearly better |
| Exact span precision | 0.379 | 0.329 | -0.051 | [-0.266, +0.118] | no clear difference |
| Exact span recall | 0.079 | 0.171 | +0.093 | [+0.038, +0.151] | B clearly better |
| Role macro-F1 (roles with gold support) | 0.076 | 0.063 | -0.013 | [-0.094, +0.045] | no clear difference |
| Category macro-F1 | 0.092 | 0.145 | +0.053 | [-0.009, +0.120] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.035 | 0.035 | +0.000 | [-0.047, +0.046] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.280 | 0.391 | +0.111 | [-0.117, +0.317] | no clear difference |
| Reversed meaning rate (lower is better) | 0.100 | 0.047 | -0.053 | [-0.250, +0.094] | no clear difference |
| Category accuracy on exactly matched spans | 0.818 | 0.917 | +0.098 | [-0.136, +0.447] | no clear difference |
| Role accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
