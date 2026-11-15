# PyTorch vs ONNX fp32: hand-labelled dev (declared gate)

- Gold: `annotations/pilot/pilot-2.jsonl` (dev split of `splits/pool-v1.json`; origin: manual; 10 documents)
- Baseline (A): `reports/neural/run-3/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Candidate (B): `reports/onnx-int8/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2-fp32-dev.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 10

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2) | B (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.346 | 0.346 | +0.000 | [+0.000, +0.000] | no clear difference |
| Exact span F1 | 0.385 | 0.385 | +0.000 | [+0.000, +0.000] | no clear difference |
| Exact span precision | 0.286 | 0.286 | +0.000 | [+0.000, +0.000] | no clear difference |
| Exact span recall | 0.588 | 0.588 | +0.000 | [+0.000, +0.000] | no clear difference |
| Role macro-F1 (roles with gold support) | 0.196 | 0.196 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category macro-F1 | 0.571 | 0.571 | +0.000 | [+0.000, +0.000] | no clear difference |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.111 | 0.111 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| False prerequisite rate (lower is better) | 0.500 | 0.500 | +0.000 | [+0.000, +0.000] | no clear difference |
| Reversed meaning rate (lower is better) | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Category accuracy on exactly matched spans | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Role accuracy on exactly matched spans | 0.900 | 0.900 | +0.000 | [+0.000, +0.000] | no clear difference |
