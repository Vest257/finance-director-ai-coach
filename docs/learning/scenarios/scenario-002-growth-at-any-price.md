# Scenario 002: Growth at Any Price

Status: Draft synthetic FinanceOS scenario pending Product Owner validation.

## Purpose

Scenario 002 asks the Finance Director of fictional Atlas Bridge to decide how to handle Northstar's renewal. It tests the causal chain from commercial terms to customer profitability, balance-sheet exposure, cash conversion, liquidity, and a defensible recommendation. It is an integrated three-statement decision, not a collection of basic P&L-ratio exercises.

The learner may choose `Approve`, `Conditionally approve`, `Delay`, or `Reject`. Each can be defensible when it is connected to the evidence and route-specific protections.

## Metadata

- Scenario ID: `SCN-002`
- Version: `2.0`
- Provenance: synthetic FinanceOS content
- Learner role: Finance Director of a fictional UK B2B technology and implementation-services company
- Domains: Commercial Finance, Balance Sheet, Cash Flow, and Liquidity
- Competencies: Financial Insight, Commercial Judgment, and Cash And Risk Discipline
- Completion time: about 35 minutes
- Difficulty: advanced

## Financial Contract

All figures are GBP millions unless stated otherwise. The learner pack shows the following raw inputs, but never the assessed derived outcomes before submission.

| Area | Raw inputs |
| --- | --- |
| Comparative P&L | FY2025/FY2026 revenue `40.00/48.00`, gross profit `18.00/18.24`, and EBITDA `4.80/3.36` |
| EBITDA-to-cash bridge | EBITDA `3.36`; receivables `(2.40)`; contract assets `(1.20)`; deferred revenue `0.40`; provision cash `(0.30)`; capitalised implementation cash `(0.80)`; interest `(0.35)`; tax `(0.25)` |
| Customer exposure | Company/Northstar receivables `12.00/3.00`; Northstar overdue `1.20`; payment terms 45 days; company/Northstar contract assets `4.50/1.80`; company/Northstar deferred revenue `3.20/0.60`; capitalised implementation `1.00`; recoverability 70%; provision `0.50` |
| Liquidity | Cash `3.80`; gross debt `8.00`; undrawn RCF `4.00`; board cash floor `3.50`; July to December baseline cash forecast |
| Routes | Discount, target margin, direct-cost base, 70% forecast-period billing/collection of the renegotiation price uplift, avoidable/retained cost, recovery, transition, replacement, and monthly route assumptions |

Definitions are explicit in the learner pack:

- Operating cash flow is the stated EBITDA-to-cash bridge total.
- Cash conversion is operating cash flow divided by EBITDA.
- Net customer working capital is Northstar receivables plus contract assets, less deferred revenue and the service-credit/transition provision.
- Total customer balance-sheet exposure is net customer working capital plus capitalised implementation.
- Exposure at risk uses 20% unrecovered receivables, 50% unrecovered contract assets, non-recoverable implementation, and the provision.
- Required RCF draw is the positive difference between the board floor and route low point; liquidity headroom is undrawn RCF less that draw.

## Cash-Flow Reconciliation

The bridge reconciles EBITDA to operating cash by applying every signed movement. Working-capital build and capitalised implementation expenditure are cash effects even where they are not current P&L expense. Interest and tax are included so the learner sees the liquidity result rather than an adjusted proxy.

The baseline monthly closing-cash forecast is July `4.10`, August `3.90`, September `3.70`, October `3.60`, November `3.80`, and December `4.00`. Learners apply each route's monthly adjustment and identify the trough rather than relying on the year-end balance.

## Route Assumptions And Outcomes

The learner receives raw assumptions for all three routes:

- Renew: a 5.0% discount, no immediate direct-cost repair, additional working-capital build, and stated monthly cash deterioration.
- Renegotiate: a 45.0% target contribution margin on a 6.00 direct-cost base, controls for implementation/support cash, payment protection, and stated monthly cash improvements.
- Exit and redeploy: revenue cessation, 5.00 avoidable direct cost, 1.00 retained direct cost, 0.80 retained allocated overhead, customer-asset recovery, 1.10 transition cash, and replacement contribution/cash timing.

The full reconciliation, including annual EBITDA, annual operating cash, monthly cash trough, RCF draw, and headroom for every route, appears only in the skip path, post-submission worked solutions, and the reconciliation summary. Retained cost is not double counted as an additional exit cash cost.

## Guided Evidence

| Stage | Evidence IDs | Focus |
| --- | --- | --- |
| Quality of earnings and cash conversion | `E-001` to `E-004` | Quality interpretation, operating cash, conversion, and largest cash absorber |
| Balance sheet and customer exposure | `E-005` to `E-008` | DSO, concentration, net working capital, total exposure, and exposure at risk |
| Route cash and liquidity | `E-009` to `E-012` | Route EBITDA/cash, monthly trough, RCF capacity, and classification |
| Finance Director decision | `E-013` to `E-015` | Recommendation, route safeguards, protections, and decision-changing assumptions |

There is one basic P&L/trend evidence (`E-001`) and fifteen substantive evidence records overall. Financial Insight has these deterministic boundaries: `Not assessed` where none of `E-001` to `E-012` supplies meaningful evidence; `Developing` where a cash-bridge result (`E-002` or `E-003`), customer-exposure result (`E-005` to `E-008`), or any all-route liquidity result (monthly troughs `E-010`, or RCF draw and headroom `E-011`) is incorrect or incomplete; `Capable` where all of those material results are correct but limited extended route calculations (`E-009`), classifications (`E-012`), or integrated interpretation (`E-001` or `E-004`) are not; and `Strong` where `E-001` to `E-012` all succeed. Commercial Judgment is capped at `Capable`; Stakeholder Communication and Strategic Leadership stay `Not assessed` without qualified manual review. CEO wording is retained only for self-review and does not affect deterministic evaluation.

## Explanation Requirements

Every numerical record provides a post-submission **How was this calculated?** explanation with the definition, formula, learner-visible sources, intermediate calculation, unit, answer, and business implication. Provision classification distinguishes creation/increase (current-period P&L and balance sheet), settlement (cash and balance sheet), and release (current-period P&L and balance sheet). Relevant structured records provide **Why does this matter?** explanations covering profit versus cash, customer credit exposure, deferred revenue, capitalised implementation cash, exit timing, RCF capacity, monthly troughs, and safeguards.

No worked calculation, model answer, or judgment explanation is rendered during the guided flow. The skip path contains the complete reconciliation, model answer, debrief, self-review checklist, action plan, and all competencies as `Not assessed`.

## Publication Validation Gate

Before publication or material change, Finance SME, Product Owner, and QA must validate financial reconciliation, tolerances, answer-leakage boundaries, every recommendation route, explanations, skip behavior, competency caps, state isolation, and desktop plus 390px layouts. See the [evaluation contract](../evaluation-contract.md).
