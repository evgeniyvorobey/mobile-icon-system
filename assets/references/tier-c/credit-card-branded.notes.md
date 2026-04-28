# credit-card-branded (tier-C, custom)

**Tier:** C (anti-example, hand-crafted in this repo)
**Source:** Custom — written for this calibration corpus, MIT license (this repo)
**Upstream URL:** N/A (file lives only in this repo at `assets/references/tier-c/credit-card-branded.svg`)
**Fetched:** 2026-04-27 (authored)

## Path data summary
- Element count: 6 (`<rect>` body + `<line>` magstripe + `<rect>` chip + 2 chip detail lines + 2 swoosh arcs)
- Total anchor points: ~14 path-command anchors plus 8 implicit on rects/lines
- Stroke width: 1.5 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Card body + magnetic stripe + chip square with cross-mullion detail + two stacked arcs in lower-right that read as a Visa-like swoosh. Elements pile up: each one might be defensible alone, but together they couple the icon to a specific payment brand.

## Failure mode
**Brand-coupled metaphor.** The swoosh narrows the icon's meaning from "credit card in general" to "Visa specifically". Once a generic icon points at one brand, every other brand looks wrong by association — and the icon stops working in any product that supports more than one card network.

## Why the LLM must NOT replicate this
Compare against tier-A `credit-card.svg` (Lucide): 2 primitives only — `<rect>` + `<line>` in upper third. No chip square, no swoosh, no brand mark. The minimal construction is what lets the icon mean "any payment card". Violates icon-vocabulary.md "Money / Payment" guidance (avoid brand-bound details) and aesthetic principle 9 (metaphor before ornament).

## Cross-reference
- icon-vocabulary.md section: Money / Payment → Credit Card
- Aesthetic principles violated: 1 (restraint — chip + swoosh are ornament), 9 (metaphor before ornament — brand swoosh hijacks meaning)
