"""Pure deterministic evaluation for Scenario 002."""

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
    RecommendationRoute,
)
from finance_director_coach.scenarios.scenario_002 import (
    EXPECTED_AVOIDABLE_COSTS,
    EXPECTED_COST_REDUCTION,
    EXPECTED_CURRENT_EBITDA_MARGIN,
    EXPECTED_CURRENT_GROSS_MARGIN,
    EXPECTED_CUSTOMER_CONTRIBUTION,
    EXPECTED_CUSTOMER_CONTRIBUTION_MARGIN,
    EXPECTED_DISCOUNTED_CONTRIBUTION_MARGIN,
    EXPECTED_ECONOMIC_REVENUE,
    EXPECTED_MARGIN_INTERPRETATION,
    EXPECTED_MISSING_INFORMATION,
    EXPECTED_PRICE_INCREASE,
    EXPECTED_PRICE_INCREASE_PERCENT,
    EXPECTED_PRIOR_EBITDA_MARGIN,
    EXPECTED_PRIOR_GROSS_MARGIN,
    EXPECTED_REQUESTED_DISCOUNT,
    EXPECTED_REVENUE_GROWTH,
    EXPECTED_TOP_DRIVERS,
    JUDGMENT_EXPLANATIONS,
    MONEY_TOLERANCE,
    PERCENTAGE_TOLERANCE,
    REQUIRED_ROUTE_SAFEGUARDS,
    Scenario002Answers,
    WORKED_CALCULATION_EXPLANATIONS,
    decision_condition_expectation,
    decision_condition_feedback,
    decision_conditions_are_valid,
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
    worked_solution: str | None = None,
    judgment_explanation: str | None = None,
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
        worked_solution=worked_solution,
        judgment_explanation=judgment_explanation,
    )


def evaluate_scenario_002_evidence(answers: Scenario002Answers) -> tuple[EvidenceRecord, ...]:
    """Evaluate only authored, observable Scenario 002 evidence."""

    revenue_sufficient = answers.revenue_growth_percent is not None
    revenue_observed = revenue_sufficient and _within(
        answers.revenue_growth_percent or 0.0, EXPECTED_REVENUE_GROWTH, PERCENTAGE_TOLERANCE
    )
    gross_values = (answers.prior_gross_margin_percent, answers.current_gross_margin_percent)
    gross_sufficient = all(value is not None for value in gross_values)
    gross_observed = gross_sufficient and _within(
        answers.prior_gross_margin_percent or 0.0, EXPECTED_PRIOR_GROSS_MARGIN, PERCENTAGE_TOLERANCE
    ) and _within(
        answers.current_gross_margin_percent or 0.0, EXPECTED_CURRENT_GROSS_MARGIN, PERCENTAGE_TOLERANCE
    )
    ebitda_values = (answers.prior_ebitda_margin_percent, answers.current_ebitda_margin_percent)
    ebitda_sufficient = all(value is not None for value in ebitda_values)
    ebitda_observed = ebitda_sufficient and _within(
        answers.prior_ebitda_margin_percent or 0.0, EXPECTED_PRIOR_EBITDA_MARGIN, PERCENTAGE_TOLERANCE
    ) and _within(
        answers.current_ebitda_margin_percent or 0.0, EXPECTED_CURRENT_EBITDA_MARGIN, PERCENTAGE_TOLERANCE
    )
    interpretation_sufficient = answers.margin_interpretation is not None
    interpretation_observed = answers.margin_interpretation == EXPECTED_MARGIN_INTERPRETATION

    contribution_values = (answers.customer_contribution, answers.customer_contribution_margin_percent)
    contribution_sufficient = all(value is not None for value in contribution_values)
    contribution_observed = contribution_sufficient and _within(
        answers.customer_contribution or 0.0, EXPECTED_CUSTOMER_CONTRIBUTION, MONEY_TOLERANCE
    ) and _within(
        answers.customer_contribution_margin_percent or 0.0,
        EXPECTED_CUSTOMER_CONTRIBUTION_MARGIN,
        PERCENTAGE_TOLERANCE,
    )
    price_values = (answers.economic_revenue, answers.price_increase, answers.price_increase_percent)
    price_sufficient = all(value is not None for value in price_values)
    price_observed = price_sufficient and _within(
        answers.economic_revenue or 0.0, EXPECTED_ECONOMIC_REVENUE, MONEY_TOLERANCE
    ) and _within(answers.price_increase or 0.0, EXPECTED_PRICE_INCREASE, MONEY_TOLERANCE) and _within(
        answers.price_increase_percent or 0.0, EXPECTED_PRICE_INCREASE_PERCENT, PERCENTAGE_TOLERANCE
    )
    cost_sufficient = answers.cost_reduction is not None
    cost_observed = cost_sufficient and _within(
        answers.cost_reduction or 0.0, EXPECTED_COST_REDUCTION, MONEY_TOLERANCE
    )
    discount_values = (answers.requested_discount, answers.discounted_contribution_margin_percent)
    discount_sufficient = all(value is not None for value in discount_values)
    discount_observed = discount_sufficient and _within(
        answers.requested_discount or 0.0, EXPECTED_REQUESTED_DISCOUNT, MONEY_TOLERANCE
    ) and _within(
        answers.discounted_contribution_margin_percent or 0.0,
        EXPECTED_DISCOUNTED_CONTRIBUTION_MARGIN,
        PERCENTAGE_TOLERANCE,
    )

    drivers_sufficient = bool(answers.top_drivers)
    drivers_observed = answers.top_drivers == EXPECTED_TOP_DRIVERS and len(answers.top_drivers) == 3
    avoidable_sufficient = bool(answers.avoidable_costs)
    avoidable_observed = answers.avoidable_costs == EXPECTED_AVOIDABLE_COSTS and len(answers.avoidable_costs) == 4
    missing_sufficient = bool(answers.missing_information)
    missing_observed = answers.missing_information == EXPECTED_MISSING_INFORMATION and len(answers.missing_information) == 3
    route_sufficient = answers.recommendation is not None
    safeguards_sufficient = route_sufficient and bool(answers.safeguards)
    safeguards_observed = bool(
        answers.recommendation
        and REQUIRED_ROUTE_SAFEGUARDS[answers.recommendation].issubset(answers.safeguards)
    )
    conditions_sufficient = (
        answers.recommendation is not None and bool(answers.decision_conditions)
    )
    conditions_observed = decision_conditions_are_valid(
        answers.recommendation, answers.decision_conditions
    )

    required_values = (
        answers.revenue_growth_percent,
        *gross_values,
        *ebitda_values,
        *contribution_values,
        *price_values,
        answers.cost_reduction,
        *discount_values,
    )
    completion_sufficient = any(value is not None for value in required_values) or bool(answers.ceo_response)
    completion_observed = (
        all(value is not None for value in required_values)
        and interpretation_sufficient
        and drivers_sufficient
        and avoidable_sufficient
        and missing_sufficient
        and route_sufficient
        and safeguards_sufficient
        and conditions_sufficient
        and bool(answers.ceo_response.strip())
    )

    return (
        _record(
            "SCN-002-E-001",
            _format_values((answers.revenue_growth_percent,)),
            f"Revenue growth is {EXPECTED_REVENUE_GROWTH:.1f}% within 0.2 percentage points",
            _result(revenue_observed, revenue_sufficient),
            (Competency.FINANCIAL_INSIGHT,),
            "You calculated company revenue growth within tolerance.",
            "Calculate growth as (current - prior) / prior x 100.",
            WORKED_CALCULATION_EXPLANATIONS["SCN-002-E-001"],
        ),
        _record(
            "SCN-002-E-002",
            _format_values(gross_values),
            f"Gross margins are {EXPECTED_PRIOR_GROSS_MARGIN:.1f}% and {EXPECTED_CURRENT_GROSS_MARGIN:.1f}% within 0.2 percentage points",
            _result(gross_observed, gross_sufficient),
            (Competency.FINANCIAL_INSIGHT,),
            "You reconciled gross profit to revenue for both periods.",
            "Divide gross profit by revenue for each period; do not compare pound movements alone.",
            WORKED_CALCULATION_EXPLANATIONS["SCN-002-E-002"],
        ),
        _record(
            "SCN-002-E-003",
            _format_values(ebitda_values),
            f"EBITDA margins are {EXPECTED_PRIOR_EBITDA_MARGIN:.1f}% and {EXPECTED_CURRENT_EBITDA_MARGIN:.1f}% within 0.2 percentage points",
            _result(ebitda_observed, ebitda_sufficient),
            (Competency.FINANCIAL_INSIGHT,),
            "You reconciled EBITDA to revenue for both periods.",
            "Divide EBITDA by revenue for each period and retain percentage-point treatment.",
            WORKED_CALCULATION_EXPLANATIONS["SCN-002-E-003"],
        ),
        _record(
            "SCN-002-E-004",
            _format_values((answers.margin_interpretation,)),
            "Recognize that revenue growth with falling gross and EBITDA margins can erode value",
            _result(interpretation_observed, interpretation_sufficient),
            (Competency.FINANCIAL_INSIGHT, Competency.COMMERCIAL_JUDGMENT),
            "You linked revenue growth to the margin deterioration that changes its quality.",
            "Interpret growth through both gross and EBITDA margin before treating it as value creation.",
            judgment_explanation=JUDGMENT_EXPLANATIONS["SCN-002-E-004"],
        ),
        _record(
            "SCN-002-E-005",
            _format_values(contribution_values),
            f"Customer contribution is GBP {EXPECTED_CUSTOMER_CONTRIBUTION:.2f}m and contribution margin is {EXPECTED_CUSTOMER_CONTRIBUTION_MARGIN:.1f}%",
            _result(contribution_observed, contribution_sufficient),
            (Competency.FINANCIAL_INSIGHT, Competency.COMMERCIAL_JUDGMENT),
            "You quantified the account's direct contribution before allocated overhead.",
            "Deduct direct customer costs from revenue, then divide by revenue for the contribution margin.",
            WORKED_CALCULATION_EXPLANATIONS["SCN-002-E-005"],
        ),
        _record(
            "SCN-002-E-006",
            _format_values(price_values),
            f"Target economics require GBP {EXPECTED_ECONOMIC_REVENUE:.2f}m revenue, GBP {EXPECTED_PRICE_INCREASE:.2f}m or {EXPECTED_PRICE_INCREASE_PERCENT:.1f}% more",
            _result(price_observed, price_sufficient),
            (Competency.FINANCIAL_INSIGHT, Competency.COMMERCIAL_JUDGMENT),
            "You translated the target margin into a precise pricing requirement.",
            "Solve direct cost / (1 - target margin), then compare that revenue with reported revenue.",
            WORKED_CALCULATION_EXPLANATIONS["SCN-002-E-006"],
        ),
        _record(
            "SCN-002-E-007",
            _format_values((answers.cost_reduction,)),
            f"The alternative cost reduction is GBP {EXPECTED_COST_REDUCTION:.2f}m within GBP 0.05m",
            _result(cost_observed, cost_sufficient),
            (Competency.FINANCIAL_INSIGHT, Competency.COMMERCIAL_JUDGMENT),
            "You quantified the cost-to-serve change needed if price is held.",
            "Calculate the allowable cost at the target margin, then compare it with direct costs.",
            WORKED_CALCULATION_EXPLANATIONS["SCN-002-E-007"],
        ),
        _record(
            "SCN-002-E-008",
            _format_values(discount_values),
            f"The extra discount costs GBP {EXPECTED_REQUESTED_DISCOUNT:.2f}m and reduces contribution margin to {EXPECTED_DISCOUNTED_CONTRIBUTION_MARGIN:.1f}%",
            _result(discount_observed, discount_sufficient),
            (Competency.FINANCIAL_INSIGHT, Competency.COMMERCIAL_JUDGMENT),
            "You quantified the disproportionate effect of the requested discount on contribution.",
            "Apply the discount to revenue, keep direct costs unchanged, then recalculate contribution margin.",
            WORKED_CALCULATION_EXPLANATIONS["SCN-002-E-008"],
        ),
        _record(
            "SCN-002-E-009",
            _format_values(sorted(answers.top_drivers)),
            "Select exactly the three largest drivers: discount, implementation overruns, and support requirements",
            _result(drivers_observed, drivers_sufficient),
            (Competency.COMMERCIAL_JUDGMENT,),
            "You prioritized the three largest quantified margin drivers.",
            "Prioritize the largest quantified value leaks rather than selecting every relevant factor.",
            judgment_explanation=JUDGMENT_EXPLANATIONS["SCN-002-E-009"],
        ),
        _record(
            "SCN-002-E-010",
            _format_values(sorted(answers.avoidable_costs)),
            "Select the four avoidable direct-cost categories and exclude retained commitments and allocated overhead",
            _result(avoidable_observed, avoidable_sufficient),
            (Competency.FINANCIAL_INSIGHT, Competency.COMMERCIAL_JUDGMENT),
            "You distinguished customer-caused costs from retained costs and allocations.",
            "Use avoidability, not allocation, when assessing the financial effect of an exit.",
            judgment_explanation=JUDGMENT_EXPLANATIONS["SCN-002-E-010"],
        ),
        _record(
            "SCN-002-E-011",
            _format_values(sorted(answers.missing_information)),
            "Select exactly customer response, capacity redeployment, and contract exit obligations",
            _result(missing_observed, missing_sufficient),
            (Competency.FINANCIAL_INSIGHT, Competency.CASH_AND_RISK_DISCIPLINE),
            "You identified the information that could materially change the commercial route.",
            "Focus on evidence that changes renewal economics, capacity deployment, or exit feasibility.",
            judgment_explanation=JUDGMENT_EXPLANATIONS["SCN-002-E-011"],
        ),
        _record(
            "SCN-002-E-012",
            _format_values((answers.recommendation.label if answers.recommendation else None,)),
            "Select Approve, Conditionally approve, Delay, or Reject",
            _result(route_sufficient, route_sufficient),
            (Competency.COMMERCIAL_JUDGMENT, Competency.STRATEGIC_LEADERSHIP),
            "You made an explicit recommendation. The route is evidence, not an automatic leadership rating.",
            "State one of the four commercial routes explicitly.",
            judgment_explanation=JUDGMENT_EXPLANATIONS["SCN-002-E-012"],
        ),
        _record(
            "SCN-002-E-013",
            _format_values(sorted(answers.safeguards)),
            "Select every core safeguard for the chosen route",
            _result(safeguards_observed, safeguards_sufficient),
            (Competency.COMMERCIAL_JUDGMENT, Competency.CASH_AND_RISK_DISCIPLINE),
            "Your safeguards meet the documented requirements for the selected route.",
            "Connect your chosen route to explicit pricing, delivery, timing, or transition controls.",
            judgment_explanation=JUDGMENT_EXPLANATIONS["SCN-002-E-013"],
        ),
        _record(
            "SCN-002-E-014",
            _format_values(sorted(answers.decision_conditions)),
            decision_condition_expectation(answers.recommendation),
            _result(conditions_observed, conditions_sufficient),
            (Competency.COMMERCIAL_JUDGMENT,),
            decision_condition_feedback(answers.recommendation),
            "Use conditions that determine whether the account creates value, not conditions based on revenue credibility alone.",
            judgment_explanation=JUDGMENT_EXPLANATIONS["SCN-002-E-014"],
        ),
        _record(
            "SCN-002-E-015",
            "All required inputs completed" if completion_observed else "One or more required inputs missing",
            "Complete every calculation, required selection, decision, safeguard, and CEO response; text presence only is checked",
            _result(completion_observed, completion_sufficient),
            (Competency.COMMERCIAL_JUDGMENT,),
            "You completed the full commercial-finance analysis sequence. Free-text quality was not evaluated.",
            "Complete each guided step before comparing your recommendation with the model response.",
        ),
    )


def _record_map(records: tuple[EvidenceRecord, ...]) -> dict[str, EvidenceRecord]:
    return {record.evidence_id: record for record in records}


def _observed(records: dict[str, EvidenceRecord], evidence_ids: Iterable[str]) -> bool:
    return all(records[evidence_id].result is EvidenceResult.OBSERVED for evidence_id in evidence_ids)


def _has_evidence(records: dict[str, EvidenceRecord], evidence_ids: Iterable[str]) -> bool:
    return any(records[evidence_id].result is not EvidenceResult.INSUFFICIENT_EVIDENCE for evidence_id in evidence_ids)


def _used_evidence(records: dict[str, EvidenceRecord], evidence_ids: Iterable[str]) -> tuple[str, ...]:
    return tuple(
        evidence_id
        for evidence_id in evidence_ids
        if records[evidence_id].result is not EvidenceResult.INSUFFICIENT_EVIDENCE
    )


def _not_assessed(competency: Competency, explanation: str, improvement: str, evidence_used: tuple[str, ...] = ()) -> CompetencyResult:
    return CompetencyResult(
        competency,
        CompetencyRating.NOT_ASSESSED,
        AssessmentSource.NOT_ASSESSED,
        evidence_used,
        explanation,
        improvement,
        "A qualified manual reviewer is required for this competency in the MVP."
        if competency in {Competency.STAKEHOLDER_COMMUNICATION, Competency.STRATEGIC_LEADERSHIP}
        else None,
    )


def identify_scenario_002_critical_omissions(
    answers: Scenario002Answers, records: tuple[EvidenceRecord, ...]
) -> tuple[str, ...]:
    by_id = _record_map(records)
    omissions: list[str] = []
    if any(by_id[item].result is EvidenceResult.NOT_OBSERVED for item in ("SCN-002-E-002", "SCN-002-E-003")):
        omissions.append("SCN-002-CO-001")
    if any(by_id[item].result is EvidenceResult.NOT_OBSERVED for item in ("SCN-002-E-005", "SCN-002-E-006", "SCN-002-E-008")):
        omissions.append("SCN-002-CO-002")
    assessed_input = any(record.result is not EvidenceResult.INSUFFICIENT_EVIDENCE for record in records)
    if answers.recommendation is None and assessed_input:
        omissions.append("SCN-002-CO-003")
    if answers.recommendation is not None and by_id["SCN-002-E-013"].result is EvidenceResult.NOT_OBSERVED:
        omissions.append("SCN-002-CO-004")
    return tuple(omissions)


def build_scenario_002_scorecard(
    records: tuple[EvidenceRecord, ...], critical_omissions: tuple[str, ...]
) -> CompetencyScorecard:
    by_id = _record_map(records)
    financial_ids = tuple(f"SCN-002-E-{number:03d}" for number in range(1, 12))
    financial_core = tuple(f"SCN-002-E-{number:03d}" for number in range(1, 9))
    if not _has_evidence(by_id, financial_ids):
        financial = _not_assessed(
            Competency.FINANCIAL_INSIGHT,
            "No meaningful company or customer economics evidence was collected.",
            "Complete the company margin and customer-economics calculations.",
        )
    elif set(critical_omissions).intersection({"SCN-002-CO-001", "SCN-002-CO-002"}) or not _observed(by_id, financial_core):
        financial = CompetencyResult(
            Competency.FINANCIAL_INSIGHT,
            CompetencyRating.DEVELOPING,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, financial_ids),
            "A core company-margin or customer-economics calculation was not observed.",
            "Reconcile revenue, direct cost, target margin, and discount impact before deciding.",
        )
    elif _observed(by_id, financial_ids):
        financial = CompetencyResult(
            Competency.FINANCIAL_INSIGHT,
            CompetencyRating.STRONG,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, financial_ids),
            "All structured company-margin, contribution, and cost-classification evidence was observed.",
            "Maintain the same traceability from customer economics to company profitability.",
        )
    else:
        financial = CompetencyResult(
            Competency.FINANCIAL_INSIGHT,
            CompetencyRating.CAPABLE,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, financial_ids),
            "The core margin and customer-economics evidence was sound, with extended interpretation incomplete.",
            "Add the driver, cost-classification, and missing-information analysis to strengthen the recommendation.",
        )

    commercial_ids = tuple(f"SCN-002-E-{number:03d}" for number in range(5, 16))
    commercial_core = ("SCN-002-E-005", "SCN-002-E-006", "SCN-002-E-008", "SCN-002-E-012", "SCN-002-E-013", "SCN-002-E-014")
    if not _has_evidence(by_id, commercial_ids):
        commercial = _not_assessed(
            Competency.COMMERCIAL_JUDGMENT,
            "No meaningful commercial-decision evidence was collected.",
            "Complete the customer economics, recommendation, safeguards, and decision conditions.",
        )
    elif set(critical_omissions).intersection({"SCN-002-CO-002", "SCN-002-CO-003", "SCN-002-CO-004"}) or not _observed(by_id, commercial_core):
        commercial = CompetencyResult(
            Competency.COMMERCIAL_JUDGMENT,
            CompetencyRating.DEVELOPING,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, commercial_ids),
            "The structured decision evidence omitted core economics, a route, conditions, or safeguards.",
            "Make the commercial route explicit and connect it to economics and operating controls.",
            "Deterministic evidence cannot evaluate executive nuance or negotiation quality.",
        )
    else:
        commercial = CompetencyResult(
            Competency.COMMERCIAL_JUDGMENT,
            CompetencyRating.CAPABLE,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, commercial_ids),
            "The structured evidence supports a complete commercial-decision path.",
            "Use qualified manual review to test the quality of tradeoffs and stakeholder challenge.",
            "Commercial Judgment is capped at Capable under deterministic MVP evaluation.",
        )

    cash_ids = ("SCN-002-E-010", "SCN-002-E-011", "SCN-002-E-013", "SCN-002-E-014")
    if not _has_evidence(by_id, cash_ids):
        cash = _not_assessed(
            Competency.CASH_AND_RISK_DISCIPLINE,
            "No material risk, avoidability, or safeguard evidence was collected.",
            "Complete the avoidable-cost, missing-information, safeguard, and decision-condition questions.",
        )
    elif "SCN-002-CO-004" in critical_omissions or not _observed(by_id, cash_ids):
        cash = CompetencyResult(
            Competency.CASH_AND_RISK_DISCIPLINE,
            CompetencyRating.DEVELOPING,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, cash_ids),
            "A structured cost-risk, information, safeguard, or decision-condition requirement was not observed.",
            "Separate avoidable from retained costs and connect uncertainties to route-specific controls.",
        )
    else:
        cash = CompetencyResult(
            Competency.CASH_AND_RISK_DISCIPLINE,
            CompetencyRating.CAPABLE,
            AssessmentSource.DETERMINISTIC,
            _used_evidence(by_id, cash_ids),
            "The structured analysis recognized retained-cost risk, missing evidence, and controls.",
            "Continue testing capacity and transition assumptions against a quantified downside case.",
        )

    stakeholder = _not_assessed(
        Competency.STAKEHOLDER_COMMUNICATION,
        "The CEO response was stored for display and self-review, not machine-scored.",
        "Use the self-review checklist or a qualified reviewer to assess communication evidence.",
    )
    strategic_evidence = tuple(
        item for item in ("SCN-002-E-011", "SCN-002-E-012") if by_id[item].result is EvidenceResult.OBSERVED
    )
    strategic = _not_assessed(
        Competency.STRATEGIC_LEADERSHIP,
        "Recommendation and missing-information evidence does not establish leadership quality.",
        "Use qualified manual review to assess ownership, alignment, and cross-functional leadership.",
        strategic_evidence,
    )
    return CompetencyScorecard((financial, commercial, cash, stakeholder, strategic))


def evaluate_scenario_002_attempt(answers: Scenario002Answers) -> EvaluationReport:
    records = evaluate_scenario_002_evidence(answers)
    omissions = identify_scenario_002_critical_omissions(answers, records)
    return EvaluationReport(records, build_scenario_002_scorecard(records, omissions), omissions)


def skipped_scenario_002_report() -> EvaluationReport:
    reason = "The learner chose skip-to-solution, so no assessed evidence was collected."
    results = tuple(
        CompetencyResult(
            competency,
            CompetencyRating.NOT_ASSESSED,
            AssessmentSource.NOT_ASSESSED,
            (),
            reason,
            "Complete a guided attempt to provide assessable evidence.",
            "Skip-to-solution is a study path, not an assessed attempt.",
        )
        for competency in Competency
    )
    return EvaluationReport((), CompetencyScorecard(results), ())
