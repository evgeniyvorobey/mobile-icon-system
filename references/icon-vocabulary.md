# Icon Vocabulary

Catalog of UI icon metaphors, recommended forms, and clichés to avoid, covering the full brand icon set used in a typical mobile app — navigation, actions, system, media, status, communication, commerce, content, social, editing, time, location, and security. Use this when planning the vocabulary phase (workflow step 6) — for each icon needed in the set, confirm metaphor and check cliché risk before generation.

## Coverage map

The vocabulary below covers the categories a complete brand icon set normally needs:

| Category | Typical count in a full set | Section below |
|---|---|---|
| Tab Bar / Bottom Nav | 3–6 | [Tab Bar / Bottom Nav Standards](#tab-bar--bottom-nav-standards) |
| Action (toolbar / button) | 6–12 | [Action Icons](#action-icons) |
| System & Settings | 3–6 | [System & Settings](#system--settings) |
| Media & Playback | 6–12 | [Media & Playback](#media--playback) |
| Status & Feedback | 4–6 | [Status & Feedback](#status--feedback) |
| Communication | 4–8 | [Communication](#communication) |
| Commerce & Wallet | 4–8 | [Commerce & Wallet](#commerce--wallet) |
| Content & Files | 6–10 | [Content & Files](#content--files) |
| Social & Engagement | 4–8 | [Social & Engagement](#social--engagement) |
| Editing | 4–8 | [Editing](#editing) |
| Time & Schedule | 3–5 | [Time & Schedule](#time--schedule) |
| Location & Maps | 3–5 | [Location & Maps](#location--maps) |
| Security & Privacy | 3–5 | [Security & Privacy](#security--privacy) |

A typical full-coverage app icon set lands at ~50–80 icons. Tab Bar comes first because it is the most public surface, but the entire set must inherit the same Brand DNA — generate as one family, never as siloed sub-sets.

## Calibration corpus references

For metaphors marked with a **Reference:** block below, the skill ships hand-curated tier-A craft examples in [`assets/references/tier-a/`](../assets/references/tier-a/) and tier-B competent examples in [`assets/references/tier-b/`](../assets/references/tier-b/). When generating one of these metaphors, the LLM should:

1. Read the corresponding `.svg` and `.notes.md` files
2. Study the cited path-data observations (anchor counts, optical corrections, mathematical derivations of distances)
3. Reproduce the *principle* (not the literal path) in the brand's geometric alphabet

External reference URLs (Material Symbols, Lucide, Phosphor) are also given for metaphors not yet covered by the in-repo corpus. These are read-only references — never fetched at runtime.

Anti-examples live in [`assets/references/tier-c/`](../assets/references/tier-c/) and demonstrate failure modes the LLM must learn to **avoid**, not emulate. See [`craft-rubric.md`](craft-rubric.md) for numerical thresholds and [`design-tool-integrations.md`](design-tool-integrations.md) for how to use the corpus when a design-tool MCP is connected.

## Tab Bar / Bottom Nav Standards

These are the most common Tab Bar destinations. Each row shows: meaning → recommended form → common cliché → cross-cultural notes.

### Home / Main

- **Meaning**: Return to app's main entry / dashboard
- **Recommended forms**: house silhouette (most universal), simple geometric anchor (e.g., diamond, circle within square)
- **Cliché**: literal house with chimney + door + window (over-detailed) — see [`tier-c/home-overdetailed.svg`](../assets/references/tier-c/home-overdetailed.svg)
- **Cross-cultural**: house metaphor reads globally; chimney does not
- **Reference:**
  - tier-A outlined: [`tier-a/home-outlined.svg`](../assets/references/tier-a/home-outlined.svg) (Lucide `house`, ISC) — door+wall as one path, peak deduced from arithmetic, all corners at consistent 2pt radius
  - tier-A filled: [`tier-a/home-filled.svg`](../assets/references/tier-a/home-filled.svg) (Phosphor `house-fill`, MIT) — single fill path with door cutout via inset path, smaller inner radius
  - tier-B (split body/floor — flickers at 20pt): [`tier-b/home-outlined.svg`](../assets/references/tier-b/home-outlined.svg) (Heroicons `home`, MIT)

### Search / Discover

- **Meaning**: Find content, query input
- **Recommended forms**: magnifying glass at 45° angle, magnifying glass + sparkle (for AI search)
- **Cliché**: too-thin handle, perfectly horizontal handle (looks like a frying pan)
- **Cross-cultural**: universal
- **Reference:**
  - tier-A: [`tier-a/search.svg`](../assets/references/tier-a/search.svg) (Lucide `search`, ISC) — `<circle>` primitive + 45° handle line, lens offset from grid center to compensate for handle weight, mathematically derived gap between lens and handle
  - tier-B (eyeballed handle length): [`tier-b/search.svg`](../assets/references/tier-b/search.svg) (Heroicons `magnifying-glass`, MIT)

### Library / Collection / Saved

- **Meaning**: User-curated content
- **Recommended forms**: stacked rectangles (books), bookmark, folder, heart (for liked)
- **Cliché**: literal book with spine and pages (over-detailed)
- **Cross-cultural**: book reads globally; folder reads as Western office metaphor

### Profile / Account / Me

- **Meaning**: User's account, identity
- **Recommended forms**: simplified person silhouette (head + shoulders), circle (avatar placeholder)
- **Cliché**: gendered figure, person + arms (too detailed) — see [`tier-c/user-gendered.svg`](../assets/references/tier-c/user-gendered.svg)
- **Cross-cultural**: avoid gender-coded forms; circle avatar is safest
- **Reference:**
  - tier-A: [`tier-a/user.svg`](../assets/references/tier-a/user.svg) (Lucide `user`, ISC) — `<circle>` head + arched-rectangle shoulders, shoulder corner radius equals head radius (one geometric alphabet), no torso/neck/face features

### Settings / More

- **Meaning**: Configuration, additional options
- **Recommended forms**: gear (cog), three-dot menu, slider, equalizer
- **Cliché**: gear with too many teeth (becomes blob at 20pt) — see [`tier-c/settings-12tooth.svg`](../assets/references/tier-c/settings-12tooth.svg); wrench
- **Cross-cultural**: gear reads globally; wrench reads as repair, not configuration
- **Reference:**
  - tier-A: [`tier-a/settings.svg`](../assets/references/tier-a/settings.svg) (Tabler `settings`, MIT) — exactly 8 teeth (optical sweet spot), `1.724` ≈ √3 chord length per tooth (mathematically derived from 360°/8), inner aperture as true stroked circle
  - tier-B (Bézier-bump teeth blur at 20pt): [`tier-b/settings-bezier.svg`](../assets/references/tier-b/settings-bezier.svg) (Lucide `settings`, ISC)
  - tier-C (12 teeth → blob at 20pt): [`tier-c/settings-12tooth.svg`](../assets/references/tier-c/settings-12tooth.svg) (Material Symbols Outlined, Apache-2.0)

### Notifications / Inbox

- **Meaning**: Alerts, messages
- **Recommended forms**: bell, envelope, dot indicator
- **Cliché**: bell with ringing lines (over-detailed); envelope with `@` symbol; color-only state indicator — see [`tier-c/notification-color-state.svg`](../assets/references/tier-c/notification-color-state.svg)
- **Cross-cultural**: bell reads as notification; envelope reads as email specifically
- **Reference:**
  - tier-A: [`tier-a/bell.svg`](../assets/references/tier-a/bell.svg) (Lucide `bell`, ISC) — dome + clapper as two paths, no ringing lines, clapper width = 2√3 mathematically derived (60° subtended), 1pt visual gap between dome and clapper
  - tier-C anti-example (color-only "unread" dot, fails accessibility): [`tier-c/notification-color-state.svg`](../assets/references/tier-c/notification-color-state.svg)

### Activity / Feed

- **Meaning**: Stream of recent events
- **Recommended forms**: square pulse waveform, list with vertical accent, activity rings
- **Cliché**: heart pulse line (medical, not social)
- **Cross-cultural**: abstract waveforms read globally

### Messages / Chat

- **Meaning**: Direct communication
- **Recommended forms**: speech bubble, two overlapping bubbles
- **Cliché**: bubble with `...` (loading state, not message)
- **Cross-cultural**: speech bubble universal
- **Reference:**
  - tier-A: [`tier-a/chat.svg`](../assets/references/tier-a/chat.svg) (Lucide `message-circle`, ISC) — single continuous path for bubble + tail (same fill rule), tail flows OUT of bubble's edge as part of the same `<path>` element, never as a separate triangle

### Cart / Shop

- **Meaning**: E-commerce purchase
- **Recommended forms**: shopping cart silhouette, shopping bag
- **Cliché**: cart with too many wheels, basket with weave detail
- **Cross-cultural**: cart reads in cart-shopping cultures; bag reads more universally

### Camera / Capture

- **Meaning**: Photo / video creation
- **Recommended forms**: rectangle with circle (lens), simplified camera body
- **Cliché**: literal SLR with detailed lens rings
- **Cross-cultural**: camera form universal
- **Reference:**
  - tier-A: [`tier-a/camera.svg`](../assets/references/tier-a/camera.svg) (Phosphor `camera` regular, MIT) — body + hood polyline + single `<circle>` lens, lens shifted DOWN from geometric center (cy=132 not 128) to compensate for hood weight at top
  - tier-B (decorative microelement): [`tier-b/camera-decorative.svg`](../assets/references/tier-b/camera-decorative.svg) (Heroicons `camera`, MIT) — includes a 0.008-unit "viewfinder light" indicator that disappears at 16pt and is noise at 24pt

## Action Icons

### Add / Create

- **Meaning**: New item
- **Recommended forms**: plus sign, plus in circle, square with plus inside
- **Cliché**: pencil writing on paper (means edit, not add)
- **Cross-cultural**: plus universal
- **Reference:**
  - tier-A: [`tier-a/plus.svg`](../assets/references/tier-a/plus.svg) (Lucide `plus`, ISC) — two crossing strokes (4 anchors total), NOT a 12-anchor outline of a plus shape; cap radius accounted for by inset coordinates so visible mass aligns to canvas

### Delete / Remove

- **Meaning**: Destroy item
- **Recommended forms**: trash can, X, minus
- **Cliché**: X used for both close and delete (ambiguous)
- **Cross-cultural**: trash can universal in software; minus is safer than X
- **Reference:**
  - tier-A: [`tier-a/trash.svg`](../assets/references/tier-a/trash.svg) (Lucide `trash-2`, ISC) — lid bar + handle arch + body + exactly 2 ribs (not 3 or 5 — sparse enough to render at 20pt), lid bar overhangs body by 2pt on each side as optical correction (lid reads as "sitting on top")

### Share

- **Meaning**: Send to others / external
- **Recommended forms**: iOS share box (square + arrow up), three connected dots
- **Cliché**: paper airplane (means send, not share)
- **Cross-cultural**: iOS share is iOS-specific; three dots is more universal
- **Reference:**
  - tier-A: [`tier-a/share.svg`](../assets/references/tier-a/share.svg) (Lucide `share`, ISC) — tray + up-arrow with explicit 3pt visual gap between arrow base and tray rim (arrow reads as "exiting"), arrow goes UP not horizontally
  - tier-B (3-circle node graph — harder to recognize at 20pt): [`tier-b/share-graph.svg`](../assets/references/tier-b/share-graph.svg) (Heroicons `share`, MIT)

### Refresh

- **Meaning**: Reload, sync
- **Recommended forms**: circular arrow with single arrowhead
- **Cliché**: too many arrows, double arrow
- **Cross-cultural**: universal

### Filter / Sort

- **Meaning**: Subset / reorder list
- **Recommended forms**: funnel (filter), three lines of varying length (sort)
- **Cliché**: gear (means settings)
- **Cross-cultural**: funnel reads globally

### Back / Forward

- **Meaning**: Navigation history
- **Recommended forms**: chevron (`<` / `>`), arrow
- **Cliché**: U-turn arrow (means undo)
- **Cross-cultural**: chevron universal; LTR cultures expect back=left

### Close / Dismiss

- **Meaning**: Exit current context
- **Recommended forms**: X (no surrounding shape), X in circle
- **Cliché**: minus sign (means remove from list)
- **Cross-cultural**: X universal
- **Reference:**
  - tier-A: [`tier-a/x.svg`](../assets/references/tier-a/x.svg) (Lucide `x`, ISC) — two 45° crossing strokes with the SAME 6pt inset as `plus.svg` (so X and + are visually balanced when adjacent in a UI)

### Menu / Hamburger

- **Meaning**: Navigation drawer
- **Recommended forms**: three horizontal lines (uniform spacing)
- **Cliché**: lines of varying length (means sort)
- **Cross-cultural**: hamburger now universal in mobile apps

## System & Settings

### Settings

- **Meaning**: App configuration
- **Recommended forms**: gear (6 teeth), three sliders, toggles
- **Cliché**: gear with too many teeth (collapses to blob at 20pt), wrench (means repair)
- **Cross-cultural**: gear universal; sliders work better at very small sizes

### Theme / Appearance

- **Meaning**: Light/dark/auto mode toggle
- **Recommended forms**: half-filled circle (sun/moon split), sun, moon
- **Cliché**: detailed sun rays, crescent moon with face
- **Cross-cultural**: sun/moon universal

### Language

- **Meaning**: Locale selector
- **Recommended forms**: globe with longitude lines, "A→文" character pair
- **Cliché**: flag (politically loaded; flags ≠ languages), only-English letters
- **Cross-cultural**: globe is safest

### Help / Info

- **Meaning**: Help center, about, documentation
- **Recommended forms**: question mark in circle (help), letter "i" in circle (info)
- **Cliché**: book (reads as documentation specifically, not help in general), lifebuoy ring
- **Cross-cultural**: "?" and "i" universal in software

### Accessibility

- **Meaning**: Accessibility settings entry
- **Recommended forms**: simplified figure with arms outstretched (the standard a11y mark)
- **Cliché**: ear, eye, hand alone — each represents a single disability not the whole settings group
- **Cross-cultural**: the universal accessibility figure is recognized internationally; do not redesign it

### Sync / Cloud

- **Meaning**: Sync state, cloud backup
- **Recommended forms**: cloud silhouette, cloud + arrow (uploading / downloading), circular arrows
- **Cliché**: cloud with raindrops (means weather), cloud with database stack visible
- **Cross-cultural**: cloud now universal in software

## Media & Playback

### Play

- **Meaning**: Start playback
- **Recommended forms**: right-pointing triangle (centered, optical), triangle in circle
- **Cliché**: triangle with shadow / 3D, triangle pointing up (means upload)
- **Cross-cultural**: universal; use optical centering — geometric center looks off-center

### Pause

- **Meaning**: Pause playback
- **Recommended forms**: two equal vertical bars
- **Cliché**: bars of unequal width or rounded ends that diverge from set's terminal language
- **Cross-cultural**: universal

### Stop

- **Meaning**: End playback
- **Recommended forms**: solid square
- **Cliché**: square outline (looks like a frame, not a control)
- **Cross-cultural**: universal in media context

### Skip Forward / Back

- **Meaning**: Next / previous track
- **Recommended forms**: triangle + vertical bar
- **Cliché**: double arrow with no terminal bar (means fast-forward / rewind, not skip)
- **Cross-cultural**: universal in media

### Fast-Forward / Rewind

- **Meaning**: Scrub forward / back
- **Recommended forms**: two stacked triangles
- **Cliché**: confused with skip (skip has the bar; FF/RW does not)
- **Cross-cultural**: universal

### Volume

- **Meaning**: Audio level
- **Recommended forms**: speaker silhouette + 0/1/2/3 wave arcs (state-aware)
- **Cliché**: musical notes (means music, not volume), speaker without waves (ambiguous)
- **Cross-cultural**: speaker universal

### Mute

- **Meaning**: Volume off
- **Recommended forms**: speaker + diagonal slash, speaker with X
- **Cliché**: speaker silhouette alone (ambiguous with volume), red X over speaker (color carries meaning, fails color-blind test)
- **Cross-cultural**: slash overlay universal

### Microphone

- **Meaning**: Voice input, recording
- **Recommended forms**: capsule on stand
- **Cliché**: detailed studio mic with grille
- **Cross-cultural**: universal

### Record

- **Meaning**: Start recording
- **Recommended forms**: solid filled circle (often with red tint at use site)
- **Cliché**: circle with "REC" label (use label outside icon, not inside)
- **Cross-cultural**: universal

### Live / Broadcast

- **Meaning**: Live stream indicator
- **Recommended forms**: filled dot + radiating arcs, "LIVE" badge
- **Cliché**: TV antenna with lines (looks like wifi or signal)
- **Cross-cultural**: dot+arc reads as broadcast in software

### Cast / AirPlay

- **Meaning**: Send media to another device
- **Recommended forms**: rectangle with concentric arcs in lower-left corner
- **Cliché**: TV with antenna (means TV, not casting)
- **Cross-cultural**: emerging convention; consider label-pairing

### Picture-in-Picture

- **Meaning**: Floating mini player
- **Recommended forms**: large rectangle with smaller rectangle inset in corner
- **Cliché**: too small inset rectangle (collapses at 20pt)
- **Cross-cultural**: emerging convention

## Status & Feedback

### Success

- **Meaning**: Action completed
- **Recommended forms**: check mark (no surrounding shape, or in circle), check in circle filled
- **Cliché**: thumbs up (carries opinion), green-only check without shape change (color-blind unsafe)
- **Cross-cultural**: check mark universal; thumbs up culturally loaded in some regions
- **Reference:**
  - tier-A: [`tier-a/check.svg`](../assets/references/tier-a/check.svg) (Lucide `check`, ISC) — single 3-anchor path with two precisely 45° strokes, bend point at (9, 17) left of horizontal center so right side carries more visual weight (correct for LTR reading)

### Error

- **Meaning**: Action failed, attention required
- **Recommended forms**: X in circle, triangle with exclamation mark (caution-style)
- **Cliché**: red dot alone (no shape ≠ no meaning), skull (too aggressive)
- **Cross-cultural**: X and triangle universal; pair shape + color, never color alone

### Warning

- **Meaning**: Caution, proceed with care
- **Recommended forms**: triangle with exclamation mark
- **Cliché**: triangle with skull (overkill), bare exclamation mark (ambiguous with info)
- **Cross-cultural**: triangle+exclamation is internationally standard for warning

### Info

- **Meaning**: Informational message
- **Recommended forms**: lowercase "i" in circle
- **Cliché**: question mark (means help), light bulb (means tip / suggestion)
- **Cross-cultural**: "i" universal

### Loading / Spinner

- **Meaning**: Operation in progress
- **Recommended forms**: arc segment (animated rotation), three dots (animated pulse), circular progress with no fill at start
- **Cliché**: hourglass (slow / stuck connotation on mobile), egg-timer
- **Cross-cultural**: spinner now universal; provide a `prefers-reduced-motion` static fallback (see [`accessibility.md`](accessibility.md))

### Progress

- **Meaning**: Determinate completion percentage
- **Recommended forms**: filled arc on circle (radial), filled bar on rectangle (linear)
- **Cliché**: cluttered progress with markers
- **Cross-cultural**: universal

## Communication

### Phone Call

- **Meaning**: Voice call
- **Recommended forms**: handset silhouette
- **Cliché**: detailed rotary phone (anachronistic), modern smartphone (means device, not call)
- **Cross-cultural**: handset universal in software despite physical handsets being rare

### Video Call

- **Meaning**: Video call
- **Recommended forms**: video camera silhouette, screen with lens
- **Cliché**: TV camera with tripod (broadcast feel), face inside screen (creepy)
- **Cross-cultural**: camera form universal

### Email

- **Meaning**: Email message
- **Recommended forms**: envelope (sealed flap visible)
- **Cliché**: envelope with `@` (redundant), envelope with paper sticking out
- **Cross-cultural**: envelope universal; `@` reads as address, not email itself

### Send

- **Meaning**: Submit message / form
- **Recommended forms**: paper airplane (45° angle), arrow → terminal
- **Cliché**: airplane that looks like an actual aircraft, mail truck
- **Cross-cultural**: paper airplane now universal in messaging

### Attachment

- **Meaning**: File attached to message
- **Recommended forms**: paper clip (45° angle)
- **Cliché**: pin (means saved / pinned, not attached)
- **Cross-cultural**: paper clip universal

### Reply / Forward

- **Meaning**: Reply to / forward a message
- **Recommended forms**: curved arrow pointing left (reply), curved arrow pointing right (forward)
- **Cliché**: arrows that look like back / forward navigation
- **Cross-cultural**: universal in mail UIs

### Contacts / Address Book

- **Meaning**: Contact list
- **Recommended forms**: book with tabs, person silhouettes overlapping
- **Cliché**: rolodex (anachronistic), single person silhouette (means profile)
- **Cross-cultural**: book-with-tabs reads as directory globally

## Commerce & Wallet

### Cart

- **Meaning**: Shopping cart
- **Recommended forms**: cart silhouette (basket on wheels)
- **Cliché**: cart with too many wheels, basket with weave detail
- **Cross-cultural**: cart reads in cart-shopping cultures; bag is more universal

### Bag

- **Meaning**: Shopping bag / purchase
- **Recommended forms**: bag with handles, shopping bag with handle loops
- **Cliché**: gift bag (means gift, not purchase)
- **Cross-cultural**: bag globally universal as shopping

### Wallet

- **Meaning**: Payment methods, balance
- **Recommended forms**: bifold wallet silhouette
- **Cliché**: detailed leather wallet, money clip
- **Cross-cultural**: bifold wallet universal in software

### Card

- **Meaning**: Credit / debit card
- **Recommended forms**: rounded rectangle with chip square
- **Cliché**: card with magnetic stripe (anachronistic), card with logo
- **Cross-cultural**: chip-card universal

### Cash / Money

- **Meaning**: Cash, payment, balance
- **Recommended forms**: stack of bills (no currency symbol), coin
- **Cliché**: dollar sign (`$`) only — locale-specific, fails internationally
- **Cross-cultural**: bills + coin reads globally; avoid currency symbols in icons

### Tag / Discount

- **Meaning**: Price tag, sale
- **Recommended forms**: tag silhouette with hole
- **Cliché**: percent sign alone (ambiguous with stats), price tag with text
- **Cross-cultural**: tag universal

### Receipt / Order

- **Meaning**: Past purchase, transaction record
- **Recommended forms**: long rectangle with horizontal lines
- **Cliché**: paper receipt with curl (over-detailed)
- **Cross-cultural**: receipt form universal

### Gift

- **Meaning**: Gift, reward
- **Recommended forms**: box with bow on top
- **Cliché**: gift bag (means shopping bag)
- **Cross-cultural**: wrapped box with bow universal

## Content & Files

### Image / Photo

- **Meaning**: Image content
- **Recommended forms**: rectangle with mountain + sun, rectangle with diagonal line through corner
- **Cliché**: detailed Polaroid frame, image with smile face
- **Cross-cultural**: mountain-and-sun reads globally as "photo"

### Video

- **Meaning**: Video content
- **Recommended forms**: rectangle with play triangle in center, film strip
- **Cliché**: TV silhouette (means broadcast)
- **Cross-cultural**: play-in-rectangle universal

### Document

- **Meaning**: Single text document
- **Recommended forms**: rectangle with corner fold, rectangle with horizontal lines
- **Cliché**: detailed page with text, paper with paperclip
- **Cross-cultural**: corner-folded rectangle universal

### Folder

- **Meaning**: File grouping
- **Recommended forms**: folder silhouette (tab on top-left)
- **Cliché**: folder with files sticking out, manila folder color
- **Cross-cultural**: folder reads as Western office; emerging convention globally

### Download

- **Meaning**: Pull file to device
- **Recommended forms**: arrow pointing down to a horizontal line, cloud + down arrow
- **Cliché**: tray with arrow (over-detailed)
- **Cross-cultural**: down-arrow + line universal

### Upload

- **Meaning**: Push file from device
- **Recommended forms**: arrow pointing up from horizontal line, cloud + up arrow
- **Cliché**: tray with up arrow
- **Cross-cultural**: up-arrow + line universal

### Link

- **Meaning**: Hyperlink, connection
- **Recommended forms**: two interlocking chain links at 45°
- **Cliché**: anchor (means navigation anchor, different meaning)
- **Cross-cultural**: chain links universal in software

### File Type Variants

- **Meaning**: PDF, DOC, IMG, etc.
- **Recommended forms**: document silhouette + 3-letter type label inside
- **Cliché**: detailed application icon (Adobe red, Word blue) — couples brand to third party
- **Cross-cultural**: document + type label universal

### Archive

- **Meaning**: Compressed file, archive
- **Recommended forms**: folder with zipper, box with horizontal lines
- **Cliché**: padlock + folder (means locked file, not archive)
- **Cross-cultural**: emerging — pair with label

## Social & Engagement

### Like / Favorite

- **Meaning**: Personal save / love
- **Recommended forms**: heart (filled active, outlined inactive), star
- **Cliché**: heart used for love + favorite + health (conflated meanings)
- **Cross-cultural**: heart universal as positive sentiment; clarify meaning per surface
- **Reference:**
  - tier-A outlined: [`tier-a/heart-outlined.svg`](../assets/references/tier-a/heart-outlined.svg) (Lucide `heart`, ISC) — single path with *almost* equal lobe radii (5.5 vs 5.49 — intentional optical asymmetry for the right lobe's visual weight), bottom V explicitly rounded with 2pt radius (not a sharp point)
  - tier-A filled: [`tier-a/heart-filled.svg`](../assets/references/tier-a/heart-filled.svg) (Phosphor `heart-fill`, MIT) — single fill path with asymmetric bottom-tip distances (left ≠ right by 4-5%) for optical balance, lobe-radius / canvas ≈ 0.243
  - tier-B (perfectly symmetric — feels less alive): [`tier-b/heart-symmetric.svg`](../assets/references/tier-b/heart-symmetric.svg) (Heroicons `heart`, MIT)

### Star / Rating

- **Meaning**: Quality rating, favorite
- **Recommended forms**: 5-point star, partial fill for half-star
- **Cliché**: detailed star with rays
- **Cross-cultural**: 5-point star universal in rating contexts

### Comment

- **Meaning**: Add or view comment
- **Recommended forms**: speech bubble (single), speech bubble with lines
- **Cliché**: bubble with `...` (loading state)
- **Cross-cultural**: bubble universal

### Share (social context)

- **Meaning**: Share to platform / repost
- **Recommended forms**: arrow + branching paths, three dots connected
- **Cliché**: paper airplane (means send, not share to feed)
- **Cross-cultural**: branching arrow more universal than iOS share box

### Repost / Retweet

- **Meaning**: Share within same platform
- **Recommended forms**: two arrows in circular arrangement
- **Cliché**: refresh icon (looks identical, different meaning)
- **Cross-cultural**: emerging convention; pair with label

### Follow / Add Friend

- **Meaning**: Subscribe, connect
- **Recommended forms**: person silhouette + plus sign
- **Cliché**: hand-shake (formal, professional context only)
- **Cross-cultural**: person+plus universal

### Block / Unfollow

- **Meaning**: Remove connection, block
- **Recommended forms**: person silhouette + minus sign (unfollow), person + slash (block)
- **Cliché**: red X without shape (color-blind unsafe)
- **Cross-cultural**: person + minus / slash universal

### Group / Community

- **Meaning**: Multiple people
- **Recommended forms**: 2–3 overlapping head silhouettes
- **Cliché**: detailed head + body figures (over-detailed at 20pt)
- **Cross-cultural**: overlapping silhouettes universal

### Trending

- **Meaning**: Popular content, rising
- **Recommended forms**: upward zig-zag arrow, flame
- **Cliché**: graph chart (means analytics, not trending)
- **Cross-cultural**: flame universal as "hot"; arrow universal as "rising"

## Editing

### Edit / Pencil

- **Meaning**: Modify existing content
- **Recommended forms**: pencil at 45° angle
- **Cliché**: pencil with eraser detail (over-detailed), pen quill (anachronistic)
- **Cross-cultural**: pencil universal

### Compose / New Document

- **Meaning**: Start new content
- **Recommended forms**: page silhouette + plus sign, pencil + page
- **Cliché**: pencil alone (means edit, not compose)
- **Cross-cultural**: page+plus universal

### Copy

- **Meaning**: Duplicate content
- **Recommended forms**: two overlapping rectangles
- **Cliché**: clipboard (means clipboard specifically)
- **Cross-cultural**: overlapping rectangles universal

### Paste

- **Meaning**: Insert from clipboard
- **Recommended forms**: clipboard silhouette with rectangle inside
- **Cliché**: clipboard alone (ambiguous), arrow into rectangle
- **Cross-cultural**: clipboard universal in software

### Cut

- **Meaning**: Move to clipboard, removing source
- **Recommended forms**: scissors at 45°
- **Cliché**: detailed scissors with finger holes (over-detailed)
- **Cross-cultural**: scissors universal

### Undo / Redo

- **Meaning**: Reverse / replay action
- **Recommended forms**: curved arrow left (undo), curved arrow right (redo)
- **Cliché**: U-turn arrow with no curve (looks like refresh)
- **Cross-cultural**: curved arrow universal

### Format / Style

- **Meaning**: Text formatting
- **Recommended forms**: "A" with horizontal lines below (paragraph style), "B" / "I" / "U" letters
- **Cliché**: paint brush (means color, not text format)
- **Cross-cultural**: letter forms work in Latin scripts; provide localized variants for CJK if format scope differs

### Link Inline

- **Meaning**: Insert hyperlink
- **Recommended forms**: chain links at 45° (same as Content / Link)
- **Cliché**: anchor
- **Cross-cultural**: chain universal

## Time & Schedule

### Clock / Time

- **Meaning**: Current time, duration
- **Recommended forms**: circle with hour + minute hands
- **Cliché**: digital LCD clock (locks to one form)
- **Cross-cultural**: analog clock universal in software despite physical clocks being rare

### Calendar

- **Meaning**: Schedule, dates
- **Recommended forms**: square with binding rings on top, square with date number
- **Cliché**: calendar with too many date cells; calendar with literal "12" inside (over-detailed) — see [`tier-c/calendar-overdetailed.svg`](../assets/references/tier-c/calendar-overdetailed.svg)
- **Cross-cultural**: square+rings universal
- **Reference:**
  - tier-A: [`tier-a/calendar.svg`](../assets/references/tier-a/calendar.svg) (Lucide `calendar`, ISC) — rounded rect body + horizontal divider + two short vertical binding posts (mirrored around x=12, exactly 4pt long = 2 stroke widths), no grid of date squares
  - tier-C anti-example (digits inside body collapse to mush at 16pt): [`tier-c/calendar-overdetailed.svg`](../assets/references/tier-c/calendar-overdetailed.svg) (Phosphor `calendar` regular variant)

### Alarm

- **Meaning**: Scheduled alert
- **Recommended forms**: bell on stand, clock with bells on top
- **Cliché**: bell (already used for notifications), klaxon
- **Cross-cultural**: clock+bells specific to alarm context

### Timer / Stopwatch

- **Meaning**: Countdown, elapsed time
- **Recommended forms**: stopwatch silhouette (circle + crown button on top)
- **Cliché**: hourglass (slow / desktop-era)
- **Cross-cultural**: stopwatch universal

### History

- **Meaning**: Past activity log
- **Recommended forms**: clock with curved arrow around it
- **Cliché**: hourglass, log book
- **Cross-cultural**: clock+arrow universal

## Location & Maps

### Pin / Location

- **Meaning**: Specific place, current location
- **Recommended forms**: teardrop pin with circle inside
- **Cliché**: pushpin (means saved / pinned, different meaning)
- **Cross-cultural**: teardrop pin universal in mapping

### Map

- **Meaning**: Map view
- **Recommended forms**: folded map with creases, map with pin
- **Cliché**: detailed road map, globe (means worldwide / language)
- **Cross-cultural**: folded-map silhouette universal

### Compass

- **Meaning**: Direction, navigation, discover
- **Recommended forms**: circle + N/S needle, simplified compass rose
- **Cliché**: detailed compass with degree markings
- **Cross-cultural**: needle-in-circle universal

### Navigation Arrow

- **Meaning**: Turn-by-turn, current heading
- **Recommended forms**: triangle pointing up (heading direction)
- **Cliché**: arrow + pin combined (means saved location)
- **Cross-cultural**: triangle universal in navigation

### Globe

- **Meaning**: World, language, internet
- **Recommended forms**: circle with longitude lines, simplified continents
- **Cliché**: detailed Earth with realistic continents (over-detailed at 20pt)
- **Cross-cultural**: simplified globe universal

## Security & Privacy

### Lock / Locked

- **Meaning**: Locked, secure, protected
- **Recommended forms**: padlock silhouette (closed shackle)
- **Cliché**: detailed padlock with keyhole (over-detailed)
- **Cross-cultural**: padlock universal

### Unlock

- **Meaning**: Unlocked, open
- **Recommended forms**: padlock with shackle at angle (open)
- **Cliché**: padlock with keyhole only (ambiguous)
- **Cross-cultural**: open shackle universal

### Shield / Protection

- **Meaning**: Security, protection, verified
- **Recommended forms**: shield silhouette, shield with check mark
- **Cliché**: detailed crest, sword + shield combo
- **Cross-cultural**: shield universal in security context

### Eye / Visibility

- **Meaning**: Show / hide content (e.g., password reveal)
- **Recommended forms**: eye silhouette (open), eye with diagonal slash (hidden)
- **Cliché**: eye with eyelashes (too detailed), peeking eye
- **Cross-cultural**: eye universal; slash overlay universal as "off"

### Key

- **Meaning**: Access, password, license
- **Recommended forms**: simplified key silhouette
- **Cliché**: detailed antique key (anachronistic)
- **Cross-cultural**: key universal

### Fingerprint / Biometric

- **Meaning**: Biometric authentication
- **Recommended forms**: stylized fingerprint loops
- **Cliché**: detailed fingerprint with all loops (over-detailed)
- **Cross-cultural**: fingerprint universal in mobile auth

### Face ID / Face Unlock

- **Meaning**: Face biometric authentication
- **Recommended forms**: square frame with simplified face (iOS Face ID style)
- **Cliché**: detailed face portrait
- **Cross-cultural**: square+face universal in mobile auth

## Cliché Map

Avoid these traps:

| Cliché | Why it fails | Alternative |
|---|---|---|
| Literal heart for "favorite" + "love" + "health" | Conflates three meanings | Heart only for personal saves; star for favorite |
| Gear for both "settings" and "system" | Single icon for two locations | Settings = gear; system = sliders or toggles |
| Bell for "notifications" with bell ringing lines | Over-detailed, unstable at 20pt | Solid bell silhouette, optional dot indicator |
| Magnifying glass with text "Aa" inside | Conflates search + accessibility | Plain magnifying glass for search |
| Pencil for "edit" and "compose" | Pencil edit = inline edit; compose = new document | Pencil for edit; document with plus for compose |
| Three dots horizontal vs vertical | Same icon different meaning | Horizontal = more options; vertical = menu |

## Vocabulary Output Format

When the skill outputs the vocabulary table for user review, use this format:

```markdown
| Tab | Metaphor | Form | Risks |
|---|---|---|---|
| Home | House | House silhouette, square keyline | Low |
| Search | Magnifying glass | 45° angle, square keyline | Low |
| Library | Stacked books | 3 rectangles, vertical-rect keyline | Low |
| Profile | Person | Head + shoulders, circle keyline | Medium — gender-coding |
| Settings | Gear | 6-toothed cog, square keyline | Medium — small-size collapse |
```

## When to Deviate

Brand-specific metaphors are encouraged when they fit:

- A music app's Library can be a vinyl record disk
- A reading app's Library can be a book spine row
- A finance app's Activity can be a candlestick chart

The rule: deviation must read at 20pt with no label. If it doesn't, fall back to the standard metaphor.

## Failure Modes

- **One icon, two meanings** — settings ≠ system, favorites ≠ saves
- **Over-detailed metaphor** — bell with ringing lines, gear with 12 teeth
- **Gendered or culturally narrow forms** — male/female figures, Western objects
- **Brand-specific metaphor that requires a label** — failed brand-specificity test
