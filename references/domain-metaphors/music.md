# Music & Audio

## Industry overview

Music and audio apps (Spotify, Apple Music, YouTube Music, Tidal, SoundCloud, Pandora, Audible, Pocket Casts, Overcast, Bandcamp, Beatport, Anchor, GarageBand) ship the densest playback control vocabulary of any consumer category. Where a generic app has play/pause, a music app has play/pause/skip-back/skip-forward/scrub-back-15/scrub-forward-30/fast-forward/rewind/shuffle/repeat-all/repeat-one/queue/lyrics/cast/picture-in-picture — each must read at 20pt while sitting in same row. Spotify's mobile player published design notes on shuffle vs repeat being the most-failed metaphors in user testing because they're conceptually close. Spotify solves with shape difference: shuffle = crossing arrows (X-pattern), repeat = circular arrow (loop pattern). Audio apps require state-pair density few other domains demand: a single play button might show idle/loading/playing/paused/buffering/cast-active/cast-error — six states for one control.

## Metaphor catalog

### Vinyl record / Disc
- **Meaning**: Library, full catalog, "all your music"
- **Recommended forms**: simple disc (circle) with single concentric ring + center dot; never spiral grooves
- **Cliché**: detailed grooves rendered as multiple concentric rings (becomes moiré pattern at 20pt); 45-rpm hole shown literally
- **Cross-cultural**: vinyl-as-music reads globally to listeners over 25; younger users may not recognize — pair with label
- **Reference**: Tidal Library tab; Bandcamp release pages
- **Universal vocabulary cross-ref**: extends [Library / Collection / Saved](../icon-vocabulary.md#library--collection--saved) — vinyl is brand-specific deviation

### Equalizer (EQ) bands
- **Meaning**: Audio settings, playback configuration, sound profile
- **Recommended forms**: 3 or 5 vertical bars of varying height (asymmetric — never stairstep); animated bars also signal "playing now"
- **Cliché**: 7+ bars (unstable at 20pt); perfectly symmetric bars (looks like settings/sort)
- **Reference**: Spotify currently-playing indicator; Apple Music now-playing badge
- **Universal vocabulary cross-ref**: distinct from [Settings](../icon-vocabulary.md#settings) gear and [Filter / Sort](../icon-vocabulary.md#filter--sort) sliders — EQ has staggered asymmetric bars

### Queue / Up Next
- **Meaning**: List of upcoming tracks
- **Recommended forms**: stacked horizontal lines (3 lines) with prefix indicator (small triangle or hamburger lozenge on left); or 3 lines of equal length
- **Cliché**: shopping-cart (means commerce); plain hamburger (means nav drawer)
- **Reference**: Spotify queue button; YouTube Music queue tab
- **Universal vocabulary cross-ref**: NOT [Menu / Hamburger](../icon-vocabulary.md#menu--hamburger) — queue lines have leading marker

### Shuffle
- **Meaning**: Random play order
- **Recommended forms**: two crossing arrows (X-pattern), arrow heads at both ends, slight curve to suggest the swap
- **Cliché**: dice (means gaming/random); zigzag arrow (looks like trending)
- **Reference**: Spotify shuffle (current is enhanced shuffle sparkle variant — note dual-state pair)

### Repeat (all / one)
- **Meaning**: Loop playback, with numeric variant for repeat-one
- **Recommended forms**: circular arrow (one full loop, single arrowhead); for repeat-one add tiny "1" inside or to side
- **Cliché**: refresh icon (looks identical — distinguish by adding loop closure point + number variant)
- **Reference**: Spotify repeat (3 states cycle: off/all/one)
- **Universal vocabulary cross-ref**: distinct from [Refresh](../icon-vocabulary.md#refresh) — repeat has explicit arrowhead at loop closure

### Lyrics
- **Meaning**: Show synced lyrics view
- **Recommended forms**: speech bubble with horizontal lines (3 lines, stepped — first short, second long, third medium); or quotation-mark glyph
- **Cliché**: musical note (means music in general); microphone (means recording)
- **Reference**: Spotify lyrics overlay; Apple Music synced lyrics
- **Universal vocabulary cross-ref**: similar mass to [Comment](../icon-vocabulary.md#comment) bubble — distinguish with line-pattern stagger

### Podcast
- **Meaning**: Podcast content, episode catalog
- **Recommended forms**: microphone + radio waves, OR rounded square with internal mic silhouette (iOS Podcasts convention)
- **Cliché**: just microphone (ambiguous with voice memo/recording/Siri); radio tower (means broadcast)
- **Reference**: Apple Podcasts app icon (purple square with mic); Pocket Casts
- **Universal vocabulary cross-ref**: extends [Microphone](../icon-vocabulary.md#microphone) — podcast adds broadcast element

### Headphones / Listening
- **Meaning**: Audio output, "listen now", listening party
- **Recommended forms**: simplified arc + two ear cups (3 elements: arc, left cup, right cup)
- **Cliché**: detailed studio cans; earbuds (different metaphor — "wireless audio")
- **Reference**: Spotify Listening toolbar; Apple Music AirPods device picker

### Microphone (recording variant)
- **Meaning**: Record audio (distinct from voice command)
- **Recommended forms**: microphone capsule on stand WITH fill state + red dot indicator at active state; recording mic uses fill when armed, outline when idle
- **Cliché**: same icon as voice-command (Siri, Google Assistant) — using only color to distinguish fails CVD
- **Reference**: GarageBand record button; Voice Memos
- **Universal vocabulary cross-ref**: extends [Microphone](../icon-vocabulary.md#microphone) — recording = filled state + dot; voice command = outlined

### Waveform
- **Meaning**: Audio file, scrubbing surface, recording in progress
- **Recommended forms**: 5–9 vertical bars at varying heights with mirrored top/bottom symmetry around horizontal axis
- **Cliché**: pulse line (means heartbeat/health); flat sine wave (means signal/wifi)
- **Reference**: SoundCloud waveform scrub bar (industry archetype)
- **Universal vocabulary cross-ref**: similar to [Activity / Feed](../icon-vocabulary.md#activity--feed) "square pulse waveform" — audio waveform has SYMMETRIC mirror around X-axis

### BPM / Tempo
- **Meaning**: Beats per minute, tempo display
- **Recommended forms**: metronome silhouette (triangle pyramid + pendulum); or numeric display 2–3 char fixed-width with small "BPM" label
- **Cliché**: heart icon (mistakes BPM for heart rate); musical note alone
- **Reference**: Beatport DJ; Ableton Note; Pioneer DJ apps

### Key signature
- **Meaning**: Track key (Camelot or musical notation)
- **Recommended forms**: text-only ("Cm", "8A") in circular keyline; not iconographic
- **Cliché**: literal sharp/flat symbols rendered as icons (only musicians read these)
- **Reference**: Beatport; Mixed In Key

### Mixer / Crossfader
- **Meaning**: DJ mix, multi-track mixer
- **Recommended forms**: two horizontal sliders stacked, OR vertical fader column with raised handle
- **Cliché**: gear (means settings); generic slider (ambiguous)
- **Reference**: djay Pro; Serato; Logic Pro mobile
- **Universal vocabulary cross-ref**: extends [Settings](../icon-vocabulary.md#settings) sliders — mixer is paired faders

### Cast / AirPlay (audio context)
- **Meaning**: Send audio to speaker, AirPods, Sonos
- **Recommended forms**: rectangle with concentric arcs in lower-left (display cast); for audio: speaker silhouette + arcs
- **Cliché**: Bluetooth glyph alone (means pairing, not active casting)
- **Reference**: Spotify Connect device picker; AirPlay
- **Universal vocabulary cross-ref**: extends [Cast / AirPlay](../icon-vocabulary.md#cast--airplay) — audio variant uses speaker base instead of rectangle

### Sleep timer
- **Meaning**: Auto-stop after N minutes
- **Recommended forms**: crescent moon + clock face combined; or timer ring with moon inside
- **Cliché**: just moon (means dark mode); just timer (means stopwatch)
- **Reference**: Spotify sleep timer; Audible sleep timer
- **Universal vocabulary cross-ref**: extends [Theme / Appearance](../icon-vocabulary.md#theme--appearance) moon and [Timer / Stopwatch](../icon-vocabulary.md#timer--stopwatch)

### Download for offline
- **Meaning**: Save track for offline play (distinct from generic file download)
- **Recommended forms**: down-arrow + horizontal line (universal download); but with state-pair: outlined-circle (idle), partial-fill arc (downloading), filled-check (downloaded)
- **Cliché**: same icon as web download with no state progression
- **Reference**: Spotify download toggle (3-state circle); Apple Music
- **Universal vocabulary cross-ref**: extends [Download](../icon-vocabulary.md#download) — music adds 3-state progress

### Playlist (collaborative, smart, generated)
- **Meaning**: Curated track collection — distinct from generic "list"
- **Recommended forms**: 3 stacked horizontal lines with note glyph attached top-left, OR rectangle with internal lines + small "+" or AI-sparkle for generated/smart variant
- **Cliché**: generic list (loses "music" semantic); folder (loses "ordered" semantic)
- **Reference**: Spotify Daylist (with AI-sparkle); Apple Music Smart Playlists
- **Universal vocabulary cross-ref**: distinct from [Library / Collection / Saved](../icon-vocabulary.md#library--collection--saved) which is the WHOLE user collection

### Shuffle Play (combined CTA)
- **Meaning**: Big primary action — "shuffle play this album"
- **Recommended forms**: filled circular button containing shuffle X-arrow with optional play triangle inside
- **Cliché**: just play button (loses shuffle); just shuffle (loses CTA primacy)
- **Reference**: Spotify album header CTA

### Liked Songs
- **Meaning**: User's personal favorites collection
- **Recommended forms**: heart-filled inside gradient or solid square keyline (Spotify convention)
- **Cliché**: outlined heart only (no container — gets lost in album-cover grid)
- **Reference**: Spotify Liked Songs (purple gradient + filled heart)
- **Universal vocabulary cross-ref**: extends [Like / Favorite](../icon-vocabulary.md#like--favorite) — Liked Songs needs the CONTAINED keyline

### Connect / Devices
- **Meaning**: Device picker for output (speaker, AirPods, car)
- **Recommended forms**: speaker + arcs (active); 2–3 device silhouettes in row (picker)
- **Cliché**: Bluetooth glyph (means pairing, not active connection)
- **Reference**: Spotify Connect; Sonos device picker

### Radio (station / mix)
- **Meaning**: Algorithmic infinite mix from a seed
- **Recommended forms**: tower with radiating arcs, OR tuning dial silhouette
- **Cliché**: car radio (anachronistic); tower with too many arcs
- **Reference**: Pandora; Apple Music Stations
- **Universal vocabulary cross-ref**: similar to [Live / Broadcast](../icon-vocabulary.md#live--broadcast) — radio differs by tower base

### Voice clip / Voice note (in audio app)
- **Meaning**: Audio message
- **Recommended forms**: waveform inside chat bubble OR mic + bubble
- **Reference**: WhatsApp voice notes (cross-domain); Voice Tweet

## Cliché map for music

| Cliché | Why it fails | Alternative |
|---|---|---|
| Heart for "favorite" everywhere AND BPM | Conflates emotional/musical | Heart for Liked Songs only; metronome for BPM |
| Single microphone for record + voice cmd + podcast | Three meanings on one shape | Recording = filled mic + dot; Voice cmd = outlined; Podcast = mic + waves |
| Repeat = refresh visually | Same form, different meaning | Repeat closes loop with explicit arrowhead at convergence |
| Vinyl with detailed grooves at 20pt | Moiré pattern, unrecognizable | Single concentric ring + center dot |
| Musical note for "audio settings" | Note means music itself | EQ bars (asymmetric) |
| Square waveform for music | Heartbeat reads as health | Symmetric mirrored bars |
| 7+ EQ bars for "settings" | Collapses at 20pt | 3–5 staggered bars |
| Color-only state for download progress | CVD-unsafe | 3-state shape progression: outline → arc → filled-check |

## State-pair examples

1. **Play / Pause / Buffering / Error / Cast-active** — 5-state primary control
2. **Shuffle off / on / enhanced (sparkle)** — Spotify-pioneered 3-state
3. **Repeat off / repeat-all / repeat-one** — 3-state with badge
4. **Download idle / downloading / downloaded** — 3-state circle
5. **Like outlined / Like filled** — same as universal heart pair, high frequency

## Industry-leading reference

Spotify mobile (iOS+Android) for now-playing row, queue/lyrics/cast lozenge, 3-state shuffle/repeat. Apple Music (iOS) for SF-Symbol austerity. Pocket Casts for filtered-queue and variable-speed. djay Pro for crossfader and beat-sync.

## Universal vocabulary integration

[Play / Pause / Skip Forward / Skip Back / Volume / Mute / Cast / Microphone](../icon-vocabulary.md#media--playback) all in Media & Playback. Music doesn't redefine — uses + adds music-specific layer above. Like/Heart in [Like / Favorite](../icon-vocabulary.md#like--favorite). Library in [Library / Collection / Saved](../icon-vocabulary.md#library--collection--saved). Sleep timer composes [Theme / Appearance](../icon-vocabulary.md#theme--appearance) moon + [Timer / Stopwatch](../icon-vocabulary.md#timer--stopwatch).
