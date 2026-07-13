# Architecture

The initial architecture should support a simple text-based scenario coach while preserving clear paths to future platform capabilities.

## Current State

This repository currently contains documentation, packaging configuration, and an empty Python package. It does not implement runtime features yet.

## Architectural Principles

- Keep the first implementation modular but small.
- Model the domain explicitly before adding infrastructure.
- Prefer plain Python modules and dataclasses before frameworks.
- Keep scenario content separate from coaching logic once implementation begins.
- Add persistence only when there is a real need to store learner state.
- Add external AI integration only behind a clear boundary after the local learning loop is defined.

## Expected Future Boundaries

These are likely future module boundaries, not commitments to implement now:

- `scenarios`: scenario definitions, prompts, and financial context.
- `competencies`: competency definitions and mapping to rubrics.
- `evaluation`: scoring and coaching feedback logic.
- `sessions`: learner interaction flow for a scenario attempt.
- `profiles`: learner history and competency progress, once persistence exists.
- `ai`: external AI provider integration, once needed.

## Initial Runtime Shape

When feature implementation begins, start with a simple command-line or text-based interaction:

```text
scenario content -> learner response -> evaluator -> structured feedback
```

The evaluator may begin as deterministic rubric logic or manually authored feedback patterns. External AI should not be introduced until the expected evaluation contract is clear.

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
- Scoring that appears precise but is not explainable.
- Scenario content coupled too tightly to a future AI provider.
