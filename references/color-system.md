# Color System

Color application rules across an icon set. Loaded in workflow phase 5 (rules), phase 9 (hi-end craft), and phase 11 (validate). Skimmable and decision-oriented; the long-form rationale, color-theory primer, and palette-construction algorithm live in [`color-system-guide.md`](color-system-guide.md).

## 1. Why color comes last

The icon must read as **silhouette before any color is applied**. Vignelli's *Canon* (p. 28, "Semantics") frames the rule: meaning comes first, expression second. Without a meaningful silhouette, color is decoration on a shape that already failed. Wathan and Schoger (*Refactoring UI*, ch. "Color") restate this in modern terms: color discipline is a *consequence* of structural design, not a substitute for it. Their explicit anti-pattern — "color compensating for weak silhouette" — is also recorded in our [`aesthetic-principles.md`](aesthetic-principles.md) §6 "Quiet over Loud."

This is why the skill defaults to **monochrome with platform tinting**: it forces the silhouette to carry meaning under any user theme, accessibility setting, or dynamic color choice. Color enters only when the silhouette has been audited and the brand explicitly demands it.

## 2. Color application modes

Four modes. Pick one per set; do not mix modes within a single icon family.

### Mode A — Pure monochrome (default)

- **When**: every UI icon family unless brand DNA explicitly forbids
- **How**: single fill or stroke color in the master SVG (convention `#000` or `currentColor`); export as iOS PDF Template Image or Android `<vector>` with `android:tint="?attr/colorOnSurface"`
- **Auditable**: the SVG contains exactly one non-`none` `fill` value (or one `stroke`); no `linearGradient`, no `radialGradient`, no per-shape color overrides
- **Anti-pattern**: baking a brand color into the master file. iOS will then refuse to tint it for selected/unselected states; Android themed icons will ignore it; high-contrast modes break.

### Mode B — Duotone

- **When**: brand DNA documents a structural two-color identity (not a preference, a *requirement* — see [`aesthetic-principles.md`](aesthetic-principles.md) §6)
- **How**: primary mass at 60-80% of visible icon area; secondary at 20-40%. Same role assignment across every icon in the set. Document the role split in `brand-dna.md`.
- **Auditable**: the SVG has exactly two distinct `fill` values; the primary fill area is between 60% and 80% of total filled area; both colors appear in the brand palette
- **Anti-pattern**: each icon uses a different secondary color. The set has no signature, only noise.

### Mode C — Brand-tinted with single accent

- **When**: hi-end / luxury positioning where restraint is the brand voice; a single accent communicates state or hierarchy
- **How**: monochrome base + ONE accent color used in 1-2 specific moments (e.g., the active Tab Bar item, an unread-notification dot)
- **Auditable**: the *icon set as a whole* uses only two colors; accent appears only on icons documented as accented in the rules file
- **Anti-pattern**: accent color dropped onto every icon for visual interest. The accent stops being information; it becomes texture.

### Mode D — Multi-color (3+ colors)

- **When**: rare for in-app UI. Appropriate for app-launcher marks, illustration, editorial graphics, and documented brand mascots
- **How**: out of scope for *UI icon families*. If the user requests this for in-app UI, ask: is this the launcher (different skill) or actually a UI icon? If UI, redirect to Mode A or C.
- **Anti-pattern**: shipping multi-color UI icons. At 24px they read as confetti, theme tinting fights them uniformly, and CVD verification becomes guesswork.

## 3. Contrast budgets (numerical, cited)

All values are **WCAG 2.2 minima** unless marked AAA. Source: [WCAG 2.2 §1.4.11 Non-text Contrast](https://www.w3.org/TR/WCAG22/#non-text-contrast) — "graphical objects" (which includes UI icons) require **3:1 against adjacent color(s)**.

| Surface | Mono icon vs surface | Selected vs unselected differential |
|---|---|---|
| Light surface (sRGB white-ish, ~#FFFFFF–#F2F2F7) | ≥ **3:1** (AA) / ≥ 4.5:1 (target for Tab Bar glyphs) | ≥ **1.5:1** between the two states |
| Dark surface (~#000000–#1C1C1E) | ≥ **3:1** (AA) | ≥ **1.5:1** |
| Translucent material (iOS Liquid Glass, Material 3 surfaces) | ≥ **3:1 vs the worst-case backdrop the material can show**, not vs the nominal token color | ≥ **1.5:1** under the same worst-case backdrop |
| Inside a tinted active container (Material 3 navigation pill) | ≥ **3:1** of `onSecondaryContainer` vs `secondaryContainer` (Material 3 guarantees this in default schemes) | n/a — state is signaled by the pill, color reinforces |

The **1.5:1 selected-vs-unselected differential** comes from `craft-rubric.md` §7.3: at lower differential, users with low vision report inability to identify the active tab even when both states individually pass 3:1 against the bar background. This is a craft floor; aim for ≥ 2:1 for hi-end work.

For translucent materials specifically, Apple's HIG guidance is to test the icon against both the lightest and darkest backdrop the material can sit over. iOS Liquid Glass and Material 3's `surfaceContainer*` family both vary with content scroll position; a glyph that hits 4.5:1 in nominal mode can drop below 3:1 once the user scrolls a dark image underneath.

## 4. Color palette construction for icon sets

Icon palettes are **tighter than UI palettes**. Refactoring UI ("You need more colors than you think") makes the case for ten shades per UI color so layouts can layer without flatness. Icons reverse this: the same icon must read identically at 16pt and 64pt, and proliferating tones inside one icon turns it into pastiche.

Numerical recommendations:

- **Pure monochrome (Mode A)**: 1 color in the icon. Usually `currentColor` so it inherits from the parent text color.
- **Duotone (Mode B)**: 2 colors, fixed across the set. No tonal variants per icon.
- **Brand-tinted with accent (Mode C)**: 2 colors total in the set vocabulary; each individual icon uses 1.
- **Status icons (success/warning/error/info)**: 4 named colors max, one per state, with a paired shape change (see §7).
- **Multi-color (Mode D)**: rare. If used, cap at 4 colors and document each by role.

Derive the icon palette **from Brand DNA**, not invented in isolation. The brand primary becomes the active tint; the brand neutral becomes the inactive tint; the brand error/success/warning colors become the status colors. If the brand has only one color documented, use system neutrals (`UIColor.label` / `?attr/colorOnSurface`) for the rest — never invent an unbranded accent.

For tonal variants needed across themes, generate a **3-stop scale per color** (light surface stop, dark surface stop, hover/pressed). The full 11-stop Tailwind 50-950 scale is for UI surfaces, not icon glyphs; pulling stops out of an existing UI scale is fine.

## 5. Theming: dark mode + Material You + iOS Dynamic Color

### Dark mode

Inverting black to white is rarely correct. Apple HIG's dark-mode guidance (`Color and contrast`) recommends shifting to a slightly desaturated, slightly lighter variant on dark surfaces (e.g., a brand `#0066CC` becomes `#3399FF` on dark) so the perceived weight remains constant. In OKLCH terms: keep hue, drop chroma ~10-20%, raise lightness to land in the L=0.70-0.85 band on dark surfaces.

### Material You (Android 13+)

Per Android's adaptive-icon spec ([developer.android.com/develop/ui/views/launch/icon_design_adaptive](https://developer.android.com/develop/ui/views/launch/icon_design_adaptive)), the launcher icon needs a **`<monochrome>` layer** to participate in user theming. For in-app icons, the same principle applies: the Material 3 dynamic color system can recolor the icon to any tone derived from the user's wallpaper. **The silhouette must carry meaning under any tint.** If the icon depends on its baked color to be readable, Material You will break it.

### iOS Dynamic Color & Display P3

iOS semantic colors (`UIColor.label`, `UIColor.secondaryLabel`, `UIColor.tintColor`) automatically adapt to light/dark, increase-contrast, and elevated surfaces. Use semantic tokens, not literal hex, in the asset catalog whenever the icon is rendered as a Template Image.

For wide-gamut authoring: **author in sRGB by default**, in Display P3 only when the brand color is explicitly defined outside sRGB (saturated reds, electric greens, neon cyans that clip in sRGB). CSS Color 4 §10.4 covers Display P3 syntax; iOS asset catalogs accept Display P3 PNGs and PDFs.

### Bake vs runtime

| Asset | Bake | Runtime tint |
|---|---|---|
| iOS Tab Bar / Toolbar / Nav Bar glyphs | never | always (Template Image) |
| iOS launcher icon | always | never |
| Android in-app icons | never | always (`?attr/colorOnSurface` or theme attr) |
| Android adaptive launcher | foreground+background baked; `<monochrome>` layer for theming | partial — themed-icon layer is recolored by system |
| Web SVG icons | never (use `currentColor`) | always (CSS `color` cascade) |
| SF Symbols (custom) | never | rendering modes choose color (§iOS deep dive) |

## 6. Color in state pairs (Tab Bar / Bottom Nav)

Pattern:
- **Selected** = full-strength brand tint (or system tint) **and** filled silhouette
- **Unselected** = muted tint (`UIColor.secondaryLabel` / `?attr/colorOnSurfaceVariant`) **and** outlined silhouette

Color is reinforcing, never the sole signal — see [`accessibility.md`](accessibility.md) "Color-blind safety" and the WCAG warning in §3 above. If the user enables grayscale mode, the silhouette change must still convey state.

Material 3 Bottom Nav adds a **selected pill** (an `onSecondaryContainer` glyph inside a `secondaryContainer` shape). The pill, not the color, is the primary state signal there. iOS Tab Bar relies on the simpler tinted-glyph + filled/outlined pair.

Failure: tinting an outlined glyph in brand color and an outlined glyph in muted color and calling it a state pair. The shape did not change. Color-blind, grayscale, and high-contrast users see no state.

## 7. Color-blind safety

The general accessibility floor is in [`accessibility.md`](accessibility.md) "Color-blind safety." Icon-specific additions:

- **Status icons must differ in shape, not only color.** Success = check, error = X or triangle, warning = triangle, info = circle. A green dot vs red dot fails for ~8% of men.
- **Color-blind-safe status palette** (verifiable under deuteranopia, protanopia, tritanopia):
  - Success green: hue ~140° in OKLCH, chroma ~0.15, lightness 0.55-0.65
  - Error red: hue ~25° (warm-shifted away from pure red, toward orange), so it doesn't collapse with success-green under deuteranopia
  - Warning yellow/amber: hue ~80°, lightness 0.75+ for adequate contrast on white
  - Info blue: hue ~245°, lightness 0.55-0.60
- **Tools to verify (current as of 2026):**
  - **Sim Daltonism** (macOS, free, by Michel Fortin) — live screen filter; still maintained as of 2026
  - **Stark** (Figma/Sketch/Chrome plugin) — CVD simulation + contrast checker
  - **Color Oracle** (cross-platform, free) — system-wide CVD simulator
  - **Adobe Color Accessibility Tools** (web) — palette CVD check
  - macOS **System Settings → Accessibility → Display → Color Filters** — built-in protanopia/deuteranopia/tritanopia simulation
  - iOS / iPadOS **Settings → Accessibility → Display & Text Size → Color Filters** — same on device
  - Chrome DevTools **Rendering → Emulate vision deficiencies** — for web icons

Run the icon set under at least deuteranopia (most common) before ship. Hi-end work runs all three.

## 8. Brand color application — common patterns

| Pattern | Description | When |
|---|---|---|
| Brand color as primary tint | All icons rendered in `var(--color-brand-primary)` | Most products. Default. |
| Brand color as accent only | Icons in neutral; brand reserved for active/selected/notification | Luxury, restraint, hi-end positioning |
| Multi-tonal brand palette | Brand has documented tonal scale (e.g., 50-950); icons use stop-500 for default, stop-700 for pressed | Mature design systems with token discipline |
| **Anti-pattern**: every icon a different brand color | Generates set incoherence — see [`aesthetic-principles.md`](aesthetic-principles.md) §6 | Never |

## 9. Workflow integration map

| Phase | Color responsibility |
|---|---|
| **5. Rules (gate)** | Declare which mode (A/B/C/D), the contrast budget per surface, the role mapping (which token = active, which = inactive, which = accent) |
| **7. Generate** | Generate silhouettes that survive monochrome collapse — color is never the only carrier |
| **9. Hi-end craft pass** | Audit each icon against the contrast budget in every theme; verify tonal scale survives Material You and Dynamic Color |
| **11. Validate in context** | Render the set under: light, dark, increase-contrast, deuteranopia, Material You sample tints, iOS tinted vs default Tab Bar |

If validation fails on any theme, the failure is logged in `cross-icon-audit.md` with the offending icon, the failing theme, and the proposed fix.

## 10. Failure modes

- **Baking color into iOS Template Images** — silent failure; tinting silently stops working in selected/unselected states
- **Multi-color UI icons** — confetti at 24px, fights theme tinting, CVD-unsafe by default
- **Color rescuing weak silhouette** — strip color and squint; if the icon falls apart, fix the silhouette (Vignelli, *Canon*, p. 28)
- **Hue-only state distinction** — fails CVD, fails grayscale, fails high-contrast
- **Skipping CVD on duotone** — silent inaccessibility for ~8% of users
- **Different color roles per icon** — set-level incoherence; the duotone has no signature
- **Inventing an accent color not in the brand palette** — brand drift, fails brand-DNA audit
- **Using literal hex in asset catalog instead of semantic tokens** — breaks dark mode, increase-contrast, and Dynamic Color
- **Missing `<monochrome>` layer on Android adaptive icon** — locks the user out of Material You theming
- **Authoring in Display P3 when the brand color is sRGB-safe** — adds gamut complexity for no perceptual gain

## Sources

- [WCAG 2.2 §1.4.11 Non-text Contrast](https://www.w3.org/TR/WCAG22/#non-text-contrast) — 3:1 floor for graphical objects (icons)
- [Apple Human Interface Guidelines — Color](https://developer.apple.com/design/human-interface-guidelines/color) — semantic colors, dynamic color, Display P3 vs sRGB guidance
- [Apple HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials) — Liquid Glass / translucent material contrast guarantees
- [Material Design 3 — Color system overview](https://m3.material.io/styles/color/system/overview) — HCT, tonal palettes, dynamic color
- [Material Design 3 — Roles](https://m3.material.io/styles/color/roles) — `onSurface`, `primary`, `onPrimary`, `secondaryContainer` semantics
- [Android — Adaptive icons](https://developer.android.com/develop/ui/views/launch/icon_design_adaptive) — `<monochrome>` layer requirement for Material You themed icons
- [W3C CSS Color 4](https://www.w3.org/TR/css-color-4/) — `oklch()` §9.4, `color()` §10.1, Display P3 §10.4
- [Björn Ottosson — A perceptual color space for image processing (Oklab)](https://bottosson.github.io/posts/oklab/) — origin of OKLab/OKLCH
- [Tailwind CSS — Colors](https://tailwindcss.com/docs/colors) — 50-950 tonal scale in OKLCH (production reference)
- Wathan, Adam & Steve Schoger. *Refactoring UI*, self-published, 2018, ch. "Color" — color discipline, "you need more colors than you think," "don't design with hex codes"
- Vignelli, Massimo. *The Vignelli Canon*, Lars Müller Publishers, 2010, pp. 28 ("Semantics"), 56 ("Discipline") — meaning before expression
- Cheng, Karen. *Designing Type*, Yale University Press, 2005, ch. 3 — optical adjustment, perceptual lightness
- [Sim Daltonism (Michel Fortin)](https://michelf.ca/projects/sim-daltonism/) — macOS CVD simulator
- [Color Oracle](https://colororacle.org/) — cross-platform CVD simulator
- See also: [`accessibility.md`](accessibility.md), [`aesthetic-principles.md`](aesthetic-principles.md), [`craft-rubric.md`](craft-rubric.md) §7.3 (state-pair contrast)

When any of these specs feel out of date, run [`live-research.md`](live-research.md) before treating values here as current.
