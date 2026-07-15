"""Generate the deterministic FinanceOS FinQA fast-drill content bank.

Use an upstream FinQA dataset directory for a full curation pass, or the
committed selected-record fixture for offline CI regeneration.  This script is
build tooling; the application never calls it at runtime.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable

from finance_director_coach.drills import (
    AnswerType,
    DrillCard,
    DrillDifficulty,
    DrillDomain,
    DrillSkill,
    execute_finqa_program,
    numeric_value,
)


SEED = "financeos-finqa-v1-2026-07-15"
SOURCE_DATASET = "FinQA"
SOURCE_ATTRIBUTION = (
    "Chen et al. (2021), FinQA: A Dataset of Numerical Reasoning over Financial Data; "
    "https://github.com/czyssrs/FinQA"
)
LICENSE = "MIT"
DATA_FILES = ("train.json", "dev.json", "test.json")
DOMAIN_TARGETS: dict[DrillDomain, int] = {
    DrillDomain.PROFIT_AND_LOSS: 20,
    DrillDomain.BALANCE_SHEET: 15,
    DrillDomain.CASH_FLOW: 10,
    DrillDomain.WORKING_CAPITAL: 15,
    DrillDomain.LIQUIDITY_AND_TREASURY: 15,
    DrillDomain.TAX: 10,
    DrillDomain.COMMERCIAL_FINANCE: 5,
    DrillDomain.INVESTMENT_AND_VALUATION: 10,
}


def _normalise_question(question: str) -> str:
    return " ".join(question.casefold().split())


def _stable_key(record: dict[str, Any]) -> tuple[str, str]:
    digest = hashlib.sha256(f"{SEED}:{record['id']}".encode()).hexdigest()
    return digest, record["id"]


def _question_domain(question: str) -> DrillDomain | None:
    text = question.casefold()
    classifications: tuple[tuple[DrillDomain, tuple[str, ...]], ...] = (
        (DrillDomain.TAX, ("tax",)),
        (DrillDomain.WORKING_CAPITAL, ("working capital", "receivable", "payable", "inventory", "collection period")),
        (DrillDomain.CASH_FLOW, ("cash flow", "cash provided", "cash used", "operating activities", "free cash")),
        (DrillDomain.LIQUIDITY_AND_TREASURY, ("liquidity", "cash balance", "cash and cash", "debt", "borrow", "interest", "credit facility", "maturit", "loan", "dividend")),
        (DrillDomain.PROFIT_AND_LOSS, ("revenue", "sales", "gross", "income", "profit", "expense", "cost", "margin", "earning", "ebitda")),
        (DrillDomain.BALANCE_SHEET, ("balance sheet", "asset", "liabilit", "equity", "goodwill", "property", "book value")),
        (DrillDomain.INVESTMENT_AND_VALUATION, ("fair value", "investment", "market value", "share", "stock", "acquisition", "valuation", "return")),
        (DrillDomain.COMMERCIAL_FINANCE, ("customer", "segment", "backlog", "contract", "unit", "product", "booking", "subscriber")),
    )
    for domain, keywords in classifications:
        if domain == DrillDomain.TAX and "tax" in text and ("pre-tax" in text or "pre tax" in text) and text.count("tax") == 1:
            continue
        if any(keyword in text for keyword in keywords):
            return domain
    return None


def _secondary_domains(question: str, primary: DrillDomain) -> tuple[DrillDomain, ...]:
    possible = _question_domain(question)
    return () if possible is None or possible == primary else (possible,)


def _visible_evidence(record: dict[str, Any]) -> tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]:
    evidence = record["qa"].get("gold_inds", {})
    context: list[str] = []
    table_rows: list[tuple[str, ...]] = []
    table = record.get("table_ori", [])
    table_indices: list[int] = []
    for key in sorted(evidence, key=lambda value: (value.split("_", 1)[0], int(value.split("_", 1)[1]))):
        text = evidence[key]
        if key.startswith("text_"):
            context.append(str(text).strip())
        elif key.startswith("table_"):
            table_indices.append(int(key.split("_", 1)[1]))
    if table_indices:
        table_rows.append(tuple(str(cell) for cell in table[0]))
        for index in sorted(set(table_indices)):
            if 0 <= index < len(table):
                table_rows.append(tuple(str(cell) for cell in table[index]))
    return tuple(context), tuple(table_rows)


def _infer_unit(record: dict[str, Any], context: tuple[str, ...], table: tuple[tuple[str, ...], ...]) -> tuple[str, AnswerType] | None:
    answer = record["qa"]["answer"]
    evidence = " ".join(context + tuple(" ".join(row) for row in table)).casefold()
    question = record["qa"]["question"].casefold()
    text = f"{question} {evidence} {answer.casefold()}"
    if "in millions" in question and "in billions" in question:
        return None
    if "percentage point" in question or "percentage" in question:
        return "percent", AnswerType.PERCENTAGE
    if "%" in answer:
        return "percent", AnswerType.PERCENTAGE
    if "price per share" in question or "cost per share" in question:
        return "USD per share", AnswerType.CURRENCY
    if "ratio of" in question or "ratio between" in question:
        return "ratio", AnswerType.NUMBER
    if "share" in question and re.search(r"\b(in |\()millions?\b", question):
        return "millions of shares", AnswerType.NUMBER
    if "$ million" in text or "millions of dollars" in text:
        return "USD millions", AnswerType.CURRENCY
    if re.search(r"\b(in |\()millions?\b", text):
        return "millions", AnswerType.CURRENCY if "$" in text or "usd" in text else AnswerType.NUMBER
    if re.search(r"\b(in |\()billions?\b", text):
        return "billions", AnswerType.CURRENCY if "$" in text or "usd" in text else AnswerType.NUMBER
    if re.search(r"\b(in |\()thousands?\b", text):
        return "thousands", AnswerType.CURRENCY if "$" in text or "usd" in text else AnswerType.NUMBER
    if "$" in text or "dollar" in text or "us$" in text:
        return "USD", AnswerType.CURRENCY
    if "years" in text or "year" in text:
        return "years", AnswerType.NUMBER
    if "shares" in text or "share" in text:
        return "shares", AnswerType.NUMBER
    if "percent" in text or "percentage" in text or "rate" in text:
        return "percent", AnswerType.PERCENTAGE
    return None


def _skill(question: str, source_answer: str, program: str) -> DrillSkill:
    text = question.casefold()
    if "%" in source_answer or "percent" in text or "margin" in text:
        return DrillSkill.PERCENTAGE_CHANGE
    if "average" in text:
        return DrillSkill.AVERAGE
    if "total" in text or "sum" in text:
        return DrillSkill.TOTAL
    if "multiply(" in program:
        return DrillSkill.MULTIPLICATION
    if "divide(" in program:
        return DrillSkill.RATIO
    return DrillSkill.ABSOLUTE_CHANGE


def _why_it_matters(domain: DrillDomain) -> str:
    statements = {
        DrillDomain.PROFIT_AND_LOSS: "This helps finance leaders quantify earnings movement before explaining its operating drivers.",
        DrillDomain.BALANCE_SHEET: "This helps finance leaders understand changes in the resources and obligations reported on the balance sheet.",
        DrillDomain.CASH_FLOW: "This helps finance leaders separate cash movement from the profit measures that may not move in step with it.",
        DrillDomain.WORKING_CAPITAL: "This helps finance leaders translate operational balances into cash and funding implications.",
        DrillDomain.LIQUIDITY_AND_TREASURY: "This helps finance leaders assess near-term funding, cash, and financing movements.",
        DrillDomain.TAX: "This helps finance leaders quantify how tax balances or rates affect reported financial results.",
        DrillDomain.COMMERCIAL_FINANCE: "This helps finance leaders connect commercial activity to a measurable financial outcome.",
        DrillDomain.INVESTMENT_AND_VALUATION: "This helps finance leaders quantify investment and valuation movements before making capital-allocation decisions.",
    }
    return statements[domain]


def _format_number(value: float) -> str:
    return f"{value:.5f}".rstrip("0").rstrip(".")


def _card_from_record(record: dict[str, Any], primary_domain: DrillDomain) -> DrillCard:
    qa = record["qa"]
    context, table = _visible_evidence(record)
    inferred_unit = _infer_unit(record, context, table)
    if inferred_unit is None:
        raise ValueError("ambiguous_unit")
    unit, answer_type = inferred_unit
    result = execute_finqa_program(qa["program"])
    source_answer = numeric_value(qa["answer"])
    tolerance = 0.00001
    if abs(result - source_answer) > tolerance:
        raise ValueError("answer_mismatch")
    steps = len(qa["steps"])
    card = DrillCard(
        card_id="FINQA-" + hashlib.sha256(record["id"].encode()).hexdigest()[:12].upper(),
        source_dataset=SOURCE_DATASET,
        source_item_id=record["id"],
        source_reference=record["filename"],
        primary_domain=primary_domain,
        secondary_domains=_secondary_domains(qa["question"], primary_domain),
        skill=_skill(qa["question"], qa["answer"], qa["program"]),
        difficulty=DrillDifficulty.FOUNDATIONAL if steps == 1 else DrillDifficulty.INTERMEDIATE,
        calculation_steps=steps,
        question=qa["question"].strip(),
        visible_context=context,
        visible_table=table,
        answer_type=answer_type,
        correct_answer=result,
        unit=unit,
        tolerance=tolerance,
        formula=qa["program"],
        worked_solution=(
            f"Apply the sourced program {qa['program']}. The result is {_format_number(result)} {unit}. "
            "Round only if the question specifies a presentation precision."
        ),
        why_it_matters=_why_it_matters(primary_domain),
        source_attribution=SOURCE_ATTRIBUTION,
        license=LICENSE,
        source_answer=qa["answer"],
        source_program=qa["program"],
        rounding="Use the unrounded calculation; accept answers within 0.00001 of the sourced result.",
    )
    card.validate()
    return card


def _eligibility_reason(record: dict[str, Any]) -> str | None:
    qa = record.get("qa", {})
    if not qa.get("question") or not qa.get("program") or not qa.get("answer"):
        return "missing_required_source_fields"
    steps = qa.get("steps", [])
    if len(steps) not in (1, 2):
        return "more_than_two_calculation_steps"
    if not qa.get("gold_inds"):
        return "missing_visible_evidence"
    if len(qa["question"]) > 180:
        return "question_not_short_drill"
    if _question_domain(qa["question"]) is None:
        return "unclassified_domain"
    try:
        execute_finqa_program(qa["program"])
    except ValueError:
        return "unsupported_or_non_deterministic_program"
    try:
        _card_from_record(record, _question_domain(qa["question"]))
    except ValueError as error:
        message = str(error)
        if message in {"ambiguous_unit", "answer_mismatch"}:
            return message
        if message.startswith("unsupported FinQA number"):
            return "unsupported_source_answer"
        if message == "question and visible context are required":
            return "missing_visible_context"
        return "invalid_card_schema"
    return None


def curate(records: Iterable[dict[str, Any]]) -> tuple[tuple[DrillCard, ...], Counter[str]]:
    """Filter and select exactly 100 cards using fixed quotas and stable order."""

    rejected: Counter[str] = Counter()
    candidates: dict[DrillDomain, list[dict[str, Any]]] = {domain: [] for domain in DrillDomain}
    seen_source_ids: set[str] = set()
    seen_questions: set[str] = set()
    for record in sorted(records, key=_stable_key):
        source_id = record.get("id", "")
        question = record.get("qa", {}).get("question", "")
        if source_id in seen_source_ids:
            rejected["duplicate_source_id"] += 1
            continue
        if _normalise_question(question) in seen_questions:
            rejected["duplicate_question"] += 1
            continue
        seen_source_ids.add(source_id)
        seen_questions.add(_normalise_question(question))
        reason = _eligibility_reason(record)
        if reason:
            rejected[reason] += 1
            continue
        domain = _question_domain(question)
        assert domain is not None
        candidates[domain].append(record)

    selected: list[DrillCard] = []
    for domain in DrillDomain:
        ordered = sorted(candidates[domain], key=_stable_key)
        target = DOMAIN_TARGETS[domain]
        if len(ordered) < target:
            raise ValueError(f"coverage shortage: {domain.value} has {len(ordered)} eligible cards; needs {target}")
        selected.extend(_card_from_record(record, domain) for record in ordered[:target])
        rejected["not_selected_after_quality_and_coverage_ordering"] += len(ordered[target:])
    selected.sort(key=lambda card: card.card_id)
    if len(selected) != 100:
        raise ValueError("selection did not produce exactly 100 cards")
    return tuple(selected), rejected


def _load_records(source: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if source.is_dir():
        records: list[dict[str, Any]] = []
        for filename in DATA_FILES:
            records.extend(json.loads((source / filename).read_text(encoding="utf-8")))
        return records, {"source_records_examined": len(records), "fixture": False}
    payload = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or "records" not in payload:
        raise ValueError("fixture must contain a records list")
    return payload["records"], {**payload.get("generation_metadata", {}), "fixture": True}


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _report(cards: tuple[DrillCard, ...], rejected: Counter[str], metadata: dict[str, Any]) -> str:
    def counts(attribute: str) -> str:
        counter = Counter(getattr(card, attribute).value if hasattr(getattr(card, attribute), "value") else getattr(card, attribute) for card in cards)
        return "\n".join(f"- {name}: {counter[name]}" for name in sorted(counter))

    gaps = [domain.value for domain in DrillDomain if not any(card.primary_domain == domain for card in cards)]
    gap_text = "None in the initial taxonomy." if not gaps else ", ".join(gaps)
    return f"""# FinQA import report\n\n## Run summary\n\n- Fixed selection seed: `{SEED}`\n- Source records examined: {metadata.get('source_records_examined', len(cards))}\n- Cards accepted: {len(cards)}\n- Cards rejected or not selected: {sum(rejected.values())}\n- Runtime network access: none; this report and the card bank are committed generated artifacts.\n\n## Rejection reasons\n\n{chr(10).join(f'- {reason}: {rejected[reason]}' for reason in sorted(rejected))}\n\n## Accepted-card coverage\n\n### Primary domain\n\n{counts('primary_domain')}\n\n### Skill\n\n{counts('skill')}\n\n### Difficulty\n\n{counts('difficulty')}\n\n### Calculation-step count\n\n{counts('calculation_steps')}\n\n## Manual-review flags\n\n- No manual-review flags were introduced by the deterministic selector. Cards retain their FinQA source ID, report reference, evidence, program, answer, attribution, and MIT licence metadata for reviewer inspection.\n\n## Coverage gaps\n\n{gap_text}\n\n## Reproducibility\n\nThe full source pass reads `train.json`, `dev.json`, and `test.json` from the upstream FinQA release. CI uses `tests/fixtures/finqa_v1_selected_records.json`, a committed snapshot of the selected source records, so tests perform no network access. Regenerate with `python scripts/import_finqa.py --source tests/fixtures/finqa_v1_selected_records.json`; run against an upstream local dataset directory to re-examine the complete release.\n\n## Attribution and licence\n\nSource: FinQA by Chen et al. (2021), [GitHub repository](https://github.com/czyssrs/FinQA). The upstream repository is MIT licensed; its required notice is retained in `THIRD_PARTY_NOTICES/FinQA-MIT.txt`.\n"""


def generate(source: Path, output: Path, report_path: Path) -> tuple[DrillCard, ...]:
    records, metadata = _load_records(source)
    cards, rejected = curate(records)
    _write_json(output, {"bank_version": "finqa_cards_v1", "selection_seed": SEED, "cards": [card.as_json() for card in cards]})
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(_report(cards, rejected, metadata), encoding="utf-8")
    return cards


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="FinQA dataset directory or committed source-record fixture")
    parser.add_argument("--output", type=Path, default=Path("data/drills/finqa_cards_v1.json"))
    parser.add_argument("--report", type=Path, default=Path("docs/learning/finqa-import-report.md"))
    args = parser.parse_args()
    cards = generate(args.source, args.output, args.report)
    print(f"Generated {len(cards)} deterministic FinQA cards.")


if __name__ == "__main__":
    main()
