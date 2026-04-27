# Color System Guide (Long-form)

Long-form rationale for color decisions in icon sets. Use the runtime checklist in [`color-system.md`](color-system.md). This file explains why the rules exist and how to reason about edge cases.

## Why Monochrome Is the Default

UI icon sets are workhorses, not headline graphics. They live alongside text, get tinted by platforms, and adapt to themes. Monochrome icons have three structural advantages:

1. **Theme-respecting** — light/dark mode, custom themes, dynamic color all work without per-icon assets
2. **Accessibility-respecting** — high-contrast modes invert correctly
3. **Cross-platform consistent** — one master file, multiple platform exports without color duplication

Multi-color icons sacrifice these advantages for marginal aesthetic gain. Reserve color for app launcher / logo work where multi-color identity is justified.

## When Color Belongs in Icons

Three specific cases:

### 1. Brand-required duotone

Some brands have a two-color identity that breaks under monochrome tinting. Example: a brand whose logo is half-blue / half-orange where the color split is structural, not decorative.

In these cases, icons inherit the duotone — but be deliberate. Run the single-tint test: does the icon's meaning survive when reduced to one color? If yes, monochrome with single-tint is the better default.

### 2. Information-bearing color

Some icons carry information through color:
- Status icons (red = error, yellow = warning, green = success)
- Severity indicators (color-coded priority)

These are not pure UI navigation icons. They sit in a category-specific gap between icon and indicator. Color is part of the meaning.

### 3. Hi-end / premium positioning

Premium apps sometimes use restrained duotone for elevation. The convention: a single brand accent color used sparingly, against a primary monochrome.

Restraint is the rule. One accent in 1-2 specific icons (e.g., the active Tab Bar state) is enough. Splash color across the whole set and it loses elevation.

## Color Roles in Detail

When duotone is used, every icon must use the same color roles. The roles are:

### Primary

- 60-80% of the icon's visible mass
- Drives brand recognition
- Should survive tinting (the icon's meaning lives in the primary)

### Secondary

- 20-40% of the icon's visible mass
- Adds emphasis, accent, or detail
- Doesn't carry meaning alone

### Reserved (optional)

Some brands reserve colors for error / warning / success states. Document those colors as not-for-icon-use.

## Tinting Behavior

### iOS template images

iOS tints template images automatically based on:
- Tab Bar tint color (system or app-set)
- Selected vs unselected state
- Light vs dark mode

Construction implication: the SVG / PDF master uses any solid color (convention: `#000`), exported as a template asset. iOS handles the rest.

Common mistake: exporting as a "regular" image with baked color. The asset catalog has a "Render As" setting — must be "Template Image" for tinting to work.

### Android vector drawables

Android uses `android:tint` and theme attributes:

- `android:tint="?attr/colorOnSurface"` — tints to current theme's on-surface color
- `app:tint="..."` — programmatic tint

For Bottom Nav, Material 3 uses:
- Active: `?attr/colorOnSecondaryContainer` (typically tinted with theme accent)
- Inactive: `?attr/colorOnSurfaceVariant` (typically muted)

### Themed icons (Material You / Android 13+)

Single-color silhouette icons that respect user's dynamic color choice. For in-app icons (not launcher), this means the icon is rendered as a single color computed from the user's wallpaper.

## Contrast Math

WCAG 2.2 contrast requirements for icons:

- **Graphical objects** (icons, UI controls): 3:1 against adjacent color
- **Large text** (18pt+ or 14pt+ bold): 3:1
- **Normal text**: 4.5:1

Icons are graphical objects → 3:1 minimum.

For state pairs, the difference between active and inactive should also support recognition:
- Same icon at 3:1 contrast vs 1.5:1 — second one might fail readability even if both meet absolute contrast against background

Tools:
- Browser DevTools accessibility panel
- Stark plugin (Figma)
- WebAIM contrast checker
- Apple's color accessibility tools

## Color Vision Deficiency (CVD)

Roughly 8% of men and 0.5% of women have CVD. The three main types:

- **Protanopia** — red-blind
- **Deuteranopia** — green-blind (most common)
- **Tritanopia** — blue-blind (rare)

For duotone icons, simulate under each:
- Stark plugin (Figma)
- Sim Daltonism (macOS)
- Color Oracle (cross-platform)

Rule: the icon should remain meaningful under each simulation. If the duotone collapses (e.g., red and green become indistinguishable under deuteranopia), redesign or fall back to monochrome.

## Theme Variants

For apps with multiple themes (light, dark, high-contrast, custom), validate icons under each:

- Light theme — default contrast
- Dark theme — inverted; thin strokes can disappear if not designed for inversion
- High-contrast — system accessibility setting; icons should respect
- Custom theme — if app offers theme customization, test edge cases

The simpler the icon's color logic, the easier it is to validate across themes. Single-tint monochrome is the simplest; survives all theme variants by definition.

## State Color

For Tab Bar / Bottom Nav state pairs, color is reinforcing — not primary signal.

The primary signal is silhouette change:
- Active: filled
- Inactive: outlined

Color reinforces:
- Active: full-strength tint
- Inactive: muted tint

If a user puts the device in grayscale mode (accessibility setting), the icons should still reveal state through silhouette change. This means filled/outlined difference must be visually distinct, not subtle.

## When User Asks for "More Color"

Common request: "the icons feel boring in monochrome, can we add color?"

Reframe the conversation:

1. Is the user asking for brand color (one accent, used sparingly)? → introduce documented duotone
2. Is the user asking for multi-color (each icon different)? → that's not UI icons, that's illustration; suggest using the launcher icon for multi-color expression instead
3. Is the user trying to compensate for weak silhouettes with color? → fix the silhouettes; color won't save them

## Failure Modes

- **Multi-color UI icons by default** — confetti at 24px, tint-incompatible
- **Baked color in iOS template images** — silent failure, breaks tinting
- **Hue-only differentiation** — fails CVD and grayscale modes
- **Color used to rescue weak silhouettes** — strip color, fix the underlying icon
- **State distinction by color alone** — fails accessibility settings
- **Duotone without single-tint fallback** — fragile; theme variations expose holes
