# Health & Wellness

## Industry overview

Health apps span medical (MyChart, Epic, Doximity), fitness (Strava, Nike Training, Peloton, Apple Fitness, Garmin), nutrition (MyFitnessPal, Cronometer, Yazio), sleep (Oura, Whoop, Sleep Cycle), mindfulness (Headspace, Calm, Insight Timer, Balance), and women's health (Flo, Clue, Natural Cycles). The domain has **the highest state-pair complexity** of any consumer category because almost every metaphor has a temporal dimension (scheduled/done/missed/skipped) and a measurement dimension (low/normal/high/critical). Apple Health pioneered activity rings (Move/Exercise/Stand). Headspace established the breathing-circle. Strava's segments page introduced the trophy + leaderboard pattern. Whoop introduced the strain/recovery dual gauge. One Medical's app uses dose-clock state pairing. The cliché-trap density is moderate but high-stakes: a "missed dose" icon that looks like "taken" is a clinical-safety failure, not a polish issue.

## Metaphor catalog

### Pulse waveform (heart rate)
- **Meaning**: Live heart rate, vitals
- **Recommended forms**: ECG-style line with 1 QRS spike (not flat sine), or simplified peak; pair with bpm number
- **Cliché**: square pulse waveform (means activity feed, not pulse); flat sine (means signal)
- **Reference**: Apple Health heart rate; Whoop; Oura
- **Universal vocabulary cross-ref**: distinct from [Activity / Feed](../icon-vocabulary.md#activity--feed) "square pulse" — health pulse is SPIKY ASYMMETRIC

### Vitals (heart, O2, temperature, BP)
- **Meaning**: Specific vital sign readings
- **Recommended forms**: heart (HR) — but with ANATOMICAL heart asymmetry (Phosphor-style) not romantic heart; lung silhouette for O2; thermometer for temp; cuff for BP
- **Cliché**: romantic heart for HR (conflates with like/favorite); generic drop for O2
- **Reference**: Apple Health vitals; Doximity; MyChart vitals page
- **Universal vocabulary cross-ref**: distinct from [Like / Favorite](../icon-vocabulary.md#like--favorite) heart — health uses anatomical asymmetric form

### Prescription / Rx
- **Meaning**: Medication, prescription
- **Recommended forms**: pill capsule (two-color split), OR "Rx" inside rounded square, OR pill bottle silhouette
- **Cliché**: aspirin tablet (over-detailed); skull (toxic stigma)
- **Cross-cultural**: capsule universal; "Rx" symbol US/UK only
- **Reference**: GoodRx; Walgreens app; CVS app; One Medical

### Dose timer / Medication reminder
- **Meaning**: Take medication at scheduled time
- **Recommended forms**: pill + clock face; OR pill in circle with progress arc
- **Cliché**: just alarm bell (loses medication); just pill (loses time)
- **Reference**: Medisafe; Apple Health Medications; CVS
- **Universal vocabulary cross-ref**: composes Pill + [Clock / Time](../icon-vocabulary.md#clock--time)

### Symptom log
- **Meaning**: Track symptoms over time
- **Recommended forms**: clipboard with check + plus, OR document with body-silhouette inside
- **Cliché**: stethoscope (means doctor visit); ambulance
- **Reference**: Bearable; Apple Health Symptoms; Flo cycle log
- **Universal vocabulary cross-ref**: extends [Document](../icon-vocabulary.md#document)

### Sleep cycle / Sleep stage
- **Meaning**: Sleep tracking, stages (REM, deep, light)
- **Recommended forms**: crescent moon + stars (sleep), wave-pattern (cycle stages)
- **Cliché**: bed silhouette (means lodging); ZZZ (cartoonish)
- **Reference**: Oura sleep score; Whoop; Sleep Cycle; Apple Health Sleep
- **Universal vocabulary cross-ref**: extends [Theme / Appearance](../icon-vocabulary.md#theme--appearance) moon

### Mindfulness / Meditation
- **Meaning**: Guided session, breath work
- **Recommended forms**: breathing circle (single concentric circle pair), OR lotus silhouette (cultural sensitivity warning), OR "Om" mark in CJK markets
- **Cliché**: literal seated yogi (gendered, culturally specific); Buddhist symbols in non-Buddhist apps
- **Cross-cultural**: concentric circle is safest; lotus reads spiritual not religious in most markets but verify
- **Reference**: Headspace breathing circle; Calm pulsing dot; Insight Timer

### Workout type catalog (run, cycle, swim, lift, yoga, HIIT)
- **Meaning**: Activity type selector
- **Recommended forms**: figure silhouette in motion specific to activity — runner, cyclist, swimmer, dumbbell for lift; consistent stick-figure grammar across set
- **Cliché**: gendered figures; detailed sport equipment
- **Reference**: Apple Workouts type picker; Strava sport selector; Garmin Connect
- **Universal vocabulary cross-ref**: extends [Profile / Account / Me](../icon-vocabulary.md#profile--account--me) figure

### Hydration
- **Meaning**: Water intake tracking
- **Recommended forms**: water drop (filled), or glass with fill-level
- **Cliché**: cloud-with-raindrop (means weather)
- **Reference**: Plant Nanny; WaterMinder; Apple Health Hydration

### Calories / Energy
- **Meaning**: Caloric intake or burn
- **Recommended forms**: flame silhouette, OR circular ring with center number
- **Cliché**: literal apple icon; fork + knife (means meal, not calories)
- **Reference**: MyFitnessPal; Apple Move ring; Lose It!
- **Universal vocabulary cross-ref**: distinct from [Trending](../icon-vocabulary.md#trending) flame — health flame is for calories specifically

### Macros (protein, carb, fat)
- **Meaning**: Macronutrient breakdown
- **Recommended forms**: 3-segment donut OR 3 horizontal stacked bars; consistent color encoding across app
- **Cliché**: just numbers; pie chart with too many slivers
- **Reference**: Cronometer; MacroFactor; Yazio
- **Universal vocabulary cross-ref**: extends Portfolio donut concept (finance) — same shape, different domain

### Activity rings
- **Meaning**: Daily goal progress (Apple Move/Exercise/Stand)
- **Recommended forms**: 3 nested circles with stroke-fill state showing progress
- **Cliché**: 5+ rings (illegible); rings without center text
- **Reference**: Apple Health/Fitness rings (canonical); Fitbit Today
- **Universal vocabulary cross-ref**: extends [Progress](../icon-vocabulary.md#progress) — health uses 3 NESTED arcs

### Streak / Consistency
- **Meaning**: Consecutive days of activity
- **Recommended forms**: flame + number badge OR row of dots
- **Cliché**: trophy (means achievement, different concept)
- **Reference**: Apple Streaks; Duolingo (cross-domain); Streaks app
- **Universal vocabulary cross-ref**: distinct from [Trending](../icon-vocabulary.md#trending)

### Period / Cycle
- **Meaning**: Menstrual cycle phase
- **Recommended forms**: drop + small marker for flow day; circle with phase segment for cycle overview
- **Cliché**: medicalized symbols; flowers (cute-washing clinical metric)
- **Cross-cultural**: highly sensitive; provide settings for symbol style
- **Reference**: Flo; Clue; Natural Cycles; Apple Health Cycle Tracking

### Mental wellness mood
- **Meaning**: Mood log (great/good/neutral/low/bad)
- **Recommended forms**: 5-point face scale (NOT just emoji — needs to ship offline as part of icon set), OR 5 weather glyphs (sun → rain)
- **Cliché**: smiley faces (juvenile); "thumbs up/down" (binary not enough)
- **Cross-cultural**: facial expressions read globally; verify smile vs neutral conventions
- **Reference**: Daylio; How We Feel; Apple Health State of Mind

### Telehealth / Video consult
- **Meaning**: Video call with provider
- **Recommended forms**: video camera + medical cross OR simplified screen + provider silhouette
- **Cliché**: just video camera (no medical context); literal stethoscope
- **Reference**: Doxy.me; Teladoc; One Medical; MDLIVE
- **Universal vocabulary cross-ref**: extends [Video Call](../icon-vocabulary.md#video-call)

### Lab results
- **Meaning**: Bloodwork, test results
- **Recommended forms**: test tube silhouette + check OR document with results bars inside
- **Cliché**: just test tube (means science generally)
- **Reference**: MyChart Labs; Quest Diagnostics; Labcorp
- **Universal vocabulary cross-ref**: extends [Document](../icon-vocabulary.md#document)

### Steps / Pedometer
- **Meaning**: Daily step count
- **Recommended forms**: footprint OR shoe silhouette OR running figure with number
- **Cliché**: literal footprint with toe-detail (over-detailed)
- **Reference**: Apple Steps; Fitbit; Pedometer++

### Care team / Provider
- **Meaning**: Doctor, nurse, specialist
- **Recommended forms**: person silhouette + medical cross badge OR stethoscope on person
- **Cliché**: gendered doctor figure
- **Reference**: One Medical; MyChart; Doximity
- **Universal vocabulary cross-ref**: extends [Profile / Account / Me](../icon-vocabulary.md#profile--account--me)

### Body silhouette (for symptom mapping)
- **Meaning**: Tap a body part to log
- **Recommended forms**: front + back outline of human body, gender-neutral, 16-20pt scaled
- **Cliché**: gendered (Vitruvian Man), too detailed musculature
- **Reference**: Apple Health body areas; Bearable
- **Universal vocabulary cross-ref**: extends [Profile / Account / Me](../icon-vocabulary.md#profile--account--me)

## Cliché map for health

| Cliché | Why it fails | Alternative |
|---|---|---|
| Romantic heart for heart rate | Conflates love and pulse | Anatomical heart for HR; romantic heart for like only |
| Square pulse waveform for vitals | Means activity feed | ECG-spike asymmetric for vitals |
| Stethoscope for "telehealth" | Means doctor visit | Video camera + medical cross |
| Pill bottle for "medication reminder" | Loses time context | Pill + clock |
| Bed for "sleep tracking" | Means lodging | Moon + stars |
| Yogi figure for "mindfulness" | Gendered, culturally narrow | Concentric breathing circle |
| Gendered runner for workouts | Excludes; reads as binary | Neutral stick figure in motion |
| Smiley emoji for mood | Juvenile; no clinical credibility | 5-point neutral face scale OR weather glyphs |
| Trophy for streaks | Means achievement | Flame + number badge |
| Cross alone for "medical" | Religious in some markets | Cross inside circle/square keyline |

## State-pair examples

1. **Dose: scheduled / taken / late / missed / skipped** — 5-state
2. **Activity ring: 0% / 25% / 50% / 75% / 100% / >100% (over)** — 6-state arc fill
3. **Heart rate zone: rest / fat-burn / cardio / peak / max** — 5-state
4. **Cycle phase: menstrual / follicular / ovulation / luteal** — 4-state segment
5. **Mood: 1–5** — 5-state face/weather pair

## Industry-leading reference

Apple Health/Fitness (activity rings, vitals catalog, medication dose-state set). Headspace (breathing-circle, session-state pair). Strava (workout-type silhouettes, segment leaderboard). Flo/Clue (menstrual cycle visualization). One Medical (telehealth + dose-timer integration). MyChart (medical-record and lab-results vocabulary).

## Universal vocabulary integration

Heart in [Like / Favorite](../icon-vocabulary.md#like--favorite) (but health uses anatomical variant). [Calendar](../icon-vocabulary.md#calendar) / [Clock](../icon-vocabulary.md#clock--time) / [Timer](../icon-vocabulary.md#timer--stopwatch) in Time & Schedule (basis for dose timer). [Document](../icon-vocabulary.md#document) in Document (basis for symptom log, lab results). [Profile / Person](../icon-vocabulary.md#profile--account--me) in Profile (basis for care team, body silhouette). [Video Call](../icon-vocabulary.md#video-call) in Video Call (basis for telehealth). [Bell / Notification](../icon-vocabulary.md#notifications--inbox) — health overuses; prefer dose-clock for medication reminders. Moon in [Theme / Appearance](../icon-vocabulary.md#theme--appearance) (basis for sleep).
