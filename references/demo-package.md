# Demo Package

`assets/demo-package/` is a compact generated example package for the fictional Tidepool Tasks mobile app. It demonstrates the skill's end-to-end flow without shipping a large icon library.

## What It Demonstrates

- Brand DNA translated into grid, stroke, terminal, corner, color, and accessibility rules.
- Vocabulary decisions for a small app surface: two navigation concepts and one action.
- Selected SVG masters using the locked rules.
- A review scorecard that records strengths, weak spots, and follow-up checks.
- Package notes that separate production-ready demo assets from omitted platform exports.

## File Map

```text
assets/demo-package/
├── README.md
├── brand-dna.md
├── system-rules.md
├── vocabulary.md
├── package-notes.md
├── selected/
│   └── rationale.md
├── reviews/
│   └── scorecard.md
└── exports/
    └── svg-masters/
        ├── ic_action_capture.svg
        ├── ic_tab_plan_filled.svg
        ├── ic_tab_plan_outlined.svg
        ├── ic_tab_today_filled.svg
        └── ic_tab_today_outlined.svg
```

## Validation

Run:

```bash
python3 scripts/smoke_test_demo_package.py
```

The smoke test validates:

- Expected package files exist.
- No unresolved double-brace placeholder tokens remain.
- SVG masters parse as XML and use the 24 by 24 grid.
- SVG masters do not reference external raster or remote assets.
- `scripts/render_icon_contact_sheet.py` can render the demo SVGs into a temporary contact sheet.

## Limits

The demo package does not include iOS PDF exports, Android vector drawable XML, motion deliverables, or a full production vocabulary. Those omissions are deliberate so the package stays small enough to live in the repository as an example.
