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


class FinancialSkill(StrEnum):
    """The finance concept a learner practises, separate from the arithmetic."""

    ASSET_MOVEMENT = "asset_movement"
    BOOK_VALUE = "book_value"
    CAPITALIZED_EXPENDITURE = "capitalized_expenditure"
    CUSTOMER_OR_SEGMENT_PERFORMANCE = "customer_or_segment_performance"
    DEBT_MOVEMENT = "debt_movement"
    EFFECTIVE_TAX_RATE = "effective_tax_rate"
    EARNINGS_PER_SHARE = "earnings_per_share"
    EQUITY_MOVEMENT = "equity_movement"
    FAIR_VALUE = "fair_value"
    FINANCING_CASH_FLOW = "financing_cash_flow"
    FREE_CASH_FLOW = "free_cash_flow"
    GROSS_MARGIN = "gross_margin"
    INTEREST_EXPENSE = "interest_expense"
    INVENTORY_MOVEMENT = "inventory_movement"
    INVESTING_CASH_FLOW = "investing_cash_flow"
    INVESTMENT_RETURN = "investment_return"
    LEASE_EXPENSE = "lease_expense"
    LIABILITY_MOVEMENT = "liability_movement"
    LIQUIDITY = "liquidity"
    NET_INCOME = "net_income"
    OPERATING_CASH_FLOW = "operating_cash_flow"
    OPERATING_EXPENSE = "operating_expense"
    OPERATING_MARGIN = "operating_margin"
    RECEIVABLES_MOVEMENT = "receivables_movement"
    REVENUE_GROWTH = "revenue_growth"
    SHARE_REPURCHASE = "share_repurchase"
    SHARE_COUNT = "share_count"
    SHARE_PRICE = "share_price"
    TAX_CASH_PAYMENT = "tax_cash_payment"
    TAX_EXPENSE = "tax_expense"
    WORKING_CAPITAL_MOVEMENT = "working_capital_movement"


class CalculationMethod(StrEnum):
    """The deterministic calculation method used by a card."""

    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    RATIO = "ratio"
    PERCENTAGE_CHANGE = "percentage_change"
    PERCENTAGE_POINT_CHANGE = "percentage_point_change"
    AVERAGE = "average"
    MULTI_STEP_RECONCILIATION = "multi_step_reconciliation"


class DrillDifficulty(StrEnum):
    FOUNDATIONAL = "foundational"
    INTERMEDIATE = "intermediate"


class UnitDimension(StrEnum):
    CURRENCY = "currency"
    NUMBER = "number"
    PERCENTAGE = "percentage"
    PERCENTAGE_POINTS = "percentage_points"
    SHARES = "shares"
    YEARS = "years"
    PER_SHARE_AMOUNT = "per_share_amount"
    RATIO = "ratio"


class UnitScale(StrEnum):
    UNIT = "unit"
    THOUSAND = "thousand"
    MILLION = "million"
    BILLION = "billion"


_SCALE_FACTORS = {
    UnitScale.UNIT: 1.0,
    UnitScale.THOUSAND: 1_000.0,
    UnitScale.MILLION: 1_000_000.0,
    UnitScale.BILLION: 1_000_000_000.0,
}


def normalize_scale(value: float, source_scale: UnitScale, target_scale: UnitScale) -> float:
    """Convert a reviewed same-dimension value between explicit finance scales."""

    return value * _SCALE_FACTORS[source_scale] / _SCALE_FACTORS[target_scale]


@dataclass(frozen=True)
class NormalizedOperand:
    """A program literal represented in its reviewed common finance unit."""

    raw_value: float
    normalized_value: float
    dimension: UnitDimension
    scale: UnitScale
    is_constant: bool


@dataclass(frozen=True)
class DrillCard:
    """An immutable, learner-ready, source-attributed numerical drill."""

    card_id: str
    source_dataset: str
    source_item_id: str
    source_reference: str
    primary_domain: DrillDomain
    secondary_domains: tuple[DrillDomain, ...]
    financial_skill: FinancialSkill
    calculation_method: CalculationMethod
    difficulty: DrillDifficulty
    calculation_steps: int
    question: str
    visible_context: tuple[str, ...]
    visible_table: tuple[tuple[str, ...], ...]
    correct_answer: float
    unit: str
    unit_dimension: UnitDimension
    unit_scale: UnitScale
    normalized_operands: tuple[NormalizedOperand, ...]
    tolerance: float
    formula: str
    worked_solution: str
    why_it_matters: str
    source_attribution: str
    license: str
    source_answer: str
    source_program: str
    rounding: str
    learner_question: str
    learner_context: tuple[str, ...]
    learner_table: tuple[tuple[str, ...], ...]
    worked_calculation: str
    review_status: str
    reviewed_for_units: bool
    reviewed_for_semantics: bool
    reviewed_for_domain: bool
    reviewed_for_learner_clarity: bool

    def validate(self) -> None:
        """Raise a clear error when a card cannot safely enter the bank."""

        if not self.card_id.startswith("FINQA-"):
            raise ValueError("card_id must start with 'FINQA-'")
        if not self.source_dataset or not self.source_item_id or not self.source_reference:
            raise ValueError("source dataset, item ID, and reference are required")
        if not self.question.strip() or not self.visible_context or not self.learner_question.strip():
            raise ValueError("source and learner questions with visible context are required")
        if not 1 <= self.calculation_steps <= 2:
            raise ValueError("calculation_steps must be one or two")
        if not self.unit.strip() or self.tolerance <= 0 or not self.normalized_operands:
            raise ValueError("unit and a positive tolerance are required")
        if not self.formula or not self.worked_solution or not self.why_it_matters:
            raise ValueError("formula, worked solution, and why-it-matters are required")
        if not self.source_attribution or self.license != "MIT":
            raise ValueError("FinQA attribution and MIT licence metadata are required")
        if not self.source_program:
            raise ValueError("source program is required for answer verification")
        if self.review_status != "approved" or not all(
            (self.reviewed_for_units, self.reviewed_for_semantics, self.reviewed_for_domain, self.reviewed_for_learner_clarity)
        ):
            raise ValueError("all individual-review fields must be approved")
        forbidden = ("add(", "subtract(", "multiply(", "divide(", "#0", "2019s", "201c", "201d")
        learner_text = " ".join(self.learner_context + (self.learner_question, self.worked_calculation) + tuple(" ".join(row) for row in self.learner_table))
        if any(token in learner_text.casefold() for token in forbidden):
            raise ValueError("learner-facing text contains source-program or OCR artefacts")
        if any("<" in cell or ">" in cell for row in self.learner_table for cell in row):
            raise ValueError("learner table contains HTML-like markup")

    def as_json(self) -> dict[str, Any]:
        value = asdict(self)
        value["primary_domain"] = self.primary_domain.value
        value["secondary_domains"] = [domain.value for domain in self.secondary_domains]
        value["financial_skill"] = self.financial_skill.value
        value["calculation_method"] = self.calculation_method.value
        value["difficulty"] = self.difficulty.value
        value["unit_dimension"] = self.unit_dimension.value
        value["unit_scale"] = self.unit_scale.value
        value["normalized_operands"] = [
            {
                "raw_value": operand.raw_value,
                "normalized_value": operand.normalized_value,
                "dimension": operand.dimension.value,
                "scale": operand.scale.value,
                "is_constant": operand.is_constant,
            }
            for operand in self.normalized_operands
        ]
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
        financial_skill=FinancialSkill(value["financial_skill"]),
        calculation_method=CalculationMethod(value["calculation_method"]),
        difficulty=DrillDifficulty(value["difficulty"]),
        calculation_steps=int(value["calculation_steps"]),
        question=value["question"],
        visible_context=tuple(value["visible_context"]),
        visible_table=tuple(tuple(row) for row in value["visible_table"]),
        correct_answer=float(value["correct_answer"]),
        unit=value["unit"],
        unit_dimension=UnitDimension(value["unit_dimension"]),
        unit_scale=UnitScale(value["unit_scale"]),
        normalized_operands=tuple(
            NormalizedOperand(
                raw_value=float(operand["raw_value"]),
                normalized_value=float(operand["normalized_value"]),
                dimension=UnitDimension(operand["dimension"]),
                scale=UnitScale(operand["scale"]),
                is_constant=bool(operand["is_constant"]),
            )
            for operand in value["normalized_operands"]
        ),
        tolerance=float(value["tolerance"]),
        formula=value["formula"],
        worked_solution=value["worked_solution"],
        why_it_matters=value["why_it_matters"],
        source_attribution=value["source_attribution"],
        license=value["license"],
        source_answer=value["source_answer"],
        source_program=value["source_program"],
        rounding=value["rounding"],
        learner_question=value["learner_question"],
        learner_context=tuple(value["learner_context"]),
        learner_table=tuple(tuple(row) for row in value["learner_table"]),
        worked_calculation=value["worked_calculation"],
        review_status=value["review_status"],
        reviewed_for_units=bool(value["reviewed_for_units"]),
        reviewed_for_semantics=bool(value["reviewed_for_semantics"]),
        reviewed_for_domain=bool(value["reviewed_for_domain"]),
        reviewed_for_learner_clarity=bool(value["reviewed_for_learner_clarity"]),
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
