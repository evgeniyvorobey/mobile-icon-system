# scissors

**Tier:** A
**Source:** Lucide outline (`scissors.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/scissors.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 5 (`<circle>` × 2 finger-loops + `<path>` × 3 blade strokes)
- Total anchor points: ~10 path-command anchors plus 8 implicit on the circles
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Two `<circle>` finger-loops at (6,6) and (6,18), perfectly mirrored around y=12. Three blade strokes converging at (12, 12) — canvas center. **Whole icon is single rotation around (12, 12)** — fold canvas across y=12 and bottom is top.

## What a generator should learn
Scissors = mirror around y=12; everything pivots through canvas center.

## Cross-reference
- icon-vocabulary.md section: Common Actions → Cut / Trim
- Aesthetic principles applied: 2 (rhythm — pivot symmetry), 3 (intentional asymmetry — none, designed as mirror), 7 (construction visible)

## Known small-size limitation

This icon is tier-A **at its design size (24pt+)** but hard-fails the silhouette stability check at 16pt — the finger-loop circles and the blade strokes merge perceptually below 20pt because the gap between loop-edge and blade-pivot drops below 1px after anti-aliasing. **Do not naively downscale this icon to 16pt.** Cut/trim affordances at 16pt should use a simpler scissor-blade-only variant or substitute the X-mark for "remove" semantics. The grader's hard_fail on this icon is informative — it documents that two-element composites (loops + blades) need explicit small-size variants.
