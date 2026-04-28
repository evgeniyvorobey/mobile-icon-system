# lock-thin (tier-C)

**Tier:** C (anti-example)
**Source:** Heroicons 24/outline (`lock-thin.svg (heroicons lock-closed)`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/outline/lock-closed.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1-2 (`<path>` body + shackle as continuous path)
- Total anchor points: ~10 path-command anchors total
- Stroke width: 1.5 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Padlock body and shackle drawn with a thinner stroke and a shackle that doesn't form a true semicircle.

## Failure mode
**Under-mass at small sizes.** Uses 4.5 shackle radius (smaller than body height/2) and stroke 1.5 instead of 2. Shackle reads as rounded U rather than true semicircle. Icon dissolves into thin lines below 20pt.

## Why the LLM must NOT replicate this
State-pair siblings need to share stroke weight; thin strokes lose mass at 16pt and the shackle's geometric reading ("true semicircle = padlock arch") collapses to a generic rounded U. Compare against tier-A `lock.svg` (Lucide): stroke 2, shackle radius 5 = body height / 2.

## Cross-reference
- icon-vocabulary.md section: Security → Lock / Unlock
- Aesthetic principles violated: 4 (weight perception — under-mass), 7 (construction visible — radius mismatch with body)
