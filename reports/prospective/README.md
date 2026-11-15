# Prospective check: newly published advisories (behaviour only)

This check runs the frozen models on advisories that **did not exist** when the corpus was
pinned. It asks how the models behave on genuinely new text. There are no labels for these
advisories, and none will be made, so this report has **no accuracy or agreement numbers**. It
describes the input and the output, and compares both with the 272 dev documents of
`batch-03`, `batch-06` and `batch-07`.

## The prospective batch

- **Source:** `github/advisory-database` at commit `9b0169eb7fb17b26d940fbcc7cdd6f2e88bebd37`
  (2026-11-15). The corpus was built with the same pipeline into its own paths; its manifest is
  [`snapshot-9b0169eb.json`](snapshot-9b0169eb.json). The pinned snapshot `1912cbd6` was not
  changed.
- **Selection** ([`prospective-1.json`](prospective-1.json), frozen): PyPI advisories whose id
  is absent from the pinned corpus and that were published after the pinned snapshot's commit
  date (2026-10-20T03:38:30Z). That gives **259 advisories**, published 2026-10-20 → 2026-11-14.
  Seven advisories that newly joined the reviewed PyPI set but were published earlier are left
  out. Four ids from the pinned corpus no longer appear in the newer snapshot.
- **Overlap:** 141 of the 259 share a PyPI package with an annotated `pilot-2`, `batch-01` or
  `batch-02` record, so this is new text, but often from known projects.
- **Systems:** the CRF `crf-batches-01-02` (v0.1.0, with the live review policy
  `review-policy-0`) and the run-3 DeBERTa (`model-deberta-3-run3`), both unchanged.

Reproduce with `bash scripts/experiments/prospective.sh [DEBERTA_BUNDLE_DIR]`. All tables:
[`summary.md`](summary.md).

## The input has shifted: new advisories are much longer

| | Prospective (259) | Dev (272) |
|---|---:|---:|
| Median words | 515 | 79 |
| Median DeBERTa tokens | 931 | 115 |
| Longer than one 512-token window | 71% | 13% |
| Longer than 2,000 tokens | 29% | 3% |
| With a Markdown list | 64% | 25% |
| With a fenced code block | 65% | 18% |

This is a trend, not an outlier. Median length in the pinned corpus was 43–133 words from 2018
to 2025, then 215 words in the first half of 2026 and 394 in the second half (to the snapshot).
The prospective batch is at 515. The annotated data is mostly older and shorter.

## The output changes with it

| | CRF, prospective | CRF, dev | DeBERTa, prospective | DeBERTa, dev |
|---|---:|---:|---:|---:|
| No explicit conditions found | 7.7% | 43.8% | 0.8% | 9.9% |
| Unsupported structure | 0% | 0% | 0% | 0% |
| Conditions per document | 4.37 | 1.11 | 15.29 | 4.50 |
| Groups per document | 0.15 | 0.03 | 2.63 | 0.75 |
| Share NOT_REQUIRED | 14.0% | 5.3% | 10.3% | 5.1% |
| Share EXCEPTION | 1.9% | 0.3% | 5.0% | 2.7% |
| Median confidence | 0.475 | 0.510 | 0.644 | 0.674 |
| CRF conditions with a negation review flag | 21.0% | 8.3% | n/a | n/a |

## Reading

- **Reviewers would see far more items per advisory.** The CRF suggests 4.4 conditions per new
  advisory, against 1.1 on dev. DeBERTa suggests 15.3. Under `review-policy-0` every suggested
  condition is marked *review required*, so reviewing load grows with advisory length.
- **The CRF almost never abstains on new advisories** (7.7%, against 43.8% on dev). Longer
  texts state more conditions and more cue words, so this is expected. It also means that the
  "no explicit conditions found" state, which this project keeps distinct from "not affected",
  will appear rarely on new advisories.
- **The hard roles appear more often.** NOT_REQUIRED and EXCEPTION make up a larger share of
  predictions, and the CRF's negation flag fires on 21% of conditions (8% on dev). These are
  the roles where both models were weakest on dev and test, so new advisories lean towards the
  known failure modes.
- **Long inputs are now the norm, not the exception.** 71% of new advisories need more than one
  512-token transformer window, and 29% exceed 2,000 tokens, which is the size of the
  benchmark's long-input latency target. Structure that crosses windows is a documented failure
  mode, and it will matter more on newer advisories.
- **What this does not show:** whether the predictions on new advisories are right. That would
  need labels. The behaviour shift suggests that the measured dev and test scores, taken mostly
  on shorter advisories, may not carry over unchanged to current advisories.
