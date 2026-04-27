# home-outlined (tier-B)

**Tier:** B
**Source:** Heroicons 24/outline (`home.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/outline/home.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>`)
- Total anchor points: ~17 path-command anchors (concatenated sub-paths)
- Stroke width: 1.5 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Single concatenated path with 12+ anchors and a clearly visible "construction joint" at `M8.25 21h8.25` — the floor line is a separate sub-path glued onto the body.

## What's missing vs tier-A
Lucide and Phosphor both make the door+wall a single shape. Heroicons split it, producing a small gap that flickers at 20pt zoom.

## What a generator should learn
A house body and door must either be modeled as one continuous path or as two cleanly disjoint shapes — never as overlapping sub-paths joined inside one `d` attribute. Construction joints must be invisible at the deployment size.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Home / Main
- Aesthetic principles applied (and where this falls short): 7 (construction visible at 200% — this icon's joint is too visible), 8 (family resemblance — vs Lucide's two-path house)
