# file

**Tier:** A
**Source:** Lucide outline (`file.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/file.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<path>` body + `<path>` corner-fold)
- Total anchor points: ~8 path-command anchors total
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Body + corner-fold `M14 2v5a1 1 0 0 0 1 1h5`. Fold is its own path, sized 5pt × 5pt. Body's right edge from y=2 to y=8 is constructed implicitly from fold — fold is geometrically necessary, not decorative. Fold radius 1 = half body's 2 (fold is "younger/sharper" than body).

## What a generator should learn
File = body + corner-fold (semantic, not decorative).

## Cross-reference
- icon-vocabulary.md section: Files & Documents → File / Document
- Aesthetic principles applied: 1 (restraint), 7 (construction visible — fold radius = body radius / 2), 9 (metaphor before ornament)
