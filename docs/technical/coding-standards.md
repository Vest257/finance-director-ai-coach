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
