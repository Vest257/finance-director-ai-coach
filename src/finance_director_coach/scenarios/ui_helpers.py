"""Small Streamlit helpers shared by scenario-owned guided flows."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping

import streamlit as st


def saved_key(widget_key: str) -> str:
    return f"saved_{widget_key}"


def state_value(state: Mapping[str, object], key: str) -> object | None:
    if key in state:
        return state[key]
    return state.get(saved_key(key))


def save_step_values(state: MutableMapping[str, object], values: Mapping[str, object]) -> None:
    for key, value in values.items():
        state[saved_key(key)] = value


def number_input(
    state: Mapping[str, object],
    label: str,
    key: str,
    help_text: str | None = None,
) -> float | None:
    saved_value = state_value(state, key)
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


def render_back_button(state: MutableMapping[str, object], step: int) -> None:
    if step <= 0:
        return
    if st.button("Back", key=f"back_from_step_{step}", icon=":material/arrow_back:"):
        save_step_values(
            state,
            {key: value for key, value in state.items() if key.startswith("input_")},
        )
        state["guided_step"] = step - 1
        st.rerun()
