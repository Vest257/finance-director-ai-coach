"""Scenario 001 learning-session orchestration."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from finance_director_coach.evaluation import evaluate_attempt, skipped_evaluation_report
from finance_director_coach.models import EvaluationReport, LearnerAnswers, RecommendationRoute
from finance_director_coach.scenarios.scenario_001 import (
    CASH_DRIVER_OPTIONS,
    HIRING_UNIT_WARNING,
    MISSING_INFORMATION_OPTIONS,
    MONETARY_INPUT_GUIDANCE,
    RECOMMENDATION_OPTIONS,
    RISK_OPTIONS,
    ROUTE_SAFEGUARD_OPTIONS,
    SCENARIO_001,
    THRESHOLD_OPTIONS,
    TRADEOFF_OPTIONS,
)


class SessionIO(Protocol):
    def write(self, text: str = "") -> None: ...

    def ask_number(self, prompt: str) -> float: ...

    def choose_one(self, prompt: str, options: Mapping[str, str]) -> str: ...

    def choose_many(self, prompt: str, options: Mapping[str, str]) -> frozenset[str]: ...

    def ask_text(self, prompt: str) -> str: ...


@dataclass(frozen=True)
class SessionResult:
    skipped: bool
    answers: LearnerAnswers | None
    report: EvaluationReport


class Scenario001Session:
    def __init__(self, interaction: SessionIO) -> None:
        self.io = interaction

    def run(self) -> SessionResult:
        self._show_scenario()
        path = self.io.choose_one(
            "Choose how you want to work through the scenario:",
            {
                "guided": "Guided attempt with deterministic evidence feedback",
                "skip": "Skip to solution for study",
            },
        )
        if path == "skip":
            report = skipped_evaluation_report()
            self._show_skip_output(report)
            return SessionResult(skipped=True, answers=None, report=report)

        answers = self._collect_guided_answers()
        report = evaluate_attempt(answers)
        self._show_guided_output(answers, report)
        return SessionResult(skipped=False, answers=answers, report=report)

    def _show_scenario(self) -> None:
        self.io.write(f"\nScenario 001 | {SCENARIO_001.title}")
        self.io.write("=" * 72)
        self.io.write(f"\nLearner role\n{SCENARIO_001.learner_role}")
        self.io.write(f"\nCompany context\n{SCENARIO_001.company_context}")
        self.io.write("\nFinancial pack")
        for section in SCENARIO_001.financial_pack:
            self.io.write(f"\n{section.title}\n{'-' * len(section.title)}\n{section.body}")
        self.io.write(f"\nCEO question\n{SCENARIO_001.initial_question}")

    def _collect_guided_answers(self) -> LearnerAnswers:
        self.io.write("\nGuided analysis")
        self.io.write(MONETARY_INPUT_GUIDANCE)
        self.io.write("Negative cash flow should include a minus sign.")

        revenue_growth = self.io.ask_number("Revenue growth percentage: ")
        ebitda_growth = self.io.ask_number("EBITDA growth percentage: ")
        cash_decrease = self.io.ask_number("Cash decrease, as a positive GBP m amount: ")
        operating_cash = self.io.ask_number("Operating cash before interest and tax, GBP m: ")
        net_operating_cash = self.io.ask_number("Net operating cash after interest and tax, GBP m: ")

        cash_drivers = self.io.choose_many(
            "Select all movements that belong in the working-capital explanation:",
            CASH_DRIVER_OPTIONS,
        )
        largest_driver = self.io.choose_one(
            "Select the largest cash-use movement:",
            {
                "receivables": "Trade receivables",
                "inventory": "Inventory",
                "contract_assets": "Contract assets and prepayments",
                "capital_expenditure": "Capital expenditure",
            },
        )
        risks = self.io.choose_many("Select all material risks supported by the pack:", RISK_OPTIONS)

        self.io.write("\nHiring and liquidity")
        self.io.write(HIRING_UNIT_WARNING)
        h2_hiring_cost = self.io.ask_number("H2 2026 hiring cost, GBP m: ")
        annual_hiring_cost = self.io.ask_number("Annual recurring hiring cost, GBP m: ")
        cash_low_point = self.io.ask_number("Hiring-case cash low point, GBP m: ")
        december_cash = self.io.ask_number("Hiring-case December cash, GBP m: ")
        board_shortfall = self.io.ask_number("Shortfall below the board cash floor, GBP m: ")
        lender_headroom = self.io.ask_number("Headroom above the lender minimum at the low point, GBP m: ")
        threshold_interpretations = self.io.choose_many(
            "Select all correct threshold statements:", THRESHOLD_OPTIONS
        )

        recommendation_key = self.io.choose_one("Choose your recommendation:", RECOMMENDATION_OPTIONS)
        recommendation = RecommendationRoute(recommendation_key)
        safeguards = self.io.choose_many(
            f"Select safeguards for '{recommendation.label}':",
            ROUTE_SAFEGUARD_OPTIONS[recommendation],
        )
        missing_information = self.io.choose_many(
            "Select the information that would materially improve the decision:",
            MISSING_INFORMATION_OPTIONS,
        )
        tradeoffs = self.io.choose_many(
            "Select the commercial tradeoffs and alternatives you would address:",
            TRADEOFF_OPTIONS,
        )
        ceo_response = self.io.ask_text(
            "Give the CEO your concise recommendation. This text is stored for self-review and is not automatically scored:\n> "
        )

        return LearnerAnswers(
            revenue_growth_percent=revenue_growth,
            ebitda_growth_percent=ebitda_growth,
            cash_decrease=cash_decrease,
            operating_cash_before_interest_tax=operating_cash,
            net_operating_cash=net_operating_cash,
            cash_drivers=cash_drivers,
            largest_cash_driver=largest_driver,
            risks=risks,
            h2_hiring_cost=h2_hiring_cost,
            annual_hiring_cost=annual_hiring_cost,
            cash_low_point=cash_low_point,
            december_cash=december_cash,
            board_floor_shortfall=board_shortfall,
            lender_headroom=lender_headroom,
            threshold_interpretations=threshold_interpretations,
            recommendation=recommendation,
            safeguards=safeguards,
            missing_information=missing_information,
            tradeoffs=tradeoffs,
            ceo_response=ceo_response,
        )

    def _show_guided_output(self, answers: LearnerAnswers, report: EvaluationReport) -> None:
        self.io.write("\nDeterministic evidence feedback")
        self.io.write("=" * 72)
        for record in report.evidence_records:
            self.io.write(f"\n[{record.evidence_id}] {record.result.value}")
            self.io.write(f"Rule: {record.expected_rule}")
            self.io.write(f"Your evidence: {record.learner_input}")
            self.io.write(f"Why: {record.feedback}")
            self.io.write(f"Next step: {record.improvement_guidance}")
            if record.worked_solution is not None:
                self.io.write(f"Worked calculation:\n{record.worked_solution}")
        if report.critical_omissions:
            self.io.write(f"\nCritical omission gates triggered: {', '.join(report.critical_omissions)}")

        self._show_scorecard(report)
        self.io.write(f"\nYour CEO response (not automatically scored)\n{answers.ceo_response}")
        self._show_learning_output()

    def _show_skip_output(self, report: EvaluationReport) -> None:
        self.io.write("\nSkip-to-solution study path")
        self.io.write("No assessed learner evidence was collected.")
        self.io.write(f"\nFinancial reconciliation\n{SCENARIO_001.reconciliation_summary}")
        self._show_scorecard(report)
        self._show_learning_output()

    def _show_scorecard(self, report: EvaluationReport) -> None:
        self.io.write("\nQualitative competency scorecard")
        self.io.write("=" * 72)
        for result in report.scorecard.results:
            self.io.write(
                f"\n{result.competency.value}: {result.rating.value} "
                f"[source: {result.assessment_source.value}]"
            )
            evidence = ", ".join(result.evidence_used) if result.evidence_used else "None"
            self.io.write(f"Evidence used: {evidence}")
            self.io.write(f"Why: {result.explanation}")
            self.io.write(f"Improve: {result.improvement_guidance}")
            if result.limitation:
                self.io.write(f"Limitation: {result.limitation}")

    def _show_learning_output(self) -> None:
        self.io.write(f"\nModel Finance Director answer\n{'=' * 72}\n{SCENARIO_001.model_answer}")
        self.io.write(f"\nFull debrief\n{'=' * 72}\n{SCENARIO_001.debrief}")
        self.io.write("\nSelf-review checklist [source: self-review]")
        for item in SCENARIO_001.self_review_checklist:
            self.io.write(f"- {item}")
        self.io.write("\nLearner action plan")
        for index, item in enumerate(SCENARIO_001.action_plan, start=1):
            self.io.write(f"{index}. {item}")
