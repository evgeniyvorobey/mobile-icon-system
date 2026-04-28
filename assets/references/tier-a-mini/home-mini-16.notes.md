# home-mini-16

**Tier:** A
**Source:** Heroicons 16/solid (mini) (`home-mini-16.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/16/solid/home.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>` filled house silhouette)
- Total anchor points: ~8 path-command anchors
- Stroke width: none (mini icons are fill-only)
- Coordinate system: viewBox 0 0 16 16

## Why this tier
16pt-mini exemplar of the home metaphor. The 24pt outlined house has a separate roof and body; at 16pt those merge into a single filled silhouette. Door cutout still present (so the silhouette doesn't blob) but rendered via subpath cutout (single path with `Z M`) rather than a separate `<rect>` — fewer elements survives the rasterization to 16×16 pixels.

## What a generator should learn
16pt home = single fill silhouette with door as subpath cutout; merge separate elements into one path.

## Cross-reference
- icon-vocabulary.md section: Native-small / Mini → Home (16pt)
- Aesthetic principles applied: 1 (restraint — single path), 4 (weight perception — fill survives), 5 (system over single — mini-family rule)
