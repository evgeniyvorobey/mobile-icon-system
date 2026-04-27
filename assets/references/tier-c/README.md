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

For each file, the sibling `*.notes.md` documents the failure mode in detail
and points to the tier-A reference the LLM should compare against instead.
