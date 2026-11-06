# Model card: TriggerMap condition extractors

**Status (2026-11-06): v0.1.0 is a preview release** of `crf-batches-01-02` with the uncalibrated
review policy ([release notes](release_notes/v0.1.0.md)). No system has been through a release
evaluation. Labels after the pilot are model drafts
(owner's decision, 2026-11-05), and the release gates need hand-labelled test records, so the
gates cannot currently be judged as declared. Every number on this page is a preliminary
dev-split measurement, not a release result. Release gates are in [`targets.md`](targets.md).

## Intended use

TriggerMap extracts configuration, usage, access and platform conditions from English
advisories for PyPI packages, together with each condition's role and explicit `ALL`/`ANY`
groups. Each extraction becomes a *suggested* checklist item, linked to its source evidence. A
reviewer confirms or corrects every item before export.

## Not for

- deciding that an application is or is not vulnerable without human review;
- automatically suppressing, closing or prioritising alerts from unreviewed output;
- treating "no explicit conditions found" as "not affected";
- inferring conditions that the advisory does not state;
- other ecosystems, non-English text, linked external pages or PDF input;
- replacing dependency and version matching (for example OSV-Scanner).

## Systems

| System | What it is | Status |
|---|---|---|
| `rules-2` | Deterministic cue rules over the shared preprocessing (no learning) | Runs; 100% formatting-consistent on 300 documents |
| CRF | `python-crfsuite` BIO span tagger with logistic-regression category, role and group classifiers. Features `crf-features-1`, optional spaCy part-of-speech tags | Trained on pilot data only |
| DistilBERT | `distilbert/distilbert-base-cased` (Apache-2.0), revision `6ea81172465e8b0ad3fddeed32b986cdcdcffcf0` | Run 3: held-out agreement typed F1 0.099 (CRF 0.127), [`reports/neural/run-3/`](../reports/neural/run-3/README.md) |
| DeBERTa-v3-small | `microsoft/deberta-v3-small` (MIT), revision `a36c739020e01763fe789b4b85e2df55d6180012` | Run 3: held-out agreement typed F1 0.185, false-prerequisite rate 0.483 (CRF 0.127 / 0.412; differences not clear), [`reports/neural/run-3/`](../reports/neural/run-3/README.md) |

The transformer models share one design:
- the encoder is fine-tuned, never pretrained;
- a BIO span head sits on the encoder;
- span-pooled category and role classifiers, plus a pairwise group classifier within a
  sentence or list block;
- 512-token windows with a 64-token stride, the governing heading or list lead-in prepended,
  and predictions merged by source offsets.

The configs are in `configs/experiments/`. All systems end in the same deterministic validator,
which rejects invalid offsets, dangling group members and contradictory groups.

## Provenance

Every bundle's `metadata.json` records:
- the model id;
- the preprocessing and feature versions;
- hyperparameters and seed;
- the training-record hash and count;
- the label origins of the training records (`training_origins`);
- label counts.

Transformer bundles also record:
- the base revision;
- the split-manifest hash;
- per-epoch dev metrics, training time and peak GPU memory.

A release manifest (`triggermap release create`) adds the image digest, the weights digest and
the review-policy version.

## Training data

Training uses the train pool of `splits/pool-v1.json` only (see
[`dataset_card.md`](dataset_card.md)). The models trained so far used `pilot-2` (39 in the
train split) and `batch-01` (100). Of these 139 records, 7 are `manual`. The other 132 are
model drafts. `crf-batches-01-02` adds `batch-02` (239 records: 7 `manual`, 232 model drafts).
Its dev results, as agreement with the model drafts and as accuracy on the 10 hand-labelled
documents, are in [`reports/agreement/`](../reports/agreement/README.md).

## Preliminary dev results

These are measured on the **10 hand-labelled dev documents** (17 gold conditions). The intervals
are 95% project-group bootstrap intervals from 1,000 resamples.

| System | Typed-condition micro-F1 | False-prerequisite rate |
|---|---:|---:|
| `rules-2` | 0.095 [0.000, 0.333] | 0.750 [0.000, 1.000] |
| `crf-pilot-2` (39 training records) | 0.231 [0.062, 0.417] | 0.444 [0.000, 0.667] |
| `crf-pilot-2-batch-01` (139 training records) | 0.444 [0.133, 0.667] | 0.300 [0.000, 0.750] |

None of the paired differences is clear at this sample size. Sources:
[`reports/pilot/`](../reports/pilot/README.md) and
[`reports/training-origin/`](../reports/training-origin/README.md). Serving-cost measurements
from a local proxy are in [`benchmarks.md`](benchmarks.md). They do not count toward the
target-host gates.

## Metrics

Metric definitions are in [`evaluation.md`](evaluation.md).
- **Primary:** typed-condition micro-F1.
- **Also reported:**
  - exact span P/R/F1;
  - role macro-F1, with per-class support;
  - group exact match;
  - complete-document exact match, with and without conditions;
  - false-prerequisite and reversed-meaning rates;
  - precision against coverage, with retained recall;
  - calibration error.

## Known failure modes

These are expected from the guidelines. [`error_catalogue.md`](error_catalogue.md) lists the
disagreements of `crf-batches-01-02` with the 172 model-drafted dev records (agreement, not
accuracy): 265 missed conditions, 59 invented prerequisites, 50 boundary errors, 16 group
errors, 13 category errors, 13 spurious conditions, 9 reversed meanings and 7 role errors. A
catalogue against hand-labelled gold needs a release candidate and hand-labelled records.

- **Negation scope:** a required absence confused with not required.
- **Impact read as a prerequisite:** consequences or impact taken as conditions.
- **Workarounds read as conditions:** workaround or mitigation language taken as conditions.
- **Coordination:** `ALL` and `ANY` confused ("A and B", "A or B", "either").
- **Lost list scope:** the heading or lead-in sets the logic, and the scope is lost.
- **Cross-sentence references:** "this option", "in that case".
- **Unseen identifiers:** flags, method names and paths split by subword tokenisation.
- **Default-on settings dropped.**
- **Code blocks and hedging:** conditions stated only in code blocks, or hedged.
- **Window boundaries:** structure that crosses a window boundary.
- **Span boundaries:** boundary errors on modifiers and multiword feature names.

## Calibration and default model

Confidence calibration (Platt scaling) and review thresholds were fitted on the selection half
of the model-drafted dev records and measured on the held-out half
([`reports/calibration/`](../reports/calibration/README.md)):
- **Calibration error (ECE):** falls from 0.305 to 0.101 for the CRF and from 0.548 to 0.059
  for DeBERTa.
- **At matched review thresholds:** DeBERTa keeps two to three times as many agreeing
  conditions, but it is not clearly more precise and does not invent fewer prerequisites.

The default model is therefore still the CRF. The live review policy stays
`review-policy-0` (uncalibrated: every prediction is flagged), because thresholds fitted on
model drafts measure agreement, not accuracy.

## Release process

- **Thresholds.** Review thresholds and confidence cut-offs are chosen on the dev calibration
  half (`triggermap calibrate`), never on test.
- **Promotion.** A candidate is promoted only when it meets every gate in
  [`targets.md`](targets.md) in a declared test evaluation, logged in `docs/test-access-log.md`.
  Its release manifest records the gates, the reason and the release it replaces.
- **Rollback.** Rollback restores the complete previous bundle and image
  ([`deployment.md`](deployment.md)). The rollback drill is tested.
- **Preview releases.** While the gates cannot be judged, a release is marked *preview*. Its
  notes state that no gate was evaluated, and every prediction is flagged for review. v0.1.0
  is the first ([release notes](release_notes/v0.1.0.md)).
