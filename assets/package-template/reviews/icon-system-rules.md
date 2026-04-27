# Icon System Rules — {{PROJECT_NAME}}

Project: {{PROJECT_NAME}}
Owner: {{OWNER}}
Date: {{DATE}}
Skill version: {{SKILL_VERSION}}

The locked rule set. This is the authoritative document engineering refers to when adding new icons. Confirmed by user at workflow phase 5 gate.

## Grid

- **Base**: <!-- e.g., 24×24 -->
- **Live area**: <!-- e.g., 20×20 (2pt keyline padding) -->
- **Pixel grid increment**: <!-- e.g., 0.5pt -->
- **Keyline shapes used**: <!-- e.g., square 18, circle ⌀20, vertical 16×20, horizontal 20×16 -->

## Stroke

- **Weight (orthogonal)**: <!-- e.g., 1.75pt -->
- **Weight (diagonal compensation)**: <!-- e.g., 1.85pt (5%) -->
- **Cap style**: <!-- e.g., round -->
- **Join style**: <!-- e.g., round -->
- **Miterlimit (if miter joins)**: <!-- e.g., 4 -->
- **Internal detail stroke (if contrast pair)**: <!-- e.g., 1pt -->

## Terminals + Corners

- **Terminal style**: <!-- round / square / cut -->
- **Outer corner radius**: <!-- e.g., 2pt -->
- **Inner corner radius**: <!-- e.g., 0 (matches outer / half outer / 0) -->

## Style

- **Default**: <!-- outlined / filled / both -->
- **State pair**: <!-- e.g., filled = selected/active; outlined = unselected/inactive -->
- **Single-state icons**: <!-- list scopes that use only one state, e.g., action icons single-state -->

## Color

- **Mode**: <!-- monochrome platform-tinted / duotone / multi-color -->
- **iOS export**: <!-- PDF template image, Render As: Template Image -->
- **Android export**: <!-- vector drawable with android:tint="?attr/colorOnSurface" -->
- **Baked color allowed?**: <!-- no -->
- **Duotone color roles (if used)**: 
  - Primary: <!-- color, 60-80% of icon mass -->
  - Secondary: <!-- color, 20-40% of icon mass -->
  - Reserved: <!-- colors not used in icons -->

## Optical Corrections

- **Diagonal stroke compensation**: <!-- e.g., 3-7% thicker -->
- **Circle overshoot**: <!-- e.g., 1-2% of bounding box -->
- **Visual centering for directional icons**: <!-- yes -->
- **Negative-space density compensation**: <!-- yes — 2-3% scale-up for dense icons -->

## Naming Convention

Format: `ic_{{scope}}_{{name}}_{{state}}.{{ext}}`

Scopes:
- `tab_` — Tab Bar / Bottom Nav
- `nav_` — navigation icons (back, forward, menu, close)
- `action_` — action icons (add, share, edit, delete)
- `status_` — status indicators
- `inline_` — inline / list affordances

State suffixes:
- `_filled`
- `_outlined`
- (no suffix for single-state icons)

Examples:
- `ic_tab_home_filled.svg`
- `ic_action_share.svg`
- `ic_nav_back.svg`

## Brand DNA Source

<!-- Document where the rules came from -->

- [ ] Read from `brand-dna.md` at <!-- path -->
- [ ] Extracted from <!-- logo file path -->
- [ ] Provided directly by user

## Approval

- **Confirmed by**: {{OWNER}}
- **Date confirmed**: {{DATE}}
- **Notes**: <!-- any deviations from auto-proposal, exceptions, etc. -->
