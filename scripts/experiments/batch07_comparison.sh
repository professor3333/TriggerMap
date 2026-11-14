#!/usr/bin/env bash
# Score systems on the 100 batch-07 dev documents against both model drafts.
#
#   bash scripts/experiments/batch07_comparison.sh [TRANSFORMER_BUNDLE_DIR ...]
#
# Predicts batch-07 with the released CRF (artifacts/crf-batches-01-02, also the v0.1.0 release
# asset), rules-2 and any transformer bundles given, then runs `triggermap multiref` against
# draft 1 (annotations/batches/batch-07.jsonl) and draft 2 (annotations/second-drafts/). The CRF
# is the paired baseline. Existing prediction files are reused, so adding a bundle later only
# predicts that bundle. No system was trained, tuned or selected on batch-07; the test split is
# not touched. Scores against model drafts are agreement with the drafts, not accuracy.
#
# Transformers run on CPU with 2 threads (about 45 s and 1.1 GB for DeBERTa-v3-small).
set -euo pipefail
[ -f pyproject.toml ] && [ -d annotations ] || { echo "run from the repository root" >&2; exit 1; }
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-2} MKL_NUM_THREADS=${MKL_NUM_THREADS:-2}
export TOKENIZERS_PARALLELISM=false

TM=(uv run --no-sync triggermap)
SAMPLE=annotations/batches/batch-07.json
OUT=reports/batch-07-comparison
mkdir -p "$OUT/predictions"

predict() {  # <out name> <predict args...>
  local out="$OUT/predictions/$1.jsonl"
  shift
  [ -s "$out" ] && { echo "reusing $out"; return; }
  "${TM[@]}" predict "$@" --sample "$SAMPLE" --out "$out"
}

predict crf-batches-01-02 --model crf --model-dir artifacts/crf-batches-01-02
predict rules-2 --model rules
preds=("$OUT/predictions/crf-batches-01-02.jsonl" "$OUT/predictions/rules-2.jsonl")
for bundle in "$@"; do
  name=$(basename "$bundle")
  predict "$name" --model transformer --model-dir "$bundle"
  preds+=("$OUT/predictions/$name.jsonl")
done
for f in "$OUT"/predictions/*.jsonl; do
  case " ${preds[*]} " in *" $f "*) ;; *) preds+=("$f") ;; esac  # bundles added in earlier runs
done

"${TM[@]}" multiref annotations/batches/batch-07.jsonl annotations/second-drafts/batch-07.jsonl \
  "${preds[@]}" --title "batch-07: systems against both model drafts (baseline crf-batches-01-02)" \
  --out "$OUT/batch-07.md"
