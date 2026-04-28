# check-micro-20

**Tier:** A
**Source:** Heroicons 20/solid (micro) (`check-micro-20.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/tailwindlabs/heroicons/master/optimized/20/solid/check.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>` filled checkmark wedge)
- Total anchor points: ~6 path-command anchors
- Stroke width: none (micro icons are fill-only)
- Coordinate system: viewBox 0 0 20 20

## Why this tier
20pt-micro exemplar of the check metaphor — the intermediate canvas between mini-16 and regular-24. Same fill-wedge construction as mini-16, but vertex rounding scales proportionally larger (≈12% of canvas vs mini's ≈8%) and the joint can be slightly thinner because 20pt has more pixels to allocate to anti-aliasing. Demonstrates that mini/micro/regular tiers each have distinct calibration.

## What a generator should learn
20pt-micro is its own tier — vertex rounding and joint thickness sit between 16pt-mini and 24pt-regular, not interpolated automatically.

## Cross-reference
- icon-vocabulary.md section: Native-small / Micro → Check (20pt)
- Aesthetic principles applied: 4 (weight perception — distinct from mini and regular), 5 (system over single — micro-family rule)
