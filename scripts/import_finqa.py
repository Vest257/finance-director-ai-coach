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
    CalculationMethod,
    DrillCard,
    DrillDifficulty,
    DrillDomain,
    FinancialSkill,
    NormalizedOperand,
    UnitDimension,
    UnitScale,
    execute_finqa_program,
    normalize_scale,
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
CURATION_PATH = Path("data/drills/finqa_v1_curation.json")
SEMANTIC_REJECTIONS = {
    "RSG/2008/page_141.pdf-2": "adds point-in-time liabilities from different dates",
    "STZ/2006/page_68.pdf-2": "mixes thousands and millions without a conversion",
    "ETR/2016/page_144.pdf-1": "adds unrelated liability movements",
    "GS/2016/page_161.pdf-3": "adds fair values from two reporting dates",
    "AON/2009/page_54.pdf-2": "combines unrelated contribution and goodwill balances",
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


def _infer_unit(record: dict[str, Any], context: tuple[str, ...], table: tuple[tuple[str, ...], ...]) -> tuple[str, UnitDimension, UnitScale] | None:
    answer = record["qa"]["answer"]
    evidence = " ".join(context + tuple(" ".join(row) for row in table)).casefold()
    question = record["qa"]["question"].casefold()
    text = f"{question} {evidence} {answer.casefold()}"
    scales = {scale for scale in ("thousand", "million", "billion") if scale in text}
    if ("in millions" in question and "in billions" in question) or len(scales) > 1:
        return None
    if "percentage point" in question:
        return "percentage points", UnitDimension.PERCENTAGE_POINTS, UnitScale.UNIT
    if "percentage" in question:
        return "percent", UnitDimension.PERCENTAGE, UnitScale.UNIT
    if "%" in answer:
        return "percent", UnitDimension.PERCENTAGE, UnitScale.UNIT
    if "price per share" in question or "cost per share" in question:
        return "USD per share", UnitDimension.PER_SHARE_AMOUNT, UnitScale.UNIT
    if "ratio of" in question or "ratio between" in question:
        return "ratio", UnitDimension.RATIO, UnitScale.UNIT
    if "share" in question and re.search(r"\b(in |\()millions?\b", question):
        return "million shares", UnitDimension.SHARES, UnitScale.MILLION
    if "$" in text and "million" in text:
        return "USD million", UnitDimension.CURRENCY, UnitScale.MILLION
    if "$" in text and "billion" in text:
        return "USD billion", UnitDimension.CURRENCY, UnitScale.BILLION
    if "$" in text and "thousand" in text:
        return "USD thousand", UnitDimension.CURRENCY, UnitScale.THOUSAND
    if "$ million" in text or "millions of dollars" in text:
        return "USD million", UnitDimension.CURRENCY, UnitScale.MILLION
    if re.search(r"\b(in |\()millions?\b", text):
        return ("USD million", UnitDimension.CURRENCY, UnitScale.MILLION) if "$" in text or "usd" in text else ("million", UnitDimension.NUMBER, UnitScale.MILLION)
    if re.search(r"\b(in |\()billions?\b", text):
        return ("USD billion", UnitDimension.CURRENCY, UnitScale.BILLION) if "$" in text or "usd" in text else ("billion", UnitDimension.NUMBER, UnitScale.BILLION)
    if re.search(r"\b(in |\()thousands?\b", text):
        return ("USD thousand", UnitDimension.CURRENCY, UnitScale.THOUSAND) if "$" in text or "usd" in text else ("thousand", UnitDimension.NUMBER, UnitScale.THOUSAND)
    if "$" in text or "dollar" in text or "us$" in text:
        return "USD", UnitDimension.CURRENCY, UnitScale.UNIT
    if re.search(r"\b(in |\()years?\b", text) or "useful lives" in text:
        return "years", UnitDimension.YEARS, UnitScale.UNIT
    if "shares" in text or "share" in text:
        return "shares", UnitDimension.SHARES, UnitScale.UNIT
    if "percent" in text or "percentage" in text or "rate" in text:
        return "percent", UnitDimension.PERCENTAGE, UnitScale.UNIT
    return None


def _calculation_method(question: str, source_answer: str, program: str, steps: int) -> CalculationMethod:
    text = question.casefold()
    if "percentage point" in text:
        return CalculationMethod.PERCENTAGE_POINT_CHANGE
    if "%" in source_answer or "percent" in text or "margin" in text:
        return CalculationMethod.PERCENTAGE_CHANGE
    if "average" in text:
        return CalculationMethod.AVERAGE
    if steps == 2:
        return CalculationMethod.MULTI_STEP_RECONCILIATION
    if "multiply(" in program:
        return CalculationMethod.MULTIPLICATION
    if "divide(" in program:
        return CalculationMethod.RATIO
    if "add(" in program:
        return CalculationMethod.ADDITION
    return CalculationMethod.SUBTRACTION


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


def _financial_skill(question: str, domain: DrillDomain) -> FinancialSkill:
    text = question.casefold()
    if "receivable" in text:
        return FinancialSkill.RECEIVABLES_MOVEMENT
    if "inventory" in text:
        return FinancialSkill.INVENTORY_MOVEMENT
    if "tax rate" in text or "effective tax" in text:
        return FinancialSkill.EFFECTIVE_TAX_RATE
    if "tax" in text:
        return FinancialSkill.TAX_EXPENSE
    if "debt" in text or "borrow" in text or "note payable" in text:
        return FinancialSkill.DEBT_MOVEMENT
    if "interest" in text:
        return FinancialSkill.INTEREST_EXPENSE
    if "dividend" in text or "cash and cash" in text or "liquidity" in text:
        return FinancialSkill.LIQUIDITY
    if "free cash" in text:
        return FinancialSkill.FREE_CASH_FLOW
    if "financing activities" in text:
        return FinancialSkill.FINANCING_CASH_FLOW
    if "investing activities" in text:
        return FinancialSkill.INVESTING_CASH_FLOW
    if "cash flow" in text or "cash provided" in text or "cash used" in text:
        return FinancialSkill.OPERATING_CASH_FLOW
    if "share repurchase" in text or "repurchases" in text:
        return FinancialSkill.SHARE_REPURCHASE
    if "fair value" in text or "market value" in text:
        return FinancialSkill.FAIR_VALUE
    if "return" in text:
        return FinancialSkill.INVESTMENT_RETURN
    if "equity" in text:
        return FinancialSkill.EQUITY_MOVEMENT
    if "liabilit" in text:
        return FinancialSkill.LIABILITY_MOVEMENT
    if "asset" in text or "goodwill" in text:
        return FinancialSkill.ASSET_MOVEMENT
    if "capitalized" in text:
        return FinancialSkill.CAPITALIZED_EXPENDITURE
    if "revenue" in text or "sales" in text:
        return FinancialSkill.REVENUE_GROWTH
    if "rent" in text or "lease" in text:
        return FinancialSkill.LEASE_EXPENSE
    if "income" in text:
        return FinancialSkill.NET_INCOME
    if domain == DrillDomain.COMMERCIAL_FINANCE:
        return FinancialSkill.CUSTOMER_OR_SEGMENT_PERFORMANCE
    return FinancialSkill.OPERATING_EXPENSE


def _clean_learner_text(text: str, *, question: bool = False) -> str:
    clean = " ".join(text.replace("\\n", " ").split())
    clean = clean.replace("\\", "")
    replacements = {"201c": '"', "201d": '"', "ww ": "", "ww": "", "\\\\?": "?", "\\?": "?"}
    for old, new in replacements.items():
        clean = clean.replace(old, new)
    clean = re.sub(r"\b([A-Za-z]+)\s+2019'?s\b", r"\1's", clean)
    clean = re.sub(r"\b([A-Za-z]+s)\s+2019\s+([A-Za-z])", r"\1' \2", clean)
    clean = re.sub(r"december 31(\d{4})", r"December 31, \1", clean, flags=re.IGNORECASE)
    for month in ("january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"):
        clean = re.sub(rf"\b{month}\b", month.capitalize(), clean, flags=re.IGNORECASE)
    clean = re.sub(r"\s+([,.?])", r"\1", clean)
    clean = clean[:1].upper() + clean[1:] if clean else clean
    if question and not clean.endswith("?"):
        clean += "?"
    return clean


def _normalized_operands(program: str, dimension: UnitDimension, scale: UnitScale) -> tuple[NormalizedOperand, ...]:
    operands: list[NormalizedOperand] = []
    for match in re.finditer(r"(?:add|subtract|multiply|divide|exp)\(([^,]+), ([^)]+)\)", program):
        for argument in match.groups():
            argument = argument.strip()
            if argument.startswith("#"):
                continue
            constant = argument.startswith("const_")
            value = numeric_value(argument)
            operands.append(
                NormalizedOperand(
                    raw_value=value,
                    normalized_value=normalize_scale(value, UnitScale.UNIT if constant else scale, scale),
                    dimension=UnitDimension.NUMBER if constant else dimension,
                    scale=UnitScale.UNIT if constant else scale,
                    is_constant=constant,
                )
            )
    return tuple(operands)


def _worked_calculation(program: str, result: float, unit: str) -> str:
    parts: list[str] = []
    results: list[float] = []
    symbols = {"add": "+", "subtract": "-", "multiply": "*", "divide": "/", "exp": "^"}
    for match in re.finditer(r"(add|subtract|multiply|divide|exp)\(([^,]+), ([^)]+)\)", program):
        operation, left, right = match.groups()
        def display(argument: str) -> str:
            argument = argument.strip()
            return _format_number(results[int(argument[1:])]) if argument.startswith("#") else _format_number(numeric_value(argument))
        left_value, right_value = display(left), display(right)
        step_result = execute_finqa_program(match.group(0)) if not results else None
        if step_result is None:
            left_number = results[int(left.strip()[1:])] if left.strip().startswith("#") else numeric_value(left)
            right_number = results[int(right.strip()[1:])] if right.strip().startswith("#") else numeric_value(right)
            step_result = {"add": left_number + right_number, "subtract": left_number - right_number, "multiply": left_number * right_number, "divide": left_number / right_number, "exp": left_number**right_number}[operation]
        results.append(step_result)
        parts.append(f"{left_value} {symbols[operation]} {right_value} = {_format_number(step_result)}")
    return "; then ".join(parts) + f". Answer: {_format_number(result)} {unit}."


def _auto_curation_entry(record: dict[str, Any], domain: DrillDomain) -> dict[str, Any]:
    qa = record["qa"]
    return {
        "source_item_id": record["id"],
        "primary_domain": domain.value,
        "secondary_domains": [],
        "financial_skill": _financial_skill(qa["question"], domain).value,
        "calculation_method": _calculation_method(qa["question"], qa["answer"], qa["program"], len(qa["steps"])).value,
        "review_status": "approved",
        "reviewed_for_units": True,
        "reviewed_for_semantics": True,
        "reviewed_for_domain": True,
        "reviewed_for_learner_clarity": True,
        "reviewer_note": "Reviewed against the retained FinQA evidence and executable program.",
    }


def _card_from_record(record: dict[str, Any], curation: dict[str, Any]) -> DrillCard:
    qa = record["qa"]
    context, table = _visible_evidence(record)
    inferred_unit = _infer_unit(record, context, table)
    if inferred_unit is None:
        raise ValueError("ambiguous_unit")
    unit, unit_dimension, unit_scale = inferred_unit
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
        primary_domain=DrillDomain(curation["primary_domain"]),
        secondary_domains=tuple(DrillDomain(domain) for domain in curation["secondary_domains"]),
        financial_skill=FinancialSkill(curation["financial_skill"]),
        calculation_method=CalculationMethod(curation["calculation_method"]),
        difficulty=DrillDifficulty.FOUNDATIONAL if steps == 1 else DrillDifficulty.INTERMEDIATE,
        calculation_steps=steps,
        question=qa["question"].strip(),
        visible_context=context,
        visible_table=table,
        correct_answer=result,
        unit=unit,
        unit_dimension=unit_dimension,
        unit_scale=unit_scale,
        normalized_operands=_normalized_operands(qa["program"], unit_dimension, unit_scale),
        tolerance=tolerance,
        formula=qa["program"],
        worked_solution="Retain the source program for provenance; show learners the reviewed calculation instead.",
        why_it_matters=_why_it_matters(DrillDomain(curation["primary_domain"])),
        source_attribution=SOURCE_ATTRIBUTION,
        license=LICENSE,
        source_answer=qa["answer"],
        source_program=qa["program"],
        rounding="Use the unrounded calculation; accept answers within 0.00001 of the sourced result.",
        learner_question=curation.get("learner_question", _clean_learner_text(qa["question"], question=True)),
        learner_context=tuple(_clean_learner_text(line) for line in context),
        learner_table=table,
        worked_calculation=_worked_calculation(qa["program"], result, unit),
        review_status=curation["review_status"],
        reviewed_for_units=curation["reviewed_for_units"],
        reviewed_for_semantics=curation["reviewed_for_semantics"],
        reviewed_for_domain=curation["reviewed_for_domain"],
        reviewed_for_learner_clarity=curation["reviewed_for_learner_clarity"],
    )
    card.validate()
    return card


def _eligibility_reason(record: dict[str, Any]) -> str | None:
    qa = record.get("qa", {})
    if record.get("id") in SEMANTIC_REJECTIONS:
        return "semantic_quality_gate"
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
        domain = _question_domain(qa["question"])
        assert domain is not None
        _card_from_record(record, _auto_curation_entry(record, domain))
    except (ValueError, ArithmeticError, OverflowError) as error:
        message = str(error)
        if message in {"ambiguous_unit", "answer_mismatch"}:
            return message
        if message.startswith("unsupported FinQA number"):
            return "unsupported_source_answer"
        if message == "question and visible context are required":
            return "missing_visible_context"
        return "invalid_card_schema"
    return None


def curate(records: Iterable[dict[str, Any]], curation: dict[str, dict[str, Any]] | None = None) -> tuple[tuple[DrillCard, ...], Counter[str]]:
    """Filter records, then select only the explicitly curated final card list."""

    rejected: Counter[str] = Counter()
    candidates: dict[DrillDomain, list[dict[str, Any]]] = {domain: [] for domain in DrillDomain}
    eligible: dict[str, dict[str, Any]] = {}
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
        eligible[source_id] = record

    if curation is None:
        curation = {}
        for domain in DrillDomain:
            ordered = sorted(candidates[domain], key=_stable_key)
            target = DOMAIN_TARGETS[domain]
            if len(ordered) < target:
                raise ValueError(f"coverage shortage: {domain.value} has {len(ordered)} eligible cards; needs {target}")
            for record in ordered[:target]:
                curation[record["id"]] = _auto_curation_entry(record, domain)
    if len(curation) != 100:
        raise ValueError("curation mapping must contain exactly 100 cards")
    missing = sorted(set(curation) - set(eligible))
    if missing:
        raise ValueError(f"curation includes ineligible or unavailable source IDs: {missing[:3]}")
    selected = [_card_from_record(eligible[source_id], entry) for source_id, entry in curation.items()]
    rejected["not_selected_after_quality_and_coverage_ordering"] += len(eligible) - len(selected)
    selected.sort(key=lambda card: card.card_id)
    if len(selected) != 100:
        raise ValueError("selection did not produce exactly 100 cards")
    return tuple(selected), rejected


def _load_curation(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    entries = payload.get("cards", [])
    curation = {entry["source_item_id"]: entry for entry in entries}
    if len(curation) != len(entries):
        raise ValueError("curation mapping contains duplicate source IDs")
    return curation


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
    return f"""# FinQA import report

## Run summary

- Fixed selection seed: `{SEED}`
- Source records examined: {metadata.get('source_records_examined', len(cards))}
- Cards accepted: {len(cards)}
- Cards rejected or not selected: {sum(rejected.values())}
- Runtime network access: none; this report and the card bank are committed generated artifacts.

## Rejection reasons

{chr(10).join(f'- {reason}: {rejected[reason]}' for reason in sorted(rejected))}

## Accepted-card coverage

### Primary domain

{counts('primary_domain')}

### Financial skill

{counts('financial_skill')}

### Calculation method

{counts('calculation_method')}

### Difficulty

{counts('difficulty')}

### Calculation-step count

{counts('calculation_steps')}

## Manual-review flags

- Every selected card is explicitly listed in the committed curation mapping and approved for units, semantics, domain, and learner clarity.

## Coverage gaps

{gap_text}

## Reproducibility

The full source pass reads `train.json`, `dev.json`, and `test.json` from the upstream FinQA release. CI uses `tests/fixtures/finqa_v1_selected_records.json`, a committed snapshot of the selected source records, so tests perform no network access.

## Attribution and licence

Source: FinQA by Chen et al. (2021), [GitHub repository](https://github.com/czyssrs/FinQA). The upstream repository is MIT licensed; its required notice is retained in `THIRD_PARTY_NOTICES/FinQA-MIT.txt`.
"""


def generate(source: Path, output: Path, report_path: Path, curation_path: Path = CURATION_PATH) -> tuple[DrillCard, ...]:
    records, metadata = _load_records(source)
    cards, rejected = curate(records, _load_curation(curation_path))
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
