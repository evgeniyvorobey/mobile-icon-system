# Liquid Glass

Liquid Glass is the iOS 26 system material — every first-party icon ships in it, and Apple gates third-party adoption through Icon Composer ([developer.apple.com/icon-composer/](https://developer.apple.com/icon-composer/), [WWDC25 Session 220](https://developer.apple.com/videos/play/wwdc2025/220/)). iOS-first brands shipping after iOS 26 must engage with this style or look platform-foreign. The style reduces to a deterministic SVG layer recipe — four layers, one gradient, one specular crescent, one under-glyph shadow — so it is implementable from rules without image generation. This pack ships in v0.4 because Liquid Glass is now the platform default on the largest installed mobile base; the construction is layer-based, not silhouette-based, so every Brand-DNA primitive is preserved underneath.

## When to use this style

**Strong fit:** iOS-first apps, iOS-priority cross-platform apps shipping for iOS 26+, brand archetypes "modern / premium / platform-native", any brand whose Brand DNA accepts gradient surfaces.

**Weak fit:** Android-first apps (Material 3 expressive will fight this material), accessibility-sensitive apps where Forced Colors must drive primary appearance, "anti-gradient by declaration" brands (Vignelli-discipline minimal brands — defer to monochrome or outlined).

**Decision flowchart hint:** if the app has no Tab Bar, the request is for a launcher — route to a logo workflow. If the app has a Tab Bar, Liquid Glass is acceptable for the launcher AND optional for in-app contexts the brand permits.

## Construction rules

### Layer model

Exactly **4 layers in z-order from back to front**:

1. `bg` — background gradient. Never flat fill. `<linearGradient>` at 135° (top-left to bottom-right). Stop 1: brand primary at 100% saturation, offset 0%, alpha 1.0. Stop 2: brand primary darkened 18-24% in HSL `L`, offset 100%, alpha 1.0. Optional third stop at 60% offset with original color at alpha 0.92 to suggest curvature.
2. `glyph` — primary symbol. Solid white (`#FFFFFF`) at alpha 1.0 default, or brand-secondary for tinted brands. Stroke follows Brand DNA.
3. `specular` — top-edge highlight. `<path>` traced along upper third of squircle, filled white at `fill-opacity="0.32"`, blurred via `<filter><feGaussianBlur stdDeviation="2.4"/></filter>` at 1024px master. Crescent shape occupying top 38% of height, tapered to nothing at the equator.
4. `shadow` — under-glyph shadow. Single soft shadow on the glyph layer only. `<filter><feGaussianBlur stdDeviation="6"/></filter>` plus `dy="3"` at 1024px master, fill `#000` at `fill-opacity="0.18"`. Lifts glyph off background.

### Numerical thresholds

- Master canvas: 1024×1024 pt (Apple standard)
- Safe area: 15% from each edge for critical elements
- Squircle corner radius: `0.2237 × side` (iOS 26 squircle constant — do not round)
- Specular blur stdDeviation: 2.4 at master scale
- Shadow blur stdDeviation: 6 at master scale; `dy=3`
- Specular fill opacity: 0.28-0.36
- Shadow fill opacity: 0.14-0.22
- Background gradient angle: 135°
- Background stop-2 darkening: 18-24% L in HSL
- Centroid shift: 1.2-1.8% downward (compensates for top-heavy specular); 2% extra for triangular glyphs

### SVG features required

`<linearGradient>`, `<radialGradient>` (circular bg variants), `<filter>` with `<feGaussianBlur>`, `<feOffset>`, `<feComposite>` (clipping specular to squircle), `<mask>` (clear-mode cutouts). All inline.

### Color rules specific to this style

Brand primary becomes background gradient stop 1; stop 2 is the same hue darkened 18-24% in HSL `L`. Glyph is white by default; switch to brand-secondary only when the brand has a documented two-color identity. Never introduce a third hue. Specular and shadow are achromatic — material light, not pigment.

### Optical correction adjustments specific to this style

The mandatory specular crescent biases visual mass toward the top of the squircle. Apply a **1.2-1.8% downward centroid shift** to the glyph layer. Triangular glyphs (play, send, location pin) need an extra 2% downward shift on top of the standard top-heavy correction in [`craft-rubric.md`](../craft-rubric.md) §1.5.

## Brand DNA mapping

| Brand DNA dimension | Behavior under Liquid Glass |
|---|---|
| Geometric alphabet | inherited unchanged (line, arc, rectangle, circle, polygon) |
| Stroke language | inherited; applies to glyph layer only |
| Terminal style | inherited unchanged |
| Corner treatment (outer) | **overridden** — forced to Apple squircle at `0.2237 × side` |
| Color logic | **augmented** — brand primary drives background gradient; glyph defaults to white |
| Optical correction | **augmented** — adds mandatory 1.2-1.8% downward centroid shift |

**Refuse if:** brand is anti-gradient by declaration (e.g., Vignelli-discipline minimal brands). Surface the conflict in phase 5 and ask the user to override their Brand DNA explicitly before proceeding.

## Accessibility implications

Default mode is contrast-safe — Liquid Glass icons ship their own background gradient. **Clear mode is dangerous**: the glyph sits over arbitrary wallpaper and inherits its contrast. Ship every icon with three tested variants (default, dark, clear). Validate clear mode against worst-case wallpaper (mid-grey 50%) at 3:1 per WCAG 2.2 §1.4.11 — see [`accessibility.md`](../accessibility.md). Specular and shadow are decorative under Forced Colors / Increase Contrast; never use them for informational content.

## Anti-patterns

1. **Heavy backdrop-blur on the icon body** — Liquid Glass is opaque in default mode; backdrop-blur belongs on a window, not an icon.
2. **Specular as a hard white stripe** instead of a blurred crescent — iPhone 4-era "glossy" treatment, retired by Apple.
3. **Multiple specular highlights per icon** — one light source. Two highlights read as two suns and break the material illusion.
4. **Stacking neumorphic inner shadows inside the gradient cell** — mixes paradigms; either Liquid Glass or neumorphism, never both.
5. **Skipping the under-glyph shadow** — icon reads as a flat sticker on a gradient, not as a glyph on glass.

## Reference library

- [developer.apple.com/icon-composer/](https://developer.apple.com/icon-composer/) — first-party tool, layer-model authority.
- [developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) — material guidance.
- [developer.apple.com/documentation/TechnologyOverviews/liquid-glass](https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass) — material characteristics.
- [WWDC25 Session 220](https://developer.apple.com/videos/play/wwdc2025/220/) — primary construction reference.
- [WWDC25 Session 361](https://developer.apple.com/videos/play/wwdc2025/361/) — Icon Composer walkthrough.
- [getskyscraper.com/blog/liquid-glass-app-icon-design-ios-26-guide](https://getskyscraper.com/blog/liquid-glass-app-icon-design-ios-26-guide) — secondary engineering reference.

Apple sources are first-party documentation; license per Apple developer agreement (use as reference for your own icons; do not redistribute Apple's icons).

## Workflow integration

- **Phase 5** — add Liquid Glass sub-rule block (layer order, gradient stops, specular `stdDeviation`, shadow `stdDeviation`, squircle radius constant). Force user to confirm three appearance modes (default, dark, clear) before vocabulary.
- **Phase 7** — each variant includes all 4 layers as separate `<g>` groups with stable IDs (`bg`, `glyph`, `specular`, `shadow`). Variant search per [`workflow.md`](../workflow.md) phase 7 still applies; the layer model is invariant.
- **Phase 8 Pass A** — layer-count check (must equal 4). Pass B asks: "Is the specular a crescent, not a stripe?" and "Does the under-glyph shadow exist?"
- **Phase 9** — optical correction adds the centroid shift above. Compare against `assets/references/tier-a-liquidglass/` (when corpus is populated).
- **Phase 11** — render every icon in default + dark + clear modes against three wallpaper backgrounds (light flat, dark flat, mid-grey 50%) and run the 3:1 check.

## Failure modes

- Specular rendered as a hard white stripe (iPhone 4 glossy era).
- Two or more specular highlights per icon — breaks single-light-source illusion.
- Background gradient flattened to a single stop — kills the material.
- Under-glyph shadow omitted — glyph reads as flat sticker.
- Squircle radius rounded to `0.22 × side` instead of exact `0.2237 × side`.
- Glyph at geometric center without the 1.2-1.8% downward centroid shift.
- Gradient applied to anti-gradient Brand DNA without explicit user override.

## Sources

See Reference library above. Plus W3C WCAG 2.2 §1.4.11 (Non-text Contrast) — [w3.org/WAI/WCAG22/Understanding/non-text-contrast.html](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).
