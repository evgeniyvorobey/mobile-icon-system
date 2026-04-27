# Cross-Icon Consistency

Rules for keeping a set of icons feeling like a family. Stroke weights drift, terminals vary, and visual weight imbalances are the most common reasons icon sets feel "off" even when individual icons are well-drawn. This file is the audit checklist for the cross-icon consistency phase (workflow step 8).

## The Six Consistency Dimensions

Every icon set must be consistent across these six dimensions. Document any deviations with explicit reason.

### 1. Stroke Weight

- All icons share the same numeric stroke weight (e.g., 1.75pt at 24px grid)
- Diagonals use the documented optical compensation (e.g., 1.85pt)
- Internal detail strokes use the documented secondary weight (e.g., 1pt) only where Brand DNA permits
- No icon has a "slightly thicker" stroke for emphasis — emphasis comes from filled state, not weight drift

### 2. Terminal Style

- All stroke endings use the same SVG cap style (`butt` / `round` / `square`)
- All joins use the same join style (`miter` / `round` / `bevel`)
- No mixing — even one round-capped icon in a square-capped set breaks the family feeling

### 3. Corner Radius

- Outer corners use a single radius value or scaled progression (e.g., 2pt for major, 1pt for minor)
- Inner corners follow a documented rule (e.g., always 0, always match outer, always half outer)
- Curve quality: G1 tangent continuity minimum at every corner
- No mixing of sharp + rounded corners on icons of similar topology without reason

### 4. Visual Weight

The hardest dimension. Visual weight is the perceived "ink density" of an icon. A set is balanced when no icon dominates or recedes when viewed in a row.

- Lay out all icons at target size in one row
- Squint test — does anything pop or fade?
- Filled icons read heavier than outlined; if mixing, balance with size or stroke weight
- Dense detail (e.g., gear with many teeth) reads heavier than sparse (e.g., circle); compensate by simplifying

Visual weight is balanced when the row has even rhythm. This is a perceptual judgment, not a numeric one.

### 5. Optical Centering

- Each icon visually centered in its bounding box (geometric centering ≠ optical centering)
- Icons with directional bias (e.g., play triangle, magnifying glass with handle) need explicit optical adjustment
- Cross-icon: optical centers should align across the row when icons sit on the same baseline

### 6. Filled / Outlined Pair Construction

When the set includes both states (Tab Bar standard):

- Filled and outlined share the **same silhouette** — outlined is not a smaller, simpler version
- Filled fill respects the same construction grid
- Outlined stroke follows the contour of the filled silhouette + internal detail strokes
- Switching between states should never feel like a different icon

## Audit Procedure

Run this audit after generating the set, before evaluation:

### Step 1: Stroke audit

```
For each icon:
  - Inspect SVG: extract all stroke-width values
  - Verify: all values match documented set rules
  - Verify: diagonal strokes use compensation if documented
  - Flag any deviation
```

### Step 2: Terminal + join audit

```
For each icon:
  - Inspect SVG: extract stroke-linecap, stroke-linejoin
  - Verify: matches documented terminal style
  - Flag any deviation
```

### Step 3: Corner radius audit

```
For each icon:
  - Identify all corners (outer + inner)
  - Measure radius
  - Verify: matches documented corner rule
  - Flag any deviation
```

### Step 4: Visual weight audit (squint test)

```
- Render all icons at target size in one horizontal row
- Stand 1m back from screen, squint
- Note any icon that pops out or recedes
- Adjust dense icons (simplify), light icons (add structure or thicken stroke per documented rule)
```

### Step 5: Optical centering audit

```
For each icon:
  - Compute bounding box of visible mass
  - Compare to grid bounding box
  - Adjust position if needed (max ±1pt at 24px grid)
```

### Step 6: State-pair audit (Tab Bar)

```
For each icon:
  - Compare filled and outlined silhouettes
  - Verify: same outer contour
  - Verify: outlined doesn't simplify the filled topology
  - Toggle rapidly between states — should feel like state change, not icon change
```

## Audit Output Format

Output the audit as a table:

```markdown
| Icon | Stroke | Terminal | Corner | Weight | Centering | State pair | Action |
|---|---|---|---|---|---|---|---|
| Home | ✓ 1.75pt | ✓ round | ✓ 2pt | ✓ | ✓ | ✓ | none |
| Search | ✓ 1.75pt | ✓ round | ✓ 2pt | heavy | ✓ | ✓ | reduce handle thickness |
| Library | ✓ 1.75pt | ✓ round | ✓ 2pt | ✓ | ✗ off-center | ✓ | shift right 1pt |
| Profile | ✓ 1.75pt | ✓ round | ✓ 2pt | light | ✓ | ✓ | tighten head/shoulder spacing |
| Settings | ✗ 1.5pt diagonal | ✓ round | ✓ 2pt | ✓ | ✓ | ✓ | thicken diagonals to 1.85pt |
```

Then list corrections in priority order.

## Tolerances

These are the maximum tolerable deviations before re-work is required:

- Stroke weight: 0pt deviation (match exactly, except documented diagonal compensation)
- Terminal/join: 0 deviation
- Corner radius: ±0.25pt at 24px grid
- Visual weight: subjective; if 2+ reviewers flag the same icon as outlier, re-work
- Optical centering: ±0.5pt at 24px grid

## Failure Modes

- **Auditing one icon at a time** — consistency is a set-level property; must compare across the row
- **Tolerating drift "for variety"** — variety in icon sets is achieved through metaphor and topology, not stroke variation
- **Ignoring filled/outlined pair coherence** — the most common reason Tab Bar icons feel cheap
- **Geometric centering instead of optical centering** — directional icons always need optical adjustment
- **Skipping the squint test** — quantitative checks miss perceptual imbalance
