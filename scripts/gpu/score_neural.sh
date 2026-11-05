#!/usr/bin/env bash
# Score the GPU runs packed by run_neural.sh on the development machine (no GPU needed).
#
#   bash scripts/gpu/score_neural.sh ~/Downloads/triggermap-neural-results.tgz
#
# Writes reports/neural/<run>_dev_agreement.md (agreement with the model-drafted dev batches 03
# and 06, not accuracy), <run>_dev_manual.md (the 10 hand-labelled dev documents) and paired
# comparisons of each grid's best run against crf-batches-01-02. The test split is not touched.
set -euo pipefail

archive=${1:?usage: score_neural.sh RESULTS.tgz}
[ -f pyproject.toml ] && [ -d annotations ] || { echo "run from the repository root" >&2; exit 1; }

# Unpack into a fresh directory and copy only the expected files.
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
tar -xzf "$archive" -C "$tmp" reports/neural
rm -rf reports/neural/predictions  # results of the archive being scored, nothing older
mkdir -p reports/neural/predictions
cp "$tmp"/reports/neural/experiment_*.md reports/neural/ 2>/dev/null || true
cp "$tmp"/reports/neural/predictions/*.jsonl "$tmp"/reports/neural/predictions/*.metadata.json \
  reports/neural/predictions/

TM=(uv run --no-sync triggermap)
AGREE=(annotations/batches/batch-03.jsonl)
AGREE_ADD=(--add-gold annotations/batches/batch-06.jsonl)
CRF=reports/agreement/predictions/crf-batches-01-02.jsonl

for pred in reports/neural/predictions/*.jsonl; do
  run=$(basename "$pred" .jsonl)
  "${TM[@]}" evaluate "${AGREE[@]}" "$pred" "${AGREE_ADD[@]}" --split dev \
    --title "Agreement with model drafts: $run" --out "reports/neural/${run}_dev_agreement.md" >/dev/null
  "${TM[@]}" evaluate annotations/pilot/pilot-2.jsonl "$pred" --split dev --gold-origin manual \
    --title "Hand-labelled dev: $run" --out "reports/neural/${run}_dev_manual.md" >/dev/null
done

# Best run per grid by early-stopping score (model-drafted dev), never by the manual slice.
best=$(python3 -I - <<'EOF'
import json
from pathlib import Path
best = {}
for meta in Path("reports/neural/predictions").glob("*.metadata.json"):
    data = json.loads(meta.read_text())
    family = "-".join(data["model_id"].split("-")[:2])  # grid, e.g. deberta-2
    score = data.get("best_dev_typed_f1") or 0.0
    if family not in best or score > best[family][0]:
        best[family] = (score, meta.name.removesuffix(".metadata.json"))
print(" ".join(run for _, run in best.values()))
EOF
)
for run in $best; do
  pred=reports/neural/predictions/$run.jsonl
  "${TM[@]}" compare "${AGREE[@]}" "$CRF" "$pred" "${AGREE_ADD[@]}" --split dev \
    --title "Agreement: crf-batches-01-02 -> $run" --out "reports/neural/compare_agreement_$run.md" >/dev/null
  "${TM[@]}" compare annotations/pilot/pilot-2.jsonl "$CRF" "$pred" --split dev --gold-origin manual \
    --title "Hand-labelled dev: crf-batches-01-02 -> $run" --out "reports/neural/compare_manual_$run.md" >/dev/null
done
echo "best runs: $best"
ls reports/neural
