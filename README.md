# FinanceOS

FinanceOS is planned as a long-term Finance Director and CFO simulation platform. Its first product is the Finance Director Scenario Coach: a text-based scenario coach that helps learners practice finance leadership decisions, receive structured feedback, and understand the competencies they are developing.

This repository currently contains the project foundation only. It intentionally does not include product features, a frontend, database, or external AI integration yet.

## Current Goals

- Establish a clear product and technical direction.
- Keep the initial Python architecture simple and modular.
- Make assumptions, scope, and decisions visible to future contributors.
- Prepare for future support of scenarios, scoring, learner profiles, financial packs, AI roleplay, and competency tracking.

## Repository Structure

```text
.
+-- docs/
|   +-- learning/
|   |   +-- competency-framework.md
|   |   +-- domain-framework.md
|   |   +-- scenario-design.md
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
|       +-- __init__.py
+-- tests/
|   +-- __init__.py
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
- [Scenario design](docs/learning/scenario-design.md)
- [Architecture](docs/technical/architecture.md)
- [Coding standards](docs/technical/coding-standards.md)
- [Roadmap](docs/project-management/roadmap.md)
- [Decision log](docs/project-management/decision-log.md)

## Development Setup

This project uses Python packaging through `pyproject.toml`.

```bash
python -m pip install -e ".[dev]"
pytest
```

No runtime dependencies are required yet.

## Non-Goals For The Foundation

- No frontend framework.
- No database.
- No external AI API integration.
- No scenario engine implementation.
- No placeholder services that do not serve the first text-based scenario coach.

## Status

Foundation created. Feature implementation has not started.
