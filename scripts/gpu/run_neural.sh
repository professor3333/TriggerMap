#!/usr/bin/env bash
# Train and score the DistilBERT and DeBERTa-v3-small grids on one CUDA GPU (Kaggle, Colab or a
# rented box), then pack the results for scoring on the development machine.
#
#   git clone https://github.com/professor3333/TriggerMap.git && cd TriggerMap
#   bash scripts/gpu/run_neural.sh                 # both grids (24 runs)
#   CONFIGS="distilbert" bash scripts/gpu/run_neural.sh
#   TORCH_INDEX=https://download.pytorch.org/whl/cu126 bash scripts/gpu/run_neural.sh
#
# PyPI's torch 2.14 wheels target CUDA 13: they need a recent NVIDIA driver and a Turing (T4) or
# newer GPU. If the CUDA check below fails, set TORCH_INDEX to a CUDA 12 wheel index as shown.
#
# Writes $OUT_DIR/triggermap-neural-results.tgz (reports, predictions, run metadata, MLflow runs;
# no weights) and $OUT_DIR/triggermap-neural-bundles.tgz (the best bundle of each grid, by dev
# typed F1). OUT_DIR defaults to /kaggle/working on Kaggle, otherwise ./gpu-out.
#
# Selection never sees the test split, the hand-labelled dev documents or the held-out half:
# training uses the train split of the pilot and batches 01-02, and early stopping uses only
# the selection half of the model-drafted dev batches 03 and 06 (splits/selection-v1).
# Re-running resumes: finished runs are not retrained.
set -euo pipefail

CONFIGS=${CONFIGS:-"distilbert deberta"}
if [ -d /kaggle/working ]; then OUT_DIR=${OUT_DIR:-/kaggle/working}; else OUT_DIR=${OUT_DIR:-gpu-out}; fi
SNAPSHOT=1912cbd6ce9d4cb141636adc4abafb4eb77a93e6
CORPUS_SHA256=734043ff982a337f6cc593745160e997f20ee62609183ff857edce3d47d2b655
UV_VERSION=0.12.5
TRAIN_GOLD=(annotations/pilot/pilot-2.jsonl annotations/batches/batch-01.jsonl annotations/batches/batch-02.jsonl)
DEV_GOLD=(annotations/batches/batch-03.jsonl annotations/batches/batch-06.jsonl)
DEV_SUBSET=splits/selection-v1/selection.json  # early stopping; holdout.json is for comparisons
SAMPLES=(annotations/pilot/pilot_manifest.json annotations/batches/batch-03.json annotations/batches/batch-06.json)

[ -f pyproject.toml ] && [ -d annotations ] || { echo "run from the repository root" >&2; exit 1; }
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || { echo "no CUDA GPU found" >&2; exit 1; }
mkdir -p "$OUT_DIR"

# 1. Environment: Python 3.12 with CUDA PyTorch from PyPI. --no-sources skips the CPU-only torch
#    index that pyproject.toml pins for Linux development machines.
command -v uv >/dev/null || python3 -m pip install --quiet "uv==$UV_VERSION"
uv venv --quiet --allow-existing --python 3.12 .venv-gpu
uv pip install --quiet --python .venv-gpu --no-sources -e ".[neural]"
if [ -n "${TORCH_INDEX:-}" ]; then
  uv pip install --quiet --python .venv-gpu --reinstall-package torch \
    --index-url "$TORCH_INDEX" --extra-index-url https://pypi.org/simple "torch>=2.14,<2.15"
fi
TM=(.venv-gpu/bin/triggermap)
.venv-gpu/bin/python -c "import torch; assert torch.cuda.is_available(), 'torch has no CUDA: see TORCH_INDEX at the top of this script'; print('torch', torch.__version__, torch.cuda.get_device_name(0))"

# 2. Corpus from the pinned snapshot; stop if it is not byte-identical to the documented one.
if [ ! -f data/processed/advisories.jsonl ]; then
  "${TM[@]}" ingest fetch --commit "$SNAPSHOT"
  "${TM[@]}" ingest build
fi
echo "$CORPUS_SHA256  data/processed/advisories.jsonl" | sha256sum -c -

# 3. Grids, then predictions of every run on the pilot and dev-batch documents.
mkdir -p reports/neural/predictions
for config in $CONFIGS; do
  "${TM[@]}" experiment --config "configs/experiments/$config.toml" \
    --gold "${TRAIN_GOLD[@]}" --dev-gold "${DEV_GOLD[@]}" --dev-subset "$DEV_SUBSET" \
    --out-root artifacts/experiments --report "reports/neural/experiment_$config.md"
done
# Only the runs of the current configs (their model_id prefixes); older grids are left out.
# shellcheck disable=SC2086  # one argument per config / prefix
prefixes=$(.venv-gpu/bin/python - $CONFIGS <<'EOF'
import sys, tomllib
for config in sys.argv[1:]:
    with open(f"configs/experiments/{config}.toml", "rb") as fh:
        print(tomllib.load(fh)["train"]["model_id"])
EOF
)
find reports/neural/predictions -type f -delete  # stale files from an older grid
for prefix in $prefixes; do
  for bundle in artifacts/experiments/"$prefix"-*/; do
    [ -f "$bundle/metadata.json" ] || continue
    run=$(basename "$bundle")
    "${TM[@]}" predict --model transformer --model-dir "$bundle" \
      --sample "${SAMPLES[@]}" --out "reports/neural/predictions/$run.jsonl"
    cp "$bundle/metadata.json" "reports/neural/predictions/$run.metadata.json"
  done
done

# 4. Pack. Results carry no weights; bundles hold the best run of each grid.
pack=(reports/neural)
[ -d mlruns ] && pack+=(mlruns)
tar czf "$OUT_DIR/triggermap-neural-results.tgz" "${pack[@]}"
# shellcheck disable=SC2086  # one argument per config / prefix
best=$(.venv-gpu/bin/python - $prefixes <<'EOF'
import json, sys
from pathlib import Path
for prefix in sys.argv[1:]:
    runs = [
        (json.loads((p / "metadata.json").read_text()).get("best_dev_typed_f1") or 0.0, str(p))
        for p in Path("artifacts/experiments").glob(f"{prefix}-*") if (p / "metadata.json").exists()
    ]
    if runs:
        print(max(runs)[1])
EOF
)
# shellcheck disable=SC2086
[ -n "$best" ] && tar czf "$OUT_DIR/triggermap-neural-bundles.tgz" $best
ls -lh "$OUT_DIR"/triggermap-neural-*.tgz
echo "Copy triggermap-neural-results.tgz back and run: bash scripts/gpu/score_neural.sh <path>"
