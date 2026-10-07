/* James Skipper Painting site script. No dependencies. */
(function () {
  "use strict";

  var DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Business hours, always in Virginia (Eastern) time. Hours are placeholders until the client confirms them. */
  function localNow() {
    var parts = new Intl.DateTimeFormat("en-US", {
      timeZone: "America/New_York", weekday: "long", hour: "numeric", minute: "numeric", hour12: false
    }).formatToParts(new Date());
    var get = function (t) { return (parts.find(function (p) { return p.type === t; }) || {}).value; };
    return { day: DAYS.indexOf(get("weekday")), mins: (parseInt(get("hour"), 10) % 24) * 60 + parseInt(get("minute"), 10) };
  }
  function applyHours() {
    var now = localNow();
    var weekday = now.day >= 1 && now.day <= 5;
    var open = weekday && now.mins >= 480 && now.mins < 1020;
    var text = open ? "Open now until 5pm"
      : weekday && now.mins < 480 ? "Opens today at 8am"
      : "Closed, opens " + (now.day === 5 || now.day === 6 ? "Monday" : "tomorrow") + " at 8am";
    document.querySelectorAll("[data-hours-status]").forEach(function (el) {
      el.classList.toggle("is-open", open);
      var t = el.querySelector("[data-hours-text]");
      if (t) t.textContent = text;
    });
    document.querySelectorAll("[data-day]").forEach(function (row) {
      row.classList.toggle("is-today", row.getAttribute("data-day") === DAYS[now.day]);
    });
  }

  /* Sticky header gets a hairline shadow once you scroll. */
  function stickyHeader() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 4); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* Navigation block overlay menu (mobile). */
  function overlayMenu() {
    var openBtn = document.querySelector(".wp-block-navigation__responsive-container-open");
    var panel = document.querySelector(".wp-block-navigation__responsive-container");
    if (!openBtn || !panel) return;
    var closeBtn = panel.querySelector(".wp-block-navigation__responsive-container-close");
    function open() {
      panel.classList.add("is-menu-open", "has-modal-open");
      openBtn.setAttribute("aria-expanded", "true");
      document.documentElement.classList.add("has-modal-open");
      closeBtn.focus();
    }
    function close() {
      panel.classList.remove("is-menu-open", "has-modal-open");
      openBtn.setAttribute("aria-expanded", "false");
      document.documentElement.classList.remove("has-modal-open");
      openBtn.focus();
    }
    openBtn.addEventListener("click", open);
    closeBtn.addEventListener("click", close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && panel.classList.contains("is-menu-open")) close(); });
  }

  /* Image block "Expand on click" lightbox, same zoom animation as WordPress core. */
  function lightbox() {
    var figures = document.querySelectorAll(".wp-lightbox-container");
    if (!figures.length) return;
    var overlay = document.createElement("div");
    overlay.className = "wp-lightbox-overlay zoom";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Enlarged image");
    overlay.tabIndex = -1;
    overlay.innerHTML = '<button type="button" aria-label="Close" class="wp-lightbox-close-button"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false"><path d="m13.06 12 6.47-6.47-1.06-1.06L12 10.94 5.53 4.47 4.47 5.53 10.94 12l-6.47 6.47 1.06 1.06L12 13.06l6.47 6.47 1.06-1.06L13.06 12Z"></path></svg></button>' +
      '<div class="lightbox-image-container"><figure class="wp-block-image"><img alt=""></figure></div><div class="scrim" aria-hidden="true"></div>';
    document.body.appendChild(overlay);
    var big = overlay.querySelector("img");
    var lastTrigger = null;

    function openFrom(img, trigger) {
      lastTrigger = trigger;
      // Same approach as WordPress core: zoom from the thumbnail's crop, never stretch it.
      var r = img.getBoundingClientRect();
      var natW = img.naturalWidth || r.width, natH = img.naturalHeight || r.height;
      var ratio = natW / natH;
      var maxW = Math.min(window.innerWidth - 80, 1400), maxH = window.innerHeight - 120;
      var w = Math.min(maxW, natW), h = w / ratio;
      if (h > maxH) { h = maxH; w = h * ratio; }
      var scale = Math.max(r.width / w, r.height / h);
      var left = r.left - (w * scale - r.width) / 2;
      var top = r.top - (h * scale - r.height) / 2;
      var dx = Math.max(0, (w - r.width / scale) / 2), dy = Math.max(0, (h - r.height / scale) / 2);
      var s = overlay.style;
      s.setProperty("--wp--lightbox-container-width", w + "px");
      s.setProperty("--wp--lightbox-container-height", h + "px");
      s.setProperty("--wp--lightbox-image-width", w + "px");
      s.setProperty("--wp--lightbox-image-height", h + "px");
      s.setProperty("--wp--lightbox-scale", String(scale));
      s.setProperty("--wp--lightbox-initial-left-position", left + "px");
      s.setProperty("--wp--lightbox-initial-top-position", top + "px");
      s.setProperty("--wp--lightbox-initial-clip", "inset(" + dy + "px " + dx + "px " + dy + "px " + dx + "px)");
      s.setProperty("--wp--lightbox-scrollbar-width", (window.innerWidth - document.documentElement.clientWidth) + "px");
      big.src = img.currentSrc || img.src;
      big.alt = img.alt;
      overlay.classList.remove("show-closing-animation");
      overlay.classList.add("active");
      document.documentElement.classList.add("has-lightbox-open");
      overlay.focus();
    }
    function close() {
      if (!overlay.classList.contains("active")) return;
      overlay.classList.remove("active");
      overlay.classList.add("show-closing-animation");
      document.documentElement.classList.remove("has-lightbox-open");
      if (lastTrigger) lastTrigger.focus({ preventScroll: true });
    }
    figures.forEach(function (fig) {
      var img = fig.querySelector("img");
      var btn = fig.querySelector(".lightbox-trigger");
      var go = function () { openFrom(img, btn); };
      img.addEventListener("click", go);
      if (btn) btn.addEventListener("click", go);
    });
    overlay.addEventListener("click", close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
    window.addEventListener("scroll", close, { passive: true });
  }

  /* Gentle entrance animation as blocks scroll into view. */
  function reveal() {
    var items = document.querySelectorAll(".wp-reveal");
    if (!items.length) return;
    if (reduceMotion || !("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("is-revealed"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-revealed"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* Forms, following Gravity Forms behavior and wording. */
  var MSG = {
    required: "This field is required.",
    email: "The email address entered is invalid, please check the formatting (e.g. email@domain.com).",
    phone: "Phone format: (###) ###-####",
    zip: "Please enter a valid 5-digit ZIP code."
  };
  function setError(el, message) {
    var wrap = el.closest(".gfield");
    if (!wrap) return;
    wrap.classList.toggle("has-error", Boolean(message));
    var out = wrap.querySelector(".validation_message");
    if (out) out.textContent = message || "";
    if (el.matches("input, select, textarea")) el.setAttribute("aria-invalid", message ? "true" : "false");
  }
  function validateInput(el) {
    var v = el.value.trim();
    if (el.required && !v) { setError(el, MSG.required); return false; }
    if (v && el.name === "zip" && !/^\d{5}$/.test(v)) { setError(el, MSG.zip); return false; }
    if (v && el.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) { setError(el, MSG.email); return false; }
    if (v && el.type === "tel" && v.replace(/\D/g, "").length !== 10) { setError(el, MSG.phone); return false; }
    setError(el, "");
    return true;
  }
  function validateGroup(wrap) {
    var ok = Boolean(wrap.querySelector("input:checked"));
    wrap.classList.toggle("has-error", !ok);
    var out = wrap.querySelector(".validation_message");
    if (out) out.textContent = ok ? "" : MSG.required;
    return ok;
  }
  function validateScope(scope) {
    var ok = true;
    scope.querySelectorAll(".gfield input:not([type=checkbox]):not([type=radio]), .gfield select, .gfield textarea").forEach(function (el) {
      if (!validateInput(el)) ok = false;
    });
    scope.querySelectorAll("[data-group-required]").forEach(function (g) { if (!validateGroup(g)) ok = false; });
    return ok;
  }
  function formatPhone(input) {
    input.addEventListener("input", function () {
      var d = input.value.replace(/\D/g, "").slice(0, 10);
      input.value = d.length > 6 ? "(" + d.slice(0, 3) + ") " + d.slice(3, 6) + "-" + d.slice(6)
        : d.length > 3 ? "(" + d.slice(0, 3) + ") " + d.slice(3)
        : d.length ? "(" + d : "";
    });
  }

  function gforms() {
    document.querySelectorAll(".gform_wrapper form").forEach(function (form) {
      var wrapper = form.closest(".gform_wrapper");
      var banner = wrapper.querySelector(".gform_validation_errors");
      var pages = Array.prototype.slice.call(form.querySelectorAll(".gform_page"));
      var current = 0;

      function fail(scope) {
        if (banner) banner.hidden = false;
        var bad = scope.querySelector(".has-error input, .has-error select, .has-error textarea");
        (banner || form).scrollIntoView({ block: "center", behavior: reduceMotion ? "auto" : "smooth" });
        if (bad) setTimeout(function () { bad.focus({ preventScroll: true }); }, 300);
      }
      function showPage(i, moveFocus) {
        current = i;
        pages.forEach(function (p, idx) { p.hidden = idx !== i; });
        var pct = Math.round((i + 1) / pages.length * 100);
        var bar = wrapper.querySelector(".gf_progressbar_percentage");
        if (bar) { bar.style.width = pct + "%"; bar.querySelector("span").textContent = pct + "%"; }
        var title = wrapper.querySelector(".gf_progressbar_title");
        if (title) title.textContent = "Step " + (i + 1) + " of " + pages.length + " - " + pages[i].getAttribute("data-title");
        // Gravity Forms "Steps" indicator
        wrapper.querySelectorAll(".gf_step").forEach(function (step, idx) {
          step.classList.toggle("gf_step_active", idx === i);
          step.classList.toggle("gf_step_completed", idx < i);
        });
        var say = wrapper.querySelector("[data-step-announce]");
        if (say && moveFocus) say.textContent = "Step " + (i + 1) + " of " + pages.length + ": " + pages[i].getAttribute("data-title");
        if (moveFocus) {
          // Keep the form in view without jumping the page, then put the cursor in the first field.
          if (wrapper.getBoundingClientRect().top < 0) wrapper.scrollIntoView({ block: "start" });
          var first = pages[i].querySelector("input:not([type=radio]):not([type=checkbox]), textarea, input:checked, input");
          if (first) first.focus({ preventScroll: true });
        }
      }
      function goNext() {
        if (validateScope(pages[current])) { if (banner) banner.hidden = true; showPage(current + 1, true); }
        else fail(pages[current]);
      }

      if (pages.length) {
        var params = new URLSearchParams(window.location.search);
        (params.get("service") || "").split(",").forEach(function (v) {
          var box = form.querySelector('[name="service"][value="' + v + '"]');
          if (box) box.checked = true;
        });
        if (params.get("zip")) form.querySelector('[name="zip"]').value = params.get("zip").replace(/\D/g, "").slice(0, 5);
        form.addEventListener("click", function (e) {
          var next = e.target.closest(".gform_next_button");
          var prev = e.target.closest(".gform_previous_button");
          if (next) goNext();
          if (prev) { if (banner) banner.hidden = true; showPage(current - 1, true); }
        });
        // One-tap step: picking a card with a mouse or finger moves on (keyboard users press Next).
        var advanceTimer;
        if (form.hasAttribute("data-autoadvance")) {
          form.addEventListener("click", function (e) {
            var card = e.target.closest(".gcard");
            if (!card || e.detail === 0 || current === pages.length - 1) return;
            var input = card.querySelector('input[type="radio"]');
            if (!input || !pages[current].contains(input)) return;
            var from = current;
            clearTimeout(advanceTimer);
            advanceTimer = setTimeout(function () { if (input.checked && current === from) goNext(); }, 260);
          });
        }
        showPage(0);
      }

      form.addEventListener("change", function (e) {
        var g = e.target.closest("[data-group-required]");
        if (g && g.classList.contains("has-error")) validateGroup(g);
      });
      form.querySelectorAll("input, select, textarea").forEach(function (el) {
        el.addEventListener("blur", function () { if (el.closest(".has-error") || el.value.trim()) validateInput(el); });
      });

      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var scope = pages.length ? pages[current] : form;
        if (!validateScope(scope)) { fail(scope); return; }
        // Prototype: nothing is sent. To go live, post new FormData(form) to the form service here.
        var first = (form.querySelector('[name="name"]') || {}).value || "";
        var done = wrapper.querySelector(".gform_confirmation_wrapper");
        done.querySelectorAll("[data-echo]").forEach(function (el) {
          var field = form.querySelector('[name="' + el.getAttribute("data-echo") + '"]');
          el.textContent = field ? field.value.trim() : "";
        });
        var nameSlot = done.querySelector("[data-first-name]");
        if (nameSlot) nameSlot.textContent = first.trim().split(" ")[0] ? ", " + first.trim().split(" ")[0] : "";
        form.hidden = true;
        if (banner) banner.hidden = true;
        wrapper.querySelectorAll(".gf_progressbar_wrapper, .gf_page_steps").forEach(function (el) { el.hidden = true; });
        done.hidden = false;
        splat(wrapper.closest(".quote-box"));
        done.scrollIntoView({ block: "center", behavior: reduceMotion ? "auto" : "smooth" });
      });
    });
  }

  /* Services mega menu: opens on hover (desktop) or with the arrow button. */
  function megaMenu() {
    var hoverable = window.matchMedia("(hover: hover) and (min-width: 1000px)");
    document.querySelectorAll(".has-mega-menu").forEach(function (item) {
      var btn = item.querySelector(".wp-block-navigation-submenu__toggle");
      var timer;
      function open() { clearTimeout(timer); item.classList.add("is-open"); btn.setAttribute("aria-expanded", "true"); }
      function close() { clearTimeout(timer); item.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); }
      item.addEventListener("mouseenter", function () { if (hoverable.matches) open(); });
      item.addEventListener("mouseleave", function () { if (hoverable.matches) timer = setTimeout(close, 180); });
      btn.addEventListener("click", function () { item.classList.contains("is-open") ? close() : open(); });
      item.addEventListener("focusout", function (e) { if (!item.contains(e.relatedTarget)) close(); });
      document.addEventListener("click", function (e) { if (!item.contains(e.target)) close(); });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && item.classList.contains("is-open")) { close(); btn.focus(); }
      });
    });
  }

  /* Hero quote box easter eggs: roll the roller for a new paint color; paint splats on submit. */
  var PAINTS = [["Harbor Blue", "#4068ee", "#2b2f9a"], ["Chesapeake Teal", "#159a9c", "#0b4f6c"], ["Lagoon", "#1fa6d0", "#2457b3"],
    ["Twilight Violet", "#7a66e0", "#2b2a7a"], ["Bayside Sage", "#4f9a7c", "#24524a"], ["Midnight Navy", "#34477f", "#0d1630"]];
  function paintRoller() {
    var box = document.querySelector(".quote-box");
    var btn = box && box.querySelector(".quote-box__roller");
    if (!btn) return;
    var tag = box.querySelector(".quote-box__swatch"), i = 0, timer;
    btn.addEventListener("click", function () {
      i = (i + 1) % PAINTS.length;
      box.style.setProperty("--qb-a", PAINTS[i][1]);
      box.style.setProperty("--qb-b", PAINTS[i][2]);
      btn.classList.remove("is-rolling"); void btn.offsetWidth; btn.classList.add("is-rolling");
      tag.textContent = PAINTS[i][0];
      tag.classList.add("is-shown");
      clearTimeout(timer);
      timer = setTimeout(function () { tag.classList.remove("is-shown"); }, 1400);
    });
  }
  function splat(box) {
    if (!box || reduceMotion) return;
    var style = getComputedStyle(box);
    var colors = [style.getPropertyValue("--qb-a").trim(), style.getPropertyValue("--qb-b").trim(), "#a9bcff", "#2fc4c4", "#8b7cf6"];
    var blob = "M13 2c3 0 4 3 6 4s5 0 6 3-2 4-2 6 3 4 1 6-5 0-7 1-3 4-6 3-3-3-5-4-6 0-6-3 2-4 1-6-3-4-1-6 5-1 6-2 3-4 5-4z";
    for (var n = 0; n < 14; n++) {
      var el = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      el.setAttribute("viewBox", "0 0 26 26");
      el.setAttribute("class", "qb-splat");
      el.setAttribute("aria-hidden", "true");
      el.innerHTML = '<path d="' + blob + '" fill="' + colors[n % colors.length] + '"/>';
      var a = Math.random() * Math.PI * 2, d = 90 + Math.random() * 120, sz = 12 + Math.random() * 18;
      el.style.left = "calc(50% - 13px)"; el.style.top = "40%";
      el.style.width = sz + "px"; el.style.height = sz + "px";
      el.style.setProperty("--dx", Math.cos(a) * d + "px");
      el.style.setProperty("--dy", Math.sin(a) * d + "px");
      el.style.setProperty("--rot", (Math.random() * 360 - 180) + "deg");
      box.appendChild(el);
      setTimeout(function (x) { return function () { x.remove(); }; }(el), 1200);
    }
  }

  /* Paint tips: highlight the topic in view and keep its pill visible in the scrolling bar. */
  function tipsNav() {
    var bar = document.querySelector(".tips-nav__inner");
    if (!bar || !("IntersectionObserver" in window)) return;
    var links = {};
    bar.querySelectorAll('a[href^="#"]').forEach(function (a) { links[a.getAttribute("href").slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        Object.keys(links).forEach(function (id) { links[id].removeAttribute("aria-current"); });
        var a = links[e.target.id];
        if (!a) return;
        a.setAttribute("aria-current", "true");
        bar.scrollTo({ left: a.offsetLeft - 20, behavior: reduceMotion ? "auto" : "smooth" });
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    Object.keys(links).forEach(function (id) { var sec = document.getElementById(id); if (sec) io.observe(sec); });
  }

  /* Mobile action bar appears once the main call-to-action has scrolled out of view. */
  function mobileActions() {
    var bar = document.querySelector(".mobile-actions");
    if (!bar) return;
    var anchor = document.querySelector("[data-hero-cta]");
    if (anchor && "IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        bar.classList.toggle("is-visible", !entries[0].isIntersecting && entries[0].boundingClientRect.top < 0);
      }).observe(anchor);
    } else {
      var onScroll = function () { bar.classList.toggle("is-visible", window.scrollY > 240); };
      onScroll();
      window.addEventListener("scroll", onScroll, { passive: true });
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    applyHours();
    setInterval(applyHours, 60000);
    stickyHeader();
    overlayMenu();
    megaMenu();
    mobileActions();
    tipsNav();
    paintRoller();
    lightbox();
    reveal();
    document.querySelectorAll('input[type="tel"]').forEach(formatPhone);
    gforms();
    document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
  });
})();
