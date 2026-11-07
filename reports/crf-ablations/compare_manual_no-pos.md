# Hand-labelled dev (10): full -> no-pos

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/crf-ablations/predictions/crf-abl-full.jsonl` (crf-abl-full)
- Candidate (B): `reports/crf-ablations/predictions/crf-abl-no-pos.jsonl` (crf-abl-no-pos)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (crf-abl-full) | B (crf-abl-no-pos) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.370 | 0.370 | +0.000 | [+0.000, +0.000] | no clear difference |
| Exact span F1 | 0.370 | 0.370 | +0.000 | [+0.000, +0.000] | no clear difference |
| Exact span precision | 0.500 | 0.500 | +0.000 | [+0.000, +0.000] | no clear difference |
| Exact span recall | 0.294 | 0.294 | +0.000 | [+0.000, +0.000] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.200 | 0.200 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category macro-F1 | 0.237 | 0.237 | +0.000 | [+0.000, +0.000] | no clear difference |
| Group exact-match F1 | 0.500 | 0.500 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.222 | 0.222 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.333 | 0.333 | +0.000 | [+0.000, +0.000] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
