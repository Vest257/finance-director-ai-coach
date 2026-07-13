"""Typed domain models for scenario attempts and evaluation output."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class RecommendationRoute(str, Enum):
    """The four decisions available to the learner."""

    APPROVE = "approve"
    CONDITIONALLY_APPROVE = "conditionally_approve"
    DELAY = "delay"
    REJECT = "reject"

    @property
    def label(self) -> str:
        return {
            self.APPROVE: "Approve",
            self.CONDITIONALLY_APPROVE: "Conditionally approve",
            self.DELAY: "Delay",
            self.REJECT: "Reject",
        }[self]


class Competency(str, Enum):
    FINANCIAL_INSIGHT = "Financial Insight"
    COMMERCIAL_JUDGMENT = "Commercial Judgment"
    CASH_AND_RISK_DISCIPLINE = "Cash And Risk Discipline"
    STAKEHOLDER_COMMUNICATION = "Stakeholder Communication"
    STRATEGIC_LEADERSHIP = "Strategic Leadership"


class CompetencyRating(str, Enum):
    DEVELOPING = "Developing"
    CAPABLE = "Capable"
    STRONG = "Strong"
    NOT_ASSESSED = "Not assessed"


class AssessmentSource(str, Enum):
    DETERMINISTIC = "deterministic"
    SELF_REVIEW = "self-review"
    MANUAL_REVIEW = "manual-review"
    NOT_ASSESSED = "not-assessed"


class EvidenceResult(str, Enum):
    OBSERVED = "Observed"
    NOT_OBSERVED = "Not observed"
    INSUFFICIENT_EVIDENCE = "Insufficient evidence"


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    learner_input: str
    expected_rule: str
    result: EvidenceResult
    competencies_informed: tuple[Competency, ...]
    feedback: str
    improvement_guidance: str


@dataclass(frozen=True)
class CompetencyResult:
    competency: Competency
    rating: CompetencyRating
    assessment_source: AssessmentSource
    evidence_used: tuple[str, ...]
    explanation: str
    improvement_guidance: str
    limitation: str | None = None


@dataclass(frozen=True)
class CompetencyScorecard:
    results: tuple[CompetencyResult, ...]

    def for_competency(self, competency: Competency) -> CompetencyResult:
        return next(result for result in self.results if result.competency is competency)


@dataclass(frozen=True)
class LearnerAnswers:
    revenue_growth_percent: float | None = None
    ebitda_growth_percent: float | None = None
    cash_decrease: float | None = None
    operating_cash_before_interest_tax: float | None = None
    net_operating_cash: float | None = None
    cash_drivers: frozenset[str] = field(default_factory=frozenset)
    largest_cash_driver: str | None = None
    risks: frozenset[str] = field(default_factory=frozenset)
    h2_hiring_cost: float | None = None
    annual_hiring_cost: float | None = None
    cash_low_point: float | None = None
    december_cash: float | None = None
    board_floor_shortfall: float | None = None
    lender_headroom: float | None = None
    threshold_interpretations: frozenset[str] = field(default_factory=frozenset)
    recommendation: RecommendationRoute | None = None
    safeguards: frozenset[str] = field(default_factory=frozenset)
    missing_information: frozenset[str] = field(default_factory=frozenset)
    tradeoffs: frozenset[str] = field(default_factory=frozenset)
    ceo_response: str = ""


ScenarioAttempt = LearnerAnswers


@dataclass(frozen=True)
class EvaluationReport:
    evidence_records: tuple[EvidenceRecord, ...]
    scorecard: CompetencyScorecard
    critical_omissions: tuple[str, ...]


@dataclass(frozen=True)
class ContentSection:
    title: str
    body: str


@dataclass(frozen=True)
class ScenarioContent:
    scenario_id: str
    title: str
    learner_role: str
    company_context: str
    financial_pack: tuple[ContentSection, ...]
    initial_question: str
    model_answer: str
    debrief: str
    self_review_checklist: tuple[str, ...]
    action_plan: tuple[str, ...]
    reconciliation_summary: str
