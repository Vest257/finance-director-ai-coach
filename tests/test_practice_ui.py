"""Streamlit behavior checks for the separate Fast Drill Mode page."""

from __future__ import annotations

from streamlit.testing.v1 import AppTest


def _practice_entry() -> None:
    from finance_director_coach.practice_ui import run_practice_app

    run_practice_app()


def test_practice_submission_reveals_feedback_then_next_question() -> None:
    app = AppTest.from_function(_practice_entry, default_timeout=10).run()
    assert not app.exception
    assert app.title[0].value == "Practice"
    rendered_before_submit = str(app)
    assert "Worked calculation:" not in rendered_before_submit
    assert "Correct answer:" not in rendered_before_submit

    card_id = app.session_state["practice_card_id"]
    app.number_input(key="practice_answer").set_value(1503.0)
    app.button[0].click().run()
    assert not app.exception
    assert [message.value for message in app.success] == ["Correct. Submitted answer: 1503."]
    assert any("Worked calculation:" in item.value for item in app.markdown)
    assert len(app.session_state["practice_attempts"]) == 1

    app.button[0].click().run()
    assert not app.exception
    assert app.session_state["practice_card_id"] != card_id
    assert app.session_state["practice_submitted"] is False


def test_practice_filters_can_show_a_clear_zero_result_state() -> None:
    app = AppTest.from_function(_practice_entry, default_timeout=10).run()
    app.selectbox(key="practice_domain").set_value("P&L")
    app.selectbox(key="practice_skill").set_value("book_value")
    app.selectbox(key="practice_difficulty").set_value("foundational").run()
    assert not app.exception
    assert [message.value for message in app.warning] == [
        "No cards match this combination. Choose a different filter combination."
    ]
