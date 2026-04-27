# notification-color-state (tier-C, custom)

**Tier:** C (anti-example, hand-crafted in this repo)
**Source:** Custom — written for this calibration corpus, MIT license (this repo)
**Upstream URL:** N/A (file lives only in this repo at `assets/references/tier-c/notification-color-state.svg`)
**Fetched:** 2026-04-27 (authored)

## Path data summary
- Element count: 3 (`<path>` bell body + `<path>` clapper + `<circle>` red dot)
- Total anchor points: ~14 path-command anchors plus 4 implicit on the indicator circle
- Stroke width: 1.5 (bell); the indicator dot uses `fill="red"` only (no stroke)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
A bell icon at 24×24 with a red `<circle>` dot at the upper right. The dot is the entire "unread state" — there is no shape change, no badge ring, no shape addition between the read and unread variants. The only differentiation is the red fill.

## Failure mode
**Color-only state distinction.** Violates accessibility:
- Fails on Forced Colors mode (Windows High Contrast): system overrides `fill="red"` with the user's chosen foreground color, removing the distinction.
- Indistinguishable under deuteranopia simulation (red ↔ dark grey collapse).
- Screen readers see no semantic difference between read and unread; both icons are byte-identical except for one attribute.

## Why the LLM must NOT replicate this
State must be distinguishable by shape, not color. A correct unread indicator is an outlined or filled badge ring (the badge's presence/absence is the state, the color is decoration). Generally: when generating icon families with state variants, the state difference should survive monochrome rendering.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Notifications / Inbox
- references/accessibility.md: state must be distinguishable without color (Forced Colors, color-blindness)
- Aesthetic principles violated: 6 (quiet over loud — color compensating for missing shape), 9 (metaphor before ornament — color is the only ornament carrying meaning)
