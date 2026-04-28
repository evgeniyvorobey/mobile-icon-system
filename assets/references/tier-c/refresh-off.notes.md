# refresh-off (tier-C)

**Tier:** C (anti-example)
**Source:** Lucide outline (`refresh-off.svg (lucide refresh-cw-off)`), ISC license
**Upstream URL:** https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/refresh-cw-off.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: multiple (`<path>` refresh fragments + slash)
- Total anchor points: ~14 path-command anchors total
- Stroke width: 2 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Refresh icon with a corner-to-corner slash through it.

## Failure mode
Useful for cloud/sync state pair: refresh-cw + refresh-cw-off teach slash-on-action language for off-states across entire system. Catalogued as tier-C only because it pre-empts tier-A's choice — use sparingly.

## Why the LLM must NOT replicate this
Treat as a calibration anchor for the slash-on-action off-state language across the family (paired with eye-off, mic-off, cloud-off). Don't lift this construction blindly — its slash isn't always the right answer for every off-state.

## Cross-reference
- icon-vocabulary.md section: Common Actions → Refresh / Sync (off-state)
- Aesthetic principles violated: 3 (intentional asymmetry — slash), 5 (system over single — slash language consistency)
