# TriggerMap

**Security advisories → evidence-linked exposure checklists.**

> Status: early development (Phase 1, feasibility). Nothing below the roadmap line is
> implemented yet; this README only describes features that exist.

A vulnerability alert tells you a dependency is affected. The advisory prose tells you *when*:
an optional feature must be enabled, a particular function used, the attacker already
authenticated, or several conditions must hold together. TriggerMap extracts those conditions
from English advisories for Python (PyPI) packages, classifies each one as a prerequisite,
an exception, or an explicitly unnecessary condition, keeps their ALL/ANY grouping, and links
every checklist item to the exact source text so a developer can verify it.

It complements dependency scanners such as
[OSV-Scanner](https://github.com/google/osv-scanner): the scanner says *which* dependency is
affected; TriggerMap surfaces the *conditions* stated in the advisory.

## Data

Advisories come from the public [GitHub Advisory Database](https://github.com/github/advisory-database)
(CC BY 4.0). Attribution, the pinned snapshot commit and measured counts will be documented in
`docs/dataset_card.md`.

## Development

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pytest
```
