# battery-low

**Tier:** A
**Source:** Lucide outline (`battery-low.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/battery-low.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 3 (`<rect>` body + `<path>` cap + `<line>` low-cell)
- Total anchor points: ~5 implicit anchors plus 4 implicit on rect
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Body identical + two parallel "low-cell" lines `M22 14v-4` and `M6 14v-4`. **One inner cell at x=6** indicates "1/4 battery". **Body unchanged across battery states** — only interior content changes. Canonical state-progression language: empty/low/charging share immutable body.

## What a generator should learn
Battery family = immutable body, varying interior — never change the silhouette.

## Cross-reference
- icon-vocabulary.md section: Status → Battery (low state)
- Aesthetic principles applied: 2 (rhythm — state progression), 5 (system over single — shared family body)
