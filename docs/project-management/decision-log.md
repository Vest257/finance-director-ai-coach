# Decision Log

This log records important product and architecture decisions. Add entries in reverse chronological order.

## 2026-07-13: Create Foundation Before Features

Decision: Create repository documentation, package skeleton, and project configuration before implementing product features.

Rationale:

- The product has a multi-year vision and needs shared direction.
- The first implementation should stay focused on a text-based scenario coach.
- Future engineers need clear assumptions, scope, and boundaries.

Implications:

- No runtime features are implemented in the foundation.
- Product and technical docs become the source of truth for early development.

## 2026-07-13: Start Without Frontend, Database, Or External AI

Decision: Do not add a frontend framework, database, or external AI API integration at this stage.

Rationale:

- The immediate goal is validating the learning loop.
- Infrastructure choices should follow demonstrated product needs.
- Avoiding premature dependencies keeps early iteration fast.

Implications:

- Initial implementation should be text-based.
- State should remain in memory or simple files until persistence is justified.
- AI provider integration should wait until evaluation and roleplay contracts are clearer.

## 2026-07-13: Use Modular Python With Pytest

Decision: Use a simple Python package under `src/finance_director_coach` with tests under `tests`.

Rationale:

- Python is a good fit for quick iteration, text workflows, and later AI integration.
- A `src` layout keeps package imports explicit.
- `pytest` is familiar and lightweight.

Implications:

- Code should use type hints and clear module boundaries.
- Dependencies should remain minimal.
