# star-filled

**Tier:** A
**Source:** Phosphor fill (`star-filled.svg (phosphor star-fill)`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/phosphor-icons/core/main/raw/fill/star-fill.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>` filled 5-point star)
- Total anchor points: ~10 path-command anchors (10 vertices)
- Stroke width: none (fill-only)
- Coordinate system: viewBox 0 0 256 256

## Why this tier
Single fill path. **All vertices use radius 16.4 at 256-canvas (1.54%)** — much sharper than outlined star's 2.123/24 ≈ 8.8%. Filled star vertices are sharper because fill itself adds visual softness; outlined needs softer vertices to compensate for sharp stroke-cap effect at small sizes.

## What a generator should learn
Filled state-pair sibling uses sharper vertex radius than its outlined sibling — fill softens, so vertices can be sharper.

## Cross-reference
- icon-vocabulary.md section: Social & Engagement → Star / Rate (filled, state pair)
- Aesthetic principles applied: 2 (rhythm — pair), 4 (weight perception — fill vs outline compensation), 7 (construction visible)
