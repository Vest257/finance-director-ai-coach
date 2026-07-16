# Architecture

The initial architecture should support a simple text-based scenario coach while preserving clear paths to future platform capabilities.

## Current State

This repository implements Scenario 001 with a shared typed Python core, a CLI, and a Streamlit Alpha 0.1 pilot interface. Streamlit is a presentation and interaction layer only. The application has no persistence, database, authentication, telemetry, or external AI integration.

Current runtime boundaries are:

- `models.py`: typed attempts, evidence, ratings, scorecards, and scenario content.
- `scenarios/scenario_001.py`: approved content, options, finance constants, and reconciliation functions.
- `evaluation.py`: pure deterministic evidence and competency evaluation.
- `session.py`: guided and skip-to-solution learning flows.
- `cli.py` and `__main__.py`: validated console input and application entry point.
- `streamlit_ui.py`: in-memory browser interaction and rendering over the existing content, models, and evaluator.
- `practice.py`: pure drill-bank loading, filtering, answer checking, sequencing, and session-attempt helpers.
- `practice_ui.py`: the separate in-memory Streamlit Practice surface.
- `streamlit_app.py`: root Streamlit and Community Cloud entrypoint; owns navigation between Scenario Coach and Practice.

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

## Runtime Shape

The first implementation uses this command-line interaction:

```text
scenario content -> learner response -> evaluator -> structured feedback
```

The browser pilot preserves the same core flow:

```text
Streamlit widgets -> LearnerAnswers -> evaluator -> evidence and scorecard -> Streamlit results
```

Streamlit session state retains only the current in-memory attempt and widget values. Start over clears that state. The optional plain-text summary is assembled locally from the learner's submitted answers and evaluation report; it is offered as a download and is not stored by the application.

Fast Drill Mode V1 is a separate page-navigated Practice surface. It uses the committed reviewed `data/drills/finqa_cards_v1.json` bank and deterministic core functions for filtering, tolerance checks, and stable card sequencing. The bank is generated deterministically from the committed FinQA fixture and authored `data/drills/finqa_v1_curation.json` ledger; generated-bank changes must use that importer-and-curation workflow. Practice attempts exist only in namespaced Streamlit session state for the browser session, so they cannot interfere with the Scenario Coach's current in-memory attempt and widgets. Each learning surface resets only the state it owns: Scenario Coach preserves all `practice_*` keys, and Practice leaves Scenario Coach keys unchanged. No state persists across browser sessions. The mode has no persistence, accounts, learner profile, adaptive sequencing, streaks, leaderboard, or overall learner score.

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
- Streamlit stage flow, reset behavior, answer-leakage boundaries, and delegation to the core evaluator.
- FinQA-bank reconciliation, provenance and taxonomy, deterministic regeneration, and unit normalization.
- Practice history and state isolation.

Avoid brittle tests around wording unless exact wording is a product requirement.

## Key Risks

- Overengineering before the learning loop is validated.
- Generic coaching that does not feel finance-specific.
- Competency ratings that appear precise but are not explainable.
- Deterministic evaluation presented as understanding open-ended reasoning.
- Scenario content coupled too tightly to a future AI provider.
