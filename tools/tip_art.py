"""Flat illustrations for the Paint tips page (inline SVG, 320x200, brand palette).

Each one shows what its tip says, so the page reads at a glance. Drawn by hand, no stock.
"""

NAVY = "#0d1630"
BLUE = "#476ef0"
LB = "#a9bcff"
BG = "#eef2fb"
FONT = 'font-family="Manrope, sans-serif"'


def _svg(label, body, vb="0 0 320 200"):
    return (f'<svg class="tip-art__svg" viewBox="{vb}" role="img" aria-label="{label}" focusable="false" '
            f'xmlns="http://www.w3.org/2000/svg">{body}</svg>')


def _label(x, y, text, weight=600, size=11, fill=NAVY, anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" {FONT} font-size="{size}" font-weight="{weight}" fill="{fill}">{text}</text>'


def _can(x, y, band, text, w=76, h=84, text_fill="#fff"):
    return (f'<rect x="{x - 4}" y="{y - 9}" width="{w + 8}" height="11" rx="3" fill="{NAVY}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#fff" stroke="{NAVY}" stroke-width="2.5"/>'
            f'<rect x="{x}" y="{y + h * 0.3:.0f}" width="{w}" height="{h * 0.36:.0f}" fill="{band}"/>'
            + (_label(x + w / 2, y + h * 0.3 + h * 0.18 + 4.5, text, 800, 13 if w > 60 else 10, text_fill) if text else ""))


def _check(cx, cy, r=9):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BLUE}"/>'
            f'<path d="M{cx - 4} {cy}l3 3 5-6" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')


def _cross(cx, cy, r=9):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#c0392b"/>'
            f'<path d="M{cx - 3.5} {cy - 3.5}l7 7M{cx + 3.5} {cy - 3.5}l-7 7" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>')


def _bulb(cx, glow, cone, tint, panel_x, label):
    return (f'<path d="M{cx} 0v20" stroke="{NAVY}" stroke-width="2"/><path d="M{cx - 7} 20h14l-2 7h-10z" fill="{NAVY}"/>'
            f'<circle cx="{cx}" cy="35" r="9" fill="{glow}"/>'
            f'<polygon points="{cx - 8},42 {cx + 8},42 {panel_x + 124},176 {panel_x - 4},176" fill="{cone}" opacity=".55"/>'
            f'<rect x="{panel_x}" y="72" width="120" height="104" rx="6" fill="#d9cdb6"/>'
            f'<rect x="{panel_x + 32}" y="98" width="56" height="44" rx="3" fill="#9fb59b"/>'
            f'<rect x="{panel_x}" y="72" width="120" height="104" rx="6" fill="{tint}" opacity=".3"/>'
            + _label(cx, 194, label))


def _siding(fill, line, step=18, start=14):
    lines = "".join(f'<path d="M0 {y}H320" stroke="{line}" stroke-width="2"/>' for y in range(start, 200, step))
    return f'<rect width="320" height="200" fill="{fill}"/>{lines}'


ART = {
    "light": _svg("The same wall color under a cool bulb and a warm bulb",
                  f'<rect width="320" height="200" fill="{BG}"/>'
                  + _bulb(84, "#e3edff", "#cfe0ff", "#5f8dff", 24, "Cool light")
                  + _bulb(236, "#ffe3b0", "#ffd79a", "#ff9f2e", 176, "Warm bulb")),

    "white": _svg("A roller painting color over a white wall",
                  '<rect width="320" height="200" fill="#f7f5f0"/>'
                  '<rect x="150" y="0" width="170" height="168" fill="#c8785b"/>'
                  '<path d="M150 30c-8 2-14 0-22 4l-6 4v112l8 2c8-3 12 1 20-2z" fill="#c8785b"/>'
                  '<rect x="0" y="168" width="320" height="32" fill="#d9c3a5"/>'
                  '<rect x="206" y="40" width="70" height="54" rx="2" fill="#fff"/><rect x="212" y="46" width="58" height="42" fill="#efe3d0"/>'
                  '<path d="M218 82l16-18 10 10 8-7 18 15z" fill="#9fb59b"/>'
                  '<rect x="196" y="120" width="106" height="40" rx="10" fill="#2b3550"/><rect x="188" y="132" width="18" height="32" rx="7" fill="#2b3550"/><rect x="292" y="132" width="18" height="32" rx="7" fill="#2b3550"/>'
                  f'<rect x="110" y="56" width="16" height="66" rx="5" fill="#c8785b" stroke="{NAVY}" stroke-width="2"/>'
                  f'<path d="M110 89H94v36" fill="none" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
                  f'<rect x="88" y="124" width="12" height="38" rx="5" fill="{NAVY}"/>'),

    "small": _svg("A small room in a bold color with a lighter ceiling",
                  f'<rect width="320" height="200" fill="{BG}"/>'
                  '<polygon points="70,14 250,14 210,52 110,52" fill="#f3f7f6"/>'
                  '<polygon points="70,14 110,52 110,142 70,186" fill="#2c6670"/>'
                  '<polygon points="250,14 210,52 210,142 250,186" fill="#2c6670"/>'
                  '<rect x="110" y="52" width="100" height="90" fill="#3b818a"/>'
                  '<polygon points="70,186 110,142 210,142 250,186" fill="#c99b6b"/>'
                  '<rect x="138" y="70" width="44" height="34" rx="2" fill="#f3f7f6"/><rect x="143" y="75" width="34" height="24" fill="#e0b25c"/>'
                  + _label(160, 38, "LIGHTER CEILING", 800, 9.5, "#2c6670")
                  + f'<path d="M56 100H18m0 0 8-6m-8 6 8 6M264 100h38m0 0-8-6m8 6-8 6" fill="none" stroke="{BLUE}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'),

    "bedroom": _svg("A bedroom in several shades of one neutral color",
                    '<rect width="320" height="200" fill="#ece4d4"/>'
                    '<rect x="58" y="36" width="204" height="134" fill="#d8ccb5"/>'
                    '<rect x="86" y="84" width="148" height="44" rx="6" fill="#b8a98d"/>'
                    '<rect x="68" y="120" width="184" height="50" rx="6" fill="#fbf9f4"/>'
                    '<rect x="94" y="106" width="52" height="20" rx="8" fill="#fff"/><rect x="174" y="106" width="52" height="20" rx="8" fill="#fff"/>'
                    '<rect x="68" y="140" width="184" height="30" rx="4" fill="#cdbfa4"/>'
                    '<rect x="0" y="170" width="320" height="30" fill="#bfa98a"/>'
                    '<g stroke="#fff" stroke-width="2"><rect x="270" y="20" width="14" height="44" rx="2" fill="#ece4d4"/><rect x="284" y="20" width="14" height="44" rx="2" fill="#d8ccb5"/><rect x="298" y="20" width="14" height="44" rx="2" fill="#b8a98d"/></g>'),

    "roof": _svg("A cream house under a terracotta roof, with matching paint chips",
                 f'<rect width="320" height="200" fill="{BG}"/>'
                 '<rect x="0" y="172" width="320" height="28" fill="#cfe0c3"/>'
                 '<polygon points="38,98 120,42 202,98" fill="#b5603f"/>'
                 '<rect x="56" y="96" width="128" height="76" fill="#e8dcc4"/>'
                 f'<rect x="108" y="128" width="24" height="44" fill="{NAVY}"/>'
                 '<rect x="70" y="110" width="26" height="22" fill="#cfe0ff" stroke="#fff" stroke-width="3"/><rect x="144" y="110" width="26" height="22" fill="#cfe0ff" stroke="#fff" stroke-width="3"/>'
                 '<rect x="226" y="38" width="64" height="32" rx="4" fill="#e8dcc4"/><rect x="226" y="80" width="64" height="32" rx="4" fill="#9fb59b"/><rect x="226" y="122" width="64" height="32" rx="4" fill="#7b8ba0"/>'
                 f'<rect x="226" y="38" width="64" height="32" rx="4" fill="none" stroke="{NAVY}" stroke-width="2"/>'
                 + _check(290, 38)),

    "style": _svg("A colonial house painted in a period red",
                  f'<rect width="320" height="200" fill="{BG}"/>'
                  '<rect x="0" y="176" width="320" height="24" fill="#cfe0c3"/>'
                  '<rect x="84" y="26" width="14" height="30" fill="#6e2c22"/><rect x="222" y="26" width="14" height="30" fill="#6e2c22"/>'
                  '<polygon points="62,62 160,30 258,62" fill="#3a3f4b"/>'
                  '<rect x="72" y="60" width="176" height="116" fill="#8c3a2e"/>'
                  + "".join(f'<rect x="{x}" y="74" width="20" height="28" fill="#d9e4f5" stroke="#fff" stroke-width="3"/>' for x in (86, 118, 150, 182, 214))
                  + "".join(f'<rect x="{x}" y="124" width="20" height="28" fill="#d9e4f5" stroke="#fff" stroke-width="3"/>' for x in (86, 118, 182, 214))
                  + f'<polygon points="144,128 160,116 176,128" fill="#fff"/><rect x="148" y="128" width="24" height="48" fill="{NAVY}"/>'),

    "wateroil": _svg("Two paint cans: water based dries faster, oil based lasts longer",
                     f'<rect width="320" height="200" fill="{BG}"/>'
                     '<path d="M100 26c6 9 11 15 11 21a11 11 0 0 1-22 0c0-6 5-12 11-21z" fill="#a9bcff"/>'
                     '<path d="M220 26c6 9 11 15 11 21a11 11 0 0 1-22 0c0-6 5-12 11-21z" fill="#d9a441"/>'
                     + _can(62, 82, BLUE, "WATER") + _can(182, 82, "#a0712c", "OIL")
                     + _label(100, 188, "Dries faster") + _label(220, 188, "Lasts longer")),

    "ac": _svg("A window AC unit dripping onto a rotting sill and peeling siding",
               _siding("#e9e4da", "#d6cebf")
               + '<rect x="104" y="18" width="112" height="94" fill="#fff"/><rect x="114" y="28" width="92" height="38" fill="#cfe0ff"/>'
               '<rect x="98" y="110" width="124" height="10" fill="#fff"/><path d="M146 110h46v10h-40z" fill="#8b6a46"/>'
               f'<rect x="122" y="68" width="76" height="42" rx="3" fill="#b9c0ca" stroke="{NAVY}" stroke-width="2"/>'
               + "".join(f'<path d="M{x} 76v26" stroke="#8d96a3" stroke-width="2"/>' for x in range(132, 192, 8))
               + "".join(f'<path d="M{x} {y}c3 5 6 8 6 11a6 6 0 0 1-12 0c0-3 3-6 6-11z" fill="#8fb3ff"/>' for x, y in ((150, 128), (172, 146), (158, 166)))
               + '<path d="M112 136l20-5 7 11-11 14-17-6z" fill="#b8ad97"/><path d="M110 134l4 6 6-2z" fill="#fff"/>'
               '<path d="M188 150l22-6 4 14-19 9z" fill="#b8ad97"/><path d="M208 142l6 4-2 6z" fill="#fff"/>'),

    "peel": _svg("Peeling paint on siding next to a can of primer",
                 _siding("#7f9db5", "#6c8aa2", 20, 16)
                 + '<rect x="0" y="176" width="320" height="24" fill="#e9e4da"/>'
                 '<path d="M30 44l38-6 10 14-8 18-34 4-10-12z" fill="#c99b6b"/><path d="M68 38l12-8 4 16z" fill="#b8cbd9"/>'
                 '<path d="M104 104l44-4 6 18-16 14-30-2z" fill="#c99b6b"/><path d="M148 100l14 2-6 14z" fill="#b8cbd9"/>'
                 '<path d="M40 128l30 2 4 22-26 6-12-14z" fill="#c99b6b"/><path d="M26 140l14-12 2 16z" fill="#b8cbd9"/>'
                 + _can(226, 96, BLUE, "PRIMER", w=70, h=80)),

    "layers": _svg("Layers: paint on top of primer on top of the surface",
                   f'<rect width="320" height="200" fill="{BG}"/>'
                   '<rect x="40" y="132" width="240" height="38" rx="3" fill="#c99b6b"/>'
                   '<path d="M150 146c30-4 60 4 90 0M150 158c36 3 70-3 110 0" stroke="#b5875a" stroke-width="2" fill="none"/>'
                   '<rect x="40" y="102" width="166" height="30" rx="3" fill="#fbfbf9" stroke="#d3defc" stroke-width="2"/>'
                   f'<rect x="40" y="72" width="120" height="30" rx="3" fill="{BLUE}"/>'
                   + _label(54, 92, "Paint", 700, 12, "#fff", "start")
                   + _label(54, 122, "Primer", 700, 12, NAVY, "start")
                   + _label(54, 156, "Surface", 700, 12, "#fff", "start")
                   + _label(170, 92, "sticks to primer", 500, 10.5, NAVY, "start")
                   + _label(216, 122, "seals and grips", 500, 10.5, NAVY, "start")),

    "spackle": _svg("Spackle works on a wall crack, not on wood trim",
                    f'<rect width="320" height="200" fill="{BG}"/>'
                    '<rect x="16" y="20" width="136" height="152" rx="6" fill="#f7f5f0"/>'
                    '<path d="M60 52l8 14-6 10 10 16-4 12" fill="none" stroke="#b9b2a5" stroke-width="2"/>'
                    '<path d="M78 92l34-24 10 8-30 30z" fill="#cfd5df"/>'
                    f'<path d="M112 68l20-14 8 8-18 16z" fill="{NAVY}"/>'
                    '<rect x="168" y="20" width="136" height="152" rx="6" fill="#f7f5f0"/>'
                    '<rect x="196" y="20" width="34" height="152" fill="#e7d6bb"/><path d="M204 30v132M214 26v140M222 34v120" stroke="#d8c3a2" stroke-width="1.5"/>'
                    '<path d="M228 90l34-24 10 8-30 30z" fill="#cfd5df"/>'
                    f'<path d="M262 66l20-14 8 8-18 16z" fill="{NAVY}"/>'
                    '<path d="M214 122c6-2 10 2 9 7s-8 6-11 2-2-8 2-9z" fill="#f2efe9" stroke="#c9c2b4"/>'
                    + _check(34, 38) + _cross(186, 38)
                    + _label(84, 192, "Walls") + _label(236, 192, "Wood trim")),

    "sheen": _svg("Sheen scale from flat to gloss, with eggshell picked out",
                  f'<rect width="320" height="200" fill="{BG}"/>'
                  + "".join(
                      f'<rect x="{18 + i * 58}" y="36" width="50" height="112" rx="4" fill="#6f86c9"/>'
                      f'<ellipse cx="{36 + i * 58}" cy="70" rx="12" ry="34" transform="rotate(-18 {36 + i * 58} 70)" fill="#fff" opacity="{op}"/>'
                      for i, op in enumerate((0, .14, .26, .38, .55)))
                  + f'<rect x="72" y="32" width="58" height="120" rx="6" fill="none" stroke="{NAVY}" stroke-width="2.5"/>'
                  + "".join(_label(43 + i * 58, 172, t, 800 if i == 1 else 500, 10.5) for i, t in enumerate(("Flat", "Eggshell", "Satin", "Semi-gloss", "Gloss")))),

    "oil": _svg("Oil-based paint: slower to dry, tough finish",
                f'<rect width="320" height="200" fill="{BG}"/>'
                + _can(122, 70, "#a0712c", "OIL")
                + f'<circle cx="60" cy="100" r="26" fill="#fff" stroke="{NAVY}" stroke-width="2.5"/><path d="M60 86v14l10 7" fill="none" stroke="{NAVY}" stroke-width="2.5" stroke-linecap="round"/>'
                + f'<path d="M260 72l22 8v16c0 14-9 24-22 30-13-6-22-16-22-30V80z" fill="{NAVY}"/><path d="M250 99l7 7 13-13" fill="none" stroke="{LB}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
                + _label(60, 150, "Slower to dry") + _label(260, 150, "Tough finish")),

    "extra": _svg("Three gallons of paint plus a small can kept for touch-ups",
                  f'<rect width="320" height="200" fill="{BG}"/>'
                  '<rect x="0" y="162" width="320" height="38" fill="#dfe6f5"/>'
                  + _can(26, 92, BLUE, "", w=56, h=70) + _can(92, 92, BLUE, "", w=56, h=70) + _can(158, 92, BLUE, "", w=56, h=70)
                  + f'<path d="M232 126h16m-8-8v16" stroke="{NAVY}" stroke-width="3" stroke-linecap="round"/>'
                  + _can(260, 122, LB, "", w=40, h=40)
                  + f'<path d="M254 92h52v18h-52z" fill="#fff" stroke="{NAVY}" stroke-width="1.5"/>' + _label(280, 105, "touch-ups", 700, 9.5)),

    "office": _svg("A bright office with white walls and ceiling",
                   '<rect width="320" height="200" fill="#fbfbf8"/>'
                   '<rect x="0" y="160" width="320" height="40" fill="#d6d2c8"/>'
                   '<rect x="58" y="0" width="64" height="8" fill="#d3defc"/><rect x="198" y="0" width="64" height="8" fill="#d3defc"/>'
                   '<polygon points="58,8 122,8 150,160 30,160" fill="#fff1c4" opacity=".55"/><polygon points="198,8 262,8 290,160 170,160" fill="#fff1c4" opacity=".55"/>'
                   '<rect x="136" y="44" width="48" height="64" fill="#cfe0ff" stroke="#e6e9f2" stroke-width="3"/>'
                   f'<rect x="36" y="128" width="96" height="6" fill="{NAVY}"/><rect x="44" y="134" width="5" height="26" fill="{NAVY}"/><rect x="119" y="134" width="5" height="26" fill="{NAVY}"/><rect x="70" y="108" width="30" height="20" rx="2" fill="#2b3550"/>'
                   f'<rect x="188" y="128" width="96" height="6" fill="{NAVY}"/><rect x="196" y="134" width="5" height="26" fill="{NAVY}"/><rect x="271" y="134" width="5" height="26" fill="{NAVY}"/><rect x="222" y="108" width="30" height="20" rx="2" fill="#2b3550"/>'),
}


# Featured demo: the same wall under daylight, a cool white bulb and a warm bulb (CSS switches the tint).
LIGHT_DEMO = _svg("A living room wall that changes tone with the light", (
    '<rect class="demo-wall" width="480" height="300" fill="#d5c8ae"/>'
    '<rect class="demo-window" x="304" y="46" width="124" height="134" fill="#cfe4ff"/>'
    '<path d="M366 46v134M304 113h124" stroke="#fff" stroke-width="5"/><rect x="304" y="46" width="124" height="134" fill="none" stroke="#fff" stroke-width="7"/>'
    '<rect x="96" y="58" width="120" height="76" fill="#fff"/><rect x="104" y="66" width="104" height="60" fill="#e9dcc6"/><path d="M112 118l26-28 16 16 14-11 32 23z" fill="#9fb59b"/>'
    '<rect x="0" y="240" width="480" height="60" fill="#b98d62"/>'
    '<rect x="60" y="168" width="196" height="62" rx="14" fill="#3a4660"/><rect x="48" y="186" width="28" height="56" rx="10" fill="#3a4660"/><rect x="240" y="186" width="28" height="56" rx="10" fill="#3a4660"/>'
    '<rect x="70" y="150" width="84" height="34" rx="12" fill="#4a5774"/><rect x="162" y="150" width="84" height="34" rx="12" fill="#4a5774"/>'
    '<filter id="demo-soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>'
    '<circle class="demo-glow" cx="292" cy="146" r="40" filter="url(#demo-soft)"/>'
    f'<path d="M292 158v82M276 240h32" stroke="{NAVY}" stroke-width="4" stroke-linecap="round"/><path d="M272 126h40l8 30h-56z" fill="#efe6d6"/>'
    '<rect class="demo-tint" width="480" height="300"/>'
), vb="0 0 480 300")
