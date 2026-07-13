"""Scenario 002 content and reconciled commercial-finance calculations."""

from __future__ import annotations

from dataclasses import dataclass, field
from textwrap import dedent

from finance_director_coach.models import ContentSection, RecommendationRoute, ScenarioContent
from finance_director_coach.scenarios.contracts import ScenarioMetadata

MONEY_TOLERANCE = 0.05
PERCENTAGE_TOLERANCE = 0.2
MONETARY_INPUT_GUIDANCE = (
    "All monetary answers are entered in GBP millions.\n\n"
    "1.00 = GBP 1,000,000\n\n"
    "0.10 = GBP 100,000"
)

COMPANY_INCOME_STATEMENT: dict[str, tuple[float, float]] = {
    "Revenue": (40.00, 48.00),
    "Cost of sales": (-22.00, -29.76),
    "Gross profit": (18.00, 18.24),
    "Operating expenses": (-13.20, -14.88),
    "EBITDA": (4.80, 3.36),
}

CUSTOMER_STANDARD_PRICE = 10.50
CUSTOMER_REPORTED_REVENUE = 9.00
CUSTOMER_DIRECT_COSTS: dict[str, float] = {
    "Redeployable delivery capacity after 90 days": 2.00,
    "Delivery notice and tooling commitments": 0.50,
    "Implementation overruns": 1.20,
    "Incremental support": 1.10,
    "Customer-specific engineering": 0.70,
    "Service-level credits": 0.50,
}
ALLOCATED_HEAD_OFFICE_OVERHEAD = 0.80
AVOIDABLE_DIRECT_COST_KEYS = frozenset(
    {
        "Redeployable delivery capacity after 90 days",
        "Implementation overruns",
        "Incremental support",
        "Customer-specific engineering",
    }
)
RETAINED_DIRECT_COST_KEYS = frozenset(
    {"Delivery notice and tooling commitments", "Service-level credits"}
)
TARGET_CONTRIBUTION_MARGIN = 0.45
REQUESTED_ADDITIONAL_DISCOUNT_RATE = 0.05
CUSTOMER_DELIVERY_CAPACITY_PERCENT = 0.28
CUSTOMER_SENIOR_ENGINEERING_PERCENT = 0.35
REPLACEMENT_CONTRIBUTION_AFTER_REDEPLOYMENT = 3.70

MARGIN_INTERPRETATION_OPTIONS: dict[str, str] = {
    "growth_with_margin_erosion": "Revenue has grown, but lower gross and EBITDA margins show the growth is eroding value.",
    "growth_proves_profitability": "Revenue growth proves the customer is economically attractive.",
    "margin_decline_is_irrelevant": "Margin deterioration is irrelevant while total company revenue is increasing.",
    "discount_is_cash_neutral": "An additional discount changes revenue but not contribution.",
}
EXPECTED_MARGIN_INTERPRETATION = "growth_with_margin_erosion"

DRIVER_OPTIONS: dict[str, str] = {
    "deep_discount": "Deep commercial discount below list price",
    "implementation_overruns": "Implementation overruns",
    "support_requirements": "Higher support requirements",
    "customer_engineering": "Customer-specific engineering",
    "service_levels": "Unfavorable service-level commitments",
    "price_indexation_delay": "Delayed price indexation",
    "capacity_diversion": "Capacity diverted from more profitable customers",
    "improved_collections": "Improved collections",
}
AVOIDABLE_COST_OPTIONS: dict[str, str] = {
    "delivery_capacity": "GBP 2.00m of redeployable delivery capacity after 90 days",
    "implementation_overruns": "GBP 1.20m of implementation overruns",
    "incremental_support": "GBP 1.10m of incremental support",
    "customer_engineering": "GBP 0.70m of customer-specific engineering",
    "notice_and_tooling": "GBP 0.50m of delivery notice and tooling commitments",
    "service_level_credits": "GBP 0.50m of service-level credits retained during transition",
    "allocated_overhead": "GBP 0.80m of allocated head-office overhead",
}
EXPECTED_AVOIDABLE_COSTS = frozenset(
    {"delivery_capacity", "implementation_overruns", "incremental_support", "customer_engineering"}
)

MISSING_INFORMATION_OPTIONS: dict[str, str] = {
    "retention_response": "Customer retention and response to pricing or scope changes",
    "capacity_redeployment": "Timing and confidence of redeploying capacity to profitable demand",
    "contract_exit_costs": "Contract termination, notice, and service-transition obligations",
    "ceo_preference": "The CEO's personal preference",
    "historic_revenue": "The customer's historical revenue only",
}
EXPECTED_MISSING_INFORMATION = frozenset(
    {"retention_response", "capacity_redeployment", "contract_exit_costs"}
)

DECISION_CONDITION_OPTIONS: dict[str, str] = {
    "target_margin": "Renewal economics meet the defined 45% contribution-margin target",
    "scope_service_reset": "Scope, service levels, and implementation commitments are reset to a deliverable level",
    "extra_discount": "Grant the requested extra discount without a commercial return",
    "revenue_credibility": "Retain the customer for market credibility regardless of economics",
    "capacity_release": "Capacity can be released or redeployed if commercial terms cannot be repaired",
}
RENEWAL_DECISION_CONDITIONS = frozenset({"target_margin", "scope_service_reset"})
REJECT_DECISION_CONDITIONS = frozenset({"capacity_release", "target_margin"})
DECISION_CONDITION_EXPECTATIONS: dict[RecommendationRoute, str] = {
    RecommendationRoute.APPROVE: (
        "For Approve, select exactly target contribution margin and scope/service reset"
    ),
    RecommendationRoute.CONDITIONALLY_APPROVE: (
        "For Conditionally approve, select exactly target contribution margin and scope/service reset"
    ),
    RecommendationRoute.DELAY: (
        "For Delay, select exactly two conditions: capacity release plus either target contribution margin or scope/service reset"
    ),
    RecommendationRoute.REJECT: (
        "For Reject, select exactly capacity release and target contribution margin"
    ),
}

ROUTE_SAFEGUARD_OPTIONS: dict[RecommendationRoute, dict[str, str]] = {
    RecommendationRoute.APPROVE: {
        "signed_scope": "Sign a revised scope and service-level schedule before renewal",
        "margin_monitoring": "Set a monthly contribution-margin and delivery-cost review",
        "discount_trade": "Trade any discount for committed volume, reduced scope, or paid implementation",
        "exit_trigger": "Set an exit or escalation trigger if economics deteriorate",
    },
    RecommendationRoute.CONDITIONALLY_APPROVE: {
        "target_margin": "Secure pricing and scope that meet the 45% contribution-margin target",
        "implementation_cap": "Cap implementation overruns and require paid change control",
        "service_reset": "Reset support and service-level commitments to a costed service model",
        "commercial_owner": "Name commercial and delivery owners for monthly economics reviews",
    },
    RecommendationRoute.DELAY: {
        "negotiation_window": "Set a short negotiation window and decision date",
        "profitability_case": "Complete a validated customer profitability and exit-cost case",
        "interim_controls": "Freeze additional scope and require change control during negotiation",
        "replacement_plan": "Validate capacity redeployment and replacement-contribution assumptions",
    },
    RecommendationRoute.REJECT: {
        "transition_plan": "Agree an orderly customer and delivery transition plan",
        "capacity_redeployment": "Redeploy or resize capacity against validated profitable demand",
        "commercial_reentry": "Set economics required before any future proposal is considered",
        "stakeholder_plan": "Communicate the financial rationale and customer-management plan",
    },
}
REQUIRED_ROUTE_SAFEGUARDS: dict[RecommendationRoute, frozenset[str]] = {
    RecommendationRoute.APPROVE: frozenset({"signed_scope", "margin_monitoring", "discount_trade"}),
    RecommendationRoute.CONDITIONALLY_APPROVE: frozenset(
        {"target_margin", "implementation_cap", "service_reset"}
    ),
    RecommendationRoute.DELAY: frozenset(
        {"negotiation_window", "profitability_case", "interim_controls"}
    ),
    RecommendationRoute.REJECT: frozenset(
        {"transition_plan", "capacity_redeployment", "commercial_reentry"}
    ),
}
RECOMMENDATION_OPTIONS: dict[str, str] = {
    RecommendationRoute.APPROVE.value: RecommendationRoute.APPROVE.label,
    RecommendationRoute.CONDITIONALLY_APPROVE.value: RecommendationRoute.CONDITIONALLY_APPROVE.label,
    RecommendationRoute.DELAY.value: RecommendationRoute.DELAY.label,
    RecommendationRoute.REJECT.value: RecommendationRoute.REJECT.label,
}


def income_statement_growth(line_item: str) -> float:
    prior, current = COMPANY_INCOME_STATEMENT[line_item]
    return round((current - prior) / prior * 100, 1)


def margin(line_item: str, period_index: int) -> float:
    return round(
        COMPANY_INCOME_STATEMENT[line_item][period_index]
        / COMPANY_INCOME_STATEMENT["Revenue"][period_index]
        * 100,
        1,
    )


def customer_direct_cost() -> float:
    return round(sum(CUSTOMER_DIRECT_COSTS.values()), 2)


def existing_discount_amount() -> float:
    return round(CUSTOMER_STANDARD_PRICE - CUSTOMER_REPORTED_REVENUE, 2)


def existing_discount_percentage() -> float:
    return round(existing_discount_amount() / CUSTOMER_STANDARD_PRICE * 100, 1)


def quantified_margin_driver_values() -> dict[str, float]:
    """Return value leaks that can be ranked from learner-visible raw inputs."""

    return {
        "deep_discount": existing_discount_amount(),
        "implementation_overruns": CUSTOMER_DIRECT_COSTS["Implementation overruns"],
        "support_requirements": CUSTOMER_DIRECT_COSTS["Incremental support"],
        "customer_engineering": CUSTOMER_DIRECT_COSTS["Customer-specific engineering"],
        "service_levels": CUSTOMER_DIRECT_COSTS["Service-level credits"],
    }


def ranked_quantified_margin_drivers() -> tuple[str, ...]:
    return tuple(
        driver
        for driver, _ in sorted(
            quantified_margin_driver_values().items(), key=lambda item: (-item[1], item[0])
        )
    )


def customer_contribution() -> float:
    return round(CUSTOMER_REPORTED_REVENUE - customer_direct_cost(), 2)


def customer_contribution_margin() -> float:
    return round(customer_contribution() / CUSTOMER_REPORTED_REVENUE * 100, 1)


def economically_attractive_revenue() -> float:
    return round(customer_direct_cost() / (1 - TARGET_CONTRIBUTION_MARGIN), 2)


def required_price_increase() -> float:
    return round(economically_attractive_revenue() - CUSTOMER_REPORTED_REVENUE, 2)


def required_price_increase_percent() -> float:
    return round(required_price_increase() / CUSTOMER_REPORTED_REVENUE * 100, 1)


def required_cost_reduction() -> float:
    target_cost = CUSTOMER_REPORTED_REVENUE * (1 - TARGET_CONTRIBUTION_MARGIN)
    return round(customer_direct_cost() - target_cost, 2)


def requested_discount_amount() -> float:
    return round(CUSTOMER_REPORTED_REVENUE * REQUESTED_ADDITIONAL_DISCOUNT_RATE, 2)


def contribution_after_requested_discount() -> float:
    return round(customer_contribution() - requested_discount_amount(), 2)


def contribution_margin_after_requested_discount() -> float:
    discounted_revenue = CUSTOMER_REPORTED_REVENUE - requested_discount_amount()
    return round(contribution_after_requested_discount() / discounted_revenue * 100, 1)


def avoidable_exit_cost() -> float:
    return round(sum(CUSTOMER_DIRECT_COSTS[key] for key in AVOIDABLE_DIRECT_COST_KEYS), 2)


def retained_direct_cost() -> float:
    return round(sum(CUSTOMER_DIRECT_COSTS[key] for key in RETAINED_DIRECT_COST_KEYS), 2)


def current_company_ebitda() -> float:
    return COMPANY_INCOME_STATEMENT["EBITDA"][1]


def proposed_renewal_ebitda() -> float:
    return round(current_company_ebitda() - requested_discount_amount(), 2)


def target_renewal_ebitda() -> float:
    return round(current_company_ebitda() + required_price_increase(), 2)


def exit_and_redeploy_ebitda() -> float:
    return round(
        current_company_ebitda()
        - CUSTOMER_REPORTED_REVENUE
        + avoidable_exit_cost()
        + REPLACEMENT_CONTRIBUTION_AFTER_REDEPLOYMENT,
        2,
    )


def decision_conditions_are_valid(
    route: RecommendationRoute | None, conditions: frozenset[str]
) -> bool:
    if route is None or len(conditions) != 2:
        return False
    if route is RecommendationRoute.DELAY:
        return "capacity_release" in conditions and len(
            conditions.intersection(RENEWAL_DECISION_CONDITIONS)
        ) == 1
    if route is RecommendationRoute.REJECT:
        return conditions == REJECT_DECISION_CONDITIONS
    return conditions == RENEWAL_DECISION_CONDITIONS


def decision_condition_expectation(route: RecommendationRoute | None) -> str:
    if route is None:
        return "Choose a recommendation route, then select exactly two compatible decision conditions"
    return DECISION_CONDITION_EXPECTATIONS[route]


def decision_condition_feedback(route: RecommendationRoute | None) -> str:
    if route in {RecommendationRoute.APPROVE, RecommendationRoute.CONDITIONALLY_APPROVE}:
        return "You set conditions that repair both the economics and operating model."
    if route is RecommendationRoute.DELAY:
        return "You set a condition to test repair and a condition to release or redeploy capacity if it is not achievable."
    if route is RecommendationRoute.REJECT:
        return "You tied rejection to unrepaired economics and credible capacity release or redeployment."
    return "You set conditions that match the selected decision route."


EXPECTED_REVENUE_GROWTH = income_statement_growth("Revenue")
EXPECTED_PRIOR_GROSS_MARGIN = margin("Gross profit", 0)
EXPECTED_CURRENT_GROSS_MARGIN = margin("Gross profit", 1)
EXPECTED_PRIOR_EBITDA_MARGIN = margin("EBITDA", 0)
EXPECTED_CURRENT_EBITDA_MARGIN = margin("EBITDA", 1)
EXPECTED_CUSTOMER_CONTRIBUTION = customer_contribution()
EXPECTED_CUSTOMER_CONTRIBUTION_MARGIN = customer_contribution_margin()
EXPECTED_ECONOMIC_REVENUE = economically_attractive_revenue()
EXPECTED_PRICE_INCREASE = required_price_increase()
EXPECTED_PRICE_INCREASE_PERCENT = required_price_increase_percent()
EXPECTED_COST_REDUCTION = required_cost_reduction()
EXPECTED_REQUESTED_DISCOUNT = requested_discount_amount()
EXPECTED_DISCOUNTED_CONTRIBUTION_MARGIN = contribution_margin_after_requested_discount()
EXPECTED_PROPOSED_RENEWAL_EBITDA = proposed_renewal_ebitda()
EXPECTED_TARGET_RENEWAL_EBITDA = target_renewal_ebitda()
EXPECTED_EXIT_AND_REDEPLOY_EBITDA = exit_and_redeploy_ebitda()
EXPECTED_TOP_DRIVERS = frozenset(ranked_quantified_margin_drivers()[:3])


def _worked_calculation_explanations() -> dict[str, str]:
    prior_revenue, current_revenue = COMPANY_INCOME_STATEMENT["Revenue"]
    prior_gp, current_gp = COMPANY_INCOME_STATEMENT["Gross profit"]
    prior_ebitda, current_ebitda = COMPANY_INCOME_STATEMENT["EBITDA"]
    return {
        "SCN-002-E-001": dedent(
            f"""
            Formula: (current revenue - prior revenue) / prior revenue x 100.

            (GBP {current_revenue:.2f}m - GBP {prior_revenue:.2f}m) / GBP {prior_revenue:.2f}m x 100
            = **{EXPECTED_REVENUE_GROWTH:.1f}%**.

            Enter **{EXPECTED_REVENUE_GROWTH:.1f}** as percentage points. Revenue is growing, but this calculation does not show whether that growth is profitable.
            """
        ).strip(),
        "SCN-002-E-002": dedent(
            f"""
            Gross-margin percentage = gross profit / revenue x 100.

            Prior period: GBP {prior_gp:.2f}m / GBP {prior_revenue:.2f}m x 100 = **{EXPECTED_PRIOR_GROSS_MARGIN:.1f}%**.

            Current period: GBP {current_gp:.2f}m / GBP {current_revenue:.2f}m x 100 = **{EXPECTED_CURRENT_GROSS_MARGIN:.1f}%**.

            Enter **{EXPECTED_PRIOR_GROSS_MARGIN:.1f}** and **{EXPECTED_CURRENT_GROSS_MARGIN:.1f}** as percentage points. Gross profit rose in pounds, but it did not keep pace with revenue.
            """
        ).strip(),
        "SCN-002-E-003": dedent(
            f"""
            EBITDA-margin percentage = EBITDA / revenue x 100.

            Prior period: GBP {prior_ebitda:.2f}m / GBP {prior_revenue:.2f}m x 100 = **{EXPECTED_PRIOR_EBITDA_MARGIN:.1f}%**.

            Current period: GBP {current_ebitda:.2f}m / GBP {current_revenue:.2f}m x 100 = **{EXPECTED_CURRENT_EBITDA_MARGIN:.1f}%**.

            Enter **{EXPECTED_PRIOR_EBITDA_MARGIN:.1f}** and **{EXPECTED_CURRENT_EBITDA_MARGIN:.1f}** as percentage points. The fall is an executive signal that revenue growth is consuming disproportionate cost.
            """
        ).strip(),
        "SCN-002-E-005": dedent(
            f"""
            Customer contribution = reported revenue - direct, customer-specific costs.

            GBP {CUSTOMER_REPORTED_REVENUE:.2f}m - GBP {customer_direct_cost():.2f}m = **GBP {EXPECTED_CUSTOMER_CONTRIBUTION:.2f}m**.

            Contribution margin = GBP {EXPECTED_CUSTOMER_CONTRIBUTION:.2f}m / GBP {CUSTOMER_REPORTED_REVENUE:.2f}m x 100 = **{EXPECTED_CUSTOMER_CONTRIBUTION_MARGIN:.1f}%**.

            Enter **{EXPECTED_CUSTOMER_CONTRIBUTION:.2f}** in GBP millions and **{EXPECTED_CUSTOMER_CONTRIBUTION_MARGIN:.1f}** as percentage points. The GBP {ALLOCATED_HEAD_OFFICE_OVERHEAD:.2f}m allocation is not part of contribution because it is not caused by this customer.
            """
        ).strip(),
        "SCN-002-E-006": dedent(
            f"""
            Formula: target revenue = direct costs / (1 - target contribution margin).

            At the defined {TARGET_CONTRIBUTION_MARGIN * 100:.0f}% target, direct costs must equal 55% of revenue.

            Economically attractive revenue = GBP {customer_direct_cost():.2f}m / (1 - {TARGET_CONTRIBUTION_MARGIN:.2f})
            = GBP {customer_direct_cost():.2f}m / 0.55 = **GBP {EXPECTED_ECONOMIC_REVENUE:.2f}m**.

            Required price increase = GBP {EXPECTED_ECONOMIC_REVENUE:.2f}m - GBP {CUSTOMER_REPORTED_REVENUE:.2f}m = **GBP {EXPECTED_PRICE_INCREASE:.2f}m**.

            Percentage increase = GBP {EXPECTED_PRICE_INCREASE:.2f}m / GBP {CUSTOMER_REPORTED_REVENUE:.2f}m x 100 = **{EXPECTED_PRICE_INCREASE_PERCENT:.1f}%**.

            Enter **{EXPECTED_ECONOMIC_REVENUE:.2f}**, **{EXPECTED_PRICE_INCREASE:.2f}**, and **{EXPECTED_PRICE_INCREASE_PERCENT:.1f}**. The first two fields use GBP millions; the last uses percentage points.
            """
        ).strip(),
        "SCN-002-E-007": dedent(
            f"""
            At GBP {CUSTOMER_REPORTED_REVENUE:.2f}m revenue and a {TARGET_CONTRIBUTION_MARGIN * 100:.0f}% target contribution margin, allowable direct costs are:

            GBP {CUSTOMER_REPORTED_REVENUE:.2f}m x (1 - {TARGET_CONTRIBUTION_MARGIN:.2f}) = GBP {CUSTOMER_REPORTED_REVENUE * (1 - TARGET_CONTRIBUTION_MARGIN):.2f}m.

            Current direct costs are GBP {customer_direct_cost():.2f}m, so cost reduction required is GBP {customer_direct_cost():.2f}m - GBP {CUSTOMER_REPORTED_REVENUE * (1 - TARGET_CONTRIBUTION_MARGIN):.2f}m = **GBP {EXPECTED_COST_REDUCTION:.2f}m**.

            Enter **{EXPECTED_COST_REDUCTION:.2f}** in GBP millions. This is the alternative to a price increase, not an extra saving on top of it.
            """
        ).strip(),
        "SCN-002-E-008": dedent(
            f"""
            Requested extra discount = GBP {CUSTOMER_REPORTED_REVENUE:.2f}m x {REQUESTED_ADDITIONAL_DISCOUNT_RATE * 100:.1f}% = **GBP {EXPECTED_REQUESTED_DISCOUNT:.2f}m**.

            Every additional pound of discount reduces contribution by the same amount while direct costs are unchanged. New contribution is GBP {EXPECTED_CUSTOMER_CONTRIBUTION:.2f}m - GBP {EXPECTED_REQUESTED_DISCOUNT:.2f}m = GBP {contribution_after_requested_discount():.2f}m.

            New contribution margin = GBP {contribution_after_requested_discount():.2f}m / GBP {CUSTOMER_REPORTED_REVENUE - EXPECTED_REQUESTED_DISCOUNT:.2f}m x 100 = **{EXPECTED_DISCOUNTED_CONTRIBUTION_MARGIN:.1f}%**.

            Enter **{EXPECTED_REQUESTED_DISCOUNT:.2f}** in GBP millions and **{EXPECTED_DISCOUNTED_CONTRIBUTION_MARGIN:.1f}** as percentage points. The proposed discount takes already weak economics further away from the target.
            """
        ).strip(),
    }


WORKED_CALCULATION_EXPLANATIONS = _worked_calculation_explanations()

JUDGMENT_EXPLANATIONS: dict[str, str] = {
    "SCN-002-E-004": "Revenue growth is not proof of value creation. A Finance Director should test whether each incremental pound of revenue preserves gross and EBITDA margin, especially where delivery costs are customer-specific.",
    "SCN-002-E-009": (
        f"The existing discount/value leakage is GBP {existing_discount_amount():.2f}m, "
        f"implementation overruns are GBP {CUSTOMER_DIRECT_COSTS['Implementation overruns']:.2f}m, "
        f"and incremental support is GBP {CUSTOMER_DIRECT_COSTS['Incremental support']:.2f}m. "
        "These are therefore the three largest quantified margin drivers and should drive the first negotiation agenda."
    ),
    "SCN-002-E-010": "Contribution analysis separates costs that change with the customer from costs that remain after an exit. Allocated head-office overhead is relevant to total company profitability but is not automatically avoidable or a standalone reason to exit.",
    "SCN-002-E-011": "Commercial decisions need evidence about the customer's response, exit obligations, and the availability of more profitable work. Without it, neither renewal nor exit can be treated as risk-free.",
    "SCN-002-E-012": "A route is a decision, not a rating. More than one route can be defensible when its safeguards address economics, delivery risk, and capacity deployment.",
    "SCN-002-E-013": "Route-specific safeguards turn a commercial preference into a controllable decision. Pricing, scope, and change control are particularly important when customer economics have already deteriorated.",
    "SCN-002-E-014": "Renewal routes require economic and operating repair. Delay requires evidence about whether repair is achievable and whether capacity has a credible alternative use. Rejection requires evidence that economics cannot be repaired and capacity can be released or redeployed.",
}


@dataclass(frozen=True)
class Scenario002Answers:
    revenue_growth_percent: float | None = None
    prior_gross_margin_percent: float | None = None
    current_gross_margin_percent: float | None = None
    prior_ebitda_margin_percent: float | None = None
    current_ebitda_margin_percent: float | None = None
    margin_interpretation: str | None = None
    customer_contribution: float | None = None
    customer_contribution_margin_percent: float | None = None
    economic_revenue: float | None = None
    price_increase: float | None = None
    price_increase_percent: float | None = None
    cost_reduction: float | None = None
    requested_discount: float | None = None
    discounted_contribution_margin_percent: float | None = None
    top_drivers: frozenset[str] = field(default_factory=frozenset)
    avoidable_costs: frozenset[str] = field(default_factory=frozenset)
    missing_information: frozenset[str] = field(default_factory=frozenset)
    recommendation: RecommendationRoute | None = None
    safeguards: frozenset[str] = field(default_factory=frozenset)
    decision_conditions: frozenset[str] = field(default_factory=frozenset)
    ceo_response: str = ""


SCENARIO_METADATA = ScenarioMetadata(
    primary_domains=("Management Accounting", "Commercial Finance", "Pricing", "Customer Profitability", "FP&A"),
    completion_time="About 25 minutes",
    difficulty="Advanced",
    provenance="Synthetic FinanceOS scenario, authored for commercial-finance learning and product-owner validation.",
    version="1.0",
    short_description="A strategic customer drives growth while discounts and delivery costs erode value; decide whether to renew.",
)

EVIDENCE_TITLES: dict[str, str] = {
    "SCN-002-E-001": "Revenue growth",
    "SCN-002-E-002": "Gross margins",
    "SCN-002-E-003": "EBITDA margins",
    "SCN-002-E-004": "Growth interpretation",
    "SCN-002-E-005": "Customer contribution",
    "SCN-002-E-006": "Target pricing",
    "SCN-002-E-007": "Cost-reduction alternative",
    "SCN-002-E-008": "Additional-discount effect",
    "SCN-002-E-009": "Priority margin drivers",
    "SCN-002-E-010": "Avoidable cost classification",
    "SCN-002-E-011": "Missing information",
    "SCN-002-E-012": "Recommendation route",
    "SCN-002-E-013": "Route safeguards",
    "SCN-002-E-014": "Decision conditions",
    "SCN-002-E-015": "Analysis completion",
}

CRITICAL_OMISSION_LABELS: dict[str, str] = {
    "SCN-002-CO-001": "Core company-margin evidence was materially incorrect.",
    "SCN-002-CO-002": "Customer contribution, target pricing, or discount economics were materially incorrect.",
    "SCN-002-CO-003": "No explicit commercial decision route was provided.",
    "SCN-002-CO-004": "The selected route did not include its minimum economics and delivery safeguards.",
}

SCENARIO_002 = ScenarioContent(
    scenario_id="SCN-002",
    title="Growth at Any Price: Should We Renew the Contract?",
    learner_role="Finance Director of Atlas Bridge, a fictional UK-based B2B technology and implementation-services company.",
    company_context="Atlas Bridge has grown quickly through enterprise transformation work. Northstar Group is strategically visible, but its renewal request arrives as delivery, support, and engineering costs are increasing faster than revenue.",
    financial_pack=(
        ContentSection(
            "Company income statement - GBP m",
            dedent(
                """
                                              FY2025       FY2026 forecast
                Revenue                         40.00               48.00
                Cost of sales                  (22.00)             (29.76)
                Gross profit                    18.00               18.24
                Operating expenses             (13.20)             (14.88)
                EBITDA                            4.80                3.36
                """
            ).strip(),
        ),
        ContentSection(
            "Northstar renewal commercial inputs - GBP m unless stated otherwise",
            dedent(
                f"""
                Standard price for the current customer scope           {CUSTOMER_STANDARD_PRICE:>5.2f}
                Reported annual customer revenue                        {CUSTOMER_REPORTED_REVENUE:>5.2f}
                Redeployable delivery capacity after 90 days            {CUSTOMER_DIRECT_COSTS['Redeployable delivery capacity after 90 days']:>5.2f}
                Delivery notice and tooling commitments                 {CUSTOMER_DIRECT_COSTS['Delivery notice and tooling commitments']:>5.2f}
                Implementation overruns                                 {CUSTOMER_DIRECT_COSTS['Implementation overruns']:>5.2f}
                Incremental support                                     {CUSTOMER_DIRECT_COSTS['Incremental support']:>5.2f}
                Customer-specific engineering                           {CUSTOMER_DIRECT_COSTS['Customer-specific engineering']:>5.2f}
                Service-level credits                                   {CUSTOMER_DIRECT_COSTS['Service-level credits']:>5.2f}
                Current direct customer costs total                     {customer_direct_cost():>5.2f}

                Allocated head-office overhead                          {ALLOCATED_HEAD_OFFICE_OVERHEAD:>5.2f}
                Defined target contribution margin                       45.0%
                Requested additional renewal discount                     5.0%

                The allocated head-office overhead is reported separately. It is not caused by Northstar and would remain if the account exited.
                """
            ).strip(),
        ),
        ContentSection(
            "Capacity and renewal assumptions",
            dedent(
                f"""
                Northstar uses 28% of delivery capacity and 35% of senior-engineering capacity.
                GBP {avoidable_exit_cost():.2f}m of the existing direct cost base is avoidable after exit: redeployable delivery capacity, implementation overruns, incremental support, and customer-specific engineering.
                GBP {retained_direct_cost():.2f}m of the existing direct cost base remains after exit: delivery notice and tooling commitments plus service-level credits. It is already included in the GBP {customer_direct_cost():.2f}m current direct cost total and is not an additional cost.
                The allocated GBP {ALLOCATED_HEAD_OFFICE_OVERHEAD:.2f}m head-office overhead also remains and is already contained in company EBITDA.
                Validated profitable-demand opportunities could contribute GBP 3.70m after redeployment.
                """
            ).strip(),
        ),
        ContentSection(
            "Stakeholder and forecast context",
            dedent(
                """
                The CEO and Chief Revenue Officer emphasize revenue growth, market credibility, and retention.
                Northstar seeks a three-year renewal plus the requested additional discount.
                The commercial team has not yet tested the customer's response to a price increase, reduced scope, paid change control, or revised service levels.
                Contract termination and service-transition obligations have not been fully quantified.
                """
            ).strip(),
        ),
    ),
    initial_question=(
        "Northstar wants a three-year renewal and a further discount. Revenue has grown, but the account is consuming delivery and engineering capacity. Do you approve, conditionally approve, delay, or reject the renewal?"
    ),
    model_answer=(
        "I recommend conditional approval, subject to a commercially signed reset rather than a renewal at the requested terms. Company revenue has grown 20.0%, but gross margin has fallen from 45.0% to 38.0% and EBITDA margin from 12.0% to 7.0%. Northstar contributes only GBP 3.00m, or 33.3%, before allocated overhead. A further 5.0% discount removes GBP 0.45m of contribution and reduces the account margin to 29.8%.\n\n"
        "The renewal should meet a 45.0% contribution-margin target through a GBP 1.91m price increase, GBP 1.05m cost reduction, or a credible combination, with paid change control and a reset of service-level commitments. We should cap implementation exposure and run monthly customer economics reviews owned jointly by Commercial and Delivery. If Northstar will not accept viable terms, I would delay only long enough to validate exit obligations and redeployment, then transition the account rather than preserve uneconomic revenue."
    ),
    debrief=(
        "Northstar is a commercial-finance decision, not a revenue-retention reflex. Its reported revenue is GBP 9.00m, but direct costs of GBP 6.00m leave GBP 3.00m contribution. Of that existing GBP 6.00m direct-cost base, GBP 5.00m is avoidable after exit and GBP 1.00m remains; the retained GBP 1.00m is not an additional exit cost. The GBP 0.80m allocation should be understood in total profitability reporting, but it should not be treated as avoidable in an exit decision.\n\n"
        "A renewal at the additional discount reduces company EBITDA from GBP 3.36m to GBP 2.91m in the base view. Repairing price to the target improves EBITDA to GBP 5.27m. Exiting and replacing the released capacity produces GBP 3.06m after the 90-day direct-cost assumptions, so exit is not mechanically superior but remains a credible alternative when terms cannot be repaired."
    ),
    self_review_checklist=(
        "Did I separate reported revenue, contribution, and allocated overhead?",
        "Did I quantify the price, cost, and discount alternatives before deciding?",
        "Did I treat capacity as an economic resource rather than an abstract percentage?",
        "Did I propose safeguards that match my chosen route?",
        "Did I make clear what information could change the decision?",
        "Did I challenge revenue credibility constructively without treating exit as cost-free?",
    ),
    action_plan=(
        "Rebuild the customer contribution calculation with a price, scope, and cost-to-serve sensitivity.",
        "Draft a renewal negotiation mandate covering target margin, change control, service levels, and exit triggers.",
        "Create a capacity-redeployment case that distinguishes avoidable costs, retained costs, and replacement contribution.",
    ),
    reconciliation_summary=(
        f"Company revenue grows {EXPECTED_REVENUE_GROWTH:.1f}% from GBP 40.00m to GBP 48.00m, while gross margin falls from {EXPECTED_PRIOR_GROSS_MARGIN:.1f}% to {EXPECTED_CURRENT_GROSS_MARGIN:.1f}% and EBITDA margin from {EXPECTED_PRIOR_EBITDA_MARGIN:.1f}% to {EXPECTED_CURRENT_EBITDA_MARGIN:.1f}%. Northstar's GBP 9.00m revenue less GBP {customer_direct_cost():.2f}m direct cost gives GBP {EXPECTED_CUSTOMER_CONTRIBUTION:.2f}m contribution ({EXPECTED_CUSTOMER_CONTRIBUTION_MARGIN:.1f}%). A 45.0% target requires GBP {EXPECTED_ECONOMIC_REVENUE:.2f}m revenue, GBP {EXPECTED_PRICE_INCREASE:.2f}m more than reported, or GBP {EXPECTED_COST_REDUCTION:.2f}m cost reduction. The requested discount costs GBP {EXPECTED_REQUESTED_DISCOUNT:.2f}m and reduces contribution margin to {EXPECTED_DISCOUNTED_CONTRIBUTION_MARGIN:.1f}%. Exit makes GBP {avoidable_exit_cost():.2f}m of the GBP {customer_direct_cost():.2f}m current direct-cost base avoidable, leaving GBP {retained_direct_cost():.2f}m retained direct cost; that GBP {retained_direct_cost():.2f}m is already part of the current direct-cost base, not an additional cost. The allocated GBP {ALLOCATED_HEAD_OFFICE_OVERHEAD:.2f}m head-office overhead also remains and is already contained in company EBITDA. Company EBITDA is GBP {EXPECTED_PROPOSED_RENEWAL_EBITDA:.2f}m if renewed as proposed, GBP {EXPECTED_TARGET_RENEWAL_EBITDA:.2f}m at target economics, and GBP {EXPECTED_EXIT_AND_REDEPLOY_EBITDA:.2f}m after exit and redeployment under the stated assumptions."
    ),
)
