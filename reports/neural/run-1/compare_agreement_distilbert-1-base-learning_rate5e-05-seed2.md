# Agreement: crf-batches-01-02 -> distilbert-1-base-learning_rate5e-05-seed2

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Baseline (A): `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/neural/predictions/distilbert-1-base-learning_rate5e-05-seed2.jsonl` (distilbert-1-base-learning_rate5e-05-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 172

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (distilbert-1-base-learning_rate5e-05-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.145 | 0.019 | -0.126 | [-0.165, -0.084] | B clearly worse |
| Exact span F1 | 0.221 | 0.026 | -0.195 | [-0.243, -0.143] | B clearly worse |
| Exact span precision | 0.332 | 0.014 | -0.318 | [-0.384, -0.262] | B clearly worse |
| Exact span recall | 0.166 | 0.238 | +0.073 | [+0.000, +0.148] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.115 | 0.012 | -0.102 | [-0.147, -0.054] | B clearly worse |
| Category macro-F1 | 0.137 | 0.018 | -0.119 | [-0.154, -0.075] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.065 | 0.000 | -0.065 | [-0.104, -0.030] | B clearly worse |
| Complete-document exact match, documents without conditions | 0.882 | 0.000 | -0.882 | [-1.000, -0.714] | B clearly worse |
| False prerequisite rate (lower is better) | 0.353 | 0.845 | +0.492 | [+0.431, +0.579] | B clearly worse |
| Reversed meaning rate (lower is better) | 0.074 | 0.072 | -0.002 | [-0.061, +0.048] | no clear difference |
| Category accuracy on exactly matched spans | 0.797 | 0.870 | +0.073 | [-0.071, +0.237] | no clear difference |
| Role accuracy on exactly matched spans | 0.859 | 0.848 | -0.012 | [-0.127, +0.079] | no clear difference |
