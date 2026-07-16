"""Streamlit presentation layer for Fast Drill Mode V1."""

from __future__ import annotations

from collections.abc import MutableMapping

import streamlit as st

from finance_director_coach.drills import DrillDifficulty, DrillDomain, FinancialSkill
from finance_director_coach.practice import (
    PracticeAttempt,
    check_answer,
    create_attempt,
    filter_cards,
    load_practice_cards,
    next_card,
)
from finance_director_coach.streamlit_ui import APP_CSS


def initialize_practice_state(state: MutableMapping[str, object]) -> None:
    """Initialize only namespaced Practice state, leaving Scenario Coach untouched."""

    state.setdefault("practice_card_id", None)
    state.setdefault("practice_submitted", False)
    state.setdefault("practice_answer", None)
    state.setdefault("practice_attempts", [])
    state.setdefault("practice_filter_signature", None)


def reset_practice_card(state: MutableMapping[str, object]) -> None:
    """Reset current-card feedback without clearing the session attempt history."""

    state["practice_card_id"] = None
    state["practice_submitted"] = False
    state["practice_answer"] = None
    state.pop("practice_latest_attempt", None)


def clear_practice_history(state: MutableMapping[str, object]) -> None:
    """Clear only Fast Drill Mode's in-session records."""

    state["practice_attempts"] = []


def attempt_history_rows(attempts: list[PracticeAttempt]) -> list[dict[str, object]]:
    """Format session attempts newest-first for the learner-facing history table."""

    return [
        {
            "Result": "Correct" if attempt.is_correct else "Incorrect",
            "Finance domain": attempt.primary_domain,
            "Financial skill": attempt.financial_skill,
            "Difficulty": attempt.difficulty,
            "Submitted answer": attempt.submitted_answer,
            "Correct answer": attempt.correct_answer,
            "First attempt": "Yes" if attempt.first_attempt else "No",
            "Submitted at": attempt.timestamp.strftime("%Y-%m-%d %H:%M UTC"),
        }
        for attempt in reversed(attempts)
    ]


def _enum_selection(label: str, enum_type: type[DrillDomain] | type[FinancialSkill] | type[DrillDifficulty], key: str) -> object | None:
    options = [None, *list(enum_type)]
    return st.selectbox(label, options=options, format_func=lambda item: "All" if item is None else item.value, key=key)


def _render_card(card) -> None:
    st.subheader("Question")
    for paragraph in card.learner_context:
        st.write(paragraph)
    if card.learner_table:
        st.table([dict(zip(card.learner_table[0], row, strict=True)) for row in card.learner_table[1:]])
    st.markdown(f"**{card.learner_question}**")
    st.caption(f"Answer unit: {card.unit}")
    st.caption(f"Card ID: {card.card_id}")


def _render_feedback(card) -> None:
    attempt = st.session_state.get("practice_latest_attempt")
    if not isinstance(attempt, PracticeAttempt):
        return
    feedback = revealed_feedback(card, attempt)
    if attempt.is_correct:
        st.success(feedback["result"])
    else:
        st.error(feedback["result"])
    st.markdown(f"**Worked calculation:** {feedback['worked_calculation']}")
    st.markdown(f"**Interpretation:** {feedback['why_it_matters']}")


def revealed_feedback(card, attempt: PracticeAttempt | None) -> dict[str, str] | None:
    """Return learner feedback only after a completed, valid submission."""

    if attempt is None:
        return None
    result = f"Correct. Submitted answer: {attempt.submitted_answer:g}." if attempt.is_correct else (
        f"Incorrect. Submitted answer: {attempt.submitted_answer:g}. "
        f"Correct answer: {attempt.correct_answer:g}."
    )
    return {"result": result, "worked_calculation": card.worked_calculation, "why_it_matters": card.why_it_matters}


def run_practice_app() -> None:
    """Render a one-card, session-only numerical-practice flow."""

    st.markdown(APP_CSS, unsafe_allow_html=True)
    initialize_practice_state(st.session_state)
    st.markdown('<p class="pilot-kicker">FinanceOS / Alpha 0.1</p>', unsafe_allow_html=True)
    st.title("Practice")
    st.caption("Fast Drill Mode: deterministic calculation practice. Attempts stay in this browser session only.")

    filters = st.columns(3)
    with filters[0]:
        domain = _enum_selection("Finance domain", DrillDomain, "practice_domain")
    with filters[1]:
        skill = _enum_selection("Financial skill", FinancialSkill, "practice_skill")
    with filters[2]:
        difficulty = _enum_selection("Difficulty", DrillDifficulty, "practice_difficulty")
    signature = (domain, skill, difficulty)
    if st.session_state["practice_filter_signature"] != signature:
        reset_practice_card(st.session_state)
        st.session_state["practice_filter_signature"] = signature

    cards = filter_cards(load_practice_cards(), primary_domain=domain, financial_skill=skill, difficulty=difficulty)
    st.caption(f"{len(cards)} matching cards")
    if not cards:
        st.warning("No cards match this combination. Choose a different filter combination.")
        return
    card = next((item for item in cards if item.card_id == st.session_state["practice_card_id"]), None)
    if card is None:
        card = next_card(cards, None)
        st.session_state["practice_card_id"] = card.card_id
    _render_card(card)

    if not st.session_state["practice_submitted"]:
        with st.form("practice_answer_form"):
            answer = st.number_input("Your numerical answer", value=None, step=0.01, placeholder="Enter a value", key="practice_answer")
            submitted = st.form_submit_button("Check answer", type="primary", width="stretch")
        if submitted:
            outcome = check_answer(card, answer)
            if not outcome.is_valid:
                st.error(outcome.message)
            else:
                attempts = st.session_state["practice_attempts"]
                if not isinstance(attempts, list):
                    attempts = []
                attempt = create_attempt(card, outcome, attempts)
                attempts.append(attempt)
                st.session_state["practice_attempts"] = attempts
                st.session_state["practice_latest_attempt"] = attempt
                st.session_state["practice_submitted"] = True
                st.rerun()
    else:
        _render_feedback(card)
        if st.button("Next question", type="primary", icon=":material/arrow_forward:", width="stretch"):
            following = next_card(cards, card.card_id)
            st.session_state["practice_card_id"] = following.card_id if following else None
            st.session_state["practice_submitted"] = False
            st.session_state["practice_answer"] = None
            st.session_state.pop("practice_latest_attempt", None)
            st.rerun()

    attempts = st.session_state["practice_attempts"]
    if isinstance(attempts, list) and attempts:
        st.subheader("Session attempt history")
        st.caption(f"{len(attempts)} attempt{'s' if len(attempts) != 1 else ''} in this browser session.")
        st.table(attempt_history_rows(attempts))
        if st.button("Clear practice-session history", icon=":material/delete_sweep:"):
            clear_practice_history(st.session_state)
            st.rerun()
