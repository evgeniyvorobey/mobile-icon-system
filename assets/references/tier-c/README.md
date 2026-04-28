# Tier C — anti-examples (do not emulate)

**The icons in this directory are wrong on purpose.**

They are kept in the corpus so the LLM can recognize specific failure modes
when reviewing its own output, not so the LLM can reproduce them. When
phase 7 or phase 9 references a tier-C file, the model is being asked to
*compare its draft against this anti-example and confirm it has avoided the
named failure*.

Do not lift path data from these files. Do not treat their construction as
canonical. They violate the rules stated in
[`references/icon-vocabulary.md`](../../../references/icon-vocabulary.md) and
[`references/aesthetic-principles.md`](../../../references/aesthetic-principles.md)
on purpose.

## Files and failure modes

| File | Failure mode |
|---|---|
| `calendar-overdetailed.svg` | **Over-detailed.** Dates rendered inside the calendar; meaningful at preview, illegible at 16-20pt. |
| `settings-12tooth.svg` | **Blob at 20pt.** 12 cog teeth; merge into a fuzzy disc at deployment size. The reference exemplar uses 8 teeth. |
| `home-overdetailed.svg` | **Over-detailed.** Literal house with chimney, three windows with cross-mullions, door with knob. Cliché list violation. |
| `user-gendered.svg` | **Gendered.** Long-hair triangles + arms-akimbo posture code the figure as feminine. Profile icons must default to non-gendered forms. |
| `notification-color-state.svg` | **Color-only state distinction.** Unread state is conveyed only by `fill="red"` — fails Forced Colors mode and color-blindness. |
| `lock-thin.svg` | **Under-mass at small sizes.** Stroke 1.5 + shackle radius < body height/2. Padlock dissolves into thin lines at 16-20pt; shackle reads as rounded U, not true semicircle. |
| `refresh-off.svg` | **Slash-language reference.** Catalogued as tier-C anchor for the `m2 2 20 20` slash construction shared by every "X off" state in the corpus (eye-off, mic-off, cloud-off). Use as calibration reference for off-state language consistency, not as a construction to lift directly. |
| `sort-list-filter.svg` | **Visual confusion with hamburger nav.** Three lines of decreasing length read as a global navigation menu, not a sort/filter control, at 20pt. |
| `fingerprint-9loops.svg` | **Over-detailed at 20pt + bullseye reading.** 9 concentric perfect circles. Real fingerprints are 2-3 visible offset arcs (non-concentric); concentric pattern collapses to target/bullseye. |
| `credit-card-branded.svg` | **Brand-coupled metaphor.** Card body + magstripe + chip + Visa-like swoosh. Once a generic icon points at one brand, every other brand looks wrong. Compare against tier-A `credit-card.svg` (Lucide): 2 primitives only. |
| `duotone-color-only.svg` | **Color-only state for the duotone family.** Mass layer bound to literal `red`, outline to literal `black`. Fails Forced Colors mode and deuteranopia simulation. Compare against tier-A duotone exemplars where both layers bind to `currentColor`. |

For each file, the sibling `*.notes.md` documents the failure mode in detail
and points to the tier-A reference the LLM should compare against instead.
