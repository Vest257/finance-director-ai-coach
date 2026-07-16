"""The small curated scenario library used by the Streamlit pilot."""

from __future__ import annotations

from typing import cast

from finance_director_coach.evaluation import evaluate_attempt, skipped_evaluation_report
from finance_director_coach.models import LearnerAnswers
from finance_director_coach.scenarios.contracts import ScenarioRegistration
from finance_director_coach.scenarios.scenario_001 import (
    CRITICAL_OMISSION_LABELS as SCENARIO_001_CRITICAL_OMISSION_LABELS,
    EVIDENCE_TITLES as SCENARIO_001_EVIDENCE_TITLES,
    SCENARIO_001,
    SCENARIO_METADATA as SCENARIO_001_METADATA,
)
from finance_director_coach.scenarios.scenario_001_adapter import (
    build_scenario_001_answers,
    render_scenario_001_guided_step,
    scenario_001_ceo_response,
    scenario_001_recommendation_label,
)
from finance_director_coach.scenarios.scenario_002 import (
    CRITICAL_OMISSION_LABELS as SCENARIO_002_CRITICAL_OMISSION_LABELS,
    EVIDENCE_TITLES as SCENARIO_002_EVIDENCE_TITLES,
    SCENARIO_002,
    SCENARIO_METADATA as SCENARIO_002_METADATA,
    Scenario002Answers,
)
from finance_director_coach.scenarios.scenario_002_adapter import (
    build_scenario_002_answers,
    render_scenario_002_guided_step,
    scenario_002_ceo_response,
    scenario_002_recommendation_label,
)
from finance_director_coach.scenarios.scenario_002_evaluation import (
    evaluate_scenario_002_attempt,
    skipped_scenario_002_report,
)

SCENARIO_001_REGISTRATION = ScenarioRegistration[LearnerAnswers](
    content=SCENARIO_001,
    metadata=SCENARIO_001_METADATA,
    guided_step_count=4,
    evidence_titles=SCENARIO_001_EVIDENCE_TITLES,
    critical_omission_labels=SCENARIO_001_CRITICAL_OMISSION_LABELS,
    build_answers=build_scenario_001_answers,
    evaluate_attempt=evaluate_attempt,
    skipped_report=skipped_evaluation_report,
    render_guided_step=render_scenario_001_guided_step,
    recommendation_label=scenario_001_recommendation_label,
    ceo_response=scenario_001_ceo_response,
)

SCENARIO_002_REGISTRATION = ScenarioRegistration[Scenario002Answers](
    content=SCENARIO_002,
    metadata=SCENARIO_002_METADATA,
    guided_step_count=4,
    evidence_titles=SCENARIO_002_EVIDENCE_TITLES,
    critical_omission_labels=SCENARIO_002_CRITICAL_OMISSION_LABELS,
    build_answers=build_scenario_002_answers,
    evaluate_attempt=evaluate_scenario_002_attempt,
    skipped_report=skipped_scenario_002_report,
    render_guided_step=render_scenario_002_guided_step,
    recommendation_label=scenario_002_recommendation_label,
    ceo_response=scenario_002_ceo_response,
)

SCENARIOS: tuple[ScenarioRegistration[object], ...] = (
    cast(ScenarioRegistration[object], SCENARIO_001_REGISTRATION),
    cast(ScenarioRegistration[object], SCENARIO_002_REGISTRATION),
)
SCENARIOS_BY_ID = {scenario.content.scenario_id: scenario for scenario in SCENARIOS}


def get_scenario(scenario_id: str) -> ScenarioRegistration[object]:
    """Return a registered curated scenario or fail loudly for an invalid identifier."""

    return SCENARIOS_BY_ID[scenario_id]
