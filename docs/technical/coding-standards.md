# Coding Standards

## Python Version

Use Python 3.11 or newer.

## Style

- Prefer clear, typed Python.
- Keep functions small and named for domain intent.
- Use dataclasses or simple typed structures for domain objects where helpful.
- Avoid global mutable state.
- Avoid framework dependencies until a concrete use case exists.

## Type Hints

Use type hints for public functions, domain models, and module boundaries. Prefer standard library types where possible.

## Testing

Use `pytest`.

Tests should:

- Validate behavior, not implementation details.
- Cover domain rules and edge cases.
- Be easy to read as examples of intended behavior.
- Avoid network calls.

For shared presentation or learner-flow work, parameterize tests across every registered scenario where practical. Validate each affected scenario in both the briefing and guided financial-pack reference, including the absence of code-style pack blocks, editable tables, unintended indexes, and answer leakage. Visually inspect affected scenarios on desktop and at approximately 390px width; if browser automation is unavailable, record the visual validation as outstanding.

Keep financial calculations, evidence rules, and authored content in their owning scenario. Shared UI and presentation-model work must not copy one scenario's finance or evaluation behavior into another.

## Documentation

Update docs when decisions change. Important product or architecture decisions belong in `docs/project-management/decision-log.md`.

## Dependencies

Keep dependencies minimal. A dependency should be added only when it clearly reduces risk, complexity, or maintenance burden.

## Module Design

Before adding a module, identify:

- The domain concept it owns.
- The public functions or classes other modules should use.
- The tests that prove it works.

Avoid creating packages for future concepts until there is code that needs them.

## Formatting And Tooling

The foundation does not enforce a formatter yet. If formatting or linting tools are added later, document them in `pyproject.toml` and this file.

Before committing a shared change, run the complete test suite, compilation, `git diff --check`, and import-path validation, then review `git status` and the final diff. Commit and push only the intended scope, wait for CI, and confirm the pull-request state without merging, closing, or changing draft status unless explicitly instructed.
