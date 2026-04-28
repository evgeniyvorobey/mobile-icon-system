# Color System — Deep Dive

Long-form reference for color decisions in icon sets. Loaded only when phase 9 demands hi-end craft work, when the user explicitly requests color-system rationale, or when extending the system to a new platform. Builds on [`color-system.md`](color-system.md); does not replace it.

## 1. Color theory primer for icon designers

### Color spaces, ranked by relevance to icon work

| Space | What it models | When it matters for icons |
|---|---|---|
| **sRGB / Hex** | Device-native gamut, 8-bit per channel | Storage and exchange format. Master SVG fills, asset catalog colors. Universal compatibility. |
| **HSL / HSV** | Perceptually-naive cylindrical model | Convenient for designers but **lies about perceived lightness**: a yellow at L=50% reads vastly brighter than a blue at L=50%. Avoid for tonal-scale construction. |
| **OKLCH** | Perceptually uniform cylindrical model (Björn Ottosson, 2020) | The recommended space for **palette construction, dark-mode color shifts, and gradient interpolation**. Equal lightness steps look like equal steps. |
| **OKLab** | Perceptually uniform Cartesian model | Same data as OKLCH, different coordinates. Use OKLab for color *math* (averaging, blending), OKLCH for *human* manipulation (pick a hue, dial chroma). |
| **CIELAB** | Older perceptual model (CIE 1976) | Print and color science legacy. OKLab fixes its hue-rotation issues for blue. Mostly skip in icon work. |
| **HCT** | Material 3's perceptual model (CAM16-based) | Required when authoring for Material You — Material's tonal palettes are HCT-derived. Conceptually similar to OKLCH but tuned for Material's contrast guarantees. |
| **Display P3** | Wide-gamut RGB working space | Required when brand colors clip in sRGB (saturated reds, electric greens). Apple authoring default since 2016. |

### Why OKLCH is the recommended modern space

Björn Ottosson released Oklab in 2020 to fix two specific failures of HSL/HSV and CIELAB:

1. **Equal HSL lightness does not look equal**. A pure yellow at HSL `60° 100% 50%` is perceptually about 3× brighter than a pure blue at HSL `240° 100% 50%`. This breaks tonal-scale construction.
2. **CIELAB has hue-rotation artifacts** for blues — interpolating from blue toward white in CIELAB shifts the hue toward purple en route, producing muddy mid-tones in gradients and tonal scales.

OKLCH preserves perceived lightness across hues and interpolates linearly. Concrete consequences for icons:

- A 50% lightness OKLCH icon on a 100% lightness background has predictable contrast regardless of hue
- Interpolating between selected and unselected colors in OKLCH avoids muddy mid-states during transitions
- A tonal scale `[0.10, 0.25, 0.40, 0.55, 0.70, 0.85, 0.95]` produces visually even steps for any hue

CSS Color Level 4 (W3C) standardized `oklch()` and `oklab()` notations (§9.3-9.4); browser support reached all major engines by 2023. Tailwind CSS adopted OKLCH as the native color space for its v4 default palette in 2024 (every `--color-*-NNN` variable in [tailwindcss.com/docs/colors](https://tailwindcss.com/docs/colors) is an `oklch(...)` declaration). Photoshop's gradient tool ships an OKLab interpolation mode. The Material 3 HCT space is, philosophically, the same project for Material's contrast guarantees.

### Color appearance models

A color "looks different" on different surfaces because of three context effects, all of which matter at icon scale:

- **Simultaneous contrast** — a gray glyph appears warmer on a cool background, cooler on a warm background
- **Crispening** — small lightness differences look larger on midtone backgrounds than on white or black
- **Hunt effect** — chromatic colors look more saturated at higher luminance

For icons specifically: a glyph drawn in `#666666` reads as a clear gray on a white surface but as a brown-ish smear on an orange-tinted Material 3 surface. The brand-primary tint that looks luxurious on the white nav bar can look muddy on the dark surface. Authoring once and assuming it ports is the failure mode; testing per theme is the discipline.

## 2. Brand color extraction from logo SVG (mechanics)

### From an SVG file

1. Read every `<path>`, `<rect>`, `<circle>`, `<polygon>` and look for `fill="..."`, `stroke="..."`, and inline `style="fill: ..."`
2. Read `<linearGradient>` / `<radialGradient>` and inspect `<stop stop-color="...">` values
3. Read `<defs>` for reusable color symbols
4. **Tally**: which color appears in the largest area? That is the brand primary candidate. Which appears in the second-largest? Secondary candidate. Are there small-area accents that recur? Tertiary.

Be wary of:
- `currentColor` — means "inherits from parent CSS color"; the SVG itself is not authoritative
- `none` — fill/stroke explicitly disabled
- CSS-classed fills (`class="text-brand-primary"`) — must look up the class definition in the consuming stylesheet
- Per-instance overrides in HTML usage (e.g., `<svg style="color: red">`) — the master file does not know about these

### From a design system file

Order of authority when the brand exposes multiple color sources:

1. **Design tokens (JSON / Style Dictionary / Tokens Studio)** — canonical
2. **CSS custom properties** (`var(--color-brand-primary)`) — canonical for web; verify the value matches token
3. **Tailwind config / theme object** — canonical when the team uses Tailwind end-to-end
4. **Figma / Sketch published styles** — canonical for design but should map to a token
5. **Hex values pasted in marketing materials** — last resort; usually drift from the source of truth
6. **Logo SVG inspection** — last-last resort; useful only when no design system file exists

When sources conflict, project audit (the design system) wins, per [`sources.md`](sources.md) authority order. Document the canonical source in `brand-dna.md` so subsequent passes don't re-derive.

## 3. Tonal scale construction

### The 50-950 scale (industry default)

Tailwind, Material, and Radix all converge on an 11-stop scale:

`50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950`

`500` is the brand "default" stop — what shows up when someone says "the blue." `50-200` are surfaces (subtle backgrounds, hover layers). `300-400` are decoration. `500-700` are interactive elements and icons. `800-950` are text and high-contrast accents.

### Deriving a scale from a brand color in OKLCH

Recipe:

1. Convert the brand primary hex to OKLCH (e.g., `#0066CC` → roughly `oklch(0.50 0.16 250)`)
2. Hold the **hue** (third number) constant for the scale's identity
3. Adjust **lightness** (first number) at fixed stops:

   | Stop | Lightness | Notes |
   |---|---|---|
   | 50 | 0.97 | Faintest tint, surface only |
   | 100 | 0.93 | Hover surface |
   | 200 | 0.87 | Disabled background |
   | 300 | 0.78 | Light decoration |
   | 400 | 0.66 | Subdued accent |
   | **500** | **0.55** | Default brand, default icon tint |
   | 600 | 0.46 | Hover state, pressed icon |
   | 700 | 0.38 | Active text on light, focus ring |
   | 800 | 0.30 | High-contrast text |
   | 900 | 0.22 | Headlines on light |
   | 950 | 0.15 | Deepest, near-black with brand hue |

4. Adjust **chroma** (second number) along the lightness curve. Chroma must be reduced toward the lightness extremes — pure colors clip into the sRGB gamut at L<0.20 and L>0.95. Rule of thumb: chroma peaks at L=0.55-0.65 and falls off symmetrically.

### Why icons use only 3-5 stops from the 11

Icons need: **default**, **hover/pressed**, **disabled**, optionally **accent** and **selected-container**. That is 3-5 of 11 stops. The rest are for UI layout (cards, dividers, headers).

Icon-specific stop usage:

| Role | Light theme | Dark theme |
|---|---|---|
| Default monochrome icon | 700 (high contrast on white) or use neutral-500 | 200-300 (high contrast on near-black) |
| Hover / pressed | 800 light / 100 dark | 100 light / 300 dark |
| Disabled | 300 with reduced opacity 0.4 | 700 with opacity 0.4 |
| Active selected (Tab Bar) | 600 (the brand "voice") | 400 (chroma-reduced for dark surface) |
| Accent (notification dot) | brand-500 + a status color stop | mirrored |

### Verifying contrast pairs

Each adjacent stop should differ by at least **1.5:1 contrast ratio** so that hover and pressed states are visibly distinct. WCAG calculator or Stark plugin verifies. If two adjacent stops fail 1.5:1, your lightness curve is too gentle in that region — open up the gap.

## 4. Material You / dynamic color deep dive

### HCT (Hue, Chroma, Tone)

Material 3 introduced HCT to support its "tonal palette" guarantee: that any pair of tones at known distance produces predictable contrast. HCT is built on CAM16 (Color Appearance Model 2016) for hue and chroma, and CIELAB L\* for tone. The result, similar in spirit to OKLCH, is a perceptually uniform space tuned for Material's accessibility math.

Reference: [m3.material.io/styles/color/system/overview](https://m3.material.io/styles/color/system/overview).

### Tonal palette extraction

Material 3 derives a full color scheme from a single **source color** (typically extracted from the user's wallpaper, or set by the developer):

1. Map the source to the closest **key color** in HCT
2. From the key color, generate **five tonal palettes**: Primary, Secondary, Tertiary, Neutral, Neutral Variant
3. Each palette has 13 tones: `0, 10, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 95, 98, 99, 100`
4. Color **roles** (e.g., `primary`, `onPrimary`, `surfaceContainer`, `onSurface`) reference specific tones in light vs dark schemes

Material's contrast guarantees (in default light scheme):
- `primary` (Tone 40) on `onPrimary` (Tone 100) → ≥ 4.5:1
- `onSurface` (Tone 10) on `surface` (Tone 98) → ≥ 4.5:1
- `onSecondaryContainer` (Tone 10) on `secondaryContainer` (Tone 90) → ≥ 4.5:1

For an icon on a Material surface: read the role token (`onSurface` for default body icons, `onSurfaceVariant` for muted, `onPrimary` for icons inside a primary-filled button). Do not pick a tone manually — let the role do it.

### How an icon survives Material You tinting

The Material 3 dynamic-color system can recolor any role at runtime based on user wallpaper. **The icon must be a single-color silhouette** (Mode A from [`color-system.md`](color-system.md)) for this to succeed. Multi-color icons with baked tones cannot adapt; they appear unchanged regardless of user theme, looking off-brand in the user's chosen palette.

For Android themed launcher icons specifically, the `<monochrome>` layer in the adaptive-icon XML is required (per the spec linked in §5 of `color-system.md`). The system extracts a tint from wallpaper and applies it to the monochrome silhouette at render.

### Theme tinting vs baked color

| Approach | Pros | Cons |
|---|---|---|
| Tint at runtime (`?attr/colorOnSurface`) | Adapts to theme, dynamic color, accessibility | Requires monochrome silhouette |
| Bake colors into the asset | Pixel-exact across surfaces | Breaks Material You, breaks dark mode auto-adapt |

Default to runtime tint for everything except documented multi-color brand marks (launchers, app-store icons).

## 5. iOS color system deep dive

### Display P3 vs sRGB

Apple recommends **Display P3** as the working color space for new iOS work since 2016 (introduction of P3 displays on iPhone 7). The expanded gamut covers about 50% more chromatic volume than sRGB, particularly in saturated reds and greens.

Practical rule for icon work: **author in sRGB unless the brand color is explicitly outside it.** Most brand palettes (especially blues, neutrals, conventional reds) are sRGB-safe. Only when a brand commits to neon, electric, or saturated wide-gamut hues do you need P3 — at which point the asset catalog accepts a P3 PDF or PNG and iOS will downconvert on non-P3 displays.

Verify with `xcrun icc-info` or by inspecting the embedded ICC profile in the exported asset.

### Dynamic Color (semantic tokens)

Use semantic tokens, not literal colors, in code and asset catalogs:

| Token | Purpose | Behavior |
|---|---|---|
| `UIColor.label` | Primary text and icons | Adapts light/dark + increase-contrast |
| `UIColor.secondaryLabel` | Secondary text/icons (muted) | Same |
| `UIColor.tertiaryLabel` | Tertiary | Same |
| `UIColor.systemFill` | Background fill | Same |
| `UIColor.tintColor` | App tint | Inherits from app or window |
| `UIColor.systemBlue` (etc.) | Branded system colors | Adapt for light/dark |

Asset catalog: add a custom color set with light/dark/increase-contrast appearances. Code: reference the named asset, not a hex literal.

### Tab Bar tint behavior

iOS Tab Bar uses Template Images and the bar's `tintColor`:
- Selected items render in `tintColor`
- Unselected items render in `unselectedItemTintColor` (default: a system gray)
- Light/dark mode swap automatically when colors are semantic
- The image must be marked as a Template Image in the asset catalog (`Render As: Template Image`); otherwise it bakes its own color and ignores tinting

If the icon ships colored when expected to be tinted, the failure is almost always: forgot to set Render As, or used a literal `UIColor` hex instead of a semantic token.

### Liquid Glass material

Liquid Glass (the iOS 18-26 era translucent material) varies its backdrop based on what's behind. Apple HIG's contrast guarantee for icons on Liquid Glass: glyphs must remain ≥ 3:1 against the *worst-case* visible backdrop, not the nominal frosted color. In practice this means designing for the darkest content the bar can sit over (a dark image scrolled underneath) and the lightest (a white background with no content).

Apple's own SF Symbols on Liquid Glass run hierarchical mode by default, which uses opacity tiers (1.0, 0.55, 0.35) to ensure the glyph's primary stroke retains contrast even when secondary strokes drop into the translucent middle.

### SF Symbols rendering modes

| Mode | What it does | When for custom symbols |
|---|---|---|
| **Monochrome** | Single tint applied to entire glyph | Default for UI; mirrors Mode A |
| **Hierarchical** | Single hue, three opacity tiers (1.0 / 0.55 / 0.35) | When the symbol has primary/secondary/tertiary structural layers |
| **Palette** | Multiple custom colors per layer | When duotone is required (Mode B) and the symbol has named layers |
| **Multicolor** | Fixed semantic colors baked into symbol | Status, brand marks; rare in UI navigation |

Custom SF Symbols (.svg with the SF Symbols template structure) declare named layers; the rendering mode then chooses how to color them at runtime. This is the iOS equivalent of Material's `<monochrome>` separation.

## 6. Web platform color

### CSS Color 4

Browser-supported as of 2023+: `oklch()`, `oklab()`, `color(display-p3 R G B)`, `color(rec2020 R G B)`, and the `color-mix()` function for runtime interpolation in any color space.

Recommended SVG icon CSS:

```css
.icon { color: oklch(0.55 0.16 250); fill: currentColor; }
.icon[aria-current="page"] { color: oklch(0.45 0.18 250); }
@media (prefers-color-scheme: dark) {
  .icon { color: oklch(0.78 0.12 250); }
}
```

`fill: currentColor` is the canonical pattern for inline SVG icons: it inherits the cascading text color, making the icon a first-class citizen of the type system.

### prefers-color-scheme

Adapt icon tints (and rarely, the icon itself) to dark mode. Most icons should not change — the silhouette is theme-agnostic; only the tint changes via `currentColor`.

### forced-colors mode (Windows High Contrast)

When the user is in forced-colors mode, the browser substitutes user-defined system colors. SVG `currentColor` continues to work because it follows text color, which is mapped to `CanvasText`. **Baked fills are ignored** under forced-colors. Test with Edge DevTools → Rendering → Emulate CSS media feature `forced-colors: active`.

### color-scheme meta

Declare which schemes the page supports via `<meta name="color-scheme" content="light dark">` so the browser applies form-control and scrollbar tints correctly. Icons remain CSS-driven via `currentColor`.

## 7. Color in animation / state transitions

When the icon transitions selected → unselected, color fades over ~120-200ms. Two failure modes:

1. **sRGB interpolation muddiness** — interpolating from a saturated brand blue to a neutral gray in sRGB passes through a muddy desaturated midpoint
2. **Equal-step lightness mismatch** — a linear sRGB fade reads as a sudden snap because perceived lightness is non-linear

Fix: interpolate in OKLCH (perceptually uniform). Web: `transition: color 160ms; interpolate-color: oklch;` (CSS Color 5 / browser support varies — use `color-mix(in oklch, ...)` as the manual fallback).

For native: SwiftUI `Color` interpolation uses sRGB by default; use `Color.mix(_:by:in:)` with `.perceptual` (iOS 18+) when available.

### Reduced-motion considerations

Color transitions are not vestibular triggers; they are typically safe under `prefers-reduced-motion`. **However**: a color cross-fade longer than 200ms reads as motion. Cap at 200ms in standard mode; reduce to instant snap (no transition) under `prefers-reduced-motion: reduce` to err on the safe side. iOS exposes the equivalent via `UIAccessibility.isReduceMotionEnabled`.

## 8. Practical palette generation algorithm

Given: brand primary hex (e.g., `#0066CC`).

```
Step 1 — Convert
  oklchPrimary = sRGBtoOKLCH("#0066CC")
  // ≈ oklch(0.50 0.16 250)

Step 2 — Generate lightness stops
  stops = [0.97, 0.93, 0.87, 0.78, 0.66, 0.55, 0.46, 0.38, 0.30, 0.22, 0.15]
  for each stop L:
    chroma = scaleChromaForLightness(0.16, L)  // peak at L=0.55, taper to extremes
    palette[stop] = oklch(L, chroma, 250)

Step 3 — Verify contrast pairs
  for each adjacent (a, b) in stops:
    assert WCAGcontrast(palette[a], palette[b]) >= 1.5

Step 4 — Define semantic mappings (icon-specific)
  default = palette[700]          // light theme default tint
  hover   = palette[800]
  pressed = palette[600]
  disabled = withOpacity(palette[400], 0.4)
  accent  = palette[500]
  active  = palette[600]
  inactive = neutralPalette[500]

Step 5 — Test under simulated CVD
  for each profile in [protanopia, deuteranopia, tritanopia]:
    render set under profile
    assert state pairs distinguishable by shape AND luminance
    assert status icons distinguishable by shape AND luminance

Step 6 — Test under forced-colors / increase-contrast
  render with currentColor mapped to system token
  assert silhouette still reads (every icon survives single-color collapse)

Step 7 — Bake or runtime decision
  if iOS Tab Bar / Toolbar          → runtime (Template Image)
  if Android in-app                 → runtime (theme attr tint)
  if Web SVG                        → runtime (currentColor)
  if iOS launcher                   → bake
  if Android adaptive launcher      → bake bg/fg + add monochrome layer

Step 8 — Document
  emit color tokens to brand-dna.md
  emit per-icon role mapping to icon-system-rules.md
```

## 9. Color audit checklist

Before shipping a colored icon set, verify:

- [ ] Every icon SVG uses either `currentColor` or a documented brand token; no orphan hex literals
- [ ] If duotone, exactly two distinct fill values, with primary 60-80% of fill area across every icon
- [ ] Set-wide color count matches the declared mode (1 for A, 2 for B/C, 3-4 for D)
- [ ] Each icon hits ≥ 3:1 contrast on light surface (WCAG 1.4.11)
- [ ] Each icon hits ≥ 3:1 contrast on dark surface
- [ ] Each icon hits ≥ 3:1 against the worst-case translucent backdrop it can sit over
- [ ] Selected vs unselected differential ≥ 1.5:1
- [ ] State distinction is shape (filled vs outlined) plus color, never color alone
- [ ] Status icons differ in shape, not only hue
- [ ] Set passes deuteranopia simulation (Sim Daltonism / Color Oracle / iOS Color Filters)
- [ ] Set passes protanopia and tritanopia simulation (hi-end work)
- [ ] Forced-colors / increase-contrast: silhouette reads as single-color collapse
- [ ] iOS template images marked Render As: Template Image
- [ ] Android in-app icons reference theme attrs, not literal colors
- [ ] Android adaptive launcher includes `<monochrome>` layer for Material You
- [ ] Tonal scale stops verified at adjacent ≥ 1.5:1 contrast

Failure on any item blocks ship; document in `cross-icon-audit.md` with the proposed fix.

## 10. Common color failures with diagnostic recipes

### Failure A — Icon vanishes in dark mode
- **Symptom**: Icon visible on light background, invisible or near-invisible on dark
- **Diagnosis**: hex literal in asset catalog, or fill color too dark to read on dark surface
- **Fix**: replace literal with semantic token (`UIColor.label` or asset catalog with light/dark appearance pair); for SVG, switch to `currentColor`

### Failure B — Tab Bar icon ships colored, refuses to tint
- **Symptom**: Icon stays the same color in selected/unselected states; iOS Tab Bar tint setting has no effect
- **Diagnosis**: asset is not a Template Image
- **Fix**: in asset catalog, set Render As → Template Image; re-export from source as PDF with monochrome content

### Failure C — Material You theme breaks the icon
- **Symptom**: launcher icon doesn't pick up the user's wallpaper-derived tint
- **Diagnosis**: missing `<monochrome>` layer in adaptive-icon XML
- **Fix**: add `<monochrome android:drawable="@drawable/ic_launcher_foreground"/>` element; ensure foreground drawable is single-color compatible

### Failure D — Status icons indistinguishable to colorblind users
- **Symptom**: success and error icons both read as the same brown-ish dot under deuteranopia
- **Diagnosis**: relied on green/red hue distinction with similar lightness
- **Fix**: add shape distinction (check for success, X for error); shift error red toward orange (hue ~25° in OKLCH); raise lightness contrast between states

### Failure E — Muddy color transition between selected and unselected
- **Symptom**: 160ms color crossfade reads as a desaturated wash
- **Diagnosis**: sRGB interpolation passes through a low-chroma midpoint
- **Fix**: interpolate in OKLCH (`color-mix(in oklch, ...)`); shorten transition to ≤ 120ms; or simplify to opacity fade if hues are similar

### Failure F — Brand-tinted glyph fails contrast on translucent material
- **Symptom**: icon legible on solid Liquid Glass mock, illegible when scrolled over a busy image
- **Diagnosis**: tested only against nominal material color, not worst-case backdrop
- **Fix**: drop a vibrancy underlay (Apple's prescribed pattern), or shift the glyph to higher tonal stop; test against worst-case scroll position

### Failure G — Increase-contrast mode collapses duotone
- **Symptom**: under iOS Increase Contrast or Windows Forced Colors, the secondary color disappears
- **Diagnosis**: secondary color carried meaning that primary alone cannot convey
- **Fix**: redesign so primary silhouette carries meaning; secondary is decoration only (Mode A or C, not strict Mode B)

### Failure H — Tonal scale produces washed-out hover state
- **Symptom**: hover state nearly invisible on default state
- **Diagnosis**: lightness gap between adjacent stops < 1.5:1 contrast
- **Fix**: open the lightness gap (e.g., default at L=0.55, hover at L=0.42 instead of L=0.50); re-verify

### Failure I — Display P3 colors clip on sRGB displays
- **Symptom**: brand neon-green renders as flat dull green on older devices
- **Diagnosis**: P3 source has no explicit sRGB fallback
- **Fix**: provide both P3 and sRGB asset variants; let asset catalog or `<picture>` element negotiate; or pull the brand color back into sRGB if the gamut excursion isn't critical

### Failure J — Every icon a different brand-accent color
- **Symptom**: set looks like a bag of skittles, no visual hierarchy
- **Diagnosis**: violates Mode discipline; treats accent as decoration not signal
- **Fix**: collapse to Mode A (monochrome) or Mode C (one documented accent on documented icons); strip per-icon color overrides

## Sources

- [W3C CSS Color 4](https://www.w3.org/TR/css-color-4/) — `oklch()` §9.4, `color()` §10.1, Display P3 §10.4
- [W3C CSS Color 5](https://www.w3.org/TR/css-color-5/) — `color-mix()`, interpolation in named color spaces
- [W3C WCAG 2.2 §1.4.11 Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) — 3:1 graphical-object floor
- [Björn Ottosson — A perceptual color space for image processing (Oklab)](https://bottosson.github.io/posts/oklab/) — origin of OKLab/OKLCH, 2020
- [Björn Ottosson — How software gets color wrong](https://bottosson.github.io/posts/colorwrong/) — sibling post on interpolation failures
- [Tailwind CSS — Colors](https://tailwindcss.com/docs/colors) — production reference for OKLCH-based 50-950 tonal scale
- [Material Design 3 — Color system overview](https://m3.material.io/styles/color/system/overview) — HCT, source colors, key colors
- [Material Design 3 — Roles](https://m3.material.io/styles/color/roles) — `onSurface`, `primary`, `onPrimary`, container roles
- [Material Design 3 — Static color schemes](https://m3.material.io/styles/color/static) — scheme generation from a single source color
- [Apple Human Interface Guidelines — Color](https://developer.apple.com/design/human-interface-guidelines/color) — semantic colors, dynamic color, P3 vs sRGB
- [Apple HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials) — translucent material contrast guarantees
- [Apple HIG — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) — monochrome / hierarchical / palette / multicolor rendering modes
- [Apple Developer — Wide Color](https://developer.apple.com/documentation/uikit/uicolor/managing_color_compatibility) — Display P3 authoring guidance
- [Android — Adaptive icons](https://developer.android.com/develop/ui/views/launch/icon_design_adaptive) — `<monochrome>` layer, Material You theming, Android 13+ requirements
- [Android — Vector drawables](https://developer.android.com/develop/ui/views/graphics/vector-drawable-resources) — `android:tint`, theme attrs
- [Google Material — HCT color space documentation](https://material.io/blog/science-of-color-design) — CAM16 + L\* basis for HCT
- Wathan, Adam & Steve Schoger. *Refactoring UI*, self-published, 2018, ch. "Color" — "you need more colors than you think," "ditch hex for HSL," palette discipline. [refactoringui.com](https://www.refactoringui.com)
- Vignelli, Massimo. *The Vignelli Canon*, Lars Müller Publishers, 2010, p. 28 ("Semantics") — meaning before expression
- Cheng, Karen. *Designing Type*, Yale University Press, 2005, ch. 3 — optical adjustment, perceptual lightness
- Lupton, Ellen. *Thinking with Type*, 2nd ed., Princeton Architectural Press, 2010 — color in editorial systems
- [CIE — CAM16 Color Appearance Model](https://cie.co.at/publications/colorimetry-cie-system-and-its-application) — basis for HCT (paywalled standard; secondary references in Material docs)
- [Sim Daltonism (Michel Fortin)](https://michelf.ca/projects/sim-daltonism/) — macOS CVD simulator
- [Color Oracle](https://colororacle.org/) — cross-platform CVD simulator
- [Stark](https://www.getstark.co/) — Figma/Sketch/Chrome plugin, contrast + CVD
- [Adobe Color — Accessibility Tools](https://color.adobe.com/create/color-accessibility) — palette CVD verification
- See also: [`color-system.md`](color-system.md), [`accessibility.md`](accessibility.md), [`aesthetic-principles.md`](aesthetic-principles.md), [`craft-rubric.md`](craft-rubric.md), [`sources.md`](sources.md)

When any of these specs feel out of date, run [`live-research.md`](live-research.md) before treating values here as current.
