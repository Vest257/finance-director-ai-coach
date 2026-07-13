# Agent Instructions

This repository is the foundation for the Finance Director AI Coach. Agents and engineers should treat it as an early-stage product with long-term ambitions and deliberately simple initial architecture.

## Product Intent

- Build toward a Finance Director and CFO simulation platform.
- Deliver quick wins through a text-based Finance Director scenario coach first.
- Support future scenarios, scoring, learner profiles, financial packs, AI roleplay, and competency tracking.
- Keep the product useful for real finance leadership learning, not generic chatbot practice.

## Working Principles

- Do not begin feature implementation unless explicitly asked.
- Prefer clear documentation and small modular Python code.
- Avoid premature infrastructure, frameworks, databases, queues, service layers, or external API integrations.
- Make assumptions and decisions visible in `docs/project-management/decision-log.md`.
- Keep user-facing learning concepts aligned with `docs/learning/competency-framework.md`.

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
- Roadmap: `docs/project-management/roadmap.md`
- Decisions: `docs/project-management/decision-log.md`

## Current Constraints

- No frontend framework yet.
- No database yet.
- No external AI API integration yet.
- No unnecessary placeholder abstractions.
- No feature implementation in the foundation phase.
