# Sources and Authority Order

Icon-system work depends on multiple sources of truth. When they conflict, this file dictates which wins.

## Authority Order

1. **Project audit** — what exists in the user's project
2. **Brand DNA** — from existing `brand-dna.md`, extraction from brand assets, or user-supplied input (see [`brand-dna-input.md`](brand-dna-input.md))
3. **Accessibility constraints** — WCAG 2.2 AA, platform touch-target minima, screen-reader labeling rules (see [`accessibility.md`](accessibility.md)) — non-negotiable
4. **Platform official docs** — Apple HIG, Material Design 3
5. **Recognized icon-system standards** — Material Symbols, SF Symbols (as reference, not as authority over brand)
6. **HCI research** — peer-reviewed studies on icon recognition, search efficiency, accessibility
7. **Inspiration galleries** — Dribbble, Behance, IconScout, etc. (last resort, never authoritative)

When two sources conflict:

- Project truth wins over Brand DNA wins over platform docs wins over standards wins over inspiration
- Exception: accessibility constraints and platform safety constraints (touch targets, contrast minimums, RTL behavior, screen-reader labeling) override every other source including project preference. The skill ships accessible icons or it does not ship.

## Platform Official Sources

### iOS

- Apple Human Interface Guidelines → Tab Bars
- Apple HIG → Icons (general design principles)
- SF Symbols app and SF Symbols spec
- Apple Design Resources Figma libraries

### Android / Material

- Material Design 3 → Components → Navigation Bar
- Material Symbols (icon set) and the Material Symbols spec
- Google Fonts → Material Symbols documentation
- Android Developer docs → drawables, vector assets

### Cross-platform / Generic

- W3C SVG specification (for SVG mastering)
- WCAG 2.2 (for contrast and accessibility)

## Recognized Icon Standards

Use these as **reference**, never as authority over the user's brand:

- **Material Symbols** — Google's icon set, useful for cadence and metaphor reference
- **SF Symbols** — Apple's icon set, useful for iOS conventions
- **Lucide** — open-source, clean construction, good cadence reference
- **Phosphor** — multiple weights, useful for stroke contrast study
- **Tabler** — large coverage, useful for vocabulary expansion
- **Heroicons** — minimal, useful for decision-making about detail budget

Look at how they construct similar icons. Adopt cadence, not specifics.

## HCI Research Watchlist

Studies relevant to icon-set design:

- Iconography in mobile apps and recognition speed (multiple studies, 2010-present)
- Cross-cultural icon comprehension studies (especially gendered figures, hand gestures)
- Color contrast and accessibility (WCAG-aligned research)
- Touch-target size and accuracy (Apple's 44pt and Material's 48dp guidelines have research backing)

For specific studies and updates, see [`live-research.md`](live-research.md).

## Inspiration Galleries

Use only for divergent ideation, never as authoritative source:

- Dribbble icon search
- Behance icon set portfolios
- IconScout, Iconfinder

When inspiration looks great, ask: would this survive at 20pt? Is the construction documented? Does it fit a system, or is it a one-off?

## Source Citation in Responses

When recommending a specific guideline, cite the source:

```
Recommendation: Tab Bar icons at 25pt template image size.
Source: Apple Human Interface Guidelines → Tab Bars (latest spec).
Verified: {{date if recently checked}}
```

Don't claim platform behavior without citing the source. If unsure, run a live research pass before declaring.

## When Live Research Is Mandatory

Run [`live-research.md`](live-research.md) when:

- Starting a new project (specs may have changed)
- The user mentions recent platform features (Material You, iOS 17+ Tab Bar changes, etc.)
- The user asks about themed icons or dynamic color
- Specs in this file or [`platform-icon-specs.md`](platform-icon-specs.md) feel ambiguous or out of date
- Quarterly cadence for any project that's actively maintained

## Failure Modes

- **Citing inspiration as authority** — Dribbble icons may look great and break HIG simultaneously
- **Skipping live research** — Apple HIG and Material 3 update without notice
- **Over-trusting Material/SF** — they're references, not authority over user's brand
- **Ignoring project truth** — the user's existing system has equity even if it looks dated
