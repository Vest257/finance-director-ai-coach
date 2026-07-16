# MVP Scope

The MVP is the Finance Director Scenario Coach, the first product within the FinanceOS platform. Its purpose is to validate the core learning loops before investing in broader platform capabilities. The CLI is the first vertical slice; FinanceOS Alpha 0.1 adds a browser-accessible Streamlit Scenario Coach and a separate Practice surface. Scenario 001 is the only implemented scenario.

## In Scope

- A small set of curated Finance Director scenarios.
- Scenario prompts with enough context for meaningful decisions.
- Guided questions that help the learner work through the finance issue step by step.
- A skip-to-solution path for learners who are stuck or want to study the model approach first.
- Learner text responses.
- Structured feedback against a deterministic rubric.
- A qualitative competency scorecard tied to the behavioral competency framework.
- Competency ratings of `Developing`, `Capable`, `Strong`, or `Not assessed`, supported by observable evidence and improvement guidance.
- A debrief that explains the scenario, tradeoffs, and stronger reasoning pattern.
- A model Finance Director answer.
- A learner action plan for what to practice next.
- Clear explanations of stronger and weaker response patterns.
- A command-line interface.
- A Streamlit pilot interface for small-group browser testing.
- In-memory session state and a locally generated plain-text tester summary.
- A separate browser Practice page with a committed, reviewed 100-card FinQA drill bank.
- One-card deterministic numerical practice with finance-domain, financial-skill, and difficulty filters.
- Post-submission answer feedback, unit-correct worked calculations, card-specific interpretations, and visible Card IDs.
- Session-only Practice attempt history.

## Out Of Scope

- Any frontend framework beyond the approved Streamlit pilot layer.
- Database, persistent learner profiles, or cross-session progress.
- External AI API integration.
- Multi-user administration.
- Payment, authentication, or organization management.
- Dynamic financial model generation.
- Real-time stakeholder roleplay.
- Sophisticated adaptive learning paths.
- AI, authentication, leaderboards, and an overall learner score.

## MVP Learning Loops

### 1. Scenario Coach Loop

1. The learner selects or starts a scenario.
2. The scenario presents context, key numbers, and a decision prompt.
3. The learner answers guided questions or chooses skip-to-solution.
4. The learner writes a recommendation or response.
5. The coach evaluates the response against a deterministic rubric.
6. The learner receives a qualitative competency scorecard and structured feedback.
7. The learner reviews the debrief and model Finance Director answer.
8. The learner receives an action plan for the next practice step.

### 2. Fast Drill Mode Loop

1. The learner opens Practice from Streamlit navigation and optionally filters the committed drill bank.
2. The learner reviews one card, including its question, unit, and Card ID, then submits a numerical answer.
3. Practice checks the answer deterministically against the card tolerance.
4. After submission, the learner receives the result, a clear unit-correct worked calculation, and a card-specific interpretation.
5. The learner can continue to another card and review attempts from the current browser session.

## Acceptance Criteria

The MVP is useful when:

- A learner can complete at least one realistic scenario end to end.
- Feedback is specific enough to improve the next response.
- Each competency rating explains the evidence used, why it was assigned, and what would improve the response.
- The behavioral competency framework explains how judgment and communication are evaluated.
- The learning-domain framework explains which finance topics the scenario exercises.
- The architecture can support more scenarios without major rewrites.
- A learner can complete a drill and receive clear, unit-correct post-submission calculation feedback with a card-specific interpretation.

## First Scenario

The first scenario should focus on a business where revenue and EBITDA are rising while cash is falling. The learner must decide whether to approve hiring 20 additional people, challenge the plan, or recommend conditions before approval.

The scenario should test cash awareness, working capital reasoning, stakeholder communication, and the ability to challenge growth plans without ignoring commercial momentum.

The complete implementation contract is [Scenario 001: Growth With Falling Cash](../learning/scenarios/scenario-001-growth-with-falling-cash.md). Deterministic evaluation must follow the [evaluation contract](../learning/evaluation-contract.md). Open-ended communication and free-text reasoning are handled through transparent self-review, a model answer, and manual review where available; the non-AI MVP must not present keyword matching as intelligent evaluation.

## Deliberate Constraints

The MVP should not optimize for scale, personalization, or UI polish. It should optimize for learning value, clear domain structure, and fast iteration.
