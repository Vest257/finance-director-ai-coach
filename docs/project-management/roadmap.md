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

## Phase 1: Text-Based Scenario Coach

Goal: deliver the first usable Finance Director Scenario Coach learning loop through a CLI and expose the proven loop to a small browser-based pilot group.

Status: current.

Scenario 001 CLI vertical-slice milestone: merged through PR #1.

FinanceOS Alpha 0.1 Streamlit pilot milestone: scenario-library implementation work.

Delivered in this milestone:

- Implement the approved Scenario 001 content and evidence format.
- First scenario: revenue and EBITDA rising while cash falls, with a decision on hiring 20 people.
- CLI text interaction flow.
- Guided questions and skip-to-solution path.
- Deterministic rubric implementation conforming to the approved evaluation contract.
- Structured coaching feedback.
- Qualitative competency scorecard, debrief, model Finance Director answer, and action plan.
- Comprehensive tests around finance reconciliation, evaluation boundaries, session flow, and CLI validation.
- Minimal Python 3.11 continuous integration.

Alpha 0.1 pilot scope:

- Streamlit presentation layer over a curated Scenario 001 and Scenario 002 library, each with its own typed answer model and deterministic evaluator.
- Guided and skip-to-solution browser paths.
- In-memory attempt state, restart, and local plain-text tester summary.
- Post-submission worked calculations for numerical evidence and compact judgment explanations for relevant structured evidence.
- Streamlit Community Cloud deployment configuration for a small pilot group.
- No accounts, persistence, AI, database, authentication, or telemetry.

Scenario publication remains curated: finance and product-owner validation are required before a scenario is added to the registry. A general importer is deferred until repeated authoring work establishes a clear need.

Remaining Phase 1 work should follow learner testing and Product Owner prioritization; it is not presented as delivered by this milestone.

## Phase 2: Better Scenario And Feedback Quality

Goal: improve learning value before adding platform infrastructure.

Candidate deliverables:

- Expanded scenario library.
- More detailed rubrics.
- Revision loop for learner answers.
- Better competency mapping.
- Coverage across Balance Sheet, Cash Flow, Treasury, Audit, and broader Finance Director topics.
- Lightweight reporting of scenario results.

## Phase 3: Learner Memory And Progress

Goal: track learner development across attempts.

Candidate deliverables:

- Learner profile concept.
- Attempt history.
- Competency progress tracking.
- Persistence decision based on actual usage needs.

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
