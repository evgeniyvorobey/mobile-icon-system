# Visual Regression

Use visual regression after contact sheets or platform previews are rendered. The goal is to catch accidental visual changes in icon output that pass structural SVG validation: missing strokes, shifted glyphs, antialiasing drift, unexpected color changes, or contact-sheet layout regressions.

This workflow compares rendered PNG snapshots. It does not replace craft review, accessibility checks, or semantic evaluation.

## When to Use

- After changing renderers, exporters, graders, style packs, or package templates.
- Before releasing a new skill version that changes generated assets.
- When a project has approved baseline contact sheets and wants to guard against silent drift.

Skip this when no approved baseline exists. First generate and approve a baseline; then compare future snapshots against it.

## Snapshot Contract

Store visual baselines in a project package, not in the skill repo by default:

```text
reviews/visual-regression/
  baseline/
    contact-sheet.png
    ios-tab-bar.png
    android-bottom-nav.png
  current/
    contact-sheet.png
    ios-tab-bar.png
    android-bottom-nav.png
  report.json
```

PNG snapshots should be deterministic:

- same viewport size;
- same device scale;
- same light/dark theme;
- same font availability;
- same icon order;
- no timestamps or random content.

## CLI

```bash
python3 scripts/visual_regression_contact_sheet.py \
  reviews/visual-regression/baseline \
  reviews/visual-regression/current \
  --max-diff-ratio 0.003 \
  --max-channel-delta 24 \
  --report-json reviews/visual-regression/report.json
```

The script compares matching `.png` files by relative path. It fails when:

- a current screenshot is missing;
- image dimensions differ;
- the ratio of pixels over the channel-delta threshold exceeds the budget.

Use `--update-baseline` only after human review approves the current screenshots.

## Thresholds

Default tolerances are intentionally small:

- `max-channel-delta`: 24 per RGBA channel, to ignore tiny antialiasing noise.
- `max-diff-ratio`: 0.003, meaning at most 0.3% of pixels may differ materially.

For style packs with intentional softness or blur, document a larger threshold in the project package. Do not increase the global threshold to hide real regressions.

## Failure Triage

1. Open the baseline and current PNGs side by side.
2. Check whether the change is intentional and approved.
3. If intentional, update the baseline and document the reason.
4. If accidental, return to the exporter or SVG master and regenerate.

Visual regression is a tripwire, not the final judge. Human review still decides whether an approved design changed for a good reason.
