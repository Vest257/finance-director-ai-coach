# Scenario 001: Growth With Falling Cash

- Status: accepted by the Product Owner for Phase 1 implementation.
- Product: Finance Director Scenario Coach.
- Scenario ID: `SCN-001`.
- Version: 1.0.

This document is the first scenario implementation contract. It applies the [scenario design guidance](../scenario-design.md), [evaluation contract](../evaluation-contract.md), [learning domain framework](../domain-framework.md), and [behavioral competency framework](../competency-framework.md).

## Scenario Title

Growth With Falling Cash: Should We Hire 20 People?

## Learner Role

The learner is the Finance Director of Northstar Monitoring Ltd. They report to the CEO, attend board meetings, own cash forecasting, and are expected to make a recommendation rather than only describe the financial results.

## Company Context

Northstar Monitoring Ltd is a fictional UK-based provider of industrial monitoring hardware, installation services, and recurring analytics software. It has 120 employees and sells mainly to energy, logistics, and manufacturing customers.

Large enterprise deployments have accelerated revenue growth. These contracts require hardware purchases and implementation work before customer cash is collected. Sales has also agreed longer payment terms to win several strategic accounts.

The company is profitable and growing, but cash conversion has deteriorated. The CEO believes delivery capacity is now the main constraint and wants to hire 20 additional engineers and implementation specialists.

## Current Management Issue

The CEO wants authority to begin all recruitment immediately and announce the expansion at the next board meeting. The Finance Director must approve, conditionally approve, delay, or reject the plan using the available evidence.

The decision is needed today. Some relevant information is unavailable, and the learner is expected to identify it rather than invent it.

## Stakeholders

- CEO: wants to protect growth momentum and reduce delivery backlogs.
- Finance Director: owns the recommendation, liquidity view, and decision conditions.
- Chief Revenue Officer: argues that capacity is limiting new contract wins.
- Chief Operating Officer: owns implementation capacity and the hiring plan.
- Board: expects growth but has set an internal minimum cash floor.
- Lender: provides term debt and a revolving credit facility subject to covenants.
- Employees and candidates: affected by the credibility and timing of the hiring decision.

## Learning Domains

- Primary: Balance Sheet.
- Primary: Cash Flow.
- Secondary: Treasury.
- Supporting: broader Finance Director topics, including planning and business partnering.

## Behavioral Competencies

- Financial Insight.
- Commercial Judgment.
- Cash And Risk Discipline.
- Stakeholder Communication.
- Strategic Leadership.

## Learning Objectives

By completing the scenario, the learner should be able to:

- Reconcile rising EBITDA with falling cash.
- Identify the working-capital movements driving poor cash conversion.
- Quantify the liquidity effect and timing of a hiring plan.
- Distinguish an internal cash floor from a lender covenant.
- Make a defensible recommendation under incomplete information.
- Set practical decision conditions without treating growth as inherently good or bad.
- Communicate a concise executive recommendation.

## Financial Pack

Unless stated otherwise, figures are GBP millions and have been rounded to two decimal places. Parentheses indicate costs, cash outflows, or deductions.

### Operating Context

- H1 2026 revenue includes two large enterprise deployments with 90-day payment terms.
- Five customers represent GBP 5.60m of the GBP 9.20m closing trade receivables balance.
- GBP 2.00m of trade receivables is more than 30 days overdue.
- Inventory was purchased ahead of signed installation schedules to avoid component shortages.
- The current headcount is 120.
- No dividends were paid in H1 2026.

### Simplified Comparative Income Statement

| Six months ended 30 June | H1 2025 | H1 2026 | Change |
| --- | ---: | ---: | ---: |
| Revenue | 18.00 | 22.00 | 22.2% |
| Cost of sales | (9.90) | (11.90) | 20.2% |
| Gross profit | 8.10 | 10.10 | 24.7% |
| Operating expenses before depreciation and amortization | (5.40) | (6.70) | 24.1% |
| EBITDA | 2.70 | 3.40 | 25.9% |
| Depreciation and amortization | (0.60) | (0.70) | 16.7% |
| Operating profit | 2.10 | 2.70 | 28.6% |
| Net interest expense | (0.25) | (0.20) | (20.0%) |
| Profit before tax | 1.85 | 2.50 | 35.1% |
| Tax expense | (0.37) | (0.50) | 35.1% |
| Net income | 1.48 | 2.00 | 35.1% |

The pack provides no evidence that accounting profit is misstated. The issue is conversion of profit into cash.

### Simplified Comparative Balance Sheet

| | 31 December 2025 | 30 June 2026 | Movement |
| --- | ---: | ---: | ---: |
| Cash | 7.00 | 4.30 | (2.70) |
| Trade receivables | 6.00 | 9.20 | 3.20 |
| Inventory | 2.50 | 3.60 | 1.10 |
| Contract assets and prepayments | 1.00 | 1.60 | 0.60 |
| Property, equipment, and capitalized software, net | 5.00 | 5.50 | 0.50 |
| **Total assets** | **21.50** | **24.20** | **2.70** |
| Trade payables | 3.10 | 4.00 | 0.90 |
| Accruals and deferred revenue | 2.00 | 2.40 | 0.40 |
| Interest-bearing debt | 5.50 | 4.90 | (0.60) |
| Equity | 10.90 | 12.90 | 2.00 |
| **Total liabilities and equity** | **21.50** | **24.20** | **2.70** |

The GBP 0.50m increase in net fixed assets equals GBP 1.20m of capital expenditure less GBP 0.70m of depreciation and amortization. Equity increased by H1 net income of GBP 2.00m.

### EBITDA-To-Cash Bridge

| H1 2026 | GBP m |
| --- | ---: |
| EBITDA | 3.40 |
| Increase in trade receivables | (3.20) |
| Increase in inventory | (1.10) |
| Increase in contract assets and prepayments | (0.60) |
| Increase in trade payables | 0.90 |
| Increase in accruals and deferred revenue | 0.40 |
| **Operating cash before interest and tax** | **(0.20)** |
| Cash interest paid | (0.20) |
| Cash tax paid | (0.50) |
| **Net cash from operating activities** | **(0.90)** |
| Capital expenditure | (1.20) |
| Debt principal repaid | (0.60) |
| **Net decrease in cash** | **(2.70)** |
| Opening cash | 7.00 |
| **Closing cash** | **4.30** |

The bridge explains the complete movement in cash. There were no acquisitions, dividends, equity raises, or other financing cash flows in H1 2026.

### Working-Capital Information

| Measure | Prior reference point | 30 June 2026 | Management comment |
| --- | ---: | ---: | --- |
| Trade receivables | GBP 6.00m | GBP 9.20m | Growth, 90-day terms, and slower collections |
| Days sales outstanding | 61 days | 76 days | Above the 60-day operating target |
| Receivables more than 30 days overdue | GBP 0.80m | GBP 2.00m | Concentrated in three enterprise accounts |
| Inventory | GBP 2.50m | GBP 3.60m | Components bought before installation dates |
| Inventory days | 46 days | 55 days | Above the 45-day operating target |
| Trade payables | GBP 3.10m | GBP 4.00m | Supplier terms partly offset the asset build |
| Payables days | 57 days | 61 days | No reported overdue supplier balances |

Of the GBP 0.60m increase in contract assets and prepayments, GBP 0.45m relates to implementation work performed before billing milestones and GBP 0.15m relates to prepaid cloud and insurance contracts.

### Current Cash And Liquidity Outlook

Management's base forecast before the proposed hires is:

| Month end | Baseline monthly net cash flow | Baseline closing cash |
| --- | ---: | ---: |
| June 2026 actual | - | 4.30 |
| July | (0.50) | 3.80 |
| August | (0.30) | 3.50 |
| September | 0.00 | 3.50 |
| October | 0.30 | 3.80 |
| November | 0.50 | 4.30 |
| December | 0.70 | 5.00 |

The forecast assumes overdue receivables reduce during Q4 and planned installation milestones are billed on time. It includes scheduled debt service and approved capital expenditure. No quantified downside case is included in the pack.

Cash remains positive and monthly cash flow turns positive in the base forecast, so the pack does not indicate a finite cash-exhaustion runway. The relevant liquidity measure is headroom to the GBP 3.50m board floor and GBP 2.50m lender minimum. A downside runway conclusion cannot be made without the missing sensitivity analysis.

### Financing And Covenants

- Interest-bearing debt at 30 June 2026 is GBP 4.90m.
- A GBP 3.00m revolving credit facility is undrawn and expires on 31 March 2027.
- The lender minimum cash covenant is GBP 2.50m, tested monthly.
- The board's internal minimum cash floor is GBP 3.50m.
- Management reports compliance with the leverage covenant at 30 June 2026; no covenant waiver is currently required.
- The pack does not include a lender commitment to renew the revolving credit facility.

### Proposed 20 Hires

The CEO proposes 10 starters on 1 September and 10 starters on 1 November.

- Roles: 12 implementation specialists and 8 engineers.
- Recurring fully loaded cost: GBP 84,000 per person per year, including salary, employer taxes, benefits, and software.
- Total annual recurring cost for 20 hires: GBP 1.68m.
- One-time recruitment and onboarding expense: GBP 8,000 per starter.
- Total one-time expense: GBP 0.16m.
- No incremental revenue or customer receipts from the hires are included in the approved forecast.
- All listed hiring costs are assumed to be paid and expensed in the month incurred.

| Month | Incremental hiring cash and EBITDA cost | Closing cash after cumulative hiring cost |
| --- | ---: | ---: |
| July | 0.00 | 3.80 |
| August | 0.00 | 3.50 |
| September | (0.15) | 3.35 |
| October | (0.07) | 3.58 |
| November | (0.22) | 3.86 |
| December | (0.14) | 4.42 |
| **H2 2026 total** | **(0.58)** | **4.42** |

The exact H2 hiring cost is GBP 0.58m: GBP 0.42m recurring cost plus GBP 0.16m one-time cost. The forecast low point becomes GBP 3.35m in September, GBP 0.15m below the board floor and GBP 0.85m above the lender minimum cash covenant.

## Important Assumptions

- Income statement, balance sheet, and cash bridge figures are management accounts prepared on a consistent basis.
- Tax expense equals cash tax paid in H1 2026; there is no material tax payable movement.
- No dividends or unlisted financing flows occurred in H1 2026.
- Baseline forecast collections and installation billing occur when management expects.
- Hiring dates and costs follow the proposed schedule with no attrition, vacancy delay, or cost overrun.
- The hiring plan creates no incremental H2 revenue or receipts in the presented forecast.
- The undrawn revolving credit facility remains available under its current terms until expiry.

## Information Unavailable To The Learner

The learner should identify the significance of missing information rather than assume favorable answers. The pack does not provide:

- A customer-by-customer aged receivables report or written collection commitments.
- A quantified downside cash forecast.
- A role-by-role capacity, productivity, or revenue business case for the hires.
- Evidence of how quickly new hires become productive.
- Current employee utilization, regretted attrition, or contractor alternatives.
- Signed candidate offers or unavoidable recruitment commitments.
- Board approval for a temporary exception to the GBP 3.50m internal cash floor.
- A confirmed refinancing or renewal plan for the March 2027 revolving credit facility expiry.

## Initial CEO Question

> Revenue and EBITDA are both ahead, and delivery says we are turning away work. I want to hire all 20 people now and tell the board today. Are you approving the plan? Give me the decision, the finance case, and any actions you need from the team.

## Guided Questions

Each guided question has an ID so learner inputs can trace to evaluation evidence.

1. `GQ-001`: By how much did revenue, EBITDA, and cash change, and what does that combination tell you?
2. `GQ-002`: Reconcile H1 EBITDA to operating cash before interest and tax and to the closing cash balance.
3. `GQ-003`: Select the working-capital movements that materially explain the cash decline and identify the largest driver.
4. `GQ-004`: What risks are visible in receivables, inventory, contract assets, and the baseline forecast?
5. `GQ-005`: Calculate the H2 2026 hiring cost, forecast low point, December cash, and headroom to both cash thresholds.
6. `GQ-006`: Choose `Approve`, `Conditionally approve`, `Delay`, or `Reject`.
7. `GQ-007`: Select or state the safeguards, conditions, and operating actions appropriate to your recommendation.
8. `GQ-008`: Identify the unavailable information you need and explain how it could change the decision.
9. `GQ-009`: Give the CEO a concise final recommendation in executive language.

## Skip-To-Solution Path

The learner may skip directly to the model Finance Director answer and debrief. The path should still show:

- The complete financial reconciliation.
- Critical observations and missing information.
- Acceptable alternative recommendations.
- The self-review checklist.
- The learner action plan.

Skipping does not produce an assessed attempt. Every competency is shown as `Not assessed` with the explanation that no learner evidence was collected.

## Required Learner Outputs

- Numerical answers for `GQ-001`, `GQ-002`, and `GQ-005`.
- Structured selections for material drivers, risks, recommendation, safeguards, and missing information.
- A final recommendation selected from the four permitted routes.
- A concise free-text CEO response.
- Optional self-review after comparing the response with the model answer.

## Deterministically Assessable Elements

Numerical tolerance is GBP 0.05m for monetary values and 0.2 percentage points for growth rates unless stated otherwise.

| Evidence ID | Requirement | Expected evidence | Competencies informed |
| --- | --- | --- | --- |
| `E-001` | Growth calculation | Revenue growth 22.2%; EBITDA growth 25.9% | Financial Insight |
| `E-002` | Cash movement | Cash decreased by GBP 2.70m, from GBP 7.00m to GBP 4.30m | Financial Insight; Cash And Risk Discipline |
| `E-003` | Operating cash reconciliation | Operating cash before interest and tax was negative GBP 0.20m; net operating cash was negative GBP 0.90m | Financial Insight |
| `E-004` | Driver recognition | Receivables, inventory, and contract assets/prepayments selected as uses of cash; payables and accruals selected as partial offsets | Financial Insight |
| `E-005` | Largest driver | Trade receivables selected as the largest cash-use movement | Financial Insight |
| `E-006` | Hiring cost | H2 cost GBP 0.58m; annual recurring cost GBP 1.68m | Commercial Judgment |
| `E-007` | Liquidity calculation | Low point GBP 3.35m; December cash GBP 4.42m | Cash And Risk Discipline |
| `E-008` | Threshold interpretation | Board floor breached by GBP 0.15m; lender minimum retained with GBP 0.85m headroom at the low point | Cash And Risk Discipline |
| `E-009` | Decision | One permitted recommendation route selected | Commercial Judgment; Strategic Leadership |
| `E-010` | Route safeguards | Required safeguards for the selected route are chosen | Commercial Judgment; Cash And Risk Discipline |
| `E-011` | Missing information | Material missing information is selected, including collections, downside liquidity, and hiring business case | Financial Insight; Strategic Leadership |
| `E-012` | Required steps | All required calculation, selection, and recommendation steps completed | Commercial Judgment |
| `E-013` | Tradeoff recognition | Growth capacity, recurring cost, timing risk, and at least one alternative capacity action selected | Commercial Judgment |
| `E-014` | Core risk recognition | Overdue or concentrated receivables, the board-floor breach, and forecast dependence on collections selected | Cash And Risk Discipline |
| `E-015` | Extended risk recognition | Inventory or contract-asset pressure, RCF expiry, unsupported hiring benefit, and missing downside case also selected | Cash And Risk Discipline |

## Self-Review And Manual-Review Elements

The non-AI MVP must not automatically judge the free-text CEO response. The learner uses this self-review checklist:

- Did I lead with a clear decision?
- Did I distinguish EBITDA growth from cash conversion?
- Did I quantify the largest working-capital movements and liquidity effect?
- Did I separate the board floor from the lender covenant?
- Did I explain conditions as practical management actions?
- Did I identify missing information without using it as an excuse to avoid a decision?
- Did I communicate concisely and constructively?

Where a Finance SME, coach, or manager is available, the manual reviewer may assign a competency rating for Stakeholder Communication and Strategic Leadership using the scorecard rules below. The review must cite phrases or omissions from the learner's response.

## Critical Observations

- Revenue increased 22.2% and EBITDA increased 25.9%, but cash decreased GBP 2.70m.
- The GBP 3.20m receivables increase is the largest cash-flow driver.
- Inventory and contract assets/prepayments used a further GBP 1.70m.
- Payables and accruals provided GBP 1.30m of partial funding, so supplier timing masks some of the working-capital pressure.
- H1 operating cash before interest and tax was negative GBP 0.20m despite GBP 3.40m EBITDA.
- Cash interest and tax took net operating cash to negative GBP 0.90m; capital expenditure and debt repayment used another GBP 1.80m.
- Days sales outstanding rose from 61 to 76 days and overdue receivables rose to GBP 2.00m.
- The hires add GBP 0.58m of H2 cost and GBP 1.68m of recurring annual cost before any benefit.
- The hiring plan reduces the forecast low point to GBP 3.35m, below the board floor but above the lender covenant.
- The forecast depends on improved collections and timely milestone billing, but no downside case is provided.

## Critical Omissions

| Omission ID | Critical omission | Competencies affected |
| --- | --- | --- |
| `CO-001` | Treating EBITDA growth as evidence of cash strength without addressing working capital | Financial Insight; Cash And Risk Discipline |
| `CO-002` | Materially misstating the cash bridge, hiring cost, liquidity low point, or threshold headroom | Financial Insight; Cash And Risk Discipline |
| `CO-003` | Giving no recommendation | Commercial Judgment; Strategic Leadership |
| `CO-004` | Approving expenditure without acknowledging the board-floor breach or including liquidity safeguards | Commercial Judgment; Cash And Risk Discipline |
| `CO-005` | Claiming that the lender cash covenant is already breached | Financial Insight; Stakeholder Communication |
| `CO-006` | Relying on hiring benefits or collections as certain when the pack does not evidence them | Commercial Judgment; Strategic Leadership |

## Evaluation Traceability

| Learner requirement | Evidence rule | Critical omission gate | Feedback ownership |
| --- | --- | --- | --- |
| `GQ-001` | `E-001`, `E-002` | `CO-001`, `CO-002` | Growth-versus-cash observation and correction |
| `GQ-002` | `E-003` | `CO-001`, `CO-002` | EBITDA-to-cash reconciliation feedback |
| `GQ-003` | `E-004`, `E-005` | `CO-001` | Working-capital driver feedback |
| `GQ-004` | `E-014`, `E-015` | `CO-006` | Risk and unavailable-information feedback |
| `GQ-005` | `E-006`, `E-007`, `E-008` | `CO-002`, `CO-004`, `CO-005` | Hiring cost, liquidity, and threshold feedback |
| `GQ-006` | `E-009` | `CO-003` | Decision completeness feedback |
| `GQ-007` | `E-010`, `E-013` | `CO-004`, `CO-006` | Route-specific safeguard and tradeoff feedback |
| `GQ-008` | `E-011` | `CO-006` | Missing-evidence and next-analysis feedback |
| `GQ-009` | Manual-review rubric and self-review checklist | `CO-003`, `CO-005`, `CO-006` | Communication and leadership feedback |

## Acceptable Alternative Recommendations

No recommendation label is inherently strong or weak. The learner's evidence and safeguards determine the rating.

For `E-010` to be observed, the learner must select every core safeguard for the chosen route. Additional safeguards may strengthen the response but do not compensate for a missing core safeguard.

| Route | Core safeguards required for `E-010` | Stronger evidence |
| --- | --- | --- |
| Approve | Explicit board-floor exception or funding source; weekly 13-week cash monitoring; named collections action; trigger to slow or stop starts | Role-level demand case and RCF expiry plan |
| Conditionally approve | Measurable first-tranche condition; measurable second-tranche gate; cash threshold; named owners | Downside forecast, collection target, and time-to-productivity evidence |
| Delay | Decision date; specific information required; interim collections or capacity action | Quantified threshold that would convert delay to approval or rejection |
| Reject | Financial reason for rejection; requirements for a revised proposal; practical alternative for urgent capacity | Explicit downside exposure and funding criterion for reconsideration |

### Approve

Approval now can be defensible because the company remains profitable, forecast cash remains above the lender minimum, and GBP 3.00m of revolving credit is undrawn. A strong approval explicitly accepts or obtains board approval for the temporary internal-floor exception, launches immediate collections actions, monitors a 13-week cash forecast, and retains the ability to slow starts if cash deteriorates.

### Conditionally Approve

Conditional approval can be defensible when recruitment proceeds but start dates or the second tranche depend on collections, cash headroom, role-level demand evidence, or board approval. Strong conditions are measurable, time-bound, and owned by named executives.

### Delay

Delay can be defensible when the learner requires a quantified downside forecast, collection evidence, and a role-level business case before committing. A strong delay sets a near-term decision date and interim actions so delay does not become passive avoidance.

### Reject

Rejecting the current plan can be defensible if the learner concludes that weak cash conversion, the internal-floor breach, and unsupported hiring benefits make the proposal unacceptable as presented. A strong rejection distinguishes rejecting this plan from rejecting growth and specifies what a revised proposal must demonstrate.

## Conditions That Strengthen Approval

- Collect a defined amount of overdue receivables by a defined date.
- Produce a weekly 13-week cash forecast with a quantified downside case.
- Keep forecast cash at or above the board floor, or obtain explicit board approval for an exception.
- Phase the two tranches and gate the second tranche on collections, utilization, delivery backlog, or signed demand.
- Provide a role-by-role business case and time-to-productivity assumption.
- Confirm revolving credit availability and present a plan before its March 2027 expiry.
- Establish named owners for collections, inventory reduction, milestone billing, and hiring controls.

## Conditions That Justify Delay Or Rejection

- No credible route to restore cash conversion or reduce overdue receivables.
- A downside forecast indicates likely breach of the lender minimum or unacceptable reliance on short-term borrowing.
- The board does not approve a floor exception and management cannot preserve GBP 3.50m cash.
- Hiring demand is unsupported by signed work, utilization, or a role-level plan.
- Recruitment commitments are inflexible despite uncertain collections and funding.
- Management refuses staged hiring, cash monitoring, or working-capital accountability.

## Competency Scorecard Rubric

The [evaluation contract](../evaluation-contract.md) governs rating precedence and evidence presentation. There is no overall numerical score.

| Competency | Core evidence for `Capable` | Additional evidence for `Strong` | Critical gates | MVP assessment source |
| --- | --- | --- | --- | --- |
| Financial Insight | `E-002`, `E-003`, `E-004`, and `E-005` observed | `E-001` and `E-011` also observed; balance sheet and cash bridge connected | `CO-001`, `CO-002`, `CO-005` | Deterministic |
| Commercial Judgment | `E-006`, `E-009`, `E-010`, and `E-012` observed | A qualified reviewer finds sound tradeoff reasoning using `E-013` and the learner's explanation | `CO-003`, `CO-004`, `CO-006` | Deterministic is capped at `Capable`; manual review is required for `Strong` |
| Cash And Risk Discipline | `E-002`, `E-007`, `E-008`, `E-014`, and route-relevant `E-010` observed | `E-015` also observed | `CO-001`, `CO-002`, `CO-004` | Deterministic |
| Stakeholder Communication | A qualified reviewer finds a clear decision, correct numbers, and understandable tradeoffs | Concise, persuasive, constructive challenge with well-sequenced actions | `CO-005` or materially misleading communication | Manual review; otherwise `Not assessed` |
| Strategic Leadership | A qualified reviewer finds ownership, a decision, and practical cross-functional actions | Aligns growth, liquidity, accountability, and contingency planning without avoiding the decision | `CO-003`, `CO-006` | Manual review; otherwise `Not assessed` |

For each competency, feedback must list the evidence observed, explain the rating, identify a specific improvement, and state the assessment source. Different recommendation routes can earn equivalent deterministic outcomes when their route requirements are met. Selecting all expected options does not prove executive judgment: Commercial Judgment cannot receive deterministic `Strong`, and recommendation evidence for Strategic Leadership does not create a deterministic leadership rating.

## Model Finance Director Answer

> I recommend conditional approval, not an unconditional commitment to all 20 starts today.
>
> H1 performance is strong on the income statement: revenue is up 22.2% and EBITDA is up 25.9%. However, cash fell GBP 2.70m. The main reason is working capital: receivables absorbed GBP 3.20m, inventory GBP 1.10m, and contract assets and prepayments GBP 0.60m, only partly offset by GBP 1.30m from payables and accruals. As a result, GBP 3.40m of EBITDA converted to negative GBP 0.20m before interest and tax and negative GBP 0.90m of operating cash after them.
>
> The proposed phasing costs GBP 0.58m in H2 and GBP 1.68m annually before productivity benefits. It lowers the forecast cash trough from GBP 3.50m to GBP 3.35m in September and December cash from GBP 5.00m to GBP 4.42m. That remains GBP 0.85m above the lender minimum, but it breaches the board's GBP 3.50m floor and relies on collections improving as forecast.
>
> I would authorize recruitment for the first 10 roles once we have a customer-level collections plan and a 13-week downside cash forecast. Their September starts should require either enough collections to preserve the GBP 3.50m floor or explicit board approval for a temporary exception. The second 10 starts should be gated on overdue receivables, delivery utilization, signed demand, and forecast liquidity. The CRO owns collections, the COO owns the role-level capacity case, and Finance reports weekly cash and working-capital progress.
>
> Before confirming the full plan, I need the aged receivables detail and committed payment dates, the role-by-role demand and time-to-productivity case, a downside cash sensitivity, and confirmation of the RCF renewal plan before March 2027. If those conditions are not met, we delay the second tranche or use contractors for the highest-priority work.

## Full Debrief

The central lesson is that income-statement growth does not by itself fund growth. Northstar generated GBP 3.40m of EBITDA, but operating assets expanded faster than operating liabilities. Receivables are the largest issue, with both concentration and overdue balances. Inventory and unbilled contract activity add further pressure. Supplier and accrual timing provided GBP 1.30m of temporary funding, which should not be mistaken for a permanent improvement.

The financial statements reconcile. Net fixed assets rose GBP 0.50m because GBP 1.20m of capital expenditure exceeded GBP 0.70m of depreciation and amortization. Equity rose by the GBP 2.00m net income. The working-capital movements in the balance sheet are the same movements in the cash bridge, and all operating, investing, and financing flows explain the GBP 2.70m fall from GBP 7.00m to GBP 4.30m.

The hiring proposal is affordable in the base forecast relative to the lender covenant, but it is not risk-free. It takes the company below the board's internal floor and creates GBP 1.68m of annual recurring cost before the pack evidences any incremental receipts. Cash does not run out in the base forecast because monthly cash flow turns positive, but no downside runway can be supported from the information provided. The undrawn facility provides flexibility, but its March 2027 expiry prevents it from being treated as permanent capital.

A Finance Director should not use incomplete information to avoid a recommendation. The stronger response gives a decision, quantifies the exposure, names what is unknown, and sets conditions that allow the business to preserve momentum while protecting liquidity. Conditional approval is the model route here, but approval, delay, or rejection can also be strong when the learner correctly uses the evidence and establishes proportionate safeguards.

## Learner Action Plan

1. Rebuild the EBITDA-to-cash bridge without looking at the answer and explain each working-capital movement in business language.
2. Draft a 60-second CEO recommendation using the sequence: decision, evidence, risk, conditions, owners.
3. Create one base and one downside hiring cash forecast, then identify the decision trigger that changes your recommendation.

## Review-Gate Record

- Chief Product Architect: confirmed alignment with FinanceOS, MVP scope, learner flow, and multiple defensible recommendations.
- Finance SME: confirmed financial realism, statement reconciliation, rubric logic, model answer, and debrief.
- Software Architect: confirmed the specification can be represented with simple content, structured inputs, and deterministic rules without new infrastructure.
- QA Engineer: confirmed acceptance criteria, arithmetic, balance-sheet and cash-bridge consistency, hiring phasing, liquidity conclusions, and evidence traceability.
- Documentation Engineer: confirmed terminology and links align with the repository sources of truth.
- Product Owner: accepted Scenario 001 for Phase 1 implementation subject to the Commercial Judgment deterministic-rating ceiling recorded in the evaluation contract.
