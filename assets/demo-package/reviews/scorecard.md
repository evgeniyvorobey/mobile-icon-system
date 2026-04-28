# Scorecard - Tidepool Tasks

Review scope: five SVG masters in `exports/svg-masters`.
Review date: 2026-04-28
Accessibility tier: WCAG AA

| Dimension | Score | Evidence | Follow-up |
|---|---:|---|---|
| Small-size legibility | B+ | Today pair and Capture read at 16pt; Plan details are stronger at 20pt+. | Check Plan at native Tab Bar size in app context. |
| Brand fit | A- | Rounded cards and dot/check details reflect the Brand DNA. | Keep future icons on the same card grammar. |
| Platform fit | A- | Monochrome `currentColor` masters are suitable for iOS templates and Android tinting. | Convert to platform exports outside this demo. |
| Set consistency | A- | Stroke, radius, and live area are consistent across the five masters. | Document exceptions if future icons need diagonal compensation. |
| Metaphor clarity | B+ | Today and Capture are clear; Plan may read as generic list without label. | Keep labels visible for navigation items. |
| Cliche avoidance | B+ | Avoids literal waves and generic sun/day symbols. | Revisit if the brand becomes more expressive. |
| State distinction | A | Filled and outlined tab states differ by shape mass. | Preserve non-color distinction in platform exports. |
| Accessibility | A- | No text in icons, no baked color, screen-reader labels documented. | Verify contrast in final product themes. |

## Second-Eye Notes

- The set is intentionally conservative; that is appropriate for a utility planning app.
- Plan is the weakest icon because list metaphors are crowded in mobile UI. Its saving trait is the shared rounded card grammar.
- Capture is intentionally an action icon rather than a third tab. Its tray shape prevents the plus from becoming an unbranded generic add icon.

## Result

Pass for demo package. Ready for contact-sheet smoke validation and downstream export experiments.
