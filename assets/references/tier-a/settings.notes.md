# settings

**Tier:** A
**Source:** Tabler Icons outline (`settings.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/tabler/tabler-icons/main/icons/outline/settings.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<path>` cog body + `<path>` inner circle aperture)
- Total anchor points: ~20 across both paths
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
(1) Eight teeth — the optical sweet spot. Six teeth read as a star; ten teeth blob at 20pt; eight survives. (2) Outer path uses repeating `1.724` units between cog peaks — `1.724 ≈ √3` ≈ 30°-arc chord length for an 8-tooth gear, meaning the geometry is mathematically derived, not eyeballed. (3) Inner aperture `<path d="M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"/>` is a stroked circle constructed from two arcs, ensuring the inner edge stays at exactly stroke-width offset from the cog body. The gap between teeth and inner circle (1pt at stroke 2) keeps both readable at 20pt.

## What a generator should learn
Gears have exactly 8 teeth. Inner aperture is a true circle, gap to teeth ≥0.5 × stroke width. Tooth spacing is derived from `360°/8 = 45°`, not eyeballed.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Settings / More (also System & Settings → Settings)
- Aesthetic principles applied: 2 (rhythm — 45° interval), 4 (weight perception — gap between teeth and inner circle), 7 (construction visible at 200%)
