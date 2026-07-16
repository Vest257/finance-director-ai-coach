"""Offline validation for the committed deterministic FinQA drill bank."""

from __future__ import annotations

from dataclasses import replace
import json
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
CURATION = REPOSITORY_ROOT / "data" / "drills" / "finqa_v1_curation.json"
REVIEWED_CARD_IDS = {
    "FINQA-009A7ECEA253": ("HWM/2016/page_79.pdf-2", "subtract(1801, 298)", 1503.0),
    "FINQA-434882BEB46E": ("PNC/2012/page_68.pdf-3", "add(81, 120), divide(#0, const_2)", 100.5),
    "FINQA-53859C0DBA1C": ("RCL/2012/page_80.pdf-2", "add(204866, 218883), divide(#0, const_2)", 211874.5),
    "FINQA-5EBB6C33025F": ("HWM/2015/page_123.pdf-2", "subtract(37, 6)", 31.0),
}


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
        assert all("<" not in cell and ">" not in cell for row in card.learner_table for cell in row)


def test_taxonomy_regressions_for_cash_flow_effective_rate_and_share_repurchase(cards) -> None:
    by_source = {card.source_item_id: card for card in cards}
    cash_flow = by_source["UNP/2009/page_38.pdf-1"]
    assert cash_flow.financial_skill.value == "operating_cash_flow"
    assert cash_flow.financial_skill.value != "operating_expense"
    effective_rate = by_source["APD/2019/page_39.pdf-2"]
    assert effective_rate.calculation_method == CalculationMethod.PERCENTAGE_POINT_CHANGE
    assert effective_rate.unit_dimension == UnitDimension.PERCENTAGE_POINTS
    assert effective_rate.unit == "percentage points"
    assert effective_rate.learner_context == ("The adjusted effective tax rate was 19.4% in fiscal year 2019 and 18.6% in fiscal year 2018.",)
    assert effective_rate.worked_calculation == "19.4% - 18.6% = 0.8 percentage points"
    share_repurchase = by_source["PPG/2012/page_29.pdf-2"]
    assert share_repurchase.primary_domain == DrillDomain.INVESTMENT_AND_VALUATION
    assert share_repurchase.secondary_domains == (DrillDomain.BALANCE_SHEET,)
    assert share_repurchase.financial_skill.value == "share_repurchase"


def test_remaining_cash_flow_loan_balance_constants_and_table_heading_regressions(cards) -> None:
    by_source = {card.source_item_id: card for card in cards}
    for card in cards:
        question = card.learner_question.casefold()
        if "operating cash flow" in question or "cash provided by operating activities" in question:
            assert card.primary_domain == DrillDomain.CASH_FLOW
            assert card.financial_skill.value == "operating_cash_flow"
    unp = by_source["UNP/2011/page_35.pdf-1"]
    assert unp.primary_domain == DrillDomain.CASH_FLOW
    assert unp.secondary_domains == (DrillDomain.WORKING_CAPITAL,)
    assert unp.financial_skill.value == "operating_cash_flow"
    assert "USD million" in unp.learner_question
    assert unp.learner_table[0][0] == "Cash Flows — USD million"
    loans_held_for_sale = by_source["PNC/2012/page_68.pdf-3"]
    assert loans_held_for_sale.primary_domain == DrillDomain.BALANCE_SHEET
    assert loans_held_for_sale.financial_skill.value == "asset_movement"
    assert loans_held_for_sale.unit_dimension == UnitDimension.CURRENCY
    assert loans_held_for_sale.unit == "USD million"
    constant = next(operand for operand in loans_held_for_sale.normalized_operands if operand.is_constant)
    assert constant.raw_value == 2.0
    assert constant.normalized_value == 2.0
    assert constant.dimension == UnitDimension.NUMBER
    assert constant.scale == UnitScale.UNIT
    for card in cards:
        for cell in (cell for row in card.learner_table for cell in row):
            assert "cash flowsmillions" not in cell.casefold()


def test_reviewed_cards_preserve_provenance_and_use_clear_foundational_content(cards) -> None:
    by_id = {card.card_id: card for card in cards}
    assert REVIEWED_CARD_IDS.keys() <= by_id.keys()
    for card_id, (source_item_id, source_program, correct_answer) in REVIEWED_CARD_IDS.items():
        card = by_id[card_id]
        assert card.source_item_id == source_item_id
        assert card.source_program == source_program
        assert card.formula == source_program
        assert card.correct_answer == correct_answer
        assert card.tolerance == 0.00001
        assert card.difficulty.value == "foundational"

    goodwill = by_id["FINQA-009A7ECEA253"]
    assert goodwill.worked_calculation == "1,801 − 298 = 1,503 USD million."
    assert goodwill.unit == "USD million"
    assert goodwill.unit_scale == UnitScale.MILLION
    assert all(name in goodwill.learner_context[0] for name in ("Arconic", "Firth Rixson", "RTI"))
    assert "acquired" not in goodwill.learner_context[0].casefold()

    loans = by_id["FINQA-434882BEB46E"]
    assert loans.worked_calculation == "(81 + 120) ÷ 2 = 100.5 USD million."
    assert loans.unit == "USD million"
    assert loans.unit_scale == UnitScale.MILLION
    assert loans.learner_table[1][0] == "Other loans held for sale"
    assert "loans held for sale table" not in " ".join(loans.learner_context).casefold()
    assert "another reporting date" in loans.why_it_matters

    intangibles = by_id["FINQA-53859C0DBA1C"]
    assert intangibles.worked_calculation == "(204,866 + 218,883) ÷ 2 = 211,874.5 USD thousand."
    assert intangibles.unit == "USD thousand"
    assert intangibles.unit_scale == UnitScale.THOUSAND
    assert intangibles.learner_table[1][0] == "Intangible assets"
    assert "intangible assets intangible assets" not in " ".join(intangibles.learner_context).casefold()
    assert "USD 211.9 million" in intangibles.why_it_matters

    useful_lives = by_id["FINQA-5EBB6C33025F"]
    assert useful_lives.worked_calculation == "37 − 6 = 31 years."
    assert useful_lives.unit == "years"
    assert useful_lives.calculation_method == CalculationMethod.SUBTRACTION
    assert useful_lives.learner_table[0] == ("Asset class", "Weighted-average useful life")
    assert "variation" not in useful_lives.learner_question.casefold()
    assert "longer than" in useful_lives.learner_question
    assert "amortization" in useful_lives.why_it_matters.casefold()


def test_approved_cards_are_explicitly_curated_and_auto_entries_remain_pending(cards) -> None:
    curation = json.loads(CURATION.read_text(encoding="utf-8"))["cards"]
    curated_ids = {entry["source_item_id"] for entry in curation if entry["review_status"] == "approved"}
    assert {card.source_item_id for card in cards} == curated_ids
    sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))
    import import_finqa

    source_record = next(record for record in json.loads(SOURCE_FIXTURE.read_text(encoding="utf-8"))["records"] if record["id"] == "UNP/2009/page_38.pdf-1")
    automatic = import_finqa._auto_curation_entry(source_record, DrillDomain.CASH_FLOW)
    assert automatic["review_status"] == "pending"
    assert not any(automatic[field] for field in ("reviewed_for_units", "reviewed_for_semantics", "reviewed_for_domain", "reviewed_for_learner_clarity"))
    pending_curation = {entry["source_item_id"]: dict(entry) for entry in curation}
    pending_curation[source_record["id"]] = automatic
    fixture_records = json.loads(SOURCE_FIXTURE.read_text(encoding="utf-8"))["records"]
    with pytest.raises(ValueError, match="individual-review"):
        import_finqa.curate(fixture_records, pending_curation)


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
