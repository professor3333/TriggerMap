# Agreement: crf-batches-01-02 -> deberta-1-base-learning_rate5e-05-seed1

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Baseline (A): `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/neural/predictions/deberta-1-base-learning_rate5e-05-seed1.jsonl` (deberta-1-base-learning_rate5e-05-seed1)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 172

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (deberta-1-base-learning_rate5e-05-seed1) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.145 | 0.023 | -0.122 | [-0.160, -0.081] | B clearly worse |
| Exact span F1 | 0.221 | 0.034 | -0.187 | [-0.236, -0.135] | B clearly worse |
| Exact span precision | 0.332 | 0.018 | -0.314 | [-0.380, -0.256] | B clearly worse |
| Exact span recall | 0.166 | 0.264 | +0.098 | [+0.025, +0.172] | B clearly better |
| Role macro-F1 (roles with gold support) | 0.115 | 0.015 | -0.100 | [-0.144, -0.051] | B clearly worse |
| Category macro-F1 | 0.137 | 0.023 | -0.114 | [-0.149, -0.070] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.065 | 0.000 | -0.065 | [-0.104, -0.030] | B clearly worse |
| Complete-document exact match, documents without conditions | 0.882 | 0.000 | -0.882 | [-1.000, -0.714] | B clearly worse |
| False prerequisite rate (lower is better) | 0.353 | 0.839 | +0.486 | [+0.420, +0.574] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.074 | 0.055 | -0.020 | [-0.079, +0.032] | no clear difference |
| Category accuracy on exactly matched spans | 0.797 | 0.804 | +0.007 | [-0.112, +0.159] | no clear difference |
| Role accuracy on exactly matched spans | 0.859 | 0.853 | -0.006 | [-0.126, +0.084] | no clear difference |
