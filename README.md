# Killion Remodeling — demo site

Rick — handyman, painting and general remodeling. Bloomington, Illinois, working
a 50-mile radius. Built by [60 Minute Sites](https://60minutesites.com) as a
demo, 30 Sep 2026.

**Read [DEMO-NOTES.md](DEMO-NOTES.md) before showing this to anyone** — the
phone number and the business-name spelling are both placeholders.

## Build

```bash
python3 _generator/build.py
```

40 static pages, no build step beyond that, no dependencies. Google Fonts is the
only third-party request.

```
_generator/content.py   every client fact and all page copy — edit here
_generator/build.py     turns content.py into HTML
assets/css/main.css     design system (North Line's, re-skinned navy/amber)
assets/js/main.js       nav, reveal, form plumbing, demo modal (§7, delete at launch)
assets/img/             SVG logo + favicon. No photographs yet, by design.
```

## What's on it

| | |
|---|---|
| Services | 7 — handyman, painting, decks, windows & doors, flooring, trim, additions |
| Service areas | 24 towns inside 50 miles, each with real mileage and county |
| Other pages | home, services hub, gallery, reviews, about, contact, sitemap, thank-you, 404 |
| Forms | homepage hero, contact, all 24 area pages → the 60MS intake endpoint |
| Photographs | none — every slot is a labelled placeholder naming the shot it needs |
| Reviews | none, and none invented. The reviews page explains why. |

## Demo state

- Demo banner, first-visit pop-up and footer disclosure on all 40 pages
- **All forms submit to 60 Minute Sites, not to Rick**, until payment clears
- `noindex` + `robots.txt` + `X-Robots-Tag` so it can never compete in search
- Everything demo-only is marked with a `DEMO` comment for deletion at launch

## Deploy

Netlify, publish directory `.`, no build command. `netlify.toml` sets the
noindex headers and two tidy-up redirects.
