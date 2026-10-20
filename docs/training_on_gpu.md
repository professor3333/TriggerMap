# Training the transformer models on a GPU

Fine-tuning DistilBERT and DeBERTa-v3-small needs a GPU; the local Mac is only for smoke
tests. These steps use Google Colab (a free T4 GPU, 16 GB, is enough). The same commands
work on any Linux GPU machine. Training never runs in CI or on the serving host.

## 1. Runtime

In Colab: **Runtime → Change runtime type → T4 GPU**. Then, in a cell:

```bash
!nvidia-smi --query-gpu=name,memory.total --format=csv
```

## 2. Code and environment

```bash
!git clone https://github.com/professor3333/TriggerMap.git
%cd TriggerMap
!pip install -q -e ".[neural]"
```

Use plain `pip` here, not `uv sync`. The project's uv configuration pins **CPU** PyTorch on
Linux (so CI stays small); `pip` ignores that setting and keeps Colab's CUDA build.

## 3. Rebuild the corpus and check it matches

```bash
!triggermap ingest fetch --commit 1912cbd6ce9d4cb141636adc4abafb4eb77a93e6
!triggermap ingest build
!git diff --exit-code data/manifests/snapshot.json && echo "corpus identical to the pinned manifest"
```

If the manifest differs, stop: the gold annotations would not match the text.

## 4. Persist results to Google Drive (survives disconnects)

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

## 5. Run the experiments

Gold files are the committed annotation JSONL files: the pilot and every imported batch.

```bash
!triggermap experiment --config configs/experiments/distilbert.toml --dry-run
!triggermap experiment --config configs/experiments/distilbert.toml \
    --gold annotations/pilot/pilot-1.jsonl annotations/batches/batch-0*.jsonl \
    --report /content/drive/MyDrive/triggermap/reports/distilbert.md
!triggermap experiment --config configs/experiments/deberta.toml \
    --gold annotations/pilot/pilot-1.jsonl annotations/batches/batch-0*.jsonl \
    --report /content/drive/MyDrive/triggermap/reports/deberta.md
```

Each config runs learning rates {2e-5, 5e-5} × seeds {0, 1, 2}. Training uses only the train
pool, model selection and the report use only the dev pool, and the test pool is never read.
After choosing a backbone, set it in `configs/experiments/ablations.toml` and run the
ablations (no context, no group objective) and learning curves (125 and 250 documents)
the same way.

Every run's `metadata.json` records the base checkpoint revision, training-data hash,
split hash, hyperparameters, seed, per-epoch dev metrics, training time and peak GPU
memory. When an MLflow experiment is configured (the default), the same values go to
`mlruns/`.

## 6. Profile before spending

Run one configuration with `--dry-run` first, then a single run, and read `train_seconds`
and `peak_gpu_memory_mb` from its `metadata.json` before launching a whole grid. Paid GPU
time is capped at about US$50 for the project. If memory runs out, reduce `batch_size` and
raise `gradient_accumulation`, keeping their product the same.

## 7. Back on your machine

Copy the reports and the chosen bundle from Drive. Browse runs with:

```bash
uvx --from mlflow==3.17.1 mlflow ui --backend-store-uri ./mlruns
```

Model bundles are not committed (`artifacts/` is gitignored); release bundles are published
separately with their metadata.
