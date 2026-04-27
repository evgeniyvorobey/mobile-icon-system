# settings-12tooth (tier-C)

**Tier:** C (anti-example)
**Source:** Material Symbols Outlined (`settings_24px.svg`), Apache-2.0 license
**Upstream URL:** https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/settings/materialsymbolsoutlined/settings_24px.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 1 (`<path>`)
- Total anchor points: ~68 path-command anchors (twelve teeth, each with curved approach)
- Stroke width: filled (no root stroke; outlined-style fill via even-odd or non-zero)
- Coordinate system: viewBox 0 -960 960 960

## Why this tier
12 cog teeth. Comparing to Tabler's 8-tooth, this is the tier-C end of "more-is-more" thinking. At 20pt the 12 teeth merge into a fuzzy-edged disc.

## Failure mode
**Blob at 20pt.** Twelve teeth at 24px viewport gives each tooth ~2pt of arc — below the visual threshold for separable features at typical UI sizes. The icon ceases to read as "gear" and starts to read as "circle with bumps."

## Why the LLM must NOT replicate this
The skill's settings reference (Tabler 8-tooth) is the empirically tested optical sweet spot. Adding teeth feels like more detail; it actually destroys the metaphor's legibility. Always derive tooth count from a stated rule (45° per tooth → 8 teeth), never from "looks more like a gear."

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Settings / More (cliché list: gear with too many teeth)
- Aesthetic principles violated: 1 (restraint), 7 (construction visible at 200% — teeth become unreadable), 9 (metaphor before ornament)
