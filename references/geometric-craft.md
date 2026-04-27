# Geometric Craft (Hi-end)

Per-icon geometric craft checklist. Run this in workflow phase 9 (hi-end only). Standard tier skips. This file is the runtime checklist; long-form rationale is in [`geometric-craft-guide.md`](geometric-craft-guide.md).

## Pre-Conditions

Before running geometric craft:

- Phase 5 icon system rules are locked
- Phase 7 set is generated
- Phase 8 cross-icon consistency audit has run

If any phase is skipped or incomplete, halt and complete it first.

## Per-Icon Checklist

For each icon, run all checks. Document any deviation.

### 1. Construction grid

- ☐ Icon is built on the documented grid (24/20/16)
- ☐ All anchors land on documented grid increments (1pt, 0.5pt, or 0.25pt as documented)
- ☐ No off-grid corrections without reason

### 2. Optical corrections

- ☐ Diagonal strokes use compensation (3-7% thicker than orthogonal)
- ☐ Circles overshoot square frames by 1-2%
- ☐ Dense negative-space icons scaled up 2-3% to balance against simpler icons
- ☐ Visual centering applied (not geometric centering for directional icons)

### 3. Anchor reduction

- ☐ Path has minimum anchors needed for the shape
- ☐ No redundant anchors on straight segments
- ☐ Curve anchors placed at extrema (0°, 90°, 180°, 270°) when possible

### 4. Tangent continuity

- ☐ G1 tangent continuity at every corner where curves meet
- ☐ G2 (curvature) continuity for hi-end where shape demands it
- ☐ No visible tangent breaks

### 5. Path cleanliness

- ☐ No floating-point artifacts in `d` attribute
- ☐ Coordinates rounded consistently (e.g., 2 decimal places max)
- ☐ Even structure across SVG `d` attributes (helpful for diff and review)
- ☐ No accidental sub-paths

### 6. Pixel alignment

- ☐ Strokes align to pixel grid at target export size
- ☐ 1pt strokes on integer-pixel positions
- ☐ Half-pt strokes (e.g., 1.5pt) centered on pixel boundaries
- ☐ Validated by exporting at target size and zooming 800%+

### 7. Stroke geometry

- ☐ Stroke `linecap` matches set rule (no exceptions)
- ☐ Stroke `linejoin` matches set rule
- ☐ Stroke `miterlimit` set explicitly if using `miter` joins (default `4`)
- ☐ No mixed stroke widths within one icon unless documented contrast pair

### 8. Filled / outlined pair coherence

If both states exist:

- ☐ Filled silhouette = exact contour of outlined construction
- ☐ Internal detail in outlined version maps to negative space in filled (where applicable)
- ☐ Toggling states feels like a state change, not an icon change

## Cross-Icon Checks (After Per-Icon)

After running per-icon, run these set-level checks:

### Stroke optical balance

- ☐ Squint test on the row: no stroke pops out
- ☐ Diagonals across set use the same compensation
- ☐ Internal detail strokes (if used) follow the documented contrast pair

### Visual weight balance

- ☐ Squint test passes
- ☐ Dense icons (gear, settings) simplified vs sparse icons (heart, square)
- ☐ No icon dominates the row

### Optical centering across baseline

- ☐ All icons sit on the same optical baseline
- ☐ Directional icons (play, search) adjusted for visual mass distribution

## Output Format

```markdown
## Geometric Craft Pass

### Per-Icon Corrections
- Home: Anchor reduction (10 → 6), tangent G1 verified
- Search: Diagonal stroke compensation 1.85pt applied to handle, optical center shift +0.5pt right
- Library: Pixel alignment corrected (was 0.7pt off-grid, now on grid), anchor reduction (14 → 10)
- Profile: Optical center shift +0.5pt up, head/shoulder spacing tightened
- Settings: Diagonal compensation 1.85pt on gear teeth, anchor reduction (32 → 24)

### Set-Level Corrections
- Squint test: Settings was 8% denser than rest, simplified gear teeth from 8 to 6
- Stroke optical balance: verified on row, no drift
- Optical baseline: all icons aligned, Profile was 0.5pt low → corrected

### Remaining Risks
- Library at 16pt: bottom shelf line nearly disappears; document 16pt fallback in package
```

## When to Halt Craft Pass

Halt and return to earlier phase if:

- A construction violates Brand DNA (return to phase 2)
- A construction violates icon system rules (return to phase 5)
- Cross-icon consistency drift surfaces (return to phase 8)
- An icon fails the silhouette test even after correction (return to phase 7 — re-generate)

## Tools

- **Vector editor with grid + ruler** (Figma, Illustrator, Affinity, Pencil)
- **SVG inspector** (browser DevTools, VS Code SVG preview)
- **Render at target size** (browser preview, Pencil .pen frame)
- **Squint test** (literal — stand 1m back from screen)

## Failure Modes

- **Skipping pre-conditions** — running craft on incomplete set produces craft on the wrong shapes
- **Per-icon only, no set checks** — set-level drift surfaces in evaluation
- **Optical corrections without measurement** — eyeballing diagonal compensation produces inconsistency
- **Pixel alignment at master size only** — must verify at target export size
- **Tangent breaks tolerated** — G1 minimum is non-negotiable for hi-end
