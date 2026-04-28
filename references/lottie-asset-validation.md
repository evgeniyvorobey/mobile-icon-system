# Lottie Asset Validation

Use this validator after the motion spec passes and before shipping runtime
assets. The motion spec validator checks intent, reduced-motion behavior, and
handoff evidence. This asset validator checks the actual Lottie JSON and
dotLottie package files.

```bash
python3 scripts/validate_lottie_assets.py exports/lottie exports/dotlottie
python3 scripts/smoke_test_lottie_assets.py
```

The validator accepts individual files or directories. Directories are scanned
recursively for `.json` and `.lottie` files.

## What It Checks

### Lottie JSON

The validator treats each `.json` file as a Lottie animation and checks:

- Root value is a JSON object.
- Version field exists as `v` or `ver`.
- `fr`, `ip`, `op`, `w`, `h`, and `layers` exist with usable types.
- Derived duration is `(op - ip) / fr * 1000` and must stay within the mobile
  icon motion budget.
- Width and height must be positive and not huge.
- `layers` must be a non-empty array.
- Layers must be objects with recognized layer types.
- Shape layers must include shape data.
- Layer timing and dimensions are type-checked when present.

It rejects features that are allowed by some Lottie renderers but are risky for
small mobile UI icons:

- Expressions, detected as non-empty string `x` properties.
- Image layers and image/external asset references.
- Text layers, font metadata, and glyph/font payloads.
- After Effects effects payloads (`ef`).
- 3D layer rendering.
- Long durations, huge viewports, and very high frame rates.

Default limits:

- Max duration: `1500` ms.
- Max width/height: `2048` px.
- Max framerate: `120` fps.

These can be adjusted with CLI flags when a target renderer or platform has a
known exception:

```bash
python3 scripts/validate_lottie_assets.py motion/lottie --max-duration-ms 2000
```

### dotLottie

The validator treats each `.lottie` file as a ZIP archive and checks:

- Archive is readable as ZIP.
- ZIP paths are safe relative paths.
- `manifest.json` exists at the archive root and is a JSON object.
- `manifest.version` is `"2"`.
- `manifest.animations` is a non-empty array.
- Each animation `id` corresponds to `a/{id}.json`.
- At least one animation JSON file exists under `a/`.
- Extra animation JSON files under `a/` are declared in the manifest.
- Each embedded animation JSON passes the same Lottie validation as standalone
  `.json` files.
- Optional `themes` entries correspond to `t/{id}.json`.
- Optional `stateMachines` entries correspond to `s/{id}.json`.
- `initial.animation`, `initial.stateMachine`, `initialTheme`, and scoped
  `themes` references point at declared or existing assets.

The dotLottie spec allows image and font asset folders, but this icon-system
validator rejects `i/` image assets and `f/` font assets. For mobile UI icons,
ship vector shape animation and convert text to outlines before export.

## Source Facts

- The Lottie format specification defines a Lottie file as a JSON-encoded
  animation object and registers the `video/lottie+json` media type:
  [Lottie Format Specification](https://lottie.github.io/lottie-spec/dev/specs/format/).
- The Lottie schema documents the top-level animation fields this validator
  checks, including `fr`, `ip`, `op`, `w`, `h`, and `layers`:
  [Lottie JSON Schema](https://lottie.github.io/lottie-spec/dev/specs/schema/).
- The Lottie format security notes call out external image references and the
  commonly used expression extension, whose security behavior depends on the
  renderer:
  [Lottie Format Specification](https://lottie.github.io/lottie-spec/dev/specs/format/).
- Lottie expression documentation describes expressions as JavaScript /
  ECMAScript-based property logic:
  [Lottie Expressions](https://lottiefiles.github.io/lottie-docs/expressions/).
- dotLottie v2 defines `.lottie` as a ZIP package with root `manifest.json`,
  required `a/` animation files, and optional `i/`, `t/`, `s/`, and `f/`
  folders:
  [dotLottie v2.0 Specification](https://dotlottie.io/spec/2.0/).

## Limitations

This is an asset hygiene validator, not a renderer. It does not render pixels,
evaluate visual correctness, prove platform parity, or implement the complete
Lottie/dotLottie schemas. Passing validation means the asset is structurally
safe enough for mobile icon handoff; it still needs target-renderer preview,
reduced-motion QA, static-frame review, and screen-reader/state verification.
