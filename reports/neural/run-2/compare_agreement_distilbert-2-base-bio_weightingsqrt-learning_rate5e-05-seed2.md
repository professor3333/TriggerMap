# Agreement: crf-batches-01-02 -> distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Baseline (A): `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/neural/predictions/distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 172

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (distilbert-2-base-bio_weightingsqrt-learning_rate5e-05-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.145 | 0.075 | -0.070 | [-0.113, -0.020] | B clearly worse |
| Exact span F1 | 0.221 | 0.101 | -0.120 | [-0.172, -0.062] | B clearly worse |
| Exact span precision | 0.332 | 0.072 | -0.260 | [-0.320, -0.202] | B clearly worse |
| Exact span recall | 0.166 | 0.171 | +0.005 | [-0.054, +0.061] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.115 | 0.060 | -0.055 | [-0.093, -0.009] | B clearly worse |
| Category macro-F1 | 0.137 | 0.066 | -0.071 | [-0.108, -0.023] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.065 | 0.013 | -0.052 | [-0.095, -0.007] | B clearly worse |
| Complete-document exact match, documents without conditions | 0.882 | 0.882 | +0.000 | [-0.263, +0.214] | no clear difference |
| False prerequisite rate (lower is better) | 0.353 | 0.541 | +0.187 | [+0.124, +0.252] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.074 | 0.046 | -0.029 | [-0.083, +0.013] | no clear difference |
| Category accuracy on exactly matched spans | 0.797 | 0.848 | +0.052 | [-0.058, +0.192] | no clear difference |
| Role accuracy on exactly matched spans | 0.859 | 0.879 | +0.019 | [-0.082, +0.108] | no clear difference |
