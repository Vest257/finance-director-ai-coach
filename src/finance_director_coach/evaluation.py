"""Pure deterministic evaluation for Scenario 001."""

from __future__ import annotations

from collections.abc import Iterable

from finance_director_coach.models import (
    AssessmentSource,
    Competency,
    CompetencyRating,
    CompetencyResult,
    CompetencyScorecard,
    EvaluationReport,
    EvidenceRecord,
    EvidenceResult,
    LearnerAnswers,
    RecommendationRoute,
)
from finance_director_coach.scenarios.scenario_001 import (
    ALTERNATIVE_CAPACITY_OPTIONS,
    CORE_MISSING_INFORMATION,
    CORE_RISKS,
    CORE_TRADEOFFS,
    EXPECTED_CASH_DRIVERS,
    EXPECTED_THRESHOLD_INTERPRETATIONS,
    EXTENDED_RISKS,
    MONEY_TOLERANCE,
    PERCENTAGE_TOLERANCE,
    REQUIRED_ROUTE_SAFEGUARDS,
)


def _within(value: float, expected: float, tolerance: float) -> bool:
    return abs(value - expected) <= tolerance + 1e-9


def _result(condition: bool, sufficient: bool) -> EvidenceResult:
    if not sufficient:
        return EvidenceResult.INSUFFICIENT_EVIDENCE
    return EvidenceResult.OBSERVED if condition else EvidenceResult.NOT_OBSERVED


def _format_values(values: Iterable[object]) -> str:
    rendered = [str(value) for value in values]
    return ", ".join(rendered) if rendered else "No input"


def _record(
    evidence_id: str,
    learner_input: str,
    expected_rule: str,
    result: EvidenceResult,
    competencies: tuple[Competency, ...],
    observed_feedback: str,
    improvement_guidance: str,
) -> EvidenceRecord:
    if result is EvidenceResult.OBSERVED:
        feedback = observed_feedback
    elif result is EvidenceResult.NOT_OBSERVED:
        feedback = f"The submitted evidence did not meet this rule: {expected_rule}"
    else:
        feedback = "There was not enough learner evidence to apply this rule."
    return EvidenceRecord(
        evidence_id=evidence_id,
        learner_input=learner_input,
        expected_rule=expected_rule,
        result=result,
        competencies_informed=competencies,
        feedback=feedback,
        improvement_guidance=improvement_guidance,
    )


def evaluate_evidence(answers: LearnerAnswers) -> tuple[EvidenceRecord, ...]:
    """Evaluate all explicit Scenario 001 evidence rules."""

    growth_values = (answers.revenue_growth_percent, answers.ebitda_growth_percent)
    growth_sufficient = all(value is not None for value in growth_values)
    growth_observed = growth_sufficient and _within(
        answers.revenue_growth_percent or 0.0, 22.2, PERCENTAGE_TOLERANCE
    ) and _within(answers.ebitda_growth_percent or 0.0, 25.9, PERCENTAGE_TOLERANCE)

    cash_sufficient = answers.cash_decrease is not None
    cash_observed = cash_sufficient and _within(answers.cash_decrease or 0.0, 2.70, MONEY_TOLERANCE)

    operating_values = (
        answers.operating_cash_before_interest_tax,
        answers.net_operating_cash,
    )
    operating_sufficient = all(value is not None for value in operating_values)
    operating_observed = operating_sufficient and _within(
        answers.operating_cash_before_interest_tax or 0.0, -0.20, MONEY_TOLERANCE
    ) and _within(answers.net_operating_cash or 0.0, -0.90, MONEY_TOLERANCE)

    hiring_values = (answers.h2_hiring_cost, answers.annual_hiring_cost)
    hiring_sufficient = all(value is not None for value in hiring_values)
    hiring_observed = hiring_sufficient and _within(
        answers.h2_hiring_cost or 0.0, 0.58, MONEY_TOLERANCE
    ) and _within(answers.annual_hiring_cost or 0.0, 1.68, MONEY_TOLERANCE)

    liquidity_values = (answers.cash_low_point, answers.december_cash)
    liquidity_sufficient = all(value is not None for value in liquidity_values)
    liquidity_observed = liquidity_sufficient and _within(
        answers.cash_low_point or 0.0, 3.35, MONEY_TOLERANCE
    ) and _within(answers.december_cash or 0.0, 4.42, MONEY_TOLERANCE)

    threshold_values = (answers.board_floor_shortfall, answers.lender_headroom)
    threshold_sufficient = all(value is not None for value in threshold_values) and bool(
        answers.threshold_interpretations
    )
    threshold_observed = (
        threshold_sufficient
        and _within(answers.board_floor_shortfall or 0.0, 0.15, MONEY_TOLERANCE)
        and _within(answers.lender_headroom or 0.0, 0.85, MONEY_TOLERANCE)
        and answers.threshold_interpretations == EXPECTED_THRESHOLD_INTERPRETATIONS
    )

    route_sufficient = answers.recommendation is not None
    safeguard_sufficient = route_sufficient and bool(answers.safeguards)
    safeguard_observed = bool(
        answers.recommendation
        and REQUIRED_ROUTE_SAFEGUARDS[answers.recommendation].issubset(answers.safeguards)
    )

    required_values = (
        *growth_values,
        answers.cash_decrease,
        *operating_values,
        *hiring_values,
        *liquidity_values,
        *threshold_values,
    )
    required_steps_complete = (
        all(value is not None for value in required_values)
        and bool(answers.cash_drivers)
        and answers.largest_cash_driver is not None
        and bool(answers.risks)
        and bool(answers.threshold_interpretations)
        and answers.recommendation is not None
        and bool(answers.safeguards)
        and bool(answers.missing_information)
        and bool(answers.tradeoffs)
        and bool(answers.ceo_response.strip())
    )

    records = (
        _record(
            "E-001",
            _format_values(growth_values),
            "Revenue growth 22.2% and EBITDA growth 25.9%, each within 0.2 percentage points",
            _result(growth_observed, growth_sufficient),
            (Competency.FINANCIAL_INSIGHT,),
            "You calculated both growth rates within the documented tolerance.",
            "Recalculate percentage growth as (current - prior) / prior x 100.",
        ),
        _record(
            "E-002",
            _format_values((answers.cash_decrease,)),
            "Cash decreased by GBP 2.70m, within GBP 0.05m",
            _result(cash_observed, cash_sufficient),
            (Competency.FINANCIAL_INSIGHT, Competency.CASH_AND_RISK_DISCIPLINE),
            "You identified the complete GBP 2.70m cash decline.",
            "Compare opening cash of GBP 7.00m with closing cash of GBP 4.30m.",
        ),
        _record(
            "E-003",
            _format_values(operating_values),
            "Operating cash before interest and tax was -GBP 0.20m and net operating cash was -GBP 0.90m",
            _result(operating_observed, operating_sufficient),
            (Competency.FINANCIAL_INSIGHT,),
            "You reconciled EBITDA to both operating-cash measures.",
            "Bridge EBITDA through working capital, then deduct cash interest and tax.",
        ),
        _record(
            "E-004",
            _format_values(sorted(answers.cash_drivers)),
            "Select the three working-capital uses and both liability offsets, with no unsupported drivers",
            _result(answers.cash_drivers == EXPECTED_CASH_DRIVERS, bool(answers.cash_drivers)),
            (Competency.FINANCIAL_INSIGHT,),
            "You distinguished working-capital uses from their partial cash offsets.",
            "Trace each selected driver to the balance-sheet movement and cash bridge.",
        ),
        _record(
            "E-005",
            _format_values((answers.largest_cash_driver,)),
            "Trade receivables is the largest cash-use movement",
            _result(answers.largest_cash_driver == "receivables", answers.largest_cash_driver is not None),
            (Competency.FINANCIAL_INSIGHT,),
            "You identified the GBP 3.20m receivables movement as the largest driver.",
            "Compare the absolute value of each cash-use movement.",
        ),
        _record(
            "E-006",
            _format_values(hiring_values),
            "H2 hiring cost GBP 0.58m and annual recurring cost GBP 1.68m",
            _result(hiring_observed, hiring_sufficient),
            (Competency.COMMERCIAL_JUDGMENT,),
            "You quantified the near-term and recurring hiring commitment.",
            "Apply the September and November start dates to monthly recurring and onboarding costs.",
        ),
        _record(
            "E-007",
            _format_values(liquidity_values),
            "Hiring-case cash low point GBP 3.35m and December cash GBP 4.42m",
            _result(liquidity_observed, liquidity_sufficient),
            (Competency.CASH_AND_RISK_DISCIPLINE,),
            "You calculated the hiring-case low point and December cash.",
            "Deduct cumulative hiring costs from each baseline monthly closing cash balance.",
        ),
        _record(
            "E-008",
            _format_values((*threshold_values, *sorted(answers.threshold_interpretations))),
            "Board floor breached by GBP 0.15m; lender minimum retained with GBP 0.85m headroom",
            _result(threshold_observed, threshold_sufficient),
            (Competency.CASH_AND_RISK_DISCIPLINE,),
            "You correctly separated the internal board floor from the lender covenant.",
            "Compare the GBP 3.35m low point separately with GBP 3.50m and GBP 2.50m.",
        ),
        _record(
            "E-009",
            _format_values((answers.recommendation.label if answers.recommendation else None,)),
            "Select Approve, Conditionally approve, Delay, or Reject",
            _result(route_sufficient, route_sufficient),
            (Competency.COMMERCIAL_JUDGMENT, Competency.STRATEGIC_LEADERSHIP),
            "You made an explicit recommendation. The route is evidence, not an automatic leadership rating.",
            "State one of the four recommendation routes explicitly.",
        ),
        _record(
            "E-010",
            _format_values(sorted(answers.safeguards)),
            "Select every core safeguard defined for the chosen recommendation route",
            _result(safeguard_observed, safeguard_sufficient),
            (Competency.COMMERCIAL_JUDGMENT, Competency.CASH_AND_RISK_DISCIPLINE),
            "Your safeguards satisfy the documented requirements for this route.",
            "Use the route-specific conditions to protect liquidity and preserve a credible next action.",
        ),
        _record(
            "E-011",
            _format_values(sorted(answers.missing_information)),
            "Include collections evidence, downside liquidity, and the hiring business case",
            _result(
                CORE_MISSING_INFORMATION.issubset(answers.missing_information),
                bool(answers.missing_information),
            ),
            (Competency.FINANCIAL_INSIGHT, Competency.STRATEGIC_LEADERSHIP),
            "You identified the minimum missing evidence needed to improve the decision.",
            "Ask what could change the recommendation: collections, downside cash, and role economics.",
        ),
        _record(
            "E-012",
            "All required inputs completed" if required_steps_complete else "One or more required inputs missing",
            "Complete every required calculation, selection, decision, and free-text response; text presence only is checked",
            _result(required_steps_complete, any(value is not None for value in required_values) or bool(answers.ceo_response)),
            (Competency.COMMERCIAL_JUDGMENT,),
            "You completed the full analysis sequence. Free-text quality was not evaluated.",
            "Complete each guided step before reviewing the solution.",
        ),
        _record(
            "E-013",
            _format_values(sorted(answers.tradeoffs)),
            "Recognize growth capacity, recurring cost, timing risk, and at least one capacity alternative",
            _result(
                CORE_TRADEOFFS.issubset(answers.tradeoffs)
                and bool(ALTERNATIVE_CAPACITY_OPTIONS.intersection(answers.tradeoffs)),
                bool(answers.tradeoffs),
            ),
            (Competency.COMMERCIAL_JUDGMENT,),
            "You recorded the central tradeoffs and an alternative action. This does not prove strong judgment.",
            "Balance the growth case with cost timing and a practical alternative.",
        ),
        _record(
            "E-014",
            _format_values(sorted(answers.risks)),
            "Recognize overdue receivables, board-floor breach, and collection-dependent forecast",
            _result(CORE_RISKS.issubset(answers.risks), bool(answers.risks)),
            (Competency.CASH_AND_RISK_DISCIPLINE,),
            "You identified the core liquidity and working-capital risks.",
            "Connect receivables and forecast assumptions to the internal cash threshold.",
        ),
        _record(
            "E-015",
            _format_values(sorted(answers.risks)),
            "Also recognize inventory/contract assets, RCF expiry, unsupported hiring benefit, and missing downside case",
            _result(EXTENDED_RISKS.issubset(answers.risks), bool(answers.risks)),
            (Competency.CASH_AND_RISK_DISCIPLINE,),
            "You identified the extended funding, forecast, and execution risks.",
            "Look beyond the immediate cash low point to forecast quality and funding expiry.",
        ),
    )
    return records


def _record_map(records: tuple[EvidenceRecord, ...]) -> dict[str, EvidenceRecord]:
    return {record.evidence_id: record for record in records}


def _observed(records: dict[str, EvidenceRecord], evidence_ids: Iterable[str]) -> bool:
    return all(records[evidence_id].result is EvidenceResult.OBSERVED for evidence_id in evidence_ids)


def _has_evidence(records: dict[str, EvidenceRecord], evidence_ids: Iterable[str]) -> bool:
    return any(
        records[evidence_id].result is not EvidenceResult.INSUFFICIENT_EVIDENCE
        for evidence_id in evidence_ids
    )


def _used_evidence(records: dict[str, EvidenceRecord], evidence_ids: Iterable[str]) -> tuple[str, ...]:
    return tuple(
        evidence_id
        for evidence_id in evidence_ids
        if records[evidence_id].result is not EvidenceResult.INSUFFICIENT_EVIDENCE
    )


def identify_critical_omissions(
    answers: LearnerAnswers, records: tuple[EvidenceRecord, ...]
) -> tuple[str, ...]:
    """Apply only explicit structured critical-omission gates."""

    by_id = _record_map(records)
    omissions: list[str] = []
    if (
        by_id["E-003"].result is EvidenceResult.NOT_OBSERVED
        and by_id["E-004"].result is EvidenceResult.NOT_OBSERVED
    ):
        omissions.append("CO-001")
    if any(
        by_id[evidence_id].result is EvidenceResult.NOT_OBSERVED
        for evidence_id in ("E-002", "E-003", "E-006", "E-007", "E-008")
    ):
        omissions.append("CO-002")
    any_assessed_input = any(
        record.result is not EvidenceResult.INSUFFICIENT_EVIDENCE for record in records
    )
    if answers.recommendation is None and any_assessed_input:
        omissions.append("CO-003")
    if answers.recommendation in {
        RecommendationRoute.APPROVE,
        RecommendationRoute.CONDITIONALLY_APPROVE,
    } and (
        by_id["E-008"].result is not EvidenceResult.OBSERVED
        or by_id["E-010"].result is not EvidenceResult.OBSERVED
    ):
        omissions.append("CO-004")
    if (
        "lender_covenant_breached" in answers.threshold_interpretations
        or "lender_covenant_breached" in answers.risks
    ):
        omissions.append("CO-005")
    if "assumptions_are_certain" in answers.risks:
        omissions.append("CO-006")
    return tuple(omissions)


def _not_assessed_result(
    competency: Competency,
    explanation: str,
    improvement: str,
    evidence_used: tuple[str, ...] = (),
    limitation: str | None = None,
) -> CompetencyResult:
    return CompetencyResult(
        competency=competency,
        rating=CompetencyRating.NOT_ASSESSED,
        assessment_source=AssessmentSource.NOT_ASSESSED,
        evidence_used=evidence_used,
        explanation=explanation,
        improvement_guidance=improvement,
        limitation=limitation,
    )


def build_scorecard(
    records: tuple[EvidenceRecord, ...], critical_omissions: tuple[str, ...]
) -> CompetencyScorecard:
    by_id = _record_map(records)

    financial_ids = ("E-001", "E-002", "E-003", "E-004", "E-005", "E-011")
    financial_core = ("E-002", "E-003", "E-004", "E-005")
    financial_strong = ("E-001", "E-011")
    if not _has_evidence(by_id, financial_ids):
        financial = _not_assessed_result(
            Competency.FINANCIAL_INSIGHT,
            "No meaningful financial-analysis evidence was collected.",
            "Complete the guided calculations and driver selections.",
        )
    elif set(critical_omissions).intersection({"CO-001", "CO-002", "CO-005"}) or not _observed(
        by_id, financial_core
    ):
        financial = CompetencyResult(
            Competency.FINANCIAL_INSIGHT,
            CompetencyRating.DEVELOPING,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, financial_ids),
            "Core profit-to-cash evidence was incorrect or a critical financial omission was triggered.",
            "Reconcile EBITDA through working capital and verify each material figure.",
        )
    elif _observed(by_id, financial_strong):
        financial = CompetencyResult(
            Competency.FINANCIAL_INSIGHT,
            CompetencyRating.STRONG,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, financial_ids),
            "All core and extended structured financial evidence was observed.",
            "Maintain the same traceability from financial movement to business driver.",
        )
    else:
        financial = CompetencyResult(
            Competency.FINANCIAL_INSIGHT,
            CompetencyRating.CAPABLE,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, financial_ids),
            "The core cash reconciliation was sound, with some extended evidence missing.",
            "Add accurate growth calculations and identify the key unavailable information.",
        )

    commercial_ids = ("E-006", "E-009", "E-010", "E-012", "E-013")
    commercial_core = ("E-006", "E-009", "E-010", "E-012")
    if not _has_evidence(by_id, commercial_ids):
        commercial = _not_assessed_result(
            Competency.COMMERCIAL_JUDGMENT,
            "No meaningful commercial-decision evidence was collected.",
            "Complete the hiring calculation, recommendation, and route safeguards.",
        )
    elif set(critical_omissions).intersection({"CO-003", "CO-004", "CO-006"}) or not _observed(
        by_id, commercial_core
    ):
        commercial = CompetencyResult(
            Competency.COMMERCIAL_JUDGMENT,
            CompetencyRating.DEVELOPING,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, commercial_ids),
            "The structured decision evidence omitted a core calculation, decision, or route safeguard.",
            "Make the decision explicit and connect route-specific safeguards to the financial exposure.",
            "Deterministic evidence cannot evaluate nuance or executive tradeoff quality.",
        )
    else:
        commercial = CompetencyResult(
            Competency.COMMERCIAL_JUDGMENT,
            CompetencyRating.CAPABLE,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, commercial_ids),
            "The structured evidence shows a complete, financially supported decision path.",
            "Use qualified manual review to test whether the reasoning demonstrates strong executive judgment.",
            "Commercial Judgment is capped at Capable under deterministic MVP evaluation.",
        )

    cash_ids = ("E-002", "E-007", "E-008", "E-010", "E-014", "E-015")
    cash_core = ("E-002", "E-007", "E-008", "E-010", "E-014")
    if not _has_evidence(by_id, cash_ids):
        cash = _not_assessed_result(
            Competency.CASH_AND_RISK_DISCIPLINE,
            "No meaningful liquidity or risk evidence was collected.",
            "Complete the cash, threshold, safeguards, and risk questions.",
        )
    elif set(critical_omissions).intersection({"CO-001", "CO-002", "CO-004"}) or not _observed(
        by_id, cash_core
    ):
        cash = CompetencyResult(
            Competency.CASH_AND_RISK_DISCIPLINE,
            CompetencyRating.DEVELOPING,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, cash_ids),
            "A core liquidity calculation, threshold, risk, or safeguard was not observed.",
            "Separate internal and lender thresholds and connect each risk to a practical safeguard.",
        )
    elif by_id["E-015"].result is EvidenceResult.OBSERVED:
        cash = CompetencyResult(
            Competency.CASH_AND_RISK_DISCIPLINE,
            CompetencyRating.STRONG,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, cash_ids),
            "All core and extended structured liquidity and risk evidence was observed.",
            "Maintain downside sensitivity and funding-expiry discipline in future cases.",
        )
    else:
        cash = CompetencyResult(
            Competency.CASH_AND_RISK_DISCIPLINE,
            CompetencyRating.CAPABLE,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, cash_ids),
            "The core liquidity position and safeguards were correctly identified.",
            "Extend the analysis to forecast quality, hiring-benefit evidence, and RCF expiry.",
        )

    stakeholder = _not_assessed_result(
        Competency.STAKEHOLDER_COMMUNICATION,
        "The CEO response was stored for display and self-review, not machine-scored.",
        "Use the self-review checklist or ask a qualified reviewer to assess communication evidence.",
        limitation="A qualified manual reviewer is required in the MVP.",
    )

    strategic_evidence = tuple(
        evidence_id
        for evidence_id in ("E-009", "E-011")
        if by_id[evidence_id].result is EvidenceResult.OBSERVED
    )
    strategic = _not_assessed_result(
        Competency.STRATEGIC_LEADERSHIP,
        "Recommendation and missing-information selections were retained as evidence but do not establish leadership quality.",
        "Use qualified manual review to assess ownership, alignment, and cross-functional leadership.",
        strategic_evidence,
        "A qualified manual reviewer is required in the MVP; route selection alone cannot create a rating.",
    )

    return CompetencyScorecard((financial, commercial, cash, stakeholder, strategic))


def evaluate_attempt(answers: LearnerAnswers) -> EvaluationReport:
    records = evaluate_evidence(answers)
    omissions = identify_critical_omissions(answers, records)
    return EvaluationReport(records, build_scorecard(records, omissions), omissions)


def skipped_evaluation_report() -> EvaluationReport:
    """Return a scorecard for skip-to-solution without assessed evidence."""

    reason = "The learner chose skip-to-solution, so no assessed evidence was collected."
    results = tuple(
        _not_assessed_result(
            competency,
            reason,
            "Complete a guided attempt to provide assessable evidence.",
            limitation="Skip-to-solution is a study path, not an assessed attempt.",
        )
        for competency in Competency
    )
    return EvaluationReport((), CompetencyScorecard(results), ())
