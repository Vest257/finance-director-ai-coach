"""Tests for the curated multi-scenario registry and shared browser shell."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from streamlit.testing.v1 import AppTest

from finance_director_coach.models import EvidenceResult
from finance_director_coach.scenarios.registry import SCENARIOS, get_scenario
from finance_director_coach.scenarios.scenario_002_evaluation import evaluate_scenario_002_attempt
from finance_director_coach.streamlit_ui import (
    GUIDED_STAGE,
    RESULTS_STAGE,
    WELCOME_STAGE,
    build_pilot_summary,
    learner_financial_pack_text,
    reset_session_state,
)

from tests.test_scenario_002 import answers_for


def test_registry_contains_unique_scenario_ids_and_distinct_typed_boundaries() -> None:
    assert tuple(scenario.content.scenario_id for scenario in SCENARIOS) == ("SCN-001", "SCN-002")
    assert len({scenario.content.scenario_id for scenario in SCENARIOS}) == len(SCENARIOS)
    assert get_scenario("SCN-001").content.title.startswith("Growth With Falling Cash")
    assert get_scenario("SCN-002").content.title.startswith("Growth at Any Price")
    assert get_scenario("SCN-001").build_answers is not get_scenario("SCN-002").build_answers
    assert get_scenario("SCN-001").evaluate_attempt is not get_scenario("SCN-002").evaluate_attempt
    report = get_scenario("SCN-002").evaluate_attempt(answers_for())
    assert next(record for record in report.evidence_records if record.evidence_id == "SCN-002-E-001").result is EvidenceResult.OBSERVED


def test_reset_clears_selected_scenario_and_all_attempt_state() -> None:
    state: dict[str, object] = {
        "stage": RESULTS_STAGE,
        "selected_scenario_id": "SCN-002",
        "report": object(),
        "answers": object(),
        "input_customer_contribution": 3.0,
        "saved_input_top_drivers": ["deep_discount"],
    }
    reset_session_state(state)
    assert state == {
        "stage": WELCOME_STAGE,
        "guided_step": 0,
        "path": None,
        "answers": None,
        "report": None,
    }


def test_switching_scenarios_cannot_retain_prior_scenario_widget_values() -> None:
    state: dict[str, object] = {
        "selected_scenario_id": "SCN-001",
        "input_h2_hiring_cost": 0.58,
        "saved_input_recommendation": "conditionally_approve",
        "report": object(),
    }
    reset_session_state(state)
    state["selected_scenario_id"] = "SCN-002"
    assert "input_h2_hiring_cost" not in state
    assert "saved_input_recommendation" not in state
    assert get_scenario(str(state["selected_scenario_id"])).content.scenario_id == "SCN-002"


def test_shared_shell_uses_registry_content_not_hardwired_scenario_one_fields() -> None:
    source = (Path(__file__).parents[1] / "src" / "finance_director_coach" / "streamlit_ui.py").read_text()
    assert "SCENARIO_001.financial_pack" not in source
    assert "SCENARIO_001.model_answer" not in source
    assert "SCENARIO_001.reconciliation_summary" not in source


def test_scenario_two_pack_is_loaded_from_the_registry_without_answer_leakage() -> None:
    pack = learner_financial_pack_text("SCN-002")
    assert pack == "\n\n".join(
        f"{section.title}\n{section.body}" for section in get_scenario("SCN-002").content.financial_pack
    )
    for hidden_phrase in (
        "Economically attractive revenue =",
        "Required price increase =",
        "Contribution margin =",
        "Company EBITDA is GBP",
    ):
        assert hidden_phrase not in pack


def test_scenario_two_results_show_post_submission_calculation_and_judgment_popovers() -> None:
    entrypoint = Path(__file__).parents[1] / "streamlit_app.py"
    correct = answers_for()
    incorrect = replace(correct, price_increase=0.10)
    for answers, expected_result in ((correct, EvidenceResult.OBSERVED), (incorrect, EvidenceResult.NOT_OBSERVED)):
        report = evaluate_scenario_002_attempt(answers)
        assert next(record for record in report.evidence_records if record.evidence_id == "SCN-002-E-006").result is expected_result
        app = AppTest.from_file(str(entrypoint), default_timeout=10).run()
        app.session_state["selected_scenario_id"] = "SCN-002"
        app.session_state["stage"] = RESULTS_STAGE
        app.session_state["path"] = "guided"
        app.session_state["answers"] = answers
        app.session_state["report"] = report
        app.run()
        labels = [popover.proto.popover.label for popover in app.get("popover")]
        assert labels.count("How was this calculated?") == 7
        assert labels.count("Why does this matter?") == 7
        assert "GBP 6.00m / 0.55" in app.get("popover")[5].markdown[0].value


def test_scenario_two_guided_stage_has_no_post_submission_answers_or_popovers() -> None:
    entrypoint = Path(__file__).parents[1] / "streamlit_app.py"
    app = AppTest.from_file(str(entrypoint), default_timeout=10).run()
    app.session_state["selected_scenario_id"] = "SCN-002"
    app.session_state["stage"] = GUIDED_STAGE
    app.session_state["guided_step"] = 1
    app.run()
    rendered = str(app)
    assert app.get("popover") == []
    for hidden_value in ("GBP 10.91m", "GBP 1.91m", "21.2%", "GBP 1.05m", "29.8%"):
        assert hidden_value not in rendered


def test_scenario_library_selects_each_scenario_and_skip_results_identify_it() -> None:
    entrypoint = Path(__file__).parents[1] / "streamlit_app.py"
    app = AppTest.from_file(str(entrypoint), default_timeout=10).run()
    assert "Growth With Falling Cash" in str(app)
    assert "Growth at Any Price" in str(app)
    app.radio(key="library_scenario_choice").set_value("SCN-002").run()
    app.button(key="start_scenario").click().run()
    assert app.session_state["selected_scenario_id"] == "SCN-002"
    assert app.title[0].value == get_scenario("SCN-002").content.title
    app.button_group(key="path_choice").set_value("skip").run()
    app.button(key="continue_from_scenario").click().run()
    assert app.session_state["stage"] == RESULTS_STAGE
    assert any("SCN-002" in caption.value for caption in app.caption)
    app.button(key="results_restart").click().run()
    assert app.session_state["stage"] == WELCOME_STAGE
    assert "selected_scenario_id" not in app.session_state


def test_scenario_two_summary_identifies_selected_scenario_without_hidden_learning_content() -> None:
    scenario = get_scenario("SCN-002")
    answers = answers_for()
    report = evaluate_scenario_002_attempt(answers)
    summary = build_pilot_summary(report, answers, scenario)
    assert "Scenario ID: SCN-002" in summary
    assert "Scenario version: 1.0" in summary
    assert "Scenario provenance: Synthetic FinanceOS scenario" in summary
    assert "SCN-002-E-001: Observed" in summary
    assert scenario.content.model_answer not in summary
    assert "GBP 6.00m / 0.55" not in summary
