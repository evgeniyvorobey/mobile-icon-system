# eye-tabler (tier-B)

**Tier:** B
**Source:** Tabler Icons outline (`eye-tabler.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/tabler/tabler-icons/main/icons/outline/eye.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<path>` almond + `<circle>` pupil)
- Total anchor points: ~12 path-command anchors plus 4 implicit on the circle
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Eye almond + pupil; almond constructed from cubic Béziers.

## What's missing vs tier-A
Almond uses cubic Béziers instead of arcs. Two halves not byte-mirrored — eye looks "tired", drooping slightly.

## What a generator should learn
Tier-A eye uses two arcs that are byte-mirrored around y=12 — Bézier construction loses the perfect symmetry.

## Cross-reference
- icon-vocabulary.md section: Security → Show / Hide (eye)
- Aesthetic principles applied (and where this falls short): 3 (intentional asymmetry — here it's accidental drooping, not intentional), 7 (construction visible — Béziers obscure the symmetry)
