# camera-decorative (tier-B)

**Tier:** B
**Source:** Heroicons 24/outline (`camera.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/outline/camera.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<path>` x2 — body + lens, plus a decorative micro-element)
- Total anchor points: ~24 path-command anchors (notable for the icon class)
- Stroke width: 1.5 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Includes a decorative `M18.75 10.5h.008v.008h-.008V10.5Z` — that's a tiny 0.008-unit "viewfinder light" indicator. At 16pt it disappears; at 24pt it's noise.

## What's missing vs tier-A
Anchor economy. Decorative microelements are amateur hour.

## What a generator should learn
Sub-pixel decorative dots and indicators do not carry meaning at deployment sizes. Either make the element large enough to read or delete it.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Camera / Capture
- Aesthetic principles applied (and where this falls short): 1 (restraint — micro-element violates), 5 (one-ornament rule — the dot adds a decoration that does not signify)
