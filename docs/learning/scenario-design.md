# Scenario Design

Scenarios are the core learning unit of the Finance Director Scenario Coach, the first FinanceOS product. Each scenario should create a realistic decision environment where the learner must apply finance leadership judgment.

## Scenario Anatomy

A scenario should include:

- Title.
- Business context.
- Learner role.
- Stakeholders involved.
- Available financial information.
- Primary learning domain from `docs/learning/domain-framework.md`.
- Decision or communication prompt.
- Guided questions.
- Skip-to-solution option.
- Expected strong response characteristics.
- Competencies assessed.
- Deterministic rubric criteria.
- Qualitative competency scorecard.
- Model Finance Director answer.
- Debrief.
- Action plan.
- Feedback guidance.
- Scenario metadata: primary domains, estimated completion time, difficulty, provenance, and version.

## Design Principles

### Make The Situation Real

Use practical business tensions: cash pressure, missed forecast, pricing decisions, board preparation, audit findings, hiring plans, covenant risk, margin erosion, or investment tradeoffs.

### Avoid Single Correct Answers

A strong Finance Director response often depends on framing, prioritization, and communication. Rubrics should recognize multiple valid approaches when the reasoning is strong. The model answer is an example, not an answer key.

### Ask For Action

Prompts should ask learners to recommend, challenge, explain, prioritize, or prepare a message. Avoid prompts that only ask for definitions.

### Guide Without Giving Away The Answer

Guided questions should help learners notice the important finance issue, such as profit-to-cash divergence, working capital pressure, covenant risk, or stakeholder incentives. They should not turn the exercise into a checklist that removes judgment.

### Support Skip-To-Solution

Learners should be able to skip to the model answer when they are stuck or using the scenario for study rather than assessment. Skipping should still show the debrief and action plan, but it should not be treated as a completed scored attempt.

### Include Constraints

Useful scenarios include constraints such as limited time, incomplete data, stakeholder pressure, conflicting incentives, or imperfect systems.

### Provide Feedback That Teaches

Feedback should identify:

- What the learner handled well.
- What they missed.
- Which risks or assumptions matter most.
- How a stronger Finance Director would frame the issue.
- Which competency the response demonstrates.

Numerical evidence should provide an optional post-submission worked calculation that shows the formula, source figures, intermediate steps, units, final answer, expected input format, and concise business interpretation. Structured interpretation, risk, cost-classification, and decision evidence may provide an optional compact "Why does this matter?" explanation. Neither type of explanation may appear in the financial pack or guided stages.

### Evaluate Only Observable Evidence

Deterministic evaluation should use calculations, structured selections, required-step completion, and explicit decision conditions. Open-ended communication and reasoning should use a self-review checklist, model answer, or manual reviewer rubric. Follow the [evaluation contract](evaluation-contract.md); do not use keyword matching as a substitute for judgment.

## Required Learner Outputs

Each MVP scenario should ask the learner for:

- Answers to guided questions.
- A final recommendation or stakeholder message.
- Optional reflection after the debrief.

## Required Coach Outputs

Each MVP scenario should provide:

- A qualitative competency scorecard using `Developing`, `Capable`, `Strong`, or `Not assessed` ratings from the behavioral competency framework.
- A debrief explaining the financial and leadership tradeoffs.
- A model Finance Director answer.
- An action plan with one to three concrete practice steps.

## Current Scenario Library

The approved first scenario uses this pattern:

- Revenue is rising.
- EBITDA is rising.
- Cash is falling.
- Leadership wants to hire 20 additional people.

The learner decides whether to approve, conditionally approve, delay, or reject the hiring plan. The scenario prioritizes Balance Sheet and Cash Flow domains, with Treasury as a secondary domain. See the complete [Scenario 001 implementation contract](scenarios/scenario-001-growth-with-falling-cash.md).

Scenario 002 is a commercial-finance renewal decision: a strategically visible customer drives revenue while discounts, implementation overruns, support demand, engineering, and service-level commitments erode contribution. It prioritizes Management Accounting, Commercial Finance, Pricing, Customer Profitability, and FP&A. See the [Scenario 002 implementation contract](scenarios/scenario-002-growth-at-any-price.md).

## Initial Scenario Categories

- Cash runway and cost control.
- Forecast miss and board communication.
- Pricing and margin pressure.
- Investment request under uncertainty.
- Audit or control weakness.
- Working capital and collections.
- Fundraising or lender update.
- CEO challenge on growth targets.

## Scenario Data

Financial packs should begin simple. Early scenarios can use plain text tables or static figures. More complex files, model uploads, and generated data should come later only when the learning loop proves useful.

## Publication Gate

Scenarios are curated registrations, not arbitrary files. Before publication, the Finance SME validates financial accuracy and reconciliation, the Product Owner validates learning intent and acceptable routes, and QA validates the learner flow, no-answer-leakage boundary, evidence, explanations, skip path, and summaries. FinanceOS does not yet provide a scenario importer, YAML authoring framework, or spreadsheet upload pipeline.
