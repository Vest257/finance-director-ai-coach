# FinanceOS

FinanceOS is planned as a long-term Finance Director and CFO simulation platform. Its first product is the Finance Director Scenario Coach: a scenario coach that helps learners practice finance leadership decisions, receive structured feedback, and understand the competencies they are developing.

This repository contains FinanceOS Alpha 0.1: Scenario 001 through both the original command-line interface and a Streamlit pilot interface for small-group browser testing. Both interfaces reuse the same in-memory scenario and deterministic evaluation core. The product has no database, persistence, authentication, telemetry, or external AI integration.

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
|       +-- streamlit_ui.py
+-- tests/
|   +-- test_cli.py
|   +-- test_evaluation.py
|   +-- test_scenario_financials.py
|   +-- test_streamlit_ui.py
+-- streamlit_app.py
+-- requirements.txt
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

Streamlit is the only direct runtime dependency. The root `requirements.txt` delegates installation back to this package so `pyproject.toml` remains the dependency source of truth for local and Community Cloud installs.

## Run The Browser Pilot

```bash
streamlit run streamlit_app.py
```

The browser pilot supports the guided attempt, skip-to-solution study path, deterministic feedback, competency scorecard, complete learning review, restart, and a locally generated plain-text tester summary.

The scenario is fictional. Pilot testers must not enter confidential, personal, or employer information.

## Run The CLI

```bash
python -m finance_director_coach
```

Choose the guided path to complete an assessed attempt, or skip to the solution for study without collecting learner evidence.

## Deploy On Streamlit Community Cloud

1. Open [Streamlit Community Cloud](https://share.streamlit.io/) and create an app from this GitHub repository.
2. Select the branch to deploy and set the entrypoint to `streamlit_app.py`.
3. Select Python 3.12 in Advanced settings to match the validated pilot environment.
4. Leave secrets and environment variables empty; this pilot has no external integrations.
5. Deploy and verify both the guided and skip-to-solution paths before sharing the link.

Community Cloud runs the entrypoint from the repository root. The one-line `requirements.txt` installs this project and its pinned Streamlit dependency from `pyproject.toml`.

## Run Tests

```bash
pytest
python -m compileall src tests streamlit_app.py
```

## Current MVP Limitations

- No database.
- No learner persistence or attempt history.
- No user accounts, authentication, or telemetry.
- No external AI API integration.
- Scenario 001 is the only implemented learning experience.
- Browser state exists only for the current Streamlit session and is cleared by Start over.
- The downloadable summary is generated locally and is not stored by FinanceOS.
- Unrestricted free-text reasoning is stored for display and self-review but is not automatically evaluated.
- Commercial Judgment is capped at `Capable` under deterministic evaluation; `Strong` requires qualified manual review.
- Stakeholder Communication and Strategic Leadership remain `Not assessed` without qualified manual review.
- No overall numerical score is produced.

## Status

Phase 0 is complete. Phase 1 remains current. The Scenario 001 CLI vertical slice is merged, and the Streamlit interface is the Alpha 0.1 pilot surface for small-group learner testing.
