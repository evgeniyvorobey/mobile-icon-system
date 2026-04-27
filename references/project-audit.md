# Project Audit

How to inspect the current app's UI patterns and existing icon set before designing or refreshing. This is workflow phase 3. The goal is a UI snapshot that informs Brand DNA application and redesign tolerance — not a critique of the current product.

## What to Inspect

### 1. Existing icon set

Search the project for current icons:

- `Assets.xcassets/` (iOS)
- `res/drawable*/` (Android)
- `assets/icons/`, `src/icons/`, `src/assets/icons/` (cross-platform)
- `public/icons/`, `static/icons/` (web/PWA)
- Figma file links if referenced in the project

For each icon found, note:
- Source (Material / SF / Lucide / custom)
- Size in source
- Stroke weight if visible
- Filled / outlined / mixed
- Color: monochrome, multi-color, baked color
- File format (SVG, PDF, PNG, vector drawable)

### 2. App screenshots

Look for:
- `assets/screenshots/`, `docs/screenshots/`
- Figma boards or design files
- Marketing materials with app UI shots

Inspect: how do current icons look in actual context? What's the visual tone of the surrounding UI?

### 3. Color tokens

Search for:
- `colors.json`, `tokens.json`, `theme.ts`, `Color.kt`, etc.
- Tailwind config, design system files
- iOS asset catalogs with color sets
- Android `colors.xml`

Capture the brand color palette so icons can use the right tints.

### 4. Typography

Look for:
- Font files in `fonts/` or `assets/fonts/`
- Type scale tokens
- Font usage in UI screenshots

Type weight informs icon stroke weight — icons next to a 1.5pt-stroke type should not use 2.5pt stroke icons.

### 5. Brand assets

Look for:
- `brand/`, `assets/brand/`
- Logo SVG / PNG masters
- `brand-dna.md` (regardless of who or what wrote it — hand-written, sibling project, external tool)
- Style guide PDFs

This feeds Brand DNA extraction (phase 2).

### 6. Design-tool sources

If the project's icons live in a design tool, prefer reading them through the corresponding MCP rather than scraping screenshots:

- Figma file URL or node URL → use Figma MCP (design context, screenshots, variables, components)
- `.pen` file in the project → use Pencil MCP exclusively (`.pen` files are encrypted; `Read`/`Grep` will fail)
- Any other connected design-tool MCP → see [`design-tool-integrations.md`](design-tool-integrations.md) for the contract pattern

State the detected source in the audit response so reviewers know whether the snapshot is tool-backed or screenshot-only.

## UI Snapshot Output

After audit, produce a snapshot the user can review:

```markdown
## Project UI Snapshot

### Existing icon set
- Source: mixed — Material Symbols + 4 custom SVGs
- Sizes: 24dp Material, 20pt custom
- Stroke: Material default (2dp filled, 1.5dp outlined); custom inconsistent (1.25-2.5pt)
- Style: outlined dominant, filled used for active Tab Bar
- Color: tinted via theme; one custom icon has baked-in color

### App tone (from screenshots)
- Sans-serif type, weight 400/600
- Generous whitespace
- Color palette: deep blue primary, off-white background, single accent yellow
- Photography heavy on profile screens

### Icon implementation gaps
- Tab Bar mixes Material outlined with custom filled — inconsistent state pair
- Settings icon is Material gear at 24dp, sits next to custom 20pt Library icon → size mismatch
- No themed (Material You) support

### Brand assets
- brand/primary-symbol.svg (geometric, 1.75pt stroke, round terminals)
- brand/wordmark.svg (geometric sans, custom)
- No brand-dna.md present

### Redesign tolerance estimate
- App has 250k MAU
- Icons not heavily marketed (no icon-focused brand recall)
- Recommendation: adjacent — preserve metaphors, new construction language inherited from logo
```

## Redesign Tolerance Determination

Before generating, decide tolerance:

### Evolutionary
- Existing set has equity (recognized by users)
- Refresh stroke style, optical corrections, state pair
- Keep silhouettes recognizable
- Use when: users would notice a fundamental change

### Adjacent
- Existing set is functional but inconsistent
- Same metaphors (Home is still a house), new construction
- Inherit Brand DNA from logo
- Use when: most icon-system refresh requests fall here

### Reset
- Existing set is generic Material/SF with no brand customization
- Or no existing set
- Full vocabulary + construction defined fresh
- Use when: new product or low icon equity

State the tolerance in the first response. User can override.

## What to NOT Do

- Don't critique the current product as a whole — focus on icon-system specifics
- Don't assume the existing icons need replacing — they may be intentional
- Don't ignore non-icon UI signals (typography, color tone) — they constrain icon choices
- Don't skip audit even if user provides Brand DNA — UI context still matters

## Integration with Brand DNA

If Brand DNA is from logo or an existing `brand-dna.md` (phase 2 mode 1 or 2), audit confirms application context:

- Does Brand DNA's stroke weight match UI typography weight?
- Does Brand DNA's color logic match current theme tokens?
- Do current icons clash with Brand DNA — meaning the refresh is justified?

If conflicts surface, flag them as risks before phase 5 (icon system rules).

## Output Format

The audit output goes into `assets/package-template/reviews/project-ui-snapshot.md` when packaging. Use the same structure for inline output during the workflow.

## Failure Modes

- **No audit, jump to generation** — produces icons that don't match the app's UI tone
- **Audit but ignore findings** — inconsistencies surface in evaluation phase
- **Audit only screenshots, no source files** — misses how icons are technically implemented
- **Critiquing instead of snapshotting** — out of scope; not the skill's job
