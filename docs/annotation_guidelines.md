# Annotation guidelines

**Version 0.1 (pilot draft).** Label schema v1, preprocessing version 1.
These rules are tested by the 100-document pilot and will change. Every change is recorded in
the [changelog](#changelog), and annotations record the guideline version they followed.

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

Write a note if none fits well. The pilot will tell us whether the categories need changing.

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
  **or** ignore responses with cookies") → one span. Rule of thumb: separate spans when a
  developer would check them separately.

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

## Changelog

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-10-20 | Pilot draft. |
