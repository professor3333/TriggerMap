#!/usr/bin/env bash
# Build the static demo pages in demo/ (published with GitHub Pages by .github/workflows/pages.yml).
#
#   bash scripts/demo/build_site.sh
#
# Renders three advisories with the released CRF (crf-batches-01-02, v0.1.0) and the live review
# policy, using the same renderer as `triggermap view`: an ordinary case (aiohttp), a hard scope
# case (Flask) and an abstention (Django). demo/index.html is written by hand. The script needs
# the local corpus (`ingest build`) and the CRF bundle, and stops if the bundle is not the
# released one. All three advisories are in the dev split; none was used to train the CRF.
set -euo pipefail
[ -f pyproject.toml ] && [ -d annotations ] || { echo "run from the repository root" >&2; exit 1; }

BUNDLE=artifacts/crf-batches-01-02
TAGGER_SHA256=d1f8cb5a94b0ba4540c585d902543e13e8b4252b9c21891f29bf6381b0c07056
CLASSIFIERS_SHA256=e7360d775bb2fa7c84557a4ab8fdaa7dc99bbf730ac290d46a860b9582c38c3c
POLICY=configs/review_policy.yaml
OUT=demo
CASES=(aiohttp:GHSA-5h86-8mv2-jq9f flask:GHSA-m2qf-hxjv-5gpq django:GHSA-xgxc-v2qg-chmh)

uv run --no-sync python -I - "$BUNDLE" "$TAGGER_SHA256" "$CLASSIFIERS_SHA256" <<'EOF'
import hashlib, sys
from pathlib import Path
bundle, tagger, classifiers = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
for name, want in (("tagger.crfsuite", tagger), ("classifiers.joblib", classifiers)):
    got = hashlib.sha256((bundle / name).read_bytes()).hexdigest()
    assert got == want, f"{bundle / name}: {got} is not the released bundle ({want})"
EOF

mkdir -p "$OUT"
for case in "${CASES[@]}"; do
  uv run --no-sync triggermap view "${case#*:}" --model crf --model-dir "$BUNDLE" \
    --review-policy "$POLICY" --out "$OUT/${case%%:*}.html"
done

uv run --no-sync python -I - "$OUT" "$POLICY" "${CASES[@]}" <<'EOF'
import json, subprocess, sys
from pathlib import Path
out, policy, cases = Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
snapshot = json.loads(Path("data/manifests/snapshot.json").read_text())
version = next(
    line.split(":", 1)[1].strip()
    for line in Path(policy).read_text().splitlines()
    if line.startswith("version:")
)
record = {
    "built_from_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    "model": "crf-batches-01-02 (release v0.1.0)",
    "review_policy": version,
    "preprocessing_version": snapshot["preprocessing_version"],
    "advisory_snapshot_commit": snapshot["source"]["commit"],
    "pages": {c.split(":")[0] + ".html": c.split(":")[1] for c in cases},
    "license": "Advisory text: GitHub Advisory Database, CC BY 4.0, shown with display markup "
    "removed and condition highlights added. Code: MIT.",
}
(out / "provenance.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
print(f"wrote {out}/provenance.json")
EOF
