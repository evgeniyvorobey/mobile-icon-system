# Multi-Style Review

Use this workflow when a client needs one icon set explored in three style candidates for A/B/C review. The goal is parallel comparison, not three separate icon systems.

## When to Use

- The icon vocabulary and Brand DNA are known.
- The client wants to compare three visual directions before production.
- The team needs apples-to-apples feedback across the same surfaces.

Do not use this flow to mix per-icon ideas. If the vocabulary, metaphors, grid, accessibility tier, or target surfaces are still changing, finish the base workflow gates first.

## Required Locks

Freeze these once, before any style generation begins:

- **Brand DNA**: one shared `brand-dna.md`.
- **Icon inventory**: same icons, states, names, and order.
- **Metaphors**: same meaning and metaphor for every icon.
- **Grid**: same base grid, live area, keylines, and optical sizing protocol.
- **Accessibility tier**: same contrast, state distinction, small-size, and touch-target requirements.
- **Target surfaces**: same iOS, Android, web, Tab Bar, Bottom Nav, action, or status surfaces.

Only style rules may vary: stroke language, fill model, terminal style, corner logic, color model, detail density, and optical correction strength.

## Parallel Generation

1. Scaffold a review package:

   ```bash
   python3 scripts/init_multi_style_review.py ./multi-style-review \
     --project-name "Project Name" \
     --owner "Design Team" \
     --icons "home, search, library, profile, settings"
   ```

2. Fill the shared files in `shared/`. These are the source of truth for all three candidates.
3. Assign one worker or generation pass to each style folder: `style-a/`, `style-b/`, `style-c/`.
4. Generate every icon in every style folder with identical filename stems and contact-sheet order.
5. Render the HTML comparison sheet:

   ```bash
   python3 scripts/render_multi_style_contact_sheet.py ./multi-style-review \
     --output ./multi-style-review/review/contact-sheet.html
   ```

6. Review using `review/scorecard.md`, `review/contact-sheet.md`, and the generated `review/contact-sheet.html`.
7. Record the client decision in `review/decision-log.md`.
8. Lock exactly one winner in `review/winner-lock.md`.

## Package Shape

```text
multi-style-review/
  shared/
    brief.md
    brand-dna.md
    icon-inventory.csv
    review-constraints.md
  style-a/
    candidate-brief.md
    icons/
    renders/
    exports/
  style-b/
    candidate-brief.md
    icons/
    renders/
    exports/
  style-c/
    candidate-brief.md
    icons/
    renders/
    exports/
  review/
    contact-sheet.md
    contact-sheet.html
    decision-log.md
    scorecard.md
    winner-lock.md
```

`contact-sheet.html` is generated after SVG candidates exist. It is intentionally
self-contained and embeds SVGs as data URIs so the reviewer can open one file
without network access. Missing candidate SVGs are shown as missing cells rather
than silently removed.

## Winner Lock

After review, production continues only from the chosen style folder. Do not silently blend style A strokes with style B corners or style C color logic.

If the client asks for a hybrid, pause production and make it explicit:

- Document the requested blend in `review/decision-log.md`.
- Treat it as a new style candidate or revised winner rule set.
- Regenerate the full inventory under that single revised rule set.
- Update `review/winner-lock.md` before production work resumes.

The production package should contain one locked style system, not a per-icon collage of review preferences.
