# Agreement: rules-2 -> crf-batches-01-02

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Baseline (A): `reports/agreement/predictions/rules-2.jsonl` (rules-2)
- Candidate (B): `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 172

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (rules-2) | B (crf-batches-01-02) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.107 | 0.145 | +0.038 | [-0.012, +0.097] | no clear difference |
| Exact span F1 | 0.142 | 0.221 | +0.079 | [+0.028, +0.138] | B clearly better |
| Exact span precision | 0.272 | 0.332 | +0.060 | [-0.018, +0.171] | no clear difference |
| Exact span recall | 0.096 | 0.166 | +0.070 | [+0.030, +0.113] | B clearly better |
| Role macro-F1 (roles with gold support) | 0.116 | 0.115 | -0.002 | [-0.071, +0.126] | no clear difference |
| Category macro-F1 | 0.098 | 0.137 | +0.039 | [-0.002, +0.082] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.019 | 0.065 | +0.045 | [+0.007, +0.084] | B clearly better |
| Complete-document exact match, documents without conditions | 0.941 | 0.882 | -0.059 | [-0.200, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.330 | 0.353 | +0.023 | [-0.091, +0.170] | no clear difference |
| Reversed meaning rate (lower is better) | 0.060 | 0.074 | +0.014 | [-0.047, +0.067] | no clear difference |
| Category accuracy on exactly matched spans | 0.865 | 0.797 | -0.068 | [-0.199, +0.083] | no clear difference |
| Role accuracy on exactly matched spans | 0.892 | 0.859 | -0.033 | [-0.113, +0.092] | no clear difference |
