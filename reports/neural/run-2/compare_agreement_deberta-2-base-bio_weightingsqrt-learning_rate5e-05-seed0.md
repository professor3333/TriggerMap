# Agreement: crf-batches-01-02 -> deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Baseline (A): `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/neural/predictions/deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0.jsonl` (deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 172

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.145 | 0.133 | -0.013 | [-0.063, +0.043] | no clear difference |
| Exact span F1 | 0.221 | 0.165 | -0.056 | [-0.111, +0.007] | no clear difference |
| Exact span precision | 0.332 | 0.108 | -0.224 | [-0.288, -0.163] | B clearly worse |
| Exact span recall | 0.166 | 0.355 | +0.189 | [+0.127, +0.254] | B clearly better |
| Role macro-F1 (roles with gold support) | 0.115 | 0.087 | -0.028 | [-0.078, +0.024] | no clear difference |
| Category macro-F1 | 0.137 | 0.129 | -0.008 | [-0.060, +0.054] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.065 | 0.026 | -0.039 | [-0.076, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 0.882 | 0.176 | -0.706 | [-0.917, -0.462] | B clearly worse |
| False prerequisite rate (lower is better) | 0.353 | 0.607 | +0.254 | [+0.188, +0.343] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.074 | 0.053 | -0.021 | [-0.089, +0.039] | no clear difference |
| Category accuracy on exactly matched spans | 0.797 | 0.898 | +0.101 | [+0.010, +0.227] | B clearly better |
| Role accuracy on exactly matched spans | 0.859 | 0.905 | +0.046 | [-0.043, +0.111] | no clear difference |
