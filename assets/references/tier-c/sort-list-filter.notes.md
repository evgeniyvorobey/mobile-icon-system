# sort-list-filter (tier-C)

**Tier:** C (anti-example)
**Source:** Lucide outline (`sort-list-filter.svg (lucide list-filter)`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/list-filter.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 3 (`<line>` × 3 of decreasing length)
- Total anchor points: 6 implicit anchors total
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Three horizontal lines of decreasing length stacked vertically.

## Failure mode
**Visual confusion with hamburger nav.** Three lines of decreasing length whose rhythm reads more like hamburger menu than sort control at 20pt.

## Why the LLM must NOT replicate this
At deployment size users will read this as the global navigation menu, not a sort/filter control. Compare against tier-A `filter.svg` (Tabler funnel) and `sort.svg` (Lucide arrow-up-down) — both have unmistakable silhouettes.

## Cross-reference
- icon-vocabulary.md section: Common Actions → Filter / Sort
- Aesthetic principles violated: 9 (metaphor before ornament — silhouette collides with hamburger), 5 (system over single — must distinguish from nav)
