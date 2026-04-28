# Rationale - Tidepool Tasks

Project: Tidepool Tasks
Owner: Demo Package
Date: 2026-04-28
Skill version: mobile-icon-system v0.6.0

## The Brief

Create a compact, brand-coherent sample package for a calm mobile planning app. The package must demonstrate the skill workflow without becoming a full production icon library.

## Brand DNA Inheritance

| Brand DNA dimension | Decision | Effect on icons |
|---|---|---|
| Geometric alphabet | Rounded cards, small dots, check/tray details | The icons share a soft task-card grammar. |
| Stroke language | 1.75pt round outline | Outlined states stay readable at 20pt. |
| Terminal style | Round caps and joins | Strokes feel consistent with the calm app tone. |
| Corner treatment | 2.5pt outer radius | Tab icons read as related siblings. |
| Color logic | Monochrome `currentColor` masters | Product can tint per platform state. |
| Optical correction | Checks and plus mark lifted slightly | Directional details do not sag in nav surfaces. |

## Alternatives Considered

### Literal Tide Motif

- Character: waves, ripples, shells.
- Why rejected: it made the brand name literal and reduced task clarity.

### Generic Utility Set

- Character: standard calendar, list, plus with no shared card grammar.
- Why rejected: it would not demonstrate Brand DNA inheritance or cross-icon consistency.

## Why The Chosen Direction Wins

The selected direction keeps each metaphor familiar while giving every glyph the same rounded card and compact-detail rhythm. Active and inactive navigation states differ by mass, not just color, which makes the demo useful for accessibility review.

## Risks Accepted

- The filled Plan icon has dense internal rhythm at 16pt. Mitigation: use it only in labeled navigation and validate with the contact sheet before platform export.
- This package does not include iOS PDF or Android vector drawable exports. Mitigation: SVG masters and rules are sufficient for the demo smoke test.

## Open Questions For Future Iteration

- Should disabled action icons be separate assets or product-tinted states?
- Should a larger package include status icons for sync, overdue, and completed tasks?

## Approvals

- Designed by: Generated demo
- Brand approved by: Not applicable
- Engineering approved by: Not applicable
- Date final: 2026-04-28
