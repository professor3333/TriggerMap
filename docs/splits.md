# Split design (`splits/pool-v1.json`, frozen)

Every one of the 6,350 PyPI advisories in snapshot `1912cbd6` is assigned to a **train**,
**dev** or **test** pool *before* scaled annotation. Annotation batches are then drawn from a
pool, so no leakage group can span splits. Built with `triggermap corpus split`; the
manifest is checked on every CI run (`tests/test_splits.py`).

## Leakage groups

Advisories are unioned into one group when they share any of:

| Relation | Source |
|---|---|
| A PyPI package (PEP 503 name) | `affected[].package` |
| An upstream GitHub repository | the `PACKAGE` reference (present in 93% of advisories) |
| Identical text or identical details (whitespace/case folded) | content hashes |
| An alias (CVE, PYSEC) | `aliases` |
| Near-duplicate details | MinHash LSH on word 5-shingles, verified exact Jaccard ≥ 0.6 |

The near-duplicate threshold was chosen on this snapshot. At Jaccard ≥ 0.6 there are 412
pairs, 31 of them across package boundaries, and the cross-package pairs inspected were shared
boilerplate wording. A lower threshold is the conservative choice for leakage, because
over-merging only makes groups larger. Result: 1,328 leakage groups; the largest
(TensorFlow and its package variants) has 433 advisories.

## Assignment rules

1. **Test** takes the *newest* groups by first publication date, among groups of at most 25
   advisories, until it holds 18.75% of documents. The test set therefore measures
   **temporal and project shift**.
2. **Dev** holds every remaining group that contains a natural (random-stratum) pilot
   document, including large projects, so that big projects stay represented in evaluation.
   It also takes a seeded random draw of small and medium groups, filling 18.75% of
   documents in capped groups. This gives dev many projects.
3. **Train** gets everything else.
4. Pilot: all 50 natural pilot documents are in evaluation pools (38 dev, 12 test). Where a
   group holds both a natural and an enriched pilot document, evaluation wins. Those 11
   enriched documents are listed in `excluded_documents`: annotated, but used neither for
   training nor for scoring.

| Pool | Documents | Groups | Groups > 25 docs | Published | Pilot natural / enriched |
|---|---:|---:|---:|---|---|
| train | 2,450 | 347 | 21 | 2018-07 → 2026-10 | 0 / 39 |
| dev | 2,703 | 423 | 15 | 2018-07 → 2026-10 | 38 / 11 (excluded) |
| test | 1,197 | 558 | 0 | 2024-04 → 2026-10 | 12 / 0 |

## Consequences and limitations

- Annotation samples from dev and test cap documents per group, and evaluation uses
  project-clustered bootstrap intervals, so no single project dominates a score.
- Test contains no project with more than 25 advisories. Performance on large, templated
  projects is measured on dev and reported separately.
- The 12 natural pilot documents in the test pool are **locked**: they are not used to score
  baselines during development. `triggermap evaluate` refuses the test split unless called
  with `--release-evaluation "<reason>"`, and logs every such run in
  `docs/test-access-log.md`.
- `triggermap train` only ever reads train-pool documents.
