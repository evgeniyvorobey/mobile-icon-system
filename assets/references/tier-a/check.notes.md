# check

**Tier:** A
**Source:** Lucide outline (`check.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/check.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>`)
- Total anchor points: 3 (one Move, two Line/relative segments forming the check stroke)
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
(1) Single 3-anchor path: `M20 6 9 17l-5-5`. (2) The angles are precisely chosen — vector from (4,12) to (9,17) is ↗ at 45°; vector from (9,17) to (20,6) is ↖ at 45°. The check is two 45° strokes, not "approximately diagonal." (3) The bend point sits at `(9, 17)` — left of horizontal center, so the long stroke (right side) carries more visual weight. This is correct for LTR reading: the eye finishes on the strong upward-right gesture.

## What a generator should learn
A check is two 45° lines meeting at a sharply offset bend. The right side is longer than the left — never symmetric.

## Cross-reference
- icon-vocabulary.md section: Status & Feedback → Success
- Aesthetic principles applied: 3 (intentional asymmetry — left arm shorter than right), 7 (construction visible — exact 45°), 9 (metaphor before ornament)
