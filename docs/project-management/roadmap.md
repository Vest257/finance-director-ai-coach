# Roadmap

This roadmap is directional. It should be updated as product discovery and implementation reveal better sequencing.

## Phase 0: Foundation

Goal: make the repository understandable and ready for focused implementation.

Status: complete.

Deliverables:

- Product vision and principles.
- Target user definition.
- MVP scope.
- Competency framework.
- Scenario design guidance.
- Architecture and coding standards.
- Roadmap and decision log.
- Python package skeleton.
- Product Owner authority and role review gates.
- Deterministic evaluation contract.
- Reconciled Scenario 001 specification and competency scorecard rubric.

## Phase 1: Scenario Coach And Fast Drill Mode

Goal: deliver the first usable Finance Director Scenario Coach learning loop through a CLI and expose the proven loop to a small browser-based pilot group.

Status: current.

Scenario 001 CLI vertical-slice milestone: merged.

FinanceOS Alpha 0.1 Streamlit pilot milestone: merged.

Fast Drill Mode V1 milestone: merged.

Delivered in this milestone:

- Scenario 001 content, CLI, deterministic rubric, structured feedback, competency scorecard, debrief, model answer, and action plan.
- Streamlit Scenario Coach with guided and skip-to-solution browser paths, in-memory attempt state, restart, and local plain-text tester summary.
- Fast Drill Mode V1: a separate Streamlit Practice page with a reviewed committed 100-card FinQA bank, deterministic numerical checks, finance-domain, financial-skill, and difficulty filters, and session-only Practice history.
- Learner-tested four-card clarity and documentation cleanup: four foundational cards clarified while preserving reviewed units and provenance; Card IDs displayed; the repeated calculation label removed; card-specific post-submission interpretations added; and deterministic regeneration enforced.
- Comprehensive tests for Scenario 001, FinQA-bank reconciliation and provenance, Practice state isolation, and browser answer-leakage boundaries.
- Minimal Python 3.11 continuous integration.

No accounts, database, durable persistence, AI, authentication, or telemetry are delivered in Phase 1.

## Phase 2: Better Scenario And Feedback Quality

Goal: improve learning value before adding platform infrastructure.

Candidate deliverables:

- Expanded scenario library, including Scenario 002 and later scenarios when separately approved and merged.
- More detailed rubrics.
- Revision loop for learner answers.
- Better competency mapping.
- Coverage across Balance Sheet, Cash Flow, Treasury, Audit, and broader Finance Director topics.
- Lightweight reporting of scenario results.

## Phase 3: Learner Memory And Progress

Goal: track learner development across attempts.

Candidate deliverables:

- Learner profile concept.
- Durable, persistent, cross-session learner history and progress (distinct from the delivered browser-session Practice table).
- Competency progress tracking.
- Persistence decision based on actual usage needs.

## Future Harder Drill Phase

Candidate drill coverage after the foundational bank:

- Two- and three-step calculations.
- Working-capital bridges, margin and contribution analysis, cash conversion, and liquidity and covenant headroom.
- Debt and interest, tax-rate effects, investment returns and valuation.
- Linked P&L, balance-sheet, and cash-flow reasoning.

## Phase 4: AI Roleplay And Richer Inputs

Goal: introduce adaptive coaching and stakeholder simulation once the product contract is clear.

Candidate deliverables:

- External AI integration boundary.
- Hybrid deterministic and AI-assisted feedback or stakeholder roleplay.
- Financial pack ingestion or structured scenario data.
- Guardrails for consistency and explainability.

## Open Sequencing Questions

- How many scenarios are needed before learner testing?
- Which Balance Sheet, Cash Flow, Treasury, and Audit scenarios should follow the first hiring decision scenario?
