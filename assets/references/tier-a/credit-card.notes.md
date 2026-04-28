# credit-card

**Tier:** A
**Source:** Lucide outline (`credit-card.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/credit-card.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<rect>` body + `<line>` magnetic-stripe)
- Total anchor points: 2 implicit on the line plus 4 implicit on the rect
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
`<rect width="20" height="14" x="2" y="5" rx="2"/>` + `<line x1="2" x2="22" y1="10" y2="10"/>`. Two primitives total. Card aspect ratio 20:14 close to real credit card 1.586:1. Magnetic-stripe line at y=10 sits 5pt from top, 9pt from bottom (upper third where real mag-stripe lives). **No chip square** — stripe alone is sufficient.

## What a generator should learn
Card = rect + horizontal stripe in upper third; avoid chip detail (couples to brand).

## Cross-reference
- icon-vocabulary.md section: Money / Payment → Credit Card
- Aesthetic principles applied: 1 (restraint — no chip), 7 (construction visible — aspect ratio close to real card), 9 (metaphor before ornament)
