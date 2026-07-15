"""Offline validation for the committed deterministic FinQA drill bank."""

from __future__ import annotations

from dataclasses import replace
import os
from pathlib import Path
import subprocess
import sys

import pytest

from finance_director_coach.drills import (
    CalculationMethod,
    DrillDomain,
    FinancialSkill,
    UnitDimension,
    UnitScale,
    execute_finqa_program,
    load_cards,
    normalize_scale,
    numeric_value,
    validate_unique,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CARD_BANK = REPOSITORY_ROOT / "data" / "drills" / "finqa_cards_v1.json"
SOURCE_FIXTURE = REPOSITORY_ROOT / "tests" / "fixtures" / "finqa_v1_selected_records.json"


@pytest.fixture(scope="module")
def cards():
    return load_cards(CARD_BANK)


def test_bank_contains_exactly_100_unique_stable_cards(cards) -> None:
    assert len(cards) == 100
    validate_unique(cards)
    assert [card.card_id for card in cards] == sorted(card.card_id for card in cards)


def test_every_card_validates_with_required_taxonomy_and_provenance(cards) -> None:
    for card in cards:
        card.validate()
        assert isinstance(card.primary_domain, DrillDomain)
        assert isinstance(card.financial_skill, FinancialSkill)
        assert isinstance(card.calculation_method, CalculationMethod)
        assert card.source_dataset == "FinQA"
        assert card.source_item_id
        assert card.source_reference
        assert card.source_attribution
        assert card.license == "MIT"


def test_every_source_program_recomputes_and_reconciles(cards) -> None:
    for card in cards:
        recomputed = execute_finqa_program(card.source_program)
        source_answer = numeric_value(card.source_answer)
        assert recomputed == pytest.approx(card.correct_answer, abs=card.tolerance)
        assert source_answer == pytest.approx(recomputed, abs=card.tolerance)
        assert 1 <= card.calculation_steps <= 2
        assert card.unit and card.normalized_operands
        assert card.tolerance > 0


def test_units_are_normalized_and_operands_are_compatible(cards) -> None:
    for card in cards:
        for operand in card.normalized_operands:
            if not operand.is_constant:
                assert operand.dimension == card.unit_dimension
                assert operand.scale == card.unit_scale
        evidence = " ".join(card.visible_context + card.learner_context).casefold()
        if card.unit_dimension == UnitDimension.CURRENCY and "million" in evidence:
            assert card.unit_scale == UnitScale.MILLION


def test_scale_conversion_and_known_unit_regressions(cards) -> None:
    assert normalize_scale(361, UnitScale.MILLION, UnitScale.UNIT) == 361_000_000
    assert normalize_scale(1_000, UnitScale.THOUSAND, UnitScale.MILLION) == 1
    by_source = {card.source_item_id: card for card in cards}
    for source_id in ("PNC/2011/page_44.pdf-1", "DISH/2013/page_138.pdf-2", "DRE/2016/page_59.pdf-2"):
        card = by_source[source_id]
        assert card.unit_dimension == UnitDimension.CURRENCY
        assert card.unit_scale == UnitScale.MILLION
        assert card.unit == "USD million"
    assert "STZ/2006/page_68.pdf-2" not in by_source
    assert "ETR/2016/page_144.pdf-1" not in by_source
    assert "RSG/2008/page_141.pdf-2" not in by_source


def test_curation_and_learner_text_are_complete(cards) -> None:
    assert any(card.secondary_domains for card in cards)
    assert any(card.calculation_method == CalculationMethod.PERCENTAGE_POINT_CHANGE for card in cards)
    prohibited = ("add(", "subtract(", "multiply(", "divide(", "#0", "2019s", "2019's", "201c", "201d", "\\?")
    for card in cards:
        assert card.review_status == "approved"
        assert all((card.reviewed_for_units, card.reviewed_for_semantics, card.reviewed_for_domain, card.reviewed_for_learner_clarity))
        learner_text = " ".join(card.learner_context + (card.learner_question, card.worked_calculation) + tuple(" ".join(row) for row in card.learner_table)).casefold()
        assert not any(token in learner_text for token in prohibited)


def test_generated_bank_is_deterministic_and_requires_no_network(tmp_path: Path) -> None:
    output = tmp_path / "finqa_cards_v1.json"
    report = tmp_path / "finqa-import-report.md"
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(REPOSITORY_ROOT / "src")
    subprocess.run(
        [
            sys.executable,
            "scripts/import_finqa.py",
            "--source",
            str(SOURCE_FIXTURE),
            "--output",
            str(output),
            "--report",
            str(report),
        ],
        cwd=REPOSITORY_ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    assert output.read_bytes() == CARD_BANK.read_bytes()
    assert report.exists()


def test_invalid_card_fails_validation_clearly(cards) -> None:
    invalid = replace(cards[0], calculation_steps=3)
    with pytest.raises(ValueError, match="one or two"):
        invalid.validate()
