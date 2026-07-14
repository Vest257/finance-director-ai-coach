"""Reconciliation, difficulty, and deterministic-boundary tests for Scenario 002."""

from __future__ import annotations

from dataclasses import replace

import pytest

from finance_director_coach.models import Competency, CompetencyRating, EvidenceResult, RecommendationRoute
from finance_director_coach.scenarios.scenario_002 import (
    BASIC_PNL_EVIDENCE_IDS, BOARD_CASH_FLOOR, CLASSIFICATION_OPTIONS, COMPANY_RECEIVABLES, EXPECTED_BALANCE_SHEET_EXPOSURE,
    EXPECTED_CASH_CONVERSION, EXPECTED_CLASSIFICATIONS, EXPECTED_DSO, EXPECTED_EXPOSURE_AT_RISK,
    EXPECTED_NET_WORKING_CAPITAL, EXPECTED_OPERATING_CASH, EXPECTED_RECEIVABLE_CONCENTRATION,
    NORTHSTAR_RECEIVABLES, PERCENTAGE_TOLERANCE, PRICE_UPLIFT_CASH_REALISATION_PERCENT, REQUIRED_ROUTE_ASSUMPTIONS,
    REQUIRED_ROUTE_PROTECTIONS, ROUTE_EBITDA, ROUTE_PROTECTION_OPTIONS, ROUTE_SAFEGUARD_OPTIONS, REQUIRED_ROUTE_SAFEGUARDS,
    SCENARIO_002, Scenario002Answers, cash_conversion_percent, customer_balance_sheet_exposure,
    customer_exposure_at_risk, net_customer_working_capital, northstar_dso,
    northstar_receivable_concentration, operating_cash_flow, route_liquidity_headroom,
    renegotiated_target_revenue, renegotiation_cash_realised, route_ebitda, route_low_cash,
    route_monthly_cash, route_operating_cash, route_rcf_draw,
)
from finance_director_coach.scenarios.scenario_002_adapter import build_scenario_002_answers
from finance_director_coach.scenarios.scenario_002_evaluation import evaluate_scenario_002_attempt, skipped_scenario_002_report

ROUTES = ("renew", "renegotiate", "exit")


def answers_for(route: RecommendationRoute = RecommendationRoute.CONDITIONALLY_APPROVE) -> Scenario002Answers:
    return Scenario002Answers(
        quality_interpretation="growth_cash_divergence", operating_cash_flow=operating_cash_flow(), cash_conversion_percent=cash_conversion_percent(), largest_cash_absorber="receivables",
        northstar_dso=northstar_dso(), receivable_concentration_percent=northstar_receivable_concentration(), net_working_capital=net_customer_working_capital(), balance_sheet_exposure=customer_balance_sheet_exposure(), exposure_at_risk=customer_exposure_at_risk(),
        route_ebitda=dict(ROUTE_EBITDA), route_operating_cash={key: route_operating_cash(key) for key in ROUTES}, route_low_cash={key: route_low_cash(key) for key in ROUTES}, route_rcf_draw={key: route_rcf_draw(key) for key in ROUTES}, route_headroom={key: route_liquidity_headroom(key) for key in ROUTES},
        classifications=EXPECTED_CLASSIFICATIONS, recommendation=route, safeguards=REQUIRED_ROUTE_SAFEGUARDS[route], protections=REQUIRED_ROUTE_PROTECTIONS[route], assumptions=REQUIRED_ROUTE_ASSUMPTIONS[route], ceo_response="Route choice is subject to cash, collection, and capacity controls.",
    )


def result(report, evidence_id: str) -> EvidenceResult:
    return next(record.result for record in report.evidence_records if record.evidence_id == evidence_id)


def test_integrated_financial_contract_reconciles() -> None:
    assert operating_cash_flow() == EXPECTED_OPERATING_CASH == -1.54
    assert cash_conversion_percent() == EXPECTED_CASH_CONVERSION == -45.8
    assert northstar_dso() == EXPECTED_DSO == 121.7
    assert northstar_receivable_concentration() == EXPECTED_RECEIVABLE_CONCENTRATION == 25.0
    assert net_customer_working_capital() == EXPECTED_NET_WORKING_CAPITAL == 3.70
    assert customer_balance_sheet_exposure() == EXPECTED_BALANCE_SHEET_EXPOSURE == 4.70
    assert customer_exposure_at_risk() == EXPECTED_EXPOSURE_AT_RISK == 2.30
    assert NORTHSTAR_RECEIVABLES / COMPANY_RECEIVABLES == 0.25


def test_route_forecasts_monthly_cash_rcf_and_headroom_reconcile() -> None:
    assert {route: route_ebitda(route) for route in ROUTES} == ROUTE_EBITDA == {"renew": 2.91, "renegotiate": 5.27, "exit": 3.06}
    for route in ROUTES:
        forecast = route_monthly_cash(route)
        assert route_low_cash(route) == min(forecast.values())
        assert route_rcf_draw(route) == max(0, round(BOARD_CASH_FLOOR - route_low_cash(route), 2))
        assert route_liquidity_headroom(route) == 4.00 - route_rcf_draw(route)
    assert {route: route_low_cash(route) for route in ROUTES} == {"renew": 3.15, "renegotiate": 3.80, "exit": 3.35}
    assert {route: route_rcf_draw(route) for route in ROUTES} == {"renew": 0.35, "renegotiate": 0.0, "exit": 0.15}


def test_renegotiation_cash_is_derived_from_the_single_collection_assumption() -> None:
    assert PRICE_UPLIFT_CASH_REALISATION_PERCENT == 70.0
    assert renegotiated_target_revenue() == 10.91
    assert renegotiation_cash_realised() == 1.34
    assert SCENARIO_002.financial_pack[2].body.count("70% of the price uplift") == 1
    assert route_operating_cash("renegotiate") == round(
        operating_cash_flow() + renegotiation_cash_realised() + 0.50 + 0.30, 2
    )


def test_pack_exposes_raw_inputs_without_assessed_results() -> None:
    pack = " ".join(section.body for section in SCENARIO_002.financial_pack).lower()
    for raw_input in ("northstar receivables 3.00", "unbilled implementation work 1.80", "undrawn rcf 4.00", "baseline closing cash", "foregone customer cash receipts"):
        assert raw_input in pack
    for hidden_result in ("operating cash flow is gbp -1.54", "northstar dso is 121.7", "annual ebitda to 5.27", "annual ebitda is 3.06", "annual operating cash outcomes", "low cash points", "required rcf draws"):
        assert hidden_result not in pack


def test_evidence_composition_and_integrated_strong_requirement() -> None:
    report = evaluate_scenario_002_attempt(answers_for())
    assert len(report.evidence_records) == 15
    assert len(BASIC_PNL_EVIDENCE_IDS) <= 2
    assert result(report, "SCN-002-E-001") is EvidenceResult.OBSERVED
    assert report.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating is CompetencyRating.STRONG
    warmup_only = evaluate_scenario_002_attempt(replace(answers_for(), operating_cash_flow=0.0))
    assert warmup_only.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating is CompetencyRating.DEVELOPING


def test_financial_insight_has_deterministic_boundaries_for_all_four_levels() -> None:
    not_assessed = evaluate_scenario_002_attempt(Scenario002Answers())
    cash_bridge_error = evaluate_scenario_002_attempt(replace(answers_for(), operating_cash_flow=0.0))
    customer_exposure_error = evaluate_scenario_002_attempt(replace(answers_for(), northstar_dso=0.0))
    route_liquidity_error = evaluate_scenario_002_attempt(
        replace(answers_for(), route_low_cash={route: 0.0 for route in ROUTES})
    )
    capable = evaluate_scenario_002_attempt(replace(answers_for(), classifications=frozenset()))
    strong = evaluate_scenario_002_attempt(answers_for())
    assert not_assessed.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating is CompetencyRating.NOT_ASSESSED
    assert cash_bridge_error.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating is CompetencyRating.DEVELOPING
    assert customer_exposure_error.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating is CompetencyRating.DEVELOPING
    assert route_liquidity_error.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating is CompetencyRating.DEVELOPING
    assert capable.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating is CompetencyRating.CAPABLE
    assert strong.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating is CompetencyRating.STRONG
    assert "Insufficient submitted evidence" in next(record.feedback for record in not_assessed.evidence_records if record.evidence_id == "SCN-002-E-002")


def test_financial_insight_distinguishes_limited_and_material_route_errors() -> None:
    limited_extended_error = evaluate_scenario_002_attempt(
        replace(answers_for(), route_operating_cash={route: 0.0 for route in ROUTES})
    )
    material_trough_error = evaluate_scenario_002_attempt(
        replace(answers_for(), route_low_cash={route: 0.0 for route in ROUTES})
    )
    material_rcf_error = evaluate_scenario_002_attempt(
        replace(answers_for(), route_rcf_draw={route: 0.0 for route in ROUTES})
    )
    material_headroom_error = evaluate_scenario_002_attempt(
        replace(answers_for(), route_headroom={route: 0.0 for route in ROUTES})
    )

    assert result(limited_extended_error, "SCN-002-E-009") is EvidenceResult.NOT_OBSERVED
    assert limited_extended_error.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating is CompetencyRating.CAPABLE
    assert result(material_trough_error, "SCN-002-E-010") is EvidenceResult.NOT_OBSERVED
    assert material_trough_error.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating is CompetencyRating.DEVELOPING
    assert result(material_rcf_error, "SCN-002-E-011") is EvidenceResult.NOT_OBSERVED
    assert material_rcf_error.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating is CompetencyRating.DEVELOPING
    assert result(material_headroom_error, "SCN-002-E-011") is EvidenceResult.NOT_OBSERVED
    assert material_headroom_error.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating is CompetencyRating.DEVELOPING


def test_ceo_response_does_not_affect_financial_insight_rating() -> None:
    correct = evaluate_scenario_002_attempt(answers_for())
    different_ceo_wording = evaluate_scenario_002_attempt(
        replace(answers_for(), ceo_response="Ignore liquidity and accept any commercial terms.")
    )

    assert different_ceo_wording.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating is correct.scorecard.for_competency(Competency.FINANCIAL_INSIGHT).rating


@pytest.mark.parametrize("field, value, evidence_id", (("northstar_dso", 1.0, "SCN-002-E-005"), ("net_working_capital", 0.0, "SCN-002-E-007"), ("route_low_cash", {"renew": 0.0, "renegotiate": 0.0, "exit": 0.0}, "SCN-002-E-010")))
def test_incorrect_and_missing_numerical_evidence(field: str, value: object, evidence_id: str) -> None:
    incorrect = evaluate_scenario_002_attempt(replace(answers_for(), **{field: value}))
    missing = evaluate_scenario_002_attempt(replace(answers_for(), **{field: None if not isinstance(value, dict) else {}}))
    assert result(incorrect, evidence_id) is EvidenceResult.NOT_OBSERVED
    assert result(missing, evidence_id) is EvidenceResult.INSUFFICIENT_EVIDENCE


def test_tolerance_boundary_and_all_routes_preserve_rating_limits() -> None:
    boundary = evaluate_scenario_002_attempt(replace(answers_for(), northstar_dso=EXPECTED_DSO + PERCENTAGE_TOLERANCE))
    outside = evaluate_scenario_002_attempt(replace(answers_for(), northstar_dso=EXPECTED_DSO + PERCENTAGE_TOLERANCE + 0.01))
    assert result(boundary, "SCN-002-E-005") is EvidenceResult.OBSERVED
    assert result(outside, "SCN-002-E-005") is EvidenceResult.NOT_OBSERVED
    for route in RecommendationRoute:
        report = evaluate_scenario_002_attempt(answers_for(route))
        assert result(report, "SCN-002-E-013") is EvidenceResult.OBSERVED
        assert result(report, "SCN-002-E-014") is EvidenceResult.OBSERVED
        assert report.scorecard.for_competency(Competency.COMMERCIAL_JUDGMENT).rating is CompetencyRating.CAPABLE
        assert report.scorecard.for_competency(Competency.STAKEHOLDER_COMMUNICATION).rating is CompetencyRating.NOT_ASSESSED
        assert report.scorecard.for_competency(Competency.STRATEGIC_LEADERSHIP).rating is CompetencyRating.NOT_ASSESSED


def test_each_recommendation_route_has_distinct_controls_protections_and_assumptions() -> None:
    assert len({frozenset(values.items()) for values in ROUTE_SAFEGUARD_OPTIONS.values()}) == 4
    assert len({frozenset(values.items()) for values in ROUTE_PROTECTION_OPTIONS.values()}) == 4
    assert len(set(REQUIRED_ROUTE_ASSUMPTIONS.values())) == 4
    for route in RecommendationRoute:
        answer = answers_for(route)
        report = evaluate_scenario_002_attempt(answer)
        assert result(report, "SCN-002-E-014") is EvidenceResult.OBSERVED
        assert result(report, "SCN-002-E-015") is EvidenceResult.OBSERVED
        assert result(evaluate_scenario_002_attempt(replace(answer, protections=frozenset())), "SCN-002-E-015") is EvidenceResult.NOT_OBSERVED
        assert result(evaluate_scenario_002_attempt(replace(answer, assumptions=frozenset())), "SCN-002-E-015") is EvidenceResult.NOT_OBSERVED


def test_provision_creation_settlement_and_release_have_distinct_classifications() -> None:
    assert "current-period P&L" in CLASSIFICATION_OPTIONS["provision_creation"]
    assert "cash and balance sheet, not current-period P&L" in CLASSIFICATION_OPTIONS["provision_settlement"]
    assert "current-period P&L and balance sheet" in CLASSIFICATION_OPTIONS["provision_release"]
    incorrect = evaluate_scenario_002_attempt(
        replace(answers_for(), classifications=EXPECTED_CLASSIFICATIONS - {"provision_settlement"})
    )
    assert result(incorrect, "SCN-002-E-012") is EvidenceResult.NOT_OBSERVED


def test_stage_three_saved_values_rebuild_the_full_scenario_002_attempt() -> None:
    answers = answers_for()
    route = answers.recommendation
    assert route is not None
    state: dict[str, object] = {
        "saved_input_quality": answers.quality_interpretation,
        "saved_input_operating_cash": answers.operating_cash_flow,
        "saved_input_cash_conversion": answers.cash_conversion_percent,
        "saved_input_cash_absorber": answers.largest_cash_absorber,
        "saved_input_dso": answers.northstar_dso,
        "saved_input_concentration": answers.receivable_concentration_percent,
        "saved_input_net_working_capital": answers.net_working_capital,
        "saved_input_balance_sheet_exposure": answers.balance_sheet_exposure,
        "saved_input_exposure_at_risk": answers.exposure_at_risk,
        "saved_input_classifications": list(answers.classifications),
        "saved_input_recommendation": route.value,
        f"saved_input_safeguards_{route.value}": list(answers.safeguards),
        "saved_input_protections": list(answers.protections),
        "saved_input_assumptions": list(answers.assumptions),
        "saved_input_ceo_response": answers.ceo_response,
    }
    for prefix, values in (("ebitda", answers.route_ebitda), ("route_cash", answers.route_operating_cash), ("low_cash", answers.route_low_cash), ("rcf_draw", answers.route_rcf_draw), ("headroom", answers.route_headroom)):
        state.update({f"saved_input_{prefix}_{route_name}": value for route_name, value in values.items()})
    assert build_scenario_002_answers(state) == answers


def test_explanations_are_post_submission_and_skip_is_unassessed() -> None:
    report = evaluate_scenario_002_attempt(answers_for())
    numerical = {"SCN-002-E-002", "SCN-002-E-003", "SCN-002-E-005", "SCN-002-E-006", "SCN-002-E-007", "SCN-002-E-008", "SCN-002-E-009", "SCN-002-E-010", "SCN-002-E-011"}
    assert {record.evidence_id for record in report.evidence_records if record.worked_solution} == numerical
    assert all(record.judgment_explanation for record in report.evidence_records if record.evidence_id in {"SCN-002-E-001", "SCN-002-E-004", "SCN-002-E-012", "SCN-002-E-013", "SCN-002-E-014", "SCN-002-E-015"})
    skipped = skipped_scenario_002_report()
    assert not skipped.evidence_records
    assert all(item.rating is CompetencyRating.NOT_ASSESSED for item in skipped.scorecard.results)
