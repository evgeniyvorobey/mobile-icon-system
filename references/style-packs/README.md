# Style Packs

Style packs are deviations from the skill's monochrome default — opinionated construction recipes for icon sets that need a visual treatment beyond outlined / filled / duotone-monochrome. Each pack adds layer rules, numerical thresholds, brand-DNA overrides, and per-phase workflow guidance the skill applies on top of the base workflow.

## What style packs are (and aren't)

A style pack **is** a verbatim construction spec: layer count, layer order, filter `stdDeviation` values, opacity bands, hue-distance constraints, optical-correction adjustments, anti-pattern catalog. Every numerical threshold has a citation; Phase 8 Pass A and Pass B include style-pack-specific checks.

A style pack **is not** a free pass to override Brand DNA. Every pack contains a "Refuse if" clause. Silent override is a failure mode.

## When the skill loads them

Style packs load **in Phase 5 only**, and **only when the user has chosen a style** beyond the monochrome default. The base workflow ([`../workflow.md`](../workflow.md)) loads no style pack by default — this keeps token cost bounded for the common case (most UI icon sets are monochrome).

The Phase 5 output includes a `Visual style:` line. Options:

- `monochrome` (default) — single-color silhouettes, platform-tinted at runtime
- `outlined` — stroke-based, no fill
- `filled` — solid silhouette, no stroke
- `duotone-mono` — two opacities of one hue
- `duotone-chromatic` — true two-color (loads [`duotone-chromatic.md`](duotone-chromatic.md))
- `liquid-glass` — iOS 26 system material (loads [`liquid-glass.md`](liquid-glass.md))
- `claymorphism` — pastel "soft plastic" treatment (loads [`claymorphism.md`](claymorphism.md))
- `3d-isometric` — deterministic axonometric layer construction (loads [`3d-isometric.md`](3d-isometric.md))
- `pixel-art` — native pixel-grid construction with bitmap-aware validation (loads [`pixel-art.md`](pixel-art.md))
- `hand-drawn` — deterministic path-jitter construction with documented seed (loads [`hand-drawn.md`](hand-drawn.md))
- `custom .style-pack` — user-supplied plugin manifest (loads [`plugin-system.md`](plugin-system.md), then run `python3 ../../scripts/validate_style_pack.py <file-or-dir>`)

## Decision tree for picking a pack

1. **iOS-first or iOS-priority on iOS 26+?** If yes and brand permits gradients → [`liquid-glass.md`](liquid-glass.md).
2. **Brand has a defined two-color identity?** If yes → [`duotone-chromatic.md`](duotone-chromatic.md). One color → fall back to `duotone-mono`.
3. **Brand archetype "warm / friendly / approachable / playful-but-not-childish" with pastel-leaning palette and rounded-corner DNA?** If yes → [`claymorphism.md`](claymorphism.md).
4. **Product needs spatial/product-object affordances, maps, commerce shelves, or game inventory?** If yes and small-size fallback is acceptable → [`3d-isometric.md`](3d-isometric.md).
5. **Retro/game/native-pixel identity is the brief?** If yes and the app accepts bitmap-like crispness constraints → [`pixel-art.md`](pixel-art.md).
6. **Editorial, craft, notes, kids, wellness, or creator-tool identity?** If yes and Brand DNA allows organic imperfection → [`hand-drawn.md`](hand-drawn.md).
7. **User supplied a plugin?** Validate the `.style-pack` manifest before applying it.
8. **None of the above?** Stay on `monochrome` / `outlined` / `filled`.

A style pack does not eliminate Phase 5's mandatory user-confirmation gate. Present the chosen style and its Brand DNA implications, then wait for confirmation before generating.

## Authority order — Brand DNA versus style pack

When a pack conflicts with Brand DNA, **Brand DNA wins by default**. Each pack's "Refuse if" clause encodes the conflicts:

- Liquid Glass refuses if brand is anti-gradient by declaration.
- Chromatic Duotone refuses if brand has only one color.
- Claymorphism refuses if brand demands sharp corners or stroked icons.
- 3D/isometric refuses if the icon must work below 20pt without a flat fallback.
- Pixel-art refuses if the brand depends on smooth curves, gradients, or optical sub-pixel correction.
- Hand-drawn refuses if Brand DNA requires exact geometry, legal/medical seriousness, or reproducibility without documented seed.
- Custom plugins refuse by their manifest's `brandDnaConstraints.refuseIf` list; missing refusal criteria invalidates the plugin.

Surface the conflict in Phase 5; ask the user to override Brand DNA explicitly. Log the override in the rules document so downstream phases audit against it.

## Registry

Build the discovery registry for shipped packs and validated plugins with:

```bash
python3 ../../scripts/build_style_pack_registry.py
```

The registry reference lives in [`registry.md`](registry.md), and the generated
JSON lives at [`../../assets/style-pack-registry/registry.json`](../../assets/style-pack-registry/registry.json).
It is a discovery index only; Phase 5 Brand DNA conflict review, accessibility
review, and user confirmation still gate every non-default style.

## v0.5 style register

The v0.5 decision record lives in [`deferred-styles.md`](deferred-styles.md). Summary:

- **Shipped:** 3D/isometric, pixel-art, hand-drawn.
- **Deferred:** skeuomorphic-lite, neon/glow.
- **Rejected as style axis:** Animated/Lottie. It is now a separate motion subsystem in [`../motion-system.md`](../motion-system.md).

## Adding a new style pack

A new built-in pack must include: layer model, numerical thresholds, SVG features required, color rules, optical-correction adjustments, brand-DNA mapping table, accessibility implications, anti-patterns (3-5), reference library with license info, per-phase integration (5 / 7 / 8 / 9 / 11), failure modes (5-7), sources. Match the existing packs' structure. Register in [`../../scripts/validate_skill_repo.py`](../../scripts/validate_skill_repo.py) `REQUIRED_FILES`, in SKILL.md Phase 5 style list, and in SKILL.md Progressive Disclosure list.

For user-supplied styles, prefer a `.style-pack` manifest instead of adding built-in docs. See [`plugin-system.md`](plugin-system.md).
