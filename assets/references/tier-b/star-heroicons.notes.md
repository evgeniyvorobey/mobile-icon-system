# star-heroicons (tier-B)

**Tier:** B
**Source:** Heroicons 24/solid (`star-heroicons.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/solid/star.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>` filled star with arc-bumps at vertices)
- Total anchor points: ~10 path-command anchors
- Stroke width: none (fill-only)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Solid 5-point star with very small arc bumps at each vertex.

## What's missing vs tier-A
Uses 1.077 arc-bumps at each vertex (small Bézier curves) rather than rounded radii. At 24pt star looks crisp; at 16pt bumps disappear, vertices read merely sharp.

## What a generator should learn
Vertex bumps need to be ratio-correct (golden-ratio inner/outer) to survive scale-down — small constant bumps disappear.

## Cross-reference
- icon-vocabulary.md section: Social & Engagement → Star / Rate
- Aesthetic principles applied (and where this falls short): 4 (weight perception — bumps don't survive shrink), 7 (construction visible — radius constant rather than ratio)
