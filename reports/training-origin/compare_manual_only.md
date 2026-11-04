# Pilot-2 dev (manual): crf-pilot-2-manual vs crf-pilot-2

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/training-origin/predictions/crf-pilot-2-manual.jsonl` (crf-pilot-2-manual)
- Candidate (B): `reports/pilot/predictions/crf-pilot-2.jsonl` (crf-pilot-2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-pilot-2-manual) | B (crf-pilot-2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.300 | 0.231 | -0.069 | [-0.260, +0.121] | no clear difference |
| Exact span F1 | 0.300 | 0.231 | -0.069 | [-0.260, +0.121] | no clear difference |
| Exact span precision | 1.000 | 0.333 | -0.667 | [-0.833, +0.000] | no clear difference |
| Exact span recall | 0.176 | 0.176 | +0.000 | [-0.150, +0.154] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.158 | 0.120 | -0.038 | [-0.215, +0.075] | no clear difference |
| Category macro-F1 | 0.193 | 0.176 | -0.017 | [-0.167, +0.077] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.111 | 0.111 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.000 | 0.444 | +0.444 | [+0.000, +0.667] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
