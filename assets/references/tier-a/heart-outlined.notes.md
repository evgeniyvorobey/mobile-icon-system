# heart-outlined

**Tier:** A
**Source:** Lucide outline (`heart.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/heart.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>`)
- Total anchor points: ~8 path-command anchors
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
(1) Single path. Two arcs `a5.5 5.5 0 0 1 9.591-3.676` and `A5.49 5.49 0 0 1 22 9.5` — the radii (5.5 and 5.49) are almost but not exactly equal. This 0.01 difference is intentional optical correction for the heart's right side which carries more visual weight. (2) The bottom point is constructed from cubic Béziers meeting at `y≈20.7`, with explicit 2pt rounding — no sharp point. (3) Apex notch says the two lobes meet at `(12, 6.something)` with a soft tangent, not a hard cusp.

## What a generator should learn
Heart lobes have *almost* equal radii (intentional asymmetry). The bottom V is rounded with explicit 2pt radius. The top notch is a soft tangent, not a cusp.

## Cross-reference
- icon-vocabulary.md section: Social & Engagement → Like / Favorite
- Aesthetic principles applied: 3 (intentional asymmetry — 5.5 vs 5.49), 4 (weight perception — right-side compensation), 7 (construction visible at 200%)
