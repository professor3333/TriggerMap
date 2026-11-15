# Test split, hand-labelled (4): rules-2 minus crf-batches-01-02

- Gold: `annotations/batches/batch-04.jsonl`, `annotations/pilot/pilot-2.jsonl` (test split of `splits/pool-v1.json`; origin: manual; 4 documents)
- Baseline (A): `reports/test-evaluation/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Candidate (B): `reports/test-evaluation/predictions/rules-2.jsonl` (rules-2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 4

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-batches-01-02) | B (rules-2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.125 | 0.167 | +0.042 | [+0.000, +0.104] | no clear difference |
| Exact span F1 | 0.125 | 0.167 | +0.042 | [+0.000, +0.104] | no clear difference |
| Exact span precision | 0.111 | 0.200 | +0.089 | [+0.000, +0.190] | no clear difference |
| Exact span recall | 0.143 | 0.143 | +0.000 | [+0.000, +0.000] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.333 | 0.250 | -0.083 | [-0.083, +0.000] | no clear difference |
| Category macro-F1 | 0.111 | 0.167 | +0.056 | [+0.000, +0.071] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.667 | 0.500 | -0.167 | [-0.750, +1.000] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
