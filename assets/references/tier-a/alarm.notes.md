# alarm

**Tier:** A
**Source:** Lucide outline (`alarm.svg (lucide alarm-clock)`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/alarm-clock.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 6 (`<circle>` body + `<path>` hands + 4 corner-accent paths)
- Total anchor points: ~14 path-command anchors total
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
`<circle cx="12" cy="13" r="8"/>` + hands + four "feet/bells". Clock body shifted to cy=13 (1pt below canvas center) leaves room for top "bells". Two top angled lines (5,3 → 2,6 and 22,6 → 19,3) are bells; two bottom lines are feet. Hands read ~9:07 (different from clock's 10:10, deliberately not matching).

## What a generator should learn
Alarm = clock body + 4 corner accents (bells top, feet bottom); hands at 9:07 to differentiate from regular clock at 10:10.

## Cross-reference
- icon-vocabulary.md section: Time & Schedule → Alarm / Reminder
- Aesthetic principles applied: 3 (intentional asymmetry — hands distinct from clock), 5 (system over single — alarm distinguishable from clock in family)
