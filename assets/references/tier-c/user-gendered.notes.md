# user-gendered (tier-C, custom)

**Tier:** C (anti-example, hand-crafted in this repo)
**Source:** Custom — written for this calibration corpus, MIT license (this repo)
**Upstream URL:** N/A (file lives only in this repo at `assets/references/tier-c/user-gendered.svg`)
**Fetched:** 2026-04-27 (authored)

## Path data summary
- Element count: 7 (`<path>` x6 + `<circle>` x1)
- Total anchor points: ~22 path-command anchors plus 4 implicit on the head circle
- Stroke width: 1.5
- Coordinate system: viewBox 0 0 24 24

## Why this tier
A profile/user icon with a head circle, two long-hair triangles flowing past the shoulders down to chest level (clearly feminine-coded), a torso with a V-neckline, and arms-akimbo (hands on hips) creating triangular cavities for the elbows.

## Failure mode
**Gendered.** Violates icon-vocabulary.md Profile guidance: "avoid gender-coded forms; circle avatar is safest." Long-hair shapes plus arms-akimbo posture read as a stylized woman, which excludes (or worse, mis-attributes) every user whose self-presentation does not match. Profile icons should default to a non-gendered form (head circle + shoulder arc, per tier-A `user.svg`).

## Why the LLM must NOT replicate this
The profile icon is the user's representation of themselves in the app. Encoding gender into that representation forces every user whose gender does not match into a misrepresentation. The safe form is a circle (or circle+shoulder-arc): it is the union of all possible profile photos rather than a specific subset. Compare against tier-A `user.svg` (Lucide): head circle + shoulder arc, no hair, no posture, no presumption.

## Cross-reference
- icon-vocabulary.md section: Tab Bar / Bottom Nav Standards → Profile / Account / Me (cliché: gendered figure)
- Aesthetic principles violated: 1 (restraint — too many primitives), 9 (metaphor before ornament — ornament codes gender)
- Cross-cultural failure: long-hair + akimbo posture is gender-coded across most cultures
