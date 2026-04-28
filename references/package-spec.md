# Package Spec

Final deliverables specification for an icon-system handoff. Use this in workflow phase 13. The package is what engineering and design teammates receive — it must be self-contained, named consistently, and usable without coming back to ask questions.

## Package Structure

```
icon-system-package/
├── README.md                       # what's in here, how to use it
├── system-rules.md                 # the locked rules (grid, stroke, terminals, corners, color)
├── brand-dna-applied.md            # which Brand DNA dimensions inform which rules
├── vocabulary.md                   # icon list with metaphors and rationale
├── concepts/                       # exploratory rounds (kept for reference)
├── selected/                       # the chosen rule set + icon set
│   ├── rationale.md                # why this direction was chosen
│   ├── usage-guidance.md           # how to use icons in product
│   ├── tab-bar-icon-notes.md       # iOS-specific notes
│   ├── bottom-nav-notes.md         # Android-specific notes
│   └── export-checklist.md         # what to export, in what format
├── motion/                         # optional animated-icon subsystem
│   ├── motion-spec.json            # validated motion contract
│   ├── static-frames/              # reduced-motion and preview frames
│   ├── lottie/                     # .json exports, one per animated icon
│   └── dotlottie/                  # .lottie bundles when used
├── style-review/                   # optional A/B/C review artifacts
│   ├── shared-brief.md
│   ├── decision-log.md
│   └── style-{a,b,c}/
├── style-plugins/                  # optional user .style-pack manifests
├── exports/
│   ├── ios/
│   │   ├── pdf/                    # template images for asset catalog
│   │   └── xcassets/               # ready-to-drop xcassets folders (optional)
│   ├── android/
│   │   ├── vector-drawables/       # vector drawable XML
│   │   └── res/                    # ready-to-drop res folder structure (optional)
│   └── svg-masters/                # source SVG files (24×24 grid)
└── reviews/
    ├── project-ui-snapshot.md      # what the audit found
    ├── icon-system-rules.md        # the rules document (mirrored from selected/)
    ├── concept-scorecard.md        # evaluation matrix output
    └── cross-icon-audit.md         # consistency audit output
```

## Per-Icon Master File

For every icon in the set, ship:

- **SVG master** — 24×24 grid (or documented grid), one file per icon, one file per state
- Naming: `ic_{purpose}_{state}.svg`
  - `ic_tab_home_filled.svg`
  - `ic_tab_home_outlined.svg`
  - `ic_action_share.svg`
  - `ic_nav_back.svg`

## Export Formats

### iOS

- **PDF template image** — single PDF file per icon (vector, scales automatically)
  - Naming: `home_filled.pdf`, `home_outlined.pdf`
  - Render As: Template Image (in xcassets)
- Optional: xcassets folder ready to drop in

### Android

- **Vector drawable XML** — one XML per icon
  - Naming: `ic_tab_home_filled.xml`, `ic_tab_home_outlined.xml`
  - Tint: `android:tint="?attr/colorOnSurface"` or per project theme
- Optional: full res folder structure

### Cross-platform (React Native, Flutter, web)

- **SVG masters** — same files used in iOS/Android source
- Document any platform-specific transforms needed

## Naming Convention

Lowercase, snake_case, prefix-organized:

- `ic_` — universal icon prefix
- `tab_` — Tab Bar / Bottom Nav scope
- `nav_` — navigation icons (back, forward, menu)
- `action_` — action icons (share, edit, delete)
- `status_` — status indicators
- `_filled` / `_outlined` — state suffix
- `_disabled` (if separate asset needed)

Example:
- `ic_tab_home_filled.svg`
- `ic_action_share.svg`
- `ic_status_success.svg`

Document the convention in `system-rules.md`.

## Motion Deliverables

Motion is packaged only when animated icons are in scope. It is not a visual style pack.

Required files:

- `motion/motion-spec.json` — validated with `python3 scripts/validate_motion_spec.py motion/motion-spec.json`
- `motion/static-frames/` — one static fallback frame per animated icon
- `motion/lottie/` — Lottie JSON files when Lottie is a delivery target
- `motion/dotlottie/` — dotLottie bundles when multiple animations, themes, or state machines are needed
- `selected/usage-guidance.md` — implementation notes explaining triggers, replay rules, reduced-motion behavior, and renderer assumptions

Motion specs must include a reduced-motion substitute. If the default animation conveys meaning, the substitute must preserve the meaning with a non-motion pattern such as a static state, highlight fade, dissolve, haptic note, or copy/state update.

## Multi-Style Review Deliverables

When the user requests A/B/C client review, scaffold a review package with:

```bash
python3 scripts/init_multi_style_review.py /path/to/review \
  --project-name "Project Name" \
  --styles liquid-glass,3d-isometric,hand-drawn
```

The review package is not the production package. After the client chooses one style, copy only the winning style into `exports/svg-masters/` and document the decision in `selected/rationale.md`.

## Style Plugin Deliverables

User-supplied `.style-pack` manifests live in `style-plugins/`. Validate them before use:

```bash
python3 scripts/validate_style_pack.py style-plugins/
```

The package must preserve the validated manifest so future designers can reproduce the construction rules.

## System Rules Document

`system-rules.md` is the authoritative ruleset. Engineering refers to this when adding new icons.

Required sections:

```markdown
# Icon System Rules — {{Project Name}}

Generated: {{date}}
Skill version: mobile-icon-system v{{version}}

## Grid
- Base: 24×24 (or documented)
- Live area: 20×20 (2pt padding)
- Pixel grid: 0.5pt increments

## Stroke
- Weight: 1.75pt orthogonal, 1.85pt diagonal (compensation rule documented)
- Cap: round
- Join: round
- Miterlimit: 4

## Terminals + Corners
- Terminal style: round
- Outer corner radius: 2pt
- Inner corner: matches outer

## Style
- Default: outlined
- States: filled (Tab Bar selected, Bottom Nav active) + outlined (other)

## Color
- Mode: monochrome, platform-tinted
- iOS: PDF template image
- Android: `android:tint="?attr/colorOnSurface"`
- No baked color

## Naming
- Convention: ic_{scope}_{name}_{state}
- Lowercase snake_case

## Optical Corrections
- Diagonal stroke compensation: 3-7%
- Circle overshoot: 1-2%
- Visual centering for directional icons
```

## Usage Guidance

`selected/usage-guidance.md` documents how to use the icons:

- Where each icon belongs (Tab Bar / Bottom Nav / action / inline)
- Which size to use at which surface
- State requirements (filled for active, outlined for inactive)
- Color tinting rules per surface
- Touch target requirements

## Platform Notes

### `tab-bar-icon-notes.md`

- Canonical size: 25pt template image
- States: filled (selected) + outlined (unselected)
- Color: monochrome, tinted by Tab Bar tint
- Asset catalog setup: Render As = Template Image
- Light + dark mode behavior verified

### `bottom-nav-notes.md`

- Canonical size: 24dp vector drawable
- States: filled (active) + outlined (inactive)
- Color: tinted via theme attributes
- Material 3 active indicator (pill background) compatible
- Themed icon (Material You) compatibility verified

## Export Checklist

`selected/export-checklist.md` is the engineering checklist. Each item is a binary check:

```markdown
## Export Checklist

### iOS
- [ ] All Tab Bar icons exported as PDF template images
- [ ] All Tab Bar icons added to xcassets with Render As: Template Image
- [ ] Light + dark mode tested in simulator
- [ ] Tinting verified on real device

### Android
- [ ] All Bottom Nav icons exported as vector drawables
- [ ] `android:tint` set per system rules
- [ ] Light + dark theme tested in emulator
- [ ] Themed (Material You) verified on Android 13+

### Cross-cutting
- [ ] SVG masters committed to design system repo
- [ ] system-rules.md committed to docs
- [ ] usage-guidance.md committed to docs
- [ ] Naming convention applied consistently
- [ ] No baked color in any asset
- [ ] Motion specs validated and static fallback frames included when animated icons ship
- [ ] Custom `.style-pack` manifests validated when custom styles are used
- [ ] Multi-style review decision logged before production exports are finalized
```

## Rationale

`selected/rationale.md` documents why this direction was chosen:

- Brand DNA dimensions that drove the rules
- Audit findings that informed redesign tolerance
- Alternative rule sets considered (from divergence pass)
- Why this set wins
- Risks accepted and mitigations

This is the document a future designer reads to understand the system without rebuilding it.

## Unresolved Risks

If any risks remain after evaluation and validation, list them in `rationale.md`:

```markdown
## Unresolved Risks

1. Library icon at 16pt — bottom shelf line nearly disappears.
   Mitigation: document 16pt fallback variant or restrict Library to ≥20pt contexts.

2. Settings gear teeth count (6) close to small-size collapse threshold.
   Mitigation: monitor analytics for Settings discovery; revisit if discovery rate drops.

3. Themed icon tinting: not yet tested on Android 14 stable channel.
   Mitigation: re-verify on first Android 14 device in QA.
```

## Failure Modes

- **Package without rules document** — engineering invents rules to fill gaps
- **Inconsistent naming** — engineering can't find icons predictably
- **Baked color in exports** — breaks tinting silently
- **No state pair in Tab Bar / Bottom Nav exports** — incomplete platform fit
- **No usage-guidance** — icons used in wrong contexts (Tab Bar icon used inline)
- **No risk documentation** — known issues become surprise bugs in production
- **Motion package without static frames** — reduced-motion users lose the state cue
- **Unvalidated `.style-pack` manifest** — future generation cannot reproduce the style safely
- **A/B/C review package treated as production** — unchosen style drafts leak into app builds
