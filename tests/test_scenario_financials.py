"""Financial reconciliation tests for Scenario 001."""

from finance_director_coach.scenarios.scenario_001 import (
    ANNUAL_COST_PER_HIRE,
    BOARD_CASH_FLOOR,
    CURRENT_ASSETS,
    INCOME_STATEMENT,
    LENDER_MINIMUM_CASH,
    OPENING_ASSETS,
    balance_sheet_totals,
    cash_after_hiring,
    cash_bridge_change,
    monthly_hiring_costs,
    net_operating_cash,
    operating_cash_before_interest_and_tax,
)


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
