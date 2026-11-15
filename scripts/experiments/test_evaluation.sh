#!/usr/bin/env bash
# Declared, one-time evaluation on the locked test split.
#
#   bash scripts/experiments/test_evaluation.sh "<reason declared by the owner>"
#
# Scores the frozen predictions in reports/test-evaluation/predictions/ (rules-2, the CRF
# crf-batches-01-02 of v0.1.0, the run-3 DeBERTa of model-deberta-3-run3) on the test split of
# pool-v1, in two slices:
#   - agreement: the 146 model-drafted test records (batch-04 and pilot-2; subset file
#     model_drafted_test_ids.json). These measure agreement with the drafting model, not accuracy;
#   - accuracy: the 4 hand-labelled test records (`--gold-origin manual`).
# Then paired comparisons: CRF vs DeBERTa and CRF vs rules-2, on both slices.
# Every run is appended to docs/test-access-log.md with the reason. Run it only for a declared
# release evaluation; nothing may be tuned on these results.
set -euo pipefail
[ -f pyproject.toml ] && [ -d annotations ] || { echo "run from the repository root" >&2; exit 1; }
REASON=${1:?usage: test_evaluation.sh "<declared reason>"}

TM=(uv run --no-sync triggermap)
OUT=reports/test-evaluation
P=$OUT/predictions
GOLD=(annotations/batches/batch-04.jsonl --add-gold annotations/pilot/pilot-2.jsonl)
TEST=(--split test --release-evaluation "$REASON")
AGREE=(--subset "$OUT/model_drafted_test_ids.json")
MANUAL=(--gold-origin manual)
CRF=crf-batches-01-02
DEB=deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2

for model in rules-2 "$CRF" "$DEB"; do
  "${TM[@]}" evaluate "${GOLD[0]}" "$P/$model.jsonl" "${GOLD[@]:1}" "${TEST[@]}" "${AGREE[@]}" \
    --title "Test split, agreement with 146 model-drafted records: $model" --out "$OUT/${model}_agreement.md"
  "${TM[@]}" evaluate "${GOLD[0]}" "$P/$model.jsonl" "${GOLD[@]:1}" "${TEST[@]}" "${MANUAL[@]}" \
    --title "Test split, 4 hand-labelled records: $model" --out "$OUT/${model}_manual.md"
done
for other in "$DEB" rules-2; do
  "${TM[@]}" compare "${GOLD[0]}" "$P/$CRF.jsonl" "$P/$other.jsonl" "${GOLD[@]:1}" "${TEST[@]}" "${AGREE[@]}" \
    --title "Test split, agreement (146): $other minus $CRF" --out "$OUT/compare_agreement_$other.md"
  "${TM[@]}" compare "${GOLD[0]}" "$P/$CRF.jsonl" "$P/$other.jsonl" "${GOLD[@]:1}" "${TEST[@]}" "${MANUAL[@]}" \
    --title "Test split, hand-labelled (4): $other minus $CRF" --out "$OUT/compare_manual_$other.md"
done
