# star-mini-16

**Tier:** A
**Source:** Heroicons 16/solid (mini) (`star-mini-16.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/16/solid/star.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>` filled star, no stroke)
- Total anchor points: ~10 path-command anchors
- Stroke width: none (mini icons are fill-only)
- Coordinate system: viewBox 0 0 16 16

## Why this tier
16pt-mini exemplar of the star metaphor. Compared to the regular 24pt outlined star, the mini version (a) converts the stroke into a fill — at 16pt strokes lose half their pixel allocation to anti-aliasing and become indistinct, so fills are mandatory; (b) drops the rounded vertex radii (or makes them proportionally larger relative to the 16-canvas) so the star reads crisp at native size; (c) omits the satellite accents that a 24pt sparkle would have — at 16pt those vanish completely.

## What a generator should learn
Mini exemplars (16pt) are fill-only, with proportionally larger rounding and zero microelement decoration. Don't shrink a 24pt outlined icon — author a mini variant.

## Cross-reference
- icon-vocabulary.md section: Native-small / Mini → Star (16pt)
- Aesthetic principles applied: 4 (weight perception — fills survive 16pt where strokes don't), 5 (system over single — mini family has its own rules)
