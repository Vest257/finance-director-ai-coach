"""Scenario 001 content, options, and reconciled finance constants."""

from __future__ import annotations

from textwrap import dedent

from finance_director_coach.models import ContentSection, RecommendationRoute, ScenarioContent

MONEY_TOLERANCE = 0.05
PERCENTAGE_TOLERANCE = 0.2

INCOME_STATEMENT: dict[str, tuple[float, float]] = {
    "Revenue": (18.00, 22.00),
    "Cost of sales": (-9.90, -11.90),
    "Gross profit": (8.10, 10.10),
    "Operating expenses before D&A": (-5.40, -6.70),
    "EBITDA": (2.70, 3.40),
    "Depreciation and amortization": (-0.60, -0.70),
    "Operating profit": (2.10, 2.70),
    "Net interest expense": (-0.25, -0.20),
    "Profit before tax": (1.85, 2.50),
    "Tax expense": (-0.37, -0.50),
    "Net income": (1.48, 2.00),
}

OPENING_ASSETS: dict[str, float] = {
    "Cash": 7.00,
    "Trade receivables": 6.00,
    "Inventory": 2.50,
    "Contract assets and prepayments": 1.00,
    "Property, equipment, and capitalized software": 5.00,
}
CURRENT_ASSETS: dict[str, float] = {
    "Cash": 4.30,
    "Trade receivables": 9.20,
    "Inventory": 3.60,
    "Contract assets and prepayments": 1.60,
    "Property, equipment, and capitalized software": 5.50,
}
OPENING_LIABILITIES_AND_EQUITY: dict[str, float] = {
    "Trade payables": 3.10,
    "Accruals and deferred revenue": 2.00,
    "Interest-bearing debt": 5.50,
    "Equity": 10.90,
}
CURRENT_LIABILITIES_AND_EQUITY: dict[str, float] = {
    "Trade payables": 4.00,
    "Accruals and deferred revenue": 2.40,
    "Interest-bearing debt": 4.90,
    "Equity": 12.90,
}

CASH_BRIDGE_COMPONENTS: dict[str, float] = {
    "EBITDA": 3.40,
    "Increase in trade receivables": -3.20,
    "Increase in inventory": -1.10,
    "Increase in contract assets and prepayments": -0.60,
    "Increase in trade payables": 0.90,
    "Increase in accruals and deferred revenue": 0.40,
    "Cash interest paid": -0.20,
    "Cash tax paid": -0.50,
    "Capital expenditure": -1.20,
    "Debt principal repaid": -0.60,
}

BASELINE_CLOSING_CASH: dict[str, float] = {
    "July": 3.80,
    "August": 3.50,
    "September": 3.50,
    "October": 3.80,
    "November": 4.30,
    "December": 5.00,
}
HIRING_STARTERS: dict[str, int] = {
    "July": 0,
    "August": 0,
    "September": 10,
    "October": 0,
    "November": 10,
    "December": 0,
}
ANNUAL_COST_PER_HIRE = 0.084
ONE_TIME_COST_PER_HIRE = 0.008
BOARD_CASH_FLOOR = 3.50
LENDER_MINIMUM_CASH = 2.50

CASH_DRIVER_OPTIONS: dict[str, str] = {
    "receivables": "Increase in trade receivables: GBP 3.20m use of cash",
    "inventory": "Increase in inventory: GBP 1.10m use of cash",
    "contract_assets": "Increase in contract assets and prepayments: GBP 0.60m use of cash",
    "payables_offset": "Increase in trade payables: GBP 0.90m cash offset",
    "accruals_offset": "Increase in accruals and deferred revenue: GBP 0.40m cash offset",
    "revenue_decline": "Revenue decline",
    "dividends": "Dividend payments",
}
EXPECTED_CASH_DRIVERS = frozenset(
    {"receivables", "inventory", "contract_assets", "payables_offset", "accruals_offset"}
)

RISK_OPTIONS: dict[str, str] = {
    "overdue_receivables": "Overdue and concentrated receivables",
    "board_floor_breach": "The hiring plan moves cash below the board floor",
    "collection_dependent_forecast": "The base forecast depends on improved collections",
    "inventory_contract_assets": "Inventory and contract-asset growth are absorbing cash",
    "rcf_expiry": "The undrawn RCF expires in March 2027",
    "unsupported_hiring_benefit": "No incremental hiring benefit is evidenced in the forecast",
    "missing_downside_case": "No quantified downside cash case is available",
    "lender_covenant_breached": "The lender minimum cash covenant is already breached",
    "assumptions_are_certain": "Collections and hiring benefits can be treated as certain",
}
CORE_RISKS = frozenset(
    {"overdue_receivables", "board_floor_breach", "collection_dependent_forecast"}
)
EXTENDED_RISKS = frozenset(
    {"inventory_contract_assets", "rcf_expiry", "unsupported_hiring_benefit", "missing_downside_case"}
)

THRESHOLD_OPTIONS: dict[str, str] = {
    "board_floor_breached": "The GBP 3.50m board floor is breached",
    "lender_minimum_retained": "The GBP 2.50m lender minimum remains satisfied",
    "board_floor_retained": "The board floor remains satisfied",
    "lender_covenant_breached": "The lender minimum cash covenant is breached",
}
EXPECTED_THRESHOLD_INTERPRETATIONS = frozenset(
    {"board_floor_breached", "lender_minimum_retained"}
)

MISSING_INFORMATION_OPTIONS: dict[str, str] = {
    "collections": "Customer-level aged receivables and committed collection dates",
    "downside_liquidity": "A quantified downside cash forecast",
    "hiring_business_case": "A role-level capacity, productivity, and revenue case",
    "time_to_productivity": "Evidence of time to productivity",
    "utilization_and_alternatives": "Utilization, attrition, and contractor alternatives",
    "recruitment_commitments": "Signed offers or unavoidable recruitment commitments",
    "board_exception": "Board approval for a temporary cash-floor exception",
    "rcf_renewal": "A confirmed RCF renewal or refinancing plan",
}
CORE_MISSING_INFORMATION = frozenset(
    {"collections", "downside_liquidity", "hiring_business_case"}
)

TRADEOFF_OPTIONS: dict[str, str] = {
    "growth_capacity": "Additional capacity may protect growth and delivery",
    "recurring_cost": "The hires create GBP 1.68m of annual recurring cost",
    "timing_risk": "Costs begin before incremental receipts are evidenced",
    "contractor_alternative": "Use contractors for urgent capacity",
    "phased_hiring_alternative": "Phase starts and gate the second tranche",
}
CORE_TRADEOFFS = frozenset({"growth_capacity", "recurring_cost", "timing_risk"})
ALTERNATIVE_CAPACITY_OPTIONS = frozenset({"contractor_alternative", "phased_hiring_alternative"})

ROUTE_SAFEGUARD_OPTIONS: dict[RecommendationRoute, dict[str, str]] = {
    RecommendationRoute.APPROVE: {
        "board_exception_or_funding": "Obtain a board-floor exception or committed funding source",
        "weekly_cash_monitoring": "Run weekly 13-week cash monitoring",
        "named_collections_action": "Assign a named owner and target for collections",
        "stop_start_trigger": "Set a trigger to slow or stop starts if cash deteriorates",
        "role_demand_case": "Complete the role-level demand case",
        "rcf_expiry_plan": "Agree an RCF expiry plan",
    },
    RecommendationRoute.CONDITIONALLY_APPROVE: {
        "first_tranche_condition": "Set a measurable condition for the first tranche",
        "second_tranche_gate": "Gate the second tranche on operating and cash evidence",
        "cash_threshold": "Set an explicit cash threshold",
        "named_owners": "Name owners for collections, capacity, and cash reporting",
        "downside_forecast": "Complete a downside cash forecast",
        "time_to_productivity": "Validate time to productivity",
    },
    RecommendationRoute.DELAY: {
        "decision_date": "Set a near-term decision date",
        "specific_information": "State the information required to reconsider",
        "interim_action": "Set an interim collections or capacity action",
        "conversion_threshold": "Define the threshold for approval or rejection",
    },
    RecommendationRoute.REJECT: {
        "financial_reason": "State the financial reason for rejecting the current plan",
        "revised_proposal_requirements": "Define requirements for a revised proposal",
        "capacity_alternative": "Provide a practical alternative for urgent capacity",
        "reconsideration_criterion": "Set a funding or downside criterion for reconsideration",
    },
}
REQUIRED_ROUTE_SAFEGUARDS: dict[RecommendationRoute, frozenset[str]] = {
    RecommendationRoute.APPROVE: frozenset(
        {"board_exception_or_funding", "weekly_cash_monitoring", "named_collections_action", "stop_start_trigger"}
    ),
    RecommendationRoute.CONDITIONALLY_APPROVE: frozenset(
        {"first_tranche_condition", "second_tranche_gate", "cash_threshold", "named_owners"}
    ),
    RecommendationRoute.DELAY: frozenset({"decision_date", "specific_information", "interim_action"}),
    RecommendationRoute.REJECT: frozenset(
        {"financial_reason", "revised_proposal_requirements", "capacity_alternative"}
    ),
}

RECOMMENDATION_OPTIONS: dict[str, str] = {
    RecommendationRoute.APPROVE.value: RecommendationRoute.APPROVE.label,
    RecommendationRoute.CONDITIONALLY_APPROVE.value: RecommendationRoute.CONDITIONALLY_APPROVE.label,
    RecommendationRoute.DELAY.value: RecommendationRoute.DELAY.label,
    RecommendationRoute.REJECT.value: RecommendationRoute.REJECT.label,
}


def balance_sheet_totals() -> tuple[float, float, float, float]:
    """Return opening and current asset and funding totals."""

    return (
        round(sum(OPENING_ASSETS.values()), 2),
        round(sum(OPENING_LIABILITIES_AND_EQUITY.values()), 2),
        round(sum(CURRENT_ASSETS.values()), 2),
        round(sum(CURRENT_LIABILITIES_AND_EQUITY.values()), 2),
    )


def operating_cash_before_interest_and_tax() -> float:
    keys = (
        "EBITDA",
        "Increase in trade receivables",
        "Increase in inventory",
        "Increase in contract assets and prepayments",
        "Increase in trade payables",
        "Increase in accruals and deferred revenue",
    )
    return round(sum(CASH_BRIDGE_COMPONENTS[key] for key in keys), 2)


def net_operating_cash() -> float:
    return round(
        operating_cash_before_interest_and_tax()
        + CASH_BRIDGE_COMPONENTS["Cash interest paid"]
        + CASH_BRIDGE_COMPONENTS["Cash tax paid"],
        2,
    )


def cash_bridge_change() -> float:
    return round(sum(CASH_BRIDGE_COMPONENTS.values()), 2)


def monthly_hiring_costs() -> dict[str, float]:
    """Calculate monthly cash cost from the two hiring tranches."""

    active_hires = 0
    monthly_costs: dict[str, float] = {}
    recurring_monthly_cost = ANNUAL_COST_PER_HIRE / 12
    for month, starters in HIRING_STARTERS.items():
        active_hires += starters
        cost = (active_hires * recurring_monthly_cost) + (starters * ONE_TIME_COST_PER_HIRE)
        monthly_costs[month] = round(cost, 2)
    return monthly_costs


def cash_after_hiring() -> dict[str, float]:
    cumulative_cost = 0.0
    result: dict[str, float] = {}
    hiring_costs = monthly_hiring_costs()
    for month, baseline_cash in BASELINE_CLOSING_CASH.items():
        cumulative_cost += hiring_costs[month]
        result[month] = round(baseline_cash - cumulative_cost, 2)
    return result


MODEL_ANSWER = dedent(
    """
    I recommend conditional approval, not an unconditional commitment to all 20 starts today.

    H1 revenue is up 22.2% and EBITDA is up 25.9%, but cash fell GBP 2.70m. Receivables absorbed GBP 3.20m, inventory GBP 1.10m, and contract assets and prepayments GBP 0.60m, only partly offset by GBP 1.30m from payables and accruals. GBP 3.40m of EBITDA therefore converted to negative GBP 0.20m before interest and tax and negative GBP 0.90m of operating cash after them.

    The proposed phasing costs GBP 0.58m in H2 and GBP 1.68m annually before productivity benefits. It lowers the cash trough from GBP 3.50m to GBP 3.35m and December cash from GBP 5.00m to GBP 4.42m. That remains GBP 0.85m above the lender minimum but breaches the board floor and relies on collections improving as forecast.

    I would authorize recruitment for the first 10 roles once we have a customer-level collections plan and a 13-week downside cash forecast. September starts require enough collections to preserve the board floor or explicit board approval for an exception. The second 10 starts are gated on overdue receivables, delivery utilization, signed demand, and forecast liquidity. The CRO owns collections, the COO owns the role-level capacity case, and Finance reports weekly cash and working-capital progress.

    Before confirming the full plan, I need aged receivables and payment dates, the role-level demand and time-to-productivity case, a downside cash sensitivity, and the RCF renewal plan. If those conditions are not met, we delay the second tranche or use contractors for priority work.
    """
).strip()

DEBRIEF = dedent(
    """
    The central lesson is that income-statement growth does not itself fund growth. Northstar generated GBP 3.40m of EBITDA, but operating assets expanded faster than operating liabilities. Receivables are the largest issue, with concentration and overdue balances. Inventory and unbilled activity add pressure. Supplier and accrual timing supplied GBP 1.30m of temporary funding and should not be mistaken for permanent improvement.

    The statements reconcile. Net fixed assets rose GBP 0.50m because GBP 1.20m of capital expenditure exceeded GBP 0.70m of depreciation and amortization. Equity rose by GBP 2.00m net income. The balance-sheet working-capital movements are the same movements in the cash bridge, and all operating, investing, and financing flows explain the GBP 2.70m decline from GBP 7.00m to GBP 4.30m.

    The hiring proposal is affordable in the base forecast relative to the lender minimum, but it is not risk-free. It takes cash below the board floor and creates GBP 1.68m of annual recurring cost before incremental receipts are evidenced. Cash does not run out in the base forecast because monthly cash flow turns positive, but no downside runway can be supported. The undrawn facility provides flexibility, while its March 2027 expiry means it is not permanent capital.

    A Finance Director should still give a decision under incomplete information. A stronger response quantifies the exposure, names what is unknown, and sets proportionate conditions. Conditional approval is the model route, but approval, delay, or rejection can be equally defensible when supported by the financial evidence and route-appropriate safeguards. Deterministic selections can demonstrate adequate analysis; they do not prove strong executive judgment.
    """
).strip()

SCENARIO_001 = ScenarioContent(
    scenario_id="SCN-001",
    title="Growth With Falling Cash: Should We Hire 20 People?",
    learner_role=(
        "You are Finance Director of Northstar Monitoring Ltd. You own the cash forecast, "
        "attend board meetings, and must make a recommendation to the CEO."
    ),
    company_context=(
        "Northstar is a fictional UK industrial monitoring business with 120 employees. "
        "Enterprise deployments have accelerated growth, but hardware and implementation "
        "spend occur before customer cash is collected. The CEO wants 20 additional hires."
    ),
    financial_pack=(
        ContentSection(
            "Income statement - GBP m",
            dedent(
                """
                Six months ended 30 June             H1 2025   H1 2026
                Revenue                                18.00     22.00
                Gross profit                            8.10     10.10
                EBITDA                                  2.70      3.40
                Operating profit                        2.10      2.70
                Net income                              1.48      2.00
                """
            ).strip(),
        ),
        ContentSection(
            "Balance sheet - GBP m",
            dedent(
                """
                                                    Dec 2025  Jun 2026
                Cash                                    7.00      4.30
                Trade receivables                       6.00      9.20
                Inventory                               2.50      3.60
                Contract assets and prepayments         1.00      1.60
                Net fixed assets                        5.00      5.50
                Total assets                           21.50     24.20

                Trade payables                          3.10      4.00
                Accruals and deferred revenue           2.00      2.40
                Interest-bearing debt                   5.50      4.90
                Equity                                 10.90     12.90
                Total liabilities and equity           21.50     24.20
                """
            ).strip(),
        ),
        ContentSection(
            "EBITDA-to-cash bridge - H1 2026, GBP m",
            dedent(
                """
                EBITDA                                           3.40
                Receivables movement                             (3.20)
                Inventory movement                               (1.10)
                Contract assets and prepayments                  (0.60)
                Payables and accruals offsets                     1.30
                Operating cash before interest and tax          (0.20)
                Cash interest and tax                            (0.70)
                Net operating cash                               (0.90)
                Capital expenditure and debt repayment           (1.80)
                Net decrease in cash                             (2.70)
                """
            ).strip(),
        ),
        ContentSection(
            "Working capital and liquidity",
            dedent(
                """
                DSO rose from 61 to 76 days. GBP 2.00m of receivables is over 30 days overdue.
                Inventory days rose from 46 to 55. Five customers hold GBP 5.60m of receivables.
                Baseline cash reaches GBP 3.50m in August and September, then GBP 5.00m in December.
                The board cash floor is GBP 3.50m. The lender minimum cash covenant is GBP 2.50m.
                A GBP 3.00m undrawn RCF expires in March 2027. No downside case is provided.
                """
            ).strip(),
        ),
        ContentSection(
            "Proposed 20 hires",
            dedent(
                """
                Ten starters are proposed for September and ten for November.
                Recurring cost is GBP 84,000 per person per year; onboarding is GBP 8,000 each.
                H2 cost is GBP 0.58m and annual recurring cost is GBP 1.68m.
                Cash after hiring reaches a GBP 3.35m low in September and GBP 4.42m in December.
                No incremental revenue or receipts from the hires are included in the forecast.
                """
            ).strip(),
        ),
    ),
    initial_question=(
        "Revenue and EBITDA are ahead, and delivery says we are turning away work. "
        "I want to hire all 20 people now. Are you approving the plan?"
    ),
    model_answer=MODEL_ANSWER,
    debrief=DEBRIEF,
    self_review_checklist=(
        "Did I lead with a clear decision?",
        "Did I distinguish EBITDA growth from cash conversion?",
        "Did I quantify working-capital movements and liquidity?",
        "Did I separate the board floor from the lender covenant?",
        "Did I explain practical conditions and named actions?",
        "Did I identify missing information without avoiding the decision?",
        "Did I communicate concisely and constructively?",
    ),
    action_plan=(
        "Rebuild the EBITDA-to-cash bridge and explain each movement in business language.",
        "Draft a 60-second CEO recommendation: decision, evidence, risk, conditions, owners.",
        "Create a base and downside hiring cash forecast and identify the decision trigger.",
    ),
    reconciliation_summary=(
        "Opening and current balance sheets reconcile at GBP 21.50m and GBP 24.20m. "
        "Operating cash before interest and tax is negative GBP 0.20m; net operating cash "
        "is negative GBP 0.90m; capex and debt repayment take the total cash decline to "
        "GBP 2.70m. Hiring costs GBP 0.58m in H2, producing a GBP 3.35m low point and "
        "GBP 4.42m December cash."
    ),
)
