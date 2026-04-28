# Domain Metaphors

Vertical-specific icon catalogs. These files **complement** [`../icon-vocabulary.md`](../icon-vocabulary.md) — they do not replace it. The universal vocabulary covers 13 categories shared by every consumer app (Home, Search, Profile, Like, Cart, Settings, Volume, Send, Camera, etc.). The domain catalogs add the metaphor stack a vertical app actually needs but that the universal library is too general to provide.

## What these files are

Each file is a curated metaphor catalog for one app vertical: industry overview, 18-22 metaphors with recommended forms / cliché map / cross-cultural notes / industry-leading references, a domain-specific cliché table, state-pair examples that exercise the most stateful icons in that domain, and a universal-vocabulary integration note that flags where the domain reuses the universal shape with a different semantic.

Domain files reference apps by name (Spotify, Robinhood, Apple Health, Notion, Amazon, Instagram, GitHub, Google Maps, Duolingo, PlayStation App). They do **not** carry third-party SVG URLs — the calibration corpus lives in [`../../assets/references/`](../../assets/references/) and is referenced from `icon-vocabulary.md`, not from here.

## When the skill loads them

Phase 4 (Build Context) extracts the user's stated app category. If that category matches one of the 10 catalog files (keyword heuristics below), Phase 6 (Vocabulary) loads:

1. [`../icon-vocabulary.md`](../icon-vocabulary.md) — universal baseline
2. The matched domain file — vertical authority
3. [`_cross-domain.md`](_cross-domain.md) — disambiguates shape reuse across domains

Do **not** preload all 10 catalogs. One domain file is ~5–8 KB; loading 10 wastes the cold-start budget. The selection is made once in Phase 4 and the relevant files are pulled in Phase 6.

If the user's domain does not match any of the 10 catalogs, fall back to `icon-vocabulary.md` only and note that domain-specific guidance is not available for this vertical.

## Authority order vs universal

When a domain catalog and the universal vocabulary disagree, **the domain wins for that app**. Examples:

- Heart in `health.md` = anatomical asymmetric form (vital sign). Heart in `icon-vocabulary.md#like--favorite` = romantic/like. Health app uses anatomical.
- Bookmark in `e-commerce.md` = wishlist. Bookmark in `icon-vocabulary.md` = generic save. E-commerce app uses bookmark for wishlist and explicitly does NOT use heart.
- Refresh in `icon-vocabulary.md#refresh` = reload. Repeat in `music.md` = loop with explicit arrowhead at closure point. Music app must distinguish — never share shape.

Always document the override explicitly in the icon-system rules (Phase 5) so the user sees the deviation rather than discovering it after generation.

## Multi-domain apps

For a fintech with chat (finance + social), a fitness app with social feed (health + social), a gaming app with marketplace (gaming + e-commerce), or any other genuine cross-domain product:

1. Load both domain files plus `_cross-domain.md`.
2. Run an explicit reconciliation pass against `_cross-domain.md` — its 10 patterns catalog every shape that recurs across domains with semantic shifts (Send cluster, Heart cluster, Lightning cluster, Cloud cluster, etc.).
3. Where two domain files disagree, prefer the one whose metaphor is the user's primary action. A fintech with a chat tab uses finance's `Send` (paper-airplane = "send money") for the payment button and either renames the chat tab's Send or redraws it (envelope-with-arrow) to break the collision.

## Domain matching keywords

Use these heuristics in Phase 4 when the user states their app category:

| User says | Load file |
|---|---|
| music streaming, podcast app, audio player, DJ tool | [`music.md`](music.md) |
| neobank, trading, brokerage, crypto, payments, wallet, P2P pay | [`finance.md`](finance.md) |
| fitness tracker, telehealth, medication reminder, mindfulness, sleep, women's health | [`health.md`](health.md) |
| note-taking, task manager, kanban, knowledge base, calendar | [`productivity.md`](productivity.md) |
| shopping, marketplace, DTC, grocery delivery, resale, subscription box | [`e-commerce.md`](e-commerce.md) |
| social network, messaging, community, short video, photo sharing, broadcast | [`social.md`](social.md) |
| developer, DevOps, monitoring, version control, CI/CD, terminal, cloud console | [`dev-tools.md`](dev-tools.md) |
| navigation, rideshare, transit, parking, EV charging, micromobility | [`transportation.md`](transportation.md) |
| learning, course, language app, test prep, flashcards, code learning | [`education.md`](education.md) |
| game, MOBA companion, RPG, gacha, party chat, game launcher, streaming gaming | [`gaming.md`](gaming.md) |

Match on the **product category**, not on a feature one tab happens to provide. A music app with a comment tab is still music — load `music.md`, not `social.md`. A travel app with a marketplace is travel (deferred — see below).

## Selection rationale

The 10 domains in v0.4 were selected because each scored ≥14 on a (prevalence × distance from universal × cliché density × state-pair count) matrix. They are the verticals where generic-icon defaults visibly fail and where a vertical-specific catalog is the single biggest quality lever for the icon set.

## Deferred to v0.5

Four additional catalogs are scoped but not shipped in v0.4. Trigger one of these and the skill should still produce the icon set from `icon-vocabulary.md` baseline; ship request to add the catalog if recurring:

- **travel** — flights, hotels, itinerary, boarding pass, loyalty miles, layover; trigger on "travel app", "flight booking", "hotel app"
- **food / delivery** — restaurant, dish, dietary tag, delivery driver tracking, tip; trigger on "food delivery", "restaurant ordering", "dine-in"
- **real estate** — listing, floor plan, mortgage, square footage, virtual tour; trigger on "real estate", "property listing", "rental"
- **dating** — profile swipe, match, super-like, ice-breaker, video call; trigger on "dating app", "matchmaking", "social discovery"
