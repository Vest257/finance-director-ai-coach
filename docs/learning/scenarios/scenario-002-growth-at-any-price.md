# Scenario 002: Growth at Any Price

Status: approved synthetic FinanceOS scenario for the curated library.

## Purpose

Scenario 002 asks a Finance Director whether Atlas Bridge should renew a strategically visible customer contract when reported growth is accompanied by deteriorating company margins and weak customer contribution.

The learner may choose `Approve`, `Conditionally approve`, `Delay`, or `Reject`. The model answer is not the only acceptable route. Every route must be supported by its documented safeguards and the available evidence.

## Metadata

- Scenario ID: `SCN-002`
- Version: `1.0`
- Provenance: synthetic FinanceOS content for commercial-finance learning and product-owner validation
- Learner role: Finance Director of a fictional UK B2B technology and implementation-services company
- Primary domains: Management Accounting, Commercial Finance, Pricing, Customer Profitability, and FP&A
- Primary competencies: Financial Insight, Commercial Judgment, Stakeholder Communication, and Strategic Leadership
- Supporting competency: Cash And Risk Discipline
- Completion time: about 25 minutes
- Difficulty: advanced

## Learner-Facing Pack

All figures are GBP millions unless stated otherwise. The learner-facing pack includes calculation inputs and an explicit exit-cost relationship:

- FY2025 and FY2026 forecast company revenue, gross profit, and EBITDA.
- Northstar's GBP 10.50m standard price, GBP 9.00m reported customer revenue, and direct cost-to-serve components.
- Separately reported allocated head-office overhead.
- A defined 45.0% target contribution margin and 5.0% requested extra discount.
- Capacity consumption, the avoidable cost categories after exit, retained commitments, and redeployment contribution assumptions.
- Stakeholder pressure and information not yet available.

The pack does not state calculated revenue growth, company margins, customer contribution, economic revenue, required price increase, cost reduction, discount effect, or option EBITDA outcomes before submission.

## Reconciled Financial Contract

| Measure | Reconciled result | Learner format |
| --- | ---: | --- |
| Company revenue growth | 20.0% | Percentage points |
| Gross margin: FY2025 / FY2026 | 45.0% / 38.0% | Percentage points |
| EBITDA margin: FY2025 / FY2026 | 12.0% / 7.0% | Percentage points |
| Northstar contribution / margin | GBP 3.00m / 33.3% | GBP m / percentage points |
| Economic revenue at 45.0% target | GBP 10.91m | GBP m |
| Required price increase | GBP 1.91m / 21.2% | GBP m / percentage points |
| Required direct-cost reduction | GBP 1.05m | GBP m |
| Additional discount / resulting margin | GBP 0.45m / 29.8% | GBP m / percentage points |
| Company EBITDA: proposed renewal | GBP 2.91m | Skip-path reconciliation only |
| Company EBITDA: target economics | GBP 5.27m | Skip-path reconciliation only |
| Company EBITDA: exit and redeployment | GBP 3.06m | Skip-path reconciliation only |

The current direct customer-cost base is GBP 6.00m. The exit-and-redeployment result deducts GBP 9.00m of revenue, adds GBP 5.00m of avoidable direct cost, and adds GBP 3.70m of replacement contribution. The remaining GBP 1.00m is retained direct cost within the existing GBP 6.00m base, not an additional exit cost: it comprises GBP 0.50m of delivery notice and tooling commitments and GBP 0.50m of service-level credits. The separately allocated GBP 0.80m head-office amount also remains, is already contained in company EBITDA, and is not treated as avoidable.

## Guided Flow

1. Company performance: calculate growth and company margins; interpret growth with margin deterioration.
2. Customer economics: calculate contribution, target pricing, cost-reduction alternative, and the requested-discount effect.
3. Drivers and risks: select exactly three priority margin drivers, four avoidable direct-cost categories, and three missing information items.
4. Decision: choose a route, select route safeguards, select exactly two decision conditions, and write a concise CEO recommendation.

Free-text CEO wording is retained for self-review only. It is not deterministically scored for keywords, length, grammar, sentiment, persuasiveness, or leadership quality.

The driver ranking is derivable from raw pack data. The standard price and reported revenue establish the current discount/value leakage; the other options are ranked only where they have a quantified cost-to-serve input. The calculated ranking remains post-submission feedback rather than learner-facing pack content.

## Evidence And Explanations

Evidence IDs run from `SCN-002-E-001` through `SCN-002-E-015`.

- Numerical evidence: `E-001`, `E-002`, `E-003`, `E-005`, `E-006`, `E-007`, and `E-008` uses explicit tolerances and a post-submission "How was this calculated?" worked solution.
- Structured evidence: `E-004`, `E-009` through `E-014` uses explicit selection rules and a post-submission "Why does this matter?" explanation where the learning value warrants it.
- `E-012` records the route, `E-013` checks the route's safeguards, and `E-015` checks sequence completion. A route alone does not create a Strategic Leadership rating.

Critical omissions are explicit gates: materially incorrect company-margin evidence, materially incorrect customer economics, no decision route, or missing route safeguards. They are not penalty points.

Commercial Judgment may be deterministically rated only `Developing` or `Capable`. Stakeholder Communication and Strategic Leadership remain `Not assessed` without a qualified manual reviewer. See the [evaluation contract](../evaluation-contract.md).

## Route Safeguards

Every route can be defensible under the stated evidence:

- Approve: revised scope, margin monitoring, a commercial trade for any discount, and an escalation trigger.
- Conditionally approve: target pricing, capped implementation exposure, service-level reset, and named commercial and delivery owners.
- Delay: short negotiation window, validated profitability and exit-cost case, interim scope controls, and a redeployment plan.
- Reject: transition plan, capacity redeployment, commercial re-entry economics, and stakeholder-management plan.

## Route-Aware Decision Conditions

The learner always selects exactly two decision conditions. The deterministic rule applies them to the selected route:

- Approve and Conditionally approve: target contribution margin and scope/service reset.
- Delay: capacity release plus either target contribution margin or scope/service reset.
- Reject: capacity release and target contribution margin.

The rule is displayed only in post-submission evidence feedback. It does not turn a selected route into a Strategic Leadership rating.

## Validation Gate

Before publication or material change, validate the financial pack, calculations, tolerances, answer-leakage boundary, all recommendation routes, explanations, skip path, scorecard limits, summary boundary, and desktop and narrow browser flows. Finance SME, Product Owner, and QA approval is required before registry publication.
