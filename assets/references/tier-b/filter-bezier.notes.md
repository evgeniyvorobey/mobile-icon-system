# filter-bezier (tier-B)

**Tier:** B
**Source:** Heroicons 24/outline (`filter-bezier.svg (heroicons funnel)`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/outline/funnel.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>`)
- Total anchor points: ~12 path-command anchors (cubic Béziers)
- Stroke width: 1.5 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Funnel rendered as a closed shape with curved cone walls.

## What's missing vs tier-A
Uses cubic Béziers for cone walls instead of straight lines, softens silhouette and reduces "funnel-ness" at 20pt. Stroke 1.5 (vs Tabler 2) further reduces filter-trough mass at small sizes.

## What a generator should learn
Tier-A filter uses straight cone walls and stroke 2 — at 20pt the straight walls preserve the funnel reading.

## Cross-reference
- icon-vocabulary.md section: Common Actions → Filter / Sort
- Aesthetic principles applied (and where this falls short): 1 (restraint — cubic walls feel ornate vs straight), 7 (construction visible — Béziers harder to audit than line segments)
