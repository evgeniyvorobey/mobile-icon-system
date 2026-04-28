# gear-duotone

**Tier:** A
**Source:** Phosphor duotone (`gear-duotone.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/phosphor-icons/core/main/raw/duotone/gear-duotone.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (mass layer + outline layer)
- Total anchor points: ~22 path-command anchors total
- Stroke width: 16 units at 256-canvas on the outline
- Coordinate system: viewBox 0 0 256 256

## Why this tier
Duotone exemplar for the settings/gear metaphor. Phosphor's gear has 8 teeth (matching tier-A `settings.svg`'s sweet-spot count). Mass layer fills the cog body (with the inner aperture cut out via second moveto) at `opacity="0.2"`; outline layer traces the teeth contour. Both layers bind to `currentColor`, so monochrome rendering (Forced Colors) collapses cleanly to the outline alone.

## What a generator should learn
Duotone family preserves tier-A craft constraints (8-tooth gear, golden-ratio star, etc.) — it's a styling layer, not a relaxation of the geometry.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Settings / More (duotone variant)
- Aesthetic principles applied: 5 (system over single — duotone preserves underlying craft), 7 (construction visible — 8-tooth count survives styling)
