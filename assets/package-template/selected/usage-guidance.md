# Usage Guidance — {{PROJECT_NAME}}

Project: {{PROJECT_NAME}}
Owner: {{OWNER}}
Date: {{DATE}}
Skill version: {{SKILL_VERSION}}

How to use these icons in production. Engineering and design teammates refer to this when placing icons in product surfaces.

## Surface Map

Which icons go where:

| Surface | Icons | Size | State |
|---|---|---|---|
| iOS Tab Bar | <!-- list --> | 25pt | filled (selected) + outlined (unselected) |
| Android Bottom Nav | <!-- list --> | 24dp | filled (active) + outlined (inactive) |
| iOS toolbar | <!-- list --> | 22-28pt | single state |
| Android toolbar | <!-- list --> | 24dp | single state |
| Inline / list | <!-- list --> | 16-20pt | single state |
| Notification | <!-- list --> | 16pt | small-size variant if available |

## State Behavior

### Tab Bar / Bottom Nav

- **Selected / active**: filled variant, full-strength tint
- **Unselected / inactive**: outlined variant, muted tint
- **Disabled (if needed)**: outlined variant, further muted tint
- **Pressed / hover**: system-default ripple / highlight; do not change icon

### Action Icons

- **Default**: full-strength tint
- **Disabled**: muted tint
- **Loading state**: replace icon with spinner in place

## Tinting

### iOS

- All Tab Bar icons are template images (Render As: Template Image in xcassets)
- Tint applied via Tab Bar `tintColor` and `unselectedItemTintColor`
- Do NOT bake color into source SVG / PDF

### Android

- All Bottom Nav icons are vector drawables with `android:tint`
- Active: `?attr/colorOnSecondaryContainer` (Material 3 default)
- Inactive: `?attr/colorOnSurfaceVariant`
- For custom themes, override these attributes

### Themed (Material You) — Android 13+

- Set `android:tint` properly to inherit dynamic color
- Verify under multiple wallpaper-derived palettes

## Touch Targets

- Minimum: 44pt (iOS) / 48dp (Android)
- For icons smaller than the target, add invisible touch padding

## When to Use Which Variant

- **Filled** — selected/active state, primary CTAs, status indicators where mass conveys meaning
- **Outlined** — unselected/inactive state, secondary actions, dense interfaces

## Cross-Platform Sharing

- Single SVG master at 24×24 lives in `exports/svg-masters/`
- Platform-specific exports derived; do not edit the platform-specific files directly
- If the master changes, regenerate platform exports

## Adding New Icons

When the product needs a new icon not in the current set:

1. Read [`reviews/icon-system-rules.md`](../reviews/icon-system-rules.md) for the locked rules
2. Use the same construction grid, stroke, terminals, corners
3. Run cross-icon consistency check vs the existing set
4. Document the addition in the package

## Fallback Behavior

If a platform / device does not support the preferred export format:

- iOS pre-templates: ship 1x/2x/3x PNG fallbacks alongside PDF
- Android pre-vector-drawable (rare): ship density-specific PNG
- Web / hybrid: SVG with `currentColor` for tinting via CSS

## Changelog Awareness

Each change to the icon set should:

1. Bump the icon system minor version
2. Document the change in `CHANGELOG.md` (set-level)
3. Re-run cross-icon consistency audit after batched changes
