# Experiment: deberta

- Config: `configs/experiments/deberta.toml`
- Gold: 3 file(s): 239 train docs
- Dev gold: `annotations/batches/batch-03.jsonl`, `annotations/batches/batch-06.jsonl`: 172 dev docs (early stopping and this table)
- Split: `splits/pool-v1.json` (41d7354e1a13)

## Runs (dev split, 95% leakage-group bootstrap intervals)

| Run | Docs | Typed F1 | Span F1 | Role macro-F1 | Group F1 | False prereq. | Best epoch | Seconds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deberta-1-base-learning_rate2e-05-seed0 | 239 | 0.006 [0.004, 0.010] | 0.010 [0.007, 0.014] | 0.005 [0.003, 0.009] | 0.000 [0.000, 0.000] | 0.854 [0.837, 0.869] | 6 | 114.9 |
| deberta-1-base-learning_rate2e-05-seed1 | 239 | 0.006 [0.004, 0.008] | 0.010 [0.007, 0.013] | 0.005 [0.002, 0.008] | 0.000 [0.000, 0.000] | 0.868 [0.850, 0.884] | 6 | 113.3 |
| deberta-1-base-learning_rate2e-05-seed2 | 239 | 0.008 [0.006, 0.012] | 0.013 [0.010, 0.018] | 0.005 [0.003, 0.008] | 0.000 [0.000, 0.000] | 0.868 [0.851, 0.885] | 6 | 112.4 |
| deberta-1-base-learning_rate5e-05-seed0 | 239 | 0.020 [0.014, 0.027] | 0.028 [0.022, 0.036] | 0.017 [0.010, 0.027] | 0.000 [0.000, 0.000] | 0.832 [0.812, 0.850] | 6 | 109.6 |
| deberta-1-base-learning_rate5e-05-seed1 | 239 | 0.023 [0.017, 0.030] | 0.034 [0.026, 0.043] | 0.015 [0.009, 0.021] | 0.000 [0.000, 0.000] | 0.839 [0.818, 0.854] | 6 | 109.7 |
| deberta-1-base-learning_rate5e-05-seed2 | 239 | 0.020 [0.014, 0.028] | 0.030 [0.023, 0.039] | 0.014 [0.008, 0.021] | 0.000 [0.000, 0.000] | 0.834 [0.813, 0.851] | 6 | 109.4 |

## Across seeds (typed F1)

| Variant | Seeds | Mean | SD |
|---|---:|---:|---:|
| deberta-1-base-learning_rate2e-05 | 3 | 0.007 | 0.001 |
| deberta-1-base-learning_rate5e-05 | 3 | 0.021 | 0.002 |
