# Craft Rubric

Numerical thresholds for icon craft. The skill applies this rubric during phase 7 (variant selection) and phase 8 Pass B (second-eye critique). Each threshold has a citation; rules-of-thumb without published authority are explicitly marked. Do not invent numbers — when this file is silent, mark a finding as "designer judgment" rather than fabricate a threshold.

## How to use this rubric

For each icon being graded:
1. Render or inspect at the target size (default 24pt; verify at 16pt for inline contexts).
2. Walk every section below. Score the icon **A** (meets the cited threshold), **B** (within tolerance band), or **C** (out of band).
3. Any **C** on any axis blocks ship until corrected (workflow phase 8 Pass B loops back to phase 7 for that icon).
4. **B** is acceptable for Standard tier. Hi-end tier requires all-A or documented exceptions.

The rubric is operationalized programmatically in [`scripts/render_and_grade.py`](../scripts/render_and_grade.py) for the measurable axes (alignment, weight, silhouette). The taste axes (intentionality, family resemblance, restraint) require LLM judgment guided by [`aesthetic-principles.md`](aesthetic-principles.md).

## 1. Optical Correction

### 1.1 Circle overshoot vs square keyline
- **A:** circle overshoots its containing square keyline by **2-5%** of keyline height (≈0.5pt at 24pt grid)
- **B:** 1-2% or 5-7%
- **C:** 0% (no compensation) or > 7% (over-corrected, reads as bulge)
- **Source:** Material Design 3 keyline grid (circle keyline 20dp inside 24dp box) — [m3.material.io/styles/icons/designing-icons](https://m3.material.io/styles/icons/designing-icons); Karen Cheng, *Designing Type* (Yale, 2005), pp. 38-42 on round-letter overshoot for type.
- **Why:** the eye reads a circle as smaller than a square of equal bounding box because less area touches the boundary.

### 1.2 Triangle / pointed-shape overshoot
- **A:** triangle overshoots square keyline by **8-12%** of keyline height
- **B:** 6-8% or 12-15%
- **C:** < 6% or > 15%
- **Source:** Material Design 3 keyline (triangle keyline 20dp height inside 24dp box) — [m3.material.io/styles/icons/designing-icons](https://m3.material.io/styles/icons/designing-icons).
- **Why:** triangles concentrate mass toward one vertex; equal bounding boxes leave them visually small and light.

### 1.3 Diagonal stroke compensation vs orthogonal stroke
- **A:** diagonals **6-10%** thicker than orthogonal strokes for outlined icons (e.g., 1.85pt diagonal at 1.75pt orthogonal)
- **B:** 5-6% or 10-12%
- **C:** uniform stroke (0%) when set is hi-end *and* no published rationale; or > 12% (visible thickening)
- **Source:** Cheng, *Designing Type*, pp. 50-55, documents diagonal-stroke thickening of 5-10% in serif and sans-serif typefaces; Adrian Frutiger, *Type Sign Symbol* (1980), same range.
- **Note:** modern monoweight icon systems (Material, Lucide, Phosphor) intentionally use uniform stroke and rely on small-size tolerance. Either approach is acceptable if explicitly chosen and documented in the icon-system rules.

### 1.4 Vertical vs horizontal stroke perception
- **A:** horizontals 3-7% thicker than verticals for outlined non-monoweight systems
- **B:** uniform when documented as a deliberate monoweight choice
- **C:** vertical thicker than horizontal (counter-optical)
- **Source:** Cheng, *Designing Type*, pp. 45-48 (5-7% canonical typographic compensation).

### 1.5 Optical centering offset for top-heavy or directional shapes
- **A:** centroid shifted up by **2-5%** of bounding box height relative to geometric center for top-heavy shapes (e.g., play triangle, house with steep roof)
- **B:** 1-2% or 5-7%
- **C:** geometric center (0%) when shape is clearly top-heavy
- **Source:** Müller-Brockmann, *Grid Systems in Graphic Design* (1981), pp. 24-30; Steve Schoger & Adam Wathan, *Refactoring UI* (2018), Chapter 7 ("Visual Hierarchy").

## 2. Pixel Grid Alignment

> **Important caveat — mathematical-derivation exemption.** The integer-anchor rule below applies to **straight-segment endpoints from M/L/H/V commands** that the designer explicitly placed. It does **not** apply to anchors derived from rotational symmetry, equal angular spacing (e.g., a gear's 8 teeth at 360°/8), √3 / golden-ratio chord geometry (e.g., Lucide bell's clapper at `12 ± √3 = 10.268 / 13.732`), or arc-circumference math. These math-derived endpoints land off the integer grid by construction and are tier-A craft, not sloppiness — the [`assets/references/tier-a/`](../assets/references/tier-a/) corpus is full of them. The programmatic alignment check in [`scripts/grade/alignment.py`](../scripts/grade/alignment.py) calibrates its default threshold (`max_off_grid_ratio_24 = 0.50`) against the corpus to avoid false positives on math-derived anchors. Use `--strict` (threshold drops to 0.05) only when auditing icons known to be hand-snapped to integer grid.

### 2.1 24×24 grid (manual designer-placed anchors)
- **A:** all M/L/H/V endpoint coordinates on integers; only curve-handle anchors and math-derived endpoints may use **non-integer** values
- **B:** ≤2 anchors at 0.5 on a non-curve segment (corner anchors), no math-derivation exemption invoked
- **C:** any non-curve, non-derived anchor at 0.25 or other sub-grid value with no documentation of intent
- **Source:** Material Symbols specification ([fonts.google.com/icons](https://fonts.google.com/icons)); Lucide design guide [lucide.dev/guide/design/icon-design-guide](https://lucide.dev/guide/design/icon-design-guide); Phosphor contribution guide [github.com/phosphor-icons/core](https://github.com/phosphor-icons/core).

### 2.2 20×20 grid
- **A:** integers only; no decimals at any anchor
- **B:** 0.5 only at curve handles, not at corners
- **C:** any sub-pixel anchor at corner or terminal
- **Source:** Heroicons "mini" 20×20 set published source SVGs ([heroicons.com](https://heroicons.com)).

### 2.3 16×16 grid
- **A:** integers only; redraw shape from scratch rather than scaling 24×24 down
- **B:** never — 16×16 has no B tier
- **C:** any decimal coordinate, or scaled-down 24×24 path
- **Source:** Heroicons "micro" 16×16 published source SVGs; W3C SVG 1.1 §7.10 (sub-pixel coordinate behavior).
- **Why:** at 16×16 a 0.5 offset is an entire half-pixel; rasterization becomes unpredictable.

### 2.4 Stroke widths that align to pixel rows at @1x and @2x
- **A:** **1pt, 1.5pt, 2pt** (clean alignment at both densities)
- **B:** other half-integer values when icon-system rule explicitly requires
- **C:** **1.25pt, 1.75pt** (sub-pixel rows at both @1x and @2x)
- **Source:** Apple, *SF Symbols 5 Release Notes* (2024); W3C SVG 1.1 §11.4 ("stroke is centered on the path").

### 2.5 1pt stroke crisp-rendering offset
- **A:** 1pt horizontal/vertical strokes positioned at **integer + 0.5** (so the centerline sits on a half-pixel and edges land on whole pixels at @1x)
- **B:** integer position with stroke rounded to even pt value (avoids sub-pixel issue differently)
- **C:** 1pt stroke at integer position (produces 0.5pt anti-aliased blur on each edge)
- **Source:** W3C SVG 1.1 §11.4; Apple, *Drawing and Printing Guide for iOS*.

## 3. Anchor Point Economy

### 3.1 Anchor count by icon complexity
Observed budgets from inspecting Phosphor (regular), Lucide, Material Symbols (rounded), Heroicons (outline 24):

- **Simple icons** (Home, Bell, Heart, Circle): A ≤ 12, B 12-16, C > 16
- **Medium icons** (Settings, Camera, User, Search): A ≤ 20, B 20-30, C > 30
- **Complex icons** (Calendar with detail, Compose, Map pin with shadow): A ≤ 40, B 40-60, C > 60

- **Source:** Direct source-SVG inspection of public icon repositories. Lucide's design guide explicitly states "use as few nodes as possible" ([lucide.dev/guide/design/icon-design-guide](https://lucide.dev/guide/design/icon-design-guide)). Phosphor contribution guide enforces the same.
- **Why:** more anchors than necessary expose the path to inconsistency, make manual correction harder, and rarely improve readability at 20pt.

### 3.2 Bezier minimums per primitive
The skill must respect the analytical minimum anchors needed for each primitive. Exceeding these is acceptable; falling below them means the curve is mathematically incomplete.

- **Circle:** 4 cubic-Bezier anchors (canonical, with handles at 0.5523 × radius — see 5.2)
- **Rounded square:** 8 anchors (4 corners × 2 handles each)
- **Arc 90°:** 2 anchors with cubic handles
- **S-curve:** 3 anchors (start, inflection, end; handle inversion at inflection)
- **Source:** Adobe Illustrator official Pen tool documentation; Tony DeRose, *Composing Bézier Simplexes* (Pixar Technical Memo, 1988).

### 3.3 Cusp ratio
- **A:** cusp (corner) anchors ≤ **30%** of total anchors for organic shapes; up to 80% for explicitly geometric shapes (rectangles, polygons)
- **B:** 30-40% for organic shapes
- **C:** > 40% cusps in an icon meant to read as organic (over-cusping)
- **Source:** designer rule of thumb (uncited; enforced by Phosphor / Lucide submission review per their public review threads but no published numerical threshold). **TODO:** verify against Adobe Type Department guidance if published.

## 4. Stroke Uniformity

### 4.1 Within-icon stroke variation
- **A:** **0%** variation for monoweight systems; up to **2%** variation when documented as deliberate (e.g., diagonal compensation per 1.3)
- **B:** 2-5% variation when documented
- **C:** any undocumented variation, or > 5% even when documented
- **Source:** Phosphor, Lucide, Material Symbols all enforce strict monoweight at the published level; Material Symbols' weight axis (Variable Fonts documentation) parameterizes weight across the set, never within an icon.

### 4.2 Cross-icon stroke consistency (numerical vs optical)
- **A:** numerically equal (0% deviation between icons in the same set at the same weight)
- **B:** up to 5% per-icon optical adjustment, with documented rationale
- **C:** > 5% deviation, or any undocumented deviation
- **Source:** Apple HIG SF Symbols overview (sets are optically tuned); Emil Kowalski on icon design [emilkowal.ski/](https://emilkowal.ski/).
- **Note:** "optical equality trumps numerical equality" is practitioner consensus, but ship default to numerical equality and only deviate with documentation.

### 4.3 Round-terminal perpendicularity
- **A:** terminal axis perpendicular to stroke direction within **±2°** at the terminal end
- **B:** ±2-5°
- **C:** > 5° or visible asymmetric terminal
- **Source:** designer rule of thumb (uncited); W3C SVG §11.4 defines `stroke-linecap: round` as a half-circle of stroke-width diameter, which is geometrically perpendicular by definition. The threshold applies to manually-drawn or path-built terminals that don't use `stroke-linecap`. **TODO:** locate published source.

## 5. Curve Quality

### 5.1 Continuity tier
- **A for icons rendered ≤ 64pt:** G1 (tangent continuous) at every smooth junction
- **A for icons rendered > 64pt:** G2 (curvature continuous) at every smooth junction
- **A for typography or marks at billboard scale:** G3
- **B:** G1 for icons up to ~100pt (visible kink risk increasing)
- **C:** G0 (visible position-only join with kink) on any "smooth" curve
- **Source:** Tony DeRose, *Composing Bézier Simplexes* (Pixar, 1988); Karen Cheng, *Designing Type* (2005), Chapter 3.
- **Practical:** for mobile UI icons rendered at 16-48pt, G1 is sufficient. Move to G2 only when the icon will appear at ≥64pt (some action button surfaces, splash imagery).

### 5.2 Bezier handle ratio for circular approximation
- **A:** handle length = **0.5523 × radius** (analytical kappa value; max radial error ≈ 0.0273%)
- **B:** 0.55 × radius (rounded; ≈ 0.04% error — invisible)
- **C:** any other ratio (introduces visible flattening or bulging)
- **Source:** Stanislav Mossakowski (1987); Pomax, *A Primer on Bézier Curves* [pomax.github.io/bezierinfo](https://pomax.github.io/bezierinfo/); Adobe Illustrator's Ellipse tool uses this internally.

## 6. Negative Space

See [`negative-space.md`](negative-space.md) for the full guidance. Numerical thresholds:

### 6.1 Trapped space minimum at 24pt grid
- **A:** ≥ **2pt** (2 grid units) gap between distinct filled regions
- **B:** 1-2pt
- **C:** < 1pt (regions merge perceptually after anti-aliasing at @1x)
- **Source:** Material Symbols design specification 2dp minimum [m3.material.io/styles/icons](https://m3.material.io/styles/icons); Phosphor contribution guide.

### 6.2 Counter-form area minimum
- **A:** ≥ **35%** of bounding box remains "empty" (counter-form area / bounding box area)
- **B:** 30-35%
- **C:** < 30% (icon reads as blob at small render sizes)
- **Source:** designer rule of thumb informed by Tschichold (*Asymmetric Typography*) on counter-form ≈ 1/3 of cap-height bounding box for legible sans-serifs. **TODO:** find icon-specific published source.

### 6.3 Density rhythm
- **A:** scanline pixel-density variation (per row and per column) ≤ **30%** of the icon's mean density
- **B:** 30-40%
- **C:** > 40%
- **Source:** designer rule of thumb (uncited); Müller-Brockmann discusses density rhythm abstractly. **TODO:** derive empirically from the calibration corpus.

## 7. Set-Level Balance

### 7.1 Visual weight variance across the set
- **A:** perceived ink mass variance ≤ **10%** across the set (max-min filled-pixel ratio)
- **B:** 10-15%
- **C:** > 15% — one icon dominates or recedes
- **Source:** designer rule of thumb informed by Apple HIG ("appear visually balanced") and practitioner consensus (Emil Kowalski, Robin Stewart). **TODO:** find a published numerical source.
- **Operationalized:** [`scripts/render_and_grade.py`](../scripts/render_and_grade.py) computes filled-pixel ratio per icon at 24pt grayscale and reports max-min variance.

### 7.2 Bounding-box utilization variance
- **A:** each icon utilizes **80-95%** of its bounding box; cross-set variance ≤ **10%**
- **B:** 75-80% utilization or 10-15% variance
- **C:** < 75% or > 95% utilization, or > 15% variance
- **Source:** Material Symbols keyline grid (square 18dp, circle 20dp, vertical-rect 16×20dp, horizontal-rect 20×16dp inside 24dp box) [m3.material.io/styles/icons/designing-icons](https://m3.material.io/styles/icons/designing-icons); SF Symbols similar keyline structure.

### 7.3 Selected vs unselected state contrast (for state pairs)
- **A:** state pair differs by **≥ 1.5:1** contrast against the backdrop, both states meet **3:1** non-text contrast against background
- **B:** 1.3-1.5:1 differentiation, both states meet 3:1
- **C:** < 1.3:1 differentiation, or either state below 3:1
- **Source:** WCAG 2.2 §1.4.11 [w3.org/WAI/WCAG22/Understanding/non-text-contrast.html](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html); also see [`accessibility.md`](accessibility.md).

## 8. Squint / Blur Tests

### 8.1 Identifiability under blur
- **A:** icon remains identifiable at **σ = 1.0px** Gaussian blur (≈4% of 24pt linear extent)
- **B:** identifiable at σ = 0.5px but degrades at σ = 1.0
- **C:** loses identity at σ ≤ 0.5px
- **Source:** practitioner consensus (uncited published threshold); Robin Stewart Config 2022 talk references the squint test without a numerical blur value. **TODO:** verify or refine empirically against the calibration corpus.

### 8.2 Silhouette connected-component count
After binarizing at 50% threshold:

- **A for filled style:** ≤ **2** connected components
- **A for outlined style:** ≤ **4** connected components
- **B:** one above the A threshold
- **C:** > A threshold + 1 (icon fragments under low resolution or low vision)
- **Source:** practitioner consensus; Helena Zhang's Phosphor design rationale at Figma Config 2023. **TODO:** verify via published source.
- **Operationalized:** [`scripts/render_and_grade.py`](../scripts/render_and_grade.py).

## 9. Auditable axes summary

For phase 8 Pass B (second-eye critique), the LLM must score every icon on every axis below. Programmatic axes are checked by [`scripts/render_and_grade.py`](../scripts/render_and_grade.py); judgment axes need LLM application of the rubric.

| Axis | Programmatic | Judgment | Rubric section |
|---|---|---|---|
| Optical correction | partial | yes | §1 |
| Pixel grid alignment | yes | no | §2 |
| Anchor economy | yes | yes (intent) | §3 |
| Stroke uniformity | yes | no | §4 |
| Curve quality | partial | yes | §5 |
| Negative space (numbers) | yes | yes (rhythm) | §6 |
| Set-level balance | yes | no | §7 |
| Squint / silhouette | yes | yes | §8 |
| Anti-example similarity | yes (v0.4+) | yes | §10.1 |
| Color-only state distinction | yes (v0.4+) | yes | §10.2 |
| Family resemblance | partial (via §10.1) | yes | see [`aesthetic-principles.md`](aesthetic-principles.md) |
| Restraint / one-ornament | no | yes | see [`aesthetic-principles.md`](aesthetic-principles.md) |
| Intentionality | partial (via §10.1) | yes | see [`aesthetic-principles.md`](aesthetic-principles.md) |
| Metaphor priority | partial (via §10.1) | yes | see [`icon-vocabulary.md`](icon-vocabulary.md) |

## 10. Semantic failures (programmatic)

Added in v0.4. These are the **first programmatic checks** for what §9's table previously listed as "LLM-judgment only" axes (family resemblance, intentionality, metaphor priority). They work by leveraging the hand-curated tier-C anti-example corpus as ground truth: if a candidate icon resembles a documented failure mode closely enough, that resemblance is itself the diagnosis.

Both checks are **hard-fail by default** — they catch unambiguous failures rather than borderline craft questions, so warn-only would let real failure modes through.

### 10.1 Anti-example similarity

- **A:** pHash Hamming distance to every tier-C anti-example > 12 at hash_size=8 (default)
- **B (warn):** distance ≤ 12 (suspicious resemblance to a documented failure mode — review against the matching anti-example's `.notes.md`)
- **C (hard-fail):** distance ≤ 5 (near-clone of a documented failure mode — the LLM has reproduced an icon known to fail; regenerate with the matching `.notes.md` Failure-mode section read aloud as a constraint)
- **Source:** Hamming-distance thresholds calibrated empirically against the tier-A and tier-C corpora — clean Lucide / Phosphor / Tabler reference icons land at distance ≥ 22 from every tier-C anti-example, while exact reproductions land at distance 0.
- **Operationalized:** [`scripts/grade/anti_example_similarity.py`](../scripts/grade/anti_example_similarity.py); CLI flag `--anti-example-corpus PATH` overrides or extends the default tier-C corpus.
- **Why hard-fail:** the failure modes documented in [`assets/references/tier-c/`](../assets/references/tier-c/) (gendered profile silhouette, 12-tooth gear blob, color-only state indicator, over-detailed home/calendar) are not borderline craft — they're known regressions. If the LLM produces a pHash near-clone of one, it has reproduced the exact mistake the anti-example was designed to catch.
- **Note on rendering:** the check composites RGBA renders over a white background before hashing, so SVGs that use `stroke="currentColor"` (default fill `none`) hash to their visible form rather than collapsing to all-zero.
- **Powerful with the corpus, not the code:** when v0.5 adds more tier-C exemplars (over-rendered envelope, gendered shopping bag, color-only chip badges), this check automatically becomes more discerning — no code change needed.

### 10.2 Color-only state distinction

- **A:** state pair shape difference ≥ 10% of pixels (color-blind, after PIL `convert('L')` and 50% binarization)
- **B (warn):** shape difference 5-10% — borderline, review manually
- **C (hard-fail):** color difference ≥ 10% AND shape difference < 5% — the pair LOOKS different in color but is the same shape
- **Source:** WCAG 2.2 §1.4.1 (Use of Color), Microsoft Forced Colors mode documentation, deuteranopia / protanopia simulation literature. The 10% color floor distinguishes this check from "the pair is identical" (which the existing pair-distinction check at [`scripts/grade/pair.py`](../scripts/grade/pair.py) already catches).
- **Operationalized:** [`scripts/grade/color_only_state.py`](../scripts/grade/color_only_state.py); runs automatically on every detected `_filled` / `_outlined` pair.
- **Why hard-fail:** a pair that survives only via color fails Forced Colors mode (the OS overrides the color), is indistinguishable under deuteranopia/protanopia, and conveys no semantic difference to a screen reader (the SVGs are byte-identical except for one attribute). This is an accessibility regression, not a craft preference. See [`accessibility.md`](accessibility.md) and the tier-C exemplar [`tier-c/notification-color-state.svg`](../assets/references/tier-c/notification-color-state.svg).
- **Algorithm note:** the check uses the full 4-channel RGBA delta for the color-aware diff (so `fill="red"` vs `fill="blue"` registers as a real difference) and PIL's `convert('L')` for the color-blind diff (so `fill="red"` vs `fill="black"` collapses to the same shape).

## Sources bibliography

**Authoritative tier:**
- Apple Human Interface Guidelines — *Icons*, *SF Symbols overview*, *Tab Bars*: [developer.apple.com/design/human-interface-guidelines/icons](https://developer.apple.com/design/human-interface-guidelines/icons)
- Apple — *SF Symbols 5 Release Notes* (2024)
- Material Design 3 — *Designing icons*: [m3.material.io/styles/icons/designing-icons](https://m3.material.io/styles/icons/designing-icons)
- Google Fonts — Material Symbols documentation: [fonts.google.com/icons](https://fonts.google.com/icons)
- W3C SVG 1.1 Specification: [w3.org/TR/SVG11](https://www.w3.org/TR/SVG11/) (especially §7.10, §11.4)
- W3C WCAG 2.2 §1.4.11 (Non-text Contrast): [w3.org/WAI/WCAG22/Understanding/non-text-contrast.html](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)
- Adobe Illustrator User Guide — Pen tool best practices

**Practitioner tier:**
- Phosphor Icons design rationale (Helena Zhang): [phosphoricons.com](https://phosphoricons.com)
- Lucide design guide: [lucide.dev/guide/design/icon-design-guide](https://lucide.dev/guide/design/icon-design-guide)
- Heroicons (Tailwind Labs): [heroicons.com](https://heroicons.com)
- Emil Kowalski on icon design: [emilkowal.ski](https://emilkowal.ski/)
- Steve Schoger & Adam Wathan, *Refactoring UI* (2018)
- Pomax, *A Primer on Bézier Curves*: [pomax.github.io/bezierinfo](https://pomax.github.io/bezierinfo/)

**Academic / canonical:**
- Karen Cheng, *Designing Type* (Yale University Press, 2005, 2nd ed. 2020)
- Josef Müller-Brockmann, *Grid Systems in Graphic Design* (1981)
- Massimo Vignelli, *The Vignelli Canon* (2010)
- Jan Tschichold, *Treasury of Alphabets and Lettering* (1952), *Asymmetric Typography*
- Adrian Frutiger, *Type Sign Symbol* (1980)
- Tony DeRose, *Composing Bézier Simplexes* (Pixar Technical Memo, 1988)

## Open TODOs

The following thresholds are widely practiced but lack published authoritative sources. They should be refined empirically against the calibration corpus once it is built, or by locating a citation.

1. **§3.3** Cusp ratio threshold for organic shapes
2. **§4.3** Round-terminal perpendicularity tolerance
3. **§6.2** Counter-form area minimum (icon-specific source)
4. **§6.3** Density rhythm scanline variance
5. **§7.1** Visual weight variance across set (published number)
6. **§8.1** Identifiability blur radius (published number)
7. **§8.2** Silhouette connected-component count (published number)

When the calibration corpus is in place, [`scripts/render_and_grade.py`](../scripts/render_and_grade.py) should run these measurements over the tier-A reference set; the median value across the corpus becomes the empirical baseline for each TODO.
