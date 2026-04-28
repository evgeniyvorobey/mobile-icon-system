# map-pin

**Tier:** A
**Source:** Lucide outline (`map-pin.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/map-pin.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<path>` teardrop + `<circle>` inner)
- Total anchor points: ~5 path-command anchors plus 4 implicit on the circle
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Outer teardrop + `<circle cx="12" cy="10" r="3"/>` inner. Teardrop top is true semicircle radius 8 centered at (12, 10). Bottom point math-derived: convergence path uses two arcs `0 1` mirrored, ensuring teardrop bottom is tangent meeting, not cusp.

## What a generator should learn
Map pin = teardrop + circle; never "pushpin" (different semantic).

## Cross-reference
- icon-vocabulary.md section: Location → Map Pin / Location
- Aesthetic principles applied: 1 (restraint — 2 elements), 7 (construction visible — tangent meeting, mirrored arcs)
