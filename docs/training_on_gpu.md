# Training the transformer models on a GPU

DistilBERT and DeBERTa-v3-small are trained offline on one CUDA GPU, never in CI or on the
serving host. `scripts/gpu/run_neural.sh` does the whole run in one command, and
`scripts/gpu/score_neural.sh` scores the packed results on the development machine.

## What the run does

1. Creates a Python 3.12 environment with CUDA PyTorch (`.venv-gpu`).
2. Rebuilds the corpus from the pinned snapshot (`1912cbd…`, a sparse clone of about 360 MB) and
   stops unless `data/processed/advisories.jsonl` has the documented SHA-256.
3. Runs `configs/experiments/distilbert.toml` and `configs/experiments/deberta.toml`: two
   span-tag weightings (`sqrt`, `none`) × two learning rates (2e-5, 5e-5) × three seeds each,
   24 runs. Each trains for up to 20 epochs. Early stopping uses patience 3 and cannot end a
   run before epoch 6 (`min_epochs`), so a model that predicts nothing at first is not cut off.
   On a T4 a run takes about 1–6 minutes. Earlier runs are recorded in
   [`reports/neural/`](../reports/neural/run-2/README.md).
   - **Training:** the train split of `pilot-2`, `batch-01` and `batch-02` (239 documents).
   - **Early stopping and run selection:** only the **selection half** of the model-drafted
     dev batches `batch-03` and `batch-06` (`--dev-gold … --dev-subset
     splits/selection-v1/selection.json`; 111 documents in 46 project groups).
   - **Not used for selection:** the held-out half (61 documents in 46 other groups), the 10
     hand-labelled dev documents and the test split. The held-out half and the hand-labelled
     documents are used only for the comparisons below.
4. Predicts with every run on the pilot, `batch-03` and `batch-06` documents.
5. Packs two archives:
   - `triggermap-neural-results.tgz`: reports, predictions, run metadata and MLflow runs. No
     weights. This is the one to bring back.
   - `triggermap-neural-bundles.tgz`: the best bundle of each grid (weights, tokenizer,
     metadata), for later export and serving.

Runs resume: if the session stops, run the script again and finished runs are reused.

## On Kaggle

1. Create a notebook. Under *Settings*, choose **GPU T4** as the accelerator and turn
   **Internet** on. (The P100 option is too old for the CUDA 13 PyTorch wheels.)
2. Run one cell:

   ```bash
   !git clone https://github.com/professor3333/TriggerMap.git && cd TriggerMap && bash scripts/gpu/run_neural.sh
   ```

3. Download both `.tgz` files from `/kaggle/working` (the *Output* panel).

If the script stops with `torch has no CUDA`, the driver is older than CUDA 13 needs. Re-run
with the CUDA 12.6 wheels:

```bash
!cd TriggerMap && TORCH_INDEX=https://download.pytorch.org/whl/cu126 bash scripts/gpu/run_neural.sh
```

On Colab or a rented machine the same commands work (without the leading `!` in a shell). The
archives are then written to `./gpu-out`.

## Scoring on the development machine

```bash
bash scripts/gpu/score_neural.sh ~/Downloads/triggermap-neural-results.tgz
```

This writes `reports/neural/`:
- `<run>_dev_holdout.md`: agreement with the held-out half of the model-drafted dev records
  (`splits/selection-v1/holdout.json`). This is not accuracy.
- `<run>_dev_manual.md`: accuracy on the 10 hand-labelled dev documents.
- `compare_*`: paired comparisons of each grid's best run, chosen by its early-stopping score,
  against `crf-batches-01-02` on both slices.

The test split is not touched.

## Manual steps and notes

### Colab: keep results on Google Drive (survives disconnects)

```python
from google.colab import drive

drive.mount("/content/drive")
```

```bash
!mkdir -p /content/drive/MyDrive/triggermap/{experiments,mlruns,reports}
!ln -sfn /content/drive/MyDrive/triggermap/experiments artifacts
!ln -sfn /content/drive/MyDrive/triggermap/mlruns mlruns
```

`triggermap experiment` skips any run whose bundle already exists, so after a disconnect
you can rerun the same command and only unfinished runs train again.

### Running the grids by hand

The script runs these commands. Use them directly for ablations or a single config, with the
environment the script created (`.venv-gpu`).

```bash
!.venv-gpu/bin/triggermap experiment --config configs/experiments/distilbert.toml --dry-run
!.venv-gpu/bin/triggermap experiment --config configs/experiments/distilbert.toml \
    --gold annotations/pilot/pilot-2.jsonl annotations/batches/batch-01.jsonl annotations/batches/batch-02.jsonl \
    --dev-gold annotations/batches/batch-03.jsonl annotations/batches/batch-06.jsonl \
    --dev-subset splits/selection-v1/selection.json \
    --report /content/drive/MyDrive/triggermap/reports/distilbert.md
```

Each config runs span-tag weightings {sqrt, none} × learning rates {2e-5, 5e-5} × seeds {0, 1, 2}. Training uses only the train
split, early stopping and the report use only the dev records of `--dev-gold` that are listed
in `--dev-subset`, and the test split is never read. `splits/selection-v1/` was drawn once with
`triggermap corpus split-dev` (by leakage group, seed 0) and is immutable.
After choosing a backbone, set it in `configs/experiments/ablations.toml` and run the
ablations (no context, no group objective) and learning curves (125 and 250 documents)
the same way.

Every run's `metadata.json` records the base checkpoint revision, training-data hash,
split hash, hyperparameters, seed, per-epoch dev metrics, training time and peak GPU
memory. When an MLflow experiment is configured (the default), the same values go to
`mlruns/`.

### Profile before spending

Run one configuration with `--dry-run` first, then a single run, and read `train_seconds`
and `peak_gpu_memory_mb` from its `metadata.json` before launching a whole grid. Paid GPU
time is capped at about US$50 for the project. If memory runs out, reduce `batch_size` and
raise `gradient_accumulation`, keeping their product the same.

### MLflow runs

The results archive includes `mlruns/`. Browse it with:

```bash
MLFLOW_ALLOW_FILE_STORE=true uvx --from mlflow==3.17.1 mlflow ui --backend-store-uri ./mlruns
```

Model bundles are not committed (`artifacts/` is gitignored); release bundles are published
separately with their metadata.
