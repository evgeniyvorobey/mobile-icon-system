# camera-duotone

**Tier:** A
**Source:** Phosphor duotone (`camera-duotone.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/phosphor-icons/core/main/raw/duotone/camera-duotone.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2-3 (mass layer + outline layer + sometimes a separate shutter accent)
- Total anchor points: ~16 path-command anchors total
- Stroke width: 16 units at 256-canvas on the outline
- Coordinate system: viewBox 0 0 256 256

## Why this tier
Duotone exemplar for the camera metaphor. Mass layer fills the body (with viewfinder cutout via second moveto) at `opacity="0.2"`; outline traces body + lens. Demonstrates how duotone handles cutouts (subpath inside the mass layer) — same `Z M` technique used in `bookmark-filled` and `home-mini-16`.

## What a generator should learn
Duotone cutouts use single-path `Z M` subpaths inside the mass layer — keep element count to 2 (mass + outline) wherever possible.

## Cross-reference
- icon-vocabulary.md section: Common Actions → Camera (duotone variant)
- Aesthetic principles applied: 1 (restraint — single mass path with cutout), 5 (system over single — Z M technique consistent across families)
