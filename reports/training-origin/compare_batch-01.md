# Pilot-2 dev (manual): crf-pilot-2 vs crf-pilot-2-batch-01

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/pilot/predictions/crf-pilot-2.jsonl` (crf-pilot-2)
- Candidate (B): `reports/training-origin/predictions/crf-pilot-2-batch-01.jsonl` (crf-pilot-2-batch-01)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-pilot-2) | B (crf-pilot-2-batch-01) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.231 | 0.444 | +0.214 | [-0.026, +0.457] | no clear difference |
| Exact span F1 | 0.231 | 0.444 | +0.214 | [-0.026, +0.457] | no clear difference |
| Exact span precision | 0.333 | 0.600 | +0.267 | [-0.100, +0.690] | no clear difference |
| Exact span recall | 0.176 | 0.353 | +0.176 | [+0.000, +0.389] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.120 | 0.231 | +0.111 | [-0.018, +0.400] | no clear difference |
| Category macro-F1 | 0.176 | 0.267 | +0.090 | [-0.032, +0.341] | no clear difference |
| Group exact-match F1 | 0.000 | 0.500 | +0.500 | [+0.000, +1.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.111 | 0.222 | +0.111 | [+0.000, +0.300] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.444 | 0.300 | -0.144 | [-0.462, +0.100] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
