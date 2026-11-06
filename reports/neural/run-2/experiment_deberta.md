# Experiment: deberta

- Config: `configs/experiments/deberta.toml`
- Gold: 3 file(s): 239 train docs
- Dev gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl`: 172 dev docs (early stopping and this table)
- Split: `splits/pool-v1.json` (41d7354e1a13)

## Runs (dev split, 95% leakage-group bootstrap intervals)

| Run | Docs | Typed F1 | Span F1 | Role macro-F1 | Group F1 | False prereq. | Best epoch | Seconds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed0 | 239 | 0.072 [0.054, 0.094] | 0.089 [0.068, 0.114] | 0.036 [0.022, 0.058] | 0.000 [0.000, 0.000] | 0.661 [0.623, 0.695] | 15 | 267.1 |
| deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed1 | 239 | 0.077 [0.060, 0.100] | 0.098 [0.078, 0.121] | 0.041 [0.026, 0.060] | 0.000 [0.000, 0.000] | 0.658 [0.619, 0.691] | 15 | 264.9 |
| deberta-2-base-bio_weightingsqrt-learning_rate2e-05-seed2 | 239 | 0.070 [0.051, 0.093] | 0.090 [0.070, 0.115] | 0.040 [0.024, 0.063] | 0.000 [0.000, 0.000] | 0.701 [0.663, 0.732] | 11 | 246.3 |
| deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed0 | 239 | 0.133 [0.108, 0.164] | 0.165 [0.141, 0.194] | 0.087 [0.059, 0.119] | 0.000 [0.000, 0.000] | 0.607 [0.566, 0.642] | 9 | 209.5 |
| deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed1 | 239 | 0.132 [0.110, 0.160] | 0.161 [0.136, 0.190] | 0.069 [0.050, 0.090] | 0.000 [0.000, 0.000] | 0.596 [0.555, 0.635] | 15 | 262.9 |
| deberta-2-base-bio_weightingsqrt-learning_rate5e-05-seed2 | 239 | 0.130 [0.102, 0.162] | 0.152 [0.124, 0.184] | 0.093 [0.054, 0.142] | 0.000 [0.000, 0.000] | 0.577 [0.533, 0.616] | 9 | 209.9 |
| deberta-2-base-bio_weightingnone-learning_rate2e-05-seed0 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.955 [0.891, 1.000] | 1 | 68.6 |
| deberta-2-base-bio_weightingnone-learning_rate2e-05-seed1 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.937 [0.880, 0.978] | 1 | 68.6 |
| deberta-2-base-bio_weightingnone-learning_rate2e-05-seed2 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.959 [0.935, 0.978] | 1 | 68.4 |
| deberta-2-base-bio_weightingnone-learning_rate5e-05-seed0 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1 | 68.5 |
| deberta-2-base-bio_weightingnone-learning_rate5e-05-seed1 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1 | 68.2 |
| deberta-2-base-bio_weightingnone-learning_rate5e-05-seed2 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1 | 68.3 |

## Across seeds (typed F1)

| Variant | Seeds | Mean | SD |
|---|---:|---:|---:|
| deberta-2-base-bio_weightingsqrt-learning_rate2e-05 | 3 | 0.073 | 0.004 |
| deberta-2-base-bio_weightingsqrt-learning_rate5e-05 | 3 | 0.131 | 0.001 |
| deberta-2-base-bio_weightingnone-learning_rate2e-05 | 3 | 0.000 | 0.000 |
| deberta-2-base-bio_weightingnone-learning_rate5e-05 | 3 | 0.000 | 0.000 |
