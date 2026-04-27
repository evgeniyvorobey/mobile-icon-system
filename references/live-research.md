# Live Research

Watchlist for sources whose freshness matters. Run live research at workflow phase 4 (build context) when freshness affects the deliverable. Not every project needs it; this file defines when it's mandatory.

## When Live Research Is Mandatory

Run a research pass when:

- Starting a new project (specs may have changed since last invocation)
- User mentions recent platform features (themed icons, Material You, iOS 17+ behaviors)
- User asks about icon sizes, state requirements, color tinting behavior
- Specs in [`platform-icon-specs.md`](platform-icon-specs.md) feel ambiguous
- Project is actively maintained and 90+ days since last research run

When live research is run, note the date in the response (`Live research run: 2026-04-27`).

## Official Watchlist

Sources to consult during a live research pass:

### Apple

- Apple Human Interface Guidelines → Tab Bars (https://developer.apple.com/design/human-interface-guidelines/tab-bars)
- HIG → App icons (related, for app launcher work — not in scope here, but useful for cross-skill alignment)
- HIG → Color and accessibility
- SF Symbols release notes (each major iOS release ships SF Symbols updates)
- Apple Developer Forums: "Tab Bar" recent threads

### Google / Material

- Material Design 3 → Components → Navigation Bar (https://m3.material.io/components/navigation-bar)
- Material 3 → Icons (https://m3.material.io/styles/icons)
- Google Fonts → Material Symbols release notes
- Material Symbols changelog
- Android Developer docs → vector drawables, themed icons

### Other platforms (if cross-shipping)

- W3C SVG 2 spec (for SVG mastering)
- WCAG 2.2 → 1.4.3 Contrast (Minimum), 2.5.5 Target Size
- React Native, Flutter, SwiftUI icon-related framework changes (release notes)

## What to Capture

During a research pass, capture:

1. Current canonical sizes (pt for iOS, dp for Android)
2. Current state-pair conventions (filled / outlined)
3. Current color/tint behavior (theme tokens, dynamic color)
4. Recent additions or deprecations
5. Any non-obvious behavior (e.g., Material 3 pill background introduction)

Output a research summary:

```markdown
## Live Research — 2026-04-27

### iOS Tab Bar
- Canonical size: 25pt template image (verified)
- States: filled (selected) + outlined (unselected) (verified)
- Color: monochrome, system-tinted (verified)
- Recent: no major changes in iOS 17 / 18

### Android Bottom Nav (Material 3)
- Canonical size: 24dp (verified)
- States: filled (active) + outlined (inactive) (verified)
- Active indicator: pill background, on by default in M3 (verified)
- Recent: themed icon support extended; dynamic color stable

### SF Symbols
- Latest version: 5 (as of last check)
- New symbols added: review the list for relevance to vocabulary

### Material Symbols
- Variable axes: weight, optical size, fill — useful for sets that span sizes
- Coverage: ~3000+ symbols
```

## What NOT to Use

- Inspiration galleries (Dribbble, Behance) — not authority
- Old design articles (>3 years) — likely outdated
- Random Stack Overflow answers — not authoritative
- Marketing pages (unless they cite the spec)

## Refresh Cadence

For an actively maintained project:

- Quarterly: full research pass on Apple HIG + Material 3
- Per-major-release: read iOS / Android release notes for any icon-related changes
- Ad hoc: when user asks about a specific feature

For a one-off project:

- Once at project start
- Note the date; don't claim freshness later

## How to Frame Research in Responses

When live research informs a recommendation, cite:

```
Per Apple HIG (verified 2026-04-27): Tab Bar template images use 25pt with the visual mass at ~20×20pt.
```

When research could not be run (offline, time-pressured), state:

```
Live research not run. Specs from platform-icon-specs.md (last verified: ...). Recommend re-verification before shipping.
```

## Failure Modes

- **Skipping research and hallucinating specs** — iOS Tab Bar size has shifted across versions; do not guess
- **Researching but not citing** — recommendations without source are weak
- **Treating Material Symbols / SF Symbols as authority** — they are reference; HIG and Material 3 docs are authority
- **Cherry-picking sources** — read the platform's spec, not just the parts that agree with the design
