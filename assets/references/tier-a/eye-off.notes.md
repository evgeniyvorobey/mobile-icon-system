# eye-off

**Tier:** A
**Source:** Lucide outline (`eye-off.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/eye-off.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 4 (`<path>` × 4)
- Total anchor points: ~12 path-command anchors across all paths
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Four sub-paths. Eye is shown HALF-CUT — pupil fragment continues arc but ends where slash crosses. Slash `m2 2 20 20` corner-to-corner exactly 45°, length `20√2 ≈ 28.28pt`. Open eye is partially redrawn so slash sits WITH the geometry.

## What a generator should learn
State-pair "X off" = redraw the geometry around the slash, not stamp slash on top.

## Cross-reference
- icon-vocabulary.md section: Security → Show / Hide (eye, off-state)
- Aesthetic principles applied: 3 (intentional asymmetry — slash diagonal), 7 (construction visible — redrawn around the slash)
