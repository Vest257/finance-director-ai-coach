"""Deterministic evaluation for Scenario 002's integrated financial evidence."""

from __future__ import annotations

from collections.abc import Callable

from finance_director_coach.models import (
    AssessmentSource,
    Competency,
    CompetencyRating,
    CompetencyResult,
    CompetencyScorecard,
    EvaluationReport,
    EvidenceRecord,
    EvidenceResult,
)
from finance_director_coach.scenarios.scenario_002 import (
    BOARD_CASH_FLOOR,
    CASH_BRIDGE,
    COMPANY_RECEIVABLES,
    EXPECTED_ASSUMPTIONS,
    EXPECTED_BALANCE_SHEET_EXPOSURE,
    EXPECTED_CASH_CONVERSION,
    EXPECTED_CLASSIFICATIONS,
    EXPECTED_DSO,
    EXPECTED_EXPOSURE_AT_RISK,
    EXPECTED_NET_WORKING_CAPITAL,
    EXPECTED_OPERATING_CASH,
    EXPECTED_RECEIVABLE_CONCENTRATION,
    EXPECTED_ROUTE_PROTECTIONS,
    MONEY_TOLERANCE,
    NORTHSTAR_RECEIVABLES,
    NORTHSTAR_REVENUE,
    PERCENTAGE_TOLERANCE,
    REQUIRED_ROUTE_SAFEGUARDS,
    ROUTE_EBITDA,
    Scenario002Answers,
    cash_conversion_percent,
    customer_balance_sheet_exposure,
    customer_exposure_at_risk,
    net_customer_working_capital,
    northstar_dso,
    northstar_receivable_concentration,
    operating_cash_flow,
    route_liquidity_headroom,
    route_low_cash,
    route_operating_cash,
    route_rcf_draw,
)

ROUTES = ("renew", "renegotiate", "exit")


def _within(value: float | None, expected: float, tolerance: float) -> bool:
    return value is not None and abs(value - expected) <= tolerance + 1e-9


def _result(observed: bool, sufficient: bool) -> EvidenceResult:
    if not sufficient:
        return EvidenceResult.INSUFFICIENT_EVIDENCE
    return EvidenceResult.OBSERVED if observed else EvidenceResult.NOT_OBSERVED


def _record(
    evidence_id: str,
    learner_input: object,
    expected_rule: str,
    observed: bool,
    sufficient: bool,
    competencies: tuple[Competency, ...],
    improvement: str,
    worked_solution: str | None = None,
    judgment_explanation: str | None = None,
) -> EvidenceRecord:
    result = _result(observed, sufficient)
    feedback = (
        "The submitted evidence met the deterministic rule."
        if result is EvidenceResult.OBSERVED
        else f"The submitted evidence did not meet this rule: {expected_rule}"
    )
    return EvidenceRecord(
        evidence_id,
        str(learner_input),
        expected_rule,
        result,
        competencies,
        feedback,
        improvement,
        worked_solution,
        judgment_explanation,
    )


def _route_sufficient(values: dict[str, float]) -> bool:
    return all(route in values for route in ROUTES)


def _route_matches(
    values: dict[str, float], expected: Callable[[str], float], tolerance: float = MONEY_TOLERANCE
) -> bool:
    return all(_within(values.get(route), expected(route), tolerance) for route in ROUTES)


def evaluate_scenario_002_evidence(answers: Scenario002Answers) -> tuple[EvidenceRecord, ...]:
    route = answers.recommendation
    safeguards_observed = bool(route and REQUIRED_ROUTE_SAFEGUARDS[route].issubset(answers.safeguards))
    protections_observed = answers.protections == EXPECTED_ROUTE_PROTECTIONS and len(answers.protections) == 2
    assumptions_observed = answers.assumptions == EXPECTED_ASSUMPTIONS and len(answers.assumptions) == 2
    route_ebitda_observed = all(
        _within(answers.route_ebitda.get(route_name), ROUTE_EBITDA[route_name], MONEY_TOLERANCE)
        for route_name in ROUTES
    )
    return (
        _record("SCN-002-E-001", answers.quality_interpretation, "Recognize that earnings quality is weakened when receivables, unbilled work, and implementation cash absorb liquidity", answers.quality_interpretation == "growth_cash_divergence", answers.quality_interpretation is not None, (Competency.FINANCIAL_INSIGHT,), "Link reported profit to the cash bridge before treating growth as value creation.", judgment_explanation="Positive EBITDA is not proof of liquidity when receivables, contract assets, and capitalised implementation consume cash."),
        _record("SCN-002-E-002", answers.operating_cash_flow, f"Operating cash flow is GBP {EXPECTED_OPERATING_CASH:.2f}m within GBP 0.05m", _within(answers.operating_cash_flow, EXPECTED_OPERATING_CASH, MONEY_TOLERANCE), answers.operating_cash_flow is not None, (Competency.FINANCIAL_INSIGHT, Competency.CASH_AND_RISK_DISCIPLINE), "Add all EBITDA-to-cash bridge movements with their signs.", f"Definition: operating cash flow is the EBITDA-to-cash bridge total. GBP 3.36m - 2.40m - 1.20m + 0.40m - 0.30m - 0.80m - 0.35m - 0.25m = GBP {EXPECTED_OPERATING_CASH:.2f}m. Profit does not fund liquidity when working capital and implementation cash absorb it."),
        _record("SCN-002-E-003", answers.cash_conversion_percent, f"Cash conversion is {EXPECTED_CASH_CONVERSION:.1f}% within 0.2 percentage points", _within(answers.cash_conversion_percent, EXPECTED_CASH_CONVERSION, PERCENTAGE_TOLERANCE), answers.cash_conversion_percent is not None, (Competency.FINANCIAL_INSIGHT, Competency.CASH_AND_RISK_DISCIPLINE), "Divide operating cash by EBITDA and retain the sign.", f"Formula: GBP {EXPECTED_OPERATING_CASH:.2f}m / GBP {CASH_BRIDGE['EBITDA']:.2f}m x 100 = {EXPECTED_CASH_CONVERSION:.1f}%. Cash conversion connects earnings to liquidity."),
        _record("SCN-002-E-004", answers.largest_cash_absorber, "Identify the increase in trade receivables as the largest cash absorber", answers.largest_cash_absorber == "receivables", answers.largest_cash_absorber is not None, (Competency.CASH_AND_RISK_DISCIPLINE,), "Prioritize the largest cash movement before discussing general profitability.", judgment_explanation="Receivables are both a cash absorber and a customer-credit exposure; Northstar's overdue balance makes the link material."),
        _record("SCN-002-E-005", answers.northstar_dso, f"Northstar DSO is {EXPECTED_DSO:.1f} days", _within(answers.northstar_dso, EXPECTED_DSO, PERCENTAGE_TOLERANCE), answers.northstar_dso is not None, (Competency.FINANCIAL_INSIGHT, Competency.CASH_AND_RISK_DISCIPLINE), "Use customer receivables / annual customer revenue x 365.", f"Definition: DSO is days of revenue tied up in receivables. GBP {NORTHSTAR_RECEIVABLES:.2f}m / GBP {NORTHSTAR_REVENUE:.2f}m x 365 = {EXPECTED_DSO:.1f} days, compared with 45 contractual days."),
        _record("SCN-002-E-006", answers.receivable_concentration_percent, f"Northstar is {EXPECTED_RECEIVABLE_CONCENTRATION:.1f}% of company receivables", _within(answers.receivable_concentration_percent, EXPECTED_RECEIVABLE_CONCENTRATION, PERCENTAGE_TOLERANCE), answers.receivable_concentration_percent is not None, (Competency.CASH_AND_RISK_DISCIPLINE,), "Divide Northstar receivables by total company receivables.", f"GBP {NORTHSTAR_RECEIVABLES:.2f}m / GBP {COMPANY_RECEIVABLES:.2f}m x 100 = {EXPECTED_RECEIVABLE_CONCENTRATION:.1f}%. Customer concentration turns a collection issue into a company-liquidity issue."),
        _record("SCN-002-E-007", answers.net_working_capital, f"Net customer working-capital exposure is GBP {EXPECTED_NET_WORKING_CAPITAL:.2f}m", _within(answers.net_working_capital, EXPECTED_NET_WORKING_CAPITAL, MONEY_TOLERANCE), answers.net_working_capital is not None, (Competency.FINANCIAL_INSIGHT, Competency.CASH_AND_RISK_DISCIPLINE), "Apply the stated definition and deduct deferred revenue and the provision.", f"GBP 3.00m receivables + GBP 1.80m contract assets - GBP 0.60m deferred revenue - GBP 0.50m provision = GBP {EXPECTED_NET_WORKING_CAPITAL:.2f}m. This is a balance-sheet and cash exposure, not current P&L."),
        _record("SCN-002-E-008", (answers.balance_sheet_exposure, answers.exposure_at_risk), f"Total exposure is GBP {EXPECTED_BALANCE_SHEET_EXPOSURE:.2f}m and exposure at risk is GBP {EXPECTED_EXPOSURE_AT_RISK:.2f}m", _within(answers.balance_sheet_exposure, EXPECTED_BALANCE_SHEET_EXPOSURE, MONEY_TOLERANCE) and _within(answers.exposure_at_risk, EXPECTED_EXPOSURE_AT_RISK, MONEY_TOLERANCE), answers.balance_sheet_exposure is not None and answers.exposure_at_risk is not None, (Competency.FINANCIAL_INSIGHT, Competency.CASH_AND_RISK_DISCIPLINE), "Separate total customer exposure from recoverability assumptions.", f"Total: GBP {EXPECTED_NET_WORKING_CAPITAL:.2f}m + GBP 1.00m capitalised implementation = GBP {EXPECTED_BALANCE_SHEET_EXPOSURE:.2f}m. At risk: GBP 0.60m receivables + GBP 0.90m contract assets + GBP 0.30m impairment + GBP 0.50m provision = GBP {EXPECTED_EXPOSURE_AT_RISK:.2f}m."),
        _record("SCN-002-E-009", (answers.route_ebitda, answers.route_operating_cash), "Reconcile all three annual EBITDA and operating-cash route outcomes", route_ebitda_observed and _route_matches(answers.route_operating_cash, route_operating_cash), _route_sufficient(answers.route_ebitda) and _route_sufficient(answers.route_operating_cash), (Competency.FINANCIAL_INSIGHT, Competency.COMMERCIAL_JUDGMENT), "Compare both earnings and operating cash for every route.", f"Annual EBITDA: renew GBP 2.91m, renegotiate GBP 5.27m, exit GBP 3.06m. Operating cash: renew GBP {route_operating_cash('renew'):.2f}m, renegotiate GBP {route_operating_cash('renegotiate'):.2f}m, exit GBP {route_operating_cash('exit'):.2f}m. Commercial terms alter both earnings and working-capital cash."),
        _record("SCN-002-E-010", answers.route_low_cash, "Reconcile the lowest monthly cash point for all three routes", _route_matches(answers.route_low_cash, route_low_cash), _route_sufficient(answers.route_low_cash), (Competency.CASH_AND_RISK_DISCIPLINE,), "Apply route monthly adjustments to the baseline and select the lowest month.", f"Low cash points: renew GBP {route_low_cash('renew'):.2f}m, renegotiate GBP {route_low_cash('renegotiate'):.2f}m, exit GBP {route_low_cash('exit'):.2f}m. The monthly trough matters more than the year-end balance."),
        _record("SCN-002-E-011", (answers.route_rcf_draw, answers.route_headroom), "Reconcile RCF draw and remaining headroom for all routes", _route_matches(answers.route_rcf_draw, route_rcf_draw) and _route_matches(answers.route_headroom, route_liquidity_headroom), _route_sufficient(answers.route_rcf_draw) and _route_sufficient(answers.route_headroom), (Competency.CASH_AND_RISK_DISCIPLINE,), "Use the board floor to calculate draw, then deduct it from undrawn RCF.", f"Board floor: GBP {BOARD_CASH_FLOOR:.2f}m. RCF draw/headroom: renew GBP {route_rcf_draw('renew'):.2f}m / GBP {route_liquidity_headroom('renew'):.2f}m; renegotiate GBP {route_rcf_draw('renegotiate'):.2f}m / GBP {route_liquidity_headroom('renegotiate'):.2f}m; exit GBP {route_rcf_draw('exit'):.2f}m / GBP {route_liquidity_headroom('exit'):.2f}m. Undrawn RCF is capacity, not permanent value."),
        _record("SCN-002-E-012", answers.classifications, "Select exactly implementation cash, receivables, and deferred revenue", answers.classifications == EXPECTED_CLASSIFICATIONS and len(answers.classifications) == 3, bool(answers.classifications), (Competency.FINANCIAL_INSIGHT,), "Classify the accounting and cash treatment, not the operational label.", judgment_explanation="Capitalised implementation can hide current cash consumption; deferred revenue can provide cash before revenue recognition."),
        _record("SCN-002-E-013", route.label if route else None, "Select one commercial recommendation route", route is not None, route is not None, (Competency.COMMERCIAL_JUDGMENT,), "Make a route explicit without treating it as an automatic leadership rating.", judgment_explanation="Different routes can be defensible because collection, recovery, commercial repair, and redeployment remain uncertain."),
        _record("SCN-002-E-014", answers.safeguards, "Select every commercial and liquidity safeguard for the selected route", safeguards_observed, bool(route and answers.safeguards), (Competency.COMMERCIAL_JUDGMENT, Competency.CASH_AND_RISK_DISCIPLINE), "Connect the route to economics, collections, and a board-floor control.", judgment_explanation="A Finance Director safeguard must cover both commercial economics and liquidity consequences."),
        _record("SCN-002-E-015", (answers.protections, answers.assumptions), "Select exactly cash/receivables protections and the two assumptions most likely to change the decision", protections_observed and assumptions_observed, bool(answers.protections or answers.assumptions), (Competency.COMMERCIAL_JUDGMENT, Competency.CASH_AND_RISK_DISCIPLINE), "Prioritize collection and redeployment uncertainty rather than revenue credibility.", judgment_explanation="RCF is liquidity capacity, not permanent value; recovery timing and capacity cash conversion determine whether it is needed."),
    )


def evaluate_scenario_002_attempt(answers: Scenario002Answers) -> EvaluationReport:
    records = evaluate_scenario_002_evidence(answers)
    by_id = {record.evidence_id: record for record in records}
    observed = lambda ids: all(by_id[evidence_id].result is EvidenceResult.OBSERVED for evidence_id in ids)
    integrated = ("SCN-002-E-002", "SCN-002-E-003", "SCN-002-E-005", "SCN-002-E-007", "SCN-002-E-008", "SCN-002-E-009", "SCN-002-E-010", "SCN-002-E-011")
    omissions: list[str] = []
    if not observed(("SCN-002-E-002", "SCN-002-E-009")): omissions.append("SCN-002-CO-001")
    if not observed(("SCN-002-E-007", "SCN-002-E-008")): omissions.append("SCN-002-CO-002")
    if answers.recommendation is None: omissions.append("SCN-002-CO-003")
    if answers.recommendation and not observed(("SCN-002-E-014", "SCN-002-E-015")): omissions.append("SCN-002-CO-004")
    financial = CompetencyResult(Competency.FINANCIAL_INSIGHT, CompetencyRating.STRONG if observed(integrated) else CompetencyRating.DEVELOPING, AssessmentSource.DETERMINISTIC, integrated, "Integrated P&L, balance-sheet, cash-flow, and liquidity evidence was assessed.", "Reconcile cash conversion, customer exposure, and route liquidity together.")
    commercial_ids = ("SCN-002-E-009", "SCN-002-E-013", "SCN-002-E-014", "SCN-002-E-015")
    commercial = CompetencyResult(Competency.COMMERCIAL_JUDGMENT, CompetencyRating.CAPABLE if observed(commercial_ids) else CompetencyRating.DEVELOPING, AssessmentSource.DETERMINISTIC, commercial_ids, "Structured commercial route evidence was assessed.", "Connect the route to commercial and liquidity controls.", "Commercial Judgment is capped at Capable under deterministic MVP evaluation.")
    cash_ids = ("SCN-002-E-002", "SCN-002-E-008", "SCN-002-E-010", "SCN-002-E-011", "SCN-002-E-015")
    cash = CompetencyResult(Competency.CASH_AND_RISK_DISCIPLINE, CompetencyRating.CAPABLE if observed(cash_ids) else CompetencyRating.DEVELOPING, AssessmentSource.DETERMINISTIC, cash_ids, "Cash and liquidity evidence was assessed.", "Test cash troughs, RCF capacity, and recoverability assumptions.")
    reason = "The CEO response was stored for self-review, not machine-scored."
    not_assessed = lambda competency: CompetencyResult(competency, CompetencyRating.NOT_ASSESSED, AssessmentSource.NOT_ASSESSED, (), reason, "Use qualified manual review for this competency.")
    return EvaluationReport(records, CompetencyScorecard((financial, commercial, cash, not_assessed(Competency.STAKEHOLDER_COMMUNICATION), not_assessed(Competency.STRATEGIC_LEADERSHIP))), tuple(omissions))


def skipped_scenario_002_report() -> EvaluationReport:
    reason = "The learner chose skip-to-solution, so no assessed evidence was collected."
    results = tuple(CompetencyResult(competency, CompetencyRating.NOT_ASSESSED, AssessmentSource.NOT_ASSESSED, (), reason, "Complete a guided attempt to provide assessable evidence.") for competency in Competency)
    return EvaluationReport((), CompetencyScorecard(results), ())
