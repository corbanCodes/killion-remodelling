#!/usr/bin/env python3
"""Killion Remodeling — site generator.

Reads content.py and writes the whole static site into the repo root.
Run:  python3 _generator/build.py

Design system is the North Line Property Services system, re-skinned to the
navy/gold/rust taken straight out of Rick's logo.
"""
import json
import re
import shutil
from pathlib import Path

import content as C

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PHOTO_DIR = ROOT / "assets" / "img" / "photos"


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
    wrench='<svg viewBox="0 0 16 16"><path d="M.102 2.223A3.004 3.004 0 0 0 3.78 5.897l6.341 6.252A3.003 3.003 0 0 0 13 16a3 3 0 1 0-.851-5.878L5.897 3.781A3.004 3.004 0 0 0 2.223.1l2.141 2.142L4 4l-1.757.364zm13.37 9.019.528.026.287.445.445.287.026.529L15 13l-.242.471-.026.529-.445.287-.287.445-.529.026L13 15l-.471-.242-.529-.026-.287-.445-.445-.287-.026-.529L11 13l.242-.471.026-.529.445-.287.287-.445.529-.026L13 11z"/></svg>',
    roller='<svg viewBox="0 0 16 16"><path d="M2 1.5A1.5 1.5 0 0 1 3.5 0h9A1.5 1.5 0 0 1 14 1.5v3A1.5 1.5 0 0 1 12.5 6H10v1.5A1.5 1.5 0 0 1 8.5 9H8v1.5a1.5 1.5 0 0 1-1 1.415V15a1 1 0 1 1-2 0v-3.085A1.5 1.5 0 0 1 4 10.5V9h-.5A1.5 1.5 0 0 1 2 7.5zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5z"/></svg>',
    deck='<svg viewBox="0 0 16 16"><path d="M1 3h14v1.5H1zM1 6h14v1.5H1zM1 9h14v1.5H1zM2.5 11.5H4V16H2.5zM12 11.5h1.5V16H12z"/></svg>',
    window='<svg viewBox="0 0 16 16"><path d="M2 1a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zm.5 1.5h5v5h-5zm6.5 0h5v5H9zm-6.5 6.5h5v5h-5zm6.5 0h5v5H9z"/></svg>',
    tile='<svg viewBox="0 0 16 16"><path d="M1 1h6.3v6.3H1zM8.7 1H15v6.3H8.7zM1 8.7h6.3V15H1zM8.7 8.7H15V15H8.7z"/></svg>',
    saw='<svg viewBox="0 0 16 16"><path d="M0 4.5 1.8 6l1.4-1.5L4.6 6 6 4.5 7.4 6l1.4-1.5L10.2 6l1.4-1.5L13 6l1.5-1.5V8H0zM0 9h15v2a1 1 0 0 1-1 1H1a1 1 0 0 1-1-1z"/></svg>',
    house='<svg viewBox="0 0 16 16"><path d="M8.707 1.5a1 1 0 0 0-1.414 0L.646 8.146a.5.5 0 0 0 .708.708L8 2.207l6.646 6.647a.5.5 0 0 0 .708-.708L13 5.793V2.5a.5.5 0 0 0-.5-.5h-2a.5.5 0 0 0-.5.5v1.293zM2.5 14a1 1 0 0 0 1 1h3v-4h3v4h3a1 1 0 0 0 1-1V9.5L8 3.5 2.5 9z"/></svg>',
    hand='<svg viewBox="0 0 16 16"><path d="M8 1a.5.5 0 0 1 .5.5v5a.5.5 0 0 0 1 0V2a.5.5 0 0 1 1 0v4.5a.5.5 0 0 0 1 0V3.5a.5.5 0 0 1 1 0V9a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V6.5a.5.5 0 0 1 1 0V9a.5.5 0 0 0 1 0V2.5a.5.5 0 0 1 1 0v4a.5.5 0 0 0 1 0v-5A.5.5 0 0 1 8 1"/></svg>',
    zoom='<svg viewBox="0 0 16 16"><path d="M6.5 1a5.5 5.5 0 1 0 3.473 9.77l3.628 3.63a.75.75 0 1 0 1.061-1.06l-3.629-3.63A5.5 5.5 0 0 0 6.5 1m-4 5.5a4 4 0 1 1 8 0 4 4 0 0 1-8 0"/><path d="M6.5 3.75a.5.5 0 0 1 .5.5V6h1.75a.5.5 0 0 1 0 1H7v1.75a.5.5 0 0 1-1 0V7H4.25a.5.5 0 0 1 0-1H6V4.25a.5.5 0 0 1 .5-.5"/></svg>',
)


def stars():
    return '<span class="stars">' + STAR * 5 + "</span>"


# ----------------------------------------------------------------- components
def img(key, cls="", lazy=True):
    """A real photograph from assets/img/photos."""
    f, alt = C.PHOTOS[key]
    attrs = f' class="{cls}"' if cls else ""
    ld = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<img src="/assets/img/photos/{f}" alt="{esc(alt)}"{attrs}{ld}>'


def figure(key, cls=""):
    return f'<figure class="shot {cls}">{img(key)}</figure>'


def gal_item(key, group="all"):
    f, alt = C.PHOTOS[key]
    return (f'    <a class="gal-item reveal" href="/assets/img/photos/{f}" '
            f'data-lightbox="{group}" data-cap="{esc(alt)}" aria-label="{esc(alt)}">'
            f'{img(key)}<span class="gal-zoom">{ICONS["zoom"]}</span></a>')


def check_list(items, cls="check-list"):
    lis = "\n".join(f"  <li>{CHECK}<span>{esc(i)}</span></li>" for i in items)
    return f'<ul class="{cls}">\n{lis}\n</ul>'


def faq_block(faqs):
    return "\n".join(
        f'<details class="faq"><summary>{esc(q)}{PLUS}</summary>\n'
        f'  <div class="faq-body"><p>{esc(a)}</p></div></details>'
        for q, a in faqs)


def service_card(s):
    key = C.SERVICE_CARD_PHOTO[s["slug"]]
    return f'''<a class="card reveal" href="/services/{s["slug"]}.html">
  <div class="card-img">{img(key)}
    <span class="card-ico">{ICONS[s["ico"]]}</span></div>
  <div class="card-body">
    <small class="card-kicker">{esc(s["kicker"])}</small>
    <h3>{esc(s["short"])}</h3>
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


# ---------------------------------------------------------------------- forms
def quote_form(form_id="quote", compact=False, minimal=False, source="", preselect=""):
    """The 60 Minute Sites intake form. Posts to 60MS, not to Rick — see the note."""
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
        <button class="btn btn-gold btn-block" type="submit">Send it to {esc(C.OWNER)} {ARROW}</button>
        <p class="form-note"><b>Demo note:</b> while this site is a demo, everything sent through
          this form goes to <a href="{C.SIXTYMS_URL}" target="_blank" rel="noopener">60&nbsp;Minute&nbsp;Sites</a>
          &mdash; not to {esc(C.OWNER)}. Forms get pointed at his own inbox once the site is paid
          for and live.</p>
      </div>
    </form>'''


# --------------------------------------------------------------- page chrome
def head(title, desc):
    f, _alt = C.PHOTOS["hero"]
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
<meta property="og:image" content="/assets/img/photos/{f}">
<meta name="theme-color" content="#012344">
<link rel="icon" type="image/png" href="/assets/img/mark.png">
<link rel="apple-touch-icon" href="/assets/img/mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,400..900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/main.css">
</head>
<body>

<!-- DEMO — delete this div, the .footer-demo block, section 8 of main.js and
     the .demo-bar/.demo-modal CSS when the site goes live. -->
<div class="demo-bar"><span class="demo-dot"></span><strong>DEMO PREVIEW</strong><span
  class="demo-tail"> &mdash; a design concept for {esc(C.BIZ)} by
  <a href="{C.SIXTYMS_URL}" target="_blank" rel="noopener">60&nbsp;Minute&nbsp;Sites</a>
  &middot; stand-in photography &middot; all forms go to 60MS, not to {esc(C.OWNER)}</span>
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
  <span class="util-hide">{ICONS["pin"]} {C.RADIUS_MI} miles around {esc(C.HOME_BASE)}</span>
  <span class="util-spacer"></span>
  <a class="util-hide" href="mailto:{C.EMAIL}">{ICONS["mail"]} {C.EMAIL}</a>
</div></div>

<header class="site-header"><div class="wrap nav-row">
  <a class="brand" href="/index.html" aria-label="{esc(C.BIZ)} &mdash; home">
    <img src="/assets/img/logo.png" alt="{esc(C.BIZ)}" width="2095" height="751">
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
    <a href="/contact.html#quote" class="btn btn-gold btn-sm nav-cta">Free Estimate</a>
  </nav>
</div></header>
'''


def page_hero(h1, p, crumbs=None, photo="rick-at-work"):
    cr = ""
    if crumbs:
        parts = [f'<a href="{href}">{esc(label)}</a>' if href else esc(label)
                 for label, href in crumbs]
        cr = f'<div class="crumbs">{" / ".join(parts)}</div>'
    return f'''
<section class="page-hero">
  <div class="hero-media">{img(photo, lazy=False)}</div>
  <div class="wrap">
  {cr}
  <h1>{h1}</h1>
  <p>{p}</p>
</div></section>
'''


def cta_band(h=None, p=None, photo="painting-exterior"):
    h = h or f"Get {C.OWNER} to Come and Look"
    p = p or ("Free estimates on anything beyond a small repair, a straight price, and the "
              "person who quotes it is the person who does the work.")
    return f'''
<section class="section cta-band">
  <div class="hero-media">{img(photo)}</div>
  <div class="wrap reveal">
  <span class="eyebrow">Free estimates</span>
  <h2>{esc(h)}</h2>
  <p>{esc(p)}</p>
  <div class="hero-ctas">
    <a class="btn btn-gold btn-lg" href="tel:{C.PHONE_TEL}">{ICONS["phone"]} Call {C.PHONE_DISPLAY}</a>
    <a class="btn btn-ghost btn-lg" href="/contact.html#quote">Send the form instead</a>
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
      <img src="/assets/img/logo-light.png" alt="{esc(C.BIZ)}" width="2095" height="751" loading="lazy">
      <p>Handyman work, painting and general remodeling, owner-operated out of
         {esc(C.HOME_BASE)} and {C.RADIUS_MI} miles around it.</p>
      <a class="btn btn-gold btn-sm" href="tel:{C.PHONE_TEL}">{ICONS["phone"]} {C.PHONE_DISPLAY}</a>
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
    {esc(C.OWNER)} what his own site could look like. The photographs are
    <a href="/credits.html">library images</a> standing in until his own are taken, there are no
    customer reviews on it yet, and
    <b>every form submits to 60 Minute Sites rather than to {esc(C.OWNER)}</b> until the site is
    paid for and live. <a href="{C.PRICING_URL}" target="_blank" rel="noopener">See pricing</a>.</div>
  <div class="wrap footer-bottom">
    <span>&copy; <span data-year>2026</span> {esc(C.BIZ)}</span>
    <span class="spacer"></span>
    <span><a href="/credits.html">Photo credits</a> &middot;
      Demo site by <a href="{C.SIXTYMS_URL}" target="_blank" rel="noopener">60 Minute Sites</a></span>
  </div>
</footer>

<nav class="dock" aria-label="Quick actions">
  <a href="tel:{C.PHONE_TEL}">{ICONS["phone"]} Call</a>
  <a href="sms:+1{C.PHONE_TEL}">{ICONS["text"]} Text</a>
  <a href="mailto:{C.EMAIL}">{ICONS["mail"]} Email</a>
  <a class="dock-primary" href="/contact.html#quote">{ICONS["cal"]} Estimate</a>
</nav>

<div class="lightbox" hidden>
  <button class="lb-close" type="button" aria-label="Close">&times;</button>
  <button class="lb-prev" type="button" aria-label="Previous">&#8249;</button>
  <img alt="">
  <button class="lb-next" type="button" aria-label="Next">&#8250;</button>
  <span class="lb-cap"></span>
</div>

<script src="/assets/js/main.js" defer></script>
</body>
</html>'''


def write(rel, html):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")


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
        f'  <div class="why reveal"><h3>{esc(h)}</h3><p>{esc(p)}</p></div>'
        for h, p in C.WHY)

    chips = " ".join(
        f'<a class="chip" href="/areas/{town_slug(t)}.html">{esc(t)}</a>'
        for t, _m, _c in C.TOWNS[:14])

    strip = "\n".join(
        gal_item(k, "home") for k in
        ["painted-room", "deck-finished", "window-install", "flooring-plank",
         "trim-work", "door-exterior"])

    html = head(
        f"{C.BIZ} — Handyman, Painting & Home Repairs in {C.CITY}, {C.STATE_ABBR}",
        f"Owner-operated handyman and painting work in {C.CITY}-Normal and {C.RADIUS_MI} miles "
        f"around it. Repairs, interior and exterior painting, decks, windows, flooring and trim. "
        f"Free estimates — call or text {C.PHONE_DISPLAY}.")
    html += nav("home")

    html += f'''
<section class="hero">
  <div class="hero-media">{img("hero", lazy=False)}</div>
  <div class="wrap hero-split">
  <div class="hero-inner">
    <span class="eyebrow">{esc(C.CITY)} &amp; Normal, {C.STATE_ABBR} &mdash; handyman, painting &amp; repairs</span>
    <h1>One Person for <em>the Whole List</em></h1>
    <p class="hero-sub">{esc(C.OWNER)} is a handyman and painter working out of {esc(C.HOME_BASE)}.
      The leaky sink, the room that needs painting, the deck boards gone soft, the door that will
      not shut &mdash; call him once and it all gets sorted by the same person.</p>
    <div class="hero-ctas">
      <a class="btn btn-gold btn-lg" href="tel:{C.PHONE_TEL}">{ICONS["phone"]} Call {C.PHONE_DISPLAY}</a>
      <a class="btn btn-ghost btn-lg" href="/contact.html#quote">Get a free estimate</a>
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
  <p style="margin-top:30px;text-align:center" class="reveal">
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
      <a class="btn btn-gold" href="/about.html">More about {esc(C.OWNER)} {ARROW}</a>
    </div>
  </div>
  <div class="reveal">{figure("rick-at-work")}</div>
</div></section>

<section class="section on-white"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">Why call him</span>
    <h2>What You Actually Get</h2></div>
  <div class="grid grid-2 why-grid">
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

<section class="section tight"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">The work</span>
    <h2>A Look at the Kind of Thing He Does</h2>
    <p>Painting, decks, windows, floors and trim &mdash; around {esc(C.CITY)}, Normal and the
       towns in between.</p></div>
  <div class="gal-grid cols-3">
{strip}
  </div>
  <p style="text-align:center;margin-top:30px" class="reveal">
    <a class="btn btn-ghost-dark" href="/gallery.html">See more of the work {ARROW}</a></p>
</div></section>

<section class="section on-white"><div class="wrap split lean">
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
        crumbs=[("Home", "/index.html"), ("What Rick Does", None)],
        photo="tools")

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
def build_service(s):
    main_photo, extra = C.SERVICE_PHOTOS[s["slug"]]
    body = "\n".join(f'    <h3>{esc(h)}</h3>\n    <p>{esc(p)}</p>' for h, p in s["body"])

    other = [x for x in C.SERVICES if x["slug"] != s["slug"]][:3]
    other_html = "\n".join(service_card(x) for x in other)

    pills = "\n".join(
        f'  <a href="/services/{x["slug"]}.html"'
        + (' class="active"' if x["slug"] == s["slug"] else "")
        + f'>{esc(x["short"])}</a>'
        for x in C.SERVICES)

    extra_shots = ""
    if extra:
        cards = "\n".join(gal_item(k, "svc") for k in extra)
        extra_shots = f'''
<section class="section tight on-white"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">The work</span>
    <h2>{esc(s["short"])} in Practice</h2></div>
  <div class="gal-grid cols-{len(extra)}">
{cards}
  </div>
</div></section>
'''

    svc_q = esc(s["short"]).replace("&amp;", "%26").replace(" ", "+")

    html = head(
        f"{s['name']} in {C.CITY}, {C.STATE_ABBR} | {C.BIZ}",
        f"{s['blurb']} Owner-operated, free estimates, {C.RADIUS_MI} miles around {C.HOME_BASE}.")
    html += nav("services")
    html += page_hero(
        esc(s["hero_h"]), esc(s["hero_p"]),
        crumbs=[("Home", "/index.html"), ("What Rick Does", "/services.html"), (s["short"], None)],
        photo=main_photo)

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
    <aside class="reveal side-cta">
      <div class="side-box">
        <h3>Get a price on this</h3>
        <p>Free estimate, and no pressure at the end of it.</p>
        <a class="btn btn-gold btn-block" href="tel:{C.PHONE_TEL}">{ICONS["phone"]} {C.PHONE_DISPLAY}</a>
        <a class="btn btn-ghost-dark btn-block" style="margin-top:10px"
           href="/contact.html?service={svc_q}#quote">Send the form instead</a>
      </div>
    </aside>
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
          "Free estimates on anything beyond a small repair.",
        photo=main_photo)
    html += footer()
    write(f"services/{s['slug']}.html", html)


# ----------------------------------------------------------------- area pages
AREA_PHOTOS = ["door-exterior", "painting-exterior", "deck-finished", "painted-room",
               "handyman-repair", "window-install"]


def build_area(town, miles, county, idx):
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
        f'      <li><a href="/services/{s["slug"]}.html">{esc(s["name"])}</a></li>'
        for s in C.SERVICES)

    html = head(
        f"Handyman & Painter in {town}, {C.STATE_ABBR} | {C.BIZ}",
        f"Handyman work, painting and home repairs in {town}, {C.STATE_ABBR}. Owner-operated, "
        f"free estimates, {C.RADIUS_MI} miles around {C.HOME_BASE}.")
    html += nav("areas")
    html += page_hero(
        f"Handyman &amp; Painting in {esc(town)}, {C.STATE_ABBR}",
        f"{esc(county)} &mdash; "
        + (f"{esc(C.OWNER)}&rsquo;s home town." if is_home
           else f"about {miles} miles from {esc(C.OWNER)}&rsquo;s base in {esc(C.CITY)}."),
        crumbs=[("Home", "/index.html"), ("Service Area", "/sitemap.html"), (town, None)],
        photo=AREA_PHOTOS[idx % len(AREA_PHOTOS)])

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
    <ul class="plain-list check-grid">
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
          "texted over usually gets you a price without anyone driving anywhere.",
        photo=AREA_PHOTOS[(idx + 3) % len(AREA_PHOTOS)])
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
        crumbs=[("Home", "/index.html"), ("About Rick", None)],
        photo="rick-at-work")

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
  <aside class="reveal side-cta">
    {figure("painting-detail")}
    <div class="channel-card">
      <h3 style="margin-bottom:2px">Get hold of {esc(C.OWNER)}</h3>
      <p>He answers his own phone.</p>
      <a class="channel" href="tel:{C.PHONE_TEL}">{ICONS["phone"]}
        <span><b>{C.PHONE_DISPLAY}</b><small>Call &mdash; fastest way</small></span></a>
      <a class="channel" href="sms:+1{C.PHONE_TEL}">{ICONS["text"]}
        <span><b>Text a photo</b><small>Usually gets you a price same day</small></span></a>
      <a class="channel" href="mailto:{C.EMAIL}">{ICONS["mail"]}
        <span><b>{C.EMAIL}</b><small>Email</small></span></a>
    </div>
  </aside>
</div></section>

<section class="section on-white"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">The shape of it</span>
    <h2>What You Get, Plainly</h2></div>
  <div class="grid grid-2 why-grid">
{chr(10).join(f'  <div class="why reveal"><h3>{esc(h)}</h3><p>{esc(p)}</p></div>' for h, p in C.WHY)}
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
    html += cta_band(photo="deck-finished")
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
        crumbs=[("Home", "/index.html"), ("Contact", None)],
        photo="window-work")

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
# No fabricated reviews anywhere. The sample cards sit inside a visible frame.
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
        crumbs=[("Home", "/index.html"), ("Reviews", None)],
        photo="carpentry-mark")

    html += f'''
<section class="section tight"><div class="wrap split lean">
  <div class="prose reveal">
    <p class="lead">{esc(C.OWNER)} has no reviews online yet, and this page is not going to
      invent any.</p>
    <p>He worked this area a few years back, was away for a stretch, and has started the
      customer list again from close to nothing. The reviews from before are not attached to
      anything you can search for.</p>
    <p>So the page stays thin for a little while, and then it will not. Every job from here ends
      with him asking for a Google review, and every one of those lands here automatically.</p>
    <h3>Which cuts both ways</h3>
    <p>If you are weighing up calling someone with no reviews, that is fair enough. Two things
      in his favour. You are dealing with the owner, so there is nobody to hide behind if the
      work is poor. And a tradesman with three reviews wants your job considerably more than one
      with three hundred &mdash; right now, he is the one with three.</p>
    <p>Ask him for a reference from a job he has done since he came back. He would far rather
      you rang one than took his word for it.</p>
  </div>
  <aside class="reveal side-cta">
    {figure("painted-room")}
    <div class="side-box">
      <h3>Be one of the first</h3>
      <p>Small jobs welcome. That is how a review list starts.</p>
      <a class="btn btn-gold btn-block" href="tel:{C.PHONE_TEL}">{ICONS["phone"]} {C.PHONE_DISPLAY}</a>
    </div>
  </aside>
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

<section class="section on-white"><div class="wrap split lean">
  <div class="reveal">
    <span class="eyebrow">If he has worked for you</span>
    <h2>A Review Is Worth More Than a Tip</h2>
    <p>For a one-person business starting over, a Google review is the single most useful thing
      a customer can hand over. It takes two minutes and it is the difference between the next
      person calling and the next person scrolling past.</p>
    <p style="font-size:.95rem;opacity:.75"><b>Demo note:</b> this button will point straight at
      {esc(C.OWNER)}&rsquo;s Google Business Profile once that is set up.</p>
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
    html += cta_band(photo="trim-work")
    html += footer()
    write("reviews.html", html)


# ------------------------------------------------------------------- gallery
def build_gallery():
    items = "\n".join(gal_item(k) for k in C.GALLERY)

    html = head(
        f"The Work — Gallery | {C.BIZ}",
        f"Painting, decks, windows, flooring and trim work by {C.BIZ} around {C.CITY} and "
        f"Normal, Illinois.")
    html += nav("gallery")
    html += page_hero(
        "The Work",
        "Painting, decks, windows, floors and trim &mdash; the kind of jobs that fill most weeks.",
        crumbs=[("Home", "/index.html"), ("Work", None)],
        photo="painting-interior")

    html += f'''
<section class="section tight"><div class="wrap">
  <div class="gal-grid cols-3">
{items}
  </div>
  <p class="gal-note reveal">These are library photographs standing in while {esc(C.OWNER)}
    gets his own taken &mdash; see <a href="/credits.html">credits</a>.</p>
</div></section>

<section class="section on-mist"><div class="wrap split lean">
  <div class="reveal">
    <span class="eyebrow">What you are looking at</span>
    <h2>One Person, Most of the Trades</h2>
    <p>Very little of what Rick does is exotic. It is painting, boards, glass, floors and trim
      &mdash; done carefully, cleaned up behind, and finished when he said it would be.</p>
    <p>The value in calling one person for all of it is not really the price. It is that nobody
      has to coordinate four trades, and nobody can blame the last person who was in the house.</p>
    <div class="hero-ctas" style="margin-bottom:0">
      <a class="btn btn-gold" href="/contact.html#quote">Get a free estimate {ARROW}</a>
    </div>
  </div>
  <div class="reveal">
    <h3>Most-asked-for jobs</h3>
    {check_list([
        "A room, a hallway or a whole interior painted",
        "The outside of the house, or just the trim and front door",
        "Deck boards, railings and a fresh coat of stain",
        "Draughty windows and doors that will not shut",
        "Tile, carpet or vinyl plank over a subfloor worth checking",
        "Baseboard, crown, casing and built-ins",
        "A list of small repairs in one visit",
    ])}
  </div>
</div></section>
'''
    html += cta_band(photo="deck-repair")
    html += footer()
    write("gallery.html", html)


# ------------------------------------------------------------------- credits
def build_credits():
    cj = HERE / "credits.json"
    rows = ""
    if cj.exists():
        data = json.loads(cj.read_text())
        seen = set()
        order = C.GALLERY + [k for k in C.PHOTOS if k not in C.GALLERY]
        for key in order:
            pid = data["plan"].get(key)
            if not pid or pid in seen:
                continue
            seen.add(pid)
            m = data["meta"][pid]
            rows += (f'      <tr><td>{esc(C.PHOTOS[key][1])}</td>'
                     f'<td><a href="{m["profile"]}" rel="noopener nofollow" target="_blank">{esc(m["who"])}</a></td>'
                     f'<td><a href="{m["page"]}" rel="noopener nofollow" target="_blank">Unsplash</a></td></tr>\n')

    html = head(f"Photo credits | {C.BIZ}", "Where the photographs on this site come from.")
    html += nav("")
    html += page_hero(
        "Photo Credits",
        "Every photograph on this site, and where it came from.",
        crumbs=[("Home", "/index.html"), ("Credits", None)],
        photo="tools")
    html += f'''
<section class="section tight"><div class="wrap prose prose-wide">
  <p class="lead">The photographs on this site are library images, not photographs of
    {esc(C.OWNER)}&rsquo;s own work.</p>
  <p>They come from <a href="https://unsplash.com" rel="noopener" target="_blank">Unsplash</a> and
    are used under the <a href="https://unsplash.com/license" rel="noopener" target="_blank">Unsplash
    licence</a>, which permits commercial use without attribution. They are credited here anyway.</p>
  <p>They stand in for the kinds of job {esc(C.OWNER)} does until there are photographs of his
    own to replace them. Swapping one in is a single file drop &mdash; same filename, same folder,
    and the whole site updates.</p>
  <div class="rate-wrap" style="margin-top:28px"><table class="rate-table">
    <thead><tr><th>Photograph</th><th>Photographer</th><th>Source</th></tr></thead>
    <tbody>
{rows}    </tbody></table></div>
  <p style="margin-top:26px;font-size:.92rem;opacity:.7">The {esc(C.BIZ)} logo is Rick&rsquo;s own.
    The rest of the site &mdash; layout, type and code &mdash; was built by
    <a href="{C.SIXTYMS_URL}" rel="noopener" target="_blank">60 Minute Sites</a>.</p>
</div></section>
'''
    html += footer()
    write("credits.html", html)


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
                      crumbs=[("Home", "/index.html"), ("Sitemap", None)],
                      photo="door-exterior")
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
      <li><a href="/credits.html">Photo credits</a></li>
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
    html += cta_band(photo="painted-room")
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
      <a class="btn btn-gold" href="tel:{C.PHONE_TEL}">{ICONS["phone"]} Call {C.PHONE_DISPLAY}</a>
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
      <a class="btn btn-gold" href="/index.html">Back to the home page</a>
      <a class="btn btn-ghost-dark" href="/sitemap.html">See the sitemap</a>
    </div>
  </div>
</div></section>
'''
    html += footer()
    write("404.html", html)


# ------------------------------------------------------------- non-HTML files
def build_meta_files():
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
        '[[headers]]\n  for = "/assets/*"\n  [headers.values]\n'
        '    Cache-Control = "public, max-age=31536000, immutable"\n\n'
        '[[redirects]]\n  from = "/services/"\n  to = "/services.html"\n  status = 301\n\n'
        '[[redirects]]\n  from = "/areas/"\n  to = "/sitemap.html"\n  status = 301\n',
        encoding="utf-8")

    (ROOT / ".gitignore").write_text(".DS_Store\n__pycache__/\n*.pyc\n", encoding="utf-8")


# ------------------------------------------------------------------- the run
def main():
    for d in ("services", "areas"):
        p = ROOT / d
        if p.exists():
            shutil.rmtree(p)

    missing = [k for k, (f, _a) in C.PHOTOS.items() if not (PHOTO_DIR / f).exists()]
    if missing:
        raise SystemExit(f"missing photo files for: {missing}")

    build_home()
    build_services_hub()
    for s in C.SERVICES:
        build_service(s)
    for i, (t, m, c) in enumerate(C.TOWNS):
        build_area(t, m, c, i)
    build_about()
    build_contact()
    build_reviews()
    build_gallery()
    build_credits()
    build_sitemap_page()
    build_thank_you()
    build_404()
    build_meta_files()

    pages = sorted(p for p in ROOT.rglob("*.html") if "_generator" not in p.parts)
    photos = sorted(PHOTO_DIR.glob("*.jpg"))
    print(f"built {len(pages)} pages")
    print(f"  {len(C.SERVICES)} services, {len(C.TOWNS)} service areas")
    print(f"  {len(photos)} photographs ({sum(p.stat().st_size for p in photos)//1024} KB)")
    if C.PHONE_IS_PLACEHOLDER:
        print(f"  ! phone is a PLACEHOLDER ({C.PHONE_DISPLAY}) — see DEMO-NOTES.md")


if __name__ == "__main__":
    main()
