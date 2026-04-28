# play

**Tier:** A
**Source:** Lucide outline (`play.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/play.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>` triangle with rounded vertices)
- Total anchor points: ~6 path-command anchors (3 vertex + 3 arc)
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Single path with rounded vertices (each `a2 2 0 0 1...` arc). Triangle vertices at (5,5), (5,19), (20,12). Right vertex at x=20, left edge at x=5 → x-centroid ≈10.83, **1.17pt LEFT of canvas center 12**. Deliberate left-shift compensates for visual mass concentration toward right vertex.

## What a generator should learn
Play triangle is OPTICALLY centered, not geometrically centered. Without left-shift, triangle reads "drifting right".

## Cross-reference
- icon-vocabulary.md section: Media → Play / Pause / Stop
- Aesthetic principles applied: 3 (intentional asymmetry — optical-vs-geometric centering), 4 (weight perception — visual mass right of geo center)
