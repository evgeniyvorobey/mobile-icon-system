# Deferred Style Status

This file tracks v0.5 style-pack decisions. Motion / Lottie is intentionally excluded from the count because it is a separate motion subsystem, not a visual style pack.

## Status list

| Style | v0.5 status | Decision |
|---|---|---|
| 3D / Isometric | Shipped | Added deterministic SVG/vector construction in [`3d-isometric.md`](3d-isometric.md). |
| Pixel Art | Shipped | Added bitmap-grid construction and bitmap-aware QA requirements in [`pixel-art.md`](pixel-art.md). |
| Hand-Drawn | Shipped | Added seeded deterministic path-jitter construction in [`hand-drawn.md`](hand-drawn.md). |
| Skeuomorphic Lite | Deferred | Still too illustrative for the UI-icon workflow; needs material-specific recipes before it can be deterministic. |
| Neon / Glow | Deferred | Needs a renderer-safe glow recipe and contrast-preserving fallback before it can ship. |

## Shipped in this batch

Three deferred styles now have standalone pack specs:

- [`3d-isometric.md`](3d-isometric.md) resolves the camera ambiguity with a fixed axonometric projection, top / front / side layers, one light vector, bounded shadows, and a flat 16pt fallback.
- [`pixel-art.md`](pixel-art.md) resolves the SVG-first mismatch by making target-size bitmap matrices the source of truth and requiring bitmap-aware grading.
- [`hand-drawn.md`](hand-drawn.md) resolves stochastic drift by freezing seed generation, jitter amplitude, protected anchors, anchor budgets, and baseline alignment.

## Still deferred or separate

Skeuomorphic Lite remains deferred because a shippable pack would need deterministic material recipes for leather, metal, paper, glass, and fabric while still preserving small-size legibility. That is broader than a single style treatment.

Neon / Glow remains deferred because glow often becomes the contrast carrier and breaks under Forced Colors / Increase Contrast. A future pack needs a solid primary silhouette plus a purely decorative glow layer, with Android-vector and no-filter fallbacks.

Neumorphism remains rejected because its typical light-shadow construction depends on low-contrast adjacent surfaces. That conflicts with WCAG non-text contrast expectations for informative icons unless the primary glyph is made solid, at which point the result is closer to claymorphism.

Motion / Lottie is handled by [`../motion-system.md`](../motion-system.md). It should not be counted as a style pack.

## Integration notes

The shared files register these packs in the style-pack README, skill Phase 5 style list, progressive-disclosure list, changelog, and validator.
