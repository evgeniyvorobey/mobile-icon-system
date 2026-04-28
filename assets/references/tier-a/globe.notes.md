# globe

**Tier:** A
**Source:** Lucide outline (`globe.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/globe.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 3 (`<circle>` sphere + `<path>` equator + `<path>` meridian)
- Total anchor points: ~6 path-command anchors plus 4 implicit on the circle
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
`<circle cx="12" cy="12" r="10"/>` + horizontal `M2 12h20` + meridian `M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20`. **Meridian uses radius 14.5, not 10** — meridian is flatter than equator due to implied 3D rotation foreshortening. 14.5 is empirical sweet spot (10 = impossible exceeds sphere; 20+ flat).

## What a generator should learn
Globe = sphere + flatter meridian arc; single number (14.5 vs 10) is the entire 3D illusion.

## Cross-reference
- icon-vocabulary.md section: Location → Globe / Region
- Aesthetic principles applied: 3 (intentional asymmetry — meridian flatter than equator), 7 (construction visible — 14.5 vs 10 is auditable)
