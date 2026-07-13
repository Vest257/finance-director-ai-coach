# Architecture

The initial architecture should support a simple text-based scenario coach while preserving clear paths to future platform capabilities.

## Current State

This repository implements the first Scenario 001 CLI vertical slice using standard-library Python. It has no frontend, persistence, database, authentication, telemetry, or external AI integration.

Current runtime boundaries are:

- `models.py`: typed attempts, evidence, ratings, scorecards, and scenario content.
- `scenarios/scenario_001.py`: approved content, options, finance constants, and reconciliation functions.
- `evaluation.py`: pure deterministic evidence and competency evaluation.
- `session.py`: guided and skip-to-solution learning flows.
- `cli.py` and `__main__.py`: validated console input and application entry point.

## Architectural Principles

- Keep the first implementation modular but small.
- Model the domain explicitly before adding infrastructure.
- Prefer plain Python modules and dataclasses before frameworks.
- Keep scenario content separate from coaching logic once implementation begins.
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

## Initial Runtime Shape

The first implementation uses this command-line interaction:

```text
scenario content -> learner response -> evaluator -> structured feedback
```

The evaluator uses deterministic rubric logic and authored feedback that follows the [evaluation contract](../learning/evaluation-contract.md). Calculations and structured selections may be machine-assessed. Free-text communication and nuanced reasoning remain self-review or manual-review evidence in the non-AI MVP. Commercial Judgment cannot receive deterministic `Strong`; Stakeholder Communication and Strategic Leadership remain unassessed without a qualified manual reviewer. External AI is not part of this phase.

Scenario 001 is specified in [Scenario 001: Growth With Falling Cash](../learning/scenarios/scenario-001-growth-with-falling-cash.md). That document is a content and evaluation contract, not a commitment to new infrastructure. The first implementation should support its explicit inputs and evidence traceability with plain Python structures before considering general-purpose authoring systems.

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

Avoid brittle tests around wording unless exact wording is a product requirement.

## Key Risks

- Overengineering before the learning loop is validated.
- Generic coaching that does not feel finance-specific.
- Competency ratings that appear precise but are not explainable.
- Deterministic evaluation presented as understanding open-ended reasoning.
- Scenario content coupled too tightly to a future AI provider.
