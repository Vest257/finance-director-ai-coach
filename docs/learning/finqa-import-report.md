# FinQA import report

## Run summary

- Fixed selection seed: `financeos-finqa-v1-2026-07-15`
- Source records examined: 8281
- Cards accepted: 100
- Cards rejected or not selected: 8181
- Runtime network access: none; this report and the card bank are committed generated artifacts.

## Rejection reasons

- ambiguous_unit: 264
- answer_mismatch: 3477
- duplicate_question: 163
- invalid_card_schema: 67
- missing_required_source_fields: 73
- more_than_two_calculation_steps: 646
- not_selected_after_quality_and_coverage_ordering: 929
- question_not_short_drill: 181
- semantic_quality_gate: 5
- unclassified_domain: 2034
- unsupported_or_non_deterministic_program: 273
- unsupported_source_answer: 69

## Accepted-card coverage

### Primary domain

- Balance Sheet: 17
- Cash Flow: 11
- Commercial Finance: 5
- Investment & Valuation: 11
- Liquidity & Treasury: 14
- P&L: 18
- Tax: 10
- Working Capital: 14

### Financial skill

- asset_movement: 13
- capitalized_expenditure: 1
- customer_or_segment_performance: 4
- debt_movement: 7
- effective_tax_rate: 4
- equity_movement: 5
- fair_value: 5
- financing_cash_flow: 1
- free_cash_flow: 1
- interest_expense: 6
- investing_cash_flow: 1
- investment_return: 2
- lease_expense: 4
- liability_movement: 1
- liquidity: 3
- net_income: 2
- operating_cash_flow: 6
- operating_expense: 4
- receivables_movement: 11
- revenue_growth: 5
- share_count: 1
- share_price: 1
- share_repurchase: 2
- tax_expense: 8
- working_capital_movement: 2

### Calculation method

- addition: 16
- average: 10
- multi_step_reconciliation: 10
- multiplication: 5
- percentage_change: 6
- percentage_point_change: 2
- ratio: 3
- subtraction: 48

### Difficulty

- foundational: 86
- intermediate: 14

### Calculation-step count

- 1: 84
- 2: 16

## Manual-review flags

- Every selected card is explicitly listed in the committed curation mapping and approved for units, semantics, domain, and learner clarity.

## Coverage gaps

None in the initial taxonomy.

## Reproducibility

The full source pass reads `train.json`, `dev.json`, and `test.json` from the upstream FinQA release. CI uses `tests/fixtures/finqa_v1_selected_records.json`, a committed snapshot of the selected source records, so tests perform no network access.

## Attribution and licence

Source: FinQA by Chen et al. (2021), [GitHub repository](https://github.com/czyssrs/FinQA). The upstream repository is MIT licensed; its required notice is retained in `THIRD_PARTY_NOTICES/FinQA-MIT.txt`.
