"""Diamond Spade logo: a spade cut like a brilliant diamond, with a
letterspaced serif wordmark. Text is converted to outlines so the SVGs
render identically everywhere (no font needed).

    python3 logo.py      -> writes SVG / PNG / PDF variants next to this file
"""
import os

import cairosvg
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib import instancer

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "CormorantGaramond.ttf")

NAVY = "#13203a"
IVORY = "#fbf7ee"
GOLD = {"hi": "#f3e2ab", "lt": "#e2c477", "md": "#c9a44c", "dk": "#a07a2c", "dd": "#7d5c1c"}

# Spade silhouette, centred on (0, 0), ~200 tall.
SPADE = ("M0 -100 C22 -62 92 -34 90 14 C88 58 44 70 14 44 C18 70 28 88 44 100 "
         "L-44 100 C-28 88 -18 70 -14 44 C-44 70 -88 58 -90 14 C-92 -34 -22 -62 0 -100 Z")

_font_cache = {}


def _font(weight):
    if weight not in _font_cache:
        _font_cache[weight] = instancer.instantiateVariableFont(TTFont(FONT), {"wght": weight})
    return _font_cache[weight]


def text_path(s, size, tracking=0.0, weight=600):
    """Return (svg path d, width) for s set in Cormorant Garamond."""
    f = _font(weight)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    k = size / f["head"].unitsPerEm
    x = 0.0
    d = []
    for ch in s:
        g = cmap.get(ord(ch))
        if g is None:
            continue
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x, 0)))
        d.append(pen.getCommands())
        x += gs[g].width * k + tracking * size
    return " ".join(d), x - tracking * size


def icon(colorway="gold", outline=None):
    """The faceted spade. colorway: gold | mono:<color>"""
    if colorway.startswith("mono"):
        c = colorway.split(":")[1]
        bg = NAVY if c == IVORY else IVORY
        out = [f'<path d="{SPADE}" fill="{c}"/>']
        # facet lines knocked out of the solid shape
        out.append(f'<g clip-path="url(#spclip)" stroke="{bg}" stroke-width="3.2" fill="none" '
                   f'stroke-linejoin="round">' + _facet_lines() + "</g>")
    else:
        out = [f'<path d="{SPADE}" fill="{GOLD["md"]}"/>',
               '<g clip-path="url(#spclip)">' + _facets() + "</g>",
               f'<g clip-path="url(#spclip)" stroke="{GOLD["dd"]}" stroke-width="1.6" fill="none" '
               f'stroke-linejoin="round" opacity="0.55">' + _facet_lines() + "</g>",
               f'<path d="{SPADE}" fill="none" stroke="{outline or GOLD["dd"]}" stroke-width="2.4"/>']
    return (f'<defs><clipPath id="spclip"><path d="{SPADE}"/></clipPath></defs>' + "".join(out))


# brilliant-cut geometry inside the spade: crown above the girdle (y=14),
# pavilion below converging on the culet (0, 52), stem below that.
_G = 14
_CROWN = [(-100, _G), (-62, _G), (-26, _G), (0, _G), (26, _G), (62, _G), (100, _G)]
_TABLE = [(-30, -30), (30, -30)]


def _facets():
    p = []
    tri = lambda pts, c: p.append('<path d="M' + " L".join(f"{x} {y}" for x, y in pts) + f' Z" fill="{c}"/>')
    T, (tl, tr) = (0, -100), _TABLE
    # table + star facets (crown)
    tri([tl, tr, (0, _G)], GOLD["hi"])
    tri([T, tl, tr], GOLD["lt"])
    tri([T, (-100, -40), tl], GOLD["md"])
    tri([T, (100, -40), tr], GOLD["lt"])
    tri([(-100, -40), tl, (-62, _G)], GOLD["lt"])
    tri([(-100, -40), (-100, _G), (-62, _G)], GOLD["dk"])
    tri([tl, (-62, _G), (0, _G)], GOLD["md"])
    tri([(100, -40), tr, (62, _G)], GOLD["md"])
    tri([(100, -40), (100, _G), (62, _G)], GOLD["lt"])
    tri([tr, (62, _G), (0, _G)], GOLD["lt"])
    # pavilion
    cul = (0, 52)
    shades = [GOLD["dk"], GOLD["md"], GOLD["lt"], GOLD["hi"], GOLD["md"], GOLD["dk"]]
    for i in range(6):
        tri([_CROWN[i], _CROWN[i + 1], cul], shades[i])
    tri([(-100, _G), cul, (-100, 100)], GOLD["dd"])
    tri([(100, _G), cul, (100, 100)], GOLD["dk"])
    # stem
    tri([cul, (-60, 110), (0, 110)], GOLD["md"])
    tri([cul, (0, 110), (60, 110)], GOLD["dk"])
    return "".join(p)


def _facet_lines():
    T, (tl, tr) = (0, -100), _TABLE
    segs = [(T, tl), (T, tr), (tl, tr), (tl, (0, _G)), (tr, (0, _G)), ((-100, -40), tl),
            ((100, -40), tr), (tl, (-62, _G)), (tr, (62, _G)), ((-100, _G), (100, _G))]
    segs += [(c, (0, 52)) for c in _CROWN[1:-1]]
    return "".join(f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}"/>' for a, b in segs)


def sparkle(x, y, r, c):
    return (f'<path transform="translate({x} {y})" fill="{c}" d="M0 {-r} Q{r * .12} {-r * .12} {r} 0 '
            f'Q{r * .12} {r * .12} 0 {r} Q{-r * .12} {r * .12} {-r} 0 Q{-r * .12} {-r * .12} 0 {-r} Z"/>')


def svg(w, h, body, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f"{rect}{body}</svg>")


def stacked(text_col, icon_way="gold", bg=None, rule=GOLD["md"]):
    W, H = 1000, 700
    _, nw = text_path("DIAMOND SPADE", 100, 0.2, 600)
    name, nw = text_path("DIAMOND SPADE", 100 * 800 / nw, 0.2, 600)
    body = (f'<g transform="translate({W / 2} 250) scale(1.6)">{icon(icon_way)}</g>'
            + sparkle(W / 2 + 118, 118, 16, rule)
            + f'<path transform="translate({(W - nw) / 2} 545)" d="{name}" fill="{text_col}"/>'
            + f'<rect x="{W / 2 - 60}" y="595" width="120" height="2.6" fill="{rule}"/>'
            + sparkle(W / 2, 596, 9, rule))
    return svg(W, H, body, bg)


def horizontal(text_col, icon_way="gold", bg=None):
    name, nw = text_path("DIAMOND SPADE", 80, 0.2, 600)
    W, H = int(nw + 370), 300
    body = (f'<g transform="translate(150 150) scale(1.12)">{icon(icon_way)}</g>'
            + f'<rect x="282" y="70" width="2.4" height="160" fill="{GOLD["md"]}"/>'
            + f'<path transform="translate(320 178)" d="{name}" fill="{text_col}"/>')
    return svg(W, H, body, bg)


def icon_only(icon_way="gold", bg=None):
    return svg(300, 300, f'<g transform="translate(150 150) scale(1.15)">{icon(icon_way)}</g>', bg)


def main():
    out = os.path.join(HERE, "diamond-spade")
    os.makedirs(out, exist_ok=True)
    variants = {
        "logo-stacked": stacked(NAVY),
        "logo-stacked-on-navy": stacked(IVORY, bg=NAVY),
        "logo-stacked-black": stacked("#111111", "mono:#111111", rule="#111111"),
        "logo-horizontal": horizontal(NAVY),
        "logo-horizontal-on-navy": horizontal(IVORY, bg=NAVY),
        "icon": icon_only(),
        "icon-on-navy": icon_only(bg=NAVY),
        "icon-black": icon_only("mono:#111111"),
        "icon-white": icon_only("mono:" + IVORY, bg=NAVY),
    }
    for name, s in variants.items():
        with open(os.path.join(out, name + ".svg"), "w") as f:
            f.write(s)
        cairosvg.svg2png(bytestring=s.encode(), write_to=os.path.join(out, name + ".png"),
                         output_width=2000 if "icon" not in name else 1024)
    cairosvg.svg2pdf(bytestring=variants["logo-stacked"].encode(),
                     write_to=os.path.join(out, "logo-stacked.pdf"))
    cairosvg.svg2pdf(bytestring=variants["logo-horizontal"].encode(),
                     write_to=os.path.join(out, "logo-horizontal.pdf"))
    print("wrote", len(variants), "variants to", out)


if __name__ == "__main__":
    main()
