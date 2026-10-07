#!/usr/bin/env python3
"""James Skipper Painting pitch prototype. Page generator (WordPress core block markup).

Built from the pitch-prototypes starter. Every fact comes from the client's Facebook page (see facts.md).
Anything we could not confirm is shown inside a visible placeholder marker so the client can edit or remove it.
Run:  python3 tools/build_site.py <site-dir>
"""
import hashlib, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from urllib.parse import quote_plus

# ---- CONFIG ----
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
BASE_URL = "https://jamesskipper.whitephoenixconsulting.com/"
NAME = "James Skipper Painting"
PHONE = "(757) 403-4451"
TEL = "+17574034451"
EMAIL = "james.skipper67@gmail.com"
FACEBOOK = "https://www.facebook.com/people/James-Skipper-Painting/100089586026542/"
FB_REVIEWS = "https://www.facebook.com/profile.php?id=100089586026542&sk=reviews"
STREET = "1122 Willow Ave"
CITY = "Chesapeake, VA 23325"
BBB = "https://www.bbb.org/us/va/chesapeake/profile/painting-contractors/james-skipper-painting-0583-90042634"
MAPS = "https://www.google.com/maps/search/?api=1&query=" + quote_plus("1122 Willow Ave, Chesapeake, VA 23325")
DIM = "#0d1630"

BUILD = time.strftime("%Y%m%d%H%M%S")
# If a browser shows a cached page from an older build, it reloads once to get the current one.
SELF_HEAL = ('<script>(function(){if(!window.fetch)return;fetch("ROOTversion.json",{cache:"no-store"})'
             '.then(function(r){return r.json()}).then(function(v){if(v.build&&v.build!=="BUILD"){var k="reload-"+v.build;'
             'try{if(sessionStorage.getItem(k))return;sessionStorage.setItem(k,"1")}catch(e){}location.reload()}}).catch(function(){})})();</script>')


def ver(rel):
    """Cache-busting version, like WordPress's ?ver= on enqueued assets."""
    with open(os.path.join(OUT, rel), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


# Written by tools/images.js: {name: [widths, full width, full height]}
with open(os.path.join(OUT, "assets", "img", "manifest.json")) as fh:
    IMGS = {k: (v[0], v[1], v[2]) for k, v in json.load(fh).items()}

SVG = {
    "phone": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "arrow": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>',
    "pin": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>',
    "roller": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect width="16" height="6" x="2" y="2" rx="2"/><path d="M10 16v-2a2 2 0 0 1 2-2h8a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect width="4" height="6" x="8" y="16" rx="1"/></svg>',
    "shield": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>',
    "mail": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>',
    # WordPress core navigation icons
    "menu": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M5 5v1.5h14V5H5zm0 7.8h14v-1.5H5v1.5zM5 19h14v-1.5H5V19z"/></svg>',
    "close": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="m13.06 12 6.47-6.47-1.06-1.06L12 10.94 5.53 4.47 4.47 5.53 10.94 12l-6.47 6.47 1.06 1.06L12 13.06l6.47 6.47 1.06-1.06L13.06 12Z"/></svg>',
    # WordPress core image block "expand on click" icon
    "expand": '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="none" viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path fill="#fff" d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z"/></svg>',
}
CUR = ' aria-current="page"'


# ---- placeholders: sample content the client confirms, edits or removes ----
PH_TITLE = "Placeholder: sample content. James Skipper Painting can confirm, edit or remove it."


def chip(label="Placeholder", cls=""):
    c = "ph-chip" + (" " + cls if cls else "")
    return f'<span class="{c}" title="{PH_TITLE}">{label}</span>'


def ph(text):
    """Inline placeholder text."""
    return f'<span class="ph" title="{PH_TITLE}">{text}</span>'


def corner(label="Placeholder"):
    return chip(label, "ph-corner")


def srcset(root, name):
    widths, w, h = IMGS[name]
    return ", ".join(f"{root}assets/img/{name}-{x}.webp {x}w" for x in widths)


def img(root, name, alt, sizes, cls="", eager=False, extra=""):
    widths, w, h = IMGS[name]
    default = widths[1] if len(widths) > 1 else widths[0]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{root}assets/img/{name}-{default}.webp" srcset="{srcset(root, name)}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{alt}" {load} decoding="async"{extra}>')


def lightbox_figure(root, name, alt, sizes, cls="wp-block-image size-large"):
    return (f'<figure class="{cls} wp-lightbox-container">{img(root, name, alt, sizes)}'
            f'<button class="lightbox-trigger" type="button" aria-haspopup="dialog" aria-label="Enlarge: {alt}">{SVG["expand"]}</button></figure>')


def button(href, label, style="", icon=None, attrs=""):
    cls = "wp-block-button" + (f" is-style-{style}" if style else "")
    ic = SVG[icon] if icon else ""
    lead = ic if icon == "phone" else ""
    trail = ic if icon == "arrow" else ""
    return f'<div class="{cls}"><a class="wp-block-button__link wp-element-button" href="{href}"{attrs}>{lead}{label}{trail}</a></div>'


def buttons(*items, center=False):
    j = " is-content-justification-center" if center else ""
    return f'<div class="wp-block-buttons is-layout-flex{j}">{"".join(items)}</div>'


def quote_link(root, service=None):
    return f"{root}quote/" + (f"?service={service}" if service else "")


def reveal(i=0):
    return f' style="--reveal-delay:{i * 0.08:.2f}s"' if i else ""


NAV = [("Home", ""), ("Services", "services/"), ("About", "about-us/"), ("Paint tips", "paint-tips/"),
       ("Reviews", "reviews/"), ("Contact", "contact-us/")]
SPECULATION = {"prerender": [{"source": "document", "where": {"and": [{"href_matches": "/*"},
               {"not": {"href_matches": "/*\\?*"}}, {"not": {"selector_matches": "a[rel~=nofollow]"}}]}, "eagerness": "moderate"}]}


def head(root, title, desc, path, extra=""):
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<!-- Prototype preview. Remove this noindex line at launch. -->
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{DIM}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE_URL}{path}">
<meta property="og:image" content="{BASE_URL}assets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{root}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@300..800&amp;display=swap">
<link rel="stylesheet" id="wp-block-library-css" href="{root}assets/css/wp-blocks.css?ver=11.2.0">
<link rel="stylesheet" id="theme-style-css" href="{root}assets/css/site.css?ver={ver('assets/css/site.css')}">
<meta name="site-build" content="{BUILD}">
<script>document.documentElement.classList.add("js");</script>
{SELF_HEAL.replace("ROOT", root).replace("BUILD", BUILD)}
<script type="speculationrules">{json.dumps(SPECULATION)}</script>
{extra}<script src="{root}assets/js/site.js?ver={ver('assets/js/site.js')}" defer></script>
</head>"""


def href(root, h):
    return (root + h) or "./"


CHEVRON = '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true" focusable="false"><path d="M1.50002 4L6.00002 8L10.5 4" stroke-width="1.5"></path></svg>'

# ---------- services ----------

SERVICES = [
    {"id": "interior-painting", "name": "Interior painting", "kind": "Inside", "img": "interior", "ph": False,
     "alt": "Painter rolling white paint onto an interior wall",
     "card": "Walls, ceilings and trim, with a color and finish that suit the room."},
    {"id": "exterior-painting", "name": "Exterior painting", "kind": "Outside", "img": "exterior", "ph": False,
     "alt": "Red two-story house with white trim on a residential street",
     "card": "Siding and trim repainted, so you can stay off the ladder."},
    {"id": "commercial-painting", "name": "Commercial painting", "kind": "Businesses", "img": "commercial", "ph": True,
     "alt": "Painter spraying walls in a room covered with plastic sheeting",
     "card": "Offices, shops and rental units, inside and out."},
    {"id": "color-advice", "name": "Help with colors", "kind": "Advice", "img": "color", "ph": True,
     "alt": "Hand holding open a fan deck of paint colors",
     "card": "Colors that work with your roof, your lighting and the size of the room."},
]
EXTRAS = ["Cabinet painting", "Deck and fence staining", "Drywall patching", "Pressure washing"]


def mega_menu(root):
    cards = "".join(
        f'<a class="mega-card" href="{root}services/#{s["id"]}">'
        f'<span class="mega-card__media"><img src="{root}assets/img/{s["img"]}-640.webp" width="640" height="427" alt="" loading="lazy" decoding="async">'
        f'{chip() if s["ph"] else ""}</span>'
        f'<span class="mega-card__title">{s["name"]}</span><span class="mega-card__text">{s["card"]}</span></a>'
        for s in SERVICES)
    return (f'<div class="mega-menu" id="mega-services"><div class="mega-menu__inner">'
            f'<div class="mega-menu__grid">{cards}</div>'
            f'<div class="mega-menu__foot"><span><strong>Also ask about:</strong> {ph(", ".join(EXTRAS).lower().capitalize())} {chip()}</span>'
            f'<a class="more-link" href="{root}services/">All services {SVG["arrow"]}</a></div></div></div>')


def preview_bar():
    return (f'<div class="preview-bar" role="note">Website preview for {NAME}. Anything marked {chip()} is sample content to confirm, edit or remove. '
            f'<span class="preview-bar__more">Photos are stock samples until we add yours.</span></div>')


def header(root, active):
    home = root or "./"
    items = []
    for l, h in NAV:
        cur = CUR if active == h else ""
        link = f'<a class="wp-block-navigation-item__content" href="{href(root, h)}"{cur}>{l}</a>'
        if h == "services/":
            items.append(f'<li class="wp-block-navigation-item has-child open-on-hover-click wp-block-navigation-submenu has-mega-menu">{link}'
                         f'<button class="wp-block-navigation__submenu-icon wp-block-navigation-submenu__toggle" type="button" aria-expanded="false" aria-controls="mega-services" aria-label="Services submenu">{CHEVRON}</button>'
                         f'{mega_menu(root)}</li>')
        else:
            items.append(f'<li class="wp-block-navigation-item">{link}</li>')
    links = "".join(items)
    sub = "".join(f'<li><a href="{root}services/#{s["id"]}">{s["name"]}</a></li>' for s in SERVICES)
    overlay = []
    for l, h in NAV:
        cur = CUR if active == h else ""
        extra = f'<ul class="overlay-sub">{sub}</ul>' if h == "services/" else ""
        overlay.append(f'<li><a href="{href(root, h)}"{cur}>{l}</a>{extra}</li>')
    overlay_links = "".join(overlay)
    return f"""<a class="skip-link screen-reader-text" href="#wp--skip-link--target">Skip to content</a>
{preview_bar()}
<header class="wp-block-template-part site-header has-global-padding">
  <div class="site-header__inner">
    <div class="wp-block-site-logo"><a href="{home}" rel="home" aria-label="{NAME}, home"><img src="{root}assets/img/logo.svg" width="182" height="78" alt="{NAME}"></a></div>
    <nav class="wp-block-navigation" aria-label="Main"><ul class="wp-block-navigation__container">{links}</ul></nav>
    <div class="header-tools">
      <a class="header-phone" href="tel:{TEL}">{SVG["phone"].replace("<svg ", '<svg width="18" height="18" ')}{PHONE}</a>
      <a class="icon-button header-call" href="tel:{TEL}" aria-label="Call {PHONE}">{SVG["phone"]}</a>
      <div class="wp-block-button header-quote"><a class="wp-block-button__link wp-element-button" href="{root}quote/">Get a quote</a></div>
      <button class="wp-block-navigation__responsive-container-open icon-button" type="button" aria-haspopup="dialog" aria-expanded="false" aria-label="Open menu">{SVG["menu"]}</button>
    </div>
  </div>
  <div class="wp-block-navigation__responsive-container" role="dialog" aria-modal="true" aria-label="Menu">
    <button class="wp-block-navigation__responsive-container-close icon-button" type="button" aria-label="Close menu">{SVG["close"]}</button>
    <ul>{overlay_links}</ul>
    {buttons(button(root + "quote/", "Get a quote"), button("tel:" + TEL, "Call " + PHONE, "outline"))}
  </div>
</header>"""


def footer(root):
    home = root or "./"
    svc = "".join(f'<li><a href="{root}services/#{s["id"]}">{s["name"]}</a>{" " + chip() if s["ph"] else ""}</li>' for s in SERVICES)
    return f"""<footer class="wp-block-template-part site-footer has-global-padding">
  <div class="site-footer__inner">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="footer-logo" href="{home}"><img src="{root}assets/img/logo.svg" width="182" height="78" alt="{NAME}" loading="lazy"></a>
        <p>Family-owned house painting in Chesapeake, Virginia, since 1994.</p>
      </div>
      <div>
        <h2>Services</h2>
        <ul>{svc}</ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="{root}about-us/">About us</a></li>
          <li><a href="{root}paint-tips/">Paint tips</a></li>
          <li><a href="{root}reviews/">Reviews</a></li>
          <li><a href="{root}contact-us/">Contact</a></li>
          <li><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a></li>
          <li><a href="{BBB}" target="_blank" rel="noopener">BBB profile</a></li>
        </ul>
      </div>
      <div>
        <h2>Get in touch</h2>
        <ul>
          <li><a href="tel:{TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{STREET}<br>{CITY}</li>
          <li>{ph("Virginia contractor license #000000")}</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom"><p>&copy; <span data-year>2026</span> {NAME}</p><p>Chesapeake, Virginia</p></div>
  </div>
</footer>"""


def mobile_actions(root):
    return f"""<div class="mobile-actions" role="region" aria-label="Quick actions">
  {button("tel:" + TEL, "Call", "outline", "phone")}
  {button(root + "quote/", "Get a quote", "", "arrow")}
</div>"""


def page(depth, path, title, desc, active, main, extra_head="", actions=True, body_class="page"):
    root = "../" * depth
    html = f"""{head(root, title, desc, path, extra_head)}
<body class="{body_class}{" has-mobile-actions" if actions else ""}">
<div class="wp-site-blocks">
{header(root, active)}
<main class="wp-block-group" id="wp--skip-link--target">
{main(root)}
</main>
{footer(root)}
</div>
{mobile_actions(root) if actions else ""}
</body>
</html>
"""
    target = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w") as f:
        f.write(html)
    print("wrote", os.path.relpath(target, OUT))


# ---------- shared sections ----------

def service_cards(root, link_to_anchor=True):
    cards = []
    for i, s in enumerate(SERVICES):
        h = f"{root}services/#{s['id']}" if link_to_anchor else f"#{s['id']}"
        tag = chip() if s["ph"] else ""
        cards.append(f"""<div class="wp-block-group service-card wp-reveal"{reveal(i)}>
  <a href="{h}">
    <figure class="wp-block-image size-large">{img(root, s["img"], s["alt"], "(min-width: 782px) 25vw, 50vw")}{tag}</figure>
    <h3 class="wp-block-heading">{s["name"]}</h3>
    <p>{s["card"]}</p>
    <span class="more-link">Learn more {SVG["arrow"]}</span>
  </a>
</div>""")
    return f'<div class="wp-block-group is-layout-grid columns-4">{"".join(cards)}</div>'


def testimonial(root, show_link=True):
    link = f'<a href="{root}reviews/">Reviews</a>' if show_link else ""
    return f"""<section class="wp-block-group alignfull section has-global-padding">
  <div class="wp-block-columns alignwide wide is-layout-flex">
    <div class="wp-block-column testimonial-col wp-reveal">
      <h2 class="wp-block-heading is-style-text-annotation">What customers say</h2>
      <div class="is-placeholder">
        {corner("Placeholder review")}
        <blockquote class="wp-block-quote is-style-plain testimonial-quote">
          <p>&ldquo;A customer's review goes here, word for word. Facebook doesn't show any reviews yet, so this space is waiting for the first one.&rdquo;</p>
          <cite><strong>Customer name</strong>, neighborhood</cite>
        </blockquote>
      </div>
      <p class="rating-line">Had us paint for you? <a href="{FB_REVIEWS}" target="_blank" rel="noopener">Leave a review on Facebook</a> {link}</p>
    </div>
    <div class="wp-block-column wp-reveal"{reveal(1)}>
      {lightbox_figure(root, "trim", "Painter working on the roof trim of a green house", "(min-width: 782px) 50vw, 100vw", "wp-block-image size-large testimonial-media")}
    </div>
  </div>
</section>"""


def tip_band(root):
    widths, w, h = IMGS["cover"]
    return f"""<div class="wp-block-cover alignfull has-parallax band-cover" style="min-height:400px">
  <div role="img" aria-label="A living room with cream walls and a white brick fireplace" class="wp-block-cover__image-background has-parallax" style="background-position:50% 50%;background-image:url({root}assets/img/cover-{widths[-1]}.webp)"></div>
  <span aria-hidden="true" class="wp-block-cover__background has-background-dim-80 has-background-dim" style="background-color:{DIM}"></span>
  <div class="wp-block-cover__inner-container has-text-align-center wp-reveal">
    <span class="band-kicker">Paint tip</span>
    <h2 class="wp-block-heading">Check the color under your own lights</h2>
    <p>Cool, fluorescent light pulls out the greens and blues in a color. Warm bulbs bring out the reds. Look at a sample in the room before you commit.</p>
    {buttons(button(root + "paint-tips/", "More paint tips", "light", "arrow"), center=True)}
  </div>
</div>"""


def cta(root, title="Tell us what needs painting", text="Send the form or give us a call. We'll get back to you."):
    return f"""<section class="wp-block-group alignfull section has-accent-5-background-color has-global-padding">
  <div class="wp-block-group has-text-align-center wp-reveal" style="max-width:680px;margin:0 auto">
    <h2 class="wp-block-heading has-text-align-center" style="font-size:var(--wp--preset--font-size--xx-large)">{title}</h2>
    <p class="has-text-align-center" style="margin-top:14px;color:var(--wp--preset--color--accent-4)">{text}</p>
    <div style="margin-top:28px">{buttons(button(root + "quote/", "Get a quote", "", "arrow"), button("tel:" + TEL, "Call " + PHONE, "outline"), center=True)}</div>
  </div>
</section>"""


def banner(root, crumb, title, lede):
    return f"""<section class="wp-block-group alignfull page-banner has-global-padding">
  <div class="page-banner__inner">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{root}">Home</a> / {crumb}</nav>
    <h1 class="wp-block-heading">{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>"""


def gfield(label, inner, required=False, half=False, stack=True, desc="", group=False, cls=""):
    req = '<span class="gfield_required" aria-hidden="true">*</span>' if required else ""
    width = " gfield--width-half" + (" stack-sm" if stack else "") if half else ""
    grp = " data-group-required" if group and required else ""
    d = f'<div class="gfield_description">{desc}</div>' if desc else ""
    tag_label = f'<legend class="gfield_label">{label}{req}</legend>' if group else ""
    if group:
        return f'<fieldset class="gfield{width} {cls}"{grp} style="border:0;margin:0;padding:0;min-width:0">{tag_label}{d}<div class="ginput_container">{inner}</div><div class="validation_message" aria-live="polite"></div></fieldset>'
    return f'<div class="gfield{width} {cls}">{label.format(req=req)}{d}<div class="ginput_container">{inner}</div><div class="validation_message" aria-live="polite"></div></div>'


def lab(for_id, text):
    return f'<label class="gfield_label" for="{for_id}">{text}{{req}}</label>'


ICON = {
    "interior-painting": '<rect width="16" height="6" x="2" y="2" rx="2"/><path d="M10 16v-2a2 2 0 0 1 2-2h8a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect width="4" height="6" x="8" y="16" rx="1"/>',
    "exterior-painting": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "inside-and-out": '<path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M8 13h8"/><path d="M12 9v8"/>',
    "commercial-painting": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>',
    "color-advice": '<circle cx="13.5" cy="6.5" r="1" fill="currentColor"/><circle cx="17.5" cy="10.5" r="1" fill="currentColor"/><circle cx="8.5" cy="7.5" r="1" fill="currentColor"/><circle cx="6.5" cy="12.5" r="1" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/>',
    "something-else": '<circle cx="12" cy="12" r="10"/><path d="M8 12h8"/><path d="M12 8v8"/>',
    "not-sure": '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
}
# Hero box: only what the Facebook page supports. The quote page lists the placeholder services too.
HERO_OPTIONS = [("interior-painting", "Interior", "Walls, ceilings, trim"), ("exterior-painting", "Exterior", "Siding, trim, windows"),
                ("inside-and-out", "Inside and out", "The whole house"), ("not-sure", "Not sure yet", "Tell us what you see")]
QUOTE_OPTIONS = [("interior-painting", "Interior painting", "Walls, ceilings and trim", False),
                 ("exterior-painting", "Exterior painting", "Siding, trim and window frames", False),
                 ("commercial-painting", "Commercial painting", "Offices, shops, rental units", True),
                 ("color-advice", "Help with colors", "Picking colors and finishes", True),
                 ("something-else", "Something else", "Tell us what you need", False),
                 ("not-sure", "Not sure yet", "Tell us what you're seeing", False)]
TICK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M20 6 9 17l-5-5"/></svg>'


def choice_card(input_type, v, l, desc="", is_ph=False):
    icon = f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICON[v]}</svg>'
    d = f'<span class="gcard__desc">{desc}{" " + chip() if is_ph else ""}</span>' if desc else ""
    return (f'<li><label class="gcard"><input type="{input_type}" name="service" value="{v}">'
            f'<span class="gcard__box"><span class="gcard__icon">{icon}</span><span class="gcard__text">{l}{d}</span>'
            f'<span class="gcard__tick">{TICK}</span></span></label></li>')


def hero_cards():
    return f'<ul class="gchoice-cards gchoice-cards--hero">{"".join(choice_card("radio", v, l, d) for v, l, d in HERO_OPTIONS)}</ul>'


def steps(labels):
    """Gravity Forms "Steps" progress indicator."""
    items = "".join(f'<div class="gf_step{" gf_step_active" if i == 0 else ""}" role="listitem"><span class="gf_step_number">{i + 1}</span>'
                    f'<span class="gf_step_label">{l}</span></div>' for i, l in enumerate(labels))
    return (f'<div class="gf_page_steps" role="list" aria-label="Form steps">{items}</div>'
            f'<p class="screen-reader-text" aria-live="polite" data-step-announce></p>')


CONFIRM_ICON = '<span class="gform_confirmation_icon" aria-hidden="true"><svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg></span>'
BACK = '<button class="wp-element-button gform_previous_button" type="button">Back</button>'


def quote_cards():
    return f'<ul class="gchoice-cards gchoice-cards--lg">{"".join(choice_card("checkbox", v, l, d, p) for v, l, d, p in QUOTE_OPTIONS)}</ul>'


HOURS = [("Monday", "8am to 5pm"), ("Tuesday", "8am to 5pm"), ("Wednesday", "8am to 5pm"), ("Thursday", "8am to 5pm"),
         ("Friday", "8am to 5pm"), ("Saturday", "Closed"), ("Sunday", "Closed")]


def hours_table():
    rows = "".join(f'<tr data-day="{d}"><td>{d}</td><td>{h}</td></tr>' for d, h in HOURS)
    return f'<table class="hours-table"><caption class="screen-reader-text">Business hours (sample)</caption>{rows}</table>'


def hours_card(extra_cls=""):
    return f"""<div class="hours-card is-placeholder{extra_cls}">
        {corner("Sample hours")}
        <h3 class="wp-block-heading">Business hours</h3>
        {hours_table()}
        <p class="hours-card__note">Facebook doesn't list hours yet. These are sample hours for James to change. You can send the quote form any time.</p>
      </div>"""


def home_contact(root):
    return f"""<section class="wp-block-group alignfull section has-accent-5-background-color has-global-padding" aria-labelledby="visit-title">
  <div class="wp-block-columns alignwide wide is-layout-flex home-hours">
    <div class="wp-block-column wp-reveal">
      <h2 class="wp-block-heading" id="visit-title" style="font-size:var(--wp--preset--font-size--xx-large)">Tell us what needs painting</h2>
      <p class="home-hours__lede">Send the form or give us a call. We'll get back to you.</p>
      {buttons(button(root + "quote/", "Get a quote", "", "arrow"), button("tel:" + TEL, "Call " + PHONE, "outline", "phone"))}
      <ul class="home-hours__details">
        <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><span>Based at</span>{STREET}, {CITY}</li>
        <li><span>Areas</span>Chesapeake and {ph("nearby Hampton Roads cities")} {chip()}</li>
      </ul>
    </div>
    <div class="wp-block-column wp-reveal" style="--reveal-delay:.08s">
      {hours_card()}
    </div>
  </div>
</section>"""


TRUST = [
    ('<circle cx="28" cy="28" r="28" fill="#eaf0fe"/><rect x="11" y="15" width="34" height="29" rx="4" fill="#0d1630"/><path d="M15 15h26a4 4 0 0 1 4 4v5H11v-5a4 4 0 0 1 4-4z" fill="#476ef0"/><rect x="18" y="10.5" width="3.2" height="8.5" rx="1.6" fill="#0d1630"/><rect x="34.8" y="10.5" width="3.2" height="8.5" rx="1.6" fill="#0d1630"/><text x="28" y="38.6" text-anchor="middle" font-family="Manrope, sans-serif" font-size="11.5" font-weight="800" fill="#fff">1994</text><polygon class="trust-art__spark" points="47.00,6.40 48.12,9.46 51.37,9.58 48.81,11.59 49.70,14.72 47.00,12.90 44.30,14.72 45.19,11.59 42.63,9.58 45.88,9.46" fill="#476ef0"/>',
     "Family owned since 1994", "Prep comes first", False),
    ('<circle cx="28" cy="28" r="28" fill="#eaf0fe"/><path d="M21 33.5 16.5 47l6-2.6 3.4 5.3 3.6-11.4z" fill="#476ef0"/><path d="M35 33.5 39.5 47l-6-2.6-3.4 5.3-3.6-11.4z" fill="#476ef0"/><circle cx="28" cy="24.5" r="14" fill="#0d1630"/><circle cx="28" cy="24.5" r="11" fill="none" stroke="#a9bcff" stroke-width="1.2" stroke-dasharray="2 2.2"/><text x="28" y="29.2" text-anchor="middle" font-family="Manrope, sans-serif" font-size="13" font-weight="800" fill="#fff">A+</text><polygon class="trust-art__spark" points="46.00,8.40 47.12,11.46 50.37,11.58 47.81,13.59 48.70,16.72 46.00,14.90 43.30,16.72 44.19,13.59 41.63,11.58 44.88,11.46" fill="#476ef0"/>',
     "BBB accredited", "A+ rating, accredited since 2015", False),
    ('<circle cx="28" cy="28" r="28" fill="#eaf0fe"/><polygon points="9,20 20,16 32,20 47,16 47,40 32,44 20,40 9,44" fill="#d3defc"/><polygon points="20,16 32,20 32,44 20,40" fill="#bccdfa"/><path d="M13 37c5-4 9-1 12-3s5-6 10-5" fill="none" stroke="#476ef0" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="1.5 3"/><path class="trust-art__pin" d="M33 8a8.5 8.5 0 0 1 8.5 8.5c0 6.5-8.5 14.5-8.5 14.5s-8.5-8-8.5-14.5A8.5 8.5 0 0 1 33 8z" fill="#0d1630"/><circle cx="33" cy="16.5" r="3.2" fill="#476ef0"/>',
     "Based in Chesapeake", "Interior and exterior painting", False),
    ('<circle cx="28" cy="28" r="28" fill="#eaf0fe"/><path d="M28 9l14 5v11c0 9.5-6 16.5-14 20-8-3.5-14-10.5-14-20V14z" fill="#0d1630"/><path d="M21.5 27.5l4.5 4.5 9-9" fill="none" stroke="#a9bcff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
     "Licensed and insured", "Add your Virginia license #", True),
]


def trust_row():
    items = []
    for i, (art, title, sub, is_ph) in enumerate(TRUST):
        cls = " is-placeholder" if is_ph else ""
        tag = corner() if is_ph else ""
        items.append(f'<div class="trust-item wp-reveal{cls}"{reveal(i)}>{tag}<svg class="trust-art" viewBox="0 0 56 56" aria-hidden="true" focusable="false">{art}</svg>'
                     f'<p><strong>{title}</strong><span>{sub}</span></p></div>')
    return f"""<section class="wp-block-group alignfull trust-row has-global-padding" aria-label="About us at a glance">
  <div class="wp-block-group is-layout-grid columns-4">{"".join(items)}</div>
</section>"""


def how_it_works():
    return f"""<section class="wp-block-group alignfull section has-global-padding" aria-labelledby="how-title">
  <div class="wide is-placeholder ph-section">
    {corner("Sample process")}
    <div class="section-head wp-reveal"><h2 class="wp-block-heading" id="how-title">How it works</h2></div>
    <div class="wp-block-columns steps is-layout-flex">
      <div class="wp-block-column wp-reveal"><span class="step-number">1</span><h3 class="wp-block-heading">Tell us about the job</h3><p>Send the form or call. Rooms, siding, trim, whatever needs paint.</p></div>
      <div class="wp-block-column wp-reveal"{reveal(1)}><span class="step-number">2</span><h3 class="wp-block-heading">We take a look</h3><p>We come out, look at the surfaces and talk through colors and finishes.</p></div>
      <div class="wp-block-column wp-reveal"{reveal(2)}><span class="step-number">3</span><h3 class="wp-block-heading">We paint</h3><p>Prep, prime where it's needed, then paint. You get a price before we start.</p></div>
    </div>
  </div>
</section>"""


# FAQ answers come from the client's own Facebook posts. The last two are placeholders.
FAQS = [
    ("How long have you been in business?",
     "Since 1994. We're a family-owned painting business based in Chesapeake, and we've been BBB accredited since 2015.", False),
    ("Which finish should I use on my walls?",
     "Eggshell is a common pick for interior walls. It's close to flat, with a little more sheen, and it washes better, so fingerprints and marks come off more easily.", False),
    ("Oil-based or water-based paint for the outside?",
     "Oil-based paint has the longest record outdoors. It stands up to weather and leaves a smooth finish, but it's harder to work with and dries more slowly than water-based acrylic.", False),
    ("Why is the paint on my siding peeling?",
     "One common reason is the wrong primer. If the primer doesn't suit the surface, the paint can't grip, and it cracks and peels.", False),
    ("Can a window AC unit damage paint?",
     "Yes. Window units are a big cause of rotted sills and peeling paint around the frame and on the siding below. If you run them, expect to repaint more often.", False),
    ("Do I need primer?",
     "Often, yes. Primer sticks to surfaces where paint alone can fail, and it seals porous spots so the paint goes on and dries evenly.", False),
    ("How much paint should I buy?",
     "A little more than the job needs. If you run short, the extra is already there, and whatever is left over is handy for touch-ups later.", False),
    ("Which areas do you cover?",
     f"We're based in Chesapeake. {ph('List the nearby cities here, for example Virginia Beach, Norfolk, Portsmouth and Suffolk.')}", True),
    ("Are estimates free?",
     ph("Say here whether estimates are free and how soon you can come out."), True),
]


def faq_section(root, title="Questions we hear a lot"):
    def item(q, a, is_ph):
        tag = " " + chip() if is_ph else ""
        return f'<details class="wp-block-details"><summary>{q}{tag}</summary><p>{a}</p></details>'
    half = (len(FAQS) + 1) // 2
    col = lambda items: "".join(item(q, a, p) for q, a, p in items)
    return f"""<section class="wp-block-group alignfull section has-global-padding" aria-labelledby="faq-title">
  <div class="wide">
    <div class="section-head wp-reveal">
      <h2 class="wp-block-heading" id="faq-title">{title}</h2>
      <p>Most of these answers come from tips we've posted on our Facebook page.</p>
    </div>
    <div class="faq-grid wp-reveal"><div>{col(FAQS[:half])}</div><div>{col(FAQS[half:])}</div></div>
  </div>
</section>"""


# ---------- Home ----------

def home(root):
    return f"""
<div class="wp-block-cover alignfull hero-cover">
  {img(root, "hero", "", "100vw", cls="wp-block-cover__image-background", eager=True, extra=' data-object-fit="cover"')}
  <span aria-hidden="true" class="wp-block-cover__background has-background-dim-80 has-background-dim" style="background-color:{DIM}"></span>
  <div class="wp-block-cover__inner-container">
    <div class="wp-block-columns is-layout-flex">
      <div class="wp-block-column">
        <h1 class="wp-block-heading">House painting in Chesapeake, VA</h1>
        <p class="hero-lede">Interior and exterior painting for your home. If the outside needs paint and you'd rather not climb a ladder, we'll take care of it.</p>
        <div data-hero-cta>{buttons(button(root + "quote/", "Get a quote", "", "arrow"), button("tel:" + TEL, "Call " + PHONE, "outline", "phone"))}</div>
        <p class="hero-meta"><span>{SVG["roller"]} Family owned since 1994</span><span>{SVG["shield"]} BBB accredited, A+ rating</span><span>{SVG["pin"]} Based in Chesapeake</span></p>
      </div>
      <div class="wp-block-column hero-form-col">
        <div class="quote-box">
          <div class="quote-box__head"><h2 class="wp-block-heading">Request a quote</h2><p>Two quick steps. Or call <a href="tel:{TEL}">{PHONE}</a></p></div>
          <div class="gform_wrapper">
            {steps(["The job", "Your details"])}
            <div class="gform_validation_errors" role="alert" hidden>There was a problem with your submission. Please review the fields below.</div>
            <form method="post" novalidate data-autoadvance>
              <div class="gform_page" data-title="The job">
                <div class="gform_fields">
                  {gfield("What needs painting?", hero_cards(), True, group=True)}
                </div>
                <div class="gform_page_footer"><button class="wp-element-button gform_next_button" type="button">Next {SVG["arrow"]}</button></div>
              </div>
              <div class="gform_page" data-title="Your details" hidden>
                <div class="gform_fields">
                  {gfield(lab("h-name", "Name"), '<input id="h-name" name="name" type="text" autocomplete="name" required>', True)}
                  {gfield(lab("h-phone", "Phone"), '<input id="h-phone" name="phone" type="tel" autocomplete="tel" required>', True, True, stack=False)}
                  {gfield(lab("h-zip", "ZIP code"), '<input id="h-zip" name="zip" type="text" inputmode="numeric" maxlength="5" autocomplete="postal-code" required>', True, True, stack=False)}
                </div>
                <p class="gform_note">We'll only use these to get back to you about this job.</p>
                <div class="gform_page_footer">{BACK}<button class="wp-element-button" type="submit">Get my quote</button></div>
              </div>
            </form>
            <div class="gform_confirmation_wrapper" hidden><div class="gform_confirmation_message" role="status">{CONFIRM_ICON}<h3 class="wp-block-heading">Thanks<span data-first-name></span>! We got your request.</h3><p>We'll call you back at <strong data-echo="phone"></strong>. Need us sooner? Call <a href="tel:{TEL}">{PHONE}</a>.</p></div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

{trust_row()}

<section class="wp-block-group alignfull section has-global-padding" aria-labelledby="services-title">
  <div class="wide">
    <div class="section-head wp-reveal">
      <h2 class="wp-block-heading" id="services-title">What we paint</h2>
      <p>Inside and outside your home. Cards marked as placeholders are services we still need James to confirm.</p>
    </div>
    {service_cards(root)}
    <div class="truck-note wp-reveal"><p><strong>Also ask about:</strong> {ph(", ".join(EXTRAS).lower().capitalize())} {chip()}</p>{buttons(button(root + "services/", "See all services", "outline"))}</div>
  </div>
</section>

<section class="wp-block-group alignfull section has-accent-5-background-color has-global-padding" aria-labelledby="about-title">
  <div class="wp-block-media-text alignwide wide is-stacked-on-mobile wp-reveal" style="grid-template-columns:48% auto">
    {lightbox_figure(root, "prep", "Painter pressing tape along a wall before painting", "(min-width: 782px) 48vw, 100vw", "wp-block-media-text__media")}
    <div class="wp-block-media-text__content">
      <h2 class="wp-block-heading is-style-text-annotation">About us</h2>
      <h2 class="wp-block-heading" id="about-title">A house painter in Chesapeake</h2>
      <p>James Skipper Painting is a family-owned business on Willow Ave in Chesapeake, Virginia. We've been painting since 1994, inside and out.</p>
      <p>Most of a good paint job happens before the paint goes on, so that's where we put the work: scraping, patching, priming and getting the surface right.</p>
      <p class="list-intro">A few things we've shared on our page:</p>
      <ul class="wp-block-list is-style-checks">
        <li>Peeling siding paint often starts with the wrong primer</li>
        <li>Pick exterior colors that work with your roof</li>
        <li>Light changes how a color looks, so test it in the room</li>
        <li>Buy a little extra paint for touch-ups</li>
      </ul>
      {buttons(button(root + "paint-tips/", "Read our paint tips", "outline"))}
    </div>
  </div>
</section>

{how_it_works()}

{testimonial(root)}

{tip_band(root)}

{faq_section(root)}

{home_contact(root)}
"""


# ---------- Services ----------

DETAIL = {
    "interior-painting": (["Walls, ceilings and trim in the rooms you live in. Want a calm bedroom? Several shades of one neutral color give it depth without feeling busy.",
                           "Small room? Bold, bright colors tend to open it up more than plain white, and a ceiling a shade lighter than the walls makes it feel airier."],
                          ["Scuffs and marks that won't wipe off", "Colors that make a room feel dark or dated"]),
    "exterior-painting": (["Been putting off the outside of the house because you don't want to balance at the top of a shaky ladder? Let's talk. We'll get it repainted while you stay on solid ground.",
                           "When you pick colors, look at the roof and the style of the house. Slate, metal, clay and terra cotta roofs all pull a color scheme in different directions."],
                          ["Paint cracking or peeling on the siding", "Peeling paint around and below window AC units"]),
    "commercial-painting": (["Offices, shops and rental units, inside and out. Bright white on walls and ceilings makes a space noticeably lighter.",
                             "Tell us about the building, the timing and anything that has to stay open while we work."],
                            ["Walls looking tired in a customer area", "A unit to repaint between tenants"]),
    "color-advice": (["Not sure where to start? We'll help you choose colors that suit the house, the roof and the light in each room.",
                      "Fluorescent light pulls a color toward green and blue. Warm bulbs bring out red. A sample on the wall tells you more than a chip in the store."],
                     ["You've been stuck on white walls", "You want the outside to match the style of the house"]),
}


def services(root):
    rows = []
    for i, s in enumerate(SERVICES):
        body, signs = DETAIL[s["id"]]
        flip = " svc-row--flip" if i % 2 else ""
        bg = " has-accent-5-background-color" if i % 2 else ""
        phc = " is-placeholder" if s["ph"] else ""
        tag = corner("Placeholder service") if s["ph"] else ""
        rows.append(f"""<section class="wp-block-group alignfull section has-global-padding{bg}" id="{s["id"]}" aria-labelledby="{s["id"]}-title">
  <div class="svc-row{flip} wide wp-reveal{phc}">
    {tag}
    {lightbox_figure(root, s["img"], s["alt"], "(min-width: 782px) 50vw, 40vw", "wp-block-image svc-row__media")}
    <div class="svc-row__head"><span class="is-style-text-annotation">{s["kind"]}</span><h2 class="wp-block-heading" id="{s["id"]}-title">{s["name"]}</h2></div>
    <div class="svc-row__body">
      {"".join(f"<p>{p}</p>" for p in body)}
      <div class="signs"><h3 class="wp-block-heading">Signs it's time</h3><ul class="wp-block-list is-style-checks">{"".join(f"<li>{x}</li>" for x in signs)}</ul></div>
      {buttons(button(quote_link(root, s["id"]), "Get a quote", "", "arrow"), button("tel:" + TEL, "Call us", "outline", "phone"))}
    </div>
  </div>
</section>""")
    extras = "".join(f"<li>{x}</li>" for x in EXTRAS)
    return f"""
{banner(root, "Services", "Our services", "House painting in Chesapeake, Virginia, inside and out.")}
<section class="wp-block-group alignfull section has-global-padding" style="padding-bottom:0" aria-label="Jump to a service">
  <div class="wide">{service_cards(root, link_to_anchor=False)}</div>
</section>
{"".join(rows)}
<section class="wp-block-group alignfull section has-global-padding" id="more" aria-labelledby="more-title">
  <div class="svc-row wide wp-reveal is-placeholder">
    {corner("Placeholder services")}
    {lightbox_figure(root, "prep", "Painter pressing tape along a wall before painting", "(min-width: 782px) 50vw, 40vw", "wp-block-image svc-row__media")}
    <div class="svc-row__head"><span class="is-style-text-annotation">Also available</span><h2 class="wp-block-heading" id="more-title">Other jobs</h2></div>
    <div class="svc-row__body">
      <p>Common extras for a house painter. Keep the ones James does and delete the rest.</p>
      <ul class="extras-list wp-block-list">{extras}</ul>
      {buttons(button(quote_link(root, "something-else"), "Ask about another job", "", "arrow"))}
    </div>
  </div>
</section>
{cta(root, "Not sure what the job needs?", "Tell us what you're seeing. We'll talk it through with you.")}
"""


# ---------- About ----------

def about(root):
    values = [("Primer first", "The right primer is what keeps paint from cracking and peeling later."),
              ("Colors that fit", "The roof, the style of the house and the light in the room all count."),
              ("The right finish", "Eggshell on walls you want to wipe clean. Oil-based where toughness matters."),
              ("Extra for touch-ups", "Buy a little more than you need and keep the rest.")]
    vhtml = "".join(f'<div class="value-tile wp-reveal"{reveal(i)}><h3 class="wp-block-heading">{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(values))
    return f"""
{banner(root, "About us", "About James Skipper Painting", "A family-owned house painting business in Chesapeake, Virginia, since 1994.")}
<section class="wp-block-group alignfull section has-global-padding">
  <div class="wp-block-columns alignwide wide is-layout-flex">
    <div class="wp-block-column wp-reveal">
      <div class="overlapped">
        {lightbox_figure(root, "trim", "Painter working on the roof trim of a green house", "(min-width: 782px) 25vw, 50vw", "wp-block-image")}
        {lightbox_figure(root, "interior", "Painter rolling white paint onto an interior wall", "(min-width: 782px) 25vw, 50vw", "wp-block-image")}
      </div>
    </div>
    <div class="wp-block-column wp-reveal" style="--reveal-delay:.08s;display:grid;gap:var(--wp--style--block-gap);align-content:center">
      <span class="is-style-text-annotation">Who we are</span>
      <h2 class="wp-block-heading">Local house painting, inside and out</h2>
      <p>James Skipper Painting is a family-owned and operated business at {STREET} in Chesapeake, Virginia. We've been painting homes since 1994.</p>
      <p>We put the effort into preparation, we adjust to what each house needs, and we care about how our customers feel when the job is done.</p>
      <p>We've been accredited by the Better Business Bureau since 2015 and hold an A+ rating.</p>
      <div class="is-placeholder ph-block">
        {corner("Placeholder story")}
        <p>Tell the story here in James's own words: how the business started in 1994, who in the family works with you, and the jobs you're proudest of. Two or three short paragraphs is plenty.</p>
      </div>
    </div>
  </div>
</section>
<section class="wp-block-group alignfull section has-accent-5-background-color has-global-padding">
  <div class="wide">
    <div class="section-head wp-reveal"><h2 class="wp-block-heading">What we tell people before they paint</h2><p>From the tips on our Facebook page.</p></div>
    <div class="wp-block-group is-layout-grid columns-4">{vhtml}</div>
  </div>
</section>
<section class="wp-block-group alignfull section has-global-padding">
  <div class="wp-block-group has-text-align-center wp-reveal is-placeholder ph-block" style="max-width:680px;margin:0 auto">
    {corner()}
    <span class="is-style-text-annotation">Licensed and insured</span>
    <h2 class="wp-block-heading" style="margin-top:14px">Your license and insurance go here</h2>
    <p style="margin-top:14px;color:var(--wp--preset--color--accent-4)">Virginia contractor license number and class, insurance, and EPA lead-safe certification if you work on homes built before 1978. Only what James actually holds.</p>
  </div>
</section>
{tip_band(root)}
{cta(root)}
"""


# ---------- Paint tips (from the client's Facebook posts, rewritten in plain words) ----------

from tip_art import ART, LIGHT_DEMO

TOPIC_ICON = {
    "color": ICON["color-advice"],
    "outside": ICON["exterior-painting"],
    "prep": '<path d="m14.622 17.897-10.68-2.913"/><path d="M18.376 2.622a1 1 0 1 1 3.002 3.002L17.36 9.643a.5.5 0 0 0 0 .707l.944.944a2.41 2.41 0 0 1 0 3.408l-.944.944a.5.5 0 0 1-.707 0L8.354 7.348a.5.5 0 0 1 0-.707l.944-.944a2.41 2.41 0 0 1 3.408 0l.944.944a.5.5 0 0 0 .707 0z"/><path d="M9 8c-1.804 2.71-3.97 3.46-6.583 3.948a.507.507 0 0 0-.302.819l7.32 8.883a1 1 0 0 0 1.185.204C12.735 20.405 16 16.792 16 15"/>',
    "finishes": '<path d="m19 11-8-8-8.6 8.6a2 2 0 0 0 0 2.8l5.2 5.2c.8.8 2 .8 2.8 0L19 11Z"/><path d="m5 2 5 5"/><path d="M2 13h15"/><path d="M22 20a2 2 0 1 1-4 0c0-1.6 1.7-2.4 2-4 .3 1.6 2 2.4 2 4Z"/>',
}

# (id, nav label, heading, photo, photo alt, intro, [(art, title, text)])
TIP_SECTIONS = [
    ("color", "Color", "Color", "tips-color", "Open paint sample pots in blues, whites, reds and yellows",
     "Picking a color is the fun part. These help it look the way you pictured once it's on the wall.", [
         ("light", "Test colors under your own lights", "Fluorescent light is cool and pulls out the green or blue in a color. Incandescent bulbs are warm and bring out the red. Look at a sample in the room you're painting."),
         ("white", "Don't settle for white walls", "Unless white is the look you want. The right color adds depth and can make a plain room feel warm and comfortable."),
         ("small", "Small rooms can take bold color", "White doesn't always make a room look bigger. Bright, bold colors open a space more than dull shades. Paint the ceiling lighter than the walls to keep it airy."),
         ("bedroom", "A calm bedroom", "Use several shades of one neutral color. The neutral keeps it restful, and the different shades give the room layers and depth."),
         ("office", "Brighter workspaces", "Bright white on ceilings and walls raises the light level in a building."),
     ]),
    ("outside", "Outside", "Outside the house", "tips-outside", "Red lap siding around a white window",
     "Outside, the color has to work with things you can't easily change, like the roof and the style of the house.", [
         ("roof", "Match the roof", "Slate, terra cotta, metal or clay: choose a color scheme that sits well with your roof so the house looks like one piece."),
         ("style", "Let the house style guide you", "The architecture can steer your colors. A colonial home, for example, often looks right in a color from that period."),
         ("ac", "Watch the window AC units", "They're a major cause of rotted sills and peeling paint around the frame and the siding below. With units in, plan to repaint more often."),
     ]),
    ("prep", "Prep", "Prep and planning", "prep", "Painter pressing tape along a wall before painting",
     "Most paint problems start underneath. Get the prep right and the finish lasts.", [
         ("peel", "Peeling siding? Check the primer", "Cracked, peeling paint on siding can come from using the wrong primer. Poor grip means the paint fails."),
         ("layers", "What primer does", "It sticks where paint alone might not, and it seals porous surfaces so the paint spreads and dries evenly."),
         ("spackle", "Spackle is for walls, not trim", "Putty or spackle works on small cracks and dents in walls. It won't stick to wood trim."),
         ("extra", "Buy a little extra", "On a big job, get a bit more paint than you think you need. If you run short it's on hand, and the rest is there for touch-ups."),
     ]),
    ("finishes", "Finishes", "Paint and finishes", "tips-finishes", "Empty room with fresh gray walls and white trim",
     "Sheen and paint type change how a wall looks, how it cleans and how long it holds up.", [
         ("sheen", "What eggshell means", "Close to flat, with more sheen. It washes better, which is why it's so common on interior walls."),
         ("wateroil", "Water based or oil based", "Those are the two kinds of exterior paint. Oil based has the longest record for lasting and standing up to weather, and it goes on smooth."),
         ("oil", "Oil-based paint, pros and cons", "Linseed or alkyd based. Harder to use and slower to dry than water-based acrylic, but the finish is tougher and can last for decades."),
     ]),
]


def topic_icon(key):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{TOPIC_ICON[key]}</svg>'


def tips_nav():
    links = "".join(f'<a href="#{sid}">{topic_icon(sid)}{label}<span class="tips-nav__count">{len(tips)}</span></a>'
                    for sid, label, _, _, _, _, tips in TIP_SECTIONS)
    return f'<nav class="tips-nav has-global-padding" aria-label="Tip topics"><div class="tips-nav__inner wide">{links}</div></nav>'


def light_demo():
    opts = [("day", "Daylight"), ("cool", "Cool bulb"), ("warm", "Warm bulb")]
    radios = "".join(f'<label><input type="radio" name="light" value="{v}"{" checked" if v == "day" else ""}><span>{l}</span></label>' for v, l in opts)
    return f"""<section class="wp-block-group alignfull section has-global-padding" aria-labelledby="demo-title">
  <div class="wp-block-columns alignwide wide is-layout-flex light-demo">
    <div class="wp-block-column wp-reveal"><figure class="light-demo__figure">{LIGHT_DEMO}</figure></div>
    <div class="wp-block-column wp-reveal"{reveal(1)}>
      <span class="is-style-text-annotation">Try it</span>
      <h2 class="wp-block-heading" id="demo-title">Same paint, different light</h2>
      <p class="light-demo__lede">A color that looked right in the store can look different at home. Switch the light and watch the wall.</p>
      <fieldset class="light-switch"><legend class="screen-reader-text">Light in the room</legend>{radios}</fieldset>
      <p class="light-demo__tip">Our tip: put a sample on the wall you're painting and look at it under the lights you actually use.</p>
    </div>
  </div>
</section>"""


def paint_tips(root):
    sections = []
    for n, (sid, label, title, photo, alt, intro, tips) in enumerate(TIP_SECTIONS):
        bg = " has-accent-5-background-color" if n % 2 == 0 else ""
        cards = "".join(
            f'<article class="wp-block-post tip-card wp-reveal" id="tip-{art}"{reveal(i % 2)}>'
            f'<figure class="wp-block-post-featured-image tip-art">{ART[art]}</figure>'
            f'<div class="tip-card__body"><h3 class="wp-block-post-title">{h}</h3><p>{t}</p></div></article>'
            for i, (art, h, t) in enumerate(tips))
        sections.append(f"""<section class="wp-block-group alignfull section has-global-padding tips-section{bg}" id="{sid}" aria-labelledby="{sid}-title">
  <div class="tips-section__inner wide">
    <div class="tips-section__head wp-reveal">
      <figure class="wp-block-image tips-section__media">{img(root, photo, alt, "(min-width: 1000px) 320px, (min-width: 600px) 240px, 100vw")}</figure>
      <div class="tips-section__text">
        <span class="tips-section__count">{len(tips)} tips</span>
        <h2 class="wp-block-heading" id="{sid}-title">{title}</h2>
        <p>{intro}</p>
      </div>
    </div>
    <div class="wp-block-post-template tips-list">{cards}</div>
  </div>
</section>""")
    return f"""
{banner(root, "Paint tips", "Paint tips", "Advice we've shared on our Facebook page, all in one place.")}
{tips_nav()}
{light_demo()}
{"".join(sections)}
<section class="wp-block-group alignfull has-global-padding" style="padding-bottom:var(--wp--preset--spacing--40)">
  <p class="tips-source wide">From posts on the <a href="{FACEBOOK}" target="_blank" rel="noopener">James Skipper Painting Facebook page</a>.</p>
</section>
{cta(root, "Have a question about your house?", "Call or send the form. We're happy to talk colors, primer and finishes.")}
"""


# ---------- Reviews ----------

def reviews(root):
    return f"""
{banner(root, "Reviews", "Reviews", "What customers say about James Skipper Painting.")}
{testimonial(root, show_link=False)}
<section class="wp-block-group alignfull section has-global-padding" style="padding-top:0">
  <div class="bbb-record wide wp-reveal">
    <div><span class="bbb-record__big">A+</span><span>BBB rating</span></div>
    <div><span class="bbb-record__big">2015</span><span>BBB accredited since</span></div>
    <div><span class="bbb-record__big">0</span><span>Complaints closed in the last 3 years</span></div>
    <p>From our <a href="{BBB}" target="_blank" rel="noopener">Better Business Bureau profile</a>.</p>
  </div>
</section>
<section class="wp-block-group alignfull section has-accent-5-background-color has-global-padding">
  <div class="wp-block-group has-text-align-center wp-reveal" style="max-width:680px;margin:0 auto">
    <h2 class="wp-block-heading">Had us paint for you?</h2>
    <p style="margin-top:14px;color:var(--wp--preset--color--accent-4)">A short review helps your neighbors find us. It means a lot to a small business.</p>
    <div style="margin-top:24px">{buttons(button(FB_REVIEWS, "Review us on Facebook", "", None, ' target="_blank" rel="noopener"'), button(BBB, "See our BBB profile", "outline", None, ' target="_blank" rel="noopener"'), center=True)}</div>
    <p style="margin-top:16px;font-size:var(--wp--preset--font-size--small);color:var(--wp--preset--color--accent-4)">{ph("Add a Google review button once the Google Business Profile is set up.")} {chip()}</p>
  </div>
</section>
{cta(root)}
"""


# ---------- Contact ----------

def contact(root):
    return f"""
{banner(root, "Contact", "Contact us", "Call, email or send us a message.")}
<section class="wp-block-group alignfull section has-global-padding">
  <div class="contact-layout wide">
    <div class="contact-cols wp-reveal">
      <div><h3 class="wp-block-heading">Phone</h3><p><a href="tel:{TEL}">{PHONE}</a></p></div>
      <div><h3 class="wp-block-heading">Based at</h3><p>{STREET}<br>{CITY}<br><a href="{MAPS}" target="_blank" rel="noopener" style="font-weight:500">Open in Maps</a></p></div>
      <div class="span-2"><h3 class="wp-block-heading">Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div class="span-2"><h3 class="wp-block-heading">Facebook</h3><p><a href="{FACEBOOK}" target="_blank" rel="noopener">James Skipper Painting</a></p></div>
      <div class="span-2">{hours_card(" hours-card--flat")}</div>
    </div>
    <div class="form-panel wp-reveal"{reveal(1)}>
      <div class="gform_wrapper">
        <div class="gform_heading"><h2 class="gform_title">Send us a message</h2><span class="gform_description">We'll get back to you soon. Want a price? The <a href="{root}quote/">quote form</a> is quicker.</span></div>
        <div class="gform_validation_errors" role="alert" hidden>There was a problem with your submission. Please review the fields below.</div>
        <form method="post" novalidate>
          <div class="gform_fields">
            {gfield(lab("c-name", "Name"), '<input id="c-name" name="name" type="text" autocomplete="name" required>', True, True)}
            {gfield(lab("c-phone", "Phone"), '<input id="c-phone" name="phone" type="tel" autocomplete="tel" required>', True, True)}
            {gfield(lab("c-email", "Email"), '<input id="c-email" name="email" type="email" autocomplete="email" required>', True)}
            {gfield(lab("c-msg", "Message"), '<textarea id="c-msg" name="message" rows="5" required></textarea>', True)}
          </div>
          <div class="gform_footer"><button class="wp-element-button" type="submit">Send message</button></div>
        </form>
        <div class="gform_confirmation_wrapper" hidden><div class="gform_confirmation_message" role="status"><h3 class="wp-block-heading">Thanks for getting in touch!</h3><p>We'll get back to you soon. If it's urgent, call <a href="tel:{TEL}">{PHONE}</a>.</p></div></div>
      </div>
    </div>
  </div>
</section>
"""


# ---------- Quote ----------

def quote(root):
    radio = lambda name, vals: "".join(f'<li><label class="gchoice"><input type="radio" name="{name}" value="{v}"> {v}</label></li>' for v in vals)
    checks = lambda name, vals: "".join(f'<li><label class="gchoice"><input type="checkbox" name="{name}" value="{v}"> {v}</label></li>' for v in vals)
    nav = lambda prev, nxt: f'<div class="gform_page_footer">{BACK if prev else ""}{nxt}</div>'
    nxt = '<button class="wp-element-button gform_next_button" type="button">Next</button>'
    sub = '<button class="wp-element-button" type="submit">Send request</button>'
    lede = 'Three quick steps. Prefer to talk? Call <a href="tel:' + TEL + '">' + PHONE + '</a>.'
    return f"""
{banner(root, "Get a quote", "Request a quote", lede)}
<section class="wp-block-group alignfull section has-global-padding">
  <div class="quote-layout">
    <div class="form-panel">
      <div class="gform_wrapper">
        {steps(["The job", "The property", "Your details"])}
        <div class="gform_validation_errors" role="alert" hidden>There was a problem with your submission. Please review the fields below.</div>
        <form method="post" novalidate>
          <div class="gform_page" data-title="The job">
            <div class="gform_fields">
              {gfield("What do you need painted?", quote_cards(), True, group=True, desc="Pick all that apply.")}
            </div>
            {nav(False, nxt)}
          </div>
          <div class="gform_page" data-title="The property" hidden>
            <div class="gform_fields">
              {gfield("Is this a home or a business?", f'<ul class="gfield_radio inline">{radio("property", ["Home", "Business"])}</ul>', True, group=True)}
              {gfield("Which parts?", f'<ul class="gfield_checkbox two-col">{checks("parts", ["Walls", "Ceilings", "Trim and doors", "Siding", "Window frames and sills", "Not sure"])}</ul>', group=True)}
              {gfield("When was it built?", f'<ul class="gfield_radio inline">{radio("built", ["Before 1978", "1978 or later", "Not sure"])}</ul>', group=True, desc="Homes built before 1978 may have lead paint, which changes how the prep is done.")}
              {gfield(lab("q-zip", "ZIP code"), '<input id="q-zip" name="zip" type="text" inputmode="numeric" maxlength="5" autocomplete="postal-code" required>', True, True, stack=False)}
              {gfield(lab("q-details", "Anything we should know?"), '<textarea id="q-details" name="details" rows="4" placeholder="For example: peeling paint on the siding by the back porch, or two bedrooms and a hallway"></textarea>')}
            </div>
            {nav(True, nxt)}
          </div>
          <div class="gform_page" data-title="Your details" hidden>
            <div class="gform_fields">
              {gfield(lab("q-name", "Name"), '<input id="q-name" name="name" type="text" autocomplete="name" required>', True, True)}
              {gfield(lab("q-phone", "Phone"), '<input id="q-phone" name="phone" type="tel" autocomplete="tel" required>', True, True)}
              {gfield(lab("q-email", "Email"), '<input id="q-email" name="email" type="email" autocomplete="email">')}
              {gfield("Best way to reach you", f'<ul class="gfield_radio inline">{radio("contact_pref", ["Phone call", "Email"])}</ul>', group=True)}
            </div>
            {nav(True, sub)}
          </div>
        </form>
        <div class="gform_confirmation_wrapper" hidden><div class="gform_confirmation_message" role="status">{CONFIRM_ICON}<h3 class="wp-block-heading">Thanks<span data-first-name></span>! Your request is in.</h3><p>We'll call you back at <strong data-echo="phone"></strong>. Need us sooner? Call <a href="tel:{TEL}">{PHONE}</a>.</p></div></div>
      </div>
    </div>
    <aside class="widget-area" aria-label="Sidebar">
      <section class="widget widget--dark">
        <h2 class="widget-title">Rather talk?</h2>
        <a class="widget-phone" href="tel:{TEL}">{PHONE}</a>
        <p><a class="widget-mail" href="mailto:{EMAIL}">{EMAIL}</a></p>
      </section>
      <section class="widget">
        <h2 class="widget-title">Paint tip</h2>
        <p>On a big job, buy a little more paint than you think you need. The extra is there if you run short, and for touch-ups later.</p>
        <p style="margin-top:10px"><a href="{root}paint-tips/">More paint tips</a></p>
      </section>
      <section class="widget is-placeholder">
        {corner()}
        <h2 class="widget-title">Estimates</h2>
        <p>{ph("Say how estimates work: free or paid, in person or from photos, and how soon you can come out.")}</p>
      </section>
    </aside>
  </div>
</section>
"""


def notfound(root):
    return f"""
<section class="wp-block-group alignfull notfound has-global-padding">
  <h1 class="wp-block-heading">We couldn't find that page</h1>
  <p>It may have moved. Try the homepage or give us a call.</p>
  {buttons(button(root, "Go to the homepage", "", "arrow"), button("tel:" + TEL, "Call " + PHONE, "outline"), center=True)}
</section>
"""


def jsonld():
    data = {
        "@context": "https://schema.org", "@type": "HousePainter", "name": NAME,
        "url": BASE_URL, "logo": BASE_URL + "assets/img/logo.png", "image": BASE_URL + "assets/img/og-image.jpg",
        "telephone": "+1-757-403-4451", "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": "Chesapeake",
                    "addressRegion": "VA", "postalCode": "23325", "addressCountry": "US"},
        "foundingDate": "1994",
        "areaServed": {"@type": "City", "name": "Chesapeake"},
        "sameAs": [FACEBOOK, BBB],
    }
    return f'<script type="application/ld+json">{json.dumps(data, separators=(",", ":"))}</script>\n'


if __name__ == "__main__":
    hw = IMGS["hero"][0]
    preload = (f'<link rel="preload" as="image" href="assets/img/hero-{hw[1]}.webp" '
               f'imagesrcset="{srcset("", "hero")}" imagesizes="100vw" fetchpriority="high">\n')
    page(0, "", "House Painting in Chesapeake, VA | James Skipper Painting",
         f"Family-owned interior and exterior house painting in Chesapeake, Virginia, since 1994. BBB accredited. Call {PHONE} or request a quote.",
         "", home, extra_head=preload + jsonld(), body_class="home page")
    page(1, "services/", "Painting Services | James Skipper Painting, Chesapeake VA",
         "Interior and exterior house painting in Chesapeake, Virginia.", "services/", services)
    page(1, "about-us/", "About Us | James Skipper Painting, Chesapeake VA",
         "A family-owned house painting business in Chesapeake, Virginia, since 1994.", "about-us/", about)
    page(1, "paint-tips/", "Paint Tips | James Skipper Painting",
         "Color, primer and finish tips from James Skipper Painting in Chesapeake, Virginia.", "paint-tips/", paint_tips)
    page(1, "reviews/", "Reviews | James Skipper Painting, Chesapeake VA",
         "Reviews of James Skipper Painting, house painting in Chesapeake, Virginia.", "reviews/", reviews)
    page(1, "contact-us/", f"Contact Us | James Skipper Painting | {PHONE}",
         f"Call {PHONE}, email {EMAIL} or send a message.", "contact-us/", contact)
    page(1, "quote/", "Request a Quote | James Skipper Painting",
         "Request a quote for interior or exterior house painting in Chesapeake, Virginia.", None, quote, actions=False)
    # 404 uses absolute links because GitHub Pages serves it at any depth
    out = f"""{head(BASE_URL, "Page not found | James Skipper Painting", "This page could not be found.", "404.html")}
<body class="error404 has-mobile-actions">
<div class="wp-site-blocks">
{header(BASE_URL, None)}
<main class="wp-block-group" id="wp--skip-link--target">{notfound(BASE_URL)}</main>
{footer(BASE_URL)}
</div>
{mobile_actions(BASE_URL)}
</body>
</html>
"""
    with open(os.path.join(OUT, "404.html"), "w") as f:
        f.write(out)
    print("wrote 404.html")
    with open(os.path.join(OUT, "version.json"), "w") as f:
        json.dump({"build": BUILD}, f)
    print("wrote version.json", BUILD)
