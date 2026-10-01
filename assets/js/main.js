/* Killion Remodeling — site behaviour
   Sections 1-7 are the real site. Section 8 is demo-only and is marked
   for deletion at launch (see DEMO-NOTES.md). */
(function () {
  "use strict";

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ------------------------------------------------- 1. sticky header */
  var header = $(".site-header");
  if (header) {
    var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 8); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ------------------------------------------------- 2. mobile nav */
  var burger = $(".nav-burger");
  var nav = $(".main-nav");
  if (burger && nav) {
    burger.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = nav.classList.toggle("open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    $$("a", nav).forEach(function (a) {
      a.addEventListener("click", function () {
        nav.classList.remove("open");
        burger.setAttribute("aria-expanded", "false");
      });
    });
    document.addEventListener("click", function (e) {
      if (!nav.contains(e.target) && e.target !== burger) {
        nav.classList.remove("open");
        burger.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* services dropdown — click to open; CSS :focus-within covers hover/keyboard */
  $$(".nav-drop > button").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var drop = btn.parentElement;
      var wasOpen = drop.classList.contains("open");
      $$(".nav-drop.open").forEach(function (d) { d.classList.remove("open"); });
      drop.classList.toggle("open", !wasOpen);
      btn.setAttribute("aria-expanded", !wasOpen ? "true" : "false");
    });
  });
  document.addEventListener("click", function () {
    $$(".nav-drop.open").forEach(function (d) {
      d.classList.remove("open");
      var b = $("button", d); if (b) b.setAttribute("aria-expanded", "false");
    });
  });

  /* ------------------------------------------------- 3. reveal on scroll */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.04 });
    $$(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    $$(".reveal").forEach(function (el) { el.classList.add("in"); });
  }

  /* ------------------------------------------------- 4. current year */
  $$("[data-year]").forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  /* ------------------------------------------------- 5. deep-link a service
     /contact.html?service=Painting pre-checks the matching box. */
  (function () {
    var want = new URLSearchParams(location.search).get("service");
    if (!want) return;
    $$('input[name="services"]').forEach(function (box) {
      if (box.value.toLowerCase() === want.toLowerCase()) box.checked = true;
    });
  })();

  /* ------------------------------------------------- 6. photo lightbox */
  (function () {
    var box = $(".lightbox");
    if (!box) return;
    var pic = $("img", box);
    var cap = $(".lb-cap", box);
    var group = [];
    var idx = 0;
    var lastFocus = null;

    function show(i) {
      if (!group.length) return;
      idx = (i + group.length) % group.length;
      var a = group[idx];
      pic.src = a.getAttribute("href");
      pic.alt = a.getAttribute("data-cap") || "";
      cap.textContent = a.getAttribute("data-cap") || "";
      var many = group.length > 1;
      $(".lb-prev", box).hidden = !many;
      $(".lb-next", box).hidden = !many;
    }

    function open(a) {
      var name = a.getAttribute("data-lightbox");
      group = $$('a[data-lightbox="' + name + '"]');
      lastFocus = document.activeElement;
      box.hidden = false;
      document.body.style.overflow = "hidden";
      show(group.indexOf(a));
      $(".lb-close", box).focus();
    }

    function close() {
      box.hidden = true;
      pic.removeAttribute("src");
      document.body.style.overflow = "";
      if (lastFocus) lastFocus.focus();
    }

    document.addEventListener("click", function (e) {
      var a = e.target.closest("a[data-lightbox]");
      if (a) { e.preventDefault(); open(a); }
    });
    box.addEventListener("click", function (e) {
      if (e.target === box || e.target.closest(".lb-close")) return close();
      if (e.target.closest(".lb-prev")) return show(idx - 1);
      if (e.target.closest(".lb-next")) return show(idx + 1);
    });
    document.addEventListener("keydown", function (e) {
      if (box.hidden) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowLeft") show(idx - 1);
      else if (e.key === "ArrowRight") show(idx + 1);
    });
  })();

  /* ------------------------------------------------- 7. form plumbing
     Every form posts to the 60 Minute Sites intake endpoint. These hidden
     fields tell 60MS which page and which campaign the lead came from. */
  var t0 = Date.now();
  $$("form[data-hq-form]").forEach(function (f) {
    var set = function (n, v) {
      var el = $('[name="' + n + '"]', f);
      if (el && !el.value) el.value = v;
    };
    var p = new URLSearchParams(location.search);
    set("traffic_source", document.referrer || "direct");
    set("landing_page", location.pathname.replace(/^\//, "") || "index");
    set("utm_campaign", p.get("utm_campaign") || "");
    set("utm_content", p.get("utm_content") || "");
    set("_next", location.origin + "/thank-you.html");
    f.addEventListener("submit", function () {
      var s = $('[name="fill_seconds"]', f);
      if (s) s.value = String(Math.round((Date.now() - t0) / 1000));
    });
  });

  /* =====================================================================
     8. DEMO ONLY — the "this is a demo" modal and the banner's re-open
        button. Delete this section, the .demo-bar markup, the .footer-demo
        markup and the .demo-bar/.demo-modal CSS when the site goes live.
     ================================================================== */
  var DEMO_KEY = "killion-demo-seen";
  var ICON_X = '<svg viewBox="0 0 16 16"><path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/></svg>';

  function demoModal() {
    var old = $(".demo-modal");
    if (old) old.remove();

    var d = document.createElement("div");
    d.className = "demo-modal";
    d.setAttribute("role", "dialog");
    d.setAttribute("aria-modal", "true");
    d.setAttribute("aria-label", "This is a demo site");
    d.innerHTML =
      '<div class="dm-card" role="document">' +
        '<button class="dm-close" type="button" aria-label="Close">' + ICON_X + "</button>" +
        '<span class="dm-badge">Demo preview</span>' +
        "<h2>This is a demo site</h2>" +
        "<p>You are looking at a design concept built for <b>Killion Remodeling</b> " +
        'by <a href="https://60minutesites.com" target="_blank" rel="noopener">60&nbsp;Minute&nbsp;Sites</a>. ' +
        "It is here so Rick can see what his own site would look like before he buys one.</p>" +
        "<p>Two things to know while you click around. The photographs are " +
        '<a href="/credits.html">library images</a> standing in until Rick&rsquo;s own are taken. ' +
        "And <b>every form on this site sends to 60 Minute Sites, not to Rick</b> &mdash; they get " +
        "pointed at his inbox once the site is paid for and live.</p>" +
        '<button class="btn btn-gold btn-block" type="button" data-dismiss>Have a look around</button>' +
        '<p class="dm-foot">Want one of these? ' +
        '<a href="https://60minutesites.com/pricing.html" target="_blank" rel="noopener">See pricing</a></p>' +
      "</div>";
    document.body.appendChild(d);
    requestAnimationFrame(function () { d.classList.add("is-on"); });

    function kill() {
      d.classList.remove("is-on");
      document.removeEventListener("keydown", onKey);
      setTimeout(function () { d.remove(); }, 220);
    }
    function onKey(e) { if (e.key === "Escape") kill(); }
    d.addEventListener("click", function (e) {
      if (e.target === d || e.target.closest("[data-dismiss]") || e.target.closest(".dm-close")) kill();
    });
    document.addEventListener("keydown", onKey);
    var ok = $("[data-dismiss]", d);
    if (ok) ok.focus();
  }
  window.demoModal = demoModal;

  /* the banner's "what's this?" button re-opens it any time */
  $$("[data-demo-open]").forEach(function (b) {
    b.addEventListener("click", function (e) { e.preventDefault(); demoModal(); });
  });

  /* auto-open once per browser session */
  (function () {
    var seen = null;
    try { seen = window.sessionStorage.getItem(DEMO_KEY); } catch (e) { seen = null; }
    if (seen) return;
    try { window.sessionStorage.setItem(DEMO_KEY, "1"); } catch (e) { /* private mode */ }
    setTimeout(demoModal, 1100);
  })();
})();
