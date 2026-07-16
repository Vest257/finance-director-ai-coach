"""Four-stage Streamlit adapter for Scenario 002's integrated finance decision."""

from __future__ import annotations

from collections.abc import Mapping

import streamlit as st

from finance_director_coach.models import RecommendationRoute
from finance_director_coach.scenarios.contracts import GuidedScenarioContext
from finance_director_coach.scenarios.scenario_002 import (
    CASH_ABSORBER_OPTIONS, CLASSIFICATION_OPTIONS, MONETARY_INPUT_GUIDANCE,
    QUALITY_OPTIONS, REQUIRED_ROUTE_SAFEGUARDS, ROUTE_DECISION_ASSUMPTION_OPTIONS,
    ROUTE_PROTECTION_OPTIONS, ROUTE_SAFEGUARD_OPTIONS,
    Scenario002Answers,
)
from finance_director_coach.scenarios.ui_helpers import number_input, render_back_button, save_step_values, state_value

ROUTES = ("renew", "renegotiate", "exit")
ROUTE_LABELS = {"renew": "Renew as proposed", "renegotiate": "Renegotiate to target economics", "exit": "Exit and redeploy"}


def _number(state: Mapping[str, object], key: str) -> float:
    value = state_value(state, key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Missing numeric input: {key}")
    return float(value)


def _selection(state: Mapping[str, object], key: str) -> frozenset[str]:
    value = state_value(state, key)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"Missing selection input: {key}")
    return frozenset(value)


def _route_values(state: Mapping[str, object], prefix: str) -> dict[str, float]:
    return {route: _number(state, f"input_{prefix}_{route}") for route in ROUTES}


def build_scenario_002_answers(state: Mapping[str, object]) -> Scenario002Answers:
    route_value = state_value(state, "input_recommendation")
    response = state_value(state, "input_ceo_response")
    if not isinstance(route_value, str) or not isinstance(response, str):
        raise ValueError("Missing Scenario 002 decision input")
    route = RecommendationRoute(route_value)
    return Scenario002Answers(
        quality_interpretation=str(state_value(state, "input_quality")),
        operating_cash_flow=_number(state, "input_operating_cash"), cash_conversion_percent=_number(state, "input_cash_conversion"), largest_cash_absorber=str(state_value(state, "input_cash_absorber")),
        northstar_dso=_number(state, "input_dso"), receivable_concentration_percent=_number(state, "input_concentration"), net_working_capital=_number(state, "input_net_working_capital"), balance_sheet_exposure=_number(state, "input_balance_sheet_exposure"), exposure_at_risk=_number(state, "input_exposure_at_risk"),
        route_ebitda=_route_values(state, "ebitda"), route_operating_cash=_route_values(state, "route_cash"), route_low_cash=_route_values(state, "low_cash"), route_rcf_draw=_route_values(state, "rcf_draw"), route_headroom=_route_values(state, "headroom"),
        classifications=_selection(state, "input_classifications"), recommendation=route, safeguards=_selection(state, f"input_safeguards_{route.value}"), protections=_selection(state, "input_protections"), assumptions=_selection(state, "input_assumptions"), ceo_response=response.strip(),
    )


def _save(state: dict[str, object], values: dict[str, object], step: int) -> None:
    save_step_values(state, values)
    state["guided_step"] = step
    st.rerun()


def _stage_one(context: GuidedScenarioContext) -> None:
    state = context.state
    st.subheader("Quality of earnings and cash conversion")
    st.info(MONETARY_INPUT_GUIDANCE)
    st.caption("The management pack already shows revenue and margin trend. Reconcile the cash bridge and interpret what it means.")
    with st.form("scn_002_cash_conversion"):
        quality = st.selectbox("Interpret the quality of earnings", list(QUALITY_OPTIONS), format_func=QUALITY_OPTIONS.__getitem__, index=None, placeholder="Select one", key="input_quality")
        left, right = st.columns(2)
        with left: operating_cash = number_input(state, "Operating cash flow (GBP m)", "input_operating_cash")
        with right: conversion = number_input(state, "EBITDA-to-operating-cash conversion (%)", "input_cash_conversion")
        absorber = st.selectbox("Largest cash absorber", list(CASH_ABSORBER_OPTIONS), format_func=CASH_ABSORBER_OPTIONS.__getitem__, index=None, placeholder="Select one", key="input_cash_absorber")
        submitted = st.form_submit_button("Save and continue", type="primary", width="stretch")
    if submitted:
        if None in (quality, operating_cash, conversion, absorber): st.error("Complete the interpretation and every cash-conversion input."); return
        _save(state, {"input_quality": quality, "input_operating_cash": operating_cash, "input_cash_conversion": conversion, "input_cash_absorber": absorber}, 1)


def _stage_two(context: GuidedScenarioContext) -> None:
    state = context.state
    render_back_button(state, 1)
    st.subheader("Balance-sheet and customer exposure")
    st.caption("Use the definitions in the financial pack. Monetary inputs are GBP millions.")
    with st.form("scn_002_balance_sheet"):
        a, b = st.columns(2)
        with a: dso = number_input(state, "Northstar DSO (days)", "input_dso")
        with b: concentration = number_input(state, "Northstar share of company receivables (%)", "input_concentration")
        c, d, e = st.columns(3)
        with c: net_wc = number_input(state, "Net customer working-capital exposure (GBP m)", "input_net_working_capital")
        with d: exposure = number_input(state, "Total customer balance-sheet exposure (GBP m)", "input_balance_sheet_exposure")
        with e: at_risk = number_input(state, "Customer balance-sheet exposure at risk (GBP m)", "input_exposure_at_risk")
        submitted = st.form_submit_button("Save and continue", type="primary", width="stretch")
    if submitted:
        if any(value is None for value in (dso, concentration, net_wc, exposure, at_risk)): st.error("Complete every balance-sheet calculation."); return
        _save(state, {"input_dso": dso, "input_concentration": concentration, "input_net_working_capital": net_wc, "input_balance_sheet_exposure": exposure, "input_exposure_at_risk": at_risk}, 2)


def _route_calculation_inputs(state: dict[str, object], route: str) -> dict[str, float | None]:
    return {
        "ebitda": number_input(state, "Annual EBITDA (GBP m)", f"input_ebitda_{route}"),
        "route_cash": number_input(state, "Annual operating cash (GBP m)", f"input_route_cash_{route}"),
        "low_cash": number_input(state, "Lowest monthly cash (GBP m)", f"input_low_cash_{route}"),
        "rcf_draw": number_input(state, "RCF draw required (GBP m)", f"input_rcf_draw_{route}"),
        "headroom": number_input(state, "Remaining RCF headroom (GBP m)", f"input_headroom_{route}"),
    }


def _stage_three(context: GuidedScenarioContext) -> None:
    state = context.state
    render_back_button(state, 2)
    st.subheader("Route cash and liquidity")
    st.caption("Compare all routes. The annual operating-cash outcome and monthly liquidity trough are different views of the same decision.")
    with st.form("scn_002_route_liquidity"):
        route_inputs: dict[str, dict[str, float | None]] = {}
        for route, tab in zip(ROUTES, st.tabs([ROUTE_LABELS[route] for route in ROUTES]), strict=True):
            with tab:
                route_inputs[route] = _route_calculation_inputs(state, route)
        classifications = st.multiselect("Select the six stated classifications, including provision creation, settlement, and release", list(CLASSIFICATION_OPTIONS), format_func=CLASSIFICATION_OPTIONS.__getitem__, key="input_classifications")
        submitted = st.form_submit_button("Save and continue", type="primary", width="stretch")
    if submitted:
        if any(value is None for values in route_inputs.values() for value in values.values()) or len(classifications) != 6: st.error("Complete every route calculation and select all six stated classifications."); return
        values = {f"input_{prefix}_{route}": route_inputs[route][prefix] for route in ROUTES for prefix in route_inputs[route]}
        values["input_classifications"] = list(classifications)
        _save(state, values, 3)


def _stage_four(context: GuidedScenarioContext) -> None:
    state = context.state
    render_back_button(state, 3)
    st.subheader("Finance Director decision")
    route_value = st.selectbox("Recommendation route", [route.value for route in RecommendationRoute], format_func=lambda value: RecommendationRoute(value).label, index=None, placeholder="Select one", key="input_recommendation")
    if route_value is None:
        st.info("Select a route to see its minimum safeguards."); return
    route = RecommendationRoute(route_value)
    with st.form("scn_002_decision"):
        safeguards = st.multiselect(f"Safeguards for {route.label}", list(ROUTE_SAFEGUARD_OPTIONS[route]), format_func=ROUTE_SAFEGUARD_OPTIONS[route].__getitem__, key=f"input_safeguards_{route.value}")
        protections = st.multiselect("Select the two minimum cash and balance-sheet protections", list(ROUTE_PROTECTION_OPTIONS[route]), format_func=ROUTE_PROTECTION_OPTIONS[route].__getitem__, key="input_protections")
        assumptions = st.multiselect("Select the two assumptions most likely to change this decision", list(ROUTE_DECISION_ASSUMPTION_OPTIONS[route]), format_func=ROUTE_DECISION_ASSUMPTION_OPTIONS[route].__getitem__, key="input_assumptions")
        st.caption("Your CEO wording is stored for self-review only. It is not scored for keywords, length, grammar, sentiment, or persuasiveness.")
        response = st.text_area("Concise recommendation to the CEO", key="input_ceo_response")
        submitted = st.form_submit_button("Submit guided attempt", type="primary", width="stretch")
    if submitted:
        if not safeguards or len(protections) != 2 or len(assumptions) != 2 or not response.strip(): st.error("Complete safeguards, exactly two protections, two assumptions, and the CEO response."); return
        save_step_values(state, {"input_recommendation": route_value, f"input_safeguards_{route.value}": list(safeguards), "input_protections": list(protections), "input_assumptions": list(assumptions), "input_ceo_response": response})
        context.submit_attempt(build_scenario_002_answers(state))


def render_scenario_002_guided_step(step: int, context: GuidedScenarioContext) -> None:
    (_stage_one, _stage_two, _stage_three, _stage_four)[min(max(step, 0), 3)](context)


def scenario_002_recommendation_label(answers: Scenario002Answers | None) -> str:
    return answers.recommendation.label if answers and answers.recommendation else "Not submitted"


def scenario_002_ceo_response(answers: Scenario002Answers | None) -> str | None:
    return answers.ceo_response if answers else None
