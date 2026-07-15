"""Pure, deterministic core for the in-memory Fast Drill Mode."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from functools import lru_cache
from math import isfinite
from pathlib import Path
from typing import Iterable
from uuid import uuid4

from finance_director_coach.drills import DrillCard, DrillDifficulty, DrillDomain, FinancialSkill, load_cards


DRILL_BANK_PATH = Path(__file__).resolve().parents[2] / "data" / "drills" / "finqa_cards_v1.json"


@dataclass(frozen=True)
class AnswerCheck:
    """The deterministic outcome of one numerical submission."""

    submitted_answer: float | None
    is_valid: bool
    is_correct: bool | None
    message: str | None = None


@dataclass(frozen=True)
class PracticeAttempt:
    """A session-only learner attempt; it has no persistence boundary."""

    attempt_id: str
    card_id: str
    primary_domain: str
    financial_skill: str
    calculation_method: str
    difficulty: str
    submitted_answer: float
    correct_answer: float
    is_correct: bool
    first_attempt: bool
    timestamp: datetime


@lru_cache(maxsize=1)
def load_practice_cards() -> tuple[DrillCard, ...]:
    """Load the reviewed committed bank exactly once per Python process."""

    return load_cards(DRILL_BANK_PATH)


def filter_cards(
    cards: Iterable[DrillCard],
    *,
    primary_domain: DrillDomain | None = None,
    financial_skill: FinancialSkill | None = None,
    difficulty: DrillDifficulty | None = None,
) -> tuple[DrillCard, ...]:
    """Return cards that satisfy every selected filter, in bank order."""

    return tuple(
        card
        for card in cards
        if (primary_domain is None or card.primary_domain is primary_domain)
        and (financial_skill is None or card.financial_skill is financial_skill)
        and (difficulty is None or card.difficulty is difficulty)
    )


def check_answer(card: DrillCard, submitted_answer: object) -> AnswerCheck:
    """Check a finite number against the card's own stored tolerance."""

    if isinstance(submitted_answer, bool) or not isinstance(submitted_answer, (int, float)):
        return AnswerCheck(None, False, None, "Enter a numerical answer before submitting.")
    numeric_answer = float(submitted_answer)
    if not isfinite(numeric_answer):
        return AnswerCheck(None, False, None, "Enter a finite numerical answer before submitting.")
    return AnswerCheck(
        submitted_answer=numeric_answer,
        is_valid=True,
        is_correct=abs(numeric_answer - card.correct_answer) <= card.tolerance,
    )


def create_attempt(
    card: DrillCard,
    check: AnswerCheck,
    existing_attempts: Iterable[PracticeAttempt],
    *,
    timestamp: datetime | None = None,
) -> PracticeAttempt:
    """Create an auditable in-memory record for a valid checked answer."""

    if not check.is_valid or check.submitted_answer is None or check.is_correct is None:
        raise ValueError("A valid checked answer is required to create an attempt.")
    attempts = tuple(existing_attempts)
    return PracticeAttempt(
        attempt_id=str(uuid4()),
        card_id=card.card_id,
        primary_domain=card.primary_domain.value,
        financial_skill=card.financial_skill.value,
        calculation_method=card.calculation_method.value,
        difficulty=card.difficulty.value,
        submitted_answer=check.submitted_answer,
        correct_answer=card.correct_answer,
        is_correct=check.is_correct,
        first_attempt=not any(attempt.card_id == card.card_id for attempt in attempts),
        timestamp=timestamp or datetime.now(UTC),
    )


def next_card(cards: tuple[DrillCard, ...], current_card_id: str | None) -> DrillCard | None:
    """Select the next stable bank-order card and wrap after the final card."""

    if not cards:
        return None
    if current_card_id is None:
        return cards[0]
    for index, card in enumerate(cards):
        if card.card_id == current_card_id:
            return cards[(index + 1) % len(cards)]
    return cards[0]
