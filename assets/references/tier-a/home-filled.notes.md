# home-filled

**Tier:** A
**Source:** Phosphor fill (`house-fill.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/phosphor-icons/core/main/raw/fill/house-fill.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (1 `<rect>` transparent canvas + 1 `<path>` silhouette)
- Total anchor points: ~24 path-command anchors in the silhouette path
- Stroke width: filled (no stroke; `fill="currentColor"` on the path)
- Coordinate system: viewBox 0 0 256 256

## Why this tier
(1) Single fill path — the silhouette IS the icon, no decorative cutouts. (2) Door cutout uses 4-anchor inset rect with smaller corner radius than the body — the optical-corner-radius rule: inner corners use a smaller radius than outer corners by the same ratio as their stroke distance from the centerline. (3) Pairs cleanly with the regular Phosphor house — both share 80×80 canvas anchors and identical roof arc.

## What a generator should learn
Filled icons make door/window cutouts via inset paths with proportionally-smaller corner radii — never as separate `fill="white"` shapes overlaid on top.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Home / Main
- Aesthetic principles applied: 1 (restraint — single path), 4 (weight perception — optical corner radius), 8 (family resemblance with the regular variant)
