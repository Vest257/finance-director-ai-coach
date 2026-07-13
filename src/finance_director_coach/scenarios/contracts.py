"""Small typed contracts for curated FinanceOS scenarios."""

from __future__ import annotations

from collections.abc import Callable, Mapping, MutableMapping
from dataclasses import dataclass
from typing import Generic, TypeVar

from finance_director_coach.models import EvaluationReport, ScenarioContent

AnswersT = TypeVar("AnswersT")


@dataclass(frozen=True)
class ScenarioMetadata:
    """Information shown in the scenario library and learner summary."""

    primary_domains: tuple[str, ...]
    completion_time: str
    difficulty: str
    provenance: str
    version: str
    short_description: str


@dataclass(frozen=True)
class GuidedScenarioContext:
    """Shared navigation hooks available to a scenario-owned guided renderer."""

    state: MutableMapping[str, object]
    submit_attempt: Callable[[object], None]


@dataclass(frozen=True)
class ScenarioRegistration(Generic[AnswersT]):
    """The explicit boundary between a curated scenario and the shared app shell."""

    content: ScenarioContent
    metadata: ScenarioMetadata
    guided_step_count: int
    evidence_titles: Mapping[str, str]
    critical_omission_labels: Mapping[str, str]
    build_answers: Callable[[Mapping[str, object]], AnswersT]
    evaluate_attempt: Callable[[AnswersT], EvaluationReport]
    skipped_report: Callable[[], EvaluationReport]
    render_guided_step: Callable[[int, GuidedScenarioContext], None]
    recommendation_label: Callable[[AnswersT | None], str]
    ceo_response: Callable[[AnswersT | None], str | None]
