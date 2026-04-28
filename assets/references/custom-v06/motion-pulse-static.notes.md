# motion-pulse-static (custom-v06)

**Tier:** v0.6 custom calibration anchor
**Source:** Custom - original repo-authored SVG, MIT license (this repo)
**Upstream URL:** N/A (not fetched; lives only in `assets/references/custom-v06/motion-pulse-static.svg`)
**Fetched:** N/A (authored for v0.6)

## Path data / structure observations
- Element count: 9 (`<circle>` x1 + `<path>` x8).
- Total anchor points: 4 implicit circle anchors plus 16 line anchors.
- Stroke width: 1.8, round caps and joins.
- Coordinate system: viewBox 0 0 24 24.
- Pairing: static reduced-motion fallback for `motion-pulse.json`.

## What a generator should learn
A motion icon must have a complete static read, not merely a frozen in-between frame. This fallback encodes the center pulse and eight signal rays as shape, so reduced-motion users receive the same semantic state without relying on animated scale or opacity.

## Licensing / provenance
Original repo-authored work for the v0.6 additive corpus. No upstream SVG, image, brand mark, or generated third-party asset was copied or traced.
