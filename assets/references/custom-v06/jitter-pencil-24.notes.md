# jitter-pencil-24 (custom-v06)

**Tier:** v0.6 custom calibration anchor
**Source:** Custom - original repo-authored SVG, MIT license (this repo)
**Upstream URL:** N/A (not fetched; lives only in `assets/references/custom-v06/jitter-pencil-24.svg`)
**Fetched:** N/A (authored for v0.6)

## Path data / structure observations
- Element count: 4 (`<path>` x4), all stroked, no fills.
- Total anchor points: ~23 path-command anchors.
- Stroke width: 1.85 with round caps and joins.
- Coordinate system: viewBox 0 0 24 24.
- Jitter method: deterministic hand-drawn offsets, seed `v06-jitter-pencil-24-seed-137`, max intended offset 0.18 pt from the clean geometric scaffold.

## What a generator should learn
Hand-drawn style should preserve the underlying icon scaffold before adding tiny deterministic path jitter. The pencil remains readable because the silhouette, nib, seam, and eraser direction still align to a conventional 24 pt pencil metaphor. Jitter belongs on points and tangents; it must not create random stroke weight, broken joins, or different seeds across state siblings.

## Licensing / provenance
Original repo-authored work for the v0.6 additive corpus. No upstream SVG, image, brand mark, or generated third-party asset was copied or traced.
