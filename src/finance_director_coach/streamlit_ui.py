"""Shared Streamlit shell for the curated FinanceOS scenario library."""

from __future__ import annotations

from collections.abc import Callable, Mapping, MutableMapping

import streamlit as st

from finance_director_coach.evaluation import evaluate_attempt, skipped_evaluation_report
from finance_director_coach.models import EvaluationReport, LearnerAnswers
from finance_director_coach.scenarios.contracts import GuidedScenarioContext, ScenarioRegistration
from finance_director_coach.scenarios.registry import (
    SCENARIOS,
    SCENARIO_001_REGISTRATION,
    get_scenario,
)
from finance_director_coach.scenarios.scenario_001_adapter import build_scenario_001_answers

# Retained as a public compatibility surface for the original browser-pilot tests.
SCENARIO_001 = SCENARIO_001_REGISTRATION.content

WELCOME_STAGE = "welcome"
SCENARIO_STAGE = "scenario"
GUIDED_STAGE = "guided"
RESULTS_STAGE = "results"

APP_CSS = """
<style>
    :root {
        --finance-ink: #172121;
        --finance-muted: #52605f;
        --finance-line: #d8dfdc;
        --finance-teal: #0f766e;
        --finance-burgundy: #8b3345;
    }
    .stApp { color: var(--finance-ink); }
    .block-container { max-width: 1080px; padding-top: 2.2rem; padding-bottom: 4rem; }
    h1, h2, h3, p, label, button { letter-spacing: 0 !important; }
    h1 { font-size: 2.45rem !important; line-height: 1.12 !important; }
    h2 { font-size: 1.55rem !important; line-height: 1.25 !important; }
    h3 { font-size: 1.1rem !important; line-height: 1.35 !important; }
    .pilot-kicker { color: var(--finance-teal); font-size: 0.78rem; font-weight: 700; margin: 0 0 0.45rem 0; text-transform: uppercase; }
    .pilot-product { color: var(--finance-muted); font-size: 1.08rem; margin: -0.7rem 0 1.5rem 0; }
    .pilot-rule { border-top: 1px solid var(--finance-line); margin: 1rem 0 1.5rem 0; }
    div[data-testid="stExpander"] { border-color: var(--finance-line); border-radius: 6px; }
    div[data-testid="stCode"] pre { background: #f1f4f2; border: 1px solid var(--finance-line); border-radius: 4px; color: var(--finance-ink); font-size: 0.84rem; }
    div[data-testid="stAlert"] { border-radius: 6px; }
    div[data-testid="stButton"] button, div[data-testid="stDownloadButton"] button { border-radius: 6px; min-height: 2.65rem; }
    .scenario-metadata { border-top: 1px solid var(--finance-line); padding: 0.75rem 0 0.5rem 0; }
    @media (max-width: 640px) {
        .block-container { padding: 1.2rem 1rem 3rem 1rem; }
        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.35rem !important; }
        div[data-testid="stCode"] pre { font-size: 0.76rem; }
    }
</style>
"""


def initialize_session_state(state: MutableMapping[str, object]) -> None:
    """Initialize only in-memory state shared across registered scenarios."""

    state.setdefault("stage", WELCOME_STAGE)
    state.setdefault("guided_step", 0)
    state.setdefault("path", None)
    state.setdefault("answers", None)
    state.setdefault("report", None)


def reset_session_state(state: MutableMapping[str, object]) -> None:
    """Return to the library and remove the selected scenario and all widget state."""

    for key in list(state):
        del state[key]
    initialize_session_state(state)


def _active_scenario(state: Mapping[str, object]) -> ScenarioRegistration[object]:
    selected_id = state.get("selected_scenario_id")
    if isinstance(selected_id, str) and selected_id in {scenario.content.scenario_id for scenario in SCENARIOS}:
        return get_scenario(selected_id)
    # The fallback protects direct deep-link and legacy test entry points. The library itself
    # always requires a learner choice before it enters a scenario.
    return get_scenario("SCN-001")


def learner_financial_pack_text(scenario_id: str = "SCN-001") -> str:
    """Return the exact learner-facing financial pack for a registered scenario."""

    scenario = get_scenario(scenario_id)
    return "\n\n".join(
        f"{section.title}\n{section.body}" for section in scenario.content.financial_pack
    )


def evaluate_guided_submission(answers: LearnerAnswers) -> EvaluationReport:
    """Compatibility wrapper that delegates Scenario 001 attempts to its unchanged evaluator."""

    return evaluate_attempt(answers)


def build_answers_from_state(state: Mapping[str, object]) -> LearnerAnswers:
    """Compatibility wrapper for the unchanged Scenario 001 answer model."""

    return build_scenario_001_answers(state)


def _submit_active_scenario(scenario: ScenarioRegistration[object], answers: object) -> None:
    report = scenario.evaluate_attempt(answers)
    st.session_state["answers"] = answers
    st.session_state["report"] = report
    st.session_state["stage"] = RESULTS_STAGE
    st.rerun()


def build_pilot_summary(
    report: EvaluationReport,
    answers: object | None,
    scenario: ScenarioRegistration[object] | None = None,
) -> str:
    """Create a local plain-text learner summary without hidden solution content."""

    selected_scenario = scenario or get_scenario("SCN-001")
    typed_answers = answers if answers is not None else None
    lines = [
        "FinanceOS Alpha 0.1 - Pilot summary",
        f"Scenario ID: {selected_scenario.content.scenario_id}",
        f"Scenario version: {selected_scenario.metadata.version}",
        f"Scenario provenance: {selected_scenario.metadata.provenance}",
        f"Recommendation route: {selected_scenario.recommendation_label(typed_answers)}",
        "",
        "Evidence results",
    ]
    if report.evidence_records:
        lines.extend(f"- {record.evidence_id}: {record.result.value}" for record in report.evidence_records)
    else:
        lines.append("- No assessed learner evidence was collected.")
    lines.extend(["", "Competency scorecard"])
    for result in report.scorecard.results:
        lines.append(
            f"- {result.competency.value}: {result.rating.value} "
            f"[source: {result.assessment_source.value}]"
        )
    lines.extend(["", "Critical omissions"])
    if report.critical_omissions:
        lines.extend(f"- {omission}" for omission in report.critical_omissions)
    else:
        lines.append("- None")
    lines.extend(["", "Learner CEO response"])
    lines.append(selected_scenario.ceo_response(typed_answers) or "Not submitted")
    lines.extend(["", "Self-review questions"])
    lines.extend(f"- {item}" for item in selected_scenario.content.self_review_checklist)
    lines.extend(
        [
            "",
            "This summary was generated locally and is not stored by FinanceOS.",
            "The CEO response was not automatically scored.",
        ]
    )
    return "\n".join(lines)


def _set_stage(stage: str) -> None:
    st.session_state["stage"] = stage
    st.rerun()


def _return_to_library() -> None:
    reset_session_state(st.session_state)
    st.rerun()


def _render_brand_header(show_restart: bool = False) -> None:
    left, right = st.columns([5, 1])
    with left:
        st.markdown('<p class="pilot-kicker">FinanceOS / Alpha 0.1</p>', unsafe_allow_html=True)
    with right:
        if show_restart and st.button(
            "Start over", key="header_restart", icon=":material/restart_alt:", width="stretch"
        ):
            _return_to_library()
    st.markdown('<div class="pilot-rule"></div>', unsafe_allow_html=True)


def _render_scenario_library() -> None:
    _render_brand_header()
    st.title("FinanceOS")
    st.markdown('<p class="pilot-product">Finance Director Scenario Coach</p>', unsafe_allow_html=True)
    st.write(
        "Choose a fictional Finance Director decision. Structured financial evidence is evaluated; "
        "unrestricted executive language remains for self-review and qualified human review."
    )
    for scenario in SCENARIOS:
        metadata = scenario.metadata
        st.subheader(scenario.content.title)
        st.write(metadata.short_description)
        details_left, details_right = st.columns(2)
        with details_left:
            st.markdown(f"**Domains:** {', '.join(metadata.primary_domains)}")
            st.markdown(f"**Completion time:** {metadata.completion_time}")
            st.markdown(f"**Difficulty:** {metadata.difficulty}")
        with details_right:
            st.markdown(f"**Source:** {metadata.provenance}")
            st.markdown(f"**Version:** {metadata.version}")
        st.markdown('<div class="scenario-metadata"></div>', unsafe_allow_html=True)
    scenario_ids = [scenario.content.scenario_id for scenario in SCENARIOS]
    selected_id = st.radio(
        "Choose a scenario",
        options=scenario_ids,
        format_func=lambda scenario_id: f"{scenario_id} - {get_scenario(scenario_id).content.title}",
        key="library_scenario_choice",
    )
    st.warning("All scenarios are fictional. Do not enter confidential, personal, or employer information.")
    if st.button(
        "Start scenario", key="start_scenario", type="primary", icon=":material/play_arrow:", width="stretch"
    ):
        reset_session_state(st.session_state)
        st.session_state["selected_scenario_id"] = selected_id
        _set_stage(SCENARIO_STAGE)


def _render_financial_pack_body(body: str) -> None:
    for paragraph in body.split("\n\n"):
        if paragraph.strip():
            st.markdown(paragraph)


def _render_pack_as_expanders(scenario: ScenarioRegistration[object]) -> None:
    for index, section in enumerate(scenario.content.financial_pack):
        with st.expander(section.title, expanded=index == 0):
            _render_financial_pack_body(section.body)


def _render_pack_reference(scenario: ScenarioRegistration[object]) -> None:
    with st.expander("Review the financial pack", expanded=False):
        for section in scenario.content.financial_pack:
            st.markdown(f"**{section.title}**")
            _render_financial_pack_body(section.body)


def _render_scenario() -> None:
    scenario = _active_scenario(st.session_state)
    _render_brand_header(show_restart=True)
    st.caption(f"{scenario.content.scenario_id} / Scenario briefing")
    st.title(scenario.content.title)
    role, context = st.columns(2)
    with role:
        st.subheader("Your role")
        st.write(scenario.content.learner_role)
    with context:
        st.subheader("Company context")
        st.write(scenario.content.company_context)
    st.subheader("CEO question")
    st.info(scenario.content.initial_question)
    st.subheader("Financial pack")
    st.caption("Figures are GBP millions unless the pack states otherwise.")
    _render_pack_as_expanders(scenario)
    st.subheader("Choose your path")
    path = st.segmented_control(
        "Learning path",
        options=["guided", "skip"],
        format_func=lambda value: {"guided": "Guided attempt", "skip": "Skip to solution"}[value],
        selection_mode="single",
        key="path_choice",
    )
    if path == "guided":
        st.caption(f"Complete {scenario.guided_step_count} sections, then submit once for deterministic feedback.")
    elif path == "skip":
        st.caption("Study the reconciliation and coaching content without creating an assessed attempt.")
    if st.button(
        "Continue", key="continue_from_scenario", type="primary", icon=":material/arrow_forward:", width="stretch"
    ):
        if path is None:
            st.error("Choose Guided attempt or Skip to solution before continuing.")
        elif path == "skip":
            st.session_state["path"] = "skip"
            st.session_state["answers"] = None
            st.session_state["report"] = scenario.skipped_report()
            _set_stage(RESULTS_STAGE)
        else:
            st.session_state["path"] = "guided"
            st.session_state["guided_step"] = 0
            _set_stage(GUIDED_STAGE)


def _render_guided() -> None:
    scenario = _active_scenario(st.session_state)
    _render_brand_header(show_restart=True)
    step = int(st.session_state.get("guided_step", 0))
    st.caption(f"Guided attempt / Step {step + 1} of {scenario.guided_step_count}")
    st.progress((step + 1) / scenario.guided_step_count)
    st.title(scenario.content.title)
    _render_pack_reference(scenario)
    scenario.render_guided_step(
        step,
        GuidedScenarioContext(
            state=st.session_state,
            submit_attempt=lambda answers: _submit_active_scenario(scenario, answers),
        ),
    )


def _source_label(value: str) -> str:
    return {
        "deterministic": "Deterministic",
        "self-review": "Self-review",
        "manual-review": "Manual review",
        "not-assessed": "Not assessed",
    }.get(value, value)


def _render_scorecard(report: EvaluationReport) -> None:
    st.subheader("Qualitative competency scorecard")
    rows = [
        {
            "Competency": result.competency.value,
            "Rating": result.rating.value,
            "Assessment source": _source_label(result.assessment_source.value),
        }
        for result in report.scorecard.results
    ]
    st.table(rows)
    for result in report.scorecard.results:
        with st.expander(f"{result.competency.value}: {result.rating.value}"):
            st.caption(f"Assessment source: {_source_label(result.assessment_source.value)}")
            st.markdown(f"**Evidence used:** {', '.join(result.evidence_used) if result.evidence_used else 'None'}")
            st.markdown(f"**Why:** {result.explanation}")
            st.markdown(f"**Next practice:** {result.improvement_guidance}")
            if result.limitation:
                st.warning(result.limitation)


def _render_evidence(report: EvaluationReport, scenario: ScenarioRegistration[object]) -> None:
    st.subheader("Deterministic evidence feedback")
    st.caption("Evidence IDs are shown for traceability. No overall score is calculated.")
    for record in report.evidence_records:
        title = scenario.evidence_titles.get(record.evidence_id, "Evidence")
        with st.expander(f"{title}: {record.result.value}"):
            st.caption(record.evidence_id)
            st.markdown(f"**Rule:** {record.expected_rule}")
            st.markdown(f"**Your evidence:** {record.learner_input}")
            st.markdown(f"**Why:** {record.feedback}")
            st.markdown(f"**Next practice:** {record.improvement_guidance}")
            if record.worked_solution is not None:
                with st.popover("How was this calculated?", type="tertiary", icon=":material/calculate:"):
                    st.markdown(record.worked_solution)
            if record.judgment_explanation is not None:
                with st.popover("Why does this matter?", type="tertiary", icon=":material/lightbulb:"):
                    st.markdown(record.judgment_explanation)


def _render_learning_content(scenario: ScenarioRegistration[object]) -> None:
    st.subheader("Learning review")
    with st.expander("Model Finance Director answer", expanded=False):
        st.write(scenario.content.model_answer)
    with st.expander("Full debrief", expanded=False):
        st.write(scenario.content.debrief)
    with st.expander("Self-review checklist", expanded=True):
        st.caption("Source: self-review")
        for item in scenario.content.self_review_checklist:
            st.markdown(f"- {item}")
    with st.expander("Learner action plan", expanded=True):
        for index, item in enumerate(scenario.content.action_plan, start=1):
            st.markdown(f"{index}. {item}")


def _render_results() -> None:
    scenario = _active_scenario(st.session_state)
    _render_brand_header(show_restart=True)
    report = st.session_state.get("report")
    if not isinstance(report, EvaluationReport):
        st.error("No completed attempt is available. Start over to choose a scenario.")
        return
    answers = st.session_state.get("answers")
    typed_answers = answers if answers is not None else None
    is_skip = st.session_state.get("path") == "skip"
    st.caption(f"{scenario.content.scenario_id} / {'Study path' if is_skip else 'Guided results'}")
    st.title("Scenario results")
    if is_skip:
        st.info("No assessed learner evidence was collected. Every competency is Not assessed.")
        st.subheader("Complete financial reconciliation")
        st.write(scenario.content.reconciliation_summary)
    else:
        st.success(f"Recommendation submitted: {scenario.recommendation_label(typed_answers)}")
        st.caption("This result evaluates structured financial evidence. It does not automatically assess the quality of unrestricted executive language.")
        _render_evidence(report, scenario)
        if report.critical_omissions:
            st.subheader("Critical omissions")
            for omission in report.critical_omissions:
                st.warning(f"{omission}: {scenario.critical_omission_labels.get(omission, 'Review this issue.')}")
    _render_scorecard(report)
    ceo_response = scenario.ceo_response(typed_answers)
    if not is_skip and ceo_response:
        st.subheader("Your CEO response")
        st.caption("Not automatically scored")
        st.write(ceo_response)
    _render_learning_content(scenario)
    st.subheader("Pilot summary")
    st.download_button(
        "Download plain-text summary",
        data=build_pilot_summary(report, typed_answers, scenario),
        file_name=f"financeos-{scenario.content.scenario_id.lower()}-pilot-summary.txt",
        mime="text/plain",
        icon=":material/download:",
        width="stretch",
    )
    st.caption("The summary is generated locally for this session and is not stored by FinanceOS.")
    if st.button("Start over", key="results_restart", icon=":material/restart_alt:", width="stretch"):
        _return_to_library()


def run_app() -> None:
    """Render the Streamlit application for the current in-memory session."""

    st.set_page_config(
        page_title="FinanceOS | Finance Director Scenario Coach",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(APP_CSS, unsafe_allow_html=True)
    initialize_session_state(st.session_state)
    stage = st.session_state["stage"]
    renderers: dict[str, Callable[[], None]] = {
        WELCOME_STAGE: _render_scenario_library,
        SCENARIO_STAGE: _render_scenario,
        GUIDED_STAGE: _render_guided,
        RESULTS_STAGE: _render_results,
    }
    renderers.get(stage, _render_scenario_library)()
