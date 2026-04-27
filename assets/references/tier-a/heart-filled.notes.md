# heart-filled

**Tier:** A
**Source:** Phosphor fill (`heart-fill.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/phosphor-icons/core/main/raw/fill/heart-fill.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (1 `<rect>` transparent canvas + 1 `<path>` silhouette)
- Total anchor points: ~13 path-command anchors in the silhouette path
- Stroke width: filled (no stroke; `fill="currentColor"` on the path)
- Coordinate system: viewBox 0 0 256 256

## Why this tier
(1) Single fill path with asymmetric distances from the heart's axis to its bottom point on left vs right (~5% asymmetry). Mass-centered, not geometry-centered. (2) The lobes use specific radii whose ratio to canvas is approximately 0.243, the golden-section-derived ratio that makes hearts feel "right." (3) Pairs with the regular Phosphor heart via shared control points.

## What a generator should learn
A filled heart is one path. Bottom-tip distances are stored asymmetrically (left ≠ right by 4-5%) for optical balance. Lobe radius / canvas ≈ 0.24.

## Cross-reference
- icon-vocabulary.md section: Social & Engagement → Like / Favorite
- Aesthetic principles applied: 1 (restraint — single path), 3 (intentional asymmetry), 8 (family resemblance with the regular variant)
