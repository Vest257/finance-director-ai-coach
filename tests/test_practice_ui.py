"""Streamlit behavior checks for the separate Fast Drill Mode page."""

from __future__ import annotations

from streamlit.testing.v1 import AppTest

from finance_director_coach.practice import check_answer, create_attempt, load_practice_cards


def _practice_entry() -> None:
    from finance_director_coach.practice_ui import run_practice_app

    run_practice_app()


def test_practice_submission_reveals_feedback_then_next_question() -> None:
    app = AppTest.from_function(_practice_entry, default_timeout=10).run()
    assert not app.exception
    assert app.title[0].value == "Practice"
    rendered_before_submit = str(app)
    card_id = app.session_state["practice_card_id"]
    assert any(f"Card ID: {card_id}" in item.value for item in app.get("caption"))
    assert "Worked calculation:" not in rendered_before_submit
    assert "Correct answer:" not in rendered_before_submit
    assert "Arconic recognized USD 1,503 million more goodwill" not in rendered_before_submit

    app.number_input(key="practice_answer").set_value(1503.0)
    app.button[0].click().run()
    assert not app.exception
    assert [message.value for message in app.success] == ["Correct. Submitted answer: 1503."]
    rendered_calculations = [item.value.replace("**", "") for item in app.markdown]
    assert "Worked calculation: 1,801 − 298 = 1,503 USD million." in rendered_calculations
    assert any("Interpretation:" in item.value for item in app.markdown)
    assert "Worked calculation: Calculation: 1,801 − 298 = 1,503 USD million." not in rendered_calculations
    assert any("Arconic recognized USD 1,503 million more goodwill" in item.value for item in app.markdown)
    assert len(app.session_state["practice_attempts"]) == 1
    history = app.table[0].value
    assert history.loc[0, "Submitted answer"] == 1503.0
    assert history.loc[0, "Correct answer"] == 1503.0
    assert history.loc[0, "First attempt"] == "Yes"

    app.button[0].click().run()
    assert not app.exception
    assert app.session_state["practice_card_id"] != card_id
    assert app.session_state["practice_submitted"] is False
    assert app.session_state["practice_answer"] is None
    assert "practice_latest_attempt" not in app.session_state


def test_history_displays_repeat_attempts_and_clear_preserves_current_feedback() -> None:
    card = load_practice_cards()[0]
    first = create_attempt(card, check_answer(card, card.correct_answer), [])
    repeat = create_attempt(card, check_answer(card, card.correct_answer + 1), [first])
    app = AppTest.from_function(_practice_entry, default_timeout=10).run()
    app.session_state["stage"] = "scenario"
    app.session_state["practice_card_id"] = card.card_id
    app.session_state["practice_submitted"] = True
    app.session_state["practice_latest_attempt"] = repeat
    app.session_state["practice_attempts"] = [first, repeat]
    app.run()
    history = app.table[0].value
    assert history.loc[0, "First attempt"] == "No"
    assert history.loc[0, "Submitted answer"] == card.correct_answer + 1
    assert history.loc[0, "Correct answer"] == card.correct_answer

    card_id = app.session_state["practice_card_id"]
    latest_attempt_id = app.session_state["practice_latest_attempt"].attempt_id
    app.button[1].click().run()
    app.run()
    assert not app.table
    assert app.session_state["practice_attempts"] == []
    assert app.session_state["practice_card_id"] == card_id
    assert app.session_state["practice_latest_attempt"].attempt_id == latest_attempt_id
    assert app.session_state["stage"] == "scenario"


def test_practice_filters_can_show_a_clear_zero_result_state() -> None:
    app = AppTest.from_function(_practice_entry, default_timeout=10).run()
    app.selectbox(key="practice_domain").set_value("P&L")
    app.selectbox(key="practice_skill").set_value("book_value")
    app.selectbox(key="practice_difficulty").set_value("foundational").run()
    assert not app.exception
    assert [message.value for message in app.warning] == [
        "No cards match this combination. Choose a different filter combination."
    ]
