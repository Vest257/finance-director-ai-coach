"""Shared Scenario 001 test data."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from finance_director_coach.models import LearnerAnswers, RecommendationRoute
from finance_director_coach.scenarios.scenario_001 import (
    CORE_MISSING_INFORMATION,
    CORE_RISKS,
    CORE_TRADEOFFS,
    EXPECTED_CASH_DRIVERS,
    EXPECTED_THRESHOLD_INTERPRETATIONS,
    EXTENDED_RISKS,
    REQUIRED_ROUTE_SAFEGUARDS,
)


@pytest.fixture
def answer_factory() -> Callable[[RecommendationRoute], LearnerAnswers]:
    def make(
        route: RecommendationRoute = RecommendationRoute.CONDITIONALLY_APPROVE,
    ) -> LearnerAnswers:
        return LearnerAnswers(
            revenue_growth_percent=22.2,
            ebitda_growth_percent=25.9,
            cash_decrease=2.70,
            operating_cash_before_interest_tax=-0.20,
            net_operating_cash=-0.90,
            cash_drivers=EXPECTED_CASH_DRIVERS,
            largest_cash_driver="receivables",
            risks=CORE_RISKS | EXTENDED_RISKS,
            h2_hiring_cost=0.58,
            annual_hiring_cost=1.68,
            cash_low_point=3.35,
            december_cash=4.42,
            board_floor_shortfall=0.15,
            lender_headroom=0.85,
            threshold_interpretations=EXPECTED_THRESHOLD_INTERPRETATIONS,
            recommendation=route,
            safeguards=REQUIRED_ROUTE_SAFEGUARDS[route],
            missing_information=CORE_MISSING_INFORMATION,
            tradeoffs=CORE_TRADEOFFS | {"contractor_alternative"},
            ceo_response="Proceed only with safeguards tied to cash and collections.",
        )

    return make
