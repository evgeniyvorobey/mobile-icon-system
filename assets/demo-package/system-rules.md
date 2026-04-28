# Icon System Rules - Tidepool Tasks

Generated: 2026-04-28
Skill version: mobile-icon-system v0.6.0
Design tool: filesystem-only
Motion scope: none

## Grid

- Base: 24 by 24.
- Live area: 20 by 20 with 2pt optical padding.
- Pixel grid: 0.5pt increments preferred; whole-point anchors for simple rectilinear forms.
- Baseline: tab icons visually center around y=12, with check marks allowed to lift 0.25pt.

## Stroke

- Weight: 1.75pt for outlined masters.
- Cap: round.
- Join: round.
- Filled state: solid silhouette with punched or drawn detail only when it remains readable at 20pt.

## Terminals And Corners

- Terminal style: round.
- Outer radius: 2.5pt for cards and panels.
- Dot radius: 0.75pt to 1pt, aligned to the same horizontal rhythm.

## Style

- Visual style: monochrome rounded-outline with filled active states for Tab Bar and Bottom Nav.
- Tab state rule: filled icons are active; outlined icons are inactive.
- Action icons ship as single outlined masters unless a pressed state needs a separate asset.

## Color

- SVG masters use `currentColor`.
- iOS: export as template images and tint from Tab Bar or button state.
- Android: convert to vector drawable and tint with theme attributes.
- No baked brand color in source masters.

## Naming

- Convention: `ic_{scope}_{name}_{state}.svg` for stateful tab icons.
- Single-state action icons use `ic_{scope}_{name}.svg`.
- Lowercase snake_case only.

## Accessibility Rules

- Non-text contrast target: 3:1 minimum against adjacent surfaces.
- Touch target: 44pt iOS, 48dp Android.
- Screen-reader labels live in product code, not inside SVG files.
- State distinction must remain visible in one color: active states use filled mass, inactive states use outline mass.
