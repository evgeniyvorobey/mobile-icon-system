# pixel-bolt-16 (custom-v06)

**Tier:** v0.6 custom calibration anchor
**Source:** Custom - original repo-authored SVG, MIT license (this repo)
**Upstream URL:** N/A (not fetched; lives only in `assets/references/custom-v06/pixel-bolt-16.svg`)
**Fetched:** N/A (authored for v0.6)

## Path data / structure observations
- Element count: 8 (`<rect>` x8), no curves, no strokes.
- Total anchor points: 32 implicit rectangle corners.
- Stroke width: none; fill-only pixel construction.
- Coordinate system: viewBox 0 0 16 16 with integer x/y/width/height values.
- Rendering hint: `shape-rendering="crispEdges"` keeps the 1 px and 2 px grid steps sharp.

## What a generator should learn
Pixel-art icons should be authored as native-grid filled modules, not as scaled-down 24 pt outlines. The bolt reads because every edge lands on integer coordinates and the diagonal is built from stepwise rectangular clusters. Do not add antialias-dependent diagonals, subpixel nudges, or thin interior cuts at 16 pt.

## Licensing / provenance
Original repo-authored work for the v0.6 additive corpus. No upstream SVG, image, brand mark, or generated third-party asset was copied or traced.
