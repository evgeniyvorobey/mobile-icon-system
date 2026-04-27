# Example Responses

Gold-standard answer shapes for icon-set requests. Each example shows what a high-quality response looks like for a representative request type.

## Example 1 — Tab Bar Refresh

**Request**: Refresh existing Tab Bar (5 icons) to match a strong logo.

**Response shape**:

```markdown
Mode: icon-system creation (refresh of partial system)
Platform scope: iOS Tab Bar + Android Bottom Nav
Brand DNA source: extracted from brand/primary-symbol.svg
Quality tier: Standard

## Assumptions
- 5 destinations: Home, Search, Library, Profile, Settings (confirm)
- Both states required (filled selected, outlined unselected)
- Existing icon recognition equity is moderate — refresh may evolve metaphors slightly

## Brand DNA (Extracted)
- Geometric alphabet: circle, vertical/horizontal lines, 45° diagonals
- Stroke language: 1.75pt uniform at 24px reference, round terminals
- Corner treatment: 2pt outer, 0 inner
- Color logic: monochrome silhouette, single-tint friendly
- Optical correction: diagonals +5%, circles overshoot 2%

Confirm extraction or correct.

## Project UI Snapshot
[short summary of audit findings]

## Proposed Icon System Rules
- Grid: 24×24 (live area 20×20)
- Stroke: 1.75pt orthogonal, 1.85pt diagonal compensation
- Cap: round | Join: round
- Outer corner: 2pt | Inner corner: 0
- Style: outlined (unselected) + filled (selected)
- Color: monochrome, platform-tinted
- Naming: ic_tab_{name}_{state}.svg

**Halt: please confirm or revise these rules before I generate the set.**

Next actions:
- Confirm Brand DNA extraction
- Confirm icon system rules
- Confirm vocabulary (Home, Search, Library, Profile, Settings — same as today?)
```

## Example 2 — User Confirms Rules; Skill Generates Set

**User**: "Rules look good. Vocabulary same as today."

**Response shape**:

```markdown
Mode: icon-system creation (refresh)
Platform scope: iOS Tab Bar + Android Bottom Nav
Brand DNA source: confirmed
Quality tier: Standard

## Vocabulary (Confirmed)
| Tab | Metaphor | Form | Cliché risk |
|---|---|---|---|
| Home | House silhouette | Square keyline, simple roof | High (standard) — recognition prioritized |
| Search | Magnifying glass | 45° angle, square keyline | Low |
| Library | Stacked books | 3 rectangles, vertical-rect keyline | Medium |
| Profile | Person | Head + shoulders, circle keyline | Medium — gendered risk |
| Settings | Gear | 6-toothed cog, square keyline | Medium — small-size collapse |

## Generated Set

### Home (filled + outlined)
[SVG inline]
- Construction: 24×24, square keyline 18, 1.75pt stroke
- Optical: visual centering ✓

### Search (filled + outlined)
[SVG inline]
- Construction: 45° handle, ⌀10 lens
- Optical: diagonal stroke +5% (1.85pt), visual centering shift +0.5pt right

### Library (filled + outlined)
[SVG inline]
- Construction: 3 rectangles, vertical-rect keyline
- Optical: small bottom-shelf line documented as 16pt risk

### Profile (filled + outlined)
[SVG inline]
- Construction: ⌀6 head, trapezoidal shoulders
- Optical: visual centering ✓; gender-neutral form

### Settings (filled + outlined)
[SVG inline]
- Construction: 6-tooth cog, ⌀12 outer
- Optical: diagonal teeth +5%, anchor reduction (32 → 24)

## Cross-Icon Consistency Audit
| Icon | Stroke | Terminal | Corner | Weight | Centering | State pair | Action |
|---|---|---|---|---|---|---|---|
| Home | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | none |
| Search | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | none |
| Library | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 16pt risk noted |
| Profile | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | none |
| Settings | ✓ | ✓ | ✓ | heavy | ✓ | ✓ | reduce gear teeth from 8 to 6 (already done) |

## Evaluation
| Dimension | Score | Notes |
|---|---|---|
| Small-size legibility (20pt) | pass | Library borderline at 16pt |
| Brand fit | 4 | Strong inheritance from logo |
| Platform fit (iOS) | pass | Template image exports clean |
| Platform fit (Android) | pass | Vector drawable, theme-tintable |
| Set consistency | 4 | Settings was heavy; corrected |
| Metaphor clarity | 4.5 | All standard, low ambiguity |
| Cliché avoidance | 3 | Standard metaphors; differentiation through stroke |
| Cross-cultural | pass | Profile uses gender-neutral form |
| State distinction | pass | Filled vs outlined obvious at 20pt |
| **Composite** | **4.0** | **Ship-ready with one follow-up (Library 16pt)** |

## Context Validation
- iOS Tab Bar light + dark: ✓
- Android Bottom Nav light + dark: ✓
- Adjacent to system icons: ✓ feels native, distinguishable
- Competitor row: ✓ recognizable; doesn't shout

## Recommendations
1. Ship the set as designed
2. Document Library 16pt fallback variant (small horizontal bookmark) in package
3. Monitor Settings discovery analytics post-launch — gear at 20pt is fine but watch real-user data

## Next actions
- Approve set or request revisions
- I'll scaffold the production package once approved
```

## Example 3 — Single Icon Addition

**Request**: Add a "Notifications" icon to existing system.

**Response shape**:

```markdown
Mode: single icon addition
Platform scope: iOS + Android (same as existing)
Brand DNA source: project (rules documented in icon-system-rules.md)
Quality tier: Standard

## Existing System Rules (Read)
[summary of rules from project's icon-system-rules.md]

## Vocabulary
- Icon: Notifications
- Metaphor: bell silhouette
- Form: solid bell, square-rect keyline
- Cliché risk: medium — bell with ringing lines avoided
- Cross-cultural: ✓ universal

## Generated Icon (filled + outlined)
[SVG inline]
- Construction: 24×24, square-rect keyline, 1.75pt stroke (matches set)
- Optical: visual centering ✓

## Cross-Icon Consistency Check (vs existing 4)
- Stroke weight: ✓ matches set (1.75pt)
- Terminal: ✓ round (matches)
- Corner: ✓ 2pt (matches)
- Visual weight: ✓ balanced against existing row

## Validation
- 20pt Tab Bar: ✓
- 24dp Bottom Nav: ✓
- Adjacent to existing 4: ✓ feels like same family

## Next actions
- Approve and add to existing exports/
- Update vocabulary.md with the new entry
```

## Common Response Patterns

### Always include
- `Mode:` line
- `Platform scope:` line
- `Brand DNA source:` line
- `Quality tier:` (or "to be confirmed")
- Labeled assumptions before generation
- Phase-5 gate explicit halt before generation

### Never do
- Generate full production package without user confirmation
- Self-select a rule set when divergence is appropriate
- Skip the consistency audit
- Score everything 5 ("looks good")
- Output SVG without construction notes

### Bilingual responses

Reply in user's language. Keep code, file names, and SVG attributes in English. Translate explanations and rationale.

## Failure Modes

- **Response without Mode/Platform/DNA-source headers** — user can't tell what context the response operates in
- **Generating before halt** — bypassing phase 5 gate
- **Score-all-5 evaluation** — not real evaluation
- **No labeled assumptions** — user has to ask follow-up questions to fill gaps
- **Validation skipped** — declared ship-ready without context tests
