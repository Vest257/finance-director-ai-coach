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

## First Scenario

The approved first scenario uses this pattern:

- Revenue is rising.
- EBITDA is rising.
- Cash is falling.
- Leadership wants to hire 20 additional people.

The learner decides whether to approve, conditionally approve, delay, or reject the hiring plan. The scenario prioritizes Balance Sheet and Cash Flow domains, with Treasury as a secondary domain. See the complete [Scenario 001 implementation contract](scenarios/scenario-001-growth-with-falling-cash.md).

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
