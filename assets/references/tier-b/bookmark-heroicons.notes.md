# bookmark-heroicons (tier-B)

**Tier:** B
**Source:** Heroicons 24/outline (`bookmark-heroicons.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/outline/bookmark.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>` pennant)
- Total anchor points: ~6 path-command anchors
- Stroke width: 1.5 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Bookmark pennant rendered with a thinner stroke than the tier-A reference.

## What's missing vs tier-A
Uses stroke-width 1.5 (vs Lucide 2). At 16pt bookmark's stroke fades. Demonstrates state-pair siblings need to share stroke weight.

## What a generator should learn
State-pair siblings (outlined/filled) need to share stroke-weight calibration — 1.5 stroke fades at 16pt.

## Cross-reference
- icon-vocabulary.md section: Social & Engagement → Bookmark / Save
- Aesthetic principles applied (and where this falls short): 4 (weight perception — stroke 1.5 fades), 5 (system over single — stroke must match family)
