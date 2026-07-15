"""Offline validation for the committed deterministic FinQA drill bank."""

from __future__ import annotations

from dataclasses import replace
import os
from pathlib import Path
import subprocess
import sys

import pytest

from finance_director_coach.drills import (
    DrillDomain,
    execute_finqa_program,
    load_cards,
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
        assert card.skill
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
        assert card.unit
        assert card.tolerance > 0


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
