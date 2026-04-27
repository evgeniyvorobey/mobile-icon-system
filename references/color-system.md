# Color System

Color application rules across the icon set. Used in workflow phase 9 (hi-end craft pass). Most UI icon sets are monochrome and tinted by the platform — this file covers both the monochrome case and the duotone / multi-color exception cases. Long-form rationale in [`color-system-guide.md`](color-system-guide.md).

## Default — Monochrome, Platform-Tinted

The default for UI icon sets:

- Icons are single-color silhouettes (no baked color)
- Platform applies tint at runtime (iOS template image, Android `android:tint`)
- One icon, multiple tints across themes

Why: tinting respects user's theme, accessibility settings, and brand color choices. Baked color fights all of these.

### Construction for monochrome

- SVG fill / stroke can be any color in the master file (`#000` is conventional)
- Export as iOS PDF template image or Android vector drawable with `android:tint="?attr/colorOnSurface"`
- Verify: opening the file in iOS asset catalog tints correctly, Android theme inversion works

## Exception — Duotone

Some brands need two colors per icon. Common patterns:

- Outline + accent fill (e.g., dark outline + colored interior)
- Two-shade silhouette (e.g., body in primary, accent detail in secondary)

When duotone is justified:

- Brand DNA documents two-color identity
- Single-tint icons would lose brand recognition
- Both colors are part of the brand's named palette

When duotone is NOT justified:

- "It looks more interesting in two colors" — design preference, not brand requirement
- Adding accent color to make a generic icon feel custom — dishonest, doesn't fix the underlying weakness

### Color roles in duotone

- **Primary** — dominant color, drives brand recognition
- **Secondary** — supporting color, used for accent or detail
- **Reserved** — never used in icons (e.g., reserved for error states)

Document the role assignment in `brand-dna.md` if duotone is used.

### Area ratio

In duotone, primary should occupy 60-80% of the icon's visible mass. Secondary occupies 20-40%. Outside this range, the secondary becomes either decoration (under 20%) or co-equal (over 40%) — neither is on-brief.

## Multi-color — Avoid for UI Icons

Multi-color (3+ colors) is appropriate for:

- App launcher / home screen marks (different construction rules — out of scope for this skill)
- Illustration
- Editorial graphics

Not appropriate for UI icons because:

- Multi-color in a 24px icon becomes confetti
- Theme tinting fights multi-color (tint applies uniformly)
- Cross-cultural readability degrades
- Accessibility (CVD) hardest to verify at small size

If user requests multi-color UI icons, ask: is this for the launcher icon (different skill) or actually for in-app UI?

## Color Application Rules

### Rule 1 — Same role across the set

If duotone is used, every icon uses the same color roles. Don't have one icon with primary-red-accent and another with primary-blue-accent.

### Rule 2 — Tint compatibility

Even duotone icons should survive tinting:

- Test the icon under a single brand tint
- If it loses meaning under single tint, the duotone is fragile
- Keep duotone optional (provide a single-tint fallback)

### Rule 3 — Contrast against backgrounds

Icons must meet WCAG 2.2 contrast minimums against their backgrounds:

- AA: 3:1 for graphical objects (icons)
- AAA: 4.5:1 for stronger compliance

Test against:
- Light theme background
- Dark theme background
- Tinted backgrounds (Material You, theme variants)

### Rule 4 — CVD (Color Vision Deficiency)

If duotone:

- Test under protanopia, deuteranopia, tritanopia simulators
- The icon must remain meaningful under each
- Don't rely on hue-only differences (e.g., red + green); use luminance contrast too

## State Color (Tab Bar / Bottom Nav)

For state pairs:

- Active state: full-strength tint (e.g., brand primary)
- Inactive state: muted tint (e.g., 60% opacity primary, or `onSurfaceVariant`)
- Difference must be readable, not just nominal

Don't rely on color alone for state distinction — silhouette change (filled vs outlined) is the primary signal, color is reinforcing.

## Accessibility Defaults

- Minimum touch target: 44pt (iOS) / 48dp (Android) — applies to interactive icons
- Minimum contrast: 3:1 against background
- CVD-safe: documented under all three simulator types
- Theme-respecting: never bake; let the platform tint

## Color Output Format

In the package, document color application:

```markdown
## Color System — Tab Bar

### Default tinting (light theme)
- Active: `#0066CC` (brand primary)
- Inactive: `#666666` (system text muted)

### Default tinting (dark theme)
- Active: `#3399FF` (brand primary on dark)
- Inactive: `#999999` (system text muted on dark)

### Themed (Material You) behavior
- Active: `?attr/colorOnSecondaryContainer`
- Inactive: `?attr/colorOnSurfaceVariant`

### Duotone (if used)
- Primary: `#0066CC` (60-80% of icon mass)
- Secondary: `#FFAA00` (20-40% of icon mass)
- Fallback (single-tint): icon remains meaningful under primary alone

### Accessibility
- Contrast verified: ✓ 4.5:1 active / 3.5:1 inactive against light bg
- CVD-safe: ✓ verified under three simulators
```

## Failure Modes

- **Baking color into iOS template images** — breaks system tinting, fails on dark mode
- **Multi-color UI icons** — confetti at 24px, tint-incompatible
- **Color rescuing weak silhouette** — strip color and check; if icon falls apart, fix the silhouette
- **Hue-only state distinction** — fails CVD and dark mode
- **Skipping CVD check on duotone** — silent inaccessibility
- **Different color roles per icon** — set-level inconsistency
