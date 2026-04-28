# image

**Tier:** A
**Source:** Lucide outline (`image.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/image.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 3 (`<rect>` frame + `<circle>` sun + `<path>` mountain)
- Total anchor points: ~6 path-command anchors plus 8 implicit on rect/circle
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
`<rect>` frame + `<circle cx="9" cy="9" r="2"/>` sun + path `m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21` mountain peak. Mountain peak is single rounded apex (~17.5, 12.5) from two arcs radius 2 mirrored around peak.

## What a generator should learn
Image = frame + sun + mountain peak (3 primitives, no realistic terrain).

## Cross-reference
- icon-vocabulary.md section: Media → Image / Photo
- Aesthetic principles applied: 1 (restraint — 3 primitives, no terrain), 7 (construction visible — mirrored 2pt arcs at apex)
