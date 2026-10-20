# Annotations

Condition-level annotations of security advisories from the
[GitHub Advisory Database](https://github.com/github/advisory-database).

## License and attribution

The advisory text is © its respective authors and GitHub, published in the GitHub Advisory
Database under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The annotations in this
directory are derived from that text. They are **modified material**: condition spans,
categories, roles, groups and document status were added by the TriggerMap project. They are
released under CC BY 4.0.

Each record carries its advisory ID (link: `https://github.com/advisories/<advisory_id>`), the
advisory-database commit it was taken from, and the SHA-256 of the annotated text.

## Contents

| Path | What |
|---|---|
| `pilot/pilot_manifest.json` | The 100-document pilot sample: IDs, strata, project groups, hashes. |
| `pilot/pilot-1.jsonl` | Pilot annotations (once imported). One `AdvisoryAnnotation` per line. |

Records follow the schema in `src/triggermap/schema/models.py` and the rules in
`docs/annotation_guidelines.md`.
