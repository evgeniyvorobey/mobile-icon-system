# Example Requests

Realistic request patterns the skill handles. Each example shows the user's request and the corresponding skill mode + tier classification.

## 1. Tab Bar Refresh — Existing App

**User**:

> Our app's Tab Bar uses Material outlined icons mixed with three custom ones — looks inconsistent. We have a logo with strong geometric character. Can you refresh the Tab Bar so all 5 icons are brand-coherent?

**Mode**: icon-system creation (refresh of partial system)
**Tier**: Standard (refresh, not premium)
**Brand DNA source**: extract from logo (Mode 2)
**Phases**: 2 → 3 → 5 (gate) → 6 → 7 → 8 → 10 → 11 → 13
**Skip**: phase 9 (craft pass) unless user upgrades

## 2. Full Icon Set From Scratch — New App

**User**:

> Designing a new health app. We have brand colors and typography but no icons yet. Need: Tab Bar (5 destinations), action icons (add, share, edit, delete), navigation (back, menu, close). Brand feels precise and warm.

**Mode**: icon-system creation (greenfield)
**Tier**: Hi-end (premium positioning + full system from scratch)
**Brand DNA source**: ask user (Mode 3)
**Phases**: full 13-phase workflow
**Notes**: divergence pass appropriate; multiple rule sets to compare

## 3. Single Icon Addition

**User**:

> We need a "Notifications" icon to add to our existing Tab Bar. Set is filled-when-active, outlined-otherwise, 1.75pt stroke, round terminals, R=2 corners. Match the existing Home, Search, Library, Profile icons.

**Mode**: single icon addition
**Tier**: Standard
**Brand DNA source**: project (rules already documented)
**Phases**: 1 → 6 (vocabulary for one icon) → 7 → 8 (cross-icon consistency vs existing 4) → 11 (in-context with existing)
**Notes**: must match existing system exactly; no rule-set divergence

## 4. Icon Set Audit (No Redesign)

**User**:

> Audit our current Tab Bar and tell me if the 5 icons hold together. Don't redesign — just evaluate. Are they consistent? Do they match our logo? Do they survive at 20pt?

**Mode**: icon-set audit / refinement (no redesign)
**Tier**: Standard
**Brand DNA source**: extract from logo (Mode 2)
**Phases**: 1 → 2 → 3 → 8 → 10 → 11 → 12
**Output**: punch list ordered by ship-risk; no concepts generated
**Notes**: closely related to "Production Audit" pattern in logo skill

## 5. Brand-Coherent Monochrome Set With Material You Support

**User**:

> Designing for Android-first. Need Bottom Nav icons (5) that work great with Material You themed icon support. Brand identity must show through even when system tints aggressively. Icons must work under wild palettes (warm, cool, neutral, vibrant).

**Mode**: icon-system creation
**Tier**: Hi-end (themed support, large palette range)
**Brand DNA source**: ask user (Mode 3) or extract (Mode 2)
**Phases**: full workflow with extra emphasis on phase 11 (themed validation)
**Notes**: monochrome construction; verify under 5+ Material You dynamic palettes

## 6. iOS-First Premium With Liquid Glass Support

**User**:

> Premium iOS productivity app. iOS 26 Liquid Glass effects render Tab Bar with translucent material. Icons must work behind glass distortion. We have a precise geometric logo (1.5pt strokes, sharp corners).

**Mode**: icon-system creation
**Tier**: Hi-end (premium + new platform behavior)
**Brand DNA source**: extract from logo (Mode 2), confirm with user
**Phases**: full workflow + extra phase 11 contexts (Liquid Glass validation)
**Notes**: live research mandatory (Liquid Glass specs); validate against translucent backdrop

## 7. Cross-Platform Set With Brand Consistency

**User**:

> Need the same icons across iOS Tab Bar, Android Bottom Nav, and our React Native admin tool. Single source of truth. How do we keep them consistent while respecting platform conventions?

**Mode**: icon-system creation (cross-platform)
**Tier**: Standard or Hi-end depending on user's appetite
**Brand DNA source**: existing or new
**Phases**: full workflow with phase 13 producing all three exports
**Notes**: SVG master is single source; per-platform exports derived; document any platform-specific deviations

## 8. Equity-Preserving Refresh

**User**:

> Our app icons are 4 years old. Users recognize them. Refresh the construction (1.5pt → 1.75pt, sharper corners → 2pt rounded) without changing silhouettes. Existing users must still find their app.

**Mode**: icon-system creation (evolutionary refresh)
**Tier**: Standard
**Brand DNA source**: extract from current set
**Phases**: 1 → 3 (heavy audit, document equity) → 5 (rules with explicit "preserve silhouettes" constraint) → 7 → 8 → 10 → 11 (with old/new side-by-side comparison) → 13
**Notes**: workflow includes "recognizability preservation" as scoring dimension

## Pattern Recognition

Common signals that map to modes:

| User signal | Mode | Tier hint |
|---|---|---|
| "refresh", "refresh", "update" | refresh / refinement | usually Standard |
| "from scratch", "new app", "greenfield" | creation | likely Hi-end |
| "add this one icon" | single icon addition | Standard |
| "audit", "evaluate", "check" | audit / no-redesign | Standard |
| "premium", "luxury", "craft" | any | Hi-end |
| "Material You", "themed icons", "Liquid Glass" | any | Hi-end |
| "match our logo" | any | requires Brand DNA Mode 1 or 2 |
| "consistent across platforms" | cross-platform | Hi-end (more validation) |

## Failure Modes in Request Interpretation

- **Treating "refresh" as "redesign"** — refresh implies preserving equity
- **Skipping divergence on greenfield** — multiple rule sets help user choose
- **Running full workflow on single-icon addition** — overproducing for the request
- **Running standard audit when user asks for premium quality** — under-delivering
- **Generating before locking phase 5 rules** — bypassing the gate
