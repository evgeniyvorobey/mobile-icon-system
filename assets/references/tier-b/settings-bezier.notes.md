# settings-bezier (tier-B)

**Tier:** B
**Source:** Lucide outline (`settings.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/settings.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 2 (`<path>` cog body + `<circle>` aperture)
- Total anchor points: ~8 path-command anchors (rounded-bump teeth use cubic Béziers)
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Lucide's gear uses 8 cubic Bézier teeth instead of straight-edged teeth. At 20pt, the rounded-bump teeth blur into a vague star. Tabler's straight-edged 8-tooth gear (A5) survives better.

## What's missing vs tier-A
Sharper tooth profiles for small-size legibility.

## What a generator should learn
Gear teeth at small sizes need a flat-edged profile. Cubic Béziers soften the silhouette, and below ~24pt the teeth merge into the cog body.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Settings / More (also System & Settings → Settings)
- Aesthetic principles applied (and where this falls short): 7 (construction visible at 200% — soft Béziers are not legible at 20pt), 9 (metaphor before ornament — softness undermines the cog metaphor)
