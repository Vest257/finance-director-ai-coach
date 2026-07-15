# FinanceOS fast-drill taxonomy

The FinQA v1 content bank is a deterministic calculation-content asset. It is not a learner interface, scoring system, progress record, or adaptive-sequencing system.

Every card has exactly one primary domain, one financial skill, one calculation method, an optional list of secondary domains, a constrained difficulty level, and one or two calculation steps. The committed curation ledger, rather than keyword order, is the authority for the final domain and skill assignments.

## Primary domains

| Domain | Scope for a short calculation drill |
| --- | --- |
| P&L | Revenue, costs, margins, earnings, and profit movement. |
| Balance Sheet | Assets, liabilities, equity, book values, and reported financial position. |
| Cash Flow | Operating, investing, financing, and free-cash-flow calculations. |
| Working Capital | Inventory, receivables, payables, and cash-conversion calculations. |
| Liquidity & Treasury | Cash, debt, interest, borrowing, maturities, dividends, and funding. |
| Tax | Tax balances, tax rates, and tax-related movements. |
| Commercial Finance | Customers, products, segments, contracts, subscribers, and commercial metrics. |
| Investment & Valuation | Investments, returns, shares, market values, acquisition, and valuation measures. |

## Financial skills

- Financial skills describe the finance concept, such as `receivables_movement`, `operating_cash_flow`, `debt_movement`, `effective_tax_rate`, `tax_expense`, `share_repurchase`, `fair_value`, or `customer_or_segment_performance`.
- Calculation methods describe how the answer is calculated: `addition`, `subtraction`, `multiplication`, `ratio`, `percentage_change`, `percentage_point_change`, `average`, or `multi_step_reconciliation`.

## Difficulty and units

- `foundational`: one executable calculation step.
- `intermediate`: two executable calculation steps.

All cards preserve FinQA signs. Percentage answers are stored as percentage values (for example, `12.5`, not `0.125`) when that is how the FinQA program and source answer are expressed. A card carries an explicit unit dimension and scale: currency, plain number, percentage, percentage points, shares, years, per-share amount, or ratio; and unit, thousand, million, or billion. The importer rejects unclear mixed scales instead of treating USD million as plain USD.

The v1 selector rejects ambiguous units and semantically unsuitable calculations instead of guessing. `data/drills/finqa_v1_curation.json` records the individual review status, domain, secondary domains, financial skill, calculation method, and reviewer note for all 100 cards.
