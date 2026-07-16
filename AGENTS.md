# Agent Instructions

This repository is the foundation for FinanceOS. FinanceOS is the platform; the Finance Director Scenario Coach is the first product. Agents and engineers should treat the work as an early-stage product with long-term ambitions and deliberately simple initial architecture.

## Product Intent

- Build FinanceOS as a Finance Director and CFO simulation platform.
- Deliver quick wins through the Finance Director Scenario Coach, with the CLI as the first vertical slice and Streamlit as the approved Alpha 0.1 pilot surface.
- Support future scenarios, evaluation, learner profiles, financial packs, AI roleplay, and competency tracking.
- Keep the product useful for real finance leadership learning, not generic chatbot practice.

## Working Principles

- Do not begin feature implementation unless explicitly asked.
- Prefer clear documentation and small modular Python code.
- Avoid premature infrastructure, frameworks, databases, queues, service layers, or external API integrations.
- Make assumptions and decisions visible in `docs/project-management/decision-log.md`.
- Keep behavioral learning concepts aligned with `docs/learning/competency-framework.md`.
- Keep finance-domain learning concepts aligned with `docs/learning/domain-framework.md`.
- Keep deterministic assessment aligned with `docs/learning/evaluation-contract.md`.

## Roles And Review Gates

### Product Owner

The Product Owner is the human owner of FinanceOS.

Responsibilities:

- Set product priorities.
- Provide practical finance experience and scenario input.
- Approve product scope and milestone acceptance.
- Test learning experiences from the learner perspective.
- Make final decisions when product, finance, or delivery tradeoffs remain unresolved.

Authority boundaries:

- Has final authority over priorities, product acceptance, and product direction.
- Receives product design proposals and reviews from the Chief Product Architect.
- Relies on the Finance SME as the authority for finance correctness.
- Delegates approved implementation to Codex and the documented engineering roles.
- Must be asked to resolve material disagreements or assumptions; agents must not silently decide them.

Review gates:

- Final approval of product scope, milestone acceptance, and changes to product direction.
- Resolution of material tradeoffs that remain after role review.

### Chief Product Architect

Responsibilities:

- Translate Product Owner priorities into a coherent FinanceOS platform vision and product sequence.
- Confirm that the Finance Director Scenario Coach remains the first product focus.
- Propose whether work belongs in the MVP, later roadmap, or backlog.

Authority boundaries:

- May propose and review product design, scope, and prioritization.
- Does not replace the Product Owner's final authority over priorities, acceptance, or direction.
- Should not prescribe implementation details unless they affect product risk or learning value.

Review gates:

- Product coherence of the vision, MVP scope, roadmap, and major scenario experience changes before Product Owner approval.
- Any proposal to add a frontend, database, AI integration, authentication, payments, or multi-user administration.

### Software Architect

Responsibilities:

- Own architecture, module boundaries, dependency posture, and technical tradeoffs.
- Keep the initial system simple while preserving room for future scenarios, evaluation, profiles, financial packs, AI roleplay, and competency tracking.
- Record architecture decisions in `docs/project-management/decision-log.md`.

Authority boundaries:

- May approve technical structure and dependency choices.
- Should not expand product scope without Chief Product Architect review and Product Owner approval.

Review gates:

- New modules, package structure changes, external dependencies, persistence choices, and integration boundaries.

### Python Engineer

Responsibilities:

- Implement Python code when feature work is explicitly requested.
- Use type hints, clear boundaries, and tests.
- Keep code aligned with `docs/technical/coding-standards.md` and `docs/technical/architecture.md`.

Authority boundaries:

- May make implementation decisions inside approved architecture.
- Should not add product capabilities, infrastructure, or dependencies without the relevant review gate.
- Must escalate material product or finance assumptions rather than resolving them silently in code.

Review gates:

- Unit tests, type-aware interfaces, and code review by the Software Architect for structural changes.

### QA Engineer

Responsibilities:

- Define validation expectations before features are accepted.
- Check deterministic rubric behavior, scenario flow, link integrity, and regression risk.
- Keep test coverage proportional to product and architecture risk.

Authority boundaries:

- May block release when acceptance criteria or validation evidence is missing.
- Should not redefine product goals or finance-domain correctness without the responsible reviewer.

Review gates:

- MVP acceptance criteria, scenario evaluation behavior, validation scripts, and release readiness.

### Documentation Engineer

Responsibilities:

- Keep repository documentation consistent, navigable, and current.
- Ensure links resolve and terminology stays aligned across product, learning, technical, and project-management docs.
- Capture decisions in the decision log when direction changes.

Authority boundaries:

- May reorganize or clarify documentation without changing approved product scope.
- Should not introduce new product promises through documentation alone.

Review gates:

- Documentation-only alignment passes, link validation, terminology changes, and contributor guidance.

### Finance SME

Responsibilities:

- Own finance-domain correctness, scenario realism, and model Finance Director answers.
- Prioritize domain coverage across Balance Sheet, Cash Flow, Treasury, Audit, and broader Finance Director topics.
- Review rubrics for practical finance leadership quality.

Authority boundaries:

- May approve or reject scenario content and finance-domain evaluation criteria.
- Should not dictate software architecture beyond domain requirements.
- Does not make final product-priority or milestone-acceptance decisions for the Product Owner.

Review gates:

- Scenario content, financial packs, deterministic rubric criteria, model answers, debriefs, and learner action plans.

## Technical Expectations

- Use Python with type hints.
- Use `pytest` for tests.
- Keep source code under `src/finance_director_coach`.
- Keep tests under `tests`.
- Follow `docs/technical/coding-standards.md`.
- Follow `docs/technical/architecture.md` before adding modules.

## Documentation Expectations

When changing product direction, update the relevant product document:

- Vision: `docs/product/vision.md`
- Principles: `docs/product/product-principles.md`
- Target users: `docs/product/target-user.md`
- MVP scope: `docs/product/mvp-scope.md`
- Learning domains: `docs/learning/domain-framework.md`
- Behavioral competencies: `docs/learning/competency-framework.md`
- Evaluation contract: `docs/learning/evaluation-contract.md`
- Scenario specifications: `docs/learning/scenarios/`
- Roadmap: `docs/project-management/roadmap.md`
- Decisions: `docs/project-management/decision-log.md`

## Scenario Library-Wide Delivery

- Treat every scenario registered in `SCENARIOS` as one product surface.
- Before changing shared UI, presentation models, content rendering, navigation, summaries, responsive behavior, or accessibility, inspect every registered scenario and apply the change to each affected scenario in the same task.
- Do not leave a registered scenario on a materially inferior fallback because the immediate request names another scenario.
- Keep financial calculations, evidence rules, and authored content scenario-owned. Do not copy them into unrelated scenarios.
- A scenario-specific exception requires an explicit Product Owner request or a documented technical blocker. Record the reason and follow-up action in the decision log.

## Financial-Pack Presentation

- Use scenario-owned typed `FinancialPackTable` content for naturally tabular inputs: statements, cash-flow bridges, working-capital and liquidity schedules, forecasts, route assumptions and comparisons, and glossaries.
- Use prose only for genuine narrative context, qualifications, and supporting explanations; never flatten a financial table into prose as a substitute for structured presentation.
- Preserve every learner-visible input, assumption, unit, sign, and qualifier. Do not reveal calculated answers, worked solutions, or evaluation outcomes in the briefing or guided flow.
- Use the same shared renderer for the briefing and guided financial-pack reference. Keep financial-pack expanders, with the first section open by default.
- Tables are static and non-editable, hide indexes, use responsive container width, and must work on desktop and at approximately 390px width.

## Cross-Scenario Validation And Completion

- Parameterize shared presentation and flow tests across registered scenarios where practical. For any shared presentation change, validate every registered scenario in both the briefing and guided financial-pack reference.
- Check for code-style financial-pack blocks, editable tables, unintended indexes, answer leakage, and responsive presentation. Visually inspect each affected scenario on desktop and at approximately 390px width; if browser automation is unavailable, report that visual check as outstanding rather than passed.
- Before declaring a shared change complete, inspect all registered scenarios and run the full test suite, compilation, `git diff --check`, and import-path validation.
- Review `git status` and the final diff before committing. Commit and push scoped changes automatically, then wait for CI and verify the pull-request state.
- Never merge, close, or mark a draft pull request ready for review unless the Product Owner explicitly requests it.

## Current Constraints

- Streamlit is approved only as the in-memory Alpha 0.1 presentation layer; do not add another frontend framework without review.
- No database yet.
- No external AI API integration yet.
- No unnecessary placeholder abstractions.
- Feature implementation must remain within approved Phase 1 scope and review gates.
