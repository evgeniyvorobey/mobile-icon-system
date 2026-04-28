# Finance & Banking

## Industry overview

Finance apps (Robinhood, Wealthfront, Coinbase, Cash App, Venmo, Zelle, Chime, Revolut, Wise, Stripe Dashboard, Square, QuickBooks Self-Employed, YNAB, Mint, Plaid, Fidelity, Schwab, Vanguard, M1, Public, eToro, Binance) are the **most cliché-prone domain** in mobile design because non-finance designers default to symbols (`$`, `€`, `£`) and red/green color encoding that fail CVD and internationalization simultaneously. Robinhood's 2020 outage post-mortem mentioned "candlestick green-only" issue — investors with deuteranopia could not tell up days from down days. Robinhood pioneered the portfolio donut on mobile; their main chart is a sparse line chart, not a candlestick (illegible at phone width). Stripe Dashboard mobile uses ledger-style transaction lists with leading icons (debit/credit/refund/dispute/payout) where leading shape (not color) carries meaning. Cash App pioneered single-button send conflating payment with messaging — followed by Venmo, Zelle. Finance has severe regulatory and trust constraints: ambiguous icons can produce wrong-account transfers, missed deadlines, disputed charges.

## Metaphor catalog

### Candlestick chart
- **Meaning**: OHLC price visualization
- **Recommended forms**: 3 candlesticks with body + wicks, alternating up/down with shape encoding (up = wick at top + body below; down = wick at bottom + body above) — or up/down chevron paired alongside
- **Cliché**: single candle with green-only fill (CVD-unsafe); too many candles (illegible at 20pt)
- **Cross-cultural**: body-color convention varies (Asia commonly inverts: red=up, green=down) — pair shape with color always
- **Reference**: Robinhood "Candlestick" toggle (study how Robinhood does NOT use candlesticks as default); TradingView mobile; Webull; eToro

### Ticker / Stock symbol
- **Meaning**: Specific security
- **Recommended forms**: ticker text in monospace inside rounded badge ("AAPL", "TSLA"), 3–5 chars max
- **Cliché**: small company-logo PNG inside icon (couples brand to third party + breaks at retina)
- **Reference**: Robinhood; Public; Yahoo Finance

### Portfolio donut
- **Meaning**: Allocation by asset class / sector
- **Recommended forms**: 3–5 segment donut with stroke-only segments OR filled segments with patterned encoding for CVD; center number for total
- **Cliché**: pie chart with 12 slivers (illegible); rainbow palette (CVD-unsafe)
- **Reference**: Wealthfront; M1 Finance "Pie"; Schwab
- **Universal vocabulary cross-ref**: extends [Progress](../icon-vocabulary.md#progress) "filled arc on circle" — portfolio is segmented arc

### Dividend
- **Meaning**: Income payment from holding
- **Recommended forms**: coin + drop arrow OR coin + percentage OR small calendar marker on a coin
- **Cliché**: dollar sign alone; flowing-cash animation (Lottie-only, fails static)
- **Reference**: Robinhood dividend page; Public; Schwab
- **Universal vocabulary cross-ref**: composes [Cash / Money](../icon-vocabulary.md#cash--money) coin + [Calendar](../icon-vocabulary.md#calendar)

### Ledger / Transactions
- **Meaning**: List of debits/credits over time
- **Recommended forms**: rectangle with horizontal lines + leading icon column; on mobile prefer LIST OF TRANSACTION CELLS with shape-encoded leading icons rather than literal ledger metaphor
- **Cliché**: literal accounting ledger book on mobile (too dense); column of dollar signs
- **Reference**: Stripe Dashboard mobile transactions list; QuickBooks; Mint
- **Universal vocabulary cross-ref**: extends [Receipt / Order](../icon-vocabulary.md#receipt--order) — finance ledger is denser

### Statement
- **Meaning**: Periodic account summary (PDF or screen)
- **Recommended forms**: document silhouette + fold + small "PDF" or month-marker
- **Cliché**: detailed paper with logo
- **Reference**: Chase mobile statements; Schwab
- **Universal vocabulary cross-ref**: extends [Document](../icon-vocabulary.md#document)

### Tax document (W-2, 1099, K-1)
- **Meaning**: Year-end tax form, time-sensitive
- **Recommended forms**: document silhouette + small "TAX" or year badge; never bald "W-2" — doc shape carries metaphor
- **Cliché**: percentage symbol alone (means discount); briefcase (means business)
- **Cross-cultural**: tax-form labels are jurisdictional; the icon must be document-shaped, not text-shaped
- **Reference**: Robinhood Tax Center; TurboTax; H&R Block
- **Universal vocabulary cross-ref**: extends [Document](../icon-vocabulary.md#document)

### Transfer (internal vs external)
- **Meaning**: Move money between accounts
- **Recommended forms**: two arrows facing opposite directions between two account silhouettes; or single arrow from account A → account B
- **Cliché**: just circular arrow (means refresh); just two arrows (means swap)
- **Reference**: Wise transfer flow; Revolut; Chime
- **Universal vocabulary cross-ref**: distinct from [Send](../icon-vocabulary.md#send) — transfer is between USER's accounts; send is to third party

### ACH / Bank transfer
- **Meaning**: Slow rail bank-to-bank
- **Recommended forms**: bank silhouette (columned building) + arrow; or "ACH" badge inside bank icon
- **Cliché**: same icon as wire transfer (different rail, different speed)
- **Cross-cultural**: ACH is US-specific; for international apps use SEPA/SWIFT/Faster Payments labels
- **Reference**: Plaid; Stripe

### Wire transfer
- **Meaning**: Fast irreversible international transfer
- **Recommended forms**: globe + arrow OR bank + lightning bolt
- **Cliché**: confused with ACH — wire MUST visually signal speed (lightning) or distance (globe)
- **Reference**: Wise wire option; Citibank international transfer

### Exchange / Swap
- **Meaning**: FX, crypto swap, asset rotation
- **Recommended forms**: two arrows in horizontal opposition (left↔right) or vertical opposition between two asset symbols
- **Cliché**: refresh arrows (means reload); single arrow (means transfer one-way)
- **Reference**: Coinbase swap; Wise FX; Revolut
- **Universal vocabulary cross-ref**: distinct from [Refresh](../icon-vocabulary.md#refresh) and Transfer

### Watchlist
- **Meaning**: Tracked but not owned securities
- **Recommended forms**: eye + list, OR star + list, OR bookmark + list
- **Cliché**: same icon as portfolio (different concept — watch ≠ own)
- **Reference**: Robinhood watchlists; Yahoo Finance; Webull
- **Universal vocabulary cross-ref**: composes [Eye / Visibility](../icon-vocabulary.md#eye--visibility) + list, OR [Like / Favorite](../icon-vocabulary.md#like--favorite) + list

### Insights / Analytics graph
- **Meaning**: Spending/saving trends over time
- **Recommended forms**: bar chart (3 bars varying height) OR line chart with single peak
- **Cliché**: cluttered chart with axes and labels (illegible at 20pt)
- **Reference**: Mint insights; YNAB reports; Cleo
- **Universal vocabulary cross-ref**: distinct from [Trending](../icon-vocabulary.md#trending) (single arrow) — insights = bars

### Gain / Loss indicator (paired)
- **Meaning**: Up/down change with magnitude
- **Recommended forms**: up-chevron + value text in tinted color (gain), down-chevron + value text (loss); MUST pair shape with color
- **Cliché**: green/red color only (CVD fail); plus/minus alone (ambiguous with add/remove)
- **Cross-cultural**: chevron+color universal; color reversed in some Asian markets — let users pick palette
- **Reference**: Robinhood gain/loss row; Public; Schwab; Bloomberg mobile
- **Universal vocabulary cross-ref**: composes [Back / Forward](../icon-vocabulary.md#back--forward) chevron concept

### IRA / 401k / Retirement account
- **Meaning**: Tax-advantaged retirement account
- **Recommended forms**: pig-bank-with-clock-overlay OR account silhouette + small "R" badge OR horizon-line (long-term icon)
- **Cliché**: just a piggy bank (US-centric, also means generic savings)
- **Cross-cultural**: retirement-account concept exists internationally (ISA, RRSP) — use abstract account+horizon, not literal pig
- **Reference**: Wealthfront retirement goals; Fidelity; Schwab

### Crypto wallet
- **Meaning**: On-chain wallet (distinct from fiat wallet)
- **Recommended forms**: hexagon (chain motif) + wallet silhouette, OR wallet with tiny chain link badge
- **Cliché**: literal Bitcoin "B" inside (couples brand to one chain); silver coin
- **Reference**: Coinbase Wallet; MetaMask mobile; Phantom
- **Universal vocabulary cross-ref**: extends [Wallet](../icon-vocabulary.md#wallet)

### Recurring deposit / Auto-invest
- **Meaning**: Scheduled investment
- **Recommended forms**: circular arrow + cash, OR calendar + arrow into account
- **Cliché**: just refresh (loses financial context)
- **Reference**: Wealthfront recurring; M1 Smart Transfers; Acorns Round-Ups
- **Universal vocabulary cross-ref**: composes [Refresh](../icon-vocabulary.md#refresh) + [Cash / Money](../icon-vocabulary.md#cash--money)

### Pending / Cleared / Disputed (transaction states)
- **Meaning**: Transaction lifecycle state
- **Recommended forms**: pending = clock-in-circle; cleared = check-in-circle; disputed = exclamation-in-shield
- **Cliché**: color-only states (CVD); no shape change
- **Reference**: Stripe Dashboard transaction states; Chase; Wise

### Limit / Stop order
- **Meaning**: Conditional trade order
- **Recommended forms**: horizontal line crossed by arrow (limit); horizontal line with arrow stopping at it (stop)
- **Cliché**: just arrow (loses conditional)
- **Reference**: Robinhood order types; Schwab StreetSmart

### KYC / Verification
- **Meaning**: Identity verification, regulatory check
- **Recommended forms**: person silhouette + check, OR ID-card silhouette + check
- **Cliché**: shield alone (means generic security)
- **Reference**: Plaid Identity; Onfido; Persona
- **Universal vocabulary cross-ref**: composes [Profile / Account / Me](../icon-vocabulary.md#profile--account--me) + [Success](../icon-vocabulary.md#success)

### Round-up / Spare change
- **Meaning**: Acorns-style round-up to invest
- **Recommended forms**: coin + up arrow + small "+", or stack-of-coins growing
- **Cliché**: just a coin
- **Reference**: Acorns; Chime Save When I Spend; Cash App rounds
- **Universal vocabulary cross-ref**: extends [Cash / Money](../icon-vocabulary.md#cash--money)

### Bank (institution)
- **Meaning**: Bank account, financial institution
- **Recommended forms**: columned building (3 columns + roof + base) — universal bank silhouette
- **Cliché**: piggy bank (means savings, not bank); generic building
- **Reference**: Plaid bank picker; Mint accounts list

## Cliché map for finance

| Cliché | Why it fails | Alternative |
|---|---|---|
| Dollar sign `$` everywhere | Locale-fail | Currency-agnostic: bills + coin; numbers in monospace |
| Green/red as the only gain/loss signal | CVD fail; cultural inversion in Asia | Chevron up/down + tint; let user pick palette |
| Single candlestick at 20pt | Wick + body unreadable | Sparkline as default; candlestick only at chart-detail size |
| Literal accounting ledger book | Anachronistic; dense | Transaction list cells with shape-encoded leading icons |
| Briefcase = "investing" | Means business/work | Portfolio donut for investing; briefcase for business account |
| Same icon for ACH / Wire / Internal | Three rails, three risks, one shape | ACH = bank+arrow; Wire = lightning+bank; Internal = swap |
| Padlock for "secure transfer" | Means generic security | Shield + check for verified |
| `%` for both interest and discount | Conflates two concepts | Interest = arc on circle; Discount = tag |
| Detailed credit card with logo | Brand-couples to one issuer | Generic chip-card silhouette |
| Coin spinning Lottie as success | Animation-only confirms | Static check-in-circle as primary |

## State-pair examples

1. **Gain / Loss / Flat** — 3-state row icon
2. **Pending / Cleared / Failed (transaction)** — 3-state list-cell prefix
3. **KYC: Not started / In review / Verified / Rejected** — 4-state
4. **Watchlist outline / Watchlist added** — toggle pair
5. **Order open / filled / cancelled** — 3-state

## Industry-leading reference

Robinhood (sparkline-first chart language, gain/loss chevron pair). Stripe Dashboard mobile (transaction list density, leading-shape encoding). Wise (cross-border transfer flows, rail-distinguishing icons). Wealthfront (portfolio donut, goals donut-with-ring). Cash App (conflated send/pay/message metaphor). Coinbase (swap, on-chain wallet vocabulary).

## Universal vocabulary integration

[Cash, Card, Wallet, Tag, Receipt, Gift](../icon-vocabulary.md#commerce--wallet) in Commerce & Wallet. [Lock, Shield, Eye, Fingerprint, Face](../icon-vocabulary.md#security--privacy) in Security & Privacy (used heavily for transaction confirmation). [Trending arrow](../icon-vocabulary.md#trending) (but finance prefers explicit chevron+value). [Document](../icon-vocabulary.md#document) (basis for Statement, Tax). [Refresh](../icon-vocabulary.md#refresh) (basis for Recurring; never reuse for Repeat in audio).
