# FinanceOS

FinanceOS is planned as a long-term Finance Director and CFO simulation platform. Its first product is the Finance Director Scenario Coach: a text-based scenario coach that helps learners practice finance leadership decisions, receive structured feedback, and understand the competencies they are developing.

This repository contains the first Phase 1 vertical slice: a command-line implementation of Scenario 001. It intentionally does not include a frontend, database, persistence, or external AI integration.

## Current Goals

- Establish a clear product and technical direction.
- Keep the initial Python architecture simple and modular.
- Make assumptions, scope, and decisions visible to future contributors.
- Prepare for future support of scenarios, evaluation, learner profiles, financial packs, AI roleplay, and competency tracking.

## Repository Structure

```text
.
+-- docs/
|   +-- learning/
|   |   +-- competency-framework.md
|   |   +-- domain-framework.md
|   |   +-- evaluation-contract.md
|   |   +-- scenario-design.md
|   |   +-- scenarios/
|   |       +-- scenario-001-growth-with-falling-cash.md
|   +-- product/
|   |   +-- mvp-scope.md
|   |   +-- product-principles.md
|   |   +-- target-user.md
|   |   +-- vision.md
|   +-- project-management/
|   |   +-- decision-log.md
|   |   +-- roadmap.md
|   +-- technical/
|       +-- architecture.md
|       +-- coding-standards.md
+-- src/
|   +-- finance_director_coach/
|       +-- scenarios/
|       |   +-- scenario_001.py
|       +-- __init__.py
|       +-- __main__.py
|       +-- cli.py
|       +-- evaluation.py
|       +-- models.py
|       +-- session.py
+-- tests/
|   +-- test_cli.py
|   +-- test_evaluation.py
|   +-- test_scenario_financials.py
+-- AGENTS.md
+-- pyproject.toml
+-- .gitignore
```

## Documentation Map

- [Product vision](docs/product/vision.md)
- [Product principles](docs/product/product-principles.md)
- [Target user](docs/product/target-user.md)
- [MVP scope](docs/product/mvp-scope.md)
- [Competency framework](docs/learning/competency-framework.md)
- [Learning domain framework](docs/learning/domain-framework.md)
- [Evaluation contract](docs/learning/evaluation-contract.md)
- [Scenario design](docs/learning/scenario-design.md)
- [Scenario 001: Growth With Falling Cash](docs/learning/scenarios/scenario-001-growth-with-falling-cash.md)
- [Architecture](docs/technical/architecture.md)
- [Coding standards](docs/technical/coding-standards.md)
- [Roadmap](docs/project-management/roadmap.md)
- [Decision log](docs/project-management/decision-log.md)

## Installation

This project uses Python packaging through `pyproject.toml`.

```bash
python -m pip install -e ".[dev]"
```

The application has no runtime dependencies outside the Python standard library.

## Run Scenario 001

```bash
python -m finance_director_coach
```

Choose the guided path to complete an assessed attempt, or skip to the solution for study without collecting learner evidence.

## Run Tests

```bash
pytest
python -m compileall src tests
```

## Current MVP Limitations

- No frontend framework.
- No database.
- No learner persistence or attempt history.
- No external AI API integration.
- Scenario 001 is the only implemented learning experience.
- Unrestricted free-text reasoning is stored for display and self-review but is not automatically evaluated.
- Commercial Judgment is capped at `Capable` under deterministic evaluation; `Strong` requires qualified manual review.
- Stakeholder Communication and Strategic Leadership remain `Not assessed` without qualified manual review.
- No overall numerical score is produced.

## Status

Phase 0 is complete. Phase 1 remains current, with the Scenario 001 CLI vertical slice implemented for pull-request review.
