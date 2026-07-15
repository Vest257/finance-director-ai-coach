# FinanceOS fast-drill taxonomy

The FinQA v1 content bank is a deterministic calculation-content asset. It is not a learner interface, scoring system, progress record, or adaptive-sequencing system.

Every card has exactly one primary domain, one primary skill, an optional list of secondary domains, a constrained difficulty level, and one or two calculation steps. Domain tags are assigned from the wording of the source question rather than to satisfy a quota.

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

## Calculation skills

- `absolute_change`: add or subtract a financial movement.
- `average`: calculate a mean from the supplied inputs.
- `multiplication`: scale a rate or per-unit input.
- `percentage_change`: calculate or compare a percentage, percentage-point, rate, or margin movement.
- `ratio`: divide supplied inputs to produce a ratio or rate.
- `total`: add supplied components to a total.

## Difficulty and units

- `foundational`: one executable calculation step.
- `intermediate`: two executable calculation steps.

All cards preserve FinQA signs. Percentage answers are stored as percentage values (for example, `12.5`, not `0.125`) when that is how the FinQA program and source answer are expressed. Units are normalized to percent, ratio, USD, USD per share, USD millions, millions, billions, thousands, millions of shares, years, or shares only when the source question or visible evidence makes that unit unambiguous.

The v1 selector rejects ambiguous units instead of guessing. The import report records any resulting coverage gaps.
