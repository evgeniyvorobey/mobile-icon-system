# Style Packs

Style packs are deviations from the skill's monochrome default — opinionated construction recipes for icon sets that need a visual treatment beyond outlined / filled / duotone-monochrome. Each pack adds layer rules, numerical thresholds, brand-DNA overrides, and per-phase workflow guidance the skill applies on top of the base workflow.

## What style packs are (and aren't)

A style pack **is** a verbatim construction spec: layer count, layer order, filter `stdDeviation` values, opacity bands, hue-distance constraints, optical-correction adjustments, anti-pattern catalog. Every numerical threshold has a citation; Phase 8 Pass A and Pass B include style-pack-specific checks.

A style pack **is not** a free pass to override Brand DNA. Every pack contains a "Refuse if" clause. Silent override is a failure mode.

## When the skill loads them

Style packs load **in Phase 5 only**, and **only when the user has chosen a style** beyond the monochrome default. The base workflow ([`../workflow.md`](../workflow.md)) loads no style pack by default — this keeps token cost bounded for the common case (most UI icon sets are monochrome).

The Phase 5 output now includes a `Visual style:` line. Options:

- `monochrome` (default) — single-color silhouettes, platform-tinted at runtime
- `outlined` — stroke-based, no fill
- `filled` — solid silhouette, no stroke
- `duotone-mono` — two opacities of one hue
- `duotone-chromatic` — true two-color (loads [`duotone-chromatic.md`](duotone-chromatic.md))
- `liquid-glass` — iOS 26 system material (loads [`liquid-glass.md`](liquid-glass.md))
- `claymorphism` — pastel "soft plastic" treatment (loads [`claymorphism.md`](claymorphism.md))

## Decision tree for picking a pack

1. **iOS-first or iOS-priority on iOS 26+?** If yes and brand permits gradients → [`liquid-glass.md`](liquid-glass.md).
2. **Brand has a defined two-color identity?** If yes → [`duotone-chromatic.md`](duotone-chromatic.md). One color → fall back to `duotone-mono`.
3. **Brand archetype "warm / friendly / approachable / playful-but-not-childish" with pastel-leaning palette and rounded-corner DNA?** If yes → [`claymorphism.md`](claymorphism.md).
4. **None of the above?** Stay on `monochrome` / `outlined` / `filled`.

A style pack does not eliminate Phase 5's mandatory user-confirmation gate. Present the chosen style and its Brand DNA implications, then wait for confirmation before generating.

## Authority order — Brand DNA versus style pack

When a pack conflicts with Brand DNA, **Brand DNA wins by default**. Each pack's "Refuse if" clause encodes the conflicts:

- Liquid Glass refuses if brand is anti-gradient by declaration.
- Chromatic Duotone refuses if brand has only one color.
- Claymorphism refuses if brand demands sharp corners or stroked icons.

Surface the conflict in Phase 5; ask the user to override Brand DNA explicitly. Log the override in the rules document so downstream phases audit against it.

## v0.5 deferred styles

Considered for v0.4 and explicitly rejected:

- **Skeuomorphism** — industry-dead since 2013 flat pivot; not implementable as deterministic SVG rules.
- **Neumorphism** — structurally fails WCAG 2.2 §1.4.11 (low-contrast adjacent values per [Axess Lab](https://axesslab.com/neumorphism/)). Claymorphism delivers similar warmth without the contrast trap.
- **3D / isometric** — requires perspective camera (image-gen) or expensive axonometric rules; weak license-clean reference library.
- **Hand-drawn** — requires stochastic engine (path jitter); regenerated icons drift; weak license-clean library.
- **Pixel art** — wrong primitive for SVG-first skill; narrow applicability (gaming / retro only).
- **Animated / Lottie** — scope expansion (motion sub-spec); deferred as separate sub-system rather than style axis.

## Adding a new style pack

A new pack must include: layer model, numerical thresholds, SVG features required, color rules, optical-correction adjustments, brand-DNA mapping table, accessibility implications, anti-patterns (3-5), reference library with license info, per-phase integration (5 / 7 / 8 / 9 / 11), failure modes (5-7), sources. Match the three existing packs' structure. Register in [`../../scripts/validate_skill_repo.py`](../../scripts/validate_skill_repo.py) `REQUIRED_FILES`, in SKILL.md Phase 5 style list, and in SKILL.md Progressive Disclosure list.
