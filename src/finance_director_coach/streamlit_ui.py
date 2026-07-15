"""Streamlit presentation layer for the FinanceOS Alpha 0.1 pilot."""

from __future__ import annotations

from collections.abc import Callable, Mapping, MutableMapping

import streamlit as st

from finance_director_coach.evaluation import evaluate_attempt, skipped_evaluation_report
from finance_director_coach.models import EvaluationReport, LearnerAnswers, RecommendationRoute
from finance_director_coach.scenarios.scenario_001 import (
    CASH_DRIVER_OPTIONS,
    HIRING_UNIT_WARNING,
    MISSING_INFORMATION_OPTIONS,
    MONETARY_INPUT_GUIDANCE,
    RECOMMENDATION_OPTIONS,
    RISK_OPTIONS,
    ROUTE_SAFEGUARD_OPTIONS,
    SCENARIO_001,
    THRESHOLD_OPTIONS,
    TRADEOFF_OPTIONS,
)

WELCOME_STAGE = "welcome"
SCENARIO_STAGE = "scenario"
GUIDED_STAGE = "guided"
RESULTS_STAGE = "results"
GUIDED_STEP_COUNT = 4
PRACTICE_STATE_PREFIX = "practice_"

EVIDENCE_TITLES: dict[str, str] = {
    "E-001": "Growth calculations",
    "E-002": "Cash movement",
    "E-003": "EBITDA-to-cash reconciliation",
    "E-004": "Working-capital drivers",
    "E-005": "Largest cash driver",
    "E-006": "Hiring cost",
    "E-007": "Liquidity forecast",
    "E-008": "Cash thresholds",
    "E-009": "Recommendation",
    "E-010": "Route safeguards",
    "E-011": "Missing information",
    "E-012": "Analysis completion",
    "E-013": "Commercial tradeoffs",
    "E-014": "Core risks",
    "E-015": "Extended risks",
}

CRITICAL_OMISSION_LABELS: dict[str, str] = {
    "CO-001": "The response did not reconcile EBITDA growth with working-capital cash pressure.",
    "CO-002": "A material cash, hiring, liquidity, or threshold calculation was misstated.",
    "CO-003": "No recommendation route was provided.",
    "CO-004": "The approval route did not adequately address the board-floor exposure.",
    "CO-005": "The response treated the lender minimum as already breached.",
    "CO-006": "Unsupported collections or hiring benefits were treated as certain.",
}

APP_CSS = """
<style>
    :root {
        --finance-ink: #172121;
        --finance-muted: #52605f;
        --finance-line: #d8dfdc;
        --finance-teal: #0f766e;
        --finance-burgundy: #8b3345;
        --finance-green: #2f6b4f;
    }
    .stApp { color: var(--finance-ink); }
    .block-container {
        max-width: 1080px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }
    h1, h2, h3, p, label, button { letter-spacing: 0 !important; }
    h1 { font-size: 2.45rem !important; line-height: 1.12 !important; }
    h2 { font-size: 1.55rem !important; line-height: 1.25 !important; }
    h3 { font-size: 1.1rem !important; line-height: 1.35 !important; }
    .pilot-kicker {
        color: var(--finance-teal);
        font-size: 0.78rem;
        font-weight: 700;
        margin: 0 0 0.45rem 0;
        text-transform: uppercase;
    }
    .pilot-product {
        color: var(--finance-muted);
        font-size: 1.08rem;
        margin: -0.7rem 0 1.5rem 0;
    }
    .pilot-rule {
        border-top: 1px solid var(--finance-line);
        margin: 1rem 0 1.5rem 0;
    }
    div[data-testid="stExpander"] {
        border-color: var(--finance-line);
        border-radius: 6px;
    }
    div[data-testid="stCode"] pre {
        background: #f1f4f2;
        border: 1px solid var(--finance-line);
        border-radius: 4px;
        color: var(--finance-ink);
        font-size: 0.84rem;
    }
    div[data-testid="stAlert"] { border-radius: 6px; }
    div[data-testid="stButton"] button,
    div[data-testid="stDownloadButton"] button {
        border-radius: 6px;
        min-height: 2.65rem;
    }
    .threshold-note {
        border-left: 4px solid var(--finance-burgundy);
        color: var(--finance-ink);
        margin: 0.4rem 0 1.2rem 0;
        padding: 0.25rem 0 0.25rem 0.85rem;
    }
    @media (max-width: 640px) {
        .block-container { padding: 1.2rem 1rem 3rem 1rem; }
        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.35rem !important; }
        div[data-testid="stCode"] pre { font-size: 0.76rem; }
    }
</style>
"""


def initialize_session_state(state: MutableMapping[str, object]) -> None:
    """Initialize only the in-memory state required by the pilot."""

    state.setdefault("stage", WELCOME_STAGE)
    state.setdefault("guided_step", 0)
    state.setdefault("path", None)
    state.setdefault("answers", None)
    state.setdefault("report", None)


def reset_session_state(state: MutableMapping[str, object]) -> None:
    """Clear Scenario Coach state while preserving the Practice-owned namespace."""

    for key in list(state):
        if not key.startswith(PRACTICE_STATE_PREFIX):
            del state[key]
    initialize_session_state(state)


def learner_financial_pack_text() -> str:
    """Return the exact learner-facing pack sourced from Scenario 001."""

    return "\n\n".join(
        f"{section.title}\n{section.body}" for section in SCENARIO_001.financial_pack
    )


def evaluate_guided_submission(answers: LearnerAnswers) -> EvaluationReport:
    """Delegate a completed browser attempt to the core evaluator."""

    return evaluate_attempt(answers)


def _saved_key(widget_key: str) -> str:
    return f"saved_{widget_key}"


def _state_value(state: Mapping[str, object], key: str) -> object | None:
    if key in state:
        return state[key]
    return state.get(_saved_key(key))


def _save_step_values(values: Mapping[str, object]) -> None:
    for key, value in values.items():
        st.session_state[_saved_key(key)] = value


def build_pilot_summary(
    report: EvaluationReport,
    answers: LearnerAnswers | None,
) -> str:
    """Create a local plain-text learner summary without solution content."""

    recommendation = (
        answers.recommendation.label
        if answers is not None and answers.recommendation is not None
        else "Not submitted"
    )
    lines = [
        "FinanceOS Alpha 0.1 - Pilot summary",
        f"Scenario ID: {SCENARIO_001.scenario_id}",
        f"Recommendation route: {recommendation}",
        "",
        "Evidence results",
    ]
    if report.evidence_records:
        lines.extend(
            f"- {record.evidence_id}: {record.result.value}"
            for record in report.evidence_records
        )
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
    lines.append(answers.ceo_response if answers is not None else "Not submitted")
    lines.extend(["", "Self-review questions"])
    lines.extend(f"- {item}" for item in SCENARIO_001.self_review_checklist)
    lines.extend(
        [
            "",
            "This summary was generated locally and is not stored by FinanceOS.",
            "The CEO response was not automatically scored.",
        ]
    )
    return "\n".join(lines)


def _number_from_state(state: Mapping[str, object], key: str) -> float:
    value = _state_value(state, key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Missing numeric input: {key}")
    return float(value)


def _strings_from_state(state: Mapping[str, object], key: str) -> frozenset[str]:
    value = _state_value(state, key)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"Missing selection input: {key}")
    return frozenset(value)


def build_answers_from_state(state: Mapping[str, object]) -> LearnerAnswers:
    """Translate validated widget state into the existing attempt model."""

    route_value = _state_value(state, "input_recommendation")
    if not isinstance(route_value, str):
        raise ValueError("Missing recommendation route")
    recommendation = RecommendationRoute(route_value)
    response = _state_value(state, "input_ceo_response")
    if not isinstance(response, str):
        raise ValueError("Missing CEO response")

    return LearnerAnswers(
        revenue_growth_percent=_number_from_state(state, "input_revenue_growth"),
        ebitda_growth_percent=_number_from_state(state, "input_ebitda_growth"),
        cash_decrease=_number_from_state(state, "input_cash_decrease"),
        operating_cash_before_interest_tax=_number_from_state(state, "input_operating_cash"),
        net_operating_cash=_number_from_state(state, "input_net_operating_cash"),
        cash_drivers=_strings_from_state(state, "input_cash_drivers"),
        largest_cash_driver=str(_state_value(state, "input_largest_driver")),
        risks=_strings_from_state(state, "input_risks"),
        h2_hiring_cost=_number_from_state(state, "input_h2_hiring_cost"),
        annual_hiring_cost=_number_from_state(state, "input_annual_hiring_cost"),
        cash_low_point=_number_from_state(state, "input_cash_low_point"),
        december_cash=_number_from_state(state, "input_december_cash"),
        board_floor_shortfall=_number_from_state(state, "input_board_shortfall"),
        lender_headroom=_number_from_state(state, "input_lender_headroom"),
        threshold_interpretations=_strings_from_state(state, "input_thresholds"),
        recommendation=recommendation,
        safeguards=_strings_from_state(state, f"input_safeguards_{recommendation.value}"),
        missing_information=_strings_from_state(state, "input_missing_information"),
        tradeoffs=_strings_from_state(state, "input_tradeoffs"),
        ceo_response=response.strip(),
    )


def _set_stage(stage: str) -> None:
    st.session_state["stage"] = stage
    st.rerun()


def _render_brand_header(show_restart: bool = False) -> None:
    left, right = st.columns([5, 1])
    with left:
        st.markdown('<p class="pilot-kicker">FinanceOS / Alpha 0.1</p>', unsafe_allow_html=True)
    with right:
        if show_restart and st.button(
            "Start over",
            key="header_restart",
            icon=":material/restart_alt:",
            width="stretch",
        ):
            reset_session_state(st.session_state)
            st.rerun()
    st.markdown('<div class="pilot-rule"></div>', unsafe_allow_html=True)


def _render_welcome() -> None:
    _render_brand_header()
    st.title("FinanceOS")
    st.markdown('<p class="pilot-product">Finance Director Scenario Coach</p>', unsafe_allow_html=True)
    st.subheader(SCENARIO_001.title)
    st.write(
        "This early pilot lets you work through a realistic Finance Director decision, "
        "receive transparent feedback on structured financial evidence, and compare your "
        "recommendation with a model response."
    )
    col_time, col_scope = st.columns(2)
    with col_time:
        st.markdown("**Expected time**")
        st.write("About 20 minutes")
    with col_scope:
        st.markdown("**Pilot boundary**")
        st.write("Structured financial evidence is evaluated; unrestricted executive language is not.")
    st.warning(
        "This scenario is fictional. Do not enter confidential, personal, or employer information."
    )
    if st.button(
        "Start scenario",
        key="start_scenario",
        type="primary",
        icon=":material/play_arrow:",
        width="stretch",
    ):
        _set_stage(SCENARIO_STAGE)


def _render_pack_as_expanders() -> None:
    for index, section in enumerate(SCENARIO_001.financial_pack):
        with st.expander(section.title, expanded=index == 0):
            st.code(section.body, language=None, wrap_lines=False)


def _render_pack_reference() -> None:
    with st.expander("Review the financial pack", expanded=False):
        for section in SCENARIO_001.financial_pack:
            st.markdown(f"**{section.title}**")
            st.code(section.body, language=None, wrap_lines=False)


def _render_scenario() -> None:
    _render_brand_header(show_restart=True)
    st.caption(f"{SCENARIO_001.scenario_id} / Scenario briefing")
    st.title(SCENARIO_001.title)
    role, context = st.columns(2)
    with role:
        st.subheader("Your role")
        st.write(SCENARIO_001.learner_role)
    with context:
        st.subheader("Company context")
        st.write(SCENARIO_001.company_context)

    st.subheader("CEO question")
    st.info(SCENARIO_001.initial_question)
    st.subheader("Financial pack")
    st.caption("Figures are GBP millions unless the pack states otherwise.")
    _render_pack_as_expanders()

    st.subheader("Choose your path")
    path = st.segmented_control(
        "Learning path",
        options=["guided", "skip"],
        format_func=lambda value: {
            "guided": "Guided attempt",
            "skip": "Skip to solution",
        }[value],
        selection_mode="single",
        key="path_choice",
    )
    if path == "guided":
        st.caption("Complete four sections, then submit once for deterministic feedback.")
    elif path == "skip":
        st.caption("Study the reconciliation and coaching content without creating an assessed attempt.")

    if st.button(
        "Continue",
        key="continue_from_scenario",
        type="primary",
        icon=":material/arrow_forward:",
        width="stretch",
    ):
        if path is None:
            st.error("Choose Guided attempt or Skip to solution before continuing.")
        elif path == "skip":
            st.session_state["path"] = "skip"
            st.session_state["answers"] = None
            st.session_state["report"] = skipped_evaluation_report()
            _set_stage(RESULTS_STAGE)
        else:
            st.session_state["path"] = "guided"
            st.session_state["guided_step"] = 0
            _set_stage(GUIDED_STAGE)


def _number_input(label: str, key: str, help_text: str | None = None) -> float | None:
    saved_value = _state_value(st.session_state, key)
    default_value = (
        float(saved_value)
        if isinstance(saved_value, (int, float)) and not isinstance(saved_value, bool)
        else None
    )
    value = st.number_input(
        label,
        value=default_value,
        step=0.01,
        format="%.2f",
        placeholder="Enter a value",
        help=help_text,
        key=key,
    )
    return float(value) if value is not None else None


def _back_button(step: int) -> None:
    if step <= 0:
        return
    if st.button(
        "Back",
        key=f"back_from_step_{step}",
        icon=":material/arrow_back:",
    ):
        _save_step_values(
            {
                key: value
                for key, value in st.session_state.items()
                if key.startswith("input_")
            }
        )
        st.session_state["guided_step"] = step - 1
        st.rerun()


def _render_monetary_input_guidance(*, hiring_warning: bool = False) -> None:
    st.info(MONETARY_INPUT_GUIDANCE)
    if hiring_warning:
        st.warning(HIRING_UNIT_WARNING)


def _render_financial_analysis_step() -> None:
    st.subheader("Growth and cash conversion")
    st.write("Enter growth answers as percentage points.")
    _render_monetary_input_guidance()
    with st.form("financial_analysis_form"):
        growth_left, growth_right = st.columns(2)
        with growth_left:
            revenue_growth = _number_input(
                "Revenue growth (%)",
                "input_revenue_growth",
                "Calculate (current period - prior period) / prior period x 100.",
            )
        with growth_right:
            ebitda_growth = _number_input(
                "EBITDA growth (%)",
                "input_ebitda_growth",
                "Calculate (current period - prior period) / prior period x 100.",
            )
        cash_decrease = _number_input(
            "Cash decrease (positive GBP m amount)",
            "input_cash_decrease",
        )
        operating_cash = _number_input(
            "Operating cash before interest and tax (GBP m)",
            "input_operating_cash",
            "Use a minus sign for negative cash flow.",
        )
        net_operating_cash = _number_input(
            "Net operating cash after interest and tax (GBP m)",
            "input_net_operating_cash",
            "Use a minus sign for negative cash flow.",
        )
        submitted = st.form_submit_button(
            "Save and continue",
            type="primary",
            icon=":material/arrow_forward:",
            width="stretch",
        )
    if submitted:
        if any(
            value is None
            for value in (
                revenue_growth,
                ebitda_growth,
                cash_decrease,
                operating_cash,
                net_operating_cash,
            )
        ):
            st.error("Complete all five calculations before continuing.")
        else:
            _save_step_values(
                {
                    "input_revenue_growth": revenue_growth,
                    "input_ebitda_growth": ebitda_growth,
                    "input_cash_decrease": cash_decrease,
                    "input_operating_cash": operating_cash,
                    "input_net_operating_cash": net_operating_cash,
                }
            )
            st.session_state["guided_step"] = 1
            st.rerun()


def _render_drivers_and_risks_step() -> None:
    _back_button(1)
    st.subheader("Working capital and risk")
    st.caption("For multiple-selection questions, choose every option supported by the pack.")
    with st.form("drivers_and_risks_form"):
        cash_drivers = st.multiselect(
            "Movements in the working-capital explanation",
            options=list(CASH_DRIVER_OPTIONS),
            format_func=CASH_DRIVER_OPTIONS.__getitem__,
            default=_state_value(st.session_state, "input_cash_drivers") or (),
            key="input_cash_drivers",
        )
        largest_driver_options = [
            "receivables",
            "inventory",
            "contract_assets",
            "capital_expenditure",
        ]
        saved_largest_driver = _state_value(st.session_state, "input_largest_driver")
        largest_driver = st.selectbox(
            "Largest cash-use movement",
            options=largest_driver_options,
            format_func={
                "receivables": "Trade receivables",
                "inventory": "Inventory",
                "contract_assets": "Contract assets and prepayments",
                "capital_expenditure": "Capital expenditure",
            }.__getitem__,
            index=(
                largest_driver_options.index(saved_largest_driver)
                if saved_largest_driver in largest_driver_options
                else None
            ),
            placeholder="Select one",
            key="input_largest_driver",
        )
        risks = st.multiselect(
            "Material risks supported by the pack",
            options=list(RISK_OPTIONS),
            format_func=RISK_OPTIONS.__getitem__,
            default=_state_value(st.session_state, "input_risks") or (),
            key="input_risks",
        )
        submitted = st.form_submit_button(
            "Save and continue",
            type="primary",
            icon=":material/arrow_forward:",
            width="stretch",
        )
    if submitted:
        if not cash_drivers or largest_driver is None or not risks:
            st.error("Select at least one driver and risk, and identify the largest cash-use movement.")
        else:
            _save_step_values(
                {
                    "input_cash_drivers": list(cash_drivers),
                    "input_largest_driver": largest_driver,
                    "input_risks": list(risks),
                }
            )
            st.session_state["guided_step"] = 2
            st.rerun()


def _render_hiring_and_liquidity_step() -> None:
    _back_button(2)
    st.subheader("Hiring and liquidity")
    _render_monetary_input_guidance(hiring_warning=True)
    st.markdown(
        '<div class="threshold-note"><strong>Keep the thresholds separate:</strong> '
        "the board floor is an internal limit; the lender minimum is a covenant.</div>",
        unsafe_allow_html=True,
    )
    with st.form("hiring_and_liquidity_form"):
        cost_left, cost_right = st.columns(2)
        with cost_left:
            h2_cost = _number_input("H2 2026 hiring cost (GBP m)", "input_h2_hiring_cost")
        with cost_right:
            annual_cost = _number_input(
                "Annual recurring hiring cost (GBP m)",
                "input_annual_hiring_cost",
            )
        cash_left, cash_right = st.columns(2)
        with cash_left:
            low_point = _number_input(
                "Hiring-case cash low point (GBP m)",
                "input_cash_low_point",
            )
        with cash_right:
            december_cash = _number_input(
                "Hiring-case December cash (GBP m)",
                "input_december_cash",
            )
        threshold_left, threshold_right = st.columns(2)
        with threshold_left:
            board_shortfall = _number_input(
                "Shortfall below the board cash floor (GBP m)",
                "input_board_shortfall",
            )
        with threshold_right:
            lender_headroom = _number_input(
                "Headroom above the lender minimum at the low point (GBP m)",
                "input_lender_headroom",
            )
        thresholds = st.multiselect(
            "Threshold interpretation",
            options=list(THRESHOLD_OPTIONS),
            format_func=THRESHOLD_OPTIONS.__getitem__,
            default=_state_value(st.session_state, "input_thresholds") or (),
            key="input_thresholds",
        )
        submitted = st.form_submit_button(
            "Save and continue",
            type="primary",
            icon=":material/arrow_forward:",
            width="stretch",
        )
    if submitted:
        if any(
            value is None
            for value in (
                h2_cost,
                annual_cost,
                low_point,
                december_cash,
                board_shortfall,
                lender_headroom,
            )
        ) or not thresholds:
            st.error("Complete every hiring and liquidity calculation and select threshold statements.")
        else:
            _save_step_values(
                {
                    "input_h2_hiring_cost": h2_cost,
                    "input_annual_hiring_cost": annual_cost,
                    "input_cash_low_point": low_point,
                    "input_december_cash": december_cash,
                    "input_board_shortfall": board_shortfall,
                    "input_lender_headroom": lender_headroom,
                    "input_thresholds": list(thresholds),
                }
            )
            st.session_state["guided_step"] = 3
            st.rerun()


def _render_decision_step() -> None:
    _back_button(3)
    st.subheader("Recommendation and actions")
    recommendation_options = list(RECOMMENDATION_OPTIONS)
    saved_recommendation = _state_value(st.session_state, "input_recommendation")
    recommendation_value = st.selectbox(
        "Recommendation route",
        options=recommendation_options,
        format_func=RECOMMENDATION_OPTIONS.__getitem__,
        index=(
            recommendation_options.index(saved_recommendation)
            if saved_recommendation in recommendation_options
            else None
        ),
        placeholder="Select one",
        key="input_recommendation",
    )
    if recommendation_value is None:
        st.info("Select a recommendation route to see the relevant safeguard options.")
        return

    recommendation = RecommendationRoute(recommendation_value)
    safeguards_key = f"input_safeguards_{recommendation.value}"
    with st.form("decision_form"):
        safeguards = st.multiselect(
            f"Safeguards for {recommendation.label}",
            options=list(ROUTE_SAFEGUARD_OPTIONS[recommendation]),
            format_func=ROUTE_SAFEGUARD_OPTIONS[recommendation].__getitem__,
            default=_state_value(st.session_state, safeguards_key) or (),
            key=safeguards_key,
        )
        missing_information = st.multiselect(
            "Information that would materially improve the decision",
            options=list(MISSING_INFORMATION_OPTIONS),
            format_func=MISSING_INFORMATION_OPTIONS.__getitem__,
            default=_state_value(st.session_state, "input_missing_information") or (),
            key="input_missing_information",
        )
        tradeoffs = st.multiselect(
            "Commercial tradeoffs and capacity alternatives",
            options=list(TRADEOFF_OPTIONS),
            format_func=TRADEOFF_OPTIONS.__getitem__,
            default=_state_value(st.session_state, "input_tradeoffs") or (),
            key="input_tradeoffs",
        )
        st.caption(
            "Your wording is retained for comparison and self-review. It is not scored for keywords, "
            "length, grammar, sentiment, or communication quality."
        )
        ceo_response = st.text_area(
            "Concise recommendation to the CEO",
            height=150,
            placeholder="State your decision, finance case, risks, conditions, and next actions.",
            key="input_ceo_response",
        )
        submitted = st.form_submit_button(
            "Submit guided attempt",
            type="primary",
            icon=":material/check_circle:",
            width="stretch",
        )
    if submitted:
        if not safeguards or not missing_information or not tradeoffs or not ceo_response.strip():
            st.error(
                "Select safeguards, missing information, and tradeoffs, then provide your CEO response."
            )
            return
        _save_step_values(
            {
                "input_recommendation": recommendation_value,
                safeguards_key: list(safeguards),
                "input_missing_information": list(missing_information),
                "input_tradeoffs": list(tradeoffs),
                "input_ceo_response": ceo_response,
            }
        )
        answers = build_answers_from_state(st.session_state)
        st.session_state["answers"] = answers
        st.session_state["report"] = evaluate_guided_submission(answers)
        _set_stage(RESULTS_STAGE)


def _render_guided() -> None:
    _render_brand_header(show_restart=True)
    step = int(st.session_state.get("guided_step", 0))
    st.caption(f"Guided attempt / Step {step + 1} of {GUIDED_STEP_COUNT}")
    st.progress((step + 1) / GUIDED_STEP_COUNT)
    st.title(SCENARIO_001.title)
    _render_pack_reference()
    if step == 0:
        _render_financial_analysis_step()
    elif step == 1:
        _render_drivers_and_risks_step()
    elif step == 2:
        _render_hiring_and_liquidity_step()
    else:
        _render_decision_step()


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
            evidence = ", ".join(result.evidence_used) if result.evidence_used else "None"
            st.markdown(f"**Evidence used:** {evidence}")
            st.markdown(f"**Why:** {result.explanation}")
            st.markdown(f"**Next practice:** {result.improvement_guidance}")
            if result.limitation:
                st.warning(result.limitation)


def _render_evidence(report: EvaluationReport) -> None:
    st.subheader("Deterministic evidence feedback")
    st.caption("Evidence IDs are shown for traceability. No overall score is calculated.")
    for record in report.evidence_records:
        title = EVIDENCE_TITLES.get(record.evidence_id, "Evidence")
        with st.expander(f"{title}: {record.result.value}"):
            st.caption(record.evidence_id)
            st.markdown(f"**Rule:** {record.expected_rule}")
            st.markdown(f"**Your evidence:** {record.learner_input}")
            st.markdown(f"**Why:** {record.feedback}")
            st.markdown(f"**Next practice:** {record.improvement_guidance}")
            if record.worked_solution is not None:
                with st.popover(
                    "How was this calculated?",
                    type="tertiary",
                    icon=":material/calculate:",
                ):
                    st.markdown(record.worked_solution)


def _render_learning_content() -> None:
    st.subheader("Learning review")
    with st.expander("Model Finance Director answer", expanded=False):
        st.write(SCENARIO_001.model_answer)
    with st.expander("Full debrief", expanded=False):
        st.write(SCENARIO_001.debrief)
    with st.expander("Self-review checklist", expanded=True):
        st.caption("Source: self-review")
        for item in SCENARIO_001.self_review_checklist:
            st.markdown(f"- {item}")
    with st.expander("Learner action plan", expanded=True):
        for index, item in enumerate(SCENARIO_001.action_plan, start=1):
            st.markdown(f"{index}. {item}")


def _render_results() -> None:
    _render_brand_header(show_restart=True)
    report = st.session_state.get("report")
    if not isinstance(report, EvaluationReport):
        st.error("No completed attempt is available. Start over to begin the scenario.")
        return
    answers = st.session_state.get("answers")
    typed_answers = answers if isinstance(answers, LearnerAnswers) else None
    is_skip = st.session_state.get("path") == "skip"

    st.caption(f"{SCENARIO_001.scenario_id} / {'Study path' if is_skip else 'Guided results'}")
    st.title("Scenario results")
    if is_skip:
        st.info("No assessed learner evidence was collected. Every competency is Not assessed.")
        st.subheader("Complete financial reconciliation")
        st.write(SCENARIO_001.reconciliation_summary)
    else:
        recommendation = (
            typed_answers.recommendation.label
            if typed_answers is not None and typed_answers.recommendation is not None
            else "Not submitted"
        )
        st.success(f"Recommendation submitted: {recommendation}")
        st.caption(
            "This result evaluates structured financial evidence. It does not automatically assess "
            "the quality of unrestricted executive language."
        )
        _render_evidence(report)
        if report.critical_omissions:
            st.subheader("Critical omissions")
            for omission in report.critical_omissions:
                st.warning(f"{omission}: {CRITICAL_OMISSION_LABELS.get(omission, 'Review this issue.')}")

    _render_scorecard(report)
    if not is_skip and typed_answers is not None:
        st.subheader("Your CEO response")
        st.caption("Not automatically scored")
        st.write(typed_answers.ceo_response)
    _render_learning_content()

    st.subheader("Pilot summary")
    st.download_button(
        "Download plain-text summary",
        data=build_pilot_summary(report, typed_answers),
        file_name=f"financeos-{SCENARIO_001.scenario_id.lower()}-pilot-summary.txt",
        mime="text/plain",
        icon=":material/download:",
        width="stretch",
    )
    st.caption("The summary is generated locally for this session and is not stored by FinanceOS.")
    if st.button(
        "Start over",
        key="results_restart",
        icon=":material/restart_alt:",
        width="stretch",
    ):
        reset_session_state(st.session_state)
        st.rerun()


def run_app() -> None:
    """Render the Streamlit application for the current session state."""

    st.markdown(APP_CSS, unsafe_allow_html=True)
    initialize_session_state(st.session_state)
    stage = st.session_state["stage"]
    renderers: dict[str, Callable[[], None]] = {
        WELCOME_STAGE: _render_welcome,
        SCENARIO_STAGE: _render_scenario,
        GUIDED_STAGE: _render_guided,
        RESULTS_STAGE: _render_results,
    }
    renderers.get(stage, _render_welcome)()
