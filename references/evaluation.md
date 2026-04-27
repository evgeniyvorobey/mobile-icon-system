# Evaluation Framework

Generic evaluation framework. For icon-set-specific scoring, see [`icon-set-evaluation.md`](icon-set-evaluation.md). This file describes the meta-pattern: how to evaluate any deliverable in this skill, why scoring exists, and how to read results.

## Why Evaluate

Evaluation forces explicit reasoning about decisions that would otherwise stay implicit. "This looks good" is not actionable; "this scores 4 on brand fit, 2 on cliché avoidance" is.

Evaluation also provides a paper trail when handing off to engineering, marketing, or future design work — the rationale is captured.

## Evaluation Outputs

Every evaluation produces:

1. **Per-dimension scores** with notes
2. **Composite verdict** (ship / ship with follow-ups / re-work needed)
3. **Top 3 improvement moves** in priority order
4. **Unresolved risks** carried forward

## Score Types

Three score types used across this skill:

### Pass / fail

Used for non-negotiable dimensions (e.g., touch target compliance, state-pair existence).

- Pass = meets the bar
- Fail = blocks shipping
- "Pass with note" = meets bar but has documented concern

### 1-5 scale

Used for quality dimensions (e.g., brand fit, metaphor clarity).

- 1 = unacceptable, re-work required
- 2 = below bar, significant issues
- 3 = acceptable, room to improve
- 4 = strong, minor refinements possible
- 5 = excellent, ship as-is

### Composite

Average of 1-5 dimensions; pass/fail dimensions checked separately.

- ≥4.0 average + all pass/fail clear = ship-ready
- 3.0-3.9 average + all pass/fail clear = ship with follow-ups (document them)
- <3.0 average OR any fail = re-work

## Evaluation Discipline

### Score honestly

- Don't bump borderline scores up to ship
- Don't score everything 5 ("looks great") — that's not evaluation, that's approval
- Don't score everything 3 ("could be better") — that's noise

### Score with evidence

- Each score should reference a specific check
- "Brand fit: 4 — stroke language matches logo, but corner radius slightly drifts on Settings"
- Not: "Brand fit: 4 — feels right"

### Evaluate the right unit

- Per-icon scores miss set-level failures
- Set-level scores miss icon-level details
- Both are needed, applied appropriately

## Common Evaluation Mistakes

### Self-approval

When the designer evaluates their own work, scores trend high. Counter by:

- Imagine a critical reviewer with no investment in the set
- Find the single weakest icon — what's its score?
- Find the single weakest dimension across the set — score that

### Aesthetic-only

"It looks good" is not evaluation. Force structural questions:

- Does it pass at intended size?
- Does it match Brand DNA?
- Does it survive the cliché audit?

### Over-evaluation

Spending an hour on evaluation when the set has obvious failures wastes time. If the first dimension reveals a fail, fix it before scoring further.

## Reading Evaluation Output

When the user receives evaluation:

- They should learn the most important issue immediately
- Ship verdict is the headline
- Per-dimension scores explain why
- Improvement moves are actionable, not vague

## Integration with Other Phases

Evaluation runs in workflow phase 10. It's not a standalone phase — it consumes outputs from generation (phase 7), consistency audit (phase 8), and craft pass (phase 9).

When evaluation finds critical failures, return to the appropriate earlier phase:

- Construction failures → phase 5 (rules) or phase 7 (regenerate)
- Consistency drift → phase 8 (re-audit)
- Craft issues → phase 9 (re-craft)
- Validation failures → phase 11 (context test, not just evaluation)

## Failure Modes

- **Evaluating without rules** — without the documented icon system rules, every score is subjective
- **Evaluating without context** — must include in-context tests (phase 11), not just bench evaluation
- **Skipping rejection criteria** — pass/fail dimensions exist for a reason
- **Treating evaluation as approval** — it's diagnosis, not endorsement
