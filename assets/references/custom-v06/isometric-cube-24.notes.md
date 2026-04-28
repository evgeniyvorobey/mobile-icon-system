# isometric-cube-24 (custom-v06)

**Tier:** v0.6 custom calibration anchor
**Source:** Custom - original repo-authored SVG, MIT license (this repo)
**Upstream URL:** N/A (not fetched; lives only in `assets/references/custom-v06/isometric-cube-24.svg`)
**Fetched:** N/A (authored for v0.6)

## Path data / structure observations
- Element count: 5 (`<polygon>` x3 + `<path>` x2).
- Total anchor points: 18 polygon points plus 17 path-command anchors.
- Stroke width: 1.25 for the outer cage and interior seams.
- Coordinate system: viewBox 0 0 24 24.
- Tonal structure: three `currentColor` faces use opacity levels .92, .78, and .62 instead of unrelated hues.

## What a generator should learn
3D/isometric UI icons need a simple planar grammar: top, left, right, outer cage, and only the seams needed to explain volume. The generator should preserve shared vertices between faces and avoid perspective drift, bevel clutter, cast shadows, or color palettes that make the icon stop behaving like a tintable UI glyph.

## Licensing / provenance
Original repo-authored work for the v0.6 additive corpus. No upstream SVG, image, brand mark, or generated third-party asset was copied or traced.
