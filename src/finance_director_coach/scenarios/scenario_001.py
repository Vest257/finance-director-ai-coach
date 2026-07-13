"""Scenario 001 content, options, and reconciled finance constants."""

from __future__ import annotations

from textwrap import dedent

from finance_director_coach.models import ContentSection, RecommendationRoute, ScenarioContent

MONEY_TOLERANCE = 0.05
PERCENTAGE_TOLERANCE = 0.2
MONETARY_INPUT_GUIDANCE = (
    "All monetary answers are entered in GBP millions.\n\n"
    "1.00 = GBP 1,000,000\n\n"
    "0.10 = GBP 100,000"
)
HIRING_UNIT_WARNING = (
    "Entering 580 would mean GBP 580 million, not GBP 580,000. "
    "Use the GBP-million format shown above."
)

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
    "recurring_cost": "The hires create a material annual recurring cost",
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


def income_statement_growth(line_item: str) -> float:
    """Return rounded percentage growth for a comparative income-statement line."""

    prior, current = INCOME_STATEMENT[line_item]
    return round((current - prior) / prior * 100, 1)


def cash_decrease() -> float:
    """Return the positive decrease between opening and current cash."""

    return round(OPENING_ASSETS["Cash"] - CURRENT_ASSETS["Cash"], 2)


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


def h2_hiring_cost() -> float:
    """Return the total hiring cash cost in the July-to-December forecast."""

    return round(sum(monthly_hiring_costs().values()), 2)


def annual_recurring_hiring_cost() -> float:
    """Return annual recurring cost for every proposed starter."""

    return round(sum(HIRING_STARTERS.values()) * ANNUAL_COST_PER_HIRE, 2)


def hiring_cash_low_point() -> float:
    """Return the lowest monthly closing cash balance after hiring costs."""

    return min(cash_after_hiring().values())


def hiring_december_cash() -> float:
    """Return December closing cash after cumulative hiring costs."""

    return cash_after_hiring()["December"]


def board_floor_shortfall() -> float:
    """Return the positive shortfall below the internal board cash floor."""

    return round(BOARD_CASH_FLOOR - hiring_cash_low_point(), 2)


def lender_minimum_headroom() -> float:
    """Return positive headroom above the lender minimum at the low point."""

    return round(hiring_cash_low_point() - LENDER_MINIMUM_CASH, 2)


EXPECTED_REVENUE_GROWTH = income_statement_growth("Revenue")
EXPECTED_EBITDA_GROWTH = income_statement_growth("EBITDA")
EXPECTED_CASH_DECREASE = cash_decrease()
EXPECTED_OPERATING_CASH = operating_cash_before_interest_and_tax()
EXPECTED_NET_OPERATING_CASH = net_operating_cash()
EXPECTED_H2_HIRING_COST = h2_hiring_cost()
EXPECTED_ANNUAL_HIRING_COST = annual_recurring_hiring_cost()
EXPECTED_CASH_LOW_POINT = hiring_cash_low_point()
EXPECTED_DECEMBER_CASH = hiring_december_cash()
EXPECTED_BOARD_SHORTFALL = board_floor_shortfall()
EXPECTED_LENDER_HEADROOM = lender_minimum_headroom()


def _worked_calculation_explanations() -> dict[str, str]:
    revenue_prior, revenue_current = INCOME_STATEMENT["Revenue"]
    ebitda_prior, ebitda_current = INCOME_STATEMENT["EBITDA"]
    opening_cash = OPENING_ASSETS["Cash"]
    closing_cash = CURRENT_ASSETS["Cash"]
    monthly_cost_per_hire = ANNUAL_COST_PER_HIRE / 12
    annual_cost_gbp = ANNUAL_COST_PER_HIRE * 1_000_000
    monthly_cost_gbp = monthly_cost_per_hire * 1_000_000
    onboarding_cost_gbp = ONE_TIME_COST_PER_HIRE * 1_000_000
    september_starters = HIRING_STARTERS["September"]
    november_starters = HIRING_STARTERS["November"]
    forecast_months = tuple(HIRING_STARTERS)
    september_recurring_months = len(forecast_months) - forecast_months.index("September")
    november_recurring_months = len(forecast_months) - forecast_months.index("November")
    september_cost = round(
        september_starters
        * (monthly_cost_per_hire * september_recurring_months + ONE_TIME_COST_PER_HIRE),
        2,
    )
    november_cost = round(
        november_starters
        * (monthly_cost_per_hire * november_recurring_months + ONE_TIME_COST_PER_HIRE),
        2,
    )
    monthly_costs = monthly_hiring_costs()
    hiring_forecast = cash_after_hiring()

    return {
        "E-001": dedent(
            f"""
            **Revenue growth**

            Formula: (current period - prior period) / prior period x 100.

            (GBP {revenue_current:.2f}m - GBP {revenue_prior:.2f}m) / GBP {revenue_prior:.2f}m x 100
            = {EXPECTED_REVENUE_GROWTH:.1f}%.

            **EBITDA growth**

            (GBP {ebitda_current:.2f}m - GBP {ebitda_prior:.2f}m) / GBP {ebitda_prior:.2f}m x 100
            = {EXPECTED_EBITDA_GROWTH:.1f}%.

            Enter **{EXPECTED_REVENUE_GROWTH:.1f}** and **{EXPECTED_EBITDA_GROWTH:.1f}**. The fields expect percentage points, not decimal fractions.
            """
        ).strip(),
        "E-002": dedent(
            f"""
            Formula: opening cash - closing cash = cash decrease.

            GBP {opening_cash:.2f}m - GBP {closing_cash:.2f}m = GBP {EXPECTED_CASH_DECREASE:.2f}m.

            The field asks for the decrease as a positive GBP-million amount, so enter **{EXPECTED_CASH_DECREASE:.2f}**.
            """
        ).strip(),
        "E-003": dedent(
            f"""
            Cash uses carry minus signs; increases in payables and accruals are positive cash offsets.

            **Operating cash before interest and tax**

            GBP {CASH_BRIDGE_COMPONENTS['EBITDA']:.2f}m EBITDA
            - GBP {abs(CASH_BRIDGE_COMPONENTS['Increase in trade receivables']):.2f}m receivables
            - GBP {abs(CASH_BRIDGE_COMPONENTS['Increase in inventory']):.2f}m inventory
            - GBP {abs(CASH_BRIDGE_COMPONENTS['Increase in contract assets and prepayments']):.2f}m contract assets and prepayments
            + GBP {CASH_BRIDGE_COMPONENTS['Increase in trade payables']:.2f}m payables
            + GBP {CASH_BRIDGE_COMPONENTS['Increase in accruals and deferred revenue']:.2f}m accruals and deferred revenue
            = **GBP {EXPECTED_OPERATING_CASH:.2f}m**.

            **Net operating cash**

            GBP {EXPECTED_OPERATING_CASH:.2f}m
            - GBP {abs(CASH_BRIDGE_COMPONENTS['Cash interest paid']):.2f}m cash interest
            - GBP {abs(CASH_BRIDGE_COMPONENTS['Cash tax paid']):.2f}m cash tax
            = **GBP {EXPECTED_NET_OPERATING_CASH:.2f}m**.

            Enter **{EXPECTED_OPERATING_CASH:.2f}** and **{EXPECTED_NET_OPERATING_CASH:.2f}**. Keep the minus signs because both are cash outflows in GBP millions.
            """
        ).strip(),
        "E-006": dedent(
            f"""
            Annual fully loaded cost per hire is GBP {annual_cost_gbp:,.0f}.

            GBP {annual_cost_gbp:,.0f} / 12 = GBP {monthly_cost_gbp:,.0f} monthly recurring cost per hire.

            **September cohort:** {september_starters} starters incur four months of recurring cost plus onboarding:
            {september_starters} x ({september_recurring_months} x GBP {monthly_cost_gbp:,.0f} + GBP {onboarding_cost_gbp:,.0f})
            = GBP {september_cost * 1_000_000:,.0f} = **GBP {september_cost:.2f}m**.

            **November cohort:** {november_starters} starters incur two months of recurring cost plus onboarding:
            {november_starters} x ({november_recurring_months} x GBP {monthly_cost_gbp:,.0f} + GBP {onboarding_cost_gbp:,.0f})
            = GBP {november_cost * 1_000_000:,.0f} = **GBP {november_cost:.2f}m**.

            H2 total = GBP {september_cost:.2f}m + GBP {november_cost:.2f}m = **GBP {EXPECTED_H2_HIRING_COST:.2f}m**.

            Annual recurring cost = {sum(HIRING_STARTERS.values())} x GBP {annual_cost_gbp:,.0f}
            = GBP {EXPECTED_ANNUAL_HIRING_COST * 1_000_000:,.0f} = **GBP {EXPECTED_ANNUAL_HIRING_COST:.2f}m**.

            Enter **{EXPECTED_H2_HIRING_COST:.2f}** and **{EXPECTED_ANNUAL_HIRING_COST:.2f}** because the fields use GBP millions.
            """
        ).strip(),
        "E-007": dedent(
            f"""
            Apply each month's hiring cash cost to the visible baseline forecast and carry the cost forward cumulatively.

            Monthly hiring cash costs in GBP millions are: July {monthly_costs['July']:.2f}, August {monthly_costs['August']:.2f}, September {monthly_costs['September']:.2f}, October {monthly_costs['October']:.2f}, November {monthly_costs['November']:.2f}, December {monthly_costs['December']:.2f}.

            September: baseline GBP {BASELINE_CLOSING_CASH['September']:.2f}m - cumulative hiring cost GBP {sum(monthly_costs[month] for month in ('July', 'August', 'September')):.2f}m = **GBP {hiring_forecast['September']:.2f}m**. This is the low point.

            December: baseline GBP {BASELINE_CLOSING_CASH['December']:.2f}m - cumulative H2 hiring cost GBP {EXPECTED_H2_HIRING_COST:.2f}m = **GBP {EXPECTED_DECEMBER_CASH:.2f}m**.

            Enter **{EXPECTED_CASH_LOW_POINT:.2f}** for the low point and **{EXPECTED_DECEMBER_CASH:.2f}** for December cash; both fields use GBP millions.
            """
        ).strip(),
        "E-008": dedent(
            f"""
            Compare the GBP {EXPECTED_CASH_LOW_POINT:.2f}m hiring-case low point with each threshold separately.

            **Board-floor shortfall:** GBP {BOARD_CASH_FLOOR:.2f}m - GBP {EXPECTED_CASH_LOW_POINT:.2f}m = **GBP {EXPECTED_BOARD_SHORTFALL:.2f}m**. The internal board floor is breached.

            **Lender-covenant headroom:** GBP {EXPECTED_CASH_LOW_POINT:.2f}m - GBP {LENDER_MINIMUM_CASH:.2f}m = **GBP {EXPECTED_LENDER_HEADROOM:.2f}m**. The lender minimum remains satisfied.

            Enter the positive GBP-million amounts **{EXPECTED_BOARD_SHORTFALL:.2f}** and **{EXPECTED_LENDER_HEADROOM:.2f}**.
            """
        ).strip(),
    }


WORKED_CALCULATION_EXPLANATIONS = _worked_calculation_explanations()


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
                Opening cash at 31 December 2025                  7.00
                EBITDA                                            3.40
                Increase in trade receivables                    (3.20)
                Increase in inventory                            (1.10)
                Increase in contract assets and prepayments      (0.60)
                Increase in trade payables                        0.90
                Increase in accruals and deferred revenue         0.40
                Cash interest paid                               (0.20)
                Cash tax paid                                    (0.50)
                Capital expenditure                              (1.20)
                Debt principal repaid                            (0.60)
                """
            ).strip(),
        ),
        ContentSection(
            "Working capital and liquidity",
            dedent(
                """
                DSO rose from 61 to 76 days. GBP 2.00m of receivables is over 30 days overdue.
                Inventory days rose from 46 to 55. Five customers hold GBP 5.60m of receivables.
                The board cash floor is GBP 3.50m. The lender minimum cash covenant is GBP 2.50m.
                A GBP 3.00m undrawn RCF expires in March 2027. No downside case is provided.
                """
            ).strip(),
        ),
        ContentSection(
            "Baseline monthly closing-cash forecast - GBP m",
            dedent(
                """
                July                                             3.80
                August                                           3.50
                September                                        3.50
                October                                          3.80
                November                                         4.30
                December                                         5.00
                """
            ).strip(),
        ),
        ContentSection(
            "Proposed 20 hires",
            dedent(
                """
                Ten starters are proposed for September and ten for November.
                Annual fully loaded cost is GBP 84,000 per hire; one-time onboarding cost is GBP 8,000 per hire.
                Recurring cost accrues evenly by month from and including each starter's start month.
                One-time onboarding cost is paid in each starter's start month.
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
