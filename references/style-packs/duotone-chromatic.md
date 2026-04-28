# Chromatic Duotone

Chromatic Duotone is the **true two-color** variant — distinct from `duotone-monochrome` (which uses two opacities of one hue). Phosphor ships 7,488 duotone icons in this family ([phosphoricons.com](https://phosphoricons.com), MIT per [github.com/phosphor-icons/core/blob/main/LICENSE](https://github.com/phosphor-icons/core/blob/main/LICENSE)); Untitled UI ships 4,600+; DuoIcons (MIT) and Iconoir (MIT) provide additional license-clean libraries. By 2026 UI library adoption, chromatic duotone is the dominant non-monochrome treatment.

This pack ships in v0.4 because the technical lift is small (two paths, two fills, one opacity), the reference corpus is large and license-clean, and the style fills a gap `duotone-monochrome` cannot: brands whose identity depends on **two hues** rather than two values of one hue.

## When to use this style

**Strong fit:** brands with a documented two-color identity (primary + accent), product-led brands wanting a friendlier alternative to flat outlined sets, brands whose icon system must read at both 16pt and 32pt. Phosphor's duotone family is the calibration corpus.

**Weak fit:** monochrome-only brands (chromatic duotone over-colors the row), brands without a defined accent (introducing one is dishonest), stroke-only Brand DNA that refuses fills.

**Decision flowchart hint:** if the brand has only one color, refuse and fall back to `duotone-monochrome`. If the secondary color is reserved (e.g., for error states), refuse and surface in phase 5.

## Construction rules

### Layer model

Exactly **2 layers**, both flat fills, no gradients, no filters:

1. `secondary` — accent mass. Body, container, or background plate. Filled at brand-secondary at `fill-opacity="0.32"`. The 32% is empirically derived: Phosphor uses 0.2; Untitled UI ~0.4; DuoIcons defaults 0.5. 32% is the contrast-tested middle holding 3:1 against `#FFFFFF` for most brand mid-tones.
2. `primary` — leading ink. Foreground silhouette, the part carrying the metaphor. Filled at brand-primary at `fill-opacity="1.0"`.

The two layers are **disjoint paths** (`fill-rule="evenodd"`) — never overlap except at the seam. Overlap creates a third color from alpha-blending and breaks the two-color promise.

### Numerical thresholds

- Secondary fill opacity: **0.30-0.36** on light mode, **0.38-0.44** on dark mode (Weber-Fechner perception correction)
- Path count: exactly **2**
- Anchor budget per layer: same as monochrome equivalent (8-14 anchors typical at 24pt, per [`craft-rubric.md`](../craft-rubric.md) §3.1)
- Color hue distance: secondary within **60° hue (HSL)** of primary, or within **30°** of brand accent
- Total layer count: 2
- Optical mass compensation: secondary sized **4-6% larger** than its monochrome equivalent (the 32% opacity reads visually lighter than its area suggests)

### SVG features required

Two `<path>` elements. `fill-rule="evenodd"`. `fill-opacity` on the secondary path. **No `<filter>`, no `<linearGradient>`, no `<radialGradient>`.** CSS `currentColor` may be exposed as `var(--icon-primary)` and `var(--icon-secondary)` for theme-able variants — but the SVG master must include hard-coded fallback fills so the icon survives raster export and Forced-Colors environments.

### Color rules specific to this style

Two and only two colors, both from brand tokens. **Never a third.** 32% opacity canonical for secondary on light mode; **40% on dark mode** (Weber-Fechner perception). Primary must have higher contrast against surface than secondary; if not, swap them. Secondary must share hue family with primary or with brand accent — random hue pairs make the set read as flag iconography.

### Stroke-style sub-variant

Outlined-style brands use a "duo-stroke" sub-variant: the secondary path is stroked at brand stroke weight at 32% opacity rather than filled. Document the choice in phase 5; do not silently swap.

### Optical correction adjustments specific to this style

Apply secondary-mass compensation: enlarge the secondary path by **4-6%** of its bounding-box dimension, OR shift the icon centroid by **0.3-0.6pt** toward the secondary mass. On top of the standard corrections in [`craft-rubric.md`](../craft-rubric.md) §1.

## Brand DNA mapping

| Brand DNA dimension | Behavior under Chromatic Duotone |
|---|---|
| Geometric alphabet | inherited unchanged |
| Stroke language | **disabled by default** (style is fill-based); switch to duo-stroke sub-variant if Brand DNA is stroke-only |
| Terminal style | inherited unchanged |
| Corner treatment | inherited unchanged |
| Color logic | **overridden** — two-color rule replaces single-ink defaults; tertiary forbidden |
| Optical correction | **augmented** — adds secondary-mass compensation (4-6% size or 0.3-0.6pt centroid shift) |

**Refuse if:** the brand has only one color in its palette. Fall back to `duotone-monochrome` and surface the conflict in phase 5.

## Accessibility implications

Light-mode contrast: the **primary fill must hit 3:1 against surface alone**, ignoring secondary. The secondary at 32% over white evaluates to roughly 1.5-2.0:1 — never carry informational weight on secondary alone. State changes must rely on the primary path's structure or fill swap, never on secondary opacity. **Forced-Colors mode collapses both fills to system colors** — design so the metaphor reads when both paths render at 100% same color. The disjoint-path constraint is accessibility insurance, not just construction hygiene. See [`accessibility.md`](../accessibility.md).

## Anti-patterns

1. **Three-color "triotone"** — secondary + tertiary at varying opacities. No longer duotone; mini-illustration.
2. **Overlapping primary and secondary paths** — alpha-blending introduces a third color and breaks the two-color promise.
3. **Secondary at opacity 0.5** — too heavy, dilutes the primary lead.
4. **Random hue pairs** — set reads as flag iconography. Constrain hue distance per the numerical threshold above.
5. **Treating secondary as a drop shadow** — a darker primary placed below and to the right is monochrome-with-shadow, not chromatic duotone.

## Reference library

- [phosphoricons.com](https://phosphoricons.com) — MIT, 7,488 icons across 6 styles including duotone (verified MIT 2023 at [github.com/phosphor-icons/core/blob/main/LICENSE](https://github.com/phosphor-icons/core/blob/main/LICENSE))
- [duoicons.vercel.app](https://duoicons.vercel.app/) — MIT, 91 icons, theme-able primary/secondary via CSS variables
- [iconoir.com](https://iconoir.com/) — MIT, 1,671 icons, theme-able multi-fill (verified MIT at [github.com/iconoir-icons/iconoir/blob/main/LICENSE](https://github.com/iconoir-icons/iconoir/blob/main/LICENSE))
- [untitledui.com/icons](https://www.untitledui.com/icons) — Duocolor and Duotone styles
- [hugeicons.com/icons/duotone](https://hugeicons.com/icons/duotone) — duotone variant in rounded / standard / sharp formats

## Workflow integration

- **Phase 5** — duotone sub-block (secondary opacity, secondary mass compensation, hue-distance constraint). Force the user to declare which two brand tokens map to primary and secondary before proceeding.
- **Phase 7** — each variant produces a 2-layer SVG with `<path id="secondary" fill-opacity="0.32"/>` and `<path id="primary"/>`. Disjoint-path check is mandatory.
- **Phase 8 Pass A** — 2-layer / 2-color count check (any third color is a fail). Pass B asks: "Is the primary the metaphor-carrier?" and "Does the secondary contribute mass, or is it just shade?"
- **Phase 9** — apply secondary-mass compensation. Compare against `assets/references/tier-a-duotone/` (Phosphor + DuoIcons mirror, when corpus is populated).
- **Phase 11** — primary-only contrast check (3:1 against surface, secondary ignored). Render in Forced-Colors / High-Contrast simulator and verify metaphor still reads when both paths collapse to the same color.

## Failure modes

- Three or more visible colors per icon — fails Pass A.
- Primary and secondary paths overlap, producing a third blended color.
- Secondary fill opacity outside 0.30-0.36 (light) / 0.38-0.44 (dark).
- Hue distance > 60° between primary and secondary with no shared accent anchor.
- Primary contrast < 3:1 against surface — accessibility fail regardless of secondary.
- Secondary used as drop shadow (offset down-right, darker hue).
- Brand has one color and the LLM invents a secondary — fails Brand DNA inheritance per [`brand-dna-input.md`](../brand-dna-input.md).

## Sources

See Reference library above. Plus W3C WCAG 2.2 §1.4.11 — [w3.org/WAI/WCAG22/Understanding/non-text-contrast.html](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html); Microsoft Forced Colors Mode documentation referenced in [`accessibility.md`](../accessibility.md).
