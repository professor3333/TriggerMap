# Annotation guidelines

**Version 0.2 (post-pilot draft).** Label schema v1 (record schema 1.1), preprocessing version 1.
Version 0.2 resolves the questions raised by the pilot (rules **R1–R8**, cite them in notes). It is
frozen when the revised pilot is imported as `pilot-2` (section 13), and batch annotation follows
it. Every change is recorded in the [changelog](#changelog), and annotations record the guideline
version they followed.

## 1. Goal

A developer reads an advisory for a dependency they use and asks: *does this describe my
deployment?* We mark the text that answers that question: the **conditions** under which a
vulnerable version is actually exposed, whether each condition is required, an exception, or
explicitly unnecessary, and whether conditions must hold **together** or **alternatively**.

Annotate only what the text **explicitly states**. Never add a condition you infer from
background knowledge, however obvious it seems.

## 2. What you annotate

- Annotate the **canonical text** panel ("text"). It is the advisory summary followed by its
  details, with Markdown markup removed (backticks, `#`, list markers, link targets), one line
  per paragraph, heading, list item, table row or code line.
- The **Original Markdown** panel is for reference only (for example, to see list numbering or
  where a code span was). Never annotate there.
- Spans stay within one line of the canonical text.

## 3. What is a condition?

A condition is a statement about the **application, its configuration, its environment or the
attacker** that, according to the text, determines whether the vulnerability can be exploited.

Test: *Could a developer check this against their own deployment, and does the text say it
matters for exposure?* If both answers are yes, it is a condition.

### Not conditions (leave unannotated)

| Kind of text | Example | Why not |
|---|---|---|
| Affected versions | "versions before 3.9.2 are affected" | Version matching is OSV metadata, not a condition. |
| Using the package at all | "applications using Flask" | That is the baseline of every advisory. A specific *mode, feature or function* of the package **is** a condition ("using aiohttp as a web server"). |
| Impact / consequence | "an attacker can read arbitrary files" | Describes what happens, not when. |
| Vulnerability mechanism | "the parser does not validate the path" | Describes the bug, not the deployment. |
| Workaround / mitigation | "disable the option immediately", "upgrade to 2.3.2" | Advice, even if it implies a condition. Annotate the condition only where the text states it as a condition. |
| Generic best practice | "we recommend a reverse proxy" | Not stated as required for exposure. |
| Severity, CVSS, credits, links | "CVSS 7.5", "thanks to …" | Not conditions. |
| Payload construction (R1) | "a ZIP whose entry names do not match", "chains containing duplicate self-signed certificates" | How the attacker builds the input. A developer cannot check their deployment for it. |
| Limits on impact (R6) | "access continues until the session expires" | Bounds how long or how far the impact goes, not whether the application is exposed. |
| Behaviour after the fix | "the patched version now marks it unsafe" | Version matching covers fixed releases. |
| Proof-of-concept specifics | "the PoC listens on port 8002" | Example values, unless the prose says the vulnerability requires them. |
| Unspecified hedges (R4) | "in some circumstances", "under certain configurations" | Names nothing a developer could check. |

## 4. Categories

Choose the category describing **what the developer would check**.

| Category | Use for | Examples |
|---|---|---|
| `CONFIGURATION` | The value of an option, flag, setting, environment variable or config file, including defaults | "follow_symlinks set to True", "SESSION_REFRESH_EACH_REQUEST is enabled", "DEBUG=True" |
| `USAGE` | What the application's code does with the package: functions called, features or modes used, kinds of input processed | "using aiohttp as a web server", "calls yaml.load on untrusted input", "does not access or modify the session" |
| `ACCESS` | What the attacker must have or be: authentication, privileges, network position, ability to upload, victim interaction | "an authenticated user with edit permission", "able to send requests to the server", "the victim opens a crafted link" |
| `PLATFORM` | The environment outside the application code: OS, Python version, hardware, infrastructure, file-system state | "on Windows", "Python 3.7 or earlier", "hosted behind a caching proxy …", "symlinks" in the static directory |

Tie-breakers, in order:
1. A setting of the package or application → `CONFIGURATION`, even if set in code
   (`session.permanent = True`).
2. Something the application's code does or calls → `USAGE`.
3. A property of the attacker → `ACCESS`.
4. Anything about the surrounding environment → `PLATFORM`.

Settled by the pilot:

- **R1. Input.** *What kind of input the application processes* is `USAGE`: "processing
  untrusted images", "parsing certificate chains supplied by clients". The span keeps the
  adjectives inside that noun phrase (`untrusted`, `user-supplied`, `crafted`, `malicious`,
  `invalid`) and stops before clauses that describe how the payload is built ("… containing
  duplicate self-signed certificates" is left out). *The attacker's ability to deliver it* is
  `ACCESS`: "attacker control of the chain input", "can upload files".
- **R2. Request parameters.** An option the attacker sets in their own request
  (`trust_remote_code=true` sent in the request) is attacker capability, `ACCESS`. A server-side
  setting that must *allow* that option is `CONFIGURATION`.
- **R3. Events in the environment.** Something that must happen in the environment (a server
  restart, a scheduled job running, a package being reinstalled) is `PLATFORM`. Something the
  victim must do stays `ACCESS`.

Write a note if none fits well.

## 5. Roles

| Role | Meaning | Cues (not decisive) |
|---|---|---|
| `REQUIRED` | Must hold for the application to be exposed. **Includes required absences.** | when, if, only if, requires, must, as long as |
| `EXCEPTION` | If it holds, the application is **not** exposed (a carve-out). | unless, except, not affected if, safe when |
| `NOT_REQUIRED` | The text **explicitly** says something is *not* needed for exposure. | even if/when … not, need not, no … required, regardless of |
| `UNCERTAIN` | You cannot determine the role from the text. Use sparingly and add a note. | |

### The most important distinction: required absence vs. not required

- "The application **does not set** a Cache-Control header": the absence of the header is
  itself a requirement → `REQUIRED`, and **the negation is inside the span**:
  `does not set a Cache-Control header to indicate that a page is private or should not be cached`.
- "… even when **symlinks are not present**": the author says symlinks are unnecessary →
  `NOT_REQUIRED`, and the span names the thing that is unnecessary **without** the negating
  words: `symlinks`.

Ask: *is the negation part of what must be true (include it, `REQUIRED`), or is it the author
saying something is unnecessary (leave it out, `NOT_REQUIRED`)?*

### Settled by the pilot

- **R4. Hedging.** A hedge on *whether the vulnerability can be exploited* ("may allow", "can
  lead to") does not change any role. A hedge on *whether a stated condition is needed*
  ("mainly dangerous when X", "typically requires X", "in some configurations, such as X") makes
  that condition `UNCERTAIN`, with a note. A hedge that names no checkable condition ("in some
  circumstances") is not annotated.
- **R5. Ineffective protections.** "Even with X enabled", "X does not prevent this",
  "regardless of X": the text says the *absence* of X is not needed. Annotate `X` (without the
  negating words) in its own category with role `NOT_REQUIRED`. Never `EXCEPTION`: X does not
  protect. Example: "restrictive url_fetcher configuration does not prevent exploitation" →
  `restrictive url_fetcher configuration`, CONFIGURATION, NOT_REQUIRED.
- **R6. Exceptions remove exposure, not impact.** `EXCEPTION` is only for something that, if it
  holds, means the application is not exposed at all. Something that only shortens or limits
  the impact (session expiry, rate limits that slow an attack) is not a condition.
- **R7. Variant- and escalation-specific conditions.** When the advisory describes several
  attack variants, or a main vulnerability plus an escalated impact, a condition that the text
  ties to **only one variant or only the escalation** is `UNCERTAIN`. Write a note naming the
  variant ("variant: URL fetch to internal hosts"), and do not group it with conditions of the
  main vulnerability. If the whole advisory is about that variant, its conditions are
  `REQUIRED` as usual. This keeps conditions visible without presenting them as prerequisites
  for every exposure.

## 6. Span boundaries

A span is the **minimal contiguous phrase that fully states the condition**.

Include:
- the predicate and its object or value (`sets session.permanent = True`);
- negation that is part of the requirement (`does not strip cookies`);
- qualifiers that change meaning (`untrusted`, `user-controlled`, `remote`, `with edit permission`);
- quotes or punctuation that belong to an identifier (`'follow_symlinks' is set to True`).

Exclude:
- the conditional cue (`when`, `if`, `unless`, `only if`, `even when`);
- generic subjects (`the application`, `an app`, `users`, `you`) and modals (`must`, `can`);
- parenthetical evidence such as `(the default)`. The default status is useful to the
  reviewer, but it is not part of the condition;
- trailing punctuation.

Splitting:
- Two conditions coordinated with their own predicates ("using X **and** enabling Y") → two
  spans, plus a group (section 7).
- An "or"/"and" **inside one description** ("a caching proxy that does not strip cookies
  **or** ignore responses with cookies", "kernels and terminals disabled or delegated to remote
  hosts") → one span. Rule of thumb: separate spans when a developer would check them separately.

Qualifiers that the text leaves unspecified stay as written. "An authenticated user with
specific data permissions" is one `ACCESS` span. Never add the permission names, character
sets or sizes the text does not give.

References (**R8**):
- When the only statement of a condition uses a reference ("the variable is not set", "that
  page") and the referent is named **earlier in the same paragraph**, annotate the phrase as
  written and name the referent in a note ("the variable = A2U_AUTH_TOKEN").
- When the referent is outside the paragraph, annotate the phrase with role `UNCERTAIN`.
- When the condition is also stated with its name elsewhere, annotate both statements (see
  Repetition below).

Code:
- Annotate inside code only when the prose presents the code as the vulnerable setup
  ("only vulnerable with setup code like:"). Mark the smallest token sequence that carries
  the condition (`follow_symlinks=True`), on one line.

Repetition:
- Annotate **every explicit statement** of a condition, even if an earlier sentence said
  the same thing. Merging duplicates into one checklist item is a later, automatic step.

## 7. Groups

Group conditions only when the text **explicitly** states their logic **within one sentence or
one list block**. A list block includes its lead-in sentence.

| Operator | When | Example |
|---|---|---|
| `ALL` | All must hold together | "When using X **and** enabling Y with Z", "**all of the following** conditions" |
| `ANY` | Any one suffices | "if X **or** Y", "**either** …", "**one of** the following" |
| `UNRESOLVED` | Clearly connected, but the logic is unclear or nested | "X and Y or Z" |

Rules:
- Do not group a single condition.
- Do not group across paragraphs or headings, or conditions that merely appear in neighbouring
  sentences without an explicit connective.
- Each condition belongs to at most one group. If you would need nested groups, put all the
  members in one `UNRESOLVED` group and add a note.
- Exceptions can form groups: "unless X or Y" → X and Y are `EXCEPTION`, grouped `ANY`.

**In Label Studio:** select one condition, then create a relation to another and set its
label (`ALL`/`ANY`/`UNRESOLVED`). All linked conditions form one group, so a three-member
group needs two links (c1–c2, c2–c3). Every link within a group must carry the same label.

## 8. Document status

| Status | When |
|---|---|
| `HAS_CONDITIONS` | At least one condition is annotated. |
| `NO_EXPLICIT_CONDITION` | The text states no condition beyond using an affected version. Typical: "X before 1.2 allows remote attackers to …". |
| `UNSUPPORTED_STRUCTURE` | Conditions exist but cannot be represented: nested logic that `UNRESOLVED` would hide, conditions that only make sense across paragraphs, or conditions only in a table. Annotate whatever spans you can, and add a note. |

"No explicit condition" never means "not vulnerable". It means the text does not say.

## 9. Worked examples

These examples apply the rules above. They are proposals to confirm or change during the pilot.

**aiohttp, GHSA-5h86-8mv2-jq9f, Impact section**

> When using aiohttp as a web server and enabling static resource resolution with
> follow_symlinks set to True, it can lead to this vulnerability.

| Span | Category | Role |
|---|---|---|
| `using aiohttp as a web server` | USAGE | REQUIRED |
| `enabling static resource resolution` | USAGE | REQUIRED |
| `follow_symlinks set to True` | CONFIGURATION | REQUIRED |

Group: `ALL` (c1, c2, c3).

> … resulting in unauthorized access to arbitrary files on the system, even when symlinks
> are not present.

`symlinks` → PLATFORM, NOT_REQUIRED. "unauthorized access to arbitrary files" is impact and
is not annotated.

> If using follow_symlinks=True outside of a restricted local development environment,
> disable the option immediately.

A workaround: no annotation.

**Flask, GHSA-m2qf-hxjv-5gpq**

> When all of the following conditions are met, … The risk depends on all these conditions
> being met.
> 1. The application must be hosted behind a caching proxy that does not strip cookies or
>    ignore responses with cookies.
> 2. The application sets session.permanent = True.
> 3. The application does not access or modify the session at any point during a request.
> 4. SESSION_REFRESH_EACH_REQUEST is enabled (the default).
> 5. The application does not set a Cache-Control header to indicate that a page is private
>    or should not be cached.

| Span | Category | Role |
|---|---|---|
| `hosted behind a caching proxy that does not strip cookies or ignore responses with cookies` | PLATFORM | REQUIRED |
| `sets session.permanent = True` | CONFIGURATION | REQUIRED |
| `does not access or modify the session at any point during a request` | USAGE | REQUIRED |
| `SESSION_REFRESH_EACH_REQUEST is enabled` | CONFIGURATION | REQUIRED |
| `does not set a Cache-Control header to indicate that a page is private or should not be cached` | USAGE | REQUIRED |

Group: `ALL` over all five. The lead-in "all of the following conditions" is part of the list
block.

## 10. Mechanical normalisation

The importer trims whitespace at span edges and reports each trim. It never changes a label,
a role, a group or any non-whitespace boundary. Every other problem (a span that does not
match its text, a missing role, contradictory links, a status that disagrees with the spans) is
reported back for you to fix in Label Studio.

## 11. Notes

Use the notes box whenever you hesitate: an unclear category, a borderline workaround, a span
boundary you are unsure of. Notes are reviewed after the pilot to revise these guidelines.

## 12. Unsupported classes (pilot gate)

The pilot gate (`docs/pilot_gate.md`, regenerated with `triggermap annotate gate`) projects each
role and group operator to the planned 800 documents. Classes projected below 50 examples are
**unsupported**:

| Class | Pilot gate result | What it means |
|---|---|---|
| `UNCERTAIN` | unsupported | Keep annotating as before. Models do not claim it; it is a *Review required* state. |
| `ANY` | unsupported | Keep annotating. Predicted `ANY` groups are shown for review, and results are reported as low-support. |
| `UNRESOLVED` | unsupported | Keep annotating; always *Review required*. |
| `EXCEPTION` | supported in training only | No exceptions occurred in the natural pilot documents, so dev/test support will be very small. Training examples come from enriched batches. |

Unsupported means *too few examples to learn or measure*, not *removed*. Never invent or
adapt examples to fill a class.

## 13. Migrating the pilot to v0.2

`pilot-1` was labelled under v0.1 and stays as it is. Before batch-01:

1. In Label Studio, re-check every pilot task that R1–R8 could affect: any note or draft review
   flag about crafted input, ineffective protections, hedging, impact-specific or
   variant-specific conditions, request parameters, lifecycle events or references. Edit,
   resubmit, and cite the rule in the note ("R5").
2. Export and import as a new version:
   `triggermap annotate import data/label_studio/export.json --annotator A1 --annotation-version pilot-2 --out annotations/pilot/pilot-2.jsonl`.
3. Regenerate the gate (`triggermap annotate gate --gold annotations/pilot/pilot-2.jsonl --export data/label_studio/export.json`).
   Version 0.2 is frozen at that point.

## Changelog

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-10-20 | Pilot draft. |
| 0.2 | 2026-11-02 | Post-pilot draft. R1 input vs payload construction; R2 attacker-set request parameters are ACCESS; R3 environment events are PLATFORM; R4 hedging; R5 ineffective protections are NOT_REQUIRED; R6 exceptions remove exposure, not impact; R7 variant/escalation-specific conditions are UNCERTAIN; R8 references. New "not conditions" rows, unspecified qualifiers, unsupported classes from the pilot gate (UNCERTAIN, ANY, UNRESOLVED), pilot migration to `pilot-2`. |
