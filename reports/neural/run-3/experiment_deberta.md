# Experiment: deberta

- Config: `configs/experiments/deberta.toml`
- Gold: 3 file(s): 239 train docs
- Dev gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl`, subset `splits/selection-v1/selection.json`: 111 dev docs (early stopping and this table)
- Split: `splits/pool-v1.json` (41d7354e1a13)

## Runs (dev split, 95% leakage-group bootstrap intervals)

| Run | Docs | Typed F1 | Span F1 | Role macro-F1 | Group F1 | False prereq. | Best epoch | Seconds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed0 | 239 | 0.107 [0.083, 0.139] | 0.125 [0.100, 0.157] | 0.060 [0.032, 0.105] | 0.000 [0.000, 0.000] | 0.610 [0.555, 0.654] | 19 | 303.7 |
| deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed1 | 239 | 0.089 [0.062, 0.127] | 0.115 [0.085, 0.155] | 0.049 [0.026, 0.075] | 0.000 [0.000, 0.000] | 0.602 [0.539, 0.649] | 20 | 300.7 |
| deberta-3-base-bio_weightingsqrt-learning_rate2e-05-seed2 | 239 | 0.105 [0.070, 0.150] | 0.136 [0.100, 0.182] | 0.080 [0.034, 0.140] | 0.000 [0.000, 0.000] | 0.606 [0.553, 0.650] | 20 | 301.6 |
| deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed0 | 239 | 0.167 [0.130, 0.219] | 0.220 [0.177, 0.270] | 0.120 [0.062, 0.182] | 0.000 [0.000, 0.000] | 0.466 [0.405, 0.513] | 18 | 298.1 |
| deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed1 | 239 | 0.168 [0.136, 0.208] | 0.203 [0.170, 0.243] | 0.090 [0.058, 0.120] | 0.000 [0.000, 0.000] | 0.534 [0.451, 0.592] | 16 | 283.4 |
| deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2 | 239 | 0.185 [0.141, 0.248] | 0.230 [0.185, 0.289] | 0.125 [0.062, 0.210] | 0.000 [0.000, 0.000] | 0.494 [0.414, 0.545] | 19 | 298.9 |
| deberta-3-base-bio_weightingnone-learning_rate2e-05-seed0 | 239 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.939 [0.896, 0.970] | 1 | 87.6 |
| deberta-3-base-bio_weightingnone-learning_rate2e-05-seed1 | 239 | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.003] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.913 [0.866, 0.947] | 1 | 87.8 |
| deberta-3-base-bio_weightingnone-learning_rate2e-05-seed2 | 239 | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.003] | 0.000 [0.000, 0.001] | 0.000 [0.000, 0.000] | 0.920 [0.895, 0.945] | 1 | 87.9 |
| deberta-3-base-bio_weightingnone-learning_rate5e-05-seed0 | 239 | 0.154 [0.117, 0.198] | 0.182 [0.142, 0.224] | 0.140 [0.041, 0.216] | 0.000 [0.000, 0.000] | 0.430 [0.360, 0.475] | 16 | 281.7 |
| deberta-3-base-bio_weightingnone-learning_rate5e-05-seed1 | 239 | 0.144 [0.108, 0.191] | 0.173 [0.140, 0.215] | 0.071 [0.038, 0.108] | 0.000 [0.000, 0.000] | 0.459 [0.381, 0.511] | 20 | 296.5 |
| deberta-3-base-bio_weightingnone-learning_rate5e-05-seed2 | 239 | 0.133 [0.095, 0.190] | 0.171 [0.135, 0.222] | 0.110 [0.039, 0.189] | 0.000 [0.000, 0.000] | 0.502 [0.419, 0.558] | 15 | 266.2 |

## Across seeds (typed F1)

| Variant | Seeds | Mean | SD |
|---|---:|---:|---:|
| deberta-3-base-bio_weightingsqrt-learning_rate2e-05 | 3 | 0.100 | 0.010 |
| deberta-3-base-bio_weightingsqrt-learning_rate5e-05 | 3 | 0.173 | 0.010 |
| deberta-3-base-bio_weightingnone-learning_rate2e-05 | 3 | 0.000 | 0.000 |
| deberta-3-base-bio_weightingnone-learning_rate5e-05 | 3 | 0.143 | 0.011 |
