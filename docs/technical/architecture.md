# Architecture

The initial architecture should support a simple text-based scenario coach while preserving clear paths to future platform capabilities.

## Current State

This repository implements a small curated scenario library with a shared typed Python core, a Scenario 001 CLI, and a Streamlit Alpha 0.1 pilot interface. Streamlit is a presentation and interaction layer only. The application has no persistence, database, authentication, telemetry, or external AI integration.

Current runtime boundaries are:

- `models.py`: typed attempts, evidence, ratings, scorecards, and scenario content.
- `scenarios/scenario_001.py` and `scenarios/scenario_002.py`: approved scenario content, finance constants, reconciliation functions, evidence metadata, and explanation content.
- `scenarios/scenario_002_evaluation.py`: Scenario 002's pure deterministic evidence and competency evaluation. `evaluation.py` remains the unchanged Scenario 001 evaluator.
- `scenarios/contracts.py`: the typed `ScenarioRegistration`, metadata, and guided-flow boundary.
- `scenarios/registry.py`: the explicit, in-code registry of approved scenarios.
- `scenarios/*_adapter.py`: scenario-specific typed answer translation and guided Streamlit questions.
- `session.py`: guided and skip-to-solution learning flows.
- `cli.py` and `__main__.py`: validated console input and application entry point. The CLI deliberately defaults to Scenario 001; it is not a scenario-library surface yet.
- `streamlit_ui.py`: scenario-library selection, in-memory browser state, shared briefing and results presentation, restart, and local summary rendering.
- `streamlit_app.py`: root Streamlit and Community Cloud entrypoint.

## Architectural Principles

- Keep the first implementation modular but small.
- Model the domain explicitly before adding infrastructure.
- Prefer plain Python modules and dataclasses before frameworks.
- Keep scenario content and scenario-specific rules separate from the shared coaching shell.
- Register each published scenario explicitly. A registration owns metadata, content, typed answer construction, deterministic evaluator, skip report, evidence labels, and guided flow.
- Do not make the shared UI aware of a scenario's finance figures, question fields, options, or evaluation rules.
- Add persistence only when there is a real need to store learner state.
- Add external AI integration only behind a clear boundary after the local learning loop is defined.

## Expected Future Boundaries

These remain possible future boundaries, not commitments to implement now:

- `scenarios`: scenario definitions, prompts, and financial context.
- `competencies`: competency definitions and mapping to rubrics.
- `evaluation`: evidence checks, competency ratings, and coaching feedback logic.
- `sessions`: learner interaction flow for a scenario attempt.
- `profiles`: learner history and competency progress, once persistence exists.
- `ai`: external AI provider integration, once needed.

## Runtime Shape

The first implementation uses this command-line interaction:

```text
scenario content -> learner response -> evaluator -> structured feedback
```

The browser pilot uses a small library boundary before preserving the same core flow:

```text
scenario library -> selected registration -> scenario-specific answers -> scenario evaluator -> evidence and scorecard -> shared Streamlit results
```

Streamlit session state retains only the current in-memory attempt and widget values. Start over clears that state. The optional plain-text summary is assembled locally from the learner's submitted answers and evaluation report; it is offered as a download and is not stored by the application.

The evaluator uses deterministic rubric logic and authored feedback that follows the [evaluation contract](../learning/evaluation-contract.md). Calculations and structured selections may be machine-assessed. Free-text communication and nuanced reasoning remain self-review or manual-review evidence in the non-AI MVP. Commercial Judgment cannot receive deterministic `Strong`; Stakeholder Communication and Strategic Leadership remain unassessed without a qualified manual reviewer. External AI is not part of this phase.

The current library contains [Scenario 001: Growth With Falling Cash](../learning/scenarios/scenario-001-growth-with-falling-cash.md) and [Scenario 002: Growth at Any Price](../learning/scenarios/scenario-002-growth-at-any-price.md). These are curated content and evaluation contracts, not arbitrary data files. They retain explicit inputs and traceability with plain Python structures rather than a general-purpose authoring engine.

## Scenario Publication Boundary

The registry is intentionally an in-code list of approved scenario registrations. FinanceOS does not yet include YAML, spreadsheet, or arbitrary-file import because authoring, validation, versioning, and approval needs are not proven.

Before a scenario is added to the registry, the Finance SME must validate the financial pack and reconciliations, and the Product Owner must validate learning intent, evidence rules, answer-leakage boundaries, explanation content, and acceptable recommendation routes. QA must verify the tested learner flow before publication.

## Data Persistence

No database is planned for the foundation or earliest MVP. If state is needed during early experiments, prefer in-memory objects or simple files before choosing a database.

## External Integrations

No external AI API integration is planned yet. When introduced, it should be isolated behind an interface that keeps provider-specific details out of core scenario and evaluation logic.

## Testing Strategy

Testing should focus on domain behavior:

- Scenario validation.
- Competency mapping.
- Evaluation output structure.
- Session flow.
- Streamlit stage flow, reset behavior, answer-leakage boundaries, and delegation to the core evaluator.

Avoid brittle tests around wording unless exact wording is a product requirement.

## Key Risks

- Overengineering before the learning loop is validated.
- Generic coaching that does not feel finance-specific.
- Competency ratings that appear precise but are not explainable.
- Deterministic evaluation presented as understanding open-ended reasoning.
- Scenario content coupled too tightly to a future AI provider.
