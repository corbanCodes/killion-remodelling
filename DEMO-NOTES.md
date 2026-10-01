# Killion Remodeling — demo notes

Read before the call with Rick. Built 30 Sep 2026 from the phone-call notes.

---

## 1. Two things to confirm before you show him anything

### The business name spelling

The call notes say **"KILLIONS REMODELLING"**. The repo is `killion-remodelling`.
The site currently says **"Killion Remodeling"** (US spelling, no S).

Three plausible spellings and only one is his. Ask him on the call, then change
**two lines** in `_generator/content.py` and rebuild:

```python
BIZ = "Killion Remodeling"
BIZ_SHORT = "Killion"
```

The logo is SVG text, so it also needs a one-word edit in
`assets/img/logo.svg` and `assets/img/logo-light.svg` if the spelling changes.

`OWNER_FULL = "Rick Killion"` is an assumption too — his surname was never
actually confirmed on the call.

### The phone number — this is the real blocker

**Rick never gave a phone number.** A lead-generation site for a handyman with
no phone number on it is the one thing that stops the whole thing working, and
the dock on mobile, the util bar, the CTA band on every page and both hero
buttons are all wired to it.

The site currently shows **(309) 555-0100**. That is a deliberately fake number
— 555-01xx is the reserved fictional range, so it cannot accidentally ring a
real stranger if Rick forwards the demo link to someone.

Get his cell on the call, then change two lines in `_generator/content.py`:

```python
PHONE_DISPLAY = "(309) 555-0100"
PHONE_TEL     = "3095550100"
```

and rebuild. It appears in 40 pages and updates everywhere.

---

## 2. What the demo discloses, and where

Nothing on this site pretends to be real. Every stand-in is labelled.

- **Demo banner** on all 40 pages. On phones it collapses to
  `DEMO PREVIEW [What's this?]`; the button re-opens the modal any time.
- **Pop-up modal** on first visit per browser session (1.1s delay, dismissible,
  Escape closes it). It says who built it, that the photos are placeholders,
  and that the forms go to 60MS rather than to Rick.
- **Footer block** on every page repeating all of that.
- **Every form** carries a visible note: *"while this site is a demo, everything
  sent through this form goes to 60 Minute Sites — not to Rick."*
- **thank-you.html** repeats it after a submission, so nobody walks away
  thinking Rick got their message.
- **noindex, nofollow** on all 40 pages, `robots.txt` disallows everything, and
  `netlify.toml` sets `X-Robots-Tag: noindex`. Three layers, because this demo
  must never outrank whatever Rick eventually launches.

---

## 3. Forms — where they go

All forms POST to the standard 60 Minute Sites intake endpoint:

```
https://60minutesites.com/form/general-contact-form-a935
```

They really do submit — this is not a dummy that pops a modal. Per your
instruction, **everything goes to 60MS until payment clears.** Each submission
carries `business`, `source` (which page), `landing_page`, `traffic_source`,
`fill_seconds`, UTM fields and a honeypot, same as the other 60MS sites.

Forms live on: the homepage hero (4 fields, deliberately short), `contact.html`
(full, with service tick-boxes) and all 24 area pages.

**At launch**, point them at Rick's inbox and delete the `form-note` paragraph
in `quote_form()` in `_generator/build.py`.

A nice touch worth showing him: the "Send the form" button on each service page
deep-links as `/contact.html?service=Painting#quote`, which lands on the contact
form with that service already ticked.

---

## 4. There are no photographs, and that is on purpose

Rick sent none. Rather than fill the site with library photos of other people's
houses — which customers spot instantly — **every image slot is a labelled
placeholder naming the shot it wants.**

`gallery.html` is the whole shot list laid out as a page. Show him that page on
the call; it turns "send me some photos" into a concrete list of 16.

The eight that matter most, in order:

1. **Rick actually working** — brush in hand, on a ladder, measuring. A face
   shot does more than the other fifteen combined.
2. Two or three painted rooms, shot from a corner with the blinds open.
3. A before/after pair taken from the *same spot*.
4. A finished deck, shot low along the boards.
5. A new window from inside, a new door from outside.
6. A tile floor or backsplash, taken from low down.
7. A close-up of trim or a built-in.
8. The van with a ladder on it.

Shooting notes for him: morning or late afternoon rather than midday, stand
square on, hold the phone still, and take the *before* photo before starting —
that is the one people always forget and it is worth as much as the after.

Eight photos is enough to launch. Sixteen fills the site.

Replacing a slot is one line: swap the `.ph` div for
`<img src="/assets/img/whatever.jpg" alt="...">`. Nothing else changes.

---

## 5. The video — his question about dos and don'ts

He asked on the call about doing a video explaining what he does. He is right
that it would help: for a one-man trade with no reviews yet, sixty seconds of
the actual person is the single strongest trust signal available.

There are two slots waiting for it, on the homepage and on `about.html`.

**Do:**

- Shoot it on his phone, held **vertical**, propped on something solid. No
  hand-holding — a wobbling frame reads as amateur in a way nothing else does.
- Stand with a window or the sun **in front of** him, not behind.
- Somewhere quiet. Phone microphones pick up wind and traffic badly; a garage
  with the door shut beats a nice-looking driveway.
- Open with his name, the business and the town in the first five seconds:
  *"I'm Rick, I run Killion Remodeling out of Bloomington."*
- Say plainly what he does and what he does not. The "I don't do full kitchens
  and bathrooms" line builds more trust than any claim could.
- Finish by telling people to call, and say the number out loud.
- Keep it **45 to 90 seconds**. Shorter than feels natural.

**Don't:**

- Don't script it word for word and read it. Bullet points on a notepad off
  camera, then talk. Three natural takes beat one perfect read.
- Don't shoot in front of a window, or he becomes a silhouette.
- Don't use music — it fights the voice and dates fast.
- Don't claim licensing, insurance, years in business or number of jobs until
  those numbers are confirmed (see §7).
- Don't mention prices. They change; the video does not.
- Don't worry about the stammer in take one. Do it three times and use the
  third.

---

## 6. Reviews — the honest treatment

Rick has no reviews. He was away four years and is starting the customer list
over. **No fabricated reviews appear anywhere on this site.**

`reviews.html` says so directly, explains why, and argues the case for calling
a tradesman who has three reviews rather than three hundred. It also asks for
one, and lists what makes a review useful.

The page does show three **sample cards** so he can see the layout — they sit
inside a dashed brick frame labelled *"SAMPLE LAYOUT — NOT REAL REVIEWS"*, and
each card's byline repeats it. They cannot be mistaken for real ones even in a
screenshot.

The "Leave a review" button is a dead link until he has a Google Business
Profile. **Setting that up is the highest-value thing he can do this week** —
it is free, it is what makes him show up on Google Maps for "handyman near me",
and it is where the reviews accumulate.

---

## 7. Things to collect from Rick

Each one unlocks something currently missing from the site.

| What | Why it matters |
|---|---|
| **Cell number** | Blocking. Nothing works without it. |
| **Name spelling** | Blocking. Confirm Killion/Killions, Remodeling/Remodelling. |
| **Licence number and insurance** | Deliberately claimed nowhere right now. Every serious competitor prints theirs. Cheapest trust upgrade available. |
| **Google Business Profile** | Free, and the main way a local handyman gets found. Unlocks the reviews page and the map pack. |
| **8–16 photos** | See §4. The gallery page is the ask, already written out. |
| **The intro video** | See §5. |
| **Years in the trade** | Deliberately not claimed, because the call notes do not say. "20 years' experience" is worth a lot and costs nothing — if it is true. |
| **Any workmanship warranty** | Even one year. Cheap, and nobody else in this trade prints one. |
| **A branded email** | `0507cubbies@gmail.com` is his real address and it works, but `rick@killionremodeling.com` reads very differently on an invoice. |
| **Hours** | The site says "call or text" and nothing more, because nothing was given. |
| **Whether he does fences** | The notes mention decks but not fences. They are adjacent work and worth a line if he does. |

---

## 8. Content decisions worth knowing about

1. **Positioned as a handyman and painter**, per your steer. The call notes
   first said kitchens and bathrooms and then corrected to decks, windows and
   handyman work — the site follows the correction and states plainly on
   `services.html` and in the FAQ that he does **not** do full kitchen and
   bathroom remodels.
2. **The gap in his history is addressed head-on**, on the homepage, the about
   page and the reviews page. Trying to hide a four-year absence from a town
   the size of Bloomington–Normal would have read worse than owning it, and
   "he wants your job more than someone with 300 reviews does" is a genuinely
   strong argument for a new business.
3. **No prices anywhere.** He gave none. Instead there is a small table
   explaining *how* each kind of job gets priced — hourly for small repairs,
   flat after a walkthrough for a room, written and itemised for anything
   bigger. Confirm that shape with him; it is an educated guess at how most
   one-man operations in this trade actually work.
4. **No licensing, insurance or experience claims.** All three are easy to add
   once confirmed and legally risky to invent.
5. **24 service-area pages** covering the 50-mile radius, each with the real
   mileage and county. These are what makes him findable for "painter Normal
   IL" once the site is indexed. The radius map is pure CSS — no Google Maps
   key, nothing to bill.
6. **Seven service pages.** Room additions is included because the call notes
   list it, but it is framed carefully: a written quote, a start date, and
   licensed trades brought in for the parts that need them.

---

## 9. How to change anything

```bash
cd killion-remodelling
python3 _generator/build.py
```

Everything a human edits lives in **`_generator/content.py`** — the phone
number, the name, the service copy, the FAQs, the town list, the shot list.
`build.py` only turns it into HTML. The design system is
`assets/css/main.css` and the behaviour is `assets/js/main.js`.

**To go live:**

1. Real phone number and confirmed name in `content.py`.
2. Point the forms at Rick's inbox in `quote_form()` and delete the demo
   `form-note` paragraph.
3. Delete the demo banner (`head()`), the footer demo block (`footer()`), and
   section 7 of `assets/js/main.js` — all three are marked with `DEMO` comments.
4. Remove `noindex, nofollow` from `head()`, open up `robots.txt`, and drop the
   `X-Robots-Tag` header from `netlify.toml`.
5. Drop the real photos into `assets/img/` and swap out the `.ph` divs.
6. Rebuild, then submit the sitemap and wire up the Google Business Profile.
