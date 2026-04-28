# mic

**Tier:** A
**Source:** Lucide outline (`mic.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/mic.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 3 (`<rect>` capsule + `<path>` cradle + `<path>` post)
- Total anchor points: ~6 path-command anchors plus 4 implicit on rect
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
`<rect width="6" height="13" x="9" y="2" rx="3"/>` capsule + arc `M19 10v2a7 7 0 0 1-14 0v-2` (cradle) + `M12 19v3` (post). Capsule corner radius 3 = capsule width / 2 (perfect rounded-end pill). Cradle terminates exactly at y=12 (canvas center).

## What a generator should learn
Mic = capsule + cradle + post; capsule sits half above/below center.

## Cross-reference
- icon-vocabulary.md section: Media → Microphone / Voice
- Aesthetic principles applied: 1 (restraint — 3 elements), 7 (construction visible — pill = width/2 radius, cradle hinge at y=12)
