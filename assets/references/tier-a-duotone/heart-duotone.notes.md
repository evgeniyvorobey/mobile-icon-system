# heart-duotone

**Tier:** A
**Source:** Phosphor duotone (`heart-duotone.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/phosphor-icons/core/main/raw/duotone/heart-duotone.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (mass layer + outline layer)
- Total anchor points: ~12 path-command anchors total
- Stroke width: 16 units at 256-canvas on the outline
- Coordinate system: viewBox 0 0 256 256

## Why this tier
Duotone exemplar for the heart metaphor. Same template as bell-duotone — mass layer at `opacity="0.2"`, both layers tied to `currentColor`. Inherits the heart's intentional left/right asymmetry from the regular Phosphor heart construction. Demonstrates the duotone family's accessibility-correct alternative to color-only state (compare anti-example `tier-c/duotone-color-only.svg`).

## What a generator should learn
State pair siblings within a duotone family share construction; never use literal colour values where `currentColor` would suffice.

## Cross-reference
- icon-vocabulary.md section: Social & Engagement → Like / Favorite (duotone variant)
- Aesthetic principles applied: 5 (system over single — same template as other duotones), 6 (color compensating fail — opacity-shape, not color-only)
