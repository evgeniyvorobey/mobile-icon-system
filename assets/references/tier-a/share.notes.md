# share

**Tier:** A
**Source:** Lucide outline (`share.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/share.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 3 (`<path>` tray + `<path>` arrowhead + `<path>` arrow stem)
- Total anchor points: ~9 path-command anchors total
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
(1) Three paths: arrow stem `M12 2v13`, arrowhead `m16 6-4-4-4 4`, tray. (2) The arrow-up metaphor is correct iOS-share semantics; the chevron arrowhead lands exactly at the stem origin (`y=2`), no overshoot or gap. (3) Tray uses 2pt radius corners — same family as Lucide's other rounded rects. The arrow stem stops at `y=15`, NOT at the tray top edge — there's a 3pt visual gap so the arrow reads as "exiting" the tray, not "drawn inside" it.

## What a generator should learn
Share = tray + up-arrow with explicit gap between arrow base and tray rim. Arrow goes UP not horizontally (sharing is "out of the box," not "send to right").

## Cross-reference
- icon-vocabulary.md section: Action Icons → Share
- Aesthetic principles applied: 2 (rhythm — 2pt corner radius shared), 4 (weight perception — 3pt gap so arrow reads as exiting), 8 (family resemblance — Lucide rounded-rect grammar)
