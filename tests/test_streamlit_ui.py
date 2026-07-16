"""Behavior tests for the FinanceOS Streamlit pilot layer."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
import importlib.util
from pathlib import Path

from streamlit.testing.v1 import AppTest

from finance_director_coach.models import (
    AssessmentSource,
    Competency,
    CompetencyRating,
    EvidenceResult,
    LearnerAnswers,
    RecommendationRoute,
)
from finance_director_coach.scenarios.scenario_001 import (
    HIRING_UNIT_WARNING,
    MONETARY_INPUT_GUIDANCE,
    SCENARIO_001,
)
from finance_director_coach import streamlit_ui


def test_streamlit_entrypoint_imports_successfully() -> None:
    entrypoint = Path(__file__).parents[1] / "streamlit_app.py"
    spec = importlib.util.spec_from_file_location("financeos_streamlit_entrypoint", entrypoint)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert callable(module.main)


def test_web_pack_is_loaded_from_core_without_answer_leakage() -> None:
    assert streamlit_ui.SCENARIO_001 is SCENARIO_001
    pack = streamlit_ui.learner_financial_pack_text()
    assert pack == "\n\n".join(
        f"{section.title}\n{section.body}" for section in SCENARIO_001.financial_pack
    )
    for derived_label in (
        "Operating cash before interest and tax",
        "Net operating cash",
        "Net decrease in cash",
        "H2 hiring cost",
        "Annual recurring hiring cost",
        "Hiring-case cash low point",
        "Hiring-case December cash",
        "Cash after hiring",
        "Shortfall below the board cash floor",
        "Headroom above the lender minimum",
    ):
        assert derived_label not in pack


def test_guided_monetary_sections_show_units_without_worked_answers() -> None:
    entrypoint = Path(__file__).parents[1] / "streamlit_app.py"
    first_step = AppTest.from_file(str(entrypoint), default_timeout=10).run()
    first_step.session_state["stage"] = streamlit_ui.GUIDED_STAGE
    first_step.session_state["guided_step"] = 0
    first_step.run()
    assert [message.value for message in first_step.info] == [MONETARY_INPUT_GUIDANCE]
    assert first_step.get("popover") == []
    assert "GBP 84,000 / 12 = GBP 7,000" not in str(first_step)

    hiring_step = AppTest.from_file(str(entrypoint), default_timeout=10).run()
    hiring_step.session_state["stage"] = streamlit_ui.GUIDED_STAGE
    hiring_step.session_state["guided_step"] = 2
    hiring_step.run()
    assert [message.value for message in hiring_step.info] == [MONETARY_INPUT_GUIDANCE]
    assert HIRING_UNIT_WARNING in [message.value for message in hiring_step.warning]
    assert all(
        control.label.endswith("(GBP m)") for control in hiring_step.number_input
    )
    assert hiring_step.get("popover") == []
    rendered = str(hiring_step)
    assert "GBP 84,000 / 12 = GBP 7,000" not in rendered
    assert "GBP 0.58m" not in rendered
    assert "GBP 1.68m" not in rendered

    decision_step = AppTest.from_file(str(entrypoint), default_timeout=10).run()
    decision_step.session_state["stage"] = streamlit_ui.GUIDED_STAGE
    decision_step.session_state["guided_step"] = 3
    decision_step.session_state["saved_input_recommendation"] = (
        RecommendationRoute.CONDITIONALLY_APPROVE.value
    )
    decision_step.run()
    decision_rendered = str(decision_step)
    assert decision_step.get("popover") == []
    assert "GBP 0.58m" not in decision_rendered
    assert "GBP 1.68m" not in decision_rendered
    assert "GBP 84,000 / 12 = GBP 7,000" not in decision_rendered


def test_results_render_worked_calculation_popovers_for_both_outcomes(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    entrypoint = Path(__file__).parents[1] / "streamlit_app.py"

    for answers, expected_hiring_result in (
        (answer_factory(), EvidenceResult.OBSERVED),
        (
            replace(
                answer_factory(),
                cash_decrease=1.0,
                h2_hiring_cost=580.0,
                annual_hiring_cost=1680.0,
            ),
            EvidenceResult.NOT_OBSERVED,
        ),
    ):
        report = streamlit_ui.evaluate_guided_submission(answers)
        assert next(
            item for item in report.evidence_records if item.evidence_id == "E-006"
        ).result is expected_hiring_result
        app = AppTest.from_file(str(entrypoint), default_timeout=10).run()
        app.session_state["stage"] = streamlit_ui.RESULTS_STAGE
        app.session_state["path"] = "guided"
        app.session_state["answers"] = answers
        app.session_state["report"] = report
        app.run()
        assert not app.exception
        popovers = app.get("popover")
        assert len(popovers) == 6
        assert all(
            popover.proto.popover.label == "How was this calculated?"
            for popover in popovers
        )
        assert "GBP 84,000 / 12 = GBP 7,000" in popovers[3].markdown[0].value


def test_skip_to_solution_remains_not_assessed() -> None:
    report = streamlit_ui.skipped_evaluation_report()
    assert report.evidence_records == ()
    assert all(
        result.rating is CompetencyRating.NOT_ASSESSED
        and result.assessment_source is AssessmentSource.NOT_ASSESSED
        for result in report.scorecard.results
    )


def test_guided_submission_delegates_to_existing_evaluator(
    monkeypatch,
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    answers = answer_factory()
    marker = object()
    received: list[LearnerAnswers] = []

    def fake_evaluate(submitted: LearnerAnswers):
        received.append(submitted)
        return marker

    monkeypatch.setattr(streamlit_ui, "evaluate_attempt", fake_evaluate)
    assert streamlit_ui.evaluate_guided_submission(answers) is marker
    assert received == [answers]


def test_guided_answers_survive_streamlit_widget_cleanup(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    answers = answer_factory()
    route = answers.recommendation
    assert route is not None
    state: dict[str, object] = {
        "saved_input_revenue_growth": answers.revenue_growth_percent,
        "saved_input_ebitda_growth": answers.ebitda_growth_percent,
        "saved_input_cash_decrease": answers.cash_decrease,
        "saved_input_operating_cash": answers.operating_cash_before_interest_tax,
        "saved_input_net_operating_cash": answers.net_operating_cash,
        "saved_input_cash_drivers": list(answers.cash_drivers),
        "saved_input_largest_driver": answers.largest_cash_driver,
        "saved_input_risks": list(answers.risks),
        "saved_input_h2_hiring_cost": answers.h2_hiring_cost,
        "saved_input_annual_hiring_cost": answers.annual_hiring_cost,
        "saved_input_cash_low_point": answers.cash_low_point,
        "saved_input_december_cash": answers.december_cash,
        "saved_input_board_shortfall": answers.board_floor_shortfall,
        "saved_input_lender_headroom": answers.lender_headroom,
        "saved_input_thresholds": list(answers.threshold_interpretations),
        "saved_input_recommendation": route.value,
        f"saved_input_safeguards_{route.value}": list(answers.safeguards),
        "saved_input_missing_information": list(answers.missing_information),
        "saved_input_tradeoffs": list(answers.tradeoffs),
        "saved_input_ceo_response": answers.ceo_response,
    }

    assert streamlit_ui.build_answers_from_state(state) == answers


def test_web_submission_preserves_rating_boundaries_and_free_text_rule(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    short = streamlit_ui.evaluate_guided_submission(
        replace(answer_factory(), ceo_response="Approve.")
    )
    long = streamlit_ui.evaluate_guided_submission(
        replace(answer_factory(), ceo_response="Executive wording does not change evidence. " * 20)
    )
    commercial = short.scorecard.for_competency(Competency.COMMERCIAL_JUDGMENT)
    stakeholder = short.scorecard.for_competency(Competency.STAKEHOLDER_COMMUNICATION)
    strategic = short.scorecard.for_competency(Competency.STRATEGIC_LEADERSHIP)
    assert commercial.rating is CompetencyRating.CAPABLE
    assert stakeholder.rating is CompetencyRating.NOT_ASSESSED
    assert strategic.rating is CompetencyRating.NOT_ASSESSED
    assert short.evidence_records == long.evidence_records
    assert short.scorecard == long.scorecard


def test_restart_clears_attempt_and_widget_state() -> None:
    practice_attempts = [object()]
    state: dict[str, object] = {
        "stage": streamlit_ui.RESULTS_STAGE,
        "report": object(),
        "answers": object(),
        "input_ceo_response": "Confidential draft",
        "input_revenue_growth": 22.2,
        "practice_domain": "P&L",
        "practice_attempts": practice_attempts,
        "practice_card_id": "FINQA-1",
    }
    streamlit_ui.reset_session_state(state)
    assert state == {
        "stage": streamlit_ui.WELCOME_STAGE,
        "guided_step": 0,
        "path": None,
        "answers": None,
        "report": None,
        "practice_domain": "P&L",
        "practice_attempts": practice_attempts,
        "practice_card_id": "FINQA-1",
    }


def test_download_summary_contains_results_without_solution_or_hidden_state(
    answer_factory: Callable[[RecommendationRoute], LearnerAnswers],
) -> None:
    answers = replace(
        answer_factory(),
        ceo_response="Conditionally approve with cash and collections gates.",
    )
    report = streamlit_ui.evaluate_guided_submission(answers)
    summary = streamlit_ui.build_pilot_summary(report, answers)
    assert "Scenario ID: SCN-001" in summary
    assert "Recommendation route: Conditionally approve" in summary
    assert "E-001: Observed" in summary
    assert "Financial Insight: Strong [source: deterministic]" in summary
    assert "Conditionally approve with cash and collections gates." in summary
    assert "Self-review questions" in summary
    assert "not stored by FinanceOS" in summary
    assert SCENARIO_001.model_answer not in summary
    assert SCENARIO_001.debrief not in summary
    assert "Confidential draft" not in summary
    assert "GBP 84,000 / 12 = GBP 7,000" not in summary


def test_streamlit_welcome_skip_and_restart_flow() -> None:
    entrypoint = Path(__file__).parents[1] / "streamlit_app.py"
    app = AppTest.from_file(str(entrypoint), default_timeout=10).run()
    assert not app.exception
    assert app.title[0].value == "FinanceOS"

    app.button(key="start_scenario").click().run()
    assert not app.exception
    assert app.title[0].value == SCENARIO_001.title

    app.button_group(key="path_choice").set_value("skip").run()
    app.button(key="continue_from_scenario").click().run()
    assert not app.exception
    assert app.session_state["stage"] == streamlit_ui.RESULTS_STAGE
    report = app.session_state["report"]
    assert all(
        result.rating is CompetencyRating.NOT_ASSESSED
        for result in report.scorecard.results
    )
    assert any(
        "Complete financial reconciliation" == subheader.value
        for subheader in app.subheader
    )
    assert app.get("popover") == []

    app.button(key="results_restart").click().run()
    assert not app.exception
    assert app.session_state["stage"] == streamlit_ui.WELCOME_STAGE
    assert app.title[0].value == "FinanceOS"
