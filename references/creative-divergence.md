# Creative Divergence

When the icon system rules feel generic or the user wants more variety in rule sets to choose from, run a divergence pass before locking the rules in phase 5. This file defines divergence axes for icon systems (not for individual icons — divergence operates at the system-rule level).

## When to Run Divergence

Run a divergence pass when:

- The category feels generic (e.g., yet another fintech app with rounded outlined icons)
- The user requests "more options" or "explore more"
- Brand DNA is permissive (allows multiple system-rule interpretations)
- The first rule set feels obvious

Skip divergence when:

- Brand DNA is highly prescriptive (only one valid system rule set follows)
- The user has already chosen a direction
- The project is a narrow refresh

## Divergence Axes

Vary rule sets across these axes — one rule set per axis combination:

### Axis 1 — Style

- All filled (solid silhouettes only)
- All outlined (stroke-based)
- Mixed (filled for active, outlined for inactive — Tab Bar standard)
- Duotone (two colors per icon)

### Axis 2 — Stroke weight

- Light (1.25pt-1.5pt at 24px)
- Standard (1.75pt at 24px)
- Bold (2pt-2.5pt at 24px)
- Variable (1pt thin / 2pt thick contrast)

### Axis 3 — Terminal style

- All round
- All square
- All cut
- Mixed per Brand DNA logic

### Axis 4 — Corner treatment

- Sharp (R=0)
- Slightly rounded (R=1pt at 24px)
- Generously rounded (R=2-4pt)
- Variable (different per icon family within set)

### Axis 5 — Construction language

- Pure geometric (only orthogonals + 45° + arcs)
- Organic (free curves allowed)
- Hybrid (geometric base, organic accents)
- Pixel-grid (forced to 2px increments — pixel-art feel)

## Divergence Output

Run divergence by generating 3-4 rule-set candidates that vary along 2-3 of the axes above. Each candidate must:

- Be internally consistent (one combination, not a mix)
- Be applicable to the full vocabulary (test by sketching 2-3 icons)
- Have a one-line tagline that captures its character

Example output:

```markdown
## Divergence Pass

### Set A — "Calm Precision"
- Style: outlined (filled for selected only)
- Stroke: 1.75pt standard, no contrast
- Terminals: round
- Corners: 2pt rounded
- Construction: pure geometric
- Character: trustworthy, software-tool feel

### Set B — "Friendly Weight"
- Style: filled for both states (filled-secondary for inactive)
- Stroke: N/A (silhouette only)
- Terminals: round corners
- Corners: 4pt generously rounded
- Construction: organic, hybrid
- Character: approachable, consumer feel

### Set C — "Editorial Sharp"
- Style: outlined throughout
- Stroke: contrast pair (1pt thin, 2pt thick)
- Terminals: square
- Corners: sharp R=0
- Construction: pure geometric, strong horizontals/verticals
- Character: confident, design-tool feel
```

## Worked Examples

### Bad Set: Decorative Pseudo-Difference

A set that looks varied but isn't. Common pattern: same metaphor, same construction, only color or surface treatment changes.

```
Set 1: Home icon, blue
Set 2: Home icon, blue with shadow
Set 3: Home icon, blue with gradient
Set 4: Home icon, blue with rounded background
```

These have the same metaphor class, the same construction, and the same monochrome mapping. They are not divergent — they are decorative variations of the same idea. Reject this pattern.

### Good Set: True Divergence

Different rule sets that produce genuinely different families. The icons drawn under each rule set look like different products.

```
Set A: outlined / 1.75pt / round / R=2 — software tool feel
Set B: filled silhouette / R=4 organic — consumer app feel
Set C: outlined / 1pt-2pt contrast / square / R=0 — editorial / design feel
```

Drawing the Home icon under each set produces visibly different icons — different stroke, different corners, different topology. That is divergence.

## Pseudo-Difference Filter

Before presenting divergence sets, filter out pseudo-differences:

- Same metaphor class? Same construction? Same monochrome mapping? → pseudo-difference, reject
- Same rules with only stroke weight nudged 0.25pt? → pseudo-difference
- Same rules with one terminal style swapped? → pseudo-difference
- Different metaphor families, different construction, different stroke language? → true divergence

The test: render the Home icon under each rule set. If you can't tell them apart at first glance, the divergence is fake.

## After Divergence — Choose, Then Proceed

User picks one rule set. Lock it in phase 5. Do not blend rules from multiple sets — that produces a mongrel system without internal consistency.

If the user wants elements from two sets, ask: which is the dominant set, and what specifically gets borrowed from the other? Document that explicitly. Don't silently mix.

## Failure Modes

- **Pseudo-difference passed off as divergence** — see filter above
- **Divergence at icon level instead of system level** — divergence is for rule sets, not individual icons
- **Too many sets** — 3-4 maximum; more becomes choice paralysis
- **Mixing sets after user choice** — internal inconsistency follows
- **Skipping divergence when category is generic** — produces yet-another-Material lookalike
