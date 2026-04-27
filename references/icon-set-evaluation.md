# Icon Set Evaluation

The 8-dimension matrix for scoring a complete icon set. Use this in workflow step 10. Score the set as a whole, not just individual icons — many icon-set failures are emergent properties (consistency drift, weight imbalance) not present in any single icon.

## The 8 Dimensions

### 1. Small-size legibility

Does each icon read at intended size without a label?

- Test at 20pt (Tab Bar), 24pt (Bottom Nav), and 16pt (inline) as applicable
- Cover the row, point at one icon — can a stranger name it?
- Failure: any icon needs a label to be understood at intended size

**Score**: pass / pass with note / fail

### 2. Brand fit

Does the set reflect the documented Brand DNA?

- Compare against `brand-dna.md` (or extracted DNA): geometric alphabet, stroke language, terminals, corners
- Side-by-side with the logo: does the set feel like the same family?
- Failure: stroke style or geometric language drifts from brand

**Score**: 1-5 (5 = inseparable from logo family)

### 3. Platform fit

Does the set respect platform conventions where required?

- iOS: filled (selected) + outlined (unselected), 25pt template, no baked color
- Android: filled (active) + outlined (inactive), 24dp vector drawable, theme-tintable
- Touch targets accommodated where icons are interactive
- Failure: missing state pair, baked color, undocumented size deviation

**Score**: pass / fail per platform

### 4. Set consistency

Does the set hold together as a family? See [`cross-icon-consistency.md`](cross-icon-consistency.md) for the full audit.

- Stroke weight: uniform (or compensated per documented rule)
- Terminals: same cap + join across set
- Corners: same radius logic
- Visual weight: balanced in row (squint test passes)
- Optical centering: aligned across baseline
- Filled/outlined pairs: share construction
- Failure: drift in any consistency dimension without documented reason

**Score**: 1-5 (5 = no detectable drift)

### 5. Metaphor clarity

Is each icon's meaning unambiguous?

- One icon, one meaning (settings ≠ system, favorites ≠ saves)
- Recognized without explanation by intended audience
- Doesn't conflict with adjacent icons in the set (e.g., bell + envelope both reading as "messages")
- Failure: ambiguous metaphor, conflicting meaning with another icon

**Score**: 1-5 per icon, average for set

### 6. Cliché avoidance

Is the set free of category clichés?

- See [`icon-vocabulary.md`](icon-vocabulary.md) for cliché map
- Compare against top-3 competitors in the category — are metaphors copied?
- Brand-specific metaphors are OK if they pass the legibility test
- Failure: every icon is the obvious choice (= no brand differentiation)

**Score**: 1-5 (5 = differentiated without sacrificing recognition)

### 7. Cross-cultural readability

Will the set work for the intended audience?

- Avoid culturally narrow metaphors (gendered figures, Western objects with no global equivalent)
- For RTL markets: directional icons (back / forward, undo) need RTL variants or symmetric forms
- For non-Latin scripts: avoid Latin-letter glyphs as iconographic elements
- Failure: any icon will confuse meaningful market segment

**Score**: pass / pass with localization note / fail

### 8. State distinction (Tab Bar / Bottom Nav)

Can the user instantly tell active from inactive state?

- Filled (active) vs outlined (inactive) is the standard
- Difference must be readable at target size, not just 1024px master
- Tint color difference alone is not sufficient — silhouette difference required
- Failure: active and inactive icons read the same at 25pt with same tint

**Score**: pass / fail

## Composite Score

Sum the dimensions:

- Pass / fail dimensions: each fail blocks shipping
- 1-5 dimensions: target ≥4.0 average for ship-ready

Output the composite as a table:

```markdown
## Icon Set Evaluation

| Dimension | Score | Notes |
|---|---|---|
| Small-size legibility | pass | 20pt clear, 16pt borderline for Settings |
| Brand fit | 4 | Strong alignment, slight diagonal stroke drift |
| Platform fit (iOS) | pass | All template images, no baked color |
| Platform fit (Android) | pass | Vector drawables, themable |
| Set consistency | 4 | Profile icon visually heavier than rest |
| Metaphor clarity | 4.5 | Library could be confused with Activity |
| Cliché avoidance | 3 | Most metaphors standard; differentiation through stroke |
| Cross-cultural | pass | No gendered figures, no Western-only objects |
| State distinction | pass | Filled vs outlined clearly readable |
| **Composite** | **4.0** | **Ship-ready with two follow-ups** |
```

## Rejection Triggers

Any of these blocks shipping regardless of composite score:

- Any icon fails small-size legibility at intended size
- State pair fails distinction test (Tab Bar / Bottom Nav)
- Brand DNA drift unexplained
- Stroke weight drift unexplained
- Touch target violation on interactive surfaces
- Cultural exclusion not addressed (gendered, RTL-broken)

## Hi-end Additional Dimensions

For hi-end work, add:

### 9. Optical correction quality

- Diagonal stroke compensation applied consistently
- Circle overshoot applied consistently
- Visual centering corrected per icon
- Negative-space density compensation where needed

**Score**: 1-5

### 10. Path cleanliness

- Anchor points minimized (no redundant vertices)
- Tangent continuity G1+ at corners
- No floating-point artifacts
- Even SVG `d` attribute structure across set

**Score**: 1-5

## Evaluation Output Format

When the skill outputs the evaluation, include:

1. The dimension table (above)
2. Per-icon notes for any 1-3 score dimension
3. Top 3 improvement moves in priority order
4. Ship-readiness verdict (ship / ship with follow-ups / re-work needed)

## Failure Modes

- **Scoring icons individually then averaging** — misses set-level failures (drift, weight imbalance)
- **Skipping the squint test** — quantitative checks miss perceptual issues
- **Tolerating a single-icon failure** — one icon failing legibility kills the set's reliability
- **Bumping borderline scores up to ship** — borderline = re-work, not "good enough"
