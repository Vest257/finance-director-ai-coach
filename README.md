# FinanceOS

FinanceOS is planned as a long-term Finance Director and CFO simulation platform. Its first product is the Finance Director Scenario Coach: a scenario coach that helps learners practice finance leadership decisions, receive structured feedback, and understand the competencies they are developing.

This repository contains FinanceOS Alpha 0.1: a curated two-scenario Streamlit Scenario Coach library, the original Scenario 001 command-line interface, and a separate Streamlit Practice surface for short deterministic finance drills. These learner surfaces use in-memory state and deterministic evaluation cores. The product has no database, cross-session persistence, authentication, telemetry, or external AI integration.

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
|   |       +-- scenario-002-growth-at-any-price.md
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
+-- data/
|   +-- drills/
|       +-- finqa_cards_v1.json
|       +-- finqa_v1_curation.json
+-- scripts/
|   +-- import_finqa.py
+-- src/
|   +-- finance_director_coach/
|       +-- scenarios/
|       |   +-- scenario_001.py
|       |   +-- scenario_002.py
|       |   +-- registry.py
|       +-- __init__.py
|       +-- __main__.py
|       +-- cli.py
|       +-- evaluation.py
|       +-- models.py
|       +-- practice.py
|       +-- practice_ui.py
|       +-- session.py
|       +-- streamlit_ui.py
+-- tests/
|   +-- test_cli.py
|   +-- test_evaluation.py
|   +-- test_finqa_drills.py
|   +-- test_practice.py
|   +-- test_practice_ui.py
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
- [Scenario 002: Growth at Any Price](docs/learning/scenarios/scenario-002-growth-at-any-price.md)
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

Use the Streamlit navigation to switch between **Scenario Coach** and **Practice**. Scenario Coach begins with a curated library and supports Scenario 001 and Scenario 002 guided attempts, skip-to-solution study paths, deterministic feedback, competency scorecards, complete learning reviews, restart to the library, and locally generated plain-text tester summaries. Practice uses the committed reviewed 100-card FinQA bank, filters by finance domain, financial skill, and difficulty, and checks numerical answers deterministically. Practice shows a card-specific interpretation after submission and keeps its attempt history only for the current browser session.

The scenario is fictional. Pilot testers must not enter confidential, personal, or employer information.

## Run The CLI

```bash
python -m finance_director_coach
```

The CLI deliberately defaults to Scenario 001. Choose the guided path to complete an assessed attempt, or skip to the solution for study without collecting learner evidence.

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
- No persistent or cross-session learner history; Practice attempts remain only in the current browser session.
- No user accounts, authentication, or telemetry.
- No external AI API integration.
- The browser scenario library contains two curated synthetic scenarios; it does not yet import arbitrary scenario files, YAML, or spreadsheets.
- Scenario Coach **Start over** clears Scenario Coach state only. Practice has its own clear-history action, and the two surfaces preserve each other's namespaced state.
- All in-memory state disappears when the browser session ends; nothing persists across browser sessions.
- The downloadable summary is generated locally and is not stored by FinanceOS.
- Unrestricted free-text reasoning is stored for display and self-review but is not automatically evaluated.
- Commercial Judgment is capped at `Capable` under deterministic evaluation; `Strong` requires qualified manual review.
- Stakeholder Communication and Strategic Leadership remain `Not assessed` without qualified manual review.
- No overall numerical score is produced.

## Status

Phase 0 is complete and Phase 1 remains current. The Scenario 001 CLI, the two-scenario Streamlit Scenario Coach library, Fast Drill Mode V1, and the learner-tested four-card clarity and documentation cleanup are merged.
