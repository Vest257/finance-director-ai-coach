# FinQA import report

## Run summary

- Fixed selection seed: `financeos-finqa-v1-2026-07-15`
- Source records examined: 8281
- Cards accepted: 100
- Cards rejected or not selected: 8181
- Runtime network access: none; this report and the card bank are committed generated artifacts.

## Rejection reasons

- ambiguous_unit: 56
- answer_mismatch: 3622
- duplicate_question: 163
- missing_required_source_fields: 73
- missing_visible_context: 663
- more_than_two_calculation_steps: 646
- not_selected_after_quality_and_coverage_ordering: 397
- question_not_short_drill: 181
- unclassified_domain: 2034
- unsupported_or_non_deterministic_program: 273
- unsupported_source_answer: 73

## Accepted-card coverage

### Primary domain

- Balance Sheet: 15
- Cash Flow: 10
- Commercial Finance: 5
- Investment & Valuation: 10
- Liquidity & Treasury: 15
- P&L: 20
- Tax: 10
- Working Capital: 15

### Skill

- absolute_change: 54
- average: 9
- multiplication: 4
- percentage_change: 5
- ratio: 3
- total: 25

### Difficulty

- foundational: 79
- intermediate: 21

### Calculation-step count

- 1: 79
- 2: 21

## Manual-review flags

- No manual-review flags were introduced by the deterministic selector. Cards retain their FinQA source ID, report reference, evidence, program, answer, attribution, and MIT licence metadata for reviewer inspection.

## Coverage gaps

None in the initial taxonomy.

## Reproducibility

The full source pass reads `train.json`, `dev.json`, and `test.json` from the upstream FinQA release. CI uses `tests/fixtures/finqa_v1_selected_records.json`, a committed snapshot of the selected source records, so tests perform no network access. Regenerate with `python scripts/import_finqa.py --source tests/fixtures/finqa_v1_selected_records.json`; run against an upstream local dataset directory to re-examine the complete release.

## Attribution and licence

Source: FinQA by Chen et al. (2021), [GitHub repository](https://github.com/czyssrs/FinQA). The upstream repository is MIT licensed; its required notice is retained in `THIRD_PARTY_NOTICES/FinQA-MIT.txt`.
