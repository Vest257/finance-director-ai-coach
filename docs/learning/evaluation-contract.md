# Evaluation Contract

This document defines the evidence and rating contract for the non-AI MVP of the Finance Director Scenario Coach. It is the source of truth for deterministic evaluation. Scenario specifications own their scenario-specific evidence, thresholds, and feedback, while the [competency framework](competency-framework.md) owns the behavioral competency definitions.

## Purpose

The evaluation must be useful, transparent, and honest about what the system can observe. It must not confuse a completed checklist with executive judgment, and it must not present crude keyword matching as intelligent evaluation.

The MVP output is a qualitative competency scorecard. It has no overall numerical score.

## Evidence Types

### Deterministically Assessable Evidence

The MVP may evaluate evidence when a clear, inspectable rule can produce the same result for the same input. Supported evidence types include:

- Numerical calculations compared with an expected value and an explicit tolerance.
- Identification of cash-flow drivers through structured selections.
- Recognition of material risks through structured selections.
- Selection of a recommendation and decision conditions.
- Completion of required analysis steps.
- Selection of information that is unavailable or still required.

Deterministic checks assess the learner's recorded choice or calculation, not an inferred intention.

### Open-Ended Evidence

The non-AI MVP cannot reliably machine-score these qualities in free text:

- Executive communication quality.
- Persuasiveness.
- Nuance and proportionality.
- Constructive stakeholder challenge.
- Overall quality of free-text reasoning.
- Whether a narrative makes appropriate use of tone, sequence, and emphasis.

Open-ended evidence must use one or more honest learning aids:

- A transparent self-review checklist.
- A model Finance Director answer.
- A manual reviewer rubric where a qualified reviewer is available.
- A `Not assessed` competency rating when the available evidence cannot support a rating.

Keyword occurrence, response length, writing style proxies, or sentiment must not be presented as reliable judgment of these qualities.

## Evidence Record

Every scenario requirement used in evaluation must have a stable identifier. An evidence record should contain:

- Requirement ID.
- Learner input or structured selection.
- Evidence type.
- Deterministic rule, including any numerical tolerance.
- Result: `Observed`, `Not observed`, or `Insufficient evidence`.
- Competency or competencies informed by the result.
- Feedback message explaining the result.
- Improvement guidance.

The scorecard must be reproducible from these records. It must not depend on hidden weighting.

## Competency Ratings

Each scenario defines the core evidence requirements and permitted assessment source for every competency it can assess. Apply ratings in this order, subject to the competency-specific source limits below:

1. `Not assessed`: use when the scenario does not elicit the competency, the learner uses skip-to-solution, the learner provides no meaningful evidence for the competency, or only open-ended evidence is available to the deterministic evaluator.
2. `Developing`: use when a competency-specific critical omission is present, a material calculation is wrong beyond the stated tolerance, evidence contradicts the recommendation, or one or more core evidence requirements are not observed.
3. `Strong`: use only when every core and strong evidence requirement for that competency is observed, no critical omission is present, and the assessment source is permitted to assign `Strong` for that competency.
4. `Capable`: use when every core evidence requirement is observed, no critical omission is present, and one or more strong evidence requirements are not observed.

The order is deliberate: insufficient evidence is not failure, and a critical omission cannot be offset by unrelated strengths.

Every reported rating must include:

- The observable evidence used.
- Why that evidence leads to the rating.
- What would improve the response or maintain strong performance.
- The assessment source: `deterministic`, `self-review`, or `manual review`.

Self-review results must be labeled as self-review and must not silently replace deterministic or manual ratings.

### Competency-Specific Source Limits

- Financial Insight may receive `Developing`, `Capable`, or `Strong` from deterministic evidence when the scenario elicits calculations, reconciliation, and structured financial analysis.
- Cash And Risk Discipline may receive `Developing`, `Capable`, or `Strong` from deterministic evidence when the scenario elicits liquidity calculations, threshold interpretation, and structured risk recognition.
- Commercial Judgment may receive only `Developing` or `Capable` from deterministic evidence. `Strong` requires a qualified manual reviewer in the MVP or hybrid AI-assisted review in a future phase because checklist completion cannot establish executive judgment.
- Stakeholder Communication and Strategic Leadership remain `Not assessed` unless a qualified manual reviewer provides evidence in the MVP. Future hybrid AI-assisted review may assess them under a separately approved contract.
- Selecting a recommendation route may be recorded as evidence relevant to Strategic Leadership, but it must not create a deterministic Strategic Leadership rating.

Every competency result must state its assessment source. Structured selections demonstrate only the selected facts, risks, or actions; selecting every expected option does not by itself prove executive judgment.

## Critical Omissions

A critical omission is a scenario-specific failure to address information essential to a safe or credible decision. Examples include:

- Ignoring a forecast liquidity breach.
- Treating EBITDA as cash without considering material working-capital movements.
- Recommending expenditure without recognizing a binding covenant or funding limit.
- Making a numerical claim that materially contradicts the financial pack.
- Giving no decision when a decision is a required output.

Each scenario must list its critical omissions and map each one to affected competencies. Critical omissions are explicit gates, not penalty points.

## Acceptable Alternative Decisions

The evaluator must assess reasoning evidence and safeguards, not conformity with a model recommendation. A scenario may define several acceptable decision routes, each with route-specific evidence and conditions.

Different recommendations may receive equivalent ratings within the permitted assessment-source limits when they:

- Use the available financial evidence correctly.
- Recognize the material risks and unavailable information.
- Include safeguards appropriate to the selected route.
- Remain internally consistent.

The model Finance Director answer is an example of strong reasoning, not the only correct response.

## Insufficient Evidence

Use `Not assessed` rather than guessing when:

- The scenario does not request evidence for the competency.
- A learner skips to the solution.
- A response is absent or so incomplete that no competency-specific rule can be applied. When enough evidence exists to apply the rule but a core requirement is omitted or incorrect, use `Developing`.
- The only evidence is open-ended and no manual reviewer is involved.

Feedback should state what evidence was missing and how the learner could provide it on another attempt. `Not assessed` must not be converted to `Developing` merely because no evidence was available.

## Traceability

Every feedback statement must trace to one or more of:

- A scenario requirement ID.
- An observed calculation or structured selection.
- A named critical omission.
- A self-review checklist item.
- A manual-review rubric item.

Scenario specifications must provide a traceability table linking required learner outputs to evidence rules, competencies, critical omissions, and feedback. Generic feedback with no traceable evidence is outside the MVP contract.

## Rules Preventing False Precision

- Do not calculate or display an overall numerical score.
- Do not show percentages, points, ranks, or decimal ratings for competencies.
- Do not average qualitative ratings.
- Do not convert `Not assessed` into a zero or failure.
- Do not create hidden weights that imply scientific measurement.
- Do not infer communication quality from keywords, length, grammar, or sentiment.
- Use explicit calculation tolerances only where rounding justifies them.
- Distinguish deterministic, self-review, and manual-review evidence in output.
- State material limitations beside the relevant rating or feedback.

## Deterministic MVP Boundary

The deterministic MVP may:

- Validate calculations and reconciliations.
- Check structured recognition of drivers, risks, missing information, and conditions.
- Confirm completion of required analysis steps.
- Apply explicit route-specific rating gates.
- Produce authored feedback tied to the evidence record.

The deterministic MVP may not claim to evaluate:

- The full quality of free-text reasoning.
- Executive presence, persuasiveness, or tone.
- Subtle stakeholder dynamics.
- Novel but valid reasoning not represented in the structured choices.

## Future Hybrid Evaluation

A future hybrid evaluator may combine deterministic evidence with AI-assisted review of open-ended responses. Deterministic calculations, critical controls, and traceability should remain authoritative. AI-assisted judgments must:

- Use the same scenario requirements and competency definitions.
- Cite response evidence for each judgment.
- Be distinguishable from deterministic results.
- Preserve acceptable alternative decisions.
- Support human review and correction.
- Avoid introducing an overall numerical score unless a later Product Owner decision establishes a validated need and method.

External AI integration remains outside the MVP and requires the documented architecture and product review gates.

## Scenario Author Checklist

Before a scenario is approved, its authors and reviewers must confirm that:

- Every deterministic requirement has a stable ID and explicit rule.
- Numerical rules state units, expected values, and tolerances.
- Core, strong, and critical-omission gates are defined per assessed competency.
- All acceptable decision routes have explicit safeguards.
- Open-ended qualities use self-review, a model answer, or manual review.
- Feedback traces to evidence.
- Skip-to-solution produces learning content but no assessed attempt.
- No rating relies on keyword matching or hidden points.
