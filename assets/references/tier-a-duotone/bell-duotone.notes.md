# bell-duotone

**Tier:** A
**Source:** Phosphor duotone (`bell-duotone.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/phosphor-icons/core/main/raw/duotone/bell-duotone.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<path>` mass layer with opacity-modulated fill + `<path>` outline)
- Total anchor points: ~12 path-command anchors total
- Stroke width: 16 units at 256-canvas on the outline; mass uses fill
- Coordinate system: viewBox 0 0 256 256

## Why this tier
Duotone exemplar for the bell metaphor. Both layers respond to `currentColor`: the mass layer uses `fill="currentColor"` with `opacity="0.2"` (a dimmer secondary tone) and the outline uses `stroke="currentColor"`. The duotone family's calibration discipline is to keep both layers tied to a single colour value so state, theming, and accessibility (Forced Colors, dark mode) all flow through `currentColor` without breaking the silhouette.

## What a generator should learn
Duotone = mass layer + outline layer where BOTH bind to `currentColor`; state/theming changes a single value and the icon adapts as a unit.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Notifications / Inbox (duotone variant)
- Aesthetic principles applied: 5 (system over single — duotone family has shared rule), 6 (color compensating fail — opacity is a SHAPE-level affordance, not color-only)
