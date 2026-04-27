# calendar-overdetailed (tier-C)

**Tier:** C (anti-example)
**Source:** Phosphor regular (`calendar.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/phosphor-icons/core/main/raw/regular/calendar.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 7 (2 `<rect>`, 3 `<line>`, 1 `<polyline>`, 1 `<path>`)
- Total anchor points: ~18 path-command anchors plus ~14 implicit anchors on rects/lines
- Stroke width: ~16 units at 256-canvas (Phosphor regular)
- Coordinate system: viewBox 0 0 256 256

## Why this tier
This calendar variant ships with `1` and `2` digits inside the calendar body. At 24pt this reads as "calendar with date 12." At 16pt the digits blob out.

## Failure mode
**Over-detailed.** Meaningful at preview size, illegible at deployment size. The `1` and `2` polyline glyphs are too thin and too close to merge into noise below ~24pt — and even at 24pt they bias the icon's meaning toward "the 12th" rather than "calendar in general."

## Why the LLM must NOT replicate this
Embedding date digits inside a calendar icon couples its semantic meaning to a specific number. A calendar icon should mean "schedule / dates in general," not "the date 12." Rendering text inside an icon also fails the squint test (negative-space.md) — the silhouette stops announcing the metaphor.

## Cross-reference
- icon-vocabulary.md section: Time & Schedule → Calendar (cliché list: literal date squares)
- Aesthetic principles violated: 1 (restraint), 7 (construction visible at 200% — text becomes noise), 9 (metaphor before ornament)
