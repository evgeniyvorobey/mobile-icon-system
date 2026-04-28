# Transportation & Maps

## Industry overview

Transportation apps include navigation (Google Maps, Apple Maps, Waze, Citymapper), ridesharing (Uber, Lyft, Grab, Bolt), public transit (Transit, Citymapper, regional transit apps), micromobility (Lime, Bird, Spin), EV charging (PlugShare, ChargePoint, EVgo, Tesla), parking (SpotHero, ParkMobile), and ferries/trains (Trainline, Amtrak). The domain extends universal Map/Pin/Compass vocabulary with mode-specific glyphs (subway, bus, tram, ferry, walk, bike, scooter, e-scooter, EV) and navigation states (turn-by-turn, lane guidance, alternate route). Google Maps' navigation pioneered the lane guidance glyph. Apple Maps' redesigned transit pioneered the mode-specific line glyph. Citymapper's journey planner introduced the multi-modal glyph row. Tesla's mobile app pioneered the EV charging arrival glyph.

## Metaphor catalog

### Turn-by-turn arrow
- **Recommended forms**: blue arrow with directional rotation; chevron path overlay
- **Cliché**: detailed compass (means discover, not navigation)
- **Reference**: Google Maps nav arrow; Apple Maps; Waze
- **Universal vocabulary cross-ref**: extends [Navigation Arrow](../icon-vocabulary.md#navigation-arrow)

### Lane guidance
- **Recommended forms**: 3 vertical chevrons in a row with one highlighted (the correct lane)
- **Cliché**: just one chevron (loses lane context)
- **Reference**: Google Maps lane assist; Waze; Apple Maps
- **Universal vocabulary cross-ref**: distinct from [Back / Forward](../icon-vocabulary.md#back--forward) chevron

### Alternate route
- **Recommended forms**: dashed line + arrow OR fork-in-road
- **Cliché**: refresh (loses route context)
- **Reference**: Google Maps alternate routes; Waze

### Traffic
- **Recommended forms**: car + warning triangle, OR road segments with color (paired with shape)
- **Cliché**: just a car (means rideshare); color-only encoding
- **Reference**: Google Maps traffic toggle; Waze
- **Universal vocabulary cross-ref**: extends [Warning](../icon-vocabulary.md#warning)

### Subway / Metro
- **Recommended forms**: train front silhouette OR stylized "M" inside circle
- **Cliché**: detailed train with cars
- **Reference**: Apple Maps transit modes; Citymapper; Transit

### Bus
- **Recommended forms**: bus silhouette (rectangle with windows + 2 wheels)
- **Cliché**: detailed bus with passengers
- **Reference**: Apple Maps; Citymapper

### Train (regional / intercity)
- **Recommended forms**: train side silhouette OR locomotive + cars
- **Cliché**: detailed steam train (anachronistic)
- **Reference**: Trainline; Amtrak; SBB Mobile

### Tram / Streetcar
- **Recommended forms**: tram silhouette + overhead wire indicator
- **Cliché**: same as bus or train (different mode)
- **Reference**: Citymapper; Apple Maps

### Ferry
- **Recommended forms**: ferry hull silhouette + simple superstructure
- **Cliché**: detailed cruise ship
- **Reference**: Citymapper Sydney ferry; Apple Maps

### Bike / Cycling
- **Recommended forms**: bicycle silhouette (2 wheels + frame triangle)
- **Cliché**: detailed bike with rider; e-bike not distinguished
- **Reference**: Google Maps cycling; Strava; Komoot

### Scooter / E-scooter
- **Recommended forms**: scooter silhouette (2 small wheels + handlebar + deck)
- **Cliché**: same as bike (different mode)
- **Reference**: Lime; Bird; Spin app icons

### EV charging
- **Recommended forms**: lightning bolt + plug OR battery + plug
- **Cliché**: just plug (no EV); just lightning
- **Reference**: PlugShare; ChargePoint; Tesla mobile; Apple Maps EV

### Fuel / Gas station
- **Recommended forms**: pump silhouette
- **Cliché**: detailed pump with hose
- **Reference**: Google Maps gas stations; GasBuddy

### Parking
- **Recommended forms**: "P" inside square keyline
- **Cliché**: car alone (means rideshare)
- **Reference**: SpotHero; ParkMobile; Apple Maps parking

### Walk / Pedestrian
- **Recommended forms**: walking figure silhouette (gender-neutral)
- **Cliché**: gendered figure
- **Reference**: Apple Maps walk; Google Maps walk; crosswalk signs
- **Universal vocabulary cross-ref**: extends [Profile / Account / Me](../icon-vocabulary.md#profile--account--me)

### Drive / Car
- **Recommended forms**: car silhouette (top-down or 3/4 angle)
- **Cliché**: rideshare car (different concept)
- **Reference**: Apple Maps drive; Google Maps drive

### Pickup / Drop-off pin
- **Recommended forms**: pin with leading-letter (A/B), OR pin with car-pickup glyph
- **Cliché**: same as generic pin (loses A/B context)
- **Reference**: Uber pickup pin; Lyft pickup pin
- **Universal vocabulary cross-ref**: extends [Pin / Location](../icon-vocabulary.md#pin--location)

### ETA / Arrival time
- **Recommended forms**: clock + arrival pin OR clock + person
- **Cliché**: just clock (loses arrival)
- **Reference**: Uber driver ETA; Apple Maps ETA
- **Universal vocabulary cross-ref**: extends [Clock / Time](../icon-vocabulary.md#clock--time)

### Multi-modal journey
- **Recommended forms**: row of mode glyphs separated by arrows (walk → bus → walk)
- **Cliché**: single mode (loses multi-modal)
- **Reference**: Citymapper journey row; Transit

### Saved place / Home / Work
- **Recommended forms**: home silhouette (Home); briefcase (Work); pin + heart (saved)
- **Cliché**: generic pin (loses semantic)
- **Reference**: Google Maps Home/Work; Apple Maps Favorites
- **Universal vocabulary cross-ref**: extends [Home / Main](../icon-vocabulary.md#home--main) and [Pin / Location](../icon-vocabulary.md#pin--location)

### Speed limit / Sign
- **Recommended forms**: red-bordered circle with number (Europe) OR rectangle with number (US)
- **Cliché**: just number (loses signage convention)
- **Cross-cultural**: highly regional — provide both conventions
- **Reference**: Waze speed limit display; Google Maps speed

## Cliché map for transportation

| Cliché | Why it fails | Alternative |
|---|---|---|
| Compass for "navigation" | Compass = direction-discover | Arrow for active nav; compass only for "where am I facing" |
| Same icon for car (drive) and car (rideshare) | Two concepts | Drive = car silhouette; Rideshare = car + person |
| Same icon for bus / train / tram | Three modes | Distinct silhouettes per mode |
| Pump with detailed hose | Over-detailed at 20pt | Simplified pump silhouette |
| Plug for EV charging only | Loses EV context | Lightning + plug OR battery + plug |
| Walking figure gendered | Excludes | Neutral silhouette |
| Generic pin for everything | Loses semantic | Pin + leading letter or symbol per type |
| Color-only traffic | CVD-fail | Red/yellow/green PAIRED with shape (X/wave/dash) |

## State-pair examples

1. **Trip: Searching / Found driver / En route / Arriving / Arrived** — 5-state for rideshare
2. **Charging: Available / In use / Out of service / Reserved** — 4-state for EV station
3. **Transit: On time / Delayed / Cancelled** — 3-state for line/route
4. **Saved: Pin / Home / Work / Favorite / Recent** — 5 distinct pin types
5. **Speed: Under limit / At limit / Over limit** — 3-state speedometer

## Industry-leading reference

Google Maps mobile (turn-by-turn, lane guidance, traffic vocabulary). Apple Maps (transit-mode glyph system). Citymapper (multi-modal journey row). Uber/Lyft (rideshare pickup/drop-off pins). PlugShare/Tesla (EV charging vocabulary). Waze (traffic and speed-limit display).

## Universal vocabulary integration

[Pin](../icon-vocabulary.md#pin--location) / [Map](../icon-vocabulary.md#map) / [Compass](../icon-vocabulary.md#compass) / [Navigation Arrow](../icon-vocabulary.md#navigation-arrow) / [Globe](../icon-vocabulary.md#globe) in Location & Maps. [Home](../icon-vocabulary.md#home--main) in Home/Main (basis for saved Home destination). [Clock](../icon-vocabulary.md#clock--time) in Clock/Time (basis for ETA). [Like / Star](../icon-vocabulary.md#like--favorite) in Like (basis for saved place).
