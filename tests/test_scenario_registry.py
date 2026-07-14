"""Tests for the curated multi-scenario registry and shared browser shell."""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from finance_director_coach.models import CompetencyRating, EvidenceResult
from finance_director_coach.scenarios.registry import SCENARIOS, get_scenario
from finance_director_coach.scenarios.scenario_002_evaluation import evaluate_scenario_002_attempt
from finance_director_coach import streamlit_ui
from finance_director_coach.streamlit_ui import (
    GUIDED_STAGE,
    RESULTS_STAGE,
    SCENARIO_STAGE,
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
        "input_northstar_dso": 121.7,
        "saved_input_classifications": ["receivables"],
    }
    reset_session_state(state)
    assert state == {"stage": WELCOME_STAGE, "guided_step": 0, "path": None, "answers": None, "report": None}


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


def test_scenario_two_pack_is_loaded_from_registry_without_assessed_results() -> None:
    pack = learner_financial_pack_text("SCN-002")
    assert pack == "\n\n".join(f"{section.title}\n{section.body}" for section in get_scenario("SCN-002").content.financial_pack)
    for hidden_phrase in ("annual EBITDA to 5.27", "annual EBITDA is 3.06", "Operating cash flow is GBP -1.54", "Low cash points"):
        assert hidden_phrase not in pack


@pytest.mark.parametrize("scenario_id", ("SCN-001", "SCN-002"))
def test_financial_pack_briefing_uses_prose_fallback_or_static_tables(scenario_id: str) -> None:
    entrypoint = Path(__file__).parents[1] / "streamlit_app.py"
    scenario = get_scenario(scenario_id)
    app = AppTest.from_file(str(entrypoint), default_timeout=10).run()
    app.session_state["selected_scenario_id"] = scenario_id
    app.session_state["stage"] = SCENARIO_STAGE
    app.run()

    assert not app.exception
    assert [expander.label for expander in app.expander] == [
        section.title for section in scenario.content.financial_pack
    ]
    assert app.expander[0].proto.expanded
    assert app.get("code") == []
    rendered = "\n".join(item.value for item in app.markdown)
    for section in scenario.content.financial_pack:
        if section.tables:
            for table in section.tables:
                if table.title:
                    assert f"**{table.title}**" in rendered
        else:
            for paragraph in section.body.split("\n\n"):
                if paragraph.strip():
                    assert paragraph in rendered
    if scenario_id == "SCN-002":
        assert len(app.dataframe) == 13
        assert app.get("data_editor") == []


def test_scenario_two_guided_financial_pack_uses_the_same_structured_renderer() -> None:
    entrypoint = Path(__file__).parents[1] / "streamlit_app.py"
    scenario = get_scenario("SCN-002")
    app = AppTest.from_file(str(entrypoint), default_timeout=10).run()
    app.session_state["selected_scenario_id"] = "SCN-002"
    app.session_state["stage"] = GUIDED_STAGE
    app.run()

    assert not app.exception
    assert [expander.label for expander in app.expander] == ["Review the financial pack"]
    assert app.get("code") == []
    rendered = "\n".join(item.value for item in app.markdown)
    for section in scenario.content.financial_pack:
        assert f"**{section.title}**" in rendered
        for table in section.tables:
            if table.title:
                assert f"**{table.title}**" in rendered
    assert len(app.dataframe) == 13
    assert app.get("data_editor") == []
    for hidden_phrase in ("annual EBITDA to 5.27", "annual EBITDA is 3.06", "Operating cash flow is GBP -1.54", "Low cash points"):
        assert hidden_phrase not in rendered


def test_scenario_two_structured_pack_retains_required_inputs_without_answers() -> None:
    scenario = get_scenario("SCN-002")
    table_text = " ".join(
        " ".join((table.title, *table.column_headings, *(cell for row in table.rows for cell in row)))
        for section in scenario.content.financial_pack
        for table in section.tables
    )
    for required_input in (
        "Northstar receivables GBP 3.00m",
        "Northstar unbilled implementation work GBP 1.80m",
        "Undrawn RCF GBP 4.00m",
        "70% of the price uplift is billed and collected within the forecast period.",
        "Foregone customer cash receipts 7.00",
    ):
        assert required_input in table_text
    for hidden_answer in (
        "Operating cash flow is GBP -1.54m",
        "annual EBITDA to 5.27",
        "Low cash points",
        "required RCF draws",
    ):
        assert hidden_answer not in table_text


def test_structured_table_renderer_hides_indices_without_editable_widgets(monkeypatch) -> None:
    table = get_scenario("SCN-002").content.financial_pack[0].tables[0]
    captured: dict[str, object] = {}

    monkeypatch.setattr(streamlit_ui.st, "markdown", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        streamlit_ui.st,
        "dataframe",
        lambda data, **kwargs: captured.update(data=data, **kwargs),
    )

    streamlit_ui._render_financial_pack_table(table)

    assert captured["hide_index"] is True
    assert captured["use_container_width"] is True
    assert captured["column_order"] == table.column_headings
    assert captured["data"] == [
        {"Metric": "Revenue", "FY2025": "40.00", "FY2026 forecast": "48.00"},
        {"Metric": "Gross profit", "FY2025": "18.00", "FY2026 forecast": "18.24"},
        {"Metric": "EBITDA", "FY2025": "4.80", "FY2026 forecast": "3.36"},
    ]


def test_scenario_two_guided_stages_do_not_render_post_submission_explanations() -> None:
    entrypoint = Path(__file__).parents[1] / "streamlit_app.py"
    for step in range(4):
        app = AppTest.from_file(str(entrypoint), default_timeout=10).run()
        app.session_state["selected_scenario_id"] = "SCN-002"
        app.session_state["stage"] = GUIDED_STAGE
        app.session_state["guided_step"] = step
        app.run()
        assert app.get("popover") == []
        assert "How was this calculated?" not in str(app)
        assert "Why does this matter?" not in str(app)


def test_scenario_two_stage_three_groups_all_inputs_in_route_tabs() -> None:
    entrypoint = Path(__file__).parents[1] / "streamlit_app.py"
    app = AppTest.from_file(str(entrypoint), default_timeout=10).run()
    app.session_state["selected_scenario_id"] = "SCN-002"
    app.session_state["stage"] = GUIDED_STAGE
    app.session_state["guided_step"] = 2
    app.run()
    assert [tab.label for tab in app.tabs] == [
        "Renew as proposed",
        "Renegotiate to target economics",
        "Exit and redeploy",
    ]
    assert len(app.number_input) == 15


def test_scenario_two_results_expose_calculations_only_after_submission() -> None:
    entrypoint = Path(__file__).parents[1] / "streamlit_app.py"
    report = evaluate_scenario_002_attempt(answers_for())
    app = AppTest.from_file(str(entrypoint), default_timeout=10).run()
    app.session_state["selected_scenario_id"] = "SCN-002"
    app.session_state["stage"] = RESULTS_STAGE
    app.session_state["path"] = "guided"
    app.session_state["answers"] = answers_for()
    app.session_state["report"] = report
    app.run()
    labels = [popover.proto.popover.label for popover in app.get("popover")]
    assert labels.count("How was this calculated?") == 9
    assert labels.count("Why does this matter?") == 6
    assert "GBP 3.36m - 2.40m" in str(app)


def test_scenario_library_selects_scenario_two_and_skip_remains_unassessed() -> None:
    entrypoint = Path(__file__).parents[1] / "streamlit_app.py"
    app = AppTest.from_file(str(entrypoint), default_timeout=10).run()
    app.radio(key="library_scenario_choice").set_value("SCN-002").run()
    app.button(key="start_scenario").click().run()
    app.button_group(key="path_choice").set_value("skip").run()
    app.button(key="continue_from_scenario").click().run()
    assert app.session_state["stage"] == RESULTS_STAGE
    rendered = "\n".join(item.value for item in app.get("markdown"))
    assert "Operating cash flow is GBP -1.54m" in rendered
    assert all("Not assessed" in expander.label for expander in app.expander[:5])


def test_scenario_two_summary_identifies_selected_scenario_without_hidden_learning_content() -> None:
    scenario = get_scenario("SCN-002")
    report = evaluate_scenario_002_attempt(answers_for())
    summary = build_pilot_summary(report, answers_for(), scenario)
    assert "Scenario ID: SCN-002" in summary
    assert "Scenario version: 2.0" in summary
    assert "SCN-002-E-001: Observed" in summary
    assert scenario.content.model_answer not in summary
    assert "GBP 3.36m - 2.40m" not in summary
