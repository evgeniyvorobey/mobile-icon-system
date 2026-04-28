# lock-keyhole (tier-B)

**Tier:** B
**Source:** Tabler Icons outline (`lock-keyhole.svg (tabler lock)`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/tabler/tabler-icons/main/icons/outline/lock.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 3 (`<rect>` body + `<path>` shackle + `<circle>` keyhole)
- Total anchor points: ~8 path-command anchors plus 4 implicit on the keyhole circle
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Three paths including separate keyhole circle inside the body.

## What's missing vs tier-A
Keyhole is decorative microelement at 24pt and fuzzy dot at 16pt. Adds detail without adding meaning.

## What a generator should learn
Tier-A lock omits the keyhole — extra elements that don't survive at 16pt should be cut.

## Cross-reference
- icon-vocabulary.md section: Security → Lock / Unlock
- Aesthetic principles applied (and where this falls short): 1 (restraint — keyhole adds detail without meaning), 7 (construction visible — element collapses below 20pt)
