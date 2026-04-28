# duotone-color-only (tier-C, custom)

**Tier:** C (anti-example, hand-crafted in this repo)
**Source:** Custom — written for this calibration corpus, MIT license (this repo)
**Upstream URL:** N/A (file lives only in this repo at `assets/references/tier-c/duotone-color-only.svg`)
**Fetched:** 2026-04-27 (authored)

## Path data summary
- Element count: 2 (`<path>` mass with `fill="red"` + `<path>` outline with `stroke="black"`)
- Total anchor points: ~12 path-command anchors total
- Stroke width: 1.5 on the outline path; mass path uses `fill="red"` only
- Coordinate system: viewBox 0 0 24 24

## Why this tier
A duotone heart where the mass layer is bound to literal `red` and the outline is bound to literal `black`. The "selected" version of this icon would differ only by changing the red value; the "unselected" by going to outline-only. State is conveyed purely by color — no shape change, no stroke-weight change, no shape addition.

## Failure mode
**Color-only state for the duotone family.** Fails Forced Colors mode (the system overrides `fill="red"` and the mass-layer state vanishes), fails deuteranopia simulation (red ↔ gray collapse), and propagates the failure across every icon in a duotone set that uses the same template.

## Why the LLM must NOT replicate this
Compare against tier-A `tier-a-duotone/heart-duotone.svg` (Phosphor): both layers respond to `currentColor`, with the mass layer modulated via opacity. State changes flow through `currentColor` so accessibility-aware rendering still resolves the silhouette. Violates references/accessibility.md (state must be distinguishable without color) and aesthetic principle 6 (color compensating for weak silhouette is loud, not informative).

## Cross-reference
- icon-vocabulary.md section: State Pairs → Duotone (filled/unfilled)
- Aesthetic principles violated: 6 (color compensating for weak silhouette), 9 (metaphor before ornament — color is the only ornament carrying meaning)
