# mic-tabler (tier-B)

**Tier:** B
**Source:** Tabler Icons outline (`mic-tabler.svg (tabler microphone)`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/tabler/tabler-icons/main/icons/outline/microphone.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 4 (`<path>` capsule + cradle + post + base bar)
- Total anchor points: ~12 path-command anchors total
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Capsule + cradle + post + an explicit horizontal base bar `M8 21l8 0`.

## What's missing vs tier-A
Four paths including separate base bar `M8 21l8 0`. Explicit base bar makes icon read as "podium mic on stand" (3-element silhouette) rather than abstract two-element handheld mic.

## What a generator should learn
Tier-A mic omits the base bar — the post alone is sufficient and reads as handheld; the bar implies a stand and narrows the metaphor.

## Cross-reference
- icon-vocabulary.md section: Media → Microphone / Voice
- Aesthetic principles applied (and where this falls short): 1 (restraint — base bar is decorative), 9 (metaphor before ornament — bar narrows the meaning)
