# Fixture attribution

The JSON files in this directory are unmodified advisory records from the
[GitHub Advisory Database](https://github.com/github/advisory-database), licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). They are used as test fixtures.

| File | Source |
|---|---|
| `GHSA-5h86-8mv2-jq9f.json` | https://github.com/advisories/GHSA-5h86-8mv2-jq9f |
| `GHSA-m2qf-hxjv-5gpq.json` | https://github.com/advisories/GHSA-m2qf-hxjv-5gpq |

`../label_studio/export_aiohttp_ls-1.23.2.json` is a real Label Studio 1.23.2 JSON export of a
task built from `GHSA-5h86-8mv2-jq9f`; it embeds that advisory's text (CC BY 4.0) and a
synthetic test annotation, not a gold label.
