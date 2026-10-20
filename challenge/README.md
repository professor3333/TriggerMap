# Challenge set

Small, constructed advisories that probe the errors that matter most: reversed meaning and
invented prerequisites. The set is **kept separate from the real-advisory test set** and
always reported on its own, never pooled with real-data scores.

| Family | What it probes |
|---|---|
| `negation_flip` | "when X is enabled" vs "even when X is not enabled" |
| `required_vs_unnecessary` | a required absence vs a condition the text says is unnecessary |
| `conjunction_flip` | "A and B" (ALL) vs "A or B" (ANY) |
| `prerequisite_vs_workaround` | a stated condition vs advice to disable the same feature |
| `paraphrase_no_cue` | conditions stated without "if/when/unless" |
| `formatting` | the same content in different Markdown |

Items related by a single edit share a `pair` id. Scoring reports how many pairs are fully
correct on *both* sides, which is the real test of scope handling.

## Authoring

One JSON object per line in `challenge_set.jsonl`. Conditions are written as **surface
strings**; `occurrence` picks the n-th match when a surface repeats. Loading resolves each
surface to canonical offsets and fails on a missing surface.

```json
{"id": "neg-01a", "family": "negation_flip", "pair": "neg-01", "status": "draft",
 "text": "The server is vulnerable when `debug` is enabled.",
 "conditions": [{"surface": "debug is enabled", "category": "CONFIGURATION", "role": "REQUIRED"}],
 "groups": []}
```

Rules:

- Labels follow `docs/annotation_guidelines.md`. Items are written after guidelines v0.2 is
  frozen, so they test the same rules the gold data uses.
- New items start as `"status": "draft"`. Only items checked by hand and set to `"verified"`
  are scored; drafts appear in a separate, unverified table.
- Never copy text from test-pool advisories.

```bash
uv run triggermap challenge --model rules      # → reports/challenge/rules-2.md
```
