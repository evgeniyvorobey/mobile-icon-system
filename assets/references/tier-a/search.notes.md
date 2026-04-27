# search

**Tier:** A
**Source:** Lucide outline (`search.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/search.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<path>` handle + `<circle>` lens)
- Total anchor points: ~5 (2 in the handle path, 4 implicit on the circle)
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
(1) Anchor economy is perfect — `<circle cx="11" cy="11" r="8"/>` plus `<path d="m21 21-4.34-4.34"/>`. Two elements, total 4 implicit anchors. (2) The handle terminates at `(21, 21)` and meets the lens at `(16.66, 16.66)` — both points sit on the line `y=x`, meaning the handle is exactly 45°. The vector `4.34 ≈ 8/√(2) × small adjustment` ≈ correct distance from circle edge to corner with a small gap so the handle doesn't visually fuse with the lens at small sizes. (3) Lens is offset to `cx=11` not `cx=12` — optically corrects for the handle's visual weight in the lower-right.

## What a generator should learn
Magnifying glass = circle primitive + 45° line primitive. Lens center is offset from grid center toward the side opposite the handle. The handle does not touch the lens edge.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Search / Discover
- Aesthetic principles applied: 1 (restraint — two primitives only), 3 (intentional asymmetry — lens offset to cx=11), 4 (weight perception — optical centering)
