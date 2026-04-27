# calendar

**Tier:** A
**Source:** Lucide outline (`calendar.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/calendar.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 4 (1 `<rect>` body + 3 `<path>` — divider, two binding posts)
- Total anchor points: ~10 across the three paths plus 4 implicit anchors on the rect
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
(1) Four primitives — body `<rect width="18" height="18" x="3" y="4" rx="2"/>`, top divider `<path d="M3 10h18"/>`, two binding posts `M8 2v4` and `M16 2v4`. Anchor count for a calendar is rarely this low. (2) Posts are spaced symmetrically: x=8 and x=16, mirrored around x=12. Each post is exactly 4pt long — two body-stroke widths. (3) The body has `rx=2` (rounded corners) but the binding posts have round endcaps, not separate rect rounds — terminal style is consistent across the icon.

## What a generator should learn
Calendar = rounded rect + horizontal divider line + two short vertical binding posts. No grid of date squares (cliché).

## Cross-reference
- icon-vocabulary.md section: Time & Schedule → Calendar
- Aesthetic principles applied: 1 (restraint — no date-grid cliché), 2 (rhythm — shared 2pt corner radius), 8 (family resemblance — terminal style consistent)
