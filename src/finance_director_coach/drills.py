"""Deterministic models and import helpers for FinanceOS calculation drills.

This module deliberately has no application UI or network dependency.  It owns
the immutable card schema and the small, auditable FinQA program interpreter
used to verify curated source material during generation and tests.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
import json
from pathlib import Path
import re
from typing import Any, Iterable


class DrillDomain(StrEnum):
    """The initial FinanceOS financial-drill domains."""

    PROFIT_AND_LOSS = "P&L"
    BALANCE_SHEET = "Balance Sheet"
    CASH_FLOW = "Cash Flow"
    WORKING_CAPITAL = "Working Capital"
    LIQUIDITY_AND_TREASURY = "Liquidity & Treasury"
    TAX = "Tax"
    COMMERCIAL_FINANCE = "Commercial Finance"
    INVESTMENT_AND_VALUATION = "Investment & Valuation"


class DrillSkill(StrEnum):
    """Constrained calculation skills represented by the first bank."""

    ABSOLUTE_CHANGE = "absolute_change"
    AVERAGE = "average"
    MULTIPLICATION = "multiplication"
    PERCENTAGE_CHANGE = "percentage_change"
    RATIO = "ratio"
    TOTAL = "total"


class DrillDifficulty(StrEnum):
    FOUNDATIONAL = "foundational"
    INTERMEDIATE = "intermediate"


class AnswerType(StrEnum):
    NUMBER = "number"
    PERCENTAGE = "percentage"
    CURRENCY = "currency"


@dataclass(frozen=True)
class DrillCard:
    """An immutable, learner-ready, source-attributed numerical drill."""

    card_id: str
    source_dataset: str
    source_item_id: str
    source_reference: str
    primary_domain: DrillDomain
    secondary_domains: tuple[DrillDomain, ...]
    skill: DrillSkill
    difficulty: DrillDifficulty
    calculation_steps: int
    question: str
    visible_context: tuple[str, ...]
    visible_table: tuple[tuple[str, ...], ...]
    answer_type: AnswerType
    correct_answer: float
    unit: str
    tolerance: float
    formula: str
    worked_solution: str
    why_it_matters: str
    source_attribution: str
    license: str
    source_answer: str
    source_program: str
    rounding: str

    def validate(self) -> None:
        """Raise a clear error when a card cannot safely enter the bank."""

        if not self.card_id.startswith("FINQA-"):
            raise ValueError("card_id must start with 'FINQA-'")
        if not self.source_dataset or not self.source_item_id or not self.source_reference:
            raise ValueError("source dataset, item ID, and reference are required")
        if not self.question.strip() or not self.visible_context:
            raise ValueError("question and visible context are required")
        if not 1 <= self.calculation_steps <= 2:
            raise ValueError("calculation_steps must be one or two")
        if not self.unit.strip() or self.tolerance <= 0:
            raise ValueError("unit and a positive tolerance are required")
        if not self.formula or not self.worked_solution or not self.why_it_matters:
            raise ValueError("formula, worked solution, and why-it-matters are required")
        if not self.source_attribution or self.license != "MIT":
            raise ValueError("FinQA attribution and MIT licence metadata are required")
        if not self.source_program:
            raise ValueError("source program is required for answer verification")

    def as_json(self) -> dict[str, Any]:
        value = asdict(self)
        value["primary_domain"] = self.primary_domain.value
        value["secondary_domains"] = [domain.value for domain in self.secondary_domains]
        value["skill"] = self.skill.value
        value["difficulty"] = self.difficulty.value
        value["answer_type"] = self.answer_type.value
        value["visible_context"] = list(self.visible_context)
        value["visible_table"] = [list(row) for row in self.visible_table]
        return value


_PROGRAM_STEP = re.compile(r"(add|subtract|multiply|divide|exp)\(([^,]+), ([^)]+)\)")


def numeric_value(value: str | float | int) -> float:
    """Parse FinQA's numeric literals, retaining parenthesised negatives."""

    text = str(value).strip().lower().replace("$", "").replace(",", "")
    text = text.replace("const_", "")
    if text.endswith("%"):
        text = text[:-1]
    negative = text.startswith("(") and text.endswith(")")
    text = text.strip("()").strip()
    try:
        parsed = float(text)
    except ValueError as error:
        raise ValueError(f"unsupported FinQA number: {value!r}") from error
    return -parsed if negative else parsed


def execute_finqa_program(program: str) -> float:
    """Execute the supported arithmetic subset of a FinQA program.

    The curated bank excludes table aggregations and comparison programs.  The
    original FinQA program remains on every card so this calculation is fully
    deterministic and independently testable.
    """

    matches = list(_PROGRAM_STEP.finditer(program))
    if not matches:
        raise ValueError("program contains no supported arithmetic steps")
    reconstructed = ", ".join(match.group(0) for match in matches)
    if reconstructed != program.strip():
        raise ValueError(f"unsupported FinQA program: {program!r}")

    results: list[float] = []
    for match in matches:
        operation, first, second = match.groups()

        def resolve(argument: str) -> float:
            argument = argument.strip()
            if argument.startswith("#"):
                index = int(argument[1:])
                try:
                    return results[index]
                except IndexError as error:
                    raise ValueError(f"program references unknown result {argument}") from error
            return numeric_value(argument)

        left, right = resolve(first), resolve(second)
        if operation == "add":
            result = left + right
        elif operation == "subtract":
            result = left - right
        elif operation == "multiply":
            result = left * right
        elif operation == "divide":
            if right == 0:
                raise ValueError("FinQA program divides by zero")
            result = left / right
        else:
            result = left**right
        results.append(result)
    return round(results[-1], 5)


def card_from_json(value: dict[str, Any]) -> DrillCard:
    """Deserialize and validate one card from the reviewable JSON bank."""

    card = DrillCard(
        card_id=value["card_id"],
        source_dataset=value["source_dataset"],
        source_item_id=value["source_item_id"],
        source_reference=value["source_reference"],
        primary_domain=DrillDomain(value["primary_domain"]),
        secondary_domains=tuple(DrillDomain(domain) for domain in value["secondary_domains"]),
        skill=DrillSkill(value["skill"]),
        difficulty=DrillDifficulty(value["difficulty"]),
        calculation_steps=int(value["calculation_steps"]),
        question=value["question"],
        visible_context=tuple(value["visible_context"]),
        visible_table=tuple(tuple(row) for row in value["visible_table"]),
        answer_type=AnswerType(value["answer_type"]),
        correct_answer=float(value["correct_answer"]),
        unit=value["unit"],
        tolerance=float(value["tolerance"]),
        formula=value["formula"],
        worked_solution=value["worked_solution"],
        why_it_matters=value["why_it_matters"],
        source_attribution=value["source_attribution"],
        license=value["license"],
        source_answer=value["source_answer"],
        source_program=value["source_program"],
        rounding=value["rounding"],
    )
    card.validate()
    return card


def load_cards(path: Path) -> tuple[DrillCard, ...]:
    """Load the committed card bank without downloading or transforming FinQA."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    cards = tuple(card_from_json(value) for value in payload["cards"])
    if len(cards) != 100:
        raise ValueError("FinQA v1 must contain exactly 100 cards")
    return cards


def validate_unique(cards: Iterable[DrillCard]) -> None:
    """Verify identifiers, FinQA source IDs, and exact question text are unique."""

    cards = tuple(cards)
    for label, values in (
        ("card IDs", [card.card_id for card in cards]),
        ("source IDs", [card.source_item_id for card in cards]),
        ("questions", [card.question.casefold() for card in cards]),
    ):
        if len(values) != len(set(values)):
            raise ValueError(f"duplicate {label} in FinQA bank")
