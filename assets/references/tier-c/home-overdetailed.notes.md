# home-overdetailed (tier-C, custom)

**Tier:** C (anti-example, hand-crafted in this repo)
**Source:** Custom — written for this calibration corpus, MIT license (this repo)
**Upstream URL:** N/A (file lives only in this repo at `assets/references/tier-c/home-overdetailed.svg`)
**Fetched:** 2026-04-27 (authored)

## Path data summary
- Element count: 13 (`<path>` x12 + `<circle>` x1) — well above the ≥7 spec
- Total anchor points: ~50 path-command anchors plus 4 implicit on the circle (well above the ≥40 spec)
- Stroke width: 1.5
- Coordinate system: viewBox 0 0 24 24

## Why this tier
This is a literal house: walls, peaked roof, chimney rectangle on the roof, three windows each with a cross mullion (4 quadrants per window), a front door with a doorframe outline, and a door knob.

## Failure mode
**Over-detailed.** Direct violation of icon-vocabulary.md cliché list ("literal house with chimney + door + window"). At 20pt all the window mullion lines, door frame, and chimney edges merge into a bristly silhouette. The recognition pivot for "home" is the simple house shape — every additional detail reduces, not increases, recognizability at deployment sizes.

## Why the LLM must NOT replicate this
Adding rendered detail to icons feels like added value during generation but actively destroys the metaphor at deployment. The chimney has zero semantic value (most users have never owned a chimney). Cross-mullion windows are 19th-century architectural detail. Door knobs disappear at 20pt. Compare against tier-A `home-outlined.svg` (Lucide): 2 paths, ~17 anchors, instantly recognizable as "home."

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Home / Main (cliché: literal house with chimney + door + window)
- Aesthetic principles violated: 1 (restraint), 7 (construction visible at 200% — every line is noise), 9 (metaphor before ornament — ornament has eaten the metaphor)
