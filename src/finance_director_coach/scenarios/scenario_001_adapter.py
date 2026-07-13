"""Scenario 001 answer translation and Streamlit guided-question flow."""

from __future__ import annotations

from collections.abc import Mapping

import streamlit as st

from finance_director_coach.models import LearnerAnswers, RecommendationRoute
from finance_director_coach.scenarios.contracts import GuidedScenarioContext
from finance_director_coach.scenarios.scenario_001 import (
    CASH_DRIVER_OPTIONS,
    HIRING_UNIT_WARNING,
    MISSING_INFORMATION_OPTIONS,
    MONETARY_INPUT_GUIDANCE,
    RECOMMENDATION_OPTIONS,
    RISK_OPTIONS,
    ROUTE_SAFEGUARD_OPTIONS,
    THRESHOLD_OPTIONS,
    TRADEOFF_OPTIONS,
)
from finance_director_coach.scenarios.ui_helpers import (
    number_input,
    render_back_button,
    save_step_values,
    state_value,
)


def _number_from_state(state: Mapping[str, object], key: str) -> float:
    value = state_value(state, key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Missing numeric input: {key}")
    return float(value)


def _strings_from_state(state: Mapping[str, object], key: str) -> frozenset[str]:
    value = state_value(state, key)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"Missing selection input: {key}")
    return frozenset(value)


def build_scenario_001_answers(state: Mapping[str, object]) -> LearnerAnswers:
    """Translate validated Scenario 001 widget state into its typed attempt model."""

    route_value = state_value(state, "input_recommendation")
    if not isinstance(route_value, str):
        raise ValueError("Missing recommendation route")
    recommendation = RecommendationRoute(route_value)
    response = state_value(state, "input_ceo_response")
    if not isinstance(response, str):
        raise ValueError("Missing CEO response")

    return LearnerAnswers(
        revenue_growth_percent=_number_from_state(state, "input_revenue_growth"),
        ebitda_growth_percent=_number_from_state(state, "input_ebitda_growth"),
        cash_decrease=_number_from_state(state, "input_cash_decrease"),
        operating_cash_before_interest_tax=_number_from_state(state, "input_operating_cash"),
        net_operating_cash=_number_from_state(state, "input_net_operating_cash"),
        cash_drivers=_strings_from_state(state, "input_cash_drivers"),
        largest_cash_driver=str(state_value(state, "input_largest_driver")),
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


def _render_financial_analysis(context: GuidedScenarioContext) -> None:
    state = context.state
    st.subheader("Growth and cash conversion")
    st.write("Enter growth answers as percentage points.")
    st.info(MONETARY_INPUT_GUIDANCE)
    with st.form("financial_analysis_form"):
        growth_left, growth_right = st.columns(2)
        with growth_left:
            revenue_growth = number_input(
                state,
                "Revenue growth (%)",
                "input_revenue_growth",
                "Calculate (current period - prior period) / prior period x 100.",
            )
        with growth_right:
            ebitda_growth = number_input(
                state,
                "EBITDA growth (%)",
                "input_ebitda_growth",
                "Calculate (current period - prior period) / prior period x 100.",
            )
        cash_decrease = number_input(state, "Cash decrease (positive GBP m amount)", "input_cash_decrease")
        operating_cash = number_input(
            state,
            "Operating cash before interest and tax (GBP m)",
            "input_operating_cash",
            "Use a minus sign for negative cash flow.",
        )
        net_operating_cash = number_input(
            state,
            "Net operating cash after interest and tax (GBP m)",
            "input_net_operating_cash",
            "Use a minus sign for negative cash flow.",
        )
        submitted = st.form_submit_button(
            "Save and continue", type="primary", icon=":material/arrow_forward:", width="stretch"
        )
    if submitted:
        if any(value is None for value in (revenue_growth, ebitda_growth, cash_decrease, operating_cash, net_operating_cash)):
            st.error("Complete all five calculations before continuing.")
            return
        save_step_values(
            state,
            {
                "input_revenue_growth": revenue_growth,
                "input_ebitda_growth": ebitda_growth,
                "input_cash_decrease": cash_decrease,
                "input_operating_cash": operating_cash,
                "input_net_operating_cash": net_operating_cash,
            },
        )
        state["guided_step"] = 1
        st.rerun()


def _render_drivers_and_risks(context: GuidedScenarioContext) -> None:
    state = context.state
    render_back_button(state, 1)
    st.subheader("Working capital and risk")
    st.caption("For multiple-selection questions, choose every option supported by the pack.")
    with st.form("drivers_and_risks_form"):
        cash_drivers = st.multiselect(
            "Movements in the working-capital explanation",
            options=list(CASH_DRIVER_OPTIONS),
            format_func=CASH_DRIVER_OPTIONS.__getitem__,
            default=state_value(state, "input_cash_drivers") or (),
            key="input_cash_drivers",
        )
        largest_driver_options = ["receivables", "inventory", "contract_assets", "capital_expenditure"]
        saved_largest_driver = state_value(state, "input_largest_driver")
        largest_driver = st.selectbox(
            "Largest cash-use movement",
            options=largest_driver_options,
            format_func={
                "receivables": "Trade receivables",
                "inventory": "Inventory",
                "contract_assets": "Contract assets and prepayments",
                "capital_expenditure": "Capital expenditure",
            }.__getitem__,
            index=(largest_driver_options.index(saved_largest_driver) if saved_largest_driver in largest_driver_options else None),
            placeholder="Select one",
            key="input_largest_driver",
        )
        risks = st.multiselect(
            "Material risks supported by the pack",
            options=list(RISK_OPTIONS),
            format_func=RISK_OPTIONS.__getitem__,
            default=state_value(state, "input_risks") or (),
            key="input_risks",
        )
        submitted = st.form_submit_button(
            "Save and continue", type="primary", icon=":material/arrow_forward:", width="stretch"
        )
    if submitted:
        if not cash_drivers or largest_driver is None or not risks:
            st.error("Select at least one driver and risk, and identify the largest cash-use movement.")
            return
        save_step_values(
            state,
            {
                "input_cash_drivers": list(cash_drivers),
                "input_largest_driver": largest_driver,
                "input_risks": list(risks),
            },
        )
        state["guided_step"] = 2
        st.rerun()


def _render_hiring_and_liquidity(context: GuidedScenarioContext) -> None:
    state = context.state
    render_back_button(state, 2)
    st.subheader("Hiring and liquidity")
    st.info(MONETARY_INPUT_GUIDANCE)
    st.warning(HIRING_UNIT_WARNING)
    st.markdown(
        '<div class="threshold-note"><strong>Keep the thresholds separate:</strong> '
        "the board floor is an internal limit; the lender minimum is a covenant.</div>",
        unsafe_allow_html=True,
    )
    with st.form("hiring_and_liquidity_form"):
        cost_left, cost_right = st.columns(2)
        with cost_left:
            h2_cost = number_input(state, "H2 2026 hiring cost (GBP m)", "input_h2_hiring_cost")
        with cost_right:
            annual_cost = number_input(state, "Annual recurring hiring cost (GBP m)", "input_annual_hiring_cost")
        cash_left, cash_right = st.columns(2)
        with cash_left:
            low_point = number_input(state, "Hiring-case cash low point (GBP m)", "input_cash_low_point")
        with cash_right:
            december_cash = number_input(state, "Hiring-case December cash (GBP m)", "input_december_cash")
        threshold_left, threshold_right = st.columns(2)
        with threshold_left:
            board_shortfall = number_input(state, "Shortfall below the board cash floor (GBP m)", "input_board_shortfall")
        with threshold_right:
            lender_headroom = number_input(state, "Headroom above the lender minimum at the low point (GBP m)", "input_lender_headroom")
        thresholds = st.multiselect(
            "Threshold interpretation",
            options=list(THRESHOLD_OPTIONS),
            format_func=THRESHOLD_OPTIONS.__getitem__,
            default=state_value(state, "input_thresholds") or (),
            key="input_thresholds",
        )
        submitted = st.form_submit_button(
            "Save and continue", type="primary", icon=":material/arrow_forward:", width="stretch"
        )
    if submitted:
        values = (h2_cost, annual_cost, low_point, december_cash, board_shortfall, lender_headroom)
        if any(value is None for value in values) or not thresholds:
            st.error("Complete every hiring and liquidity calculation and select threshold statements.")
            return
        save_step_values(
            state,
            {
                "input_h2_hiring_cost": h2_cost,
                "input_annual_hiring_cost": annual_cost,
                "input_cash_low_point": low_point,
                "input_december_cash": december_cash,
                "input_board_shortfall": board_shortfall,
                "input_lender_headroom": lender_headroom,
                "input_thresholds": list(thresholds),
            },
        )
        state["guided_step"] = 3
        st.rerun()


def _render_decision(context: GuidedScenarioContext) -> None:
    state = context.state
    render_back_button(state, 3)
    st.subheader("Recommendation and actions")
    recommendation_options = list(RECOMMENDATION_OPTIONS)
    saved_recommendation = state_value(state, "input_recommendation")
    recommendation_value = st.selectbox(
        "Recommendation route",
        options=recommendation_options,
        format_func=RECOMMENDATION_OPTIONS.__getitem__,
        index=(recommendation_options.index(saved_recommendation) if saved_recommendation in recommendation_options else None),
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
            default=state_value(state, safeguards_key) or (),
            key=safeguards_key,
        )
        missing_information = st.multiselect(
            "Information that would materially improve the decision",
            options=list(MISSING_INFORMATION_OPTIONS),
            format_func=MISSING_INFORMATION_OPTIONS.__getitem__,
            default=state_value(state, "input_missing_information") or (),
            key="input_missing_information",
        )
        tradeoffs = st.multiselect(
            "Commercial tradeoffs and capacity alternatives",
            options=list(TRADEOFF_OPTIONS),
            format_func=TRADEOFF_OPTIONS.__getitem__,
            default=state_value(state, "input_tradeoffs") or (),
            key="input_tradeoffs",
        )
        st.caption("Your wording is retained for comparison and self-review. It is not scored for keywords, length, grammar, sentiment, or communication quality.")
        ceo_response = st.text_area(
            "Concise recommendation to the CEO",
            height=150,
            placeholder="State your decision, finance case, risks, conditions, and next actions.",
            key="input_ceo_response",
        )
        submitted = st.form_submit_button(
            "Submit guided attempt", type="primary", icon=":material/check_circle:", width="stretch"
        )
    if submitted:
        if not safeguards or not missing_information or not tradeoffs or not ceo_response.strip():
            st.error("Select safeguards, missing information, and tradeoffs, then provide your CEO response.")
            return
        save_step_values(
            state,
            {
                "input_recommendation": recommendation_value,
                safeguards_key: list(safeguards),
                "input_missing_information": list(missing_information),
                "input_tradeoffs": list(tradeoffs),
                "input_ceo_response": ceo_response,
            },
        )
        context.submit_attempt(build_scenario_001_answers(state))


def render_scenario_001_guided_step(step: int, context: GuidedScenarioContext) -> None:
    """Render the approved Scenario 001 guided flow without changing its behavior."""

    renderers = (
        _render_financial_analysis,
        _render_drivers_and_risks,
        _render_hiring_and_liquidity,
        _render_decision,
    )
    renderers[min(max(step, 0), len(renderers) - 1)](context)


def scenario_001_recommendation_label(answers: LearnerAnswers | None) -> str:
    if answers is None or answers.recommendation is None:
        return "Not submitted"
    return answers.recommendation.label


def scenario_001_ceo_response(answers: LearnerAnswers | None) -> str | None:
    return answers.ceo_response if answers is not None else None
