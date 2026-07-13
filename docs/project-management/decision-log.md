# Decision Log

This log records important product and architecture decisions. Add entries in reverse chronological order.

## 2026-07-13: Define Platform, First Product, And MVP Learning Flow

Decision: Define FinanceOS as the platform and the Finance Director Scenario Coach as the first product. The first interface will be a CLI. The initial evaluation approach will be a deterministic rubric, with future evaluation expected to become hybrid once the rubric contract is proven.

Rationale:

- FinanceOS needs a platform-level identity that can support multiple future finance leadership products.
- The first product still needs to stay narrow enough to validate the learning loop quickly.
- A CLI avoids frontend complexity while preserving a complete scenario experience.
- Deterministic evaluation makes scoring explainable before introducing AI-assisted judgment.

Implications:

- MVP documentation should refer to the Finance Director Scenario Coach as the first FinanceOS product.
- Product work should include guided questions, skip-to-solution, debrief, competency score, model Finance Director answer, and action plan.
- AI-assisted evaluation remains future work and should be hybrid rather than replacing deterministic rubrics outright.

## 2026-07-13: Prioritize Finance Learning Domains Separately From Behavioral Competencies

Decision: Add a separate learning-domain framework prioritized as Balance Sheet, Cash Flow, Treasury, Audit, then broader Finance Director topics.

Rationale:

- Behavioral competencies explain how learners think, communicate, and lead.
- Finance domains explain what technical area a scenario exercises.
- Keeping the frameworks separate prevents domain coverage from being confused with leadership behavior.

Implications:

- Scenarios should identify domain coverage separately from competency scoring.
- Early scenario sequencing should emphasize Balance Sheet and Cash Flow before broader Finance Director topics.

## 2026-07-13: Select First Scenario Pattern

Decision: The first scenario will involve revenue and EBITDA rising while cash falls, with leadership deciding whether to hire 20 additional people.

Rationale:

- The pattern creates a realistic Finance Director tension between growth momentum and liquidity discipline.
- It tests profit-to-cash reasoning, working capital awareness, and stakeholder challenge.
- It aligns with the highest-priority learning domains: Balance Sheet and Cash Flow, with Treasury implications.

Implications:

- The first scenario should ask for a decision, not a definition.
- The model answer should show conditional approval or challenge based on cash drivers, runway, and hiring timing.

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
