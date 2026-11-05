# Hand-labelled dev: adding batch-02

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/agreement/predictions/crf-pilot-2-batch-01.jsonl` (crf-pilot-2-batch-01)
- Candidate (B): `reports/agreement/predictions/crf-batches-01-02.jsonl` (crf-batches-01-02)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-pilot-2-batch-01) | B (crf-batches-01-02) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.444 | 0.370 | -0.074 | [-0.182, +0.000] | no clear difference |
| Exact span F1 | 0.444 | 0.370 | -0.074 | [-0.182, +0.000] | no clear difference |
| Exact span precision | 0.600 | 0.500 | -0.100 | [-0.500, +0.027] | no clear difference |
| Exact span recall | 0.353 | 0.294 | -0.059 | [-0.200, +0.000] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.231 | 0.200 | -0.031 | [-0.122, +0.000] | no clear difference |
| Category macro-F1 | 0.267 | 0.237 | -0.030 | [-0.133, +0.000] | no clear difference |
| Group exact-match F1 | 0.500 | 0.500 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.222 | 0.222 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.300 | 0.333 | +0.033 | [-0.050, +0.500] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [-1.000, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [-1.000, +0.000] | no clear difference |
