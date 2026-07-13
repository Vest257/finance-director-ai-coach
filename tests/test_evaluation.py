"""Deterministic evidence and competency boundary tests."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace

import pytest

from finance_director_coach.evaluation import evaluate_attempt, skipped_evaluation_report
from finance_director_coach.models import (
    AssessmentSource,
    Competency,
    CompetencyRating,
    EvaluationReport,
    EvidenceRecord,
    EvidenceResult,
    LearnerAnswers,
    RecommendationRoute,
)
from finance_director_coach.scenarios.scenario_001 import REQUIRED_ROUTE_SAFEGUARDS


def record(report: EvaluationReport, evidence_id: str) -> EvidenceRecord:
    return next(item for item in report.evidence_records if item.evidence_id == evidence_id)


def test_evidence_record_worked_solution_is_backward_compatible() -> None:
    evidence = EvidenceRecord(
        evidence_id="E-test",
        learner_input="input",
        expected_rule="rule",
        result=EvidenceResult.OBSERVED,
        competencies_informed=(Competency.FINANCIAL_INSIGHT,),
        feedback="feedback",
        improvement_guidance="guidance",
    )
    assert evidence.worked_solution is None


def test_correct_and_incorrect_growth_calculations(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    correct = evaluate_attempt(answer_factory())
    incorrect = evaluate_attempt(replace(answer_factory(), revenue_growth_percent=18.0))
    assert record(correct, "E-001").result is EvidenceResult.OBSERVED
    assert record(incorrect, "E-001").result is EvidenceResult.NOT_OBSERVED


def test_percentage_tolerance_boundary(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    at_boundary = evaluate_attempt(
        replace(answer_factory(), revenue_growth_percent=22.4, ebitda_growth_percent=26.1)
    )
    outside = evaluate_attempt(replace(answer_factory(), revenue_growth_percent=22.4001))
    assert record(at_boundary, "E-001").result is EvidenceResult.OBSERVED
    assert record(outside, "E-001").result is EvidenceResult.NOT_OBSERVED


def test_monetary_tolerance_boundary(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    at_boundary = evaluate_attempt(replace(answer_factory(), cash_decrease=2.75))
    outside = evaluate_attempt(replace(answer_factory(), cash_decrease=2.7501))
    assert record(at_boundary, "E-002").result is EvidenceResult.OBSERVED
    assert record(outside, "E-002").result is EvidenceResult.NOT_OBSERVED


def test_only_numerical_evidence_records_have_worked_solutions(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    report = evaluate_attempt(answer_factory())
    numerical_ids = {"E-001", "E-002", "E-003", "E-006", "E-007", "E-008"}
    assert {
        item.evidence_id for item in report.evidence_records if item.worked_solution is not None
    } == numerical_ids
    assert all(
        item.worked_solution is None
        for item in report.evidence_records
        if item.evidence_id not in numerical_ids
    )


def test_worked_solutions_are_available_for_observed_and_not_observed_inputs(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    correct = evaluate_attempt(answer_factory())
    incorrect = evaluate_attempt(
        replace(
            answer_factory(),
            cash_decrease=1.0,
            h2_hiring_cost=580.0,
            annual_hiring_cost=1680.0,
        )
    )
    for evidence_id in ("E-002", "E-006"):
        assert record(correct, evidence_id).result is EvidenceResult.OBSERVED
        assert record(incorrect, evidence_id).result is EvidenceResult.NOT_OBSERVED
        assert record(incorrect, evidence_id).worked_solution == record(
            correct, evidence_id
        ).worked_solution


def test_hiring_worked_solution_contains_required_phasing_and_unit_steps(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    solution = record(evaluate_attempt(answer_factory()), "E-006").worked_solution
    assert solution is not None
    for expected_step in (
        "GBP 84,000 / 12 = GBP 7,000",
        "September cohort",
        "four months of recurring cost plus onboarding",
        "GBP 0.36m",
        "November cohort",
        "two months of recurring cost plus onboarding",
        "GBP 0.22m",
        "H2 total",
        "GBP 0.58m",
        "Annual recurring cost = 20 x GBP 84,000",
        "GBP 1.68m",
        "Enter **0.58** and **1.68** because the fields use GBP millions",
    ):
        assert expected_step in solution


def test_working_capital_driver_selection(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    correct = evaluate_attempt(answer_factory())
    incorrect = evaluate_attempt(
        replace(answer_factory(), cash_drivers=answer_factory().cash_drivers | {"dividends"})
    )
    assert record(correct, "E-004").result is EvidenceResult.OBSERVED
    assert record(incorrect, "E-004").result is EvidenceResult.NOT_OBSERVED


def test_largest_cash_driver_recognition(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    correct = evaluate_attempt(answer_factory())
    incorrect = evaluate_attempt(replace(answer_factory(), largest_cash_driver="inventory"))
    assert record(correct, "E-005").result is EvidenceResult.OBSERVED
    assert record(incorrect, "E-005").result is EvidenceResult.NOT_OBSERVED


def test_missing_information_and_risk_recognition(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    complete = evaluate_attempt(answer_factory())
    incomplete = evaluate_attempt(
        replace(
            answer_factory(),
            missing_information=frozenset({"collections"}),
            risks=frozenset({"overdue_receivables"}),
        )
    )
    assert record(complete, "E-011").result is EvidenceResult.OBSERVED
    assert record(complete, "E-014").result is EvidenceResult.OBSERVED
    assert record(complete, "E-015").result is EvidenceResult.OBSERVED
    assert record(incomplete, "E-011").result is EvidenceResult.NOT_OBSERVED
    assert record(incomplete, "E-014").result is EvidenceResult.NOT_OBSERVED
    assert record(incomplete, "E-015").result is EvidenceResult.NOT_OBSERVED


def test_board_floor_and_lender_covenant_interpretation(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    correct = evaluate_attempt(answer_factory())
    incorrect = evaluate_attempt(
        replace(
            answer_factory(),
            threshold_interpretations=frozenset(
                {"board_floor_retained", "lender_covenant_breached"}
            ),
        )
    )
    assert record(correct, "E-008").result is EvidenceResult.OBSERVED
    assert record(incorrect, "E-008").result is EvidenceResult.NOT_OBSERVED
    assert "CO-005" in incorrect.critical_omissions


@pytest.mark.parametrize("route", list(RecommendationRoute))
def test_all_recommendation_routes_receive_equivalent_deterministic_outcomes(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
    route: RecommendationRoute,
) -> None:
    report = evaluate_attempt(answer_factory(route))
    assert record(report, "E-009").result is EvidenceResult.OBSERVED
    assert record(report, "E-010").result is EvidenceResult.OBSERVED
    commercial = report.scorecard.for_competency(Competency.COMMERCIAL_JUDGMENT)
    assert commercial.rating is CompetencyRating.CAPABLE
    assert commercial.assessment_source is AssessmentSource.DETERMINISTIC


@pytest.mark.parametrize("route", list(RecommendationRoute))
def test_each_route_requires_its_core_safeguards(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
    route: RecommendationRoute,
) -> None:
    required = REQUIRED_ROUTE_SAFEGUARDS[route]
    incomplete = frozenset(set(required) - {next(iter(required))})
    report = evaluate_attempt(replace(answer_factory(route), safeguards=incomplete))
    assert record(report, "E-010").result is EvidenceResult.NOT_OBSERVED
    assert report.scorecard.for_competency(
        Competency.COMMERCIAL_JUDGMENT
    ).rating is CompetencyRating.DEVELOPING


def test_critical_omission_gates(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    base = answer_factory(RecommendationRoute.APPROVE)
    co1 = evaluate_attempt(
        replace(base, operating_cash_before_interest_tax=1.0, cash_drivers=frozenset({"dividends"}))
    )
    co2 = evaluate_attempt(replace(base, cash_decrease=1.0))
    co3 = evaluate_attempt(replace(base, recommendation=None, safeguards=frozenset()))
    co4 = evaluate_attempt(replace(base, safeguards=frozenset({"weekly_cash_monitoring"})))
    co6 = evaluate_attempt(replace(base, risks=base.risks | {"assumptions_are_certain"}))
    assert "CO-001" in co1.critical_omissions
    assert "CO-002" in co2.critical_omissions
    assert "CO-003" in co3.critical_omissions
    assert "CO-004" in co4.critical_omissions
    assert "CO-006" in co6.critical_omissions


def test_complete_attempt_gets_deterministic_financial_ratings(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    report = evaluate_attempt(answer_factory())
    assert report.scorecard.for_competency(
        Competency.FINANCIAL_INSIGHT
    ).rating is CompetencyRating.STRONG
    assert report.scorecard.for_competency(
        Competency.CASH_AND_RISK_DISCIPLINE
    ).rating is CompetencyRating.STRONG


def test_commercial_judgment_deterministic_rating_is_capped_at_capable(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    report = evaluate_attempt(answer_factory())
    result = report.scorecard.for_competency(Competency.COMMERCIAL_JUDGMENT)
    assert record(report, "E-013").result is EvidenceResult.OBSERVED
    assert result.rating is CompetencyRating.CAPABLE
    assert result.assessment_source is AssessmentSource.DETERMINISTIC
    assert result.limitation and "capped" in result.limitation


def test_communication_and_leadership_remain_not_assessed(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    report = evaluate_attempt(answer_factory())
    stakeholder = report.scorecard.for_competency(Competency.STAKEHOLDER_COMMUNICATION)
    strategic = report.scorecard.for_competency(Competency.STRATEGIC_LEADERSHIP)
    assert stakeholder.rating is CompetencyRating.NOT_ASSESSED
    assert strategic.rating is CompetencyRating.NOT_ASSESSED
    assert stakeholder.assessment_source is AssessmentSource.NOT_ASSESSED
    assert strategic.assessment_source is AssessmentSource.NOT_ASSESSED
    assert strategic.evidence_used == ("E-009", "E-011")


def test_free_text_keywords_and_length_do_not_affect_evaluation(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    short = evaluate_attempt(replace(answer_factory(), ceo_response="Approve."))
    long = evaluate_attempt(
        replace(
            answer_factory(),
            ceo_response=(
                "cash EBITDA persuasive strategic leadership collections covenant " * 20
            ).strip(),
        )
    )
    assert short.evidence_records == long.evidence_records
    assert short.scorecard == long.scorecard
    assert short.critical_omissions == long.critical_omissions


def test_empty_attempt_is_not_assessed_not_failed() -> None:
    report = evaluate_attempt(LearnerAnswers())
    assert report.critical_omissions == ()
    assert all(
        result.rating is CompetencyRating.NOT_ASSESSED
        for result in report.scorecard.results
    )


def test_skip_to_solution_collects_no_evidence() -> None:
    report = skipped_evaluation_report()
    assert report.evidence_records == ()
    assert report.critical_omissions == ()
    assert all(
        result.rating is CompetencyRating.NOT_ASSESSED
        for result in report.scorecard.results
    )


def test_evidence_traceability_and_required_fields(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    report = evaluate_attempt(answer_factory())
    assert {item.evidence_id for item in report.evidence_records} == {
        f"E-{number:03d}" for number in range(1, 16)
    }
    for item in report.evidence_records:
        assert item.learner_input
        assert item.expected_rule
        assert item.competencies_informed
        assert item.feedback
        assert item.improvement_guidance
    for result in report.scorecard.results:
        assert result.assessment_source
        assert result.explanation
        assert result.improvement_guidance
