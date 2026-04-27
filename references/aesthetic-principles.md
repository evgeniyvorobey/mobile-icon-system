# Aesthetic Principles

## Why this exists

A correct icon is one that reads. A *beautiful* icon is one that reads, belongs to its set, and rewards a second look. The skill can produce correct output mechanically — clip a magnifying glass to a grid and you have an icon — but correctness alone is what makes stock icon sets feel interchangeable. Beauty in icon systems is not decoration; it is the residue of disciplined refusal. Massimo Vignelli's *The Vignelli Canon* (Lars Müller Publishers, 2010; freely distributed PDF on vignelli.com) opens with the claim "design is one" — the same intelligence that governs a logotype governs an icon, a poster, a chair. Dieter Rams's tenth principle ("Good design is as little design as possible," 1980s, distilled from his Braun-era talks and published in countless secondary sources) makes the same demand on the designer: subtract until what remains has earned its place.

This file is the constraint set that prevents the skill from producing competent-but-anonymous output. Without it, even a technically clean icon will look like every other clean icon. Each principle below is auditable from an SVG by an LLM that knows what to look for; each is anchored to a named authority rather than to taste.

## Core principles

### 1. Restraint over expressiveness
**Principle.** Use the fewest primitives, weights, and ornaments that express the metaphor.
**Rationale.** Vignelli, *The Vignelli Canon*, p. 56 ("Discipline"): "Discipline is a set of self-imposed rules… Without discipline there is no design." Rams, principle 10: "less, but better." The icon set is a vocabulary; every additional primitive dilutes the others.
**Application.** Restrict each icon to ≤ 4 primitive shapes (line, arc, rectangle, circle). Restrict the whole set to a single stroke weight unless duotone is the declared style. Refuse decorative serifs, hatch fills, or "designer" flourishes that do not carry meaning.
**Anti-example.** A bell icon with a clapper, motion lines, two rings, *and* a gradient body. Four signs of "ringing" where one would do.

### 2. Rhythm over symmetry
**Principle.** Repeated intervals organize a set more powerfully than mirror symmetry organizes a single icon.
**Rationale.** Müller-Brockmann, *Grid Systems in Graphic Design*, ch. 4: rhythm — the consistent return of an interval — is what unifies a page of disparate elements. Translated to icons: a shared corner radius, a shared stroke terminal, a shared inner padding *across the set* matters more than left-right mirror balance *within an icon*.
**Application.** Define and enforce three rhythmic intervals system-wide: stroke weight, corner radius, optical padding. Audit each icon for compliance with these intervals before auditing its internal symmetry.
**Anti-example.** Twenty perfectly symmetric icons whose corner radii drift between 1pt, 1.5pt, and 2pt. The symmetry is wasted; the rhythm is broken.

### 3. Intentional asymmetry
**Principle.** Perfect symmetry reads as stock; controlled asymmetry reads as alive.
**Rationale.** Tschichold, *The New Typography* (1928, trans. McLean, UC Press 1995), argued throughout for asymmetric composition as the modern alternative to centered Beaux-Arts symmetry — asymmetry signals a designer was present. Arnheim, *Art and Visual Perception* (1954), notes that the eye reads dynamic balance as more "alive" than static balance.
**Application.** Where the metaphor permits, offset by 0.5–1pt. A bell with the clapper slightly off-axis; a folder with a tab on one side only; a chevron whose two strokes are a hair different in length to compensate optically.
**Anti-example.** A perfectly bilateral magnifying glass with the handle dead-center on the lens axis. Correct, lifeless.

### 4. Weight perception over weight measurement
**Principle.** What *looks* balanced beats what *measures* balanced.
**Rationale.** The optical-adjustment tradition is older than digital design — Cheng documents it in *Designing Type* (Yale, 2005, ch. 3): a circle drawn to the same height as a square reads smaller and must overshoot the baseline. The same is true of icons: a triangular play button must be drawn larger than the square stop button beside it to feel equal.
**Application.** Overshoot circles and triangles 2–4% beyond the bounding box of squares. Shift visually heavy elements (large solid masses) opposite to centroid to compensate. Trust the eye over the ruler.
**Anti-example.** A triangular play button identical in bounding-box to a square stop button. Measured equal, perceived smaller, feels recessive.

### 5. The one-ornament rule
**Principle.** One element per icon may break the system; that element is the icon's signature.
**Rationale.** This is the typographic *crit* of the "italic flourish" — the capital "Q" in Garamond's tail, the descender of a "y." Robert Bringhurst, *The Elements of Typographic Style* (Hartley & Marks, 4th ed. 2013, §3.2), describes how a single departure from system rules establishes character. In icon sets: the rounded corner where everything else is sharp, the open terminal where everything else closes.
**Application.** Choose one signature deviation that recurs across the set — e.g., all stroke endcaps are square *except* the bell's clapper, which is rounded. Apply it consistently; never twice per icon.
**Anti-example.** Every icon in the set has a different "personality move." The set has no signature; it has noise.

### 6. Quiet over loud
**Principle.** Restrict color, weight variation, and contrast. Luxury is restraint.
**Rationale.** Wathan & Schoger, *Refactoring UI* (self-published, 2018), ch. "Color": "Don't design with hex codes." Their entire color chapter argues for tight, deliberate palettes; their typography chapter argues for one or two weights. Apply this to icons: a set with eight stroke weights, three fills, and four colors is loud. A set with one weight, one fill rule, and the option of one accent is quiet — and quiet is what users perceive as premium.
**Application.** Default to monochrome. If duotone is required, restrict to two values and use them consistently across the set (e.g., 100% for primary mass, 24% for secondary). Never introduce an accent color into a single icon for emphasis.
**Anti-example.** A toolbar where the "delete" icon is red, the "save" is green, the rest are black. Color compensating for weak silhouette.

### 7. Construction visible at 200% zoom
**Principle.** Zoom in to 200%. The construction logic should still be legible.
**Rationale.** Phosphor's design notes ([phosphoricons.com](https://phosphoricons.com) / GitHub) and Lucide's contributor guide both make construction transparency an explicit criterion: every endpoint should land on the grid, every arc should have a stated radius, every angle should be a system-defined value (0°, 30°, 45°, 60°, 90°). At 200%, accidents become visible. Bringhurst makes the same point about typefaces (§3.4): "details are not the details, they make the design."
**Application.** Snap all endpoints to a 0.5pt sub-grid. Restrict arc radii to a closed set (e.g., {2, 4, 6, 8} pt). Restrict angles to the system's declared degree set.
**Anti-example.** At 200% zoom, two stroke endpoints are 0.13pt apart and not aligned. At 100% it looked fine. It was not fine.

### 8. Family resemblance, not uniformity
**Principle.** Icons in a set should feel related the way siblings do — not identical, not unrelated.
**Rationale.** Type-design canon: a typeface family (Roman, italic, bold, semibold) shares DNA but not geometry. Cheng, *Designing Type*, ch. 6, describes the family as a coordinated system in which proportional relationships, not absolute shapes, are inherited. Vignelli's *Canon* applies the same to identity systems (p. 78, "Visual Power"). For icons: the rectangle in your folder must be the *same kind* of rectangle as the screen in your phone — same corner treatment, same proportion logic — but not literally the same dimensions.
**Application.** Define a small grammar (corner radius rule, stroke terminal rule, optical padding rule, angle set). Every icon must speak that grammar. Two icons should share details a viewer can name on inspection.
**Anti-example.** Folder corners are 2pt rounded; phone screen corners are 4pt rounded; settings-gear teeth have square corners. Three grammars, no family.

### 9. Metaphor before ornament
**Principle.** The metaphor must read instantly. Flourishes serve the metaphor or are deleted.
**Rationale.** Vignelli, *Canon*, p. 28 ("Semantics"): "Semantics is the search for the meaning of whatever we have to design… Without it, design is mute." If the eye has to work to identify the object, no amount of beautiful detail rescues the icon.
**Application.** Squint test first (see [`negative-space.md`](negative-space.md)). If the silhouette does not announce the metaphor in 200ms, no detail work is permitted until it does. Only when the metaphor is locked may craft passes add ornament.
**Anti-example.** A "save" icon rendered as a beautifully detailed floppy disk that no user under 30 recognizes. Ornament without metaphor.

### 10. Time spent looking equals quality
**Principle.** Masters spend more time looking at icons than drawing them.
**Rationale.** *Designer consensus*; closest published version is Frank Chimero, *The Shape of Design* (self-published, 2012, ch. 4), on the discipline of seeing as primary to making. Wathan & Schoger return to this in *Refactoring UI*'s introduction: the asymmetry between novice and expert is rarely tools or technique; it is hours spent comparing. Translated to the skill: every craft pass must spend significant compute on *audit and reference comparison* before further generation.
**Application.** Phase 9 (hi-end craft pass) should allocate at least as many tokens to comparison-with-tier-A and to audit as to generation. Re-renders driven by audit notes are normal; "ship the first draft" is the failure mode.
**Anti-example.** Generate 24 icons in one pass, ship. No comparison, no second look. The set will show it.

## How to use this file

The skill loads this file in **phase 5** (icon-system-rules) so the rules document inherits the principles as constraints, and again in **phase 9** (hi-end craft pass) where each principle becomes a checklist item against which every icon is reviewed. In phase 5, principles 1–8 inform the rules; in phase 9, all ten apply, with extra weight on principles 4, 5, 7, and 10 — the ones that distinguish a polished set from a competent one.

When the user requests "essential" or "standard" tier, the skill applies principles 1, 2, 6, 8, 9 only — the floor of professional output. When the user requests "hi-end," the full ten apply, and phase 9 is mandatory.

## Anti-pattern catalog

If you see any of the following, aesthetic principles have been ignored:

- Multiple ornaments per icon (violates §1, §5)
- Stroke variation as decoration rather than function (§1, §6)
- Perfect mirror symmetry across the entire set (§3)
- Generic geometric primitives with no metaphoric anchor (§9)
- Color compensating for weak silhouette (§6, §9)
- Trends-of-the-week styling (skeuomorphism revival, glassmorphism, neumorphism) applied without metaphor justification (§1, §6)
- Different corner-radius logic per icon (§2, §8)
- Bounding-box overfill — every icon crashes into its grid edges (§2, see also [`negative-space.md`](negative-space.md))
- One-pass generation with no audit (§10)
- "Designer" flourishes that do not carry meaning (§1, §9)

## Sources

- Vignelli, Massimo. *The Vignelli Canon*. Baden: Lars Müller Publishers, 2010. Free PDF: [vignelli.com](https://www.vignelli.com) / archived at archive.org. (Cited: pp. 28 "Semantics," 56 "Discipline," 78 "Visual Power.")
- Rams, Dieter. "Ten Principles of Good Design." Distilled from Braun-era lectures, 1970s–80s; published in *Dieter Rams: As Little Design as Possible*, ed. Sophie Lovell, Phaidon, 2011.
- Müller-Brockmann, Josef. *Grid Systems in Graphic Design / Raster Systeme für die visuelle Gestaltung*. Sulgen: Niggli, 1981; current ed. 2017. (Ch. 4 on rhythm.)
- Tschichold, Jan. *The New Typography*. Trans. Ruari McLean. Berkeley: University of California Press, 1995 (orig. *Die neue Typographie*, 1928). (Asymmetric composition.)
- Lupton, Ellen. *Thinking with Type*. 2nd ed. Princeton Architectural Press, 2010. (Counter-form, white space.)
- Cheng, Karen. *Designing Type*. New Haven: Yale University Press, 2005. (Optical adjustment, ch. 3; family construction, ch. 6.)
- Wathan, Adam & Steve Schoger. *Refactoring UI*. Self-published, 2018. [refactoringui.com](https://www.refactoringui.com). (Color, typography chapters.)
- Bringhurst, Robert. *The Elements of Typographic Style*. 4th ed. Vancouver: Hartley & Marks, 2013. (§3.2 character; §3.4 details.)
- Arnheim, Rudolf. *Art and Visual Perception*. 50th Anniv. ed. UC Press, 2004 (orig. 1954). (Dynamic balance.)
- Chimero, Frank. *The Shape of Design*. Self-published, 2012. [shapeofdesignbook.com](https://shapeofdesignbook.com). (Discipline of seeing.)
- Phosphor Icons design notes. [phosphoricons.com](https://phosphoricons.com); [github.com/phosphor-icons/core](https://github.com/phosphor-icons/core).
- Lucide Icons contributor guide. [lucide.dev/guide/design](https://lucide.dev/guide/design).
