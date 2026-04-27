# Platform Icon Specs

Authoritative specs for iOS Tab Bar, Android Bottom Navigation, and adjacent platform surfaces. Always cross-check live sources via [`live-research.md`](live-research.md) before treating any value here as current — Apple HIG and Material 3 update without notice.

## iOS Tab Bar

### Sizes

- **Tab Bar icon canonical size**: 25×25pt (template image)
- **Visible mass typically**: ~20×20pt within the 25pt frame (5pt visual padding)
- **Provided assets**: 1x (25pt), 2x (50px), 3x (75px) — modern iOS uses PDF templates that scale automatically

### Style

- **Style**: outlined (unselected) and filled (selected) variants required
- **Color**: monochrome — system tints based on Tab Bar appearance and selected state
- **Output format**: PDF template image (preferred) or PNG @1x/2x/3x

### Behavior

- iOS automatically applies tint color to template images — never bake color into the asset
- Selected state uses tinted filled variant; unselected uses tinted outlined variant
- Both states must read clearly with the same tint color (don't rely on color difference)

### Construction Recommendations

- 24pt grid is acceptable for source SVG masters; export at 25pt scaled
- Stroke weight: 1.5pt for outlined variant works at 25pt scale
- Filled variant: solid fill, same silhouette as outlined contour
- Padding: keep visible mass within 20pt to avoid edge-clipping at 25pt frame

### Reference

- Apple Human Interface Guidelines → Tab Bars
- SF Symbols spec for size guidance (matches Tab Bar conventions)

## Android Bottom Navigation (Material 3)

### Sizes

- **Bottom Navigation icon canonical size**: 24×24dp
- **Touch target**: minimum 48×48dp (icon + padding)
- **Provided assets**: vector drawable XML or SVG converted to vector drawable

### Style

- **Style**: filled (active) and outlined (inactive) variants required for Material 3
- **Color**: tinted via Material color scheme (typically `onSurfaceVariant` for inactive, `onSecondaryContainer` for active)
- **Output format**: vector drawable XML (preferred) or SVG

### Behavior

- Active tab can use a pill-shape background indicator (Material 3 default)
- Inactive icons use outlined variant; active uses filled
- Color tinting applied by the system at runtime via theme

### Construction Recommendations

- 24×24dp grid native
- Stroke weight: 1.75dp standard, 2dp for emphasis
- Filled variant: solid fill matching outlined silhouette
- Optical sizing: align with Material Symbols cadence to feel native if used alongside

### Themed Icons (Android 13+)

- Single-color silhouette layer for Material You themed icon support (relevant for app launcher; less so for in-app Tab Bar but Material 3 Bottom Nav can leverage same monochrome)
- Use `android:tint` properly to take full advantage of dynamic theming

### Reference

- Material Design 3 → Components → Navigation Bar
- Material Symbols spec for size guidance

## Cross-Platform Notes

When shipping the same set on iOS + Android:

- 24×24 master SVG works for both
- Export iOS at 25pt scaled, Android at 24dp native
- Keep filled and outlined variants in sync across platforms
- Color: never bake; let each platform tint

## Action Icon Sizes

Action icons (toolbar, button, inline) typically use:

- **iOS**: 22-28pt depending on context (large action button vs inline)
- **Android**: 24dp standard, 20dp for dense layouts

## Notification / Inline Icon Sizes

For very small contexts:

- **iOS notification bar**: 12-16pt
- **Android notification bar**: 24dp source, system renders at 18dp
- **Inline list affordance**: 16-20pt typical

These almost always need a separate, simplified icon — do not just scale the 24×24 master to 16. See [`icon-grid-construction.md`](icon-grid-construction.md) for 16×16 construction.

## Common Mistakes

- **Baking color into iOS template images** — breaks system tinting
- **Using PNG for Android Bottom Nav** — vector drawable is the standard
- **Using a single icon for selected and unselected** — Material 3 expects state pair
- **Ignoring touch target padding on Android** — 48×48dp minimum
- **Designing Tab Bar at 24pt then exporting at 24** — should export at 25pt for iOS

## Live Research Reminders

Always verify these specifics against current documentation when starting a new project:

- iOS Tab Bar size (Apple has shifted from 30pt to 25pt over iOS versions)
- Material 3 active state indicator (pill background was added relatively recently)
- Themed icon support level on target Android versions
- New iOS-specific behaviors (Liquid Glass, dynamic icon variants, etc.)

See [`live-research.md`](live-research.md) for the watchlist and refresh cadence.
