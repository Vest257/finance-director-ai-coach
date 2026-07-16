# Decision Log

## 2026-07-16: Clarify Learner-Tested Foundational Drill Feedback

Decision: Keep four reviewed foundational cards honestly classified as foundational, display each card's stable Card ID, and show a single clear worked-calculation label followed by a card-specific post-submission interpretation.

Rationale:

- Learner testing identified a repeated `Calculation:` prefix after the Practice UI label.
- The feedback needs to preserve the reviewed unit and provenance while making the calculation and financial meaning immediately legible.

Implications:

- The authored curation ledger is the source of truth for the four corrected calculation strings; the generated bank is regenerated deterministically.
- Practice does not reveal the calculation or interpretation before a valid submission.

## 2026-07-15: Plan A More Demanding Future Drill Phase

Decision: Keep this focused cleanup limited to reviewed foundational cards; defer harder learner drills to a future phase.

Backlog: Add two- and three-step calculations; working-capital bridges; margin and contribution analysis; cash conversion; liquidity and covenant headroom; debt movement and interest; tax-rate effects; investment returns and valuation; and linked P&L, balance-sheet, and cash-flow reasoning.

## 2026-07-15: Add Fast Drill Mode V1 As A Separate In-Memory Practice Surface

Decision: Add a separate Streamlit Practice page backed by the committed, reviewed 100-card FinQA drill bank. Keep answer evaluation deterministic through each card's stored tolerance and retain attempts only for the current browser session.

Rationale:

- Short, one-card numerical practice provides a focused complement to the Finance Director Scenario Coach without changing scenario evaluation.
- The reviewed committed bank supports reproducible learner content without runtime FinQA imports or network access.
- Session-only state makes the first learner loop useful without prematurely adding accounts or persistence.

Implications:

- The Practice core remains UI-independent and testable outside Streamlit.
- V1 has no database, accounts, saved profile, adaptive engine, streaks, leaderboard, or overall learner score.
- Scenario Coach state and Scenario 001 evaluation rules remain isolated and unchanged.

## 2026-07-15: Complete Final FinQA Learner-Content And Taxonomy Review

Decision: Make final learner-facing corrections explicit in the committed curation ledger, including percentage-point treatment for effective tax-rate changes, cleaned learner tables, and pending-only automatic curation candidates.

Rationale:

- A card must not be marked reviewed merely because it is mechanically eligible.
- Finance concepts need to remain distinct from the arithmetic used to calculate them.
- Learner-facing tables and worked calculations must be clear while raw FinQA evidence stays intact for provenance.

Implications:

- The importer accepts only explicit approved curation entries for generated cards.
- Automatic candidate entries are pending with all review flags false.
- Effective-rate differences use percentage points rather than percentage-change units.

## 2026-07-15: Curate FinQA Drills For Learner Use

Decision: Require an explicit, individually reviewed curation ledger for each FinQA drill, separate finance concepts from arithmetic methods, and expose cleaned learner-facing wording alongside retained raw provenance.

Rationale:

- Recomputing a FinQA program alone does not establish financial meaning, compatible units, or learner clarity.
- FinanceOS needs explicit currency dimensions and scales to avoid presenting USD million as plain USD.
- Final taxonomy choices must be reviewable rather than inferred solely from a first keyword.

Implications:

- The bank rejects known scale and semantic failures, including point-in-time balance additions without a valid financial reason.
- Every card records approved review flags for units, semantics, domain, and learner clarity.
- The learner-facing question, context, table, and worked calculation omit raw FinQA syntax and known OCR artefacts while raw source fields remain available for provenance.

## 2026-07-15: Add A Deterministic FinQA Calculation-Drill Content Bank

Decision: Introduce a generated, immutable 100-card FinQA fast-drill bank and its offline deterministic import tooling, without adding a learner UI, persistence, scoring, adaptive sequencing, authentication, or runtime network access.

Rationale:

- FinanceOS needs a reviewable base of short finance calculations before a learner interaction surface is designed.
- FinQA provides executable numerical programs and source evidence that can be recomputed without an LLM.
- Committing the selected source-record fixture allows CI to validate the generated bank without downloading FinQA.

Implications:

- The current import taxonomy covers P&L, Balance Sheet, Cash Flow, Working Capital, Liquidity & Treasury, Tax, Commercial Finance, and Investment & Valuation.
- Each card retains its FinQA source ID, source report reference, citation, and MIT licence metadata.
- New drill surfaces must consume the committed JSON bank rather than perform runtime source imports.

This log records important product and architecture decisions. Add entries in reverse chronological order.

## 2026-07-13: Add Streamlit As The Alpha 0.1 Pilot Surface

Decision: Add a Streamlit browser interface for a small group of finance-professional pilot testers. Streamlit is a presentation and interaction layer over the existing Scenario 001 content, `LearnerAnswers`, deterministic evaluator, evidence records, scorecard, and learning content.

Rationale:

- The merged CLI vertical slice has established the first complete learning loop.
- A browser link reduces pilot access friction without requiring a separate frontend application or platform infrastructure.
- Streamlit supports forms, in-memory state, responsive layouts, testing, and Community Cloud deployment with one approved runtime dependency.

Implications:

- `streamlit_app.py` is the Community Cloud entrypoint and delegates to the package presentation module.
- The browser collects structured inputs and calls the same evaluator only after final submission.
- The learner-facing financial pack retains the no-answer-leakage boundary.
- Session state is in memory only; Start over clears it, and the optional summary is generated locally for download.
- The pilot does not add AI, a database, persistence, accounts, authentication, telemetry, or another frontend framework.
- CLI behavior and all approved finance and competency-rating rules remain unchanged.

## 2026-07-13: Implement The First Vertical Slice With Typed Python Boundaries

Decision: Implement Scenario 001 with plain typed Python modules for scenario content, domain models, deterministic evaluation, session orchestration, and CLI input. Use dataclasses, enums, pure evaluation functions, and pytest without adding runtime dependencies or generic content infrastructure.

Rationale:

- These boundaries are required by the current scenario and can be tested independently.
- Plain Python keeps the first learning loop easy to understand and change.
- YAML, a database, a frontend, and a generic scenario engine would add complexity without a current use case.

Implications:

- `python -m finance_director_coach` is the first product interface.
- Scenario content remains separate from learner interaction and evaluation.
- No persistence, database, AI integration, authentication, telemetry, or frontend is introduced.

## 2026-07-13: Keep Free Text For Display And Self-Review Only

Decision: Store the learner's CEO response only in the in-memory attempt for display and self-review. Do not inspect its keywords, length, grammar, sentiment, or wording during deterministic evaluation.

Rationale:

- Free-text presence can confirm completion of a required step but does not establish response quality.
- Automatic text heuristics would conflict with the approved evaluation boundary.

Implications:

- Free-text quality does not alter evidence results or competency ratings.
- The CLI labels the limitation and provides a model answer and self-review checklist.
- Future hybrid review requires a separately approved AI evaluation contract.

## 2026-07-13: Accept Scenario 001 For Phase 1 Implementation

Decision: The Product Owner accepts Scenario 001 for implementation after correcting the deterministic Commercial Judgment boundary.

Rationale:

- The scenario financial pack, learning flow, and evidence traceability passed the design review gates.
- The rating correction prevents structured checklist completion from being presented as executive judgment.

Implications:

- The `feat/scenario-001-cli` vertical slice may implement the approved specification.
- Material departures from the scenario or evaluation contract require the documented review gates.

## 2026-07-13: Cap Deterministic Commercial Judgment At Capable

Decision: Deterministic evidence may assign `Developing` or `Capable` for Commercial Judgment, but never `Strong`. Strong Commercial Judgment requires qualified manual review in the MVP or hybrid AI-assisted review in a future phase.

Rationale:

- Structured selections can show that expected calculations, risks, and safeguards were recorded.
- They cannot reliably establish nuance, proportionality, or executive tradeoff judgment.

Implications:

- Stakeholder Communication and Strategic Leadership remain `Not assessed` without qualified manual review.
- Recommendation-route selection may be retained as Strategic Leadership evidence without creating a deterministic rating.
- Financial Insight and Cash And Risk Discipline may still receive deterministic `Strong` when scenario evidence supports it.
- Every competency result must state its assessment source.

## 2026-07-13: Approve Scenario 001 As The First Implementation Contract

Decision: Use [Scenario 001: Growth With Falling Cash](../learning/scenarios/scenario-001-growth-with-falling-cash.md) as the first scenario implementation contract. Its reconciled financial pack, evidence IDs, acceptable recommendation routes, competency rubric, model answer, and debrief define the Phase 1 behavior to implement.

Rationale:

- A complete design gate reduces product ambiguity before runtime work begins.
- Reconciled figures provide a credible finance learning experience and testable implementation expectations.
- Multiple valid recommendation routes preserve realistic Finance Director judgment.

Implications:

- Phase 0 is complete and Phase 1 is current.
- Phase 1 should implement this contract without adding a frontend, database, or AI integration.
- Material scenario changes require Chief Product Architect, Finance SME, QA, and Product Owner review.

## 2026-07-13: Define The Limits Of Deterministic Free-Text Evaluation

Decision: The non-AI MVP will not claim to machine-score executive communication, persuasiveness, nuance, constructive challenge, or overall free-text reasoning. These qualities use a self-review checklist, model Finance Director answer, and manual reviewer rubric where available.

Rationale:

- Keyword matching and writing proxies do not provide credible evidence of executive judgment.
- Honest `Not assessed` ratings are preferable to invented certainty.
- The deterministic contract should remain useful when future AI-assisted review is added.

Implications:

- The [evaluation contract](../learning/evaluation-contract.md) defines the boundary and evidence traceability rules.
- Future AI-assisted evaluation must remain distinguishable from deterministic results and preserve human review.

## 2026-07-13: Use A Qualitative Competency Scorecard

Decision: The MVP output will be a competency scorecard using `Developing`, `Capable`, `Strong`, and `Not assessed`. It will not calculate an overall numerical score.

Rationale:

- Qualitative ratings match the available evidence better than numerical precision.
- Learners need evidence, explanation, and improvement guidance more than points.
- Different recommendations can demonstrate equally strong judgment.

Implications:

- Every competency rating must cite observable evidence, explain the rating, and identify an improvement.
- `Not assessed` is used for insufficient evidence and is not treated as failure.
- No hidden weights, percentages, or averaged ratings are part of the MVP.

## 2026-07-13: Establish Product Owner Authority

Decision: Define the Product Owner as the human owner of FinanceOS with final authority over priorities, product acceptance, and product direction.

Rationale:

- Product design, finance correctness, and implementation responsibilities need a clear human decision owner.
- Material disagreements should be surfaced rather than silently resolved by agents or specialist roles.

Implications:

- The Chief Product Architect proposes and reviews product design.
- The Finance SME owns finance correctness.
- Codex and the documented engineering roles implement approved work.
- Unresolved material product, finance, or delivery tradeoffs are escalated to the Product Owner.

## 2026-07-13: Define Platform, First Product, And MVP Learning Flow

Decision: Define FinanceOS as the platform and the Finance Director Scenario Coach as the first product. The first interface will be a CLI. The initial evaluation approach will be a deterministic rubric, with future evaluation expected to become hybrid once the rubric contract is proven.

Rationale:

- FinanceOS needs a platform-level identity that can support multiple future finance leadership products.
- The first product still needs to stay narrow enough to validate the learning loop quickly.
- A CLI avoids frontend complexity while preserving a complete scenario experience.
- Deterministic evaluation makes competency ratings explainable before introducing AI-assisted judgment.

Implications:

- MVP documentation should refer to the Finance Director Scenario Coach as the first FinanceOS product.
- Product work should include guided questions, skip-to-solution, debrief, a qualitative competency scorecard, model Finance Director answer, and action plan.
- AI-assisted evaluation remains future work and should be hybrid rather than replacing deterministic rubrics outright.

## 2026-07-13: Prioritize Finance Learning Domains Separately From Behavioral Competencies

Decision: Add a separate learning-domain framework prioritized as Balance Sheet, Cash Flow, Treasury, Audit, then broader Finance Director topics.

Rationale:

- Behavioral competencies explain how learners think, communicate, and lead.
- Finance domains explain what technical area a scenario exercises.
- Keeping the frameworks separate prevents domain coverage from being confused with leadership behavior.

Implications:

- Scenarios should identify domain coverage separately from competency ratings.
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
