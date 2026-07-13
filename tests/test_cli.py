"""CLI validation and end-to-end learning-flow tests."""

from __future__ import annotations

from collections.abc import Callable, Iterator

from finance_director_coach.cli import TerminalInteraction, main
from finance_director_coach.models import CompetencyRating


def fake_input(values: list[str]) -> tuple[Iterator[str], Callable[[str], str]]:
    iterator = iter(values)

    def read(_: str) -> str:
        return next(iterator)

    return iterator, read


def test_invalid_number_retries() -> None:
    outputs: list[str] = []
    _, read = fake_input(["not-a-number", "", "3.35"])
    terminal = TerminalInteraction(read, outputs.append)
    assert terminal.ask_number("Amount: ") == 3.35
    assert outputs.count("Please enter a valid number, for example 3.35 or -0.20.") == 2


def test_invalid_multiple_selection_retries() -> None:
    outputs: list[str] = []
    _, read = fake_input(["0,9", "one,two", "1,3"])
    terminal = TerminalInteraction(read, outputs.append)
    selected = terminal.choose_many("Choose:", {"a": "A", "b": "B", "c": "C"})
    assert selected == frozenset({"a", "c"})
    assert sum("Choose comma-separated" in output for output in outputs) == 2


def test_skip_to_solution_end_to_end() -> None:
    outputs: list[str] = []
    _, read = fake_input(["1", "2"])
    result = main(read, outputs.append)
    rendered = "\n".join(outputs)
    assert result is not None and result.skipped
    assert result.answers is None
    assert result.report.evidence_records == ()
    assert all(
        item.rating is CompetencyRating.NOT_ASSESSED
        for item in result.report.scorecard.results
    )
    assert "Financial reconciliation" in rendered
    assert "negative GBP 0.20m" in rendered
    assert "negative GBP 0.90m" in rendered
    assert "total cash decline to GBP 2.70m" in rendered
    assert "Hiring costs GBP 0.58m in H2" in rendered
    assert "GBP 3.35m low point" in rendered
    assert "GBP 4.42m December cash" in rendered
    assert "Model Finance Director answer" in rendered
    assert "Full debrief" in rendered
    assert "Self-review checklist [source: self-review]" in rendered
    assert "Learner action plan" in rendered


def test_guided_cli_smoke_end_to_end() -> None:
    outputs: list[str] = []
    inputs = [
        "1",  # Start Scenario 001
        "1",  # Guided path
        "22.2",
        "25.9",
        "2.70",
        "-0.20",
        "-0.90",
        "1,2,3,4,5",
        "1",
        "1,2,3,4,5,6,7",
        "0.58",
        "1.68",
        "3.35",
        "4.42",
        "0.15",
        "0.85",
        "1,2",
        "2",  # Conditionally approve
        "1,2,3,4",
        "1,2,3",
        "1,2,3,4",
        "Conditionally approve with collections, cash, and tranche gates.",
    ]
    _, read = fake_input(inputs)
    result = main(read, outputs.append)
    rendered = "\n".join(outputs)
    assert result is not None and not result.skipped
    assert result.answers is not None
    assert "[E-001] Observed" in rendered
    assert "Commercial Judgment: Capable [source: deterministic]" in rendered
    assert "Stakeholder Communication: Not assessed [source: not-assessed]" in rendered
    assert "Strategic Leadership: Not assessed [source: not-assessed]" in rendered
    assert "Your CEO response (not automatically scored)" in rendered
    assert "Model Finance Director answer" in rendered
    assert "Full debrief" in rendered
    assert "Learner action plan" in rendered
    assert "All monetary answers are entered in GBP millions." in rendered
    assert "Entering 580 would mean GBP 580 million, not GBP 580,000." in rendered
    assert "Worked calculation:" in rendered
    assert "GBP 84,000 / 12 = GBP 7,000" in rendered
