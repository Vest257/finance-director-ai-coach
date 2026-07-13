# MVP Scope

The MVP is a text-based Finance Director scenario coach. Its purpose is to validate the core learning loop before investing in broader platform capabilities.

## In Scope

- A small set of curated Finance Director scenarios.
- Scenario prompts with enough context for meaningful decisions.
- Learner text responses.
- Structured feedback against a competency rubric.
- Simple scoring or qualitative assessment.
- Clear explanations of stronger and weaker response patterns.
- A command-line or minimal text-based interface if implementation begins later.

## Out Of Scope

- Frontend framework.
- Database or persistent learner accounts.
- External AI API integration.
- Multi-user administration.
- Payment, authentication, or organization management.
- Dynamic financial model generation.
- Real-time stakeholder roleplay.
- Sophisticated adaptive learning paths.

## MVP Learning Loop

1. The learner selects or starts a scenario.
2. The scenario presents context and a decision prompt.
3. The learner writes a response.
4. The coach evaluates the response against scenario expectations and competencies.
5. The learner receives actionable feedback.
6. The learner can revise or continue to the next prompt.

## Acceptance Criteria

The MVP is useful when:

- A learner can complete at least one realistic scenario end to end.
- Feedback is specific enough to improve the next response.
- The competency framework explains what is being evaluated.
- The architecture can support more scenarios without major rewrites.

## Deliberate Constraints

The MVP should not optimize for scale, personalization, or UI polish. It should optimize for learning value, clear domain structure, and fast iteration.
