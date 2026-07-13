"""Financial reconciliation tests for Scenario 001."""

from finance_director_coach.scenarios.scenario_001 import (
    ANNUAL_COST_PER_HIRE,
    BOARD_CASH_FLOOR,
    CURRENT_ASSETS,
    EXPECTED_ANNUAL_HIRING_COST,
    EXPECTED_BOARD_SHORTFALL,
    EXPECTED_CASH_DECREASE,
    EXPECTED_CASH_LOW_POINT,
    EXPECTED_DECEMBER_CASH,
    EXPECTED_EBITDA_GROWTH,
    EXPECTED_H2_HIRING_COST,
    EXPECTED_LENDER_HEADROOM,
    EXPECTED_NET_OPERATING_CASH,
    EXPECTED_OPERATING_CASH,
    EXPECTED_REVENUE_GROWTH,
    INCOME_STATEMENT,
    LENDER_MINIMUM_CASH,
    OPENING_ASSETS,
    SCENARIO_001,
    balance_sheet_totals,
    cash_after_hiring,
    cash_bridge_change,
    monthly_hiring_costs,
    net_operating_cash,
    operating_cash_before_interest_and_tax,
)


def normalized_section(title: str) -> str:
    section = next(item for item in SCENARIO_001.financial_pack if item.title == title)
    return " ".join(section.body.split())


def test_balance_sheet_reconciles() -> None:
    assert balance_sheet_totals() == (21.50, 21.50, 24.20, 24.20)
    assert CURRENT_ASSETS["Cash"] - OPENING_ASSETS["Cash"] == -2.70
    assert round(5.00 + 1.20 - 0.70, 2) == CURRENT_ASSETS[
        "Property, equipment, and capitalized software"
    ]


def test_income_statement_growth_matches_specification() -> None:
    revenue_prior, revenue_current = INCOME_STATEMENT["Revenue"]
    ebitda_prior, ebitda_current = INCOME_STATEMENT["EBITDA"]
    assert round((revenue_current - revenue_prior) / revenue_prior * 100, 1) == 22.2
    assert round((ebitda_current - ebitda_prior) / ebitda_prior * 100, 1) == 25.9


def test_approved_numerical_answers_remain_unchanged() -> None:
    assert (
        EXPECTED_REVENUE_GROWTH,
        EXPECTED_EBITDA_GROWTH,
        EXPECTED_CASH_DECREASE,
        EXPECTED_OPERATING_CASH,
        EXPECTED_NET_OPERATING_CASH,
        EXPECTED_H2_HIRING_COST,
        EXPECTED_ANNUAL_HIRING_COST,
        EXPECTED_CASH_LOW_POINT,
        EXPECTED_DECEMBER_CASH,
        EXPECTED_BOARD_SHORTFALL,
        EXPECTED_LENDER_HEADROOM,
    ) == (22.2, 25.9, 2.70, -0.20, -0.90, 0.58, 1.68, 3.35, 4.42, 0.15, 0.85)


def test_ebitda_to_cash_reconciliation() -> None:
    assert operating_cash_before_interest_and_tax() == -0.20
    assert net_operating_cash() == -0.90
    assert cash_bridge_change() == -2.70
    assert round(7.00 + cash_bridge_change(), 2) == 4.30


def test_hiring_cost_phasing() -> None:
    assert monthly_hiring_costs() == {
        "July": 0.00,
        "August": 0.00,
        "September": 0.15,
        "October": 0.07,
        "November": 0.22,
        "December": 0.14,
    }
    assert round(sum(monthly_hiring_costs().values()), 2) == 0.58
    assert round(20 * ANNUAL_COST_PER_HIRE, 2) == 1.68


def test_hiring_cash_low_point_and_december_cash() -> None:
    forecast = cash_after_hiring()
    assert forecast == {
        "July": 3.80,
        "August": 3.50,
        "September": 3.35,
        "October": 3.58,
        "November": 3.86,
        "December": 4.42,
    }
    assert min(forecast.values()) == 3.35
    assert forecast["December"] == 4.42
    assert round(BOARD_CASH_FLOOR - min(forecast.values()), 2) == 0.15
    assert round(min(forecast.values()) - LENDER_MINIMUM_CASH, 2) == 0.85


def test_learner_financial_pack_contains_required_raw_inputs() -> None:
    income_statement = normalized_section("Income statement - GBP m")
    assert "Revenue 18.00 22.00" in income_statement
    assert "EBITDA 2.70 3.40" in income_statement

    balance_sheet = normalized_section("Balance sheet - GBP m")
    assert "Cash 7.00 4.30" in balance_sheet
    assert "Trade receivables 6.00 9.20" in balance_sheet
    assert "Interest-bearing debt 5.50 4.90" in balance_sheet

    cash_bridge = normalized_section("EBITDA-to-cash bridge - H1 2026, GBP m")
    for component in (
        "Opening cash at 31 December 2025 7.00",
        "EBITDA 3.40",
        "Increase in trade receivables (3.20)",
        "Increase in inventory (1.10)",
        "Increase in contract assets and prepayments (0.60)",
        "Increase in trade payables 0.90",
        "Increase in accruals and deferred revenue 0.40",
        "Cash interest paid (0.20)",
        "Cash tax paid (0.50)",
        "Capital expenditure (1.20)",
        "Debt principal repaid (0.60)",
    ):
        assert component in cash_bridge

    baseline_cash = normalized_section("Baseline monthly closing-cash forecast - GBP m")
    for month_and_cash in (
        "July 3.80",
        "August 3.50",
        "September 3.50",
        "October 3.80",
        "November 4.30",
        "December 5.00",
    ):
        assert month_and_cash in baseline_cash

    hiring = normalized_section("Proposed 20 hires")
    assert "Ten starters are proposed for September and ten for November." in hiring
    assert "Annual fully loaded cost is GBP 84,000 per hire" in hiring
    assert "one-time onboarding cost is GBP 8,000 per hire" in hiring
    assert "Recurring cost accrues evenly by month" in hiring
    assert "One-time onboarding cost is paid in each starter's start month." in hiring

    liquidity = normalized_section("Working capital and liquidity")
    assert "The board cash floor is GBP 3.50m." in liquidity
    assert "The lender minimum cash covenant is GBP 2.50m." in liquidity
    assert "A GBP 3.00m undrawn RCF expires in March 2027." in liquidity
    assert "No downside case is provided." in liquidity


def test_learner_financial_pack_does_not_disclose_assessed_derived_outputs() -> None:
    learner_pack = " ".join(
        f"{section.title} {section.body}" for section in SCENARIO_001.financial_pack
    ).lower()
    for derived_label in (
        "revenue growth percentage",
        "ebitda growth percentage",
        "net decrease in cash",
        "total cash decline",
        "operating cash before interest and tax",
        "net operating cash",
        "h2 hiring cost",
        "annual recurring hiring cost",
        "hiring-case cash low point",
        "hiring-case december cash",
        "cash after hiring",
        "board-floor shortfall",
        "shortfall below the board cash floor",
        "lender headroom",
        "headroom above the lender minimum",
    ):
        assert derived_label not in learner_pack
