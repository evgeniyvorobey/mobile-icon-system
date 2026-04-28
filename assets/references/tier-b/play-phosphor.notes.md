# play-phosphor (tier-B)

**Tier:** B
**Source:** Phosphor regular (`play-phosphor.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/phosphor-icons/core/main/raw/regular/play.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>` triangle)
- Total anchor points: ~6 path-command anchors
- Stroke width: 16 units at 256-canvas
- Coordinate system: viewBox 0 0 256 256

## Why this tier
Right-pointing triangle with rounded vertices.

## What's missing vs tier-A
Vertices rounded but radius much smaller relative to canvas (8/256 ≈ 3.1% vs Lucide 2/24 ≈ 8.3%). At 20pt, Phosphor's vertices read sharp; Lucide's read softened.

## What a generator should learn
Vertex-radius-to-canvas ratio matters — Phosphor's 3.1% is too sharp at deployment sizes; Lucide's 8.3% softens correctly.

## Cross-reference
- icon-vocabulary.md section: Media → Play / Pause / Stop
- Aesthetic principles applied (and where this falls short): 4 (weight perception — vertex-radius ratio affects softness), 7 (construction visible — ratio is auditable)
