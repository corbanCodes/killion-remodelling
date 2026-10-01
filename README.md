# Killion Remodelling — demo site

Rick — handyman, painting and general remodelling. Bloomington, Illinois, working
a 50-mile radius. Built by [60 Minute Sites](https://60minutesites.com) as a
demo, 30 Sep 2026; rebuilt 1 Oct 2026 with Rick's logo and real photography.

**Read [DEMO-NOTES.md](DEMO-NOTES.md) before showing this to anyone** — the
phone number is still a placeholder.

## Build

```bash
python3 _generator/build.py
```

41 static pages, no build step beyond that, no dependencies. Google Fonts is the
only third-party request.

```
_generator/content.py   every client fact, all page copy, the photo list — edit here
_generator/build.py     turns content.py into HTML
_generator/credits.json photographer data behind credits.html
assets/css/main.css     design system — palette sampled from Rick's logo
assets/js/main.js       nav, reveal, lightbox, form plumbing, demo modal (§8, delete at launch)
assets/img/             logo.png (Rick's), logo-light.png + mark.png (generated), photos/
```

## Brand

Taken straight out of the logo Rick supplied: navy `#012344`, gold `#FBAC18`,
rust `#CD3C09`. `logo-light.png` is a recoloured variant for the dark footer,
since the wordmark is navy; `mark.png` is the square icon alone, used as the
favicon.

## What's on it

| | |
|---|---|
| Services | 7 — handyman, painting, decks, windows & doors, flooring, trim, additions |
| Service areas | 24 towns inside 50 miles, each with real mileage and county |
| Other pages | home, services hub, gallery, reviews, about, contact, credits, sitemap, thank-you, 404 |
| Forms | homepage hero, contact, all 24 area pages → the 60MS intake endpoint |
| Photographs | 22 Unsplash library images, credited on `credits.html`, with a lightbox |
| Reviews | none, and none invented. The reviews page explains why. |

## Demo state

- Demo banner, first-visit pop-up and footer disclosure on all 41 pages
- **All forms submit to 60 Minute Sites, not to Rick**, until payment clears
- Photographs are library images and the site says so, in the banner, the
  pop-up, the footer, the gallery and on `credits.html`
- `noindex` + `robots.txt` + `X-Robots-Tag` so it can never compete in search
- Everything demo-only is marked with a `DEMO` comment for deletion at launch

## Deploy

Netlify, publish directory `.`, no build command. `netlify.toml` sets the
noindex headers, a long cache on `/assets/*` and two tidy-up redirects.
