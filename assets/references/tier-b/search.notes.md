# search (tier-B)

**Tier:** B
**Source:** Heroicons 24/outline (`magnifying-glass.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/24/outline/magnifying-glass.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>`)
- Total anchor points: ~5 path-command anchors (lens arc + handle line)
- Stroke width: 1.5 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
`m21 21-5.197-5.197` — the handle is `5.197` long, suggesting `√27 = 3√3`. Why this number? Because the lens uses `r=7.5` and the handle was eyeballed to "look right." Lucide's 4.34 is derived from circle-to-corner geometry; Heroicons' 5.197 is decorative.

## What's missing vs tier-A
Mathematical derivation. The handle should be a function of the lens radius, not a chosen value.

## What a generator should learn
Magnifying-glass handles are not eyeballed. Their length should be derived from the lens radius via a stated rule (e.g., distance from circle edge to corner with a specified gap).

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Search / Discover
- Aesthetic principles applied (and where this falls short): 7 (construction visible at 200% — derivation is invisible because there isn't one)
