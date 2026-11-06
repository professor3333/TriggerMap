# Agreement (held-out half): crf-batches-01-02 -> distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/neural/predictions/distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed0.jsonl` (distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed0)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (distilbert-3-base-bio_weightingsqrt-learning_rate5e-05-seed0) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.127 | 0.099 | -0.028 | [-0.088, +0.031] | no clear difference |
| Exact span F1 | 0.176 | 0.118 | -0.058 | [-0.133, +0.010] | no clear difference |
| Exact span precision | 0.281 | 0.088 | -0.193 | [-0.327, -0.090] | B clearly worse |
| Exact span recall | 0.129 | 0.179 | +0.050 | [-0.016, +0.116] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.103 | 0.069 | -0.035 | [-0.098, +0.024] | no clear difference |
| Category macro-F1 | 0.131 | 0.081 | -0.050 | [-0.116, +0.018] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.053 | 0.018 | -0.035 | [-0.078, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 0.750 | 0.750 | +0.000 | [-1.000, +0.500] | no clear difference |
| False prerequisite rate (lower is better) | 0.412 | 0.463 | +0.052 | [-0.114, +0.189] | no clear difference |
| Reversed meaning rate (lower is better) | 0.108 | 0.044 | -0.064 | [-0.217, +0.041] | no clear difference |
| Category accuracy on exactly matched spans | 0.833 | 0.880 | +0.047 | [-0.172, +0.347] | no clear difference |
| Role accuracy on exactly matched spans | 0.889 | 0.960 | +0.071 | [-0.086, +0.286] | no clear difference |
