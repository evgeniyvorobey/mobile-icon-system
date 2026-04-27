# Concept Quality

Quality gates for icon-set concepts before they enter the consistency audit. Use this in workflow phase 7 (generate the set) and phase 8 prep. Each icon must clear these gates; the set as a whole gets the consistency audit afterward.

## Per-Icon Quality Gates

Each icon must pass all four gates before consistency audit:

### Gate 1 — Meaning

- The icon represents one unambiguous concept
- The metaphor is appropriate for the destination (Home = main, not generic)
- Doesn't duplicate the meaning of another icon in the set
- Doesn't conflict with system icons the user will encounter elsewhere

Failure: ambiguous, redundant, or conflicting metaphor.

### Gate 2 — Silhouette

- Recognizable as a flat single-color silhouette (no color, no internal detail)
- Topology is stable — no thin appendages that disappear at small size
- Negative space is intentional, not leftover
- Outer contour is balanced, not lopsided

Failure: silhouette test fails (outline of icon is unrecognizable).

### Gate 3 — Recognition at intended size

- At 20pt (Tab Bar) or 24pt (Bottom Nav), the icon's meaning is clear
- No detail collapses into noise
- Stroke weight survives without becoming ink-spaghetti
- Tested against actual rendered size, not master size

Failure: details collapse, stroke gaps disappear, or shape becomes generic at target size.

### Gate 4 — Construction

- Built on the agreed grid
- Stroke weight matches set rules
- Terminals match set rules
- Corners match set rules
- Optical corrections applied per Brand DNA

Failure: improvised construction, off-grid alignment, drift from set rules.

## Set-Level Quality Cues

These are not gates per se but cues that should pass:

- **Cohesion** — icons feel like one family at first glance
- **Differentiation** — each icon is distinct from its neighbors
- **Honesty** — no icon is dressed up to compensate for weak metaphor
- **Restraint** — no icon adds detail beyond what its meaning requires

## Cliché Risk Assessment

For each icon, check against [`icon-vocabulary.md`](icon-vocabulary.md) cliché map:

- High cliché risk: standard metaphor used in standard form (low differentiation)
- Medium cliché risk: standard metaphor with small twist
- Low cliché risk: distinctive interpretation, still recognizable

Cliché risk is not automatically bad — recognition matters more than novelty in UI icons. But if the entire set is high-cliché, the set lacks brand differentiation.

## Common Quality Failures

### "Looked great in Figma" failures

- Detail at 1024px master that disappears at 24pt
- Stroke gaps that close at small size
- Anti-aliasing artifacts at non-pixel-aligned positions

### Metaphor failures

- Trying too hard for cleverness (e.g., Library as a stylized brain)
- Two metaphors fused into one icon (e.g., gear with magnifying glass = "find settings"?)
- Brand-specific metaphor that requires explanation

### Construction failures

- Stroke weight rounded to "close enough" instead of exact
- Diagonals at numeric stroke equality instead of optical compensation
- Corners with R=0 mixed in a R=2 set
- Terminal style mixed (round + square)

### Recognition failures

- Topology breaks below 20pt
- Filled and outlined variants read as different icons
- Symmetric icons missing optical centering

## Quality Output Format

Per icon, in the generation phase output:

```markdown
### Home
- Metaphor: house silhouette
- Silhouette test: ✓ (clear without color)
- 20pt recognition: ✓
- Construction: 24×24 grid, 1.75pt stroke, round terminals, 2pt corners
- Cliché risk: high (standard metaphor) — accepted, recognition prioritized

[SVG]

### Search
- Metaphor: magnifying glass at 45°
- Silhouette test: ✓
- 20pt recognition: ✓
- Construction: 24×24 grid, 1.75pt stroke, round terminals
- Cliché risk: low (45° angle + custom handle proportions)
- Optical correction: handle compensated for diagonal stroke perception

[SVG]
```

## When to Re-Generate

Send an icon back to generation if:

- Any of the 4 gates fails
- Silhouette is recognizable but feels off-brand
- Construction does not inherit Brand DNA

Do not push borderline icons forward "for now" — they will surface in evaluation and force expensive re-work.

## Failure Modes

- **Gate-passing on master size only** — must verify at intended size
- **Skipping silhouette test** — color and stroke can mask weak silhouettes
- **Treating cliché risk as binary** — most UI icons should be standard; differentiation is set-level
- **Generating before grid is locked** — phase 5 gate must close first
