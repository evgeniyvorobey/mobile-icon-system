# motion-pulse (custom-v06)

**Tier:** v0.6 custom calibration anchor
**Source:** Custom - original repo-authored JSON motion asset, MIT license (this repo)
**Upstream URL:** N/A (not fetched; lives only in `assets/references/custom-v06/motion-pulse.json`)
**Fetched:** N/A (authored for v0.6)

## Path data / structure observations
- Asset type: compact Lottie-style JSON, shape layers only.
- Canvas: 24 x 24, 30 fps, frames 0 through 30.
- Layers: 2 shape layers (`pulse-ring`, `center-dot`), no images, text, expressions, or external assets.
- Animated properties: ring opacity fades from 80 to 0 while scale expands from 78% to 122%.
- Pairing: `meta.reduced_motion_fallback` points to `motion-pulse-static.svg`.

## What a generator should learn
Motion should amplify a static metaphor with one readable transform, not replace the icon with animation-only semantics. The center dot stays stable while the ring breathes outward, so the motion can be dropped and the fallback still communicates a pulse or live status.

## Licensing / provenance
Original repo-authored work for the v0.6 additive corpus. No upstream JSON, animation preset, image, brand mark, or generated third-party asset was copied or traced.
