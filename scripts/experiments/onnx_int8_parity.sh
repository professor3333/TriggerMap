#!/usr/bin/env bash
# ONNX FP32 and dynamic INT8 vs PyTorch for a trained transformer bundle (dev only).
#
#   bash scripts/experiments/onnx_int8_parity.sh BUNDLE_DIR [WORK_DIR]
#
# Exports BUNDLE_DIR to ONNX FP32 and dynamic INT8 (WORK_DIR, default artifacts/onnx/<name>),
# predicts the pilot, batch-03, batch-06 and batch-07 documents with both runtimes on CPU
# (2 threads), and compares each with the bundle's committed PyTorch predictions:
#   - the declared gate (docs/targets.md): typed F1 on the hand-labelled dev documents
#     (`--gold-origin manual`), no drop of more than 1.0 point;
#   - agreement on the 172 model-drafted dev records of batch-03 and batch-06;
#   - how many documents keep identical conditions.
# The PyTorch predictions are read from reports/neural/run-3/predictions/<name>.jsonl and
# reports/batch-07-comparison/predictions/<name>.jsonl. Nothing touches the test split.
#
# Finished prediction files and an existing export are reused, so a rerun resumes after the
# intermittent native crash (libc++abi recursive_mutex) that onnxruntime processes sometimes hit
# at exit on macOS.
set -euo pipefail
[ -f pyproject.toml ] && [ -d annotations ] || { echo "run from the repository root" >&2; exit 1; }
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-2} MKL_NUM_THREADS=${MKL_NUM_THREADS:-2}
export TOKENIZERS_PARALLELISM=false

BUNDLE=${1:?usage: onnx_int8_parity.sh BUNDLE_DIR [WORK_DIR]}
NAME=$(basename "$BUNDLE")
WORK=${2:-artifacts/onnx/$NAME}
OUT=reports/onnx-int8
TM=(uv run --no-sync triggermap)
PT_DEV=reports/neural/run-3/predictions/$NAME.jsonl
PT_B07=reports/batch-07-comparison/predictions/$NAME.jsonl
DEV_SAMPLES=(annotations/pilot/pilot_manifest.json annotations/batches/batch-03.json annotations/batches/batch-06.json)
for f in "$PT_DEV" "$PT_B07"; do [ -s "$f" ] || { echo "missing PyTorch predictions $f" >&2; exit 1; }; done
mkdir -p "$OUT/predictions"

predict() {  # <runtime> <out file> <sample...>; reuses a finished prediction file
  local rt=$1 out=$2
  shift 2
  [ -s "$out" ] && { echo "reusing $out"; return; }
  "${TM[@]}" predict --model onnx --model-dir "$WORK/$rt" --sample "$@" --out "$out"
}

[ -f "$WORK/int8/model.int8.onnx" ] || "${TM[@]}" export onnx --bundle "$BUNDLE" --out "$WORK/fp32" --int8 "$WORK/int8"
for rt in fp32 int8; do
  predict "$rt" "$OUT/predictions/$NAME-$rt-dev.jsonl" "${DEV_SAMPLES[@]}"
  predict "$rt" "$OUT/predictions/$NAME-$rt-batch-07.jsonl" annotations/batches/batch-07.json
  "${TM[@]}" compare annotations/pilot/pilot-2.jsonl "$PT_DEV" "$OUT/predictions/$NAME-$rt-dev.jsonl" \
    --split dev --gold-origin manual --title "PyTorch vs ONNX $rt: hand-labelled dev (declared gate)" \
    --out "$OUT/${rt}_gate_manual.md"
  "${TM[@]}" compare annotations/batches/batch-03.jsonl "$PT_DEV" "$OUT/predictions/$NAME-$rt-dev.jsonl" \
    --add-gold annotations/batches/batch-06.jsonl --split dev \
    --title "PyTorch vs ONNX $rt: agreement with 172 model-drafted dev records" \
    --out "$OUT/${rt}_agreement.md"
done

uv run --no-sync python -I - "$OUT" "$NAME" "$PT_DEV" "$PT_B07" <<'EOF'
import json, sys
from pathlib import Path
out, name, pt_dev, pt_b07 = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
def load(path):
    rows = (json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines())
    return {r["advisory_id"]: r for r in rows}
def typed(r):
    return {(tuple(c["span"]), c["category"], c["role"]) for c in r["conditions"]}
pytorch = {**load(pt_dev), **load(pt_b07)}
lines = ["| Runtime | Documents | Identical documents | Conditions (PyTorch) | Conditions (runtime) | Shared |",
         "|---|---:|---:|---:|---:|---:|"]
for rt in ("fp32", "int8"):
    pred = {**load(out / f"predictions/{name}-{rt}-dev.jsonl"), **load(out / f"predictions/{name}-{rt}-batch-07.jsonl")}
    ids = sorted(set(pred) & set(pytorch))
    same = sum(typed(pred[a]) == typed(pytorch[a]) for a in ids)
    n_pt = sum(len(typed(pytorch[a])) for a in ids)
    n_rt = sum(len(typed(pred[a])) for a in ids)
    shared = sum(len(typed(pred[a]) & typed(pytorch[a])) for a in ids)
    lines.append(f"| ONNX {rt} | {len(ids)} | {same} | {n_pt} | {n_rt} | {shared} |")
(out / "identity.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
EOF
