#!/usr/bin/env python3
"""Killion Remodeling — demo-site generator.

Reads content.py and writes the whole static site into the repo root.
Run:  python3 _generator/build.py

Design system is the North Line Property Services system, re-skinned navy and
amber. The site ships with no client photographs: every image is a labelled
.ph placeholder naming the shot it wants (see content.SHOT_LIST).
"""
import re
import shutil
from pathlib import Path

import content as C

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# ------------------------------------------------------------------- helpers
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def town_slug(town):
    return slugify(town) + "-il"


# ---------------------------------------------------------------------- icons
STAR = ('<svg viewBox="0 0 16 16"><path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 '
        '6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 '
        '4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187z"/></svg>')
CHECK = ('<svg viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 '
         '0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 '
         '1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/></svg>')
ARROW = ('<svg viewBox="0 0 16 16"><path d="M1 8a.5.5 0 0 1 .5-.5h11.793L10.146 4.354a.5.5 0 1 1 '
         '.708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/></svg>')
PLUS = '<svg viewBox="0 0 16 16"><path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/></svg>'

ICONS = dict(
    phone='<svg viewBox="0 0 16 16"><path d="M3.654 1.328a.678.678 0 0 0-1.015-.063L1.605 2.3c-.483.484-.661 1.169-.45 1.77a17.6 17.6 0 0 0 4.168 6.608 17.6 17.6 0 0 0 6.608 4.168c.601.211 1.286.033 1.77-.45l1.034-1.034a.678.678 0 0 0-.063-1.015l-2.307-1.794a.68.68 0 0 0-.58-.122l-2.19.547a1.75 1.75 0 0 1-1.657-.459L5.482 8.062a1.75 1.75 0 0 1-.46-1.657l.548-2.19a.68.68 0 0 0-.122-.58z"/></svg>',
    text='<svg viewBox="0 0 16 16"><path d="M16 8c0 3.866-3.582 7-8 7a9 9 0 0 1-2.347-.306c-.584.296-1.925.864-4.181 1.234-.2.032-.352-.176-.273-.362.354-.836.674-1.95.77-2.966C.744 11.37 0 9.76 0 8c0-3.866 3.582-7 8-7s8 3.134 8 7"/></svg>',
    mail='<svg viewBox="0 0 16 16"><path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414zM0 4.697v7.104l5.803-3.558zM6.761 8.83l-6.57 4.026A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586zm3.436-.586L16 11.801V4.697z"/></svg>',
    pin='<svg viewBox="0 0 16 16"><path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10m0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6"/></svg>',
    cal='<svg viewBox="0 0 16 16"><path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5M1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4z"/></svg>',
    person='<svg viewBox="0 0 16 16"><path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6m2 3a2 2 0 0 1 2 2v1H4v-1a2 2 0 0 1 2-2zM8 9a5 5 0 0 0-5 5v1a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1a5 5 0 0 0-5-5"/></svg>',
    wallet='<svg viewBox="0 0 16 16"><path d="M0 3a2 2 0 0 1 2-2h11.5a.5.5 0 0 1 0 1H15a1 1 0 0 1 1 1v9a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v.5h13V3a1 1 0 0 0-1-1zm10.5 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2"/></svg>',
    camera='<svg viewBox="0 0 16 16"><path d="M15 12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h1.172a3 3 0 0 0 2.12-.879l.83-.828A1 1 0 0 1 6.827 3h2.344a1 1 0 0 1 .707.293l.828.828A3 3 0 0 0 12.828 5H14a1 1 0 0 1 1 1zM2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 0 1 3.172 4z"/><path d="M8 11a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5m0 1a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7"/></svg>',
    video='<svg viewBox="0 0 16 16"><path d="M0 5a2 2 0 0 1 2-2h7.5a2 2 0 0 1 1.983 1.738l3.11-1.382A1 1 0 0 1 16 4.269v7.462a1 1 0 0 1-1.406.913l-3.111-1.382A2 2 0 0 1 9.5 13H2a2 2 0 0 1-2-2z"/></svg>',
    wrench='<svg viewBox="0 0 16 16"><path d="M.102 2.223A3.004 3.004 0 0 0 3.78 5.897l6.341 6.252A3.003 3.003 0 0 0 13 16a3 3 0 1 0-.851-5.878L5.897 3.781A3.004 3.004 0 0 0 2.223.1l2.141 2.142L4 4l-1.757.364zm13.37 9.019.528.026.287.445.445.287.026.529L15 13l-.242.471-.026.529-.445.287-.287.445-.529.026L13 15l-.471-.242-.529-.026-.287-.445-.445-.287-.026-.529L11 13l.242-.471.026-.529.445-.287.287-.445.529-.026L13 11z"/></svg>',
    roller='<svg viewBox="0 0 16 16"><path d="M2 1.5A1.5 1.5 0 0 1 3.5 0h9A1.5 1.5 0 0 1 14 1.5v3A1.5 1.5 0 0 1 12.5 6H10v1.5A1.5 1.5 0 0 1 8.5 9H8v1.5a1.5 1.5 0 0 1-1 1.415V15a1 1 0 1 1-2 0v-3.085A1.5 1.5 0 0 1 4 10.5V9h-.5A1.5 1.5 0 0 1 2 7.5zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5z"/></svg>',
    deck='<svg viewBox="0 0 16 16"><path d="M1 3h14v1.5H1zM1 6h14v1.5H1zM1 9h14v1.5H1zM2.5 11.5H4V16H2.5zM12 11.5h1.5V16H12z"/></svg>',
    window='<svg viewBox="0 0 16 16"><path d="M2 1a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zm.5 1.5h5v5h-5zm6.5 0h5v5H9zm-6.5 6.5h5v5h-5zm6.5 0h5v5H9z"/></svg>',
    tile='<svg viewBox="0 0 16 16"><path d="M1 1h6.3v6.3H1zM8.7 1H15v6.3H8.7zM1 8.7h6.3V15H1zM8.7 8.7H15V15H8.7z"/></svg>',
    saw='<svg viewBox="0 0 16 16"><path d="M0 4.5 1.8 6l1.4-1.5L4.6 6 6 4.5 7.4 6l1.4-1.5L10.2 6l1.4-1.5L13 6l1.5-1.5V8H0zM0 9h15v2a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1z"/></svg>',
    house='<svg viewBox="0 0 16 16"><path d="M8.707 1.5a1 1 0 0 0-1.414 0L.646 8.146a.5.5 0 0 0 .708.708L8 2.207l6.646 6.647a.5.5 0 0 0 .708-.708L13 5.793V2.5a.5.5 0 0 0-.5-.5h-2a.5.5 0 0 0-.5.5v1.293zM2.5 14a1 1 0 0 0 1 1h3v-4h3v4h3a1 1 0 0 0 1-1V9.5L8 3.5 2.5 9z"/></svg>',
    clock='<svg viewBox="0 0 16 16"><path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71z"/><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0"/></svg>',
    hand='<svg viewBox="0 0 16 16"><path d="M8 1a.5.5 0 0 1 .5.5v5a.5.5 0 0 0 1 0V2a.5.5 0 0 1 1 0v4.5a.5.5 0 0 0 1 0V3.5a.5.5 0 0 1 1 0V9a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V6.5a.5.5 0 0 1 1 0V9a.5.5 0 0 0 1 0V2.5a.5.5 0 0 1 1 0v4a.5.5 0 0 0 1 0v-5A.5.5 0 0 1 8 1"/></svg>',
)


def stars():
    return '<span class="stars">' + STAR * 5 + "</span>"


# ----------------------------------------------------------------- components
def ph(key, extra_cls="", ratio=None):
    """A labelled photo placeholder. Delete these when real photos land."""
    _k, ratio_default, label, caption = C.SHOT_BY_KEY[key]
    r = ratio or ratio_default
    cls = " ".join(x for x in ["ph", r, extra_cls] if x)
    return (f'<div class="{cls}" role="img" aria-label="Placeholder for a photo: {esc(caption)}">'
            f'{ICONS["camera"]}<b>Photo &mdash; {esc(label)}</b>'
            f'<span>{esc(caption)}</span></div>')


def check_list(items, cls="check-list"):
    lis = "\n".join(f"  <li>{CHECK}<span>{esc(i)}</span></li>" for i in items)
    return f'<ul class="{cls}">\n{lis}\n</ul>'


def faq_block(faqs):
    out = []
    for q, a in faqs:
        out.append(f'''<details class="faq"><summary>{esc(q)}{PLUS}</summary>
  <div class="faq-body"><p>{esc(a)}</p></div></details>''')
    return "\n".join(out)


def service_card(s):
    return f'''<a class="card reveal" href="/services/{s["slug"]}.html">
  <div class="card-cap">
    <span class="cap-ico">{ICONS[s["ico"]]}</span>
    <span><small>{esc(s["kicker"])}</small><h3>{esc(s["short"])}</h3></span>
  </div>
  <div class="card-body">
    <p>{esc(s["blurb"])}</p>
    <span class="card-link">What this covers {ARROW}</span>
  </div></a>'''


def services_grid(current=""):
    return "\n".join(service_card(s) for s in C.SERVICES if s["slug"] != current)


def steps_block(steps=None):
    steps = steps or C.STEPS
    return "\n".join(
        f'<div class="step reveal"><h3>{esc(h)}</h3><p>{esc(p)}</p></div>' for h, p in steps)


def radius_map():
    pins = "\n".join(
        f'    <span class="pin" style="left:{x}%;top:{y}%">{esc(t)}</span>'
        for t, x, y in C.MAP_PINS)
    return f'''<div class="radius-map reveal" role="img" aria-label="Service area map: {C.RADIUS_MI} miles around {C.HOME_BASE}">
  <div class="rings">
    <span class="ring r1"></span><span class="ring r2"></span><span class="ring r3"></span>
  </div>
{pins}
  <span class="ring-lbl" style="top:7%">{C.RADIUS_MI}-MILE RADIUS</span>
  <span class="hub"><span class="hub-dot"></span>
    <b>{esc(C.CITY).upper()}</b><span>Home base</span></span>
</div>'''


def pricing_table():
    rows = "\n".join(
        f"      <tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in C.PRICING_ROWS)
    return f'''<div class="rate-wrap reveal"><table class="rate-table">
  <thead><tr><th>The kind of job</th><th>How it is priced</th></tr></thead>
  <tbody>
{rows}
  </tbody></table></div>'''


def video_slot():
    return f'''<div class="video-slot reveal">
  <div class="ph r916 on-dark" role="img" aria-label="Placeholder for Rick's introduction video">
    {ICONS["video"]}<b>Video &mdash; Rick introduces himself</b>
    <span>A phone-shot clip of {C.OWNER} saying who he is, what he does and where he works.
      Shooting notes are in DEMO-NOTES.md.</span>
  </div>
</div>'''


# ---------------------------------------------------------------------- forms
def quote_form(form_id="quote", compact=False, minimal=False, source="", preselect=""):
    """The 60 Minute Sites intake form. Posts to 60MS, not to Rick — see the note.

    minimal — four fields and a one-line brief (the homepage hero card).
    compact — full field set, no long message box (area pages).
    """
    if minimal:
        boxes_block = f'''
      <div class="field full"><label for="{form_id}-msg">What do you need doing?</label>
        <input id="{form_id}-msg" name="message" type="text" placeholder="Painting, a leaky sink, a deck&hellip;"></div>'''
    else:
        boxes = "\n".join(
            f'        <label class="svc-check"><input type="checkbox" name="services" '
            f'value="{esc(s["short"])}"{" checked" if preselect == s["slug"] else ""}> '
            f'{esc(s["short"])}</label>'
            for s in C.SERVICES)
        boxes_block = f'''
      <div class="field full"><label>What is it you need? <span style="font-weight:500;opacity:.6">(tick as many as apply)</span></label>
        <div class="svc-checks">
{boxes}
        </div></div>'''

    msg = "" if (compact or minimal) else f'''
      <div class="field full"><label for="{form_id}-msg">Anything else worth knowing?</label>
        <textarea id="{form_id}-msg" name="message" placeholder="A list is fine. Rooms, sizes, how soon you need it &mdash; whatever you know."></textarea></div>'''
    return f'''<form id="{form_id}" class="form-grid" action="{C.FORM_ACTION}" method="POST" data-hq-form>
      <div class="field"><label for="{form_id}-name">Your name <span class="req">*</span></label>
        <input id="{form_id}-name" name="name" type="text" autocomplete="name" placeholder="Full name" required></div>
      <div class="field"><label for="{form_id}-phone">Phone <span class="req">*</span></label>
        <input id="{form_id}-phone" name="phone" type="tel" autocomplete="tel" placeholder="(309) 555-0123" required></div>
      <div class="field"><label for="{form_id}-email">Email <span class="req">*</span></label>
        <input id="{form_id}-email" name="email" type="email" autocomplete="email" placeholder="you@email.com" required></div>
      <div class="field"><label for="{form_id}-town">Town</label>
        <input id="{form_id}-town" name="full_address" type="text" autocomplete="address-level2" placeholder="{esc(C.CITY)}, {C.STATE_ABBR}"></div>{boxes_block}{msg}
      <input type="hidden" name="business" value="{esc(C.BIZ)}">
      <input type="hidden" name="business_type" value="Handyman, painting &amp; general remodeling">
      <input type="hidden" name="source" value="{esc(source or C.BIZ + ' demo site')}">
      <input type="hidden" name="_next" value="">
      <input type="hidden" name="landing_page" value="">
      <input type="hidden" name="fill_seconds" value="">
      <input type="hidden" name="traffic_source" value="">
      <input type="hidden" name="utm_campaign" value="">
      <input type="hidden" name="utm_content" value="">
      <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="field full">
        <button class="btn btn-amber btn-block" type="submit">Send it to {esc(C.OWNER)} {ARROW}</button>
        <p class="form-note"><b>Demo note:</b> while this site is a demo, everything sent through
          this form goes to <a href="{C.SIXTYMS_URL}" target="_blank" rel="noopener">60&nbsp;Minute&nbsp;Sites</a>
          &mdash; not to {esc(C.OWNER)}. Forms get pointed at his own inbox once the site is paid
          for and live.</p>
      </div>
    </form>'''


# --------------------------------------------------------------- page chrome
def head(title, desc, canonical=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta name="theme-color" content="#13304F">
<link rel="icon" type="image/svg+xml" href="/assets/img/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,400..900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/main.css">
</head>
<body>

<!-- DEMO — delete this div, the .footer-demo block, section 7 of main.js and
     the .demo-bar/.demo-modal CSS when the site goes live. -->
<div class="demo-bar"><span class="demo-dot"></span><strong>DEMO PREVIEW</strong><span
  class="demo-tail"> &mdash; a design concept for {esc(C.BIZ)} by
  <a href="{C.SIXTYMS_URL}" target="_blank" rel="noopener">60&nbsp;Minute&nbsp;Sites</a>
  &middot; photos are placeholders and all forms go to 60MS, not to {esc(C.OWNER)}</span>
  <button type="button" data-demo-open>What&rsquo;s this?</button></div>
'''


def nav(active=""):
    drop = "\n".join(
        f'        <a href="/services/{s["slug"]}.html">{esc(s["name"])}</a>' for s in C.SERVICES)

    def cls(key):
        return ' class="active"' if active == key else ""

    return f'''
<div class="util-bar"><div class="wrap">
  <a href="tel:{C.PHONE_TEL}">{ICONS["phone"]} {C.PHONE_DISPLAY}</a>
  <span class="util-hide">{ICONS["pin"]} {esc(C.RADIUS_MI and str(C.RADIUS_MI))} miles around {esc(C.HOME_BASE)}</span>
  <span class="util-spacer"></span>
  <a class="util-hide" href="mailto:{C.EMAIL}">{ICONS["mail"]} {C.EMAIL}</a>
</div></div>

<header class="site-header"><div class="wrap nav-row">
  <a class="brand" href="/index.html">
    <img src="/assets/img/logo.svg" alt="{esc(C.BIZ)}" width="268" height="96">
  </a>
  <button class="nav-burger" aria-label="Menu" aria-expanded="false"><svg viewBox="0 0 16 16"><path d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/></svg></button>
  <nav class="main-nav">
    <div class="nav-drop"><button aria-haspopup="true" aria-expanded="false">What Rick Does
      <svg viewBox="0 0 16 16"><path d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708"/></svg></button>
      <div class="drop-menu">
        <a href="/services.html"><b>All services</b></a>
{drop}
      </div></div>
    <a href="/areas/{town_slug(C.CITY)}.html"{cls("areas")}>Service Area</a>
    <a href="/gallery.html"{cls("gallery")}>Work</a>
    <a href="/reviews.html"{cls("reviews")}>Reviews</a>
    <a href="/about.html"{cls("about")}>About Rick</a>
    <a href="/contact.html"{cls("contact")}>Contact</a>
    <a href="/contact.html#quote" class="btn btn-amber btn-sm nav-cta">Get a Free Estimate</a>
  </nav>
</div></header>
'''


def page_hero(h1, p, crumbs=None):
    cr = ""
    if crumbs:
        parts = [f'<a href="{href}">{esc(label)}</a>' if href else esc(label)
                 for label, href in crumbs]
        cr = f'<div class="crumbs">{" / ".join(parts)}</div>'
    return f'''
<section class="page-hero"><div class="wrap">
  {cr}
  <h1>{h1}</h1>
  <p>{p}</p>
</div></section>
'''


def cta_band(h=None, p=None):
    h = h or f"Get {C.OWNER} to Come and Look"
    p = p or ("Free estimates on anything beyond a small repair, a straight price, and the "
              "person who quotes it is the person who does the work.")
    return f'''
<section class="section on-ink cta-band"><div class="wrap reveal">
  <span class="eyebrow">Free estimates</span>
  <h2>{esc(h)}</h2>
  <p>{esc(p)}</p>
  <div class="hero-ctas">
    <a class="btn btn-amber" href="tel:{C.PHONE_TEL}">{ICONS["phone"]} Call {C.PHONE_DISPLAY}</a>
    <a class="btn btn-ghost" href="/contact.html#quote">Send the form instead</a>
  </div>
</div></section>
'''


def footer():
    svc = "\n".join(
        f'      <li><a href="/services/{s["slug"]}.html">{esc(s["short"])}</a></li>'
        for s in C.SERVICES)
    towns = " &middot; ".join(
        f'<a href="/areas/{town_slug(t)}.html">{esc(t)}</a>' for t, _m, _c in C.TOWNS[:12])
    return f'''
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="/assets/img/logo-light.svg" alt="{esc(C.BIZ)}" width="268" height="96">
      <p>Handyman work, painting and general remodeling, owner-operated out of
         {esc(C.HOME_BASE)} and {C.RADIUS_MI} miles around it.</p>
    </div>
    <div><h4>What Rick Does</h4><ul class="footer-links">
{svc}
      <li><a href="/services.html">All services</a></li>
    </ul></div>
    <div><h4>The Business</h4><ul class="footer-links">
      <li><a href="/about.html">About {esc(C.OWNER)}</a></li>
      <li><a href="/gallery.html">The work</a></li>
      <li><a href="/reviews.html">Reviews</a></li>
      <li><a href="/areas/{town_slug(C.CITY)}.html">Service area</a></li>
      <li><a href="/contact.html">Contact</a></li>
      <li><a href="/sitemap.html">Sitemap</a></li>
    </ul></div>
    <div><h4>Get Hold of Him</h4><ul class="footer-links">
      <li><a href="tel:{C.PHONE_TEL}">{C.PHONE_DISPLAY}</a></li>
      <li><a href="sms:+1{C.PHONE_TEL}">Text a photo</a></li>
      <li><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></li>
      <li>{esc(C.HOME_BASE)}</li>
      <li>Free estimates</li>
    </ul></div>
  </div>
  <div class="wrap footer-areas"><strong>Service area:</strong> {towns} &middot;
    <a href="/sitemap.html">all {len(C.TOWNS)} towns &rarr;</a></div>
  <!-- DEMO — delete this block when the site goes live. -->
  <div class="wrap footer-demo"><b>This is a demo site.</b> It was built by
    <a href="{C.SIXTYMS_URL}" target="_blank" rel="noopener">60 Minute Sites</a> to show
    {esc(C.OWNER)} what his own site could look like. Every photo slot is a labelled
    placeholder, there are no customer reviews on it yet, and
    <b>every form submits to 60 Minute Sites rather than to {esc(C.OWNER)}</b> until the site is
    paid for and live. <a href="{C.PRICING_URL}" target="_blank" rel="noopener">See pricing</a>.</div>
  <div class="wrap footer-bottom">
    <span>&copy; <span data-year>2026</span> {esc(C.BIZ)}</span>
    <span class="spacer"></span>
    <span>Demo site by <a href="{C.SIXTYMS_URL}" target="_blank" rel="noopener">60 Minute Sites</a></span>
  </div>
</footer>

<nav class="dock" aria-label="Quick actions">
  <a href="tel:{C.PHONE_TEL}">{ICONS["phone"]} Call</a>
  <a href="sms:+1{C.PHONE_TEL}">{ICONS["text"]} Text</a>
  <a href="mailto:{C.EMAIL}">{ICONS["mail"]} Email</a>
  <a class="dock-primary" href="/contact.html#quote">{ICONS["cal"]} Estimate</a>
</nav>

<script src="/assets/js/main.js" defer></script>
</body>
</html>'''


def write(rel, html):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    return p


# ------------------------------------------------------------------ home page
def build_home():
    trust = [
        ("person", f"{C.OWNER} does the work", "No crew you have not met"),
        ("wallet", "Free estimates", "No charge to come and look"),
        ("pin", f"{C.RADIUS_MI} miles out", f"{C.CITY} to Peoria, Champaign &amp; Decatur"),
        ("text", "Call or text", "He answers his own phone"),
    ]
    trust_html = "\n".join(
        f'  <div class="trust-item">{ICONS[i]}<span><b>{t}</b><small>{s}</small></span></div>'
        for i, t, s in trust)

    why_html = "\n".join(
        f'''  <div class="card reveal"><div class="card-body">
    <h3>{esc(h)}</h3><p>{esc(p)}</p></div></div>''' for h, p in C.WHY)

    chips = " ".join(
        f'<a class="chip" href="/areas/{town_slug(t)}.html">{esc(t)}</a>'
        for t, _m, _c in C.TOWNS[:14])

    html = head(
        f"{C.BIZ} — Handyman, Painting & Home Repairs in {C.CITY}, {C.STATE_ABBR}",
        f"Owner-operated handyman and painting work in {C.CITY}-Normal and {C.RADIUS_MI} miles "
        f"around it. Repairs, interior and exterior painting, decks, windows, flooring and trim. "
        f"Free estimates — call or text {C.PHONE_DISPLAY}.")
    html += nav("home")

    html += f'''
<section class="hero"><div class="wrap hero-split">
  <div class="hero-inner">
    <span class="eyebrow">{esc(C.CITY)} &amp; Normal, {C.STATE_ABBR} &mdash; handyman, painting &amp; repairs</span>
    <h1>One Person for <em>the Whole List</em></h1>
    <p class="hero-sub">{esc(C.OWNER)} is a handyman and painter working out of {esc(C.HOME_BASE)}.
      The leaky sink, the room that needs painting, the deck boards gone soft, the door that will
      not shut &mdash; call him once and it all gets sorted by the same person.</p>
    <div class="hero-ctas">
      <a class="btn btn-amber" href="tel:{C.PHONE_TEL}">{ICONS["phone"]} Call {C.PHONE_DISPLAY}</a>
      <a class="btn btn-ghost" href="/contact.html#quote">Get a free estimate</a>
    </div>
    <div class="hero-chips">
      <span>{CHECK} {esc(C.OWNER)} does the work himself</span>
      <span>{CHECK} Free estimates</span>
      <span>{CHECK} {C.RADIUS_MI}-mile radius</span>
      <span>{CHECK} Call, text or email</span>
    </div>
  </div>
  <div class="hero-card">
    <h3>Tell him what you need</h3>
    <p>A list is fine. So is one leaky tap.</p>
    {quote_form("quote-hero", minimal=True, source=f"{C.BIZ} demo — homepage hero")}
  </div>
</div></section>

<section class="trust-bar"><div class="wrap">
{trust_html}
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">What Rick does</span>
    <h2>Handyman Work, Painting, and the Trades Around Them</h2>
    <p>Mostly small jobs and paint. Decks, windows, flooring, trim and the occasional addition
       when somebody needs more house.</p></div>
  <div class="grid grid-3">
{services_grid()}
  </div>
  <p style="margin-top:28px;text-align:center" class="reveal">
    <a class="btn btn-ghost-dark" href="/services.html">See everything, with what each one covers {ARROW}</a></p>
</div></section>

<section class="section on-navy"><div class="wrap split">
  <div class="reveal">
    <span class="eyebrow">Straight talk</span>
    <h2>New to You, Not New to the Work</h2>
    <p>{esc(C.OWNER)} was busy in {esc(C.CITY)} a few years back. He was away for a stretch, and
      he is back now &mdash; which is the honest reason you have not seen his truck on your street
      and will not find a hundred reviews online yet.</p>
    <p>He is rebuilding the customer list from scratch. That is worth knowing both ways: it is why
      there is no long review history to show you, and it is exactly why the first people who call
      get a tradesman who very much wants the job done right.</p>
    <div class="hero-ctas" style="margin-bottom:0">
      <a class="btn btn-amber" href="/about.html">More about {esc(C.OWNER)} {ARROW}</a>
    </div>
  </div>
  {ph("rick-at-work", "on-dark reveal")}
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">Why call him</span>
    <h2>What You Actually Get</h2></div>
  <div class="grid grid-2">
{why_html}
  </div>
</div></section>

<section class="section on-mist"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">How it works</span>
    <h2>Four Steps, No Surprises</h2></div>
  <div class="grid grid-4 steps">
{steps_block()}
  </div>
</div></section>

<section class="section"><div class="wrap split lean">
  <div class="reveal">
    <span class="eyebrow">What it costs</span>
    <h2>How the Pricing Works</h2>
    <p>Rick has not put price lists on this site, because a number without seeing the job is a
      number that changes later. What he will do is tell you how your particular job gets
      priced before he drives anywhere.</p>
    <p style="font-size:.95rem;opacity:.75">Materials are listed separately on anything bigger
      than a repair, so you can see what is labour and what is lumber.</p>
  </div>
  {pricing_table()}
</div></section>

<section class="section on-ink"><div class="wrap split">
  <div class="reveal">
    <span class="eyebrow">Hear it from him</span>
    <h2>A Minute With {esc(C.OWNER)}</h2>
    <p>Hiring someone to work in your house is a trust decision, and a short clip of the person
      who will be standing in your kitchen does more for that than any amount of copy.</p>
    <p style="font-size:.95rem;opacity:.8">This slot is waiting on {esc(C.OWNER)}&rsquo;s video.
      A phone held steady, good daylight, sixty seconds &mdash; who he is, what he does, where he
      works, and what someone should call him about.</p>
  </div>
  {video_slot()}
</div></section>

<section class="section on-mist"><div class="wrap split">
  <div class="reveal">
    <span class="eyebrow">Service area</span>
    <h2>{C.RADIUS_MI} Miles Around {esc(C.CITY)}</h2>
    <p>{esc(C.CITY)} and Normal are home. From there it is about {C.RADIUS_MI} miles in every
      direction &mdash; out to Peoria, Champaign, Decatur, Pontiac and Lincoln, and all the
      smaller towns in between.</p>
    <div class="chip-row" style="margin-bottom:20px">{chips}</div>
    <p style="font-size:.95rem;opacity:.75">Just outside the circle? Call and ask anyway.</p>
  </div>
  {radius_map()}
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">Common questions</span>
    <h2>The Things People Ask First</h2></div>
  <div class="prose prose-wide reveal" style="margin:0 auto">
{faq_block(C.GENERAL_FAQS)}
  </div>
</div></section>
'''
    html += cta_band()
    html += footer()
    write("index.html", html)


# -------------------------------------------------------------- services hub
def build_services_hub():
    html = head(
        f"What Rick Does — Handyman, Painting & Remodeling | {C.BIZ}",
        f"Everything {C.BIZ} covers: handyman repairs, interior and exterior painting, decks and "
        f"porches, windows and doors, tile and carpet, trim carpentry and room additions.")
    html += nav("services")
    html += page_hero(
        "What Rick Does",
        "Handyman work and painting are most of it. Here is the full list, with what each one "
        "actually covers &mdash; and what he does not do.",
        crumbs=[("Home", "/index.html"), ("What Rick Does", None)])

    html += f'''
<section class="section"><div class="wrap">
  <div class="grid grid-3">
{services_grid()}
  </div>
</div></section>

<section class="section on-mist"><div class="wrap split lean">
  <div class="reveal">
    <span class="eyebrow">Worth saying out loud</span>
    <h2>What He Does Not Do</h2>
    <p>Full kitchen and bathroom remodels. Rick will do the tile, the flooring, the trim, the
      painting and the doors in a kitchen or a bathroom &mdash; but the whole gut-and-rebuild is
      its own specialism and belongs with somebody who does nothing else.</p>
    <p>Same with anything needing a licensed trade: opening a panel, moving gas, re-piping a
      house, structural engineering. He will tell you that on the phone rather than take the job
      and work it out as he goes.</p>
    <p style="font-size:.95rem;opacity:.75">Knowing where the line is tends to be a good sign in
      a tradesman, not a bad one.</p>
  </div>
  <div class="reveal">
    <h3>Still worth a call for</h3>
    {check_list([
        "A list of small jobs nobody else will come out for",
        "Painting a room, a whole interior or the outside of the house",
        "A deck that needs boards, railings or stain",
        "Draughty windows and doors that will not shut properly",
        "Tile, carpet or vinyl plank over a subfloor worth checking first",
        "Trim, crown, baseboard and built-ins",
        "An addition, a finished basement or a converted garage",
    ])}
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">How it works</span>
    <h2>Four Steps, No Surprises</h2></div>
  <div class="grid grid-4 steps">
{steps_block()}
  </div>
</div></section>
'''
    html += cta_band()
    html += footer()
    write("services.html", html)


# ------------------------------------------------------------- service pages
SERVICE_SHOTS = {
    "handyman": ["handyman-fix", "tools"],
    "painting": ["painting-after", "painting-before-after", "exterior-paint"],
    "decks-porches": ["deck-finished", "deck-repair"],
    "windows-doors": ["window-install", "door-install"],
    "flooring": ["tile-floor", "carpet-room"],
    "trim-carpentry": ["trim-detail", "builtin"],
    "room-additions": ["addition", "van"],
}


def build_service(s):
    shots = SERVICE_SHOTS.get(s["slug"], ["rick-at-work"])
    body = "\n".join(
        f'    <h3>{esc(h)}</h3>\n    <p>{esc(p)}</p>' for h, p in s["body"])

    other = [x for x in C.SERVICES if x["slug"] != s["slug"]][:3]
    other_html = "\n".join(service_card(x) for x in other)

    pills = "\n".join(
        f'  <a href="/services/{x["slug"]}.html"'
        f'{" class=\"active\"" if x["slug"] == s["slug"] else ""}>{esc(x["short"])}</a>'
        for x in C.SERVICES)

    extra_shots = ""
    if len(shots) > 1:
        cards = "\n".join(f"    {ph(k)}" for k in shots[1:])
        extra_shots = f'''
<section class="section tight on-white"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">The work</span>
    <h2>Photos Of This Going In</h2>
    <p>These slots are waiting on {esc(C.OWNER)}&rsquo;s own photos &mdash; each one names the
       shot it needs.</p></div>
  <div class="grid grid-2">
{cards}
  </div>
</div></section>
'''

    html = head(
        f"{s['name']} in {C.CITY}, {C.STATE_ABBR} | {C.BIZ}",
        f"{s['blurb']} Owner-operated, free estimates, {C.RADIUS_MI} miles around {C.HOME_BASE}.")
    html += nav("services")
    html += page_hero(
        esc(s["hero_h"]), esc(s["hero_p"]),
        crumbs=[("Home", "/index.html"), ("What Rick Does", "/services.html"),
                (s["short"], None)])

    html += f'''
<section class="section tight"><div class="wrap">
  <div class="pill-nav reveal">
{pills}
  </div>
  <div class="split lean">
    <div class="prose reveal">
      <p class="lead">{esc(s["lead"])}</p>
{body}
    </div>
    <div class="reveal">
      {ph(shots[0])}
      <div style="margin-top:22px">
        <h3 style="font-size:1.1rem">Get a price on this</h3>
        <div class="hero-ctas" style="margin-bottom:0">
          <a class="btn btn-amber btn-sm" href="tel:{C.PHONE_TEL}">{ICONS["phone"]} {C.PHONE_DISPLAY}</a>
          <a class="btn btn-ghost-dark btn-sm" href="/contact.html?service={esc(s["short"]).replace(" ", "+").replace("&amp;", "%26")}#quote">Send the form</a>
        </div>
      </div>
    </div>
  </div>
</div></section>

<section class="section on-mist"><div class="wrap split lean">
  <div class="reveal">
    <span class="eyebrow">{esc(s["kicker"])}</span>
    <h2>What This Covers</h2>
    <p>Not an exhaustive list &mdash; if what you need is close to something on it, it is worth
      the call.</p>
  </div>
  <div class="reveal">
{check_list(s["incl"], "check-list")}
  </div>
</div></section>
{extra_shots}
<section class="section"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">Questions</span>
    <h2>{esc(s["short"])} &mdash; The Usual Questions</h2></div>
  <div class="prose prose-wide reveal" style="margin:0 auto">
{faq_block(s["faqs"])}
  </div>
</div></section>

<section class="section on-white"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">While he is there</span>
    <h2>Other Things Worth Adding to the List</h2>
    <p>One trip is cheaper than three. People routinely add a couple of these on while he is
       already on site.</p></div>
  <div class="grid grid-3">
{other_html}
  </div>
</div></section>
'''
    html += cta_band(
        h=f"Need {s['short']} Doing?",
        p=f"Call or text {C.PHONE_DISPLAY}, or send the form and {C.OWNER} will come and look. "
          "Free estimates on anything beyond a small repair.")
    html += footer()
    write(f"services/{s['slug']}.html", html)


# ----------------------------------------------------------------- area pages
def build_area(town, miles, county):
    slug = town_slug(town)
    is_home = miles == 0
    others = [t for t, _m, _c in C.TOWNS if t != town][:13]
    chips = " ".join(
        f'<a class="chip" href="/areas/{town_slug(t)}.html">{esc(t)}</a>' for t in others)

    if is_home:
        dist_line = (f"{town} is home. {C.OWNER} is based here, which means short notice is "
                     "genuinely possible and a quick look at something small does not cost "
                     "anybody half a day.")
    else:
        dist_line = (f"{town} is about {miles} miles from {C.OWNER}&rsquo;s base in {C.CITY}, "
                     f"well inside the {C.RADIUS_MI} miles he covers. No travel surcharge, and "
                     "no pretending a two-hour round trip is a quick call-out.")

    svc_links = "\n".join(
        f'      <li><a href="/services/{s["slug"]}.html">{esc(s["name"])}</a> &mdash; '
        f'{esc(s["blurb"].split(" — ")[0].split(",")[0].strip().rstrip("."))}</li>'
        for s in C.SERVICES)

    html = head(
        f"Handyman & Painter in {town}, {C.STATE_ABBR} | {C.BIZ}",
        f"Handyman work, painting and home repairs in {town}, {C.STATE_ABBR}. Owner-operated, "
        f"free estimates. {dist_line.replace('&rsquo;', chr(39))[:90]}")
    html += nav("areas")
    html += page_hero(
        f"Handyman &amp; Painting in {esc(town)}, {C.STATE_ABBR}",
        f"{esc(county)} &mdash; "
        + (f"{esc(C.OWNER)}&rsquo;s home town." if is_home
           else f"about {miles} miles from {esc(C.OWNER)}&rsquo;s base in {esc(C.CITY)}."),
        crumbs=[("Home", "/index.html"), ("Service Area", "/sitemap.html"), (town, None)])

    html += f'''
<section class="section tight"><div class="wrap split lean">
  <div class="prose reveal">
    <p class="lead">{esc(C.OWNER)} covers {esc(town)} for handyman work, painting and the
      general repair and remodeling jobs in between.</p>
    <p>{dist_line}</p>
    <p>The call that comes in most often from towns like {esc(town)} is not one big project. It
      is a list &mdash; a tap that drips, a door that sticks, a bedroom that has needed painting
      since before the kids left, and a deck board somebody keeps meaning to deal with. Getting
      all of it done in one or two visits by the same person is the whole point.</p>
    <h3>What he gets called out for in {esc(town)}</h3>
    <ul class="plain-list">
{svc_links}
    </ul>
  </div>
  <div class="reveal">
    <div class="form-panel">
      <h3 style="margin-bottom:4px">Get an estimate in {esc(town)}</h3>
      <p style="font-size:.93rem;opacity:.7;margin-bottom:18px">Free, and no pressure at the
        end of it.</p>
      {quote_form(f"quote-{slug}", compact=True, source=f"{C.BIZ} demo — {town} area page")}
    </div>
  </div>
</div></section>

<section class="section on-mist"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">Nearby</span>
    <h2>Other Towns He Covers</h2>
    <p>{C.RADIUS_MI} miles around {esc(C.HOME_BASE)}, which is most of central Illinois.</p></div>
  <div class="chip-row reveal">{chips}
    <a class="chip more" href="/sitemap.html">All {len(C.TOWNS)} towns {ARROW}</a></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">How it works</span>
    <h2>From Your Call to the Job Done</h2></div>
  <div class="grid grid-4 steps">
{steps_block()}
  </div>
</div></section>
'''
    html += cta_band(
        h=f"Need a Hand in {town}?",
        p=f"Call or text {C.PHONE_DISPLAY}. {C.OWNER} answers his own phone, and a photo "
          "texted over usually gets you a price without anyone driving anywhere.")
    html += footer()
    write(f"areas/{slug}.html", html)


# --------------------------------------------------------------------- about
def build_about():
    html = head(
        f"About {C.OWNER} — {C.BIZ}, {C.CITY} {C.STATE_ABBR}",
        f"{C.OWNER} runs {C.BIZ} out of {C.HOME_BASE}. Handyman work, painting and general "
        f"remodeling, owner-operated, back working in {C.CITY} and building the list back up.")
    html += nav("about")
    html += page_hero(
        f"About {esc(C.OWNER)}",
        "Owner-operated means the person who quotes your job is the person who turns up to do "
        "it. That is most of what there is to say.",
        crumbs=[("Home", "/index.html"), ("About Rick", None)])

    html += f'''
<section class="section tight"><div class="wrap split lean">
  <div class="prose reveal">
    <p class="lead">{esc(C.BIZ)} is {esc(C.OWNER)}. One van, one phone number, and the same
      person from the first call to the last bit of clean-up.</p>
    <p>He does handyman work and painting, mostly, plus the trades that sit either side of them
      &mdash; decks and porches, windows and doors, tile and carpet, trim and finish carpentry,
      and room additions when a house needs to get bigger.</p>
    <h3>Back in {esc(C.CITY)}</h3>
    <p>Here is the part most businesses would rather leave off a website. {esc(C.OWNER)} was
      busy in this area a few years ago. Then he was away for a stretch, and he is back now and
      starting the customer list again from close to nothing.</p>
    <p>So no, you probably have not heard of him, and there is no decade of reviews to scroll
      through yet. Both of those are true and there is no point pretending otherwise. What is
      also true is that somebody rebuilding a reputation in a town the size of
      {esc(C.CITY)}&ndash;Normal has every reason in the world to do the job properly &mdash;
      word of mouth is the only advertising that has ever worked in this trade, and he knows it.</p>
    <h3>How he works</h3>
    <p>Free estimates on anything beyond a quick repair. A straight number rather than a range.
      Floors covered and the mess cleaned up, because somebody has to live there afterwards. And
      an honest answer when the cheaper fix is the right one, or when a job genuinely needs a
      licensed plumber or electrician instead.</p>
    <p>He would rather turn down a job he should not take than learn on your house.</p>
  </div>
  <div class="reveal">
    {ph("rick-at-work")}
    <div class="channel-card" style="margin-top:22px">
      <h3 style="margin-bottom:2px">Get hold of {esc(C.OWNER)}</h3>
      <p>He answers his own phone.</p>
      <a class="channel" href="tel:{C.PHONE_TEL}">{ICONS["phone"]}
        <span><b>{C.PHONE_DISPLAY}</b><small>Call &mdash; fastest way</small></span></a>
      <a class="channel" href="sms:+1{C.PHONE_TEL}">{ICONS["text"]}
        <span><b>Text a photo</b><small>Usually gets you a price same day</small></span></a>
      <a class="channel" href="mailto:{C.EMAIL}">{ICONS["mail"]}
        <span><b>{C.EMAIL}</b><small>Email</small></span></a>
    </div>
  </div>
</div></section>

<section class="section on-navy"><div class="wrap split">
  <div class="reveal">
    <span class="eyebrow">In his own words</span>
    <h2>A Minute With {esc(C.OWNER)}</h2>
    <p>Letting somebody into your house is a trust decision. Sixty seconds of the actual person
      talking does more for that than anything written about him in the third person.</p>
    <p style="font-size:.95rem;opacity:.82">This slot is waiting on his video. Notes on how to
      shoot it &mdash; and the handful of things not to do &mdash; are in DEMO-NOTES.md.</p>
  </div>
  {video_slot()}
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">The shape of it</span>
    <h2>What You Get, Plainly</h2></div>
  <div class="grid grid-2">
{chr(10).join(f'  <div class="card reveal"><div class="card-body"><h3>{esc(h)}</h3><p>{esc(p)}</p></div></div>' for h, p in C.WHY)}
  </div>
</div></section>

<section class="section on-mist"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">Questions</span>
    <h2>The Things People Ask First</h2></div>
  <div class="prose prose-wide reveal" style="margin:0 auto">
{faq_block(C.GENERAL_FAQS)}
  </div>
</div></section>
'''
    html += cta_band()
    html += footer()
    write("about.html", html)


# ------------------------------------------------------------------- contact
def build_contact():
    html = head(
        f"Contact {C.OWNER} — Free Estimates | {C.BIZ}",
        f"Call or text {C.PHONE_DISPLAY}, or send the form. Free estimates on handyman work, "
        f"painting and remodeling within {C.RADIUS_MI} miles of {C.HOME_BASE}.")
    html += nav("contact")
    html += page_hero(
        "Get a Free Estimate",
        "Call, text a photo, or fill the form in. Whichever is easiest &mdash; they all reach "
        "the same person.",
        crumbs=[("Home", "/index.html"), ("Contact", None)])

    html += f'''
<section class="section tight"><div class="wrap split lean">
  <div class="reveal">
    <div class="form-panel">
      <h3 style="margin-bottom:4px">Tell {esc(C.OWNER)} what you need</h3>
      <p style="font-size:.94rem;opacity:.72;margin-bottom:20px">A list is fine. So is one
        leaky tap. The more detail you give, the closer the first number will be.</p>
      {quote_form("quote", source=f"{C.BIZ} demo — contact page")}
    </div>
  </div>
  <div class="reveal">
    <div class="channel-card">
      <h3 style="margin-bottom:2px">Or just ring him</h3>
      <p>No office, no answering service &mdash; it is his cell.</p>
      <a class="channel" href="tel:{C.PHONE_TEL}">{ICONS["phone"]}
        <span><b>{C.PHONE_DISPLAY}</b><small>Call &mdash; fastest way to get an answer</small></span></a>
      <a class="channel" href="sms:+1{C.PHONE_TEL}">{ICONS["text"]}
        <span><b>Text a photo</b><small>Best for &ldquo;can you fix this?&rdquo;</small></span></a>
      <a class="channel" href="mailto:{C.EMAIL}">{ICONS["mail"]}
        <span><b>{C.EMAIL}</b><small>Email, if you would rather write it out</small></span></a>
      <p style="margin:18px 0 0;font-size:.88rem;opacity:.72">{ICONS["pin"]}
        Based in {esc(C.HOME_BASE)}, working {C.RADIUS_MI} miles around it.</p>
      <p style="margin:6px 0 0;font-size:.88rem;opacity:.72">{ICONS["wallet"]}
        Estimates are free on anything beyond a small repair.</p>
    </div>
    <div style="margin-top:22px">
      {pricing_table()}
    </div>
  </div>
</div></section>

<section class="section on-mist"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">Before you call</span>
    <h2>Three Things That Speed This Up</h2></div>
  <div class="grid grid-3 steps">
{steps_block([
    ("Take a photo",
     "One picture of the thing that is wrong beats five minutes of describing it. Text it over "
     "and you will usually get a realistic number straight back."),
    ("Write the whole list down",
     "Including the small stuff you think is not worth mentioning. One trip for eight jobs is a "
     "lot cheaper than eight separate call-outs."),
    ("Say when you need it by",
     "If it is urgent, say so. If it can wait until spring, say that too — it often means a "
     "better slot and a better price."),
])}
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">Questions</span>
    <h2>Common Questions</h2></div>
  <div class="prose prose-wide reveal" style="margin:0 auto">
{faq_block(C.GENERAL_FAQS)}
  </div>
</div></section>
'''
    html += footer()
    write("contact.html", html)


# ------------------------------------------------------------------- reviews
# No fabricated reviews anywhere. The sample cards below sit inside a visible
# "this is a layout sample" frame so nobody can mistake them for real ones.
SAMPLE_CARDS = [
    ("A", "What a real review will look like",
     "A sentence or two from a customer about what Rick did, how it went and whether they would "
     "have him back. Google shows the reviewer's name and photo next to it."),
    ("B", "And another one",
     "Reviews that mention the specific job — \"painted two bedrooms and the hallway\" — pull far "
     "more weight than \"great service\", and they help people find him in search."),
    ("C", "And a third",
     "Three to five reviews is the point where a new business starts looking established. Ten is "
     "where people stop hesitating before they call."),
]


def build_reviews():
    samples = "\n".join(f'''    <div class="review-card">
      {stars()}
      <blockquote>&ldquo;{esc(body)}&rdquo;</blockquote>
      <div class="review-meta"><span class="review-ava">{ini}</span>
        <span><b>{esc(name)}</b><small>Sample layout &mdash; not a real review</small></span></div>
    </div>''' for ini, name, body in SAMPLE_CARDS)

    html = head(
        f"Reviews — {C.BIZ}",
        f"{C.BIZ} is building its review history back up after {C.OWNER}'s return to "
        f"{C.CITY}. Here is where his Google reviews will appear.")
    html += nav("reviews")
    html += page_hero(
        "Reviews",
        "There is nothing here yet, and this page is not going to pretend otherwise.",
        crumbs=[("Home", "/index.html"), ("Reviews", None)])

    html += f'''
<section class="section tight"><div class="wrap">
  <div class="prose prose-wide reveal" style="margin:0 auto">
    <p class="lead">{esc(C.OWNER)} has no reviews online yet. That is the honest position and it
      is worth explaining rather than hiding.</p>
    <p>He was working in this area a few years back, was away for a stretch, and has started the
      customer list again from close to nothing. The reviews from before are not attached to
      anything you can search for, and he is not about to put words in anybody&rsquo;s mouth to
      fill a page.</p>
    <p>So this page will stay thin for a little while, and then it will not. Every job he does
      from here ends with him asking for a Google review, and every one of those will land on
      this page automatically.</p>
    <h3>Which cuts both ways</h3>
    <p>If you are weighing up calling someone with no reviews, that is a reasonable thing to
      hesitate over. Two things in his favour. First, you are dealing with the owner, so there is
      nobody to hide behind if the work is poor. Second, a tradesman with three reviews wants
      your job considerably more than one with three hundred &mdash; and right now, he is the
      one with three.</p>
    <p>Ask him for a reference from a job he has done since he came back. He would far rather
      you called one than took his word for it.</p>
  </div>
</div></section>

<section class="section on-mist"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">Design placeholder</span>
    <h2>Where the Reviews Will Sit</h2>
    <p>This is the layout, filled with explanatory text so the page is not empty. Nothing below
       is a real review and nothing below is attributed to a real person.</p></div>
  <div class="sample-frame reveal">
    <span class="sample-label">{ICONS["hand"]} Sample layout &mdash; not real reviews</span>
    <div class="grid grid-3">
{samples}
    </div>
  </div>
</div></section>

<section class="section"><div class="wrap split lean">
  <div class="reveal">
    <span class="eyebrow">If he has worked for you</span>
    <h2>A Review Is Worth More Than a Tip</h2>
    <p>For a one-person business starting over, a Google review is the single most useful thing
      a customer can hand over. It takes two minutes and it is the difference between the next
      person calling and the next person scrolling past.</p>
    <p style="font-size:.95rem;opacity:.75">The button here will point at {esc(C.OWNER)}&rsquo;s
      Google Business Profile once it is set up &mdash; see DEMO-NOTES.md.</p>
    <div class="hero-ctas" style="margin-bottom:0">
      <a class="btn btn-ghost-dark" href="/contact.html#quote">Leave a review (link coming) {ARROW}</a>
    </div>
  </div>
  <div class="reveal">
    <h3>What makes a review useful</h3>
    {check_list([
        "Name the job — \"painted two bedrooms and the hallway\" beats \"great work\"",
        "Say which town you are in, which helps the next neighbour find him",
        "Mention whether he turned up when he said he would",
        "Say whether the final price matched the quote",
        "Add a photo of the finished work if you took one",
    ])}
  </div>
</div></section>
'''
    html += cta_band()
    html += footer()
    write("reviews.html", html)


# ------------------------------------------------------------------- gallery
def build_gallery():
    cards = "\n".join(f"    {ph(k)}" for k, _r, _l, _c in C.SHOT_LIST)

    html = head(
        f"The Work — Photo Gallery | {C.BIZ}",
        f"Photographs of {C.OWNER}'s handyman, painting and remodeling work. This gallery is "
        f"waiting on his own photos — every slot names the shot it needs.")
    html += nav("gallery")
    html += page_hero(
        "The Work",
        "This is the one page on the site that cannot be written. It needs photographs, and "
        "here is exactly which ones.",
        crumbs=[("Home", "/index.html"), ("Work", None)])

    html += f'''
<section class="section tight"><div class="wrap">
  <div class="prose prose-wide reveal" style="margin:0 auto 40px">
    <p class="lead">Nothing sells a tradesman like photographs of finished work, and nothing
      undermines one faster than stock photos of somebody else&rsquo;s house.</p>
    <p>So this gallery is deliberately empty. Every slot below is labelled with the shot that
      belongs in it &mdash; shoot them on a phone, in daylight, and the page fills itself.
      Sixteen photos is plenty; eight is enough to launch with.</p>
    <p style="font-size:.95rem;opacity:.75">A quick note on taking them: shoot in the morning or
      late afternoon rather than the middle of a bright day, stand square on to what you are
      photographing, and get the before shot from the same spot as the after shot. The before
      photos are worth as much as the after ones.</p>
  </div>
  <div class="shot-grid">
{cards}
  </div>
</div></section>

<section class="section on-mist"><div class="wrap split lean">
  <div class="reveal">
    <span class="eyebrow">Worth knowing</span>
    <h2>Why There Are No Stock Photos Here</h2>
    <p>It would have been easy to fill this page with library photographs of other people&rsquo;s
      kitchens. Plenty of contractor sites do exactly that, and customers can tell &mdash; the
      houses look like catalogues and nothing matches the work described.</p>
    <p>Sixteen honest phone photos of real jobs in {esc(C.CITY)} and Normal will out-perform a
      hundred polished stock images, because people recognise their own neighbourhoods and
      they recognise a real job when they see one.</p>
  </div>
  <div class="reveal">
    <h3>The short version of the shot list</h3>
    {check_list([
        "One good photo of Rick actually working — this matters most",
        "Two or three painted rooms, shot from a corner",
        "A before and after pair taken from the same spot",
        "A finished deck, shot low along the boards",
        "A new window from inside and a new door from outside",
        "A tile floor or backsplash, taken from low down",
        "A close-up of trim or a built-in",
        "The van with a ladder on it",
    ])}
  </div>
</div></section>
'''
    html += cta_band()
    html += footer()
    write("gallery.html", html)


# ------------------------------------------------------------------ sitemap
def build_sitemap_page():
    svc = "\n".join(
        f'      <li><a href="/services/{s["slug"]}.html">{esc(s["name"])}</a></li>'
        for s in C.SERVICES)
    areas = "\n".join(
        f'      <li><a href="/areas/{town_slug(t)}.html">{esc(t)}, {C.STATE_ABBR}</a>'
        + (" &mdash; home base" if m == 0 else f" &mdash; {m} mi") + "</li>"
        for t, m, _c in C.TOWNS)

    html = head(f"Sitemap | {C.BIZ}", f"Every page on the {C.BIZ} site.")
    html += nav("")
    html += page_hero("Sitemap", "Every page on the site.",
                      crumbs=[("Home", "/index.html"), ("Sitemap", None)])
    html += f'''
<section class="section"><div class="wrap grid grid-3">
  <div class="reveal">
    <h3>Main pages</h3>
    <ul class="plain-list">
      <li><a href="/index.html">Home</a></li>
      <li><a href="/services.html">What Rick Does</a></li>
      <li><a href="/gallery.html">The Work</a></li>
      <li><a href="/reviews.html">Reviews</a></li>
      <li><a href="/about.html">About {esc(C.OWNER)}</a></li>
      <li><a href="/contact.html">Contact &amp; Free Estimate</a></li>
    </ul>
    <h3 style="margin-top:28px">Services</h3>
    <ul class="plain-list">
{svc}
    </ul>
  </div>
  <div class="reveal" style="grid-column:span 2">
    <h3>Service area &mdash; {len(C.TOWNS)} towns within {C.RADIUS_MI} miles</h3>
    <ul class="plain-list check-grid">
{areas}
    </ul>
  </div>
</div></section>
'''
    html += cta_band()
    html += footer()
    write("sitemap.html", html)


# ------------------------------------------------------- thank you + 404
def build_thank_you():
    html = head(f"Thanks — message sent | {C.BIZ}",
                "Your message has been sent. Here is what happens next.")
    html += nav("")
    html += f'''
<section class="section"><div class="wrap" style="max-width:720px;text-align:center">
  <div class="reveal">
    <span class="eyebrow">Message sent</span>
    <h1 style="font-size:clamp(2rem,4.4vw,3.2rem)">Thanks &mdash; That&rsquo;s Gone Through</h1>
    <p style="font-size:1.12rem;opacity:.8">{esc(C.OWNER)} picks these up himself and gets back
      to people the same day wherever he can. If it is urgent, ringing him is always faster than
      waiting on a reply.</p>
    <div class="hero-ctas" style="justify-content:center">
      <a class="btn btn-amber" href="tel:{C.PHONE_TEL}">{ICONS["phone"]} Call {C.PHONE_DISPLAY}</a>
      <a class="btn btn-ghost-dark" href="/index.html">Back to the site</a>
    </div>
    <p class="form-note" style="margin-top:30px"><b>Demo note:</b> this is a demo site, so what
      you just sent went to <a href="{C.SIXTYMS_URL}" target="_blank" rel="noopener">60 Minute
      Sites</a> rather than to {esc(C.OWNER)}. Nothing has reached him. Forms get pointed at his
      own inbox once the site is paid for and live.</p>
  </div>
</div></section>
'''
    html += footer()
    write("thank-you.html", html)


def build_404():
    html = head(f"Page not found | {C.BIZ}", "That page does not exist.")
    html += nav("")
    html += f'''
<section class="section"><div class="wrap" style="max-width:680px;text-align:center">
  <div class="reveal">
    <span class="eyebrow">404</span>
    <h1 style="font-size:clamp(2rem,4.4vw,3.2rem)">That Page Isn&rsquo;t Here</h1>
    <p style="font-size:1.1rem;opacity:.8">Something has moved or the link was wrong. The
      sitemap has everything on it, or just ring {esc(C.OWNER)} and ask.</p>
    <div class="hero-ctas" style="justify-content:center">
      <a class="btn btn-amber" href="/index.html">Back to the home page</a>
      <a class="btn btn-ghost-dark" href="/sitemap.html">See the sitemap</a>
    </div>
  </div>
</div></section>
'''
    html += footer()
    write("404.html", html)


# ------------------------------------------------------------- non-HTML files
def build_meta_files():
    # Demo site: block every crawler. Flip this at launch.
    (ROOT / "robots.txt").write_text(
        "# DEMO SITE — crawling blocked on purpose.\n"
        "# At launch: replace with 'User-agent: *' / 'Allow: /' and the real sitemap URL.\n"
        "User-agent: *\n"
        "Disallow: /\n", encoding="utf-8")

    (ROOT / "netlify.toml").write_text(
        '[build]\n  publish = "."\n\n'
        '# Demo site — keep it out of search entirely.\n'
        '[[headers]]\n  for = "/*"\n  [headers.values]\n'
        '    X-Robots-Tag = "noindex, nofollow"\n'
        '    X-Content-Type-Options = "nosniff"\n'
        '    Referrer-Policy = "strict-origin-when-cross-origin"\n\n'
        '[[redirects]]\n  from = "/services/"\n  to = "/services.html"\n  status = 301\n\n'
        '[[redirects]]\n  from = "/areas/"\n  to = "/sitemap.html"\n  status = 301\n',
        encoding="utf-8")

    (ROOT / ".gitignore").write_text(
        ".DS_Store\n__pycache__/\n*.pyc\n", encoding="utf-8")


# ------------------------------------------------------------------- the run
def main():
    # clear generated page dirs so renames cannot leave orphans behind
    for d in ("services", "areas"):
        p = ROOT / d
        if p.exists():
            shutil.rmtree(p)

    build_home()
    build_services_hub()
    for s in C.SERVICES:
        build_service(s)
    for t, m, c in C.TOWNS:
        build_area(t, m, c)
    build_about()
    build_contact()
    build_reviews()
    build_gallery()
    build_sitemap_page()
    build_thank_you()
    build_404()
    build_meta_files()

    pages = sorted(p for p in ROOT.rglob("*.html") if "_generator" not in p.parts)
    print(f"built {len(pages)} pages")
    print(f"  {len(C.SERVICES)} services, {len(C.TOWNS)} service areas")
    print(f"  photo placeholders: {len(C.SHOT_LIST)} distinct shots")
    if C.PHONE_IS_PLACEHOLDER:
        print(f"  ! phone is a PLACEHOLDER ({C.PHONE_DISPLAY}) — see DEMO-NOTES.md")


if __name__ == "__main__":
    main()
