#!/usr/bin/env python3
"""Vector redraw of the James Skipper Painting logo.

Traced from the only copy available, the 180x180 Facebook profile picture
(assets-src/fb-logo-180.png). Shapes and letter positions follow that image pixel
for pixel; type is outlined from Oswald (bold condensed) and Montserrat (regular),
both SIL Open Font License. Ask the client for the original file before launch.

Usage: python3 tools/logo.py <site-dir>
"""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
FONTS = os.path.join(OUT, "assets-src", "fonts")
BLUE = "#476ef0"   # sampled from the logo
BLACK = "#000000"
Y0 = 52            # top of the traced artwork in the 180px source

# Paint roller (source pixel coordinates, y shifted by Y0)
def y(v):
    return v - Y0

ROLLER = [
    # roller cover: narrow neck under the frame, then the full cylinder, rounded at the bottom
    f"M6 {y(58)} L13 {y(58)} C15 {y(61)} 18 {y(63)} 18 {y(66)} L18 {y(121)} C18 {y(125)} 15 {y(127.5)} 9 {y(127.5)} "
    f"C3 {y(127.5)} 0 {y(125)} 0 {y(121)} L0 {y(66)} C0 {y(63)} 4 {y(61)} 6 {y(58)} Z",
    # frame: top bar, diagonal arm, ferrule
    f"M6.5 {y(53)} L23.5 {y(53)} C27 {y(53)} 28.5 {y(54.5)} 30.5 {y(56.5)} L53 {y(77.2)} L65.5 {y(77.2)} "
    f"C67 {y(77.2)} 67.5 {y(78.5)} 67.5 {y(80)} C67.5 {y(81.5)} 66 {y(82.8)} 64 {y(82.8)} L54 {y(82.8)} "
    f"C51.5 {y(82.8)} 50 {y(81.8)} 48.5 {y(80.5)} L26 {y(59.5)} C25 {y(58.5)} 24 {y(58)} 22.5 {y(58)} L6.5 {y(58)} Z",
    # handle grip
    f"M72 {y(74)} L115.5 {y(74)} C117.5 {y(74)} 118.5 {y(76)} 118.5 {y(79.5)} C118.5 {y(83)} 117.5 {y(85.5)} 115.5 {y(85.5)} "
    f"L72 {y(85.5)} C70 {y(85.5)} 69 {y(83)} 69 {y(79.5)} C69 {y(76)} 70 {y(74)} 72 {y(74)} Z",
]


def font(name, wght):
    f = TTFont(os.path.join(FONTS, name))
    return instantiateVariableFont(f, {"wght": wght})


def glyph_paths(f, text, x_positions=None, x_left=None, x_right=None, cap_top=None, cap_bottom=None, track=0):
    """Outline `text`, scaled so cap height spans cap_top..cap_bottom.
    Either place each letter at x_positions, or fit the whole word between x_left and x_right."""
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    cap = f["OS/2"].sCapHeight
    s = (cap_bottom - cap_top) / cap
    names = [cmap[ord(c)] for c in text]
    adv = [gs[n].width for n in names]
    paths = []
    if x_positions is None:
        # natural width with tracking, then stretch horizontally to fit
        widths = [a * s for a in adv]
        natural = sum(widths) + track * (len(text) - 1)
        sx = (x_right - x_left) / natural
        x = x_left
        for n, w, c in zip(names, widths, text):
            if c != " ":
                paths.append((n, x, sx * s))
            x += (w + track) * sx
    else:
        for n, x, c in zip(names, x_positions, text):
            paths.append((n, x, s))
    out = []
    for n, x, sxx in paths:
        # left-align each glyph's ink (not its side bearing) on x
        bp = BoundsPen(gs)
        gs[n].draw(bp)
        xmin = bp.bounds[0] if bp.bounds else 0
        pen = SVGPathPen(gs)
        tp = TransformPen(pen, (sxx, 0, 0, -s, x - xmin * sxx, cap_bottom))
        gs[n].draw(tp)
        out.append(pen.getCommands())
    return " ".join(out)


def build():
    oswald = font("Oswald.ttf", 700)
    mont = font("Montserrat.ttf", 400)
    # JAMES SKIPPER: ink from x=29 to x=180, caps y=91..110 in the source
    name = glyph_paths(oswald, "JAMES SKIPPER", x_left=29.5, x_right=179.5, cap_top=y(90.6), cap_bottom=y(110.6), track=0.9)
    # PAINTING: letter-spaced, each letter's left edge measured from the source
    word = glyph_paths(mont, "PAINTING", x_positions=[29, 48, 69, 86, 105, 125, 142, 160.5], cap_top=y(113.2), cap_bottom=y(124.6))
    roller = "".join(f'<path d="{d}"/>' for d in ROLLER)
    w, h = 181, y(129)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -1 {w + 1} {h + 1}" width="{(w + 1) * 4}" height="{(h + 1) * 4}" role="img" aria-label="James Skipper Painting">'
           f'<g fill="{BLUE}">{roller}</g><path fill="{BLACK}" d="{name}"/><path fill="{BLACK}" d="{word}"/></svg>')
    mark = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -4 132 84" width="512" height="512" preserveAspectRatio="xMidYMid meet">'
            f'<g fill="{BLUE}">{roller}</g></svg>')
    os.makedirs(os.path.join(OUT, "assets", "img"), exist_ok=True)
    with open(os.path.join(OUT, "assets", "img", "logo.svg"), "w") as fh:
        fh.write(svg)
    with open(os.path.join(OUT, "assets-src", "logo-mark.svg"), "w") as fh:
        fh.write(mark)
    print("wrote assets/img/logo.svg", f"viewBox {w + 1}x{h + 1}")


if __name__ == "__main__":
    build()
