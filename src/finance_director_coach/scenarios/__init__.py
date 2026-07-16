"""Curated Finance Director scenarios.

The command-line experience deliberately defaults to Scenario 001. The browser pilot
uses :mod:`finance_director_coach.scenarios.registry` to expose the current library.
"""

from finance_director_coach.scenarios.scenario_001 import SCENARIO_001
from finance_director_coach.scenarios.scenario_002 import SCENARIO_002

__all__ = ["SCENARIO_001", "SCENARIO_002"]
