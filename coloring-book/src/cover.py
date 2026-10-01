"""Full-colour cover: front, back, and the KDP paperback wraparound."""
from ink import *
import ink
from critters import critter
from props import *
import scenes
import page
import re
import sys as _sys
import os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "brand"))
import logo

AUTHOR = "Diamond Spade"


def embed(svg_str, x, y, w):
    """Place a standalone logo SVG at (x, y) scaled to width w."""
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_str)
    vw, vh = float(vb.group(1)), float(vb.group(2))
    inner = svg_str[svg_str.index(">") + 1: svg_str.rindex("</svg>")]
    raw(f'<g transform="translate({x} {y}) scale({w / vw:.4f})">{inner}</g>')
    return w * vh / vw


def author_line(cx, y, size=26):
    """small gold faceted spade + 'by Diamond Spade', centred on cx"""
    label = f"by {AUTHOR}"
    tw = size * 0.5 * len(label)
    k = size * 1.25 / 200
    x0 = cx - (tw + 200 * k * 0.9 + 10) / 2
    raw(f'<g transform="translate({x0 + 90 * k:.1f} {y - size * 0.36:.1f}) scale({k:.4f})">{logo.icon()}</g>')
    plain_text(x0 + 180 * k + 10, y, label, size, INK, 700, "start")

BLEED = 12.5            # 0.125 in
CREAM = "#fff3e4"
PINK = "#f9a8be"
ROSE = "#ef7d9c"
MINT = "#a9e3d1"
TEAL = "#4fb79f"
SKY = "#c4e8f8"
BUTTER = "#ffe28c"
PEACH = "#ffcaa6"
LAV = "#d3c1f3"
GRASS = "#9fd88a"
LEAF = "#78c267"
BROWN = "#cf9a6e"
TAN = "#f1d3b0"
FROG = "#a5dc84"
WHITE = "#ffffff"


def big_text(x, y, s, size, fill, w=9, shadow=7, anchor="middle"):
    style = f'font-family="Baloo 2" font-weight="800" font-size="{size}" text-anchor="{anchor}"'
    raw(f'<text x="{x}" y="{y + shadow}" {style} fill="{INK}" stroke="{INK}" '
        f'stroke-width="{w * 2}" stroke-linejoin="round">{s}</text>')
    raw(f'<text x="{x}" y="{y}" {style} fill="{INK}" stroke="{INK}" '
        f'stroke-width="{w * 2}" stroke-linejoin="round">{s}</text>')
    raw(f'<text x="{x}" y="{y}" {style} fill="{fill}">{s}</text>')


def plain_text(x, y, s, size, fill=INK, weight=700, anchor="middle"):
    raw(f'<text x="{x}" y="{y}" font-family="Baloo 2" font-weight="{weight}" font-size="{size}" '
        f'text-anchor="{anchor}" fill="{fill}">{s}</text>')


def confetti(seed, x0, y0, x1, y1, n=40):
    import random
    rnd = random.Random(seed)
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        col = rnd.choice(["#ffd9e2", "#d9f2ea", "#ffeec2", "#e6dcfa"])
        k = rnd.random()
        if k < 0.4:
            raw(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(4, 8):.1f}" fill="{col}"/>')
        elif k < 0.7:
            with T(x, y, rnd.uniform(0.5, 0.8), rnd.uniform(-20, 20)):
                P("M0 14 C-30 -6 -22 -30 -6 -24 C-2 -22 0 -18 0 -16 C0 -18 2 -22 6 -24 "
                  "C22 -30 30 -6 0 14 Z", col, 0)
        else:
            with T(x, y, rnd.uniform(0.7, 1.1)):
                P("M0 -16 Q2 -2 16 0 Q2 2 0 16 Q-2 2 -16 0 Q-2 -2 0 -16 Z", col, 0)


def ribbon(cx, cy, w_, h, label, fill=TEAL, size=40):
    with Tint(fill):
        for sd in (-1, 1):
            ex = cx + sd * (w_ / 2 + 10)
            poly([(ex - sd * 40, cy - h / 2 + 14), (ex + sd * 46, cy - h / 2 + 14),
                  (ex + sd * 26, cy + 14), (ex + sd * 46, cy + h / 2 + 14), (ex - sd * 40, cy + h / 2 + 14)])
        P(f"M{cx - w_ / 2} {cy - h / 2} Q{cx} {cy - h / 2 - 18} {cx + w_ / 2} {cy - h / 2} "
          f"L{cx + w_ / 2} {cy + h / 2} Q{cx} {cy + h / 2 - 18} {cx - w_ / 2} {cy + h / 2} Z")
    raw(f'<text x="{cx}" y="{cy + size * 0.33}" font-family="Baloo 2" font-weight="800" '
        f'font-size="{size}" text-anchor="middle" fill="#ffffff">{label}</text>')


def front():
    R(-BLEED - 2, -BLEED - 2, 850 + 2 * BLEED + 4, 1100 + 2 * BLEED + 4, 0, CREAM, 0)
    confetti(7, 0, 0, 850, 1100, 60)
    # title
    author_line(425, 72)
    big_text(425, 196, "Cozy Little", 124, PINK)
    big_text(425, 330, "World", 150, BUTTER)
    with Tint(PINK):
        heart(632, 252, 1.25, 15)
    with Tint(MINT):
        sparkle(170, 262, 1.9, W)
    ribbon(425, 396, 560, 62, "24 Cute &amp; Easy Coloring Pages", TEAL, 38)

    # illustration
    C(425, 790, 345, SKY, W)
    with Clip("M80 790 A345 345 0 0 1 770 790 Z"):
        with Tint(WHITE):
            cloud(645, 585, 0.8, face=True)
        with Tint(BUTTER, PEACH):
            sun(235, 580, 0.68)
    with Tint(GRASS):
        P("M-30 905 C150 845 300 860 425 880 C560 900 700 850 880 880 L880 1140 L-30 1140 Z")
    with Tint(PINK, BUTTER):
        for fx, fy in ((70, 930), (780, 920), (740, 1000)):
            flower(fx, fy, 20)
    with Tint(LAV, BUTTER):
        flower(110, 1010, 16)
    with Tint(PEACH, WHITE):
        mushroom(800, 980, 0.6)
    critter("bear", 205, 770, 1.15, expr="joy", m="open", pose="hold",
            colors={"body": BROWN, "detail": TAN, "prop": PEACH, "prop2": PINK, "outfit": MINT},
            hold=lambda: cupcake(0, 116, 0.55, cherry=True), wear=["scarf"])
    critter("cat", 648, 776, 1.12, expr="happy", m="w", pose="hold",
            colors={"body": "#f6f0ea", "detail": PINK, "prop": LAV, "prop2": WHITE, "hat": ROSE},
            hold=lambda: teacup(0, 112, 0.6), hat="bow")
    critter("bunny", 425, 700, 1.45, expr="happy", m="w", pose="hold",
            colors={"body": "#fffaf5", "detail": PINK, "prop": PINK, "prop2": WHITE,
                    "outfit": BUTTER, "outfit2": PEACH},
            hold=lambda: mug(0, 84, 0.78, deco="heart", steamy=False), wear=["sweater"])
    with Tint(PINK):
        heart(330, 470, 0.9, -15, D); heart(540, 455, 0.7, 15, D)
    with Tint(BUTTER):
        star(120, 640, 0.8, -10); star(745, 470, 0.7, 12)
    # tagline pill
    R(115, 1010, 620, 58, 29, WHITE, W)
    plain_text(425, 1049, "Relaxing Kawaii Scenes for Adults &amp; Teens", 27, INK, 800)


def back():
    R(-BLEED - 2, -BLEED - 2, 850 + 2 * BLEED + 4, 1100 + 2 * BLEED + 4, 0, CREAM, 0)
    confetti(11, 0, 0, 850, 1100, 50)
    big_text(425, 130, "Welcome to a", 62, MINT, 6, 5)
    big_text(425, 215, "Cozy Little World!", 74, PINK, 7, 5)
    lines = [
        "Brew a cup of tea, grab your favorite pencils and slow down",
        "with 24 sweet, easy-to-color scenes full of adorable animal friends.",
    ]
    for i, l in enumerate(lines):
        plain_text(425, 280 + i * 36, l, 27, INK, 600)
    # sample pages
    picks = [2, 0, 9]
    for k, idx in enumerate(picks):
        cx = 200 + k * 225
        rot = (-6, 0, 6)[k]
        with T(cx, 545, 1, rot):
            R(-106, -131, 212, 262, 12, WHITE, W)
            k = 0.27
            with T(-425 * k, -127 - 70 * k + 8, k):
                with Thumb():
                    with Clip(page.FRAME):
                        scenes.SCENES[idx][1]()
                    P(page.FRAME, "none", W)
    feats = ["24 original one-sided illustrations",
             "Bold, clean lines – no tiny fiddly details",
             "Cafés, bakeries, picnics, rainy days &amp; bedtime",
             "Blank backs to stop marker bleed-through",
             "Large 8.5 x 11 in pages"]
    for i, f in enumerate(feats):
        y = 750 + i * 46
        with Tint(PINK):
            heart(130, y - 8, 0.75, 0, D)
        plain_text(160, y, f, 28, INK, 700, "start")
    # barcode safe zone (KDP prints the barcode here)
    R(850 - 25 - 200, 1100 - 25 - 120, 200, 120, 0, WHITE, 0)
    # publisher mark
    R(45, 965, 370, 95, 0, CREAM, 0)
    embed(logo.horizontal(logo.NAVY), 60, 975, 340)


def front_svg():
    ink.reset()
    with T(BLEED, BLEED):
        front()
    return page.svg_doc(ink.take(), 850 + 2 * BLEED, 1100 + 2 * BLEED, CREAM)


def front_trim_svg():
    ink.reset()
    front()
    return page.svg_doc(ink.take(), 850, 1100, CREAM)


def wrap_svg(page_count):
    spine = page_count * 0.2252          # KDP white paper: 0.002252 in / page
    W_ = 2 * BLEED + 850 * 2 + spine
    H_ = 1100 + 2 * BLEED
    ink.reset()
    with Clip(f"M0 0 H{W_} V{H_} H0 Z"):
        with T(BLEED, BLEED):
            back()
        with Clip(f"M{BLEED + 850} 0 H{W_} V{H_} H{BLEED + 850} Z"):
            with T(BLEED + 850 + spine, BLEED):
                front()
    return page.svg_doc(ink.take(), W_, H_, CREAM), W_ / 100, H_ / 100, spine / 100
