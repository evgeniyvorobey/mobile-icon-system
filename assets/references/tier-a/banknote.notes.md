# banknote

**Tier:** A
**Source:** Lucide outline (`banknote.svg`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/banknote.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 3 (`<rect>` body + `<path>` serial-dots + `<circle>` portrait medallion)
- Total anchor points: ~6 path-command anchors plus 8 implicit on rect/circle
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Outer `<rect>` + serial-number-dots `M6 12h.01M18 12h.01` + center `<circle cx="12" cy="12" r="2"/>`. Two `.01`-length lines at left/right are dots representing serial-number positions. Center circle is "portrait medallion" without rendering actual face. **No currency symbol — works internationally.**

## What a generator should learn
Banknote = rect + serial dots + portrait medallion; avoid `$` (locale-bound).

## Cross-reference
- icon-vocabulary.md section: Money / Payment → Cash / Bills
- Aesthetic principles applied: 1 (restraint — no $ glyph, no face), 5 (system over single — internationalisable), 9 (metaphor before ornament)

## Known small-size limitation

This icon is tier-A **at its design size (24pt+)** but hard-fails the silhouette stability check at 16pt — the `.01`-length serial-number dots vanish into the background, dropping the connected-component count. **Do not naively downscale this icon to 16pt.** For sub-20pt rendering contexts (notification rail, inline list affordance), pair with a purpose-built 16pt-native variant (Heroicons mini, or hand-redraw without the dot details). The grader's hard_fail on this icon is informative — it teaches "what works at 24pt does not always survive 16pt" and pairs with `tier-a-mini/` exemplars to show the size-variant principle.
