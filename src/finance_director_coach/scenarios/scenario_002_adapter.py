"""Scenario 002 answer translation and Streamlit guided-question flow."""

from __future__ import annotations

from collections.abc import Mapping

import streamlit as st

from finance_director_coach.models import RecommendationRoute
from finance_director_coach.scenarios.contracts import GuidedScenarioContext
from finance_director_coach.scenarios.scenario_002 import (
    AVOIDABLE_COST_OPTIONS,
    DECISION_CONDITION_OPTIONS,
    DRIVER_OPTIONS,
    MARGIN_INTERPRETATION_OPTIONS,
    MISSING_INFORMATION_OPTIONS,
    MONETARY_INPUT_GUIDANCE,
    RECOMMENDATION_OPTIONS,
    ROUTE_SAFEGUARD_OPTIONS,
    Scenario002Answers,
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


def build_scenario_002_answers(state: Mapping[str, object]) -> Scenario002Answers:
    """Translate validated Scenario 002 widget state into its typed attempt model."""

    route_value = state_value(state, "input_recommendation")
    if not isinstance(route_value, str):
        raise ValueError("Missing recommendation route")
    recommendation = RecommendationRoute(route_value)
    response = state_value(state, "input_ceo_response")
    if not isinstance(response, str):
        raise ValueError("Missing CEO response")
    return Scenario002Answers(
        revenue_growth_percent=_number_from_state(state, "input_revenue_growth"),
        prior_gross_margin_percent=_number_from_state(state, "input_prior_gross_margin"),
        current_gross_margin_percent=_number_from_state(state, "input_current_gross_margin"),
        prior_ebitda_margin_percent=_number_from_state(state, "input_prior_ebitda_margin"),
        current_ebitda_margin_percent=_number_from_state(state, "input_current_ebitda_margin"),
        margin_interpretation=str(state_value(state, "input_margin_interpretation")),
        customer_contribution=_number_from_state(state, "input_customer_contribution"),
        customer_contribution_margin_percent=_number_from_state(state, "input_customer_contribution_margin"),
        economic_revenue=_number_from_state(state, "input_economic_revenue"),
        price_increase=_number_from_state(state, "input_price_increase"),
        price_increase_percent=_number_from_state(state, "input_price_increase_percent"),
        cost_reduction=_number_from_state(state, "input_cost_reduction"),
        requested_discount=_number_from_state(state, "input_requested_discount"),
        discounted_contribution_margin_percent=_number_from_state(state, "input_discounted_contribution_margin"),
        top_drivers=_strings_from_state(state, "input_top_drivers"),
        avoidable_costs=_strings_from_state(state, "input_avoidable_costs"),
        missing_information=_strings_from_state(state, "input_missing_information"),
        recommendation=recommendation,
        safeguards=_strings_from_state(state, f"input_safeguards_{recommendation.value}"),
        decision_conditions=_strings_from_state(state, "input_decision_conditions"),
        ceo_response=response.strip(),
    )


def _render_company_performance(context: GuidedScenarioContext) -> None:
    state = context.state
    st.subheader("Company performance")
    st.write("Enter margin and growth answers as percentage points.")
    st.info(MONETARY_INPUT_GUIDANCE)
    with st.form("scn_002_company_performance_form"):
        revenue_growth = number_input(
            state,
            "Company revenue growth (%)",
            "input_revenue_growth",
            "Calculate (current period - prior period) / prior period x 100.",
        )
        st.markdown("**Gross margin**")
        prior_gross, current_gross = st.columns(2)
        with prior_gross:
            prior_gross_margin = number_input(state, "Prior gross margin (%)", "input_prior_gross_margin")
        with current_gross:
            current_gross_margin = number_input(state, "Current gross margin (%)", "input_current_gross_margin")
        st.markdown("**EBITDA margin**")
        prior_ebitda, current_ebitda = st.columns(2)
        with prior_ebitda:
            prior_ebitda_margin = number_input(state, "Prior EBITDA margin (%)", "input_prior_ebitda_margin")
        with current_ebitda:
            current_ebitda_margin = number_input(state, "Current EBITDA margin (%)", "input_current_ebitda_margin")
        interpretation_options = list(MARGIN_INTERPRETATION_OPTIONS)
        saved_interpretation = state_value(state, "input_margin_interpretation")
        margin_interpretation = st.selectbox(
            "Interpret the company performance",
            options=interpretation_options,
            format_func=MARGIN_INTERPRETATION_OPTIONS.__getitem__,
            index=(interpretation_options.index(saved_interpretation) if saved_interpretation in interpretation_options else None),
            placeholder="Select one",
            key="input_margin_interpretation",
        )
        submitted = st.form_submit_button(
            "Save and continue", type="primary", icon=":material/arrow_forward:", width="stretch"
        )
    if submitted:
        values = (
            revenue_growth,
            prior_gross_margin,
            current_gross_margin,
            prior_ebitda_margin,
            current_ebitda_margin,
        )
        if any(value is None for value in values) or margin_interpretation is None:
            st.error("Complete every company calculation and choose an interpretation before continuing.")
            return
        save_step_values(
            state,
            {
                "input_revenue_growth": revenue_growth,
                "input_prior_gross_margin": prior_gross_margin,
                "input_current_gross_margin": current_gross_margin,
                "input_prior_ebitda_margin": prior_ebitda_margin,
                "input_current_ebitda_margin": current_ebitda_margin,
                "input_margin_interpretation": margin_interpretation,
            },
        )
        state["guided_step"] = 1
        st.rerun()


def _render_customer_economics(context: GuidedScenarioContext) -> None:
    state = context.state
    render_back_button(state, 1)
    st.subheader("Customer economics")
    st.info(MONETARY_INPUT_GUIDANCE)
    st.caption("Enter all margin and price percentage answers as percentage points.")
    with st.form("scn_002_customer_economics_form"):
        st.markdown("**Customer contribution**")
        contribution_left, contribution_right = st.columns(2)
        with contribution_left:
            contribution = number_input(state, "Customer contribution (GBP m)", "input_customer_contribution")
        with contribution_right:
            contribution_margin = number_input(
                state, "Customer contribution margin (%)", "input_customer_contribution_margin"
            )
        st.markdown("**Target pricing**")
        pricing_left, pricing_middle, pricing_right = st.columns(3)
        with pricing_left:
            economic_revenue = number_input(
                state, "Economically attractive revenue (GBP m)", "input_economic_revenue"
            )
        with pricing_middle:
            price_increase = number_input(state, "Required price increase (GBP m)", "input_price_increase")
        with pricing_right:
            price_increase_percent = number_input(
                state, "Required price increase (%)", "input_price_increase_percent"
            )
        cost_reduction = number_input(
            state, "Alternative cost reduction required (GBP m)", "input_cost_reduction"
        )
        st.markdown("**Requested additional discount**")
        discount_left, discount_right = st.columns(2)
        with discount_left:
            requested_discount = number_input(
                state, "Additional discount effect (GBP m)", "input_requested_discount"
            )
        with discount_right:
            discounted_margin = number_input(
                state,
                "Contribution margin after additional discount (%)",
                "input_discounted_contribution_margin",
            )
        submitted = st.form_submit_button(
            "Save and continue", type="primary", icon=":material/arrow_forward:", width="stretch"
        )
    if submitted:
        values = (
            contribution,
            contribution_margin,
            economic_revenue,
            price_increase,
            price_increase_percent,
            cost_reduction,
            requested_discount,
            discounted_margin,
        )
        if any(value is None for value in values):
            st.error("Complete every customer-economics calculation before continuing.")
            return
        save_step_values(
            state,
            {
                "input_customer_contribution": contribution,
                "input_customer_contribution_margin": contribution_margin,
                "input_economic_revenue": economic_revenue,
                "input_price_increase": price_increase,
                "input_price_increase_percent": price_increase_percent,
                "input_cost_reduction": cost_reduction,
                "input_requested_discount": requested_discount,
                "input_discounted_contribution_margin": discounted_margin,
            },
        )
        state["guided_step"] = 2
        st.rerun()


def _render_drivers_and_risks(context: GuidedScenarioContext) -> None:
    state = context.state
    render_back_button(state, 2)
    st.subheader("Drivers and risks")
    st.caption("Prioritise the requested number of choices. Selecting every option is not an acceptable response.")
    with st.form("scn_002_drivers_and_risks_form"):
        top_drivers = st.multiselect(
            "Select the three most important margin-deterioration drivers",
            options=list(DRIVER_OPTIONS),
            format_func=DRIVER_OPTIONS.__getitem__,
            default=state_value(state, "input_top_drivers") or (),
            key="input_top_drivers",
        )
        avoidable_costs = st.multiselect(
            "Select the four direct cost categories avoidable after a customer exit",
            options=list(AVOIDABLE_COST_OPTIONS),
            format_func=AVOIDABLE_COST_OPTIONS.__getitem__,
            default=state_value(state, "input_avoidable_costs") or (),
            key="input_avoidable_costs",
        )
        missing_information = st.multiselect(
            "Select the three missing information items that could change the route",
            options=list(MISSING_INFORMATION_OPTIONS),
            format_func=MISSING_INFORMATION_OPTIONS.__getitem__,
            default=state_value(state, "input_missing_information") or (),
            key="input_missing_information",
        )
        submitted = st.form_submit_button(
            "Save and continue", type="primary", icon=":material/arrow_forward:", width="stretch"
        )
    if submitted:
        if len(top_drivers) != 3 or len(avoidable_costs) != 4 or len(missing_information) != 3:
            st.error("Select exactly three priority drivers, four avoidable cost categories, and three missing information items.")
            return
        save_step_values(
            state,
            {
                "input_top_drivers": list(top_drivers),
                "input_avoidable_costs": list(avoidable_costs),
                "input_missing_information": list(missing_information),
            },
        )
        state["guided_step"] = 3
        st.rerun()


def _render_decision(context: GuidedScenarioContext) -> None:
    state = context.state
    render_back_button(state, 3)
    st.subheader("Renewal decision")
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
        st.info("Select a recommendation route to see its safeguard options.")
        return
    recommendation = RecommendationRoute(recommendation_value)
    safeguards_key = f"input_safeguards_{recommendation.value}"
    with st.form("scn_002_decision_form"):
        safeguards = st.multiselect(
            f"Safeguards for {recommendation.label}",
            options=list(ROUTE_SAFEGUARD_OPTIONS[recommendation]),
            format_func=ROUTE_SAFEGUARD_OPTIONS[recommendation].__getitem__,
            default=state_value(state, safeguards_key) or (),
            key=safeguards_key,
        )
        decision_conditions = st.multiselect(
            "Select the two conditions that should determine the recommendation",
            options=list(DECISION_CONDITION_OPTIONS),
            format_func=DECISION_CONDITION_OPTIONS.__getitem__,
            default=state_value(state, "input_decision_conditions") or (),
            key="input_decision_conditions",
        )
        st.caption("Your wording is retained for comparison and self-review. It is not scored for keywords, length, grammar, sentiment, or communication quality.")
        ceo_response = st.text_area(
            "Concise recommendation to the CEO",
            height=150,
            placeholder="State the route, economics, safeguards, and what would change the decision.",
            key="input_ceo_response",
        )
        submitted = st.form_submit_button(
            "Submit guided attempt", type="primary", icon=":material/check_circle:", width="stretch"
        )
    if submitted:
        if not safeguards or len(decision_conditions) != 2 or not ceo_response.strip():
            st.error("Select safeguards and exactly two decision conditions, then provide your CEO response.")
            return
        save_step_values(
            state,
            {
                "input_recommendation": recommendation_value,
                safeguards_key: list(safeguards),
                "input_decision_conditions": list(decision_conditions),
                "input_ceo_response": ceo_response,
            },
        )
        context.submit_attempt(build_scenario_002_answers(state))


def render_scenario_002_guided_step(step: int, context: GuidedScenarioContext) -> None:
    """Render Scenario 002's four guided stages."""

    renderers = (
        _render_company_performance,
        _render_customer_economics,
        _render_drivers_and_risks,
        _render_decision,
    )
    renderers[min(max(step, 0), len(renderers) - 1)](context)


def scenario_002_recommendation_label(answers: Scenario002Answers | None) -> str:
    if answers is None or answers.recommendation is None:
        return "Not submitted"
    return answers.recommendation.label


def scenario_002_ceo_response(answers: Scenario002Answers | None) -> str | None:
    return answers.ceo_response if answers is not None else None
