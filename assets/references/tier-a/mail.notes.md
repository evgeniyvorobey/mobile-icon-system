# mail

**Tier:** A
**Source:** Lucide outline (`mail.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/mail.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<rect>` envelope + `<path>` flap)
- Total anchor points: ~6 path-command anchors plus 4 implicit on rect
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
`<rect>` + flap `m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7`. Flap apex at (12, 12.36) — just below canvas center. Slight downward bias creates optical "envelope flap is open" reading even with no perspective shading. Aspect ratio 20:16 = 5:4 (like real letter envelope).

## What a generator should learn
Envelope flap apex sits ~0.36pt below canvas center for optical "open" reading.

## Cross-reference
- icon-vocabulary.md section: Communication → Email / Mail
- Aesthetic principles applied: 3 (intentional asymmetry — flap below center), 4 (weight perception — optical "open")
