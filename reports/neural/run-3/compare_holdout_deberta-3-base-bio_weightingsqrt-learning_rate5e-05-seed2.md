# Agreement (held-out half): crf-batches-01-02 -> deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; subset `splits/selection-v1/holdout.json`; 61 documents)
- Baseline (A): `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/neural/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 61

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.127 | 0.185 | +0.058 | [-0.008, +0.134] | no clear difference |
| Exact span F1 | 0.176 | 0.221 | +0.045 | [-0.042, +0.132] | no clear difference |
| Exact span precision | 0.281 | 0.162 | -0.120 | [-0.266, +0.002] | no clear difference |
| Exact span recall | 0.129 | 0.350 | +0.221 | [+0.127, +0.317] | B clearly better |
| Role macro-F1 (roles with gold support) | 0.103 | 0.100 | -0.004 | [-0.086, +0.105] | no clear difference |
| Category macro-F1 | 0.131 | 0.149 | +0.018 | [-0.067, +0.099] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.053 | 0.018 | -0.035 | [-0.115, +0.047] | no clear difference |
| Complete-document exact match, documents without conditions | 0.750 | 0.250 | -0.500 | [-1.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.412 | 0.483 | +0.072 | [-0.070, +0.196] | no clear difference |
| Reversed meaning rate (lower is better) | 0.108 | 0.047 | -0.061 | [-0.198, +0.036] | no clear difference |
| Category accuracy on exactly matched spans | 0.833 | 0.857 | +0.024 | [-0.172, +0.275] | no clear difference |
| Role accuracy on exactly matched spans | 0.889 | 0.959 | +0.070 | [-0.038, +0.229] | no clear difference |
