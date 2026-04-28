# fingerprint-9loops (tier-C, custom)

**Tier:** C (anti-example, hand-crafted in this repo)
**Source:** Custom — written for this calibration corpus, MIT license (this repo)
**Upstream URL:** N/A (file lives only in this repo at `assets/references/tier-c/fingerprint-9loops.svg`)
**Fetched:** 2026-04-27 (authored)

## Path data summary
- Element count: 9 (`<circle>` × 9 — concentric rings stepped at 1pt)
- Total anchor points: 36 implicit anchors (4 per circle × 9 circles)
- Stroke width: 1 (linecap round, linejoin round)
- Coordinate system: viewBox 0 0 24 24

## Why this tier
Nine perfect circles centered on (12, 12) with radii stepping 1, 2, 3, …, 9. Concentric, identical center, no offset. Reads as a target/bullseye at 24pt; merges into a fuzzy disc at 20pt; collapses to a noisy blob at 16pt.

## Failure mode
**Over-detailed at 20pt + closed concentric pattern reads as bullseye.** A real fingerprint is a few visible offset arcs with non-coincident centers (see tier-A `fingerprint.svg` from Phosphor). Forcing 9 concentric circles destroys both the breathing-silhouette quality and the recognizability at deployment sizes.

## Why the LLM must NOT replicate this
Compare against tier-A `fingerprint.svg`: 7 partial loops, none concentric, each with slightly different center and radius. Phosphor deliberately offsets so the silhouette breathes. The anti-example violates icon-vocabulary.md "fingerprint cliché list" (closed concentric pattern) and aesthetic principle 1 (restraint — every additional loop reduces, not increases, recognizability).

## Cross-reference
- icon-vocabulary.md section: Security → Fingerprint / Biometric
- Aesthetic principles violated: 1 (restraint — 9 loops vs 2-3 visible arcs), 7 (construction visible at 200% — concentric circles audit as bullseye, not print)
