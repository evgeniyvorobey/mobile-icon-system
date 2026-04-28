# clock

**Tier:** A
**Source:** Lucide outline (`clock.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/clock.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<circle>` body + `<path>` hands)
- Total anchor points: ~5 path-command anchors plus 4 implicit on the circle
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
`<circle cx="12" cy="12" r="10"/>` + hands `M12 6v6l4 2`. **Hour hand `M12 6v6` is 6pt long** going straight up from center for 6 units (hours hand short, "12 o'clock"). Then `l4 2` minute hand. **Clock reads ~10:10** — hands form smile-shape (V-up symmetry), industry-tradition "happy clock" time.

## What a generator should learn
Clock = circle + hands at 10:10 (industry convention, not 3:00).

## Cross-reference
- icon-vocabulary.md section: Time & Schedule → Clock / Time
- Aesthetic principles applied: 3 (intentional asymmetry — hand asymmetry), 7 (construction visible — 10:10 convention auditable)
