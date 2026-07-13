"""Scenario 002 finance, evaluation, explanation, and leakage tests."""

from __future__ import annotations

from dataclasses import replace

import pytest

from finance_director_coach.models import (
    AssessmentSource,
    Competency,
    CompetencyRating,
    EvidenceResult,
    RecommendationRoute,
)
from finance_director_coach.scenarios.scenario_002 import (
    AVOIDABLE_COST_OPTIONS,
    CUSTOMER_DIRECT_COSTS,
    EXPECTED_AVOIDABLE_COSTS,
    EXPECTED_COST_REDUCTION,
    EXPECTED_CURRENT_EBITDA_MARGIN,
    EXPECTED_CURRENT_GROSS_MARGIN,
    EXPECTED_CUSTOMER_CONTRIBUTION,
    EXPECTED_CUSTOMER_CONTRIBUTION_MARGIN,
    EXPECTED_DECISION_CONDITIONS,
    EXPECTED_DISCOUNTED_CONTRIBUTION_MARGIN,
    EXPECTED_ECONOMIC_REVENUE,
    EXPECTED_EXIT_AND_REDEPLOY_EBITDA,
    EXPECTED_MARGIN_INTERPRETATION,
    EXPECTED_MISSING_INFORMATION,
    EXPECTED_PRICE_INCREASE,
    EXPECTED_PRICE_INCREASE_PERCENT,
    EXPECTED_PRIOR_EBITDA_MARGIN,
    EXPECTED_PRIOR_GROSS_MARGIN,
    EXPECTED_PROPOSED_RENEWAL_EBITDA,
    EXPECTED_REQUESTED_DISCOUNT,
    EXPECTED_REVENUE_GROWTH,
    EXPECTED_TARGET_RENEWAL_EBITDA,
    EXPECTED_TOP_DRIVERS,
    REQUIRED_ROUTE_SAFEGUARDS,
    SCENARIO_002,
    Scenario002Answers,
    avoidable_exit_cost,
    contribution_after_requested_discount,
    contribution_margin_after_requested_discount,
    customer_contribution,
    customer_contribution_margin,
    customer_direct_cost,
    economically_attractive_revenue,
    exit_and_redeploy_ebitda,
    proposed_renewal_ebitda,
    required_cost_reduction,
    required_price_increase,
    required_price_increase_percent,
    requested_discount_amount,
    target_renewal_ebitda,
)
from finance_director_coach.scenarios.scenario_002_evaluation import (
    evaluate_scenario_002_attempt,
    skipped_scenario_002_report,
)


def answers_for(route: RecommendationRoute = RecommendationRoute.CONDITIONALLY_APPROVE) -> Scenario002Answers:
    return Scenario002Answers(
        revenue_growth_percent=EXPECTED_REVENUE_GROWTH,
        prior_gross_margin_percent=EXPECTED_PRIOR_GROSS_MARGIN,
        current_gross_margin_percent=EXPECTED_CURRENT_GROSS_MARGIN,
        prior_ebitda_margin_percent=EXPECTED_PRIOR_EBITDA_MARGIN,
        current_ebitda_margin_percent=EXPECTED_CURRENT_EBITDA_MARGIN,
        margin_interpretation=EXPECTED_MARGIN_INTERPRETATION,
        customer_contribution=EXPECTED_CUSTOMER_CONTRIBUTION,
        customer_contribution_margin_percent=EXPECTED_CUSTOMER_CONTRIBUTION_MARGIN,
        economic_revenue=EXPECTED_ECONOMIC_REVENUE,
        price_increase=EXPECTED_PRICE_INCREASE,
        price_increase_percent=EXPECTED_PRICE_INCREASE_PERCENT,
        cost_reduction=EXPECTED_COST_REDUCTION,
        requested_discount=EXPECTED_REQUESTED_DISCOUNT,
        discounted_contribution_margin_percent=EXPECTED_DISCOUNTED_CONTRIBUTION_MARGIN,
        top_drivers=EXPECTED_TOP_DRIVERS,
        avoidable_costs=EXPECTED_AVOIDABLE_COSTS,
        missing_information=EXPECTED_MISSING_INFORMATION,
        recommendation=route,
        safeguards=REQUIRED_ROUTE_SAFEGUARDS[route],
        decision_conditions=EXPECTED_DECISION_CONDITIONS,
        ceo_response="Conditionally approve subject to repaired pricing, scope, and service economics.",
    )


def evidence_result(report, evidence_id: str) -> EvidenceResult:
    return next(item.result for item in report.evidence_records if item.evidence_id == evidence_id)


def test_scenario_002_financial_calculations_reconcile() -> None:
    assert customer_direct_cost() == sum(CUSTOMER_DIRECT_COSTS.values()) == 6.00
    assert customer_contribution() == EXPECTED_CUSTOMER_CONTRIBUTION == 3.00
    assert customer_contribution_margin() == EXPECTED_CUSTOMER_CONTRIBUTION_MARGIN == 33.3
    assert economically_attractive_revenue() == EXPECTED_ECONOMIC_REVENUE == 10.91
    assert required_price_increase() == EXPECTED_PRICE_INCREASE == 1.91
    assert required_price_increase_percent() == EXPECTED_PRICE_INCREASE_PERCENT == 21.2
    assert required_cost_reduction() == EXPECTED_COST_REDUCTION == 1.05
    assert requested_discount_amount() == EXPECTED_REQUESTED_DISCOUNT == 0.45
    assert contribution_after_requested_discount() == 2.55
    assert contribution_margin_after_requested_discount() == EXPECTED_DISCOUNTED_CONTRIBUTION_MARGIN == 29.8
    assert avoidable_exit_cost() == 5.00
    assert proposed_renewal_ebitda() == EXPECTED_PROPOSED_RENEWAL_EBITDA == 2.91
    assert target_renewal_ebitda() == EXPECTED_TARGET_RENEWAL_EBITDA == 5.27
    assert exit_and_redeploy_ebitda() == EXPECTED_EXIT_AND_REDEPLOY_EBITDA == 3.06


def test_scenario_002_pack_exposes_raw_inputs_without_derived_answers() -> None:
    pack = " ".join(
        " ".join(f"{section.title} {section.body}".split())
        for section in SCENARIO_002.financial_pack
    ).lower()
    for required_input in (
        "revenue 40.00 48.00",
        "gross profit 18.00 18.24",
        "ebitda 4.80 3.36",
        "reported annual customer revenue 9.00",
        "implementation overruns 1.20",
        "defined target contribution margin 45.0%",
        "requested additional renewal discount 5.0%",
        "28% of delivery capacity",
        "35% of senior-engineering capacity",
        "contribute gbp 3.70m after redeployment",
    ):
        assert required_input in pack
    for derived_label in (
        "revenue growth is 20.0%",
        "customer contribution is gbp",
        "economically attractive revenue",
        "required price increase",
        "alternative cost reduction",
        "contribution margin after",
        "renew as proposed",
        "target economics",
    ):
        assert derived_label not in pack


def test_correct_incorrect_and_missing_numerical_evidence() -> None:
    correct = evaluate_scenario_002_attempt(answers_for())
    incorrect = evaluate_scenario_002_attempt(replace(answers_for(), price_increase=0.10))
    missing = evaluate_scenario_002_attempt(replace(answers_for(), requested_discount=None))
    assert evidence_result(correct, "SCN-002-E-006") is EvidenceResult.OBSERVED
    assert evidence_result(incorrect, "SCN-002-E-006") is EvidenceResult.NOT_OBSERVED
    assert evidence_result(missing, "SCN-002-E-008") is EvidenceResult.INSUFFICIENT_EVIDENCE


def test_numerical_tolerances_and_expected_answers_are_explicit() -> None:
    at_boundary = evaluate_scenario_002_attempt(
        replace(answers_for(), price_increase=EXPECTED_PRICE_INCREASE + 0.05)
    )
    outside = evaluate_scenario_002_attempt(
        replace(answers_for(), price_increase=EXPECTED_PRICE_INCREASE + 0.0501)
    )
    assert evidence_result(at_boundary, "SCN-002-E-006") is EvidenceResult.OBSERVED
    assert evidence_result(outside, "SCN-002-E-006") is EvidenceResult.NOT_OBSERVED


def test_prioritisation_and_avoidable_cost_constraints_are_enforced() -> None:
    all_drivers = frozenset({"deep_discount", "implementation_overruns", "support_requirements", "customer_engineering"})
    too_many_costs = frozenset(AVOIDABLE_COST_OPTIONS)
    report = evaluate_scenario_002_attempt(
        replace(answers_for(), top_drivers=all_drivers, avoidable_costs=too_many_costs)
    )
    assert evidence_result(report, "SCN-002-E-009") is EvidenceResult.NOT_OBSERVED
    assert evidence_result(report, "SCN-002-E-010") is EvidenceResult.NOT_OBSERVED


@pytest.mark.parametrize("route", list(RecommendationRoute))
def test_all_recommendation_routes_can_meet_route_specific_rules(route: RecommendationRoute) -> None:
    report = evaluate_scenario_002_attempt(answers_for(route))
    assert evidence_result(report, "SCN-002-E-012") is EvidenceResult.OBSERVED
    assert evidence_result(report, "SCN-002-E-013") is EvidenceResult.OBSERVED
    result = report.scorecard.for_competency(Competency.COMMERCIAL_JUDGMENT)
    assert result.rating is CompetencyRating.CAPABLE
    assert result.assessment_source is AssessmentSource.DETERMINISTIC


def test_missing_route_safeguards_create_observed_failure_not_text_scoring() -> None:
    route = RecommendationRoute.CONDITIONALLY_APPROVE
    incomplete = frozenset({"target_margin"})
    short = evaluate_scenario_002_attempt(
        replace(answers_for(route), safeguards=incomplete, ceo_response="Approve.")
    )
    long = evaluate_scenario_002_attempt(
        replace(
            answers_for(route),
            safeguards=incomplete,
            ceo_response="persuasive strategic revenue cash leadership " * 40,
        )
    )
    assert evidence_result(short, "SCN-002-E-013") is EvidenceResult.NOT_OBSERVED
    assert short.evidence_records == long.evidence_records
    assert short.scorecard == long.scorecard


def test_scenario_002_worked_and_judgment_explanations_are_traceable() -> None:
    report = evaluate_scenario_002_attempt(answers_for())
    records = {record.evidence_id: record for record in report.evidence_records}
    numerical_ids = {
        "SCN-002-E-001",
        "SCN-002-E-002",
        "SCN-002-E-003",
        "SCN-002-E-005",
        "SCN-002-E-006",
        "SCN-002-E-007",
        "SCN-002-E-008",
    }
    assert {record_id for record_id, record in records.items() if record.worked_solution} == numerical_ids
    assert {record_id for record_id, record in records.items() if record.judgment_explanation} == {
        "SCN-002-E-004",
        "SCN-002-E-009",
        "SCN-002-E-010",
        "SCN-002-E-011",
        "SCN-002-E-012",
        "SCN-002-E-013",
        "SCN-002-E-014",
    }
    price_solution = records["SCN-002-E-006"].worked_solution
    assert price_solution is not None
    for expected_step in ("Formula", "GBP 6.00m / 0.55", "GBP 10.91m", "GBP 1.91m", "21.2%", "Enter"):
        assert expected_step in price_solution


def test_scenario_002_competency_source_limits_and_skip_path() -> None:
    report = evaluate_scenario_002_attempt(answers_for())
    assert report.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating is CompetencyRating.STRONG
    assert report.scorecard.for_competency(Competency.COMMERCIAL_JUDGMENT).rating is CompetencyRating.CAPABLE
    assert report.scorecard.for_competency(Competency.STAKEHOLDER_COMMUNICATION).rating is CompetencyRating.NOT_ASSESSED
    assert report.scorecard.for_competency(Competency.STRATEGIC_LEADERSHIP).rating is CompetencyRating.NOT_ASSESSED
    skipped = skipped_scenario_002_report()
    assert skipped.evidence_records == ()
    assert all(result.rating is CompetencyRating.NOT_ASSESSED for result in skipped.scorecard.results)
