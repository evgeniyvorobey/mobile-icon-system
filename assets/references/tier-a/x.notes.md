# x

**Tier:** A
**Source:** Lucide outline (`x.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/x.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<path>` x2 — two diagonal strokes)
- Total anchor points: 2 path-command anchors per stroke (4 endpoints total)
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
(1) Two paths, two anchors each: `M18 6 6 18` + `m6 6 12 12`. (2) Both lines are exactly 45°. They cross at `(12, 12)` precisely. (3) 6pt inset from each canvas edge — same as `plus.svg`, ensuring "x" and "+" are visually balanced when sat next to each other in a UI (a critical consistency rule for action-icon families).

## What a generator should learn
X is two 45° crossing strokes with the SAME inset as a `+` so the pair feels balanced.

## Cross-reference
- icon-vocabulary.md section: Action Icons → Close / Dismiss
- Aesthetic principles applied: 1 (restraint — anchor economy), 2 (rhythm — same inset across the +/× pair), 8 (family resemblance — pairs with plus.svg)
