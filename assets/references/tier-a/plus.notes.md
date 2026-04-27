# plus

**Tier:** A
**Source:** Lucide outline (`plus.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/plus.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<path>` horizontal stroke + `<path>` vertical stroke)
- Total anchor points: 4 (2 endpoints per stroke)
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
(1) Two paths — `M5 12h14` and `M12 5v14`. Symmetric around (12,12). 2 + 2 = 4 anchors total. (2) Strokes terminate 5pt from each canvas edge — providing a 5pt live-area inset symmetric on all sides, the same inset used by Lucide's other primitives. (3) Round caps at every endpoint — the visual mass of the cap radius is part of the apparent stroke length, so the file pulls coordinates in by exactly stroke-radius (1pt) to keep the geometric extent inside the canvas.

## What a generator should learn
A plus is two crossing strokes, not a 12-anchor outline of a plus shape. Cap radius is accounted for by inset coordinates.

## Cross-reference
- icon-vocabulary.md section: Action Icons → Add / Create
- Aesthetic principles applied: 1 (restraint — anchor economy at its limit), 2 (rhythm — same inset used across the family), 4 (weight perception — caps accounted for in coords)
