# Formatting robustness: rules-2

- Sample: 300 advisories, train and dev pools (seed 0)
- Consistent: same conditions (normalised surface, category, role) and groups
- Overall consistency: 100.0% (2,100 of 2,100 document-perturbation pairs)

| Perturbation | Documents | Input changed | Consistent | Rate | Inconsistent examples |
|---|---:|---:|---:|---:|---|
| crlf | 300 | 300 | 300 | 100.0% | none |
| bullet_style | 300 | 59 | 300 | 100.0% | none |
| extra_blank_lines | 300 | 300 | 300 | 100.0% | none |
| rewrap | 300 | 274 | 300 | 100.0% | none |
| backtick_identifiers | 300 | 81 | 300 | 100.0% | none |
| double_spaces | 300 | 300 | 300 | 100.0% | none |
| curly_quotes | 300 | 94 | 300 | 100.0% | none |
