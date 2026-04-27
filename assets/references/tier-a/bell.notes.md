# bell

**Tier:** A
**Source:** Lucide outline (`bell.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/bell.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<path>` clapper + `<path>` bell body)
- Total anchor points: ~9 path-command anchors across both paths
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
(1) Two paths only — clapper `M10.268 21 a2 2 0 0 0 3.464 0` and bell body. No "ringing lines" cliché. (2) Clapper coordinates `(10.268, 21)` and `(13.732, 21)` are symmetric around `x=12` — the gap is `3.464 = 2√3`, meaning the clapper subtends exactly 60° from the bell's centerline. Mathematically derived. (3) The dome ends at `y=15.326`, leaving a ~1pt visual gap before the clapper — this is optical correction: the bell-clapper junction is the recognition pivot, so it gets breathing room.

## What a generator should learn
Bell = dome + clapper. No ringing lines. Clapper width = √3 × stroke-width worth of separation. Visual gap between dome and clapper.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Notifications / Inbox
- Aesthetic principles applied: 1 (restraint — no motion lines), 4 (weight perception — visual gap at the junction), 7 (construction visible — 60° subtended is auditable)
