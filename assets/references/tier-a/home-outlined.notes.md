# home-outlined

**Tier:** A
**Source:** Lucide outline (`house.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/house.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<path>` x2)
- Total anchor points: ~17 path-command anchors across both paths
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
(1) Two paths only — door+window line and house body. Door is a single rounded path `M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8` — 4 anchors, two perfect 1pt corner arcs. (2) The house body uses construction-sketch arithmetic: `M3 10 a2 2 0 0 1 .709-1.528l7-6 a2 2 0 0 1 2.582 0l7 6 A2 2 0 0 1 21 10v9` — the roof apex is implicit at `(12, 4)` because `7+5=12` and `10-6=4`, never named explicitly. The 2pt corner radius at every house corner is consistent (`a2 2`). (3) Coordinate values are mostly integers (3, 10, 12, 21, 9, 19) — sub-1px hinting on common DPRs.

## What a generator should learn
Two paths (body + insert), every corner radius equal, peak deduced from arithmetic — not coordinated as a separate anchor.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Home / Main
- Aesthetic principles applied: 1 (restraint), 2 (rhythm — shared 2pt corner radius), 7 (construction visible at 200%)
