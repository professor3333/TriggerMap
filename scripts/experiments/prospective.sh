#!/usr/bin/env bash
# Prospective check: how the frozen models behave on advisories published after the snapshot.
#
#   bash scripts/experiments/prospective.sh [DEBERTA_BUNDLE_DIR]
#
# 1. Fetches github/advisory-database at PROSPECTIVE_COMMIT into its own directory (the pinned
#    snapshot in data/raw/advisory-database is not touched) and builds that corpus into
#    data/processed/prospective (manifest: reports/prospective/snapshot-<sha8>.json).
# 2. Selects advisories whose id is absent from the pinned corpus and that were published after
#    the pinned snapshot's commit date -> reports/prospective/prospective-1.json.
# 3. Predicts them with the released CRF (live review policy) and, if a bundle is given, the
#    run-3 DeBERTa. As a reference it also predicts the 272 dev documents of batch-03, batch-06
#    and batch-07 with the same CRF and policy.
# 4. Writes reports/prospective/summary.md: input and output statistics, prospective against
#    dev. There are no labels, so there is no accuracy or agreement here, only behaviour.
# Finished prediction files are reused. The test split is not used.
set -euo pipefail
[ -f pyproject.toml ] && [ -d annotations ] || { echo "run from the repository root" >&2; exit 1; }
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-2} MKL_NUM_THREADS=${MKL_NUM_THREADS:-2}
export TOKENIZERS_PARALLELISM=false

PROSPECTIVE_COMMIT=9b0169eb7fb17b26d940fbcc7cdd6f2e88bebd37
RAW=data/raw/advisory-database-prospective
PROCESSED=data/processed/prospective
OUT=reports/prospective
SNAP_MANIFEST=$OUT/snapshot-${PROSPECTIVE_COMMIT:0:8}.json
DEB=deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2
DEV_SAMPLES=(annotations/batches/batch-03.json annotations/batches/batch-06.json annotations/batches/batch-07.json)
TM=(uv run --no-sync triggermap)
mkdir -p "$OUT/predictions"

"${TM[@]}" ingest fetch --dest "$RAW" --commit "$PROSPECTIVE_COMMIT"
[ -s "$PROCESSED/advisories.jsonl" ] || "${TM[@]}" ingest build --snapshot "$RAW" --out "$PROCESSED" --manifest "$SNAP_MANIFEST"

uv run --no-sync python -I - "$PROCESSED" "$SNAP_MANIFEST" "$OUT/prospective-1.json" <<'EOF'
import json, sys
from pathlib import Path
from triggermap.ingest.build import load_corpus
processed, snap_manifest, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
pinned = {d.advisory_id for d in load_corpus(Path("data/processed/advisories.jsonl"))}
newer = {d.advisory_id: d for d in load_corpus(processed / "advisories.jsonl")}
snap = json.loads(Path("data/manifests/snapshot.json").read_text())
newsnap = json.loads(snap_manifest.read_text())
cutoff = snap["source"]["commit_date"]
ids = sorted(a for a, d in newer.items() if a not in pinned and d.published > cutoff)
items = [
    {"advisory_id": a, "content_hash": newer[a].content_hash, "published": newer[a].published,
     "words": len((newer[a].summary + " " + newer[a].details).split()), "intended_use": "prospective"}
    for a in ids
]
manifest = {
    "sample_version": "prospective-1",
    "params": {"rule": "advisory id absent from the pinned corpus and published after the pinned "
               "snapshot's commit date", "pinned_commit": snap["source"]["commit"], "cutoff": cutoff},
    "source_commit": newsnap["source"]["commit"],
    "source_commit_date": newsnap["source"]["commit_date"],
    "corpus_sha256": newsnap["outputs"]["advisories.jsonl"],
    "counts": {"prospective": len(items)},
    "items": items,
}
out.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
print(f"wrote {out} ({len(items)} advisories)")
EOF

predict() {  # <out file> <predict args...>
  local out=$1
  shift
  [ -s "$out" ] && { echo "reusing $out"; return; }
  "${TM[@]}" predict "$@" --out "$out"
}
predict "$OUT/predictions/crf-batches-01-02.jsonl" --model crf --model-dir artifacts/crf-batches-01-02 \
  --processed "$PROCESSED" --sample "$OUT/prospective-1.json" --review-policy configs/review_policy.yaml
predict "$OUT/predictions/crf-batches-01-02_dev.jsonl" --model crf --model-dir artifacts/crf-batches-01-02 \
  --sample "${DEV_SAMPLES[@]}" --review-policy configs/review_policy.yaml
if [ -n "${1:-}" ]; then
  predict "$OUT/predictions/$DEB.jsonl" --model transformer --model-dir "$1" \
    --processed "$PROCESSED" --sample "$OUT/prospective-1.json"
fi

uv run --no-sync python -I - "$OUT" "$PROCESSED" "$DEB" "${1:-}" "${DEV_SAMPLES[@]}" <<'EOF'
import json, re, statistics, sys
from collections import Counter
from pathlib import Path
from triggermap.ingest.build import load_corpus
out, processed, deb, bundle, dev_samples = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5:]

def load(path):
    rows = (json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines())
    return {r["advisory_id"]: r for r in rows}

prosp_ids = [i["advisory_id"] for i in json.loads((out / "prospective-1.json").read_text())["items"]]
dev_ids = [i["advisory_id"] for s in dev_samples for i in json.loads(Path(s).read_text())["items"]]
docs = {d.advisory_id: d for d in load_corpus(processed / "advisories.jsonl") if d.advisory_id in set(prosp_ids)}
docs |= {d.advisory_id: d for d in load_corpus(Path("data/processed/advisories.jsonl")) if d.advisory_id in set(dev_ids)}

def text_stats(ids):
    words = [len((docs[a].summary + " " + docs[a].details).split()) for a in ids]
    lists = sum(bool(re.search(r"(?m)^\s*(?:[-*+]|\d+[.)])\s+\S", docs[a].details or "")) for a in ids)
    fences = sum("```" in (docs[a].details or "") for a in ids)
    return {"documents": len(ids), "median words": statistics.median(words),
            "mean words": round(statistics.mean(words)), "with a Markdown list": lists / len(ids),
            "with a fenced code block": fences / len(ids)}

def pred_stats(pred, ids):
    rows = [pred[a] for a in ids if a in pred]
    conds = [c for r in rows for c in r["conditions"]]
    status = Counter(r["document_status"] for r in rows)
    n = len(rows)
    out = {"documents": n,
           "no explicit conditions found": status["NO_EXPLICIT_CONDITION"] / n,
           "unsupported structure": status["UNSUPPORTED_STRUCTURE"] / n,
           "conditions per document": len(conds) / n,
           "groups per document": sum(len(r["groups"]) for r in rows) / n}
    for role, k in Counter(c["role"] for c in conds).most_common():
        out[f"role {role}"] = k / len(conds)
    for cat, k in Counter(c["category"] for c in conds).most_common():
        out[f"category {cat}"] = k / len(conds)
    confs = [c["confidence"] for c in conds if c.get("confidence") is not None]
    if confs:
        out["median confidence"] = statistics.median(confs)
    reasons = Counter(f.split(":")[2] for r in rows for f in r["review_flags"] if f.count(":") >= 2)
    for reason, k in reasons.most_common():
        out[f"review reason {reason} (per condition)"] = k / max(len(conds), 1)
    return out

def fmt(v):
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, float):
        return f"{v:.3f}" if v < 1 else f"{v:.2f}"
    return str(v)

def table(title, left, right, names):
    keys = list(dict.fromkeys([*left, *right]))
    lines = [f"## {title}", "", f"| | {names[0]} | {names[1]} |", "|---|---:|---:|"]
    lines += [f"| {k} | {fmt(left.get(k, 0.0))} | {fmt(right.get(k, 0.0))} |" for k in keys]
    return lines + [""]

train_ids = set()
for f in ("annotations/pilot/pilot-2.jsonl", "annotations/batches/batch-01.jsonl", "annotations/batches/batch-02.jsonl"):
    for line in Path(f).read_text().splitlines():
        train_ids.add(json.loads(line)["advisory_id"])
pinned = {d.advisory_id: d for d in load_corpus(Path("data/processed/advisories.jsonl")) if d.advisory_id in train_ids}
train_packages = {p for d in pinned.values() for p in d.pypi_packages}
shared = sum(bool(set(docs[a].pypi_packages) & train_packages) for a in prosp_ids)

lines = ["# Prospective check: summary", "",
         "Generated by `scripts/experiments/prospective.sh`. No labels: behaviour only.", "",
         f"- New advisories sharing a PyPI package with an annotated pilot/batch-01/batch-02 record: "
         f"{shared} of {len(prosp_ids)}", ""]
lines += table("Input text", text_stats(prosp_ids), text_stats(dev_ids), ("prospective", "dev (272)"))
periods: dict[str, list[int]] = {}
for d in load_corpus(Path("data/processed/advisories.jsonl")):
    year = d.published[:4]
    key = year if year < "2025" else f"{year}-{'H1' if d.published[5:7] < '07' else 'H2'}"
    periods.setdefault(key, []).append(len((d.summary + " " + d.details).split()))
periods = dict(sorted(periods.items()))
periods["prospective (2026-10-20 to 2026-11-14)"] = [
    len((docs[a].summary + " " + docs[a].details).split()) for a in prosp_ids
]
lines += ["## Advisory length by publication date (pinned corpus, then the prospective batch)", "",
          "| Published | Advisories | Median words |", "|---|---:|---:|"]
lines += [f"| {k} | {len(v)} | {statistics.median(v):g} |" for k, v in periods.items()]
lines.append("")
if bundle:
    from transformers import AutoTokenizer
    from triggermap.text.preprocessing import compose_raw, preprocess
    tok = AutoTokenizer.from_pretrained(Path(bundle) / "tokenizer")
    lines += ["## Length in DeBERTa tokens (canonical text, no special tokens)", "",
              "| | prospective | dev (272) |", "|---|---:|---:|"]
    stats = {}
    for name, ids in (("prospective", prosp_ids), ("dev", dev_ids)):
        n = [len(tok(preprocess(compose_raw(docs[a].summary, docs[a].details)).text,
                     add_special_tokens=False)["input_ids"]) for a in ids]
        stats[name] = (statistics.median(n), sum(x > 510 for x in n) / len(n), sum(x > 2000 for x in n) / len(n))
    for i, label in enumerate(("median tokens", "more than one 512-token window", "more than 2,000 tokens")):
        lines.append(f"| {label} | {fmt(float(stats['prospective'][i]))} | {fmt(float(stats['dev'][i]))} |")
    lines.append("")
crf_p, crf_d = load(out / "predictions/crf-batches-01-02.jsonl"), load(out / "predictions/crf-batches-01-02_dev.jsonl")
lines += table("CRF crf-batches-01-02 (review-policy-0)", pred_stats(crf_p, prosp_ids), pred_stats(crf_d, dev_ids),
               ("prospective", "dev (272)"))
deb_file = out / f"predictions/{deb}.jsonl"
if deb_file.exists():
    deb_dev = {**load(f"reports/neural/run-3/predictions/{deb}.jsonl"),
               **load(f"reports/batch-07-comparison/predictions/{deb}.jsonl")}
    lines += table("DeBERTa run 3 (no review policy)", pred_stats(load(deb_file), prosp_ids),
                   pred_stats(deb_dev, dev_ids), ("prospective", "dev (272)"))
(out / "summary.md").write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {out / 'summary.md'}")
EOF
