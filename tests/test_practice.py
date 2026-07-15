"""Tests for Fast Drill Mode's UI-independent deterministic behavior."""

from __future__ import annotations

from datetime import UTC, datetime
from math import inf, nan

from finance_director_coach.drills import DrillDifficulty
from finance_director_coach.practice import (
    check_answer,
    create_attempt,
    filter_cards,
    load_practice_cards,
    next_card,
)
from finance_director_coach.practice_ui import (
    clear_practice_history,
    initialize_practice_state,
    reset_practice_card,
    revealed_feedback,
)


def test_loads_exactly_the_committed_100_card_bank() -> None:
    assert len(load_practice_cards()) == 100


def test_combined_filters_require_every_selection() -> None:
    cards = load_practice_cards()
    chosen = cards[0]
    matches = filter_cards(
        cards,
        primary_domain=chosen.primary_domain,
        financial_skill=chosen.financial_skill,
        difficulty=chosen.difficulty,
    )
    assert matches
    assert all(
        card.primary_domain is chosen.primary_domain
        and card.financial_skill is chosen.financial_skill
        and card.difficulty is chosen.difficulty
        for card in matches
    )
    assert filter_cards(cards, difficulty=DrillDifficulty.INTERMEDIATE)


def test_answer_check_uses_inclusive_tolerance_and_rejects_invalid_numbers() -> None:
    card = load_practice_cards()[0]
    assert check_answer(card, card.correct_answer + card.tolerance).is_correct is True
    assert check_answer(card, card.correct_answer + card.tolerance * 1.01).is_correct is False
    for invalid in (None, "1503", nan, inf, -inf):
        result = check_answer(card, invalid)
        assert not result.is_valid
        assert result.is_correct is None


def test_attempt_record_includes_required_fields_and_marks_reattempts() -> None:
    card = load_practice_cards()[0]
    check = check_answer(card, card.correct_answer)
    moment = datetime(2026, 7, 15, tzinfo=UTC)
    first = create_attempt(card, check, [], timestamp=moment)
    assert first.card_id == card.card_id
    assert first.primary_domain == card.primary_domain.value
    assert first.financial_skill == card.financial_skill.value
    assert first.calculation_method == card.calculation_method.value
    assert first.difficulty == card.difficulty.value
    assert first.submitted_answer == card.correct_answer
    assert first.correct_answer == card.correct_answer
    assert first.is_correct is True
    assert first.first_attempt is True
    assert first.timestamp == moment
    assert first.attempt_id
    assert create_attempt(card, check, [first]).first_attempt is False


def test_next_card_uses_bank_order_and_wraps() -> None:
    cards = load_practice_cards()[:2]
    assert next_card(cards, None) is cards[0]
    assert next_card(cards, cards[0].card_id) is cards[1]
    assert next_card(cards, cards[1].card_id) is cards[0]


def test_practice_state_reset_and_history_are_isolated_from_scenario_state() -> None:
    state: dict[str, object] = {
        "stage": "results",
        "answers": object(),
        "practice_card_id": "FINQA-1",
        "practice_submitted": True,
        "practice_answer": 12.0,
        "practice_attempts": [object()],
    }
    initialize_practice_state(state)
    reset_practice_card(state)
    assert state["stage"] == "results"
    assert state["answers"] is not None
    assert state["practice_card_id"] is None
    assert state["practice_submitted"] is False
    assert state["practice_attempts"] == [state["practice_attempts"][0]]
    clear_practice_history(state)
    assert state["practice_attempts"] == []
    assert state["stage"] == "results"


def test_no_answer_leaks_before_submit_and_feedback_reveals_afterwards() -> None:
    card = load_practice_cards()[0]
    assert revealed_feedback(card, None) is None
    correct = create_attempt(card, check_answer(card, card.correct_answer), [])
    correct_feedback = revealed_feedback(card, correct)
    assert correct_feedback is not None
    assert correct_feedback["result"].startswith("Correct.")
    assert correct_feedback["worked_calculation"] == card.worked_calculation
    incorrect = create_attempt(card, check_answer(card, card.correct_answer + 1), [])
    incorrect_feedback = revealed_feedback(card, incorrect)
    assert incorrect_feedback is not None
    assert incorrect_feedback["result"].startswith("Incorrect.")
    assert f"{card.correct_answer:g}" in incorrect_feedback["result"]
