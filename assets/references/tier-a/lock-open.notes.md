# lock-open

**Tier:** A
**Source:** Lucide outline (`lock-open.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/lock-open.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<rect>` body + `<path>` shackle, body byte-identical to `lock.svg`)
- Total anchor points: ~6 path-command anchors plus 4 implicit on the rect
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Body identical to lock. Shackle `M7 11V7a5 5 0 0 1 9.9-1` — shackle now ends at `9.9 -1` (top-right open arc) instead of returning to `17 11`. **The state difference is exactly one path command.** Body geometry byte-identical between two states. Canonical demonstration that selected/unselected pairs share base geometry, differ only at the affordance point.

## What a generator should learn
State pair = identical base geometry + minimal change at the single affordance point.

## Cross-reference
- icon-vocabulary.md section: Security → Lock / Unlock (state pair)
- Aesthetic principles applied: 3 (intentional asymmetry — only the open end), 7 (construction visible — shared base)
