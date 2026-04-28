# lock

**Tier:** A
**Source:** Lucide outline (`lock.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/lock.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<rect>` body + `<path>` shackle)
- Total anchor points: ~6 path-command anchors plus 4 implicit on the rect
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Body `<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>` + shackle `<path d="M7 11V7a5 5 0 0 1 10 0v4"/>`. Two primitives, no keyhole. Shackle width 10 = body width 18−8 (centered, 4pt padding each side). Shackle radius 5 = body height ÷ 2.

## What a generator should learn
Padlock = rectangle + arched shackle, NO keyhole detail (collapses at 16pt).

## Cross-reference
- icon-vocabulary.md section: Security → Lock / Unlock
- Aesthetic principles applied: 1 (restraint — no keyhole), 7 (construction visible — shackle radius derives from body)
