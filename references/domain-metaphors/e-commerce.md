# E-commerce & Shopping

## Industry overview

E-commerce apps include marketplaces (Amazon, eBay, Walmart, Target), DTC (Allbirds, Glossier), aggregators (Shopify Shop, Klarna), resale (Depop, Vinted, Poshmark), grocery (Instacart, DoorDash, Uber Eats), and subscription (Stitch Fix, Birchbox). The domain reuses universal Cart/Bag/Wallet vocabulary heavily but adds product variant, review system, wishlist (distinct from favorite), and fulfillment tracking. Amazon pioneered the delivery progress bar with named milestones. Shopify's mobile checkout established the Apple Pay button → checkmark flow. Stitch Fix's app showed how wishlist vs favorite vs cart are three distinct user actions.

## Metaphor catalog

### Product variant (size / color)
- **Recommended forms**: small swatch grid (color), or labeled size buttons (S/M/L)
- **Cliché**: dropdown chevron (loses visual variant); sliders (means settings)
- **Reference**: Allbirds product page; Nike SNKRS size picker

### Size chart
- **Recommended forms**: ruler silhouette OR person silhouette + measurement lines
- **Cliché**: tape measure (over-detailed); tag with text
- **Reference**: Asos size guide; Nike size chart

### Color swatch
- **Recommended forms**: small filled circle in product color, with checkmark for selected; group of 3–5 swatches
- **Cliché**: rainbow swatch (CVD-unsafe; cluttered)
- **Reference**: Glossier color picker; Sephora

### Review stars (display) vs Rating (input)
- **Recommended forms**: 5 filled stars with last partial-fill; for input, stars with tap state
- **Cliché**: same icon for display and input (different interaction)
- **Reference**: Amazon stars; Yelp; Google Reviews
- **Universal vocabulary cross-ref**: extends [Star / Rating](../icon-vocabulary.md#star--rating) — distinguish display vs input states

### Wishlist
- **Recommended forms**: bookmark + cart OR list with star OR ribbon
- **Cliché**: heart (conflates with social favorite/like)
- **Reference**: Amazon wishlists; Stitch Fix favorites; Etsy lists
- **Universal vocabulary cross-ref**: distinct from [Like / Favorite](../icon-vocabulary.md#like--favorite) heart

### Tracking / Fulfillment
- **Recommended forms**: truck silhouette + arrow OR dotted line on map OR progress milestone bar
- **Cliché**: package box alone (loses tracking)
- **Reference**: Amazon Map Tracking; Shop app; FedEx mobile

### Return / Refund
- **Recommended forms**: package + back arrow (return); cash + back arrow (refund)
- **Cliché**: just back arrow (loses commerce); X (means cancel)
- **Reference**: Amazon returns; Klarna refunds; Stripe Dashboard refund
- **Universal vocabulary cross-ref**: composes [Back / Forward](../icon-vocabulary.md#back--forward) + Package

### Gift card / Voucher
- **Recommended forms**: card silhouette + bow OR card with gift wrapping
- **Cliché**: just gift box (means physical gift); just card (means payment)
- **Reference**: Amazon gift cards; Apple Gift; Sephora
- **Universal vocabulary cross-ref**: composes [Card](../icon-vocabulary.md#card) + [Gift](../icon-vocabulary.md#gift)

### Loyalty points / Rewards
- **Recommended forms**: star + number OR coin + sparkle OR diamond/gem
- **Cliché**: trophy (means achievement)
- **Reference**: Starbucks Stars; Sephora Beauty Insider; United MileagePlus

### Promo code / Coupon
- **Recommended forms**: tag + percent OR ticket silhouette
- **Cliché**: just percent symbol (ambiguous with stats)
- **Reference**: Honey browser extension; Klarna offers; Rakuten

### Quick view / Preview
- **Recommended forms**: eye icon OR magnifying glass + plus
- **Cliché**: search (means find)
- **Reference**: Asos quick view; Amazon overlay
- **Universal vocabulary cross-ref**: extends [Eye / Visibility](../icon-vocabulary.md#eye--visibility)

### Add to cart vs Buy now
- **Recommended forms**: cart + plus (add); cart + arrow / lightning (buy now)
- **Cliché**: same icon for both (different intent)
- **Reference**: Amazon Buy Now; Shop Pay express checkout

### Stock indicator / Inventory
- **Recommended forms**: filled box (in stock); half-fill (low); empty box + slash (out)
- **Cliché**: color-only (CVD-fail)
- **Reference**: Best Buy stock badges; Amazon "Only 2 left"

### Subscribe & Save / Recurring order
- **Recommended forms**: cart + circular arrow OR box + calendar
- **Cliché**: just refresh (loses commerce)
- **Reference**: Amazon Subscribe & Save; Thrive Market

### Pickup / Curbside
- **Recommended forms**: storefront + person OR car + bag
- **Cliché**: just a store (loses pickup context)
- **Reference**: Target Drive Up; Walmart curbside; Apple In-Store Pickup

### Try-on (AR)
- **Recommended forms**: camera + face/box outline + sparkle
- **Cliché**: just camera (loses AR)
- **Reference**: Warby Parker; Sephora Virtual Artist; IKEA Place

### Reviews vs Ratings (entry points)
- **Recommended forms**: speech bubble + star (reviews); star + plus (rate)
- **Cliché**: stars alone (which one?)
- **Reference**: Yelp; Trustpilot; Google Reviews

### Compare products
- **Recommended forms**: 2 rectangles with center divider OR scale icon
- **Cliché**: split-screen (means picture-in-picture)
- **Reference**: Best Buy compare; Wirecutter comparison tables

### Express checkout / Apple Pay / Google Pay
- **Recommended forms**: lightning + payment-method badge
- **Cliché**: just payment method (loses speed)
- **Reference**: Shop Pay; Apple Pay; Google Pay

### Saved address / Saved payment method
- **Recommended forms**: home + checkmark (address); card + check (payment)
- **Cliché**: same as profile/account
- **Reference**: Amazon stored addresses; Apple Pay saved cards

### Question on product (Q&A)
- **Recommended forms**: question mark in speech bubble OR `?` + bubble
- **Cliché**: same as help (different context)
- **Reference**: Amazon Q&A; Best Buy Questions

## Cliché map for e-commerce

| Cliché | Why it fails | Alternative |
|---|---|---|
| Heart for both wishlist and favorite | Three meanings collapse | Heart for personal save; bookmark for wishlist |
| Same icon for cart and buy-now | Different intents | Add = cart+plus; Buy = cart+lightning |
| Star alone for rating + reviews | Loses interaction context | Star+plus for rate; bubble+star for reviews |
| Color swatches without check state | User can't tell selected | Selected swatch with checkmark or border |
| Truck for "delivery" everywhere | Truck=in transit; package=ordered | Use stage-specific icons across milestones |
| Gift box for gift card | Gift box = physical gift | Gift card = card+bow |
| Percent symbol alone | Ambiguous with stats | Tag + percent for promo |
| Bag and cart used interchangeably | Two distinct paradigms | Pick one and use throughout |

## State-pair examples

1. **Stock: In stock / Low / Out** — filled box / half-fill / empty+slash
2. **Order: Placed / Confirmed / Shipped / Out for Delivery / Delivered** — 5-state milestone bar
3. **Wishlist: Out / Added** — bookmark outline / bookmark filled
4. **Cart: Empty / 1 item / N items** — cart / cart+badge "1" / cart+badge "N"
5. **Variant: Available / Selected / Out of stock** — outline / outline+check / outline+slash

## Industry-leading reference

Amazon (delivery tracking, Q&A vocabulary). Allbirds/Nike (product variant pickers). Shop (Shopify) (express checkout). Sephora/Glossier (color swatch + AR try-on). Starbucks (loyalty/rewards system).

## Universal vocabulary integration

[Cart](../icon-vocabulary.md#cart) / [Bag](../icon-vocabulary.md#bag) / [Wallet](../icon-vocabulary.md#wallet) / [Card](../icon-vocabulary.md#card) / [Cash](../icon-vocabulary.md#cash--money) / [Tag](../icon-vocabulary.md#tag--discount) / [Receipt](../icon-vocabulary.md#receipt--order) / [Gift](../icon-vocabulary.md#gift) in Commerce & Wallet. [Star](../icon-vocabulary.md#star--rating) in Star/Rating (basis for reviews + loyalty). [Eye](../icon-vocabulary.md#eye--visibility) in Eye/Visibility (basis for quick view). [Heart](../icon-vocabulary.md#like--favorite) in Like/Favorite (must NOT collapse with wishlist).
