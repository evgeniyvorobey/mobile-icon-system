# fingerprint

**Tier:** A
**Source:** Phosphor regular (`fingerprint.svg`), MIT license
**Upstream URL:** https://raw.githubusercontent.com/phosphor-icons/core/main/raw/regular/fingerprint.svg
**Fetched:** 2026-04-27

## Path data summary
- Element count: 7 (`<path>` × 7 partial loops)
- Total anchor points: ~22 path-command anchors across all loops
- Stroke width: 16 units at 256-canvas (Phosphor regular weight)
- Coordinate system: viewBox 0 0 256 256

## Why this tier
Seven sub-paths, each a partial loop. **Crucially: not concentric.** Each loop has slightly different center and radius — Phosphor deliberately offsets so silhouette breathes like real print.

## What a generator should learn
Fingerprint is 2-3 visible offset arcs, never closed concentric pattern.

## Cross-reference
- icon-vocabulary.md section: Security → Fingerprint / Biometric
- Aesthetic principles applied: 3 (intentional asymmetry — offset loops), 7 (construction visible — non-concentric centers)

## Known small-size limitation

This icon is tier-A **at its design size (24pt+)** but hard-fails the silhouette stability check at 16pt — Phosphor's deliberately offset loops, which read as "real fingerprint breathing" at 24pt, merge perceptually below 20pt. **Do not naively downscale this icon to 16pt.** Biometric authentication UIs typically render at 32-48pt prominent sizes anyway; if a small-size fingerprint affordance is needed (toolbar), use a simplified 2-arc variant or substitute the iOS Touch ID system glyph. The grader's hard_fail on this icon is informative — it teaches "tier-A craft can be size-bound."
