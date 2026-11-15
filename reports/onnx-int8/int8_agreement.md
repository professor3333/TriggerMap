# PyTorch vs ONNX int8: agreement with 172 model-drafted dev records

- Gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl` (dev split of `splits/pool-v1.json`; origin: all; 172 documents)
- Baseline (A): `reports/neural/run-3/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2)
- Candidate (B): `reports/onnx-int8/predictions/deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2-int8-dev.jsonl` (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2-int8)
- Bootstrap: 1000 paired resamples, project clusters, seed 0
- Documents: 172

Differences are B minus A with 95% paired bootstrap intervals. *Clear* means the whole interval lies on one side of zero.

| Metric | A (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2) | B (deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2-int8) | B - A | 95% CI | Verdict |
|---|---:|---:|---:|:---:|---|
| Typed condition micro-F1 (span + category + role) | 0.185 | 0.111 | -0.074 | [-0.121, -0.039] | B clearly worse |
| Exact span F1 | 0.226 | 0.136 | -0.091 | [-0.137, -0.054] | B clearly worse |
| Exact span precision | 0.167 | 0.145 | -0.021 | [-0.066, +0.020] | no clear difference |
| Exact span recall | 0.352 | 0.127 | -0.225 | [-0.274, -0.182] | B clearly worse |
| Role macro-F1 (roles with gold support) | 0.114 | 0.035 | -0.078 | [-0.121, -0.043] | B clearly worse |
| Category macro-F1 | 0.167 | 0.081 | -0.086 | [-0.128, -0.051] | B clearly worse |
| Group exact-match F1 | 0.000 | 0.000 | +0.000 | [+0.000, +0.000] | no clear difference |
| Complete-document exact match, documents with conditions | 0.071 | 0.039 | -0.032 | [-0.071, +0.000] | no clear difference |
| Complete-document exact match, documents without conditions | 0.412 | 0.706 | +0.294 | [+0.083, +0.500] | B clearly better |
| False prerequisite rate (lower is better) | 0.490 | 0.370 | -0.120 | [-0.178, -0.069] | B clearly better |
| Reversed meaning rate (lower is better) | 0.037 | 0.043 | +0.005 | [-0.021, +0.035] | no clear difference |
| Category accuracy on exactly matched spans | 0.875 | 0.939 | +0.064 | [-0.033, +0.153] | no clear difference |
| Role accuracy on exactly matched spans | 0.934 | 0.878 | -0.056 | [-0.134, +0.011] | no clear difference |
