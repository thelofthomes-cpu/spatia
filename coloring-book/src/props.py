"""Cozy props. Unless noted, each prop is drawn around its own origin
(centre for small items, bottom-centre for things that stand on a surface)
and placed with x, y, s (scale) and r (rotation)."""
from ink import *
from critters import flower


# ================================================================ sky & decor
def cloud(x, y, s=1.0, face=None):
    with T(x, y, s):
        P(scallop([(-70, 20), (-80, -6), (-48, -30), (-10, -44), (30, -34), (62, -18),
                   (78, 12), (60, 26)], 0.58))
        if face == "sleep":
            S("M-26 0 Q-18 7 -10 0 M10 0 Q18 7 26 0", F + .6)
            S("M-4 12 Q0 15 4 12", F)
        elif face:
            E(-17, 0, 4.5, 6, INK, 0); E(17, 0, 4.5, 6, INK, 0)
            S("M-6 10 Q0 16 6 10", F)


def sun(x, y, s=1.0, face=True):
    with T(x, y, s):
        for i in range(10):
            with T(0, 0, 1, i * 36):
                P("M0 -58 Q-9 -70 0 -84 Q9 -70 0 -58 Z")
        C(0, 0, 50)
        if face:
            E(-16, -4, 5, 6.5, INK, 0); E(16, -4, 5, 6.5, INK, 0)
            S("M-8 12 Q0 20 8 12", F + .5)
            E(-30, 12, 8, 5, PAPER, F); E(30, 12, 8, 5, PAPER, F)


def moon(x, y, s=1.0, face=True, r=0):
    with T(x, y, s, r):
        P("M10 -80 A80 80 0 1 0 70 50 A64 64 0 1 1 10 -80 Z")
        if face:
            S("M-34 6 Q-26 14 -18 6", D)
            S("M-12 34 Q-4 40 4 32", F + .5)
            E(-40, 26, 9, 5, PAPER, F)


def star(x, y, s=1.0, r=0, w=W):
    with T(x, y, s, r):
        P(smooth(star_pts(0, 0, 22, 11), True, 0.35), PAPER, w)


def sparkle(x, y, s=1.0, w=D):
    with T(x, y, s):
        P("M0 -16 Q2 -2 16 0 Q2 2 0 16 Q-2 2 -16 0 Q-2 -2 0 -16 Z", PAPER, w)


def heart(x, y, s=1.0, r=0, w=W):
    with T(x, y, s, r):
        P("M0 14 C-30 -6 -22 -30 -6 -24 C-2 -22 0 -18 0 -16 C0 -18 2 -22 6 -24 "
          "C22 -30 30 -6 0 14 Z", PAPER, w)


def raindrop(x, y, s=1.0, w=D):
    with T(x, y, s):
        P("M0 -14 C6 -4 10 2 10 6 A10 10 0 0 1 -10 6 C-10 2 -6 -4 0 -14 Z", PAPER, w)


def note(x, y, s=1.0, r=0):
    with T(x, y, s, r):
        E(-8, 14, 9, 7, PAPER, D, -20)
        L(0, 12, 0, -18, D)
        S("M0 -18 Q12 -12 14 -2", D)


def bunting(x1, y1, x2, y2, n=7, sag=40):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + sag
    S(f"M{x1} {y1} Q{mx} {my + sag} {x2} {y2}", D)
    for i in range(n):
        t = (i + 0.5) / n
        bx = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * mx + t * t * x2
        by = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * (my + sag) + t * t * y2
        poly([(bx - 20, by - 2), (bx + 20, by - 2), (bx, by + 36)], True, PAPER, D)


def string_lights(x1, y1, x2, y2, n=8, sag=50):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + sag
    S(f"M{x1} {y1} Q{mx} {my + sag} {x2} {y2}", F)
    for i in range(n):
        t = (i + 0.5) / n
        bx = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * mx + t * t * x2
        by = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * (my + sag) + t * t * y2
        with T(bx, by, 1, (-12 if i % 2 else 12)):
            R(-6, -2, 12, 10, 2, PAPER, F)
            P("M-9 8 C-12 26 12 26 9 8 Z", PAPER, D)


# ================================================================ food & drink
def steam(x, y, s=1.0):
    with T(x, y, s):
        for dx in (-14, 0, 14):
            S(f"M{dx} 0 C{dx - 8} -10 {dx + 8} -18 {dx} -28 C{dx - 8} -38 {dx + 6} -44 {dx} -52", F + .6)


def mug(x, y, s=1.0, r=0, deco="heart", steamy=True, cocoa=False, flip=False):
    """origin: centre of mug"""
    with T(x, y, s, r, flip):
        tube("M26 -14 C50 -16 52 18 26 16", 10)
        P("M-30 -32 L30 -32 L28 24 Q28 34 18 34 L-18 34 Q-28 34 -28 24 Z")
        E(0, -32, 30, 8)
        if cocoa:
            for mx, my in ((-12, -38), (8, -40), (-2, -32), (16, -33)):
                R(mx - 8, my - 7, 16, 14, 4, PAPER, F, (mx * 3) % 40)
        if deco == "heart":
            heart(0, 2, 0.7, 0, D)
        elif deco == "paw":
            E(0, 8, 9, 7, PAPER, D)
            for px, py in ((-11, -6), (-4, -12), (4, -12), (11, -6)):
                C(px, py, 3.6, PAPER, F)
        elif deco == "stripes":
            L(-29, -8, 29, -8, F); L(-28, 12, 28, 12, F)
        if steamy:
            steam(0, -48, 0.9)


def teacup(x, y, s=1.0):
    """origin: on the table (saucer bottom)"""
    with T(x, y, s):
        E(0, -4, 44, 9)
        tube("M28 -30 C46 -32 46 -12 24 -14", 8)
        P("M-32 -40 Q-30 -6 0 -6 Q30 -6 32 -40 Z")
        E(0, -40, 32, 7)
        flower(0, -24, 9, 5, F)


def teapot(x, y, s=1.0):
    """origin: bottom centre"""
    with T(x, y, s):
        tube("M44 -60 C80 -64 80 -10 44 -20", 12)
        P("M-46 -40 C-70 -46 -80 -70 -86 -78 C-74 -76 -66 -64 -50 -60 Z")
        P("M-56 -46 C-60 -86 60 -86 56 -46 C60 -10 30 0 0 0 C-30 0 -60 -10 -56 -46 Z")
        P("M-34 -80 Q0 -96 34 -80 Q0 -72 -34 -80 Z")
        C(0, -94, 9)
        heart(0, -40, 0.9, 0, D)
        S("M-50 -62 Q0 -54 50 -62", F)


def cupcake(x, y, s=1.0, cherry=True, deco="sprinkles"):
    """origin: bottom centre"""
    with T(x, y, s):
        P("M-36 -44 L36 -44 L28 0 L-28 0 Z")
        for i in (-18, -6, 6, 18):
            L(i * 1.15, -42, i, -3, F)
        P(scallop([(-44, -42), (-40, -64), (-20, -80), (0, -92), (20, -80), (40, -64), (44, -42)],
                  0.6, closed=False) + " Q0 -36 -44 -42 Z")
        if cherry:
            S("M4 -100 Q10 -116 20 -118", D)
            C(0, -98, 10)
        if deco == "sprinkles":
            for sx, sy, a in ((-22, -60, 30), (-6, -70, -20), (16, -62, 50), (24, -50, -10), (-30, -50, 70), (4, -54, 10)):
                R(sx - 5, sy - 2, 10, 4.5, 2, PAPER, F - .8, a)


def cake(x, y, s=1.0, candles=3, strawberries=True):
    """layer cake on a stand; origin: bottom of stand"""
    with T(x, y, s):
        P("M-20 0 L20 0 L12 -24 L-12 -24 Z")
        E(0, -26, 96, 12)
        R(-80, -110, 160, 80, 14)
        S(wavy_line(-80, 80, -78, 6, 8), D)
        R(-70, -170, 140, 64, 12)
        P("M-70 -166 Q-70 -172 -60 -172 L60 -172 Q70 -172 70 -166 L70 -150 Q61.2 -134 52.5 -150 Q43.8 -134 35.0 -150 Q26.2 -134 17.5 -150 Q8.8 -134 0.0 -150 Q-8.8 -134 -17.5 -150 Q-26.2 -134 -35.0 -150 Q-43.8 -134 -52.5 -150 Q-61.2 -134 -70.0 -150 Z", PAPER, D)
        if strawberries:
            for sx in (-50, 0, 50):
                strawberry(sx, -184, 0.55)
        for i in range(candles):
            cx = -40 + i * 40 if candles > 1 else 0
            R(cx - 7, -238, 14, 46, 4)
            S(f"M{cx - 6} -226 L{cx + 6} -232 M{cx - 6} -212 L{cx + 6} -218", F)
            P(f"M{cx} -262 C{cx + 12} -250 {cx + 8} -240 {cx} -240 C{cx - 8} -240 {cx - 12} -250 {cx} -262 Z")


def strawberry(x, y, s=1.0, r=0):
    with T(x, y, s, r):
        P("M0 40 C-30 30 -38 0 -30 -14 C-20 -26 20 -26 30 -14 C38 0 30 30 0 40 Z")
        P(smooth(star_pts(0, -20, 22, 9, 5, -90), True, 0.2), PAPER, D)
        for px, py in ((-12, -2), (10, 0), (0, 12), (-14, 16), (14, 16), (0, 26), (0, -6)):
            E(px, py, 2.2, 3.4, INK, 0)


def apple(x, y, s=1.0, r=0):
    with T(x, y, s, r):
        P("M0 -26 C20 -40 46 -26 42 4 C38 34 14 42 0 34 C-14 42 -38 34 -42 4 C-46 -26 -20 -40 0 -26 Z")
        S("M0 -26 Q2 -40 8 -46", D)
        P("M6 -40 C14 -56 34 -54 36 -46 C26 -38 14 -36 6 -40 Z", PAPER, D)
        S("M-26 -10 Q-28 4 -22 14", F)


def lemon(x, y, s=1.0, r=0):
    with T(x, y, s, r):
        P("M-36 0 C-40 -6 -36 -10 -32 -10 C-22 -30 22 -30 32 -10 C36 -10 40 -6 36 0 "
          "C40 6 36 10 32 10 C22 30 -22 30 -32 10 C-36 10 -40 6 -36 0 Z")
        S("M-16 -10 Q-8 -16 4 -16", F)


def lemon_slice(x, y, s=1.0):
    with T(x, y, s):
        C(0, 0, 24); C(0, 0, 17, PAPER, F)
        for i in range(6):
            a = math.radians(i * 60)
            L(0, 0, 16 * math.cos(a), 16 * math.sin(a), F)


def carrot(x, y, s=1.0, r=0):
    with T(x, y, s, r):
        for a in (-30, 0, 30):
            with T(0, -38, 1, a):
                P("M0 0 C-10 -14 -8 -30 0 -40 C8 -30 10 -14 0 0 Z", PAPER, D)
        P("M-20 -36 Q0 -46 20 -36 C18 0 6 40 0 48 C-6 40 -18 0 -20 -36 Z")
        S("M-16 -16 L-6 -14 M8 0 L16 -2 M-10 18 L-2 20", F)


def croissant(x, y, s=1.0, r=0):
    with T(x, y, s, r):
        for cx, cy, rx, ry, a in ((-64, 8, 15, 20, -62), (64, 8, 15, 20, 62), (-40, -12, 21, 29, -36),
                                  (40, -12, 21, 29, 36), (0, -22, 27, 36, 0)):
            E(cx, cy, rx, ry, PAPER, W, a)


def bread(x, y, s=1.0, r=0):
    """round loaf, origin bottom centre"""
    with T(x, y, s, r):
        P("M-60 0 C-74 -20 -64 -60 -30 -66 C-10 -76 10 -76 30 -66 C64 -60 74 -20 60 0 Z")
        for dx in (-26, 0, 26):
            S(f"M{dx - 12} -30 Q{dx} -52 {dx + 12} -46", D)


def baguette(x, y, s=1.0, r=0):
    with T(x, y, s, r):
        P("M-90 0 C-96 -22 -70 -26 0 -24 C70 -26 96 -22 90 0 C70 16 -70 16 -90 0 Z")
        for dx in (-54, -18, 18, 54):
            S(f"M{dx - 14} -4 Q{dx} -18 {dx + 14} -12", D)


def donut(x, y, s=1.0, r=0):
    with T(x, y, s, r):
        E(0, 0, 44, 32)
        P(scallop([(-38, -4), (-30, -24), (0, -30), (30, -24), (38, -4)], 0.5, closed=False)
          + " C34 14 18 20 0 20 C-18 20 -34 14 -38 -4 Z", PAPER, D)
        E(0, -4, 14, 8)
        for sx, sy, a in ((-22, -14, 30), (18, -16, -30), (-4, 10, 60), (24, 4, 0), (-26, 4, -40)):
            R(sx - 4, sy - 1.5, 8, 3.5, 1.5, PAPER, F - 1, a)


def cookie(x, y, s=1.0):
    with T(x, y, s):
        C(0, 0, 26)
        for px, py in ((-10, -8), (8, -10), (2, 6), (-12, 10), (14, 8)):
            E(px, py, 3.6, 3, INK, 0)


def pancakes(x, y, s=1.0):
    """stack on a plate; origin bottom centre"""
    with T(x, y, s):
        E(0, -6, 110, 18)
        for i in range(4):
            yy = -24 - i * 26
            P(f"M-82 {yy} C-84 {yy - 20} 84 {yy - 20} 82 {yy} C84 {yy + 16} -84 {yy + 16} -82 {yy} Z")
        P("M-60 -122 C-50 -144 50 -144 60 -122 C62 -104 54 -96 46 -100 C40 -78 30 -80 30 -96 "
          "C10 -92 -10 -92 -24 -96 C-26 -74 -40 -74 -40 -100 C-56 -96 -64 -108 -60 -122 Z", PAPER, D)
        R(-16, -148, 32, 22, 4)
        S("M-14 -140 L14 -140", F)


def soup_pot(x, y, s=1.0):
    """origin bottom centre"""
    with T(x, y, s):
        for sx in (-1, 1):
            R(sx * 102 - 12, -96, 24, 16, 8)
        P("M-96 -100 L96 -100 L90 -10 Q88 0 70 0 L-70 0 Q-88 0 -90 -10 Z")
        E(0, -100, 96, 14)
        P("M-86 -102 Q0 -118 86 -102 Q0 -90 -86 -102 Z", PAPER, D)
        for bx, by in ((-30, -104), (24, -106), (50, -101)):
            C(bx, by, 7, PAPER, F)
        S("M-60 -56 Q0 -48 60 -56", F)


def lemonade_pitcher(x, y, s=1.0):
    with T(x, y, s):
        tube("M36 -100 C66 -100 66 -40 34 -40", 11)
        P("M-36 -120 L32 -120 L44 -132 L42 -116 L38 -8 Q38 0 28 0 L-28 0 Q-38 0 -38 -8 Z")
        S("M-36 -96 L38 -96", F)
        lemon_slice(-6, -56, 0.9)
        R(10, -88, 16, 16, 3, PAPER, F, 20)


def glass(x, y, s=1.0, straw=True):
    with T(x, y, s):
        if straw:
            tube("M6 -64 L18 -96 L32 -100", 5)
        P("M-22 -70 L22 -70 L18 0 L-18 0 Z")
        S("M-21 -54 L21 -54", F)
        lemon_slice(-20, -66, 0.5)


def pumpkin(x, y, s=1.0, face=False):
    """origin bottom centre"""
    with T(x, y, s):
        P("M-6 -70 C-10 -84 -4 -94 8 -98 L12 -90 C4 -88 4 -80 6 -70 Z", PAPER, D)
        P("M-30 -66 C-70 -72 -84 -30 -66 -10 C-56 4 -30 4 -20 -2 C-8 4 8 4 20 -2 "
          "C30 4 56 4 66 -10 C84 -30 70 -72 30 -66 C16 -74 -16 -74 -30 -66 Z")
        S("M-30 -64 C-46 -40 -42 -12 -22 -2", D)
        S("M30 -64 C46 -40 42 -12 22 -2", D)
        S("M8 -84 C20 -96 34 -92 30 -80 C26 -74 18 -78 22 -84", F)
        if face:
            E(-14, -36, 5, 6.5, INK, 0); E(14, -36, 5, 6.5, INK, 0)
            S("M-6 -24 Q0 -18 6 -24", F)


def popcorn(x, y, s=1.0):
    with T(x, y, s):
        P(scallop([(-46, -80), (-40, -108), (-16, -122), (10, -120), (34, -110), (48, -82)], 0.55,
                  closed=False) + " Z")
        P("M-50 -84 L50 -84 L38 0 L-38 0 Z")
        for sx in (-20, 0, 20):
            S(f"M{sx * 1.2} -82 L{sx * 0.9} -2", F)


# ================================================================ books
def book(x, y, s=1.0, r=0, w_=110, h=26, deco=True):
    """closed book lying flat, origin bottom-centre"""
    with T(x, y, s, r):
        R(-w_ / 2, -h, w_, h, 5)
        R(w_ / 2 - 16, -h + 5, 10, h - 10, 3, PAPER, F)
        if deco:
            S(f"M{-w_ / 2 + 14} {-h / 2} L{w_ / 2 - 30} {-h / 2}", F)


def book_stack(x, y, s=1.0, n=3):
    with T(x, y, s):
        yy = 0
        for i in range(n):
            ww = [120, 104, 112, 96][i % 4]
            with T([-4, 6, -6, 4][i % 4], yy):
                book(0, 0, 1, 0, ww, 26)
            yy -= 26


def open_book(x, y, s=1.0, r=0):
    """origin: spine bottom"""
    with T(x, y, s, r):
        P("M0 -4 C-30 -16 -60 -14 -80 -6 L-80 -66 C-60 -74 -30 -76 0 -64 Z")
        P("M0 -4 C30 -16 60 -14 80 -6 L80 -66 C60 -74 30 -76 0 -64 Z")
        for i in range(3):
            yy = -52 + i * 14
            S(f"M-66 {yy + 2} C-50 {yy - 4} -26 {yy - 4} -12 {yy + 2}", F)
            S(f"M66 {yy + 2} C50 {yy - 4} 26 {yy - 4} 12 {yy + 2}", F)


def bookshelf(x, y, w_=300, h=420, rows=3, s=1.0, seed=1):
    """origin: bottom-left"""
    import random
    rnd = random.Random(seed)
    with T(x, y, s):
        R(0, -h, w_, h, 8)
        R(14, -h + 14, w_ - 28, h - 28, 4, PAPER, D)
        rh = (h - 28) / rows
        for row in range(rows):
            base = -14 - row * rh
            if row > 0:
                R(10, base - 6, w_ - 20, 12, 3)
            bx = 22
            while bx < w_ - 40:
                kind = rnd.random()
                bw = rnd.choice([18, 22, 26, 30])
                bh = rh - rnd.choice([18, 26, 34, 40])
                if kind < 0.12 and bx < w_ - 90:
                    with T(bx + 30, base - 6):
                        plant_small(0, 0, 0.5)
                    bx += 64
                    continue
                if kind < 0.2 and bx < w_ - 70:
                    R(bx, base - 6 - 20, 50, 20, 4, PAPER, D)
                    R(bx + 4, base - 6 - 38, 44, 18, 4, PAPER, D)
                    bx += 56
                    continue
                if kind < 0.3 and bx > 30:
                    with T(bx + bh * 0.25, base - 6, 1, 18):
                        R(0, -bh, bw, bh, 4, PAPER, D)
                    bx += bw + bh * 0.35
                    continue
                R(bx, base - 6 - bh, bw, bh, 4, PAPER, D)
                if bw >= 24:
                    L(bx + 6, base - 6 - bh + 12, bx + bw - 6, base - 6 - bh + 12, F)
                bx += bw + 2


# ================================================================ plants
def plant_small(x, y, s=1.0):
    """little pot with round leaves, origin bottom centre"""
    with T(x, y, s):
        for a, l in ((-40, 60), (0, 74), (40, 60), (-14, 66), (16, 64)):
            with T(0, -44, 1, a):
                P(f"M0 0 C-14 {-l * 0.4} -12 {-l * 0.85} 0 {-l} C12 {-l * 0.85} 14 {-l * 0.4} 0 0 Z", PAPER, D)
        P("M-30 -48 L30 -48 L24 0 L-24 0 Z")
        R(-36, -56, 72, 14, 5)


def monstera(x, y, s=1.0):
    with T(x, y, s):
        for a, l in ((-50, 120), (-15, 150), (25, 135), (60, 105)):
            with T(0, -70, 1, a):
                S(f"M0 0 L0 {-l * 0.5}", D)
                P(f"M0 {-l * 0.4} C-48 {-l * 0.5} -44 {-l * 1.0} 0 {-l} C44 {-l * 1.0} 48 {-l * 0.5} 0 {-l * 0.4} Z")
                S(f"M0 {-l * 0.42} L0 {-l * 0.95}", F)
                for k in (0.55, 0.72):
                    S(f"M-34 {-l * k} L-14 {-l * k + 6} M34 {-l * k} L14 {-l * k + 6}", F)
        P("M-46 -74 L46 -74 L36 0 L-36 0 Z")
        R(-52, -84, 104, 18, 6)
        S(wavy_line(-40, 40, -40, 5, 6), F)


def cactus(x, y, s=1.0):
    with T(x, y, s):
        P("M-18 -40 C-18 -130 18 -130 18 -40 Z")
        P("M-16 -70 C-40 -70 -42 -80 -42 -100 C-42 -110 -30 -110 -30 -100 C-30 -88 -26 -84 -16 -84 Z", PAPER, D)
        P("M16 -60 C40 -60 42 -70 42 -88 C42 -98 30 -98 30 -88 C30 -78 26 -74 16 -74 Z", PAPER, D)
        flower(0, -120, 9, 5, F)
        P("M-30 -44 L30 -44 L24 0 L-24 0 Z")
        R(-35, -50, 70, 12, 5)


def tulip(x, y, h=90, s=1.0, r=0):
    with T(x, y, s, r):
        S(f"M0 0 L0 {-h}", D)
        P(f"M0 {-h * 0.35} C-30 {-h * 0.5} -34 {-h * 0.8} -26 {-h * 0.85} C-20 {-h * 0.6} -6 {-h * 0.5} 0 {-h * 0.35} Z", PAPER, D)
        P(f"M-18 {-h} C-20 {-h - 30} -12 {-h - 40} -10 {-h - 40} L0 {-h - 28} L10 {-h - 40} "
          f"C12 {-h - 40} 20 {-h - 30} 18 {-h} C14 {-h + 10} -14 {-h + 10} -18 {-h} Z")


def daisy(x, y, h=80, s=1.0, r=0, size=20):
    with T(x, y, s, r):
        S(f"M0 0 Q-6 {-h / 2} 0 {-h}", D)
        P(f"M-2 {-h * 0.4} C-26 {-h * 0.5} -30 {-h * 0.3} -26 {-h * 0.28} C-16 {-h * 0.3} -8 {-h * 0.3} -2 {-h * 0.4} Z", PAPER, D)
        flower(0, -h, size, 8, D)


def sunflower(x, y, h=200, s=1.0):
    with T(x, y, s):
        S(f"M0 0 L0 {-h}", W)
        for sy, sd in ((-h * 0.35, -1), (-h * 0.6, 1)):
            P(f"M0 {sy} C{sd * 40} {sy - 30} {sd * 70} {sy - 10} {sd * 70} {sy} C{sd * 40} {sy + 16} 20 {sy} 0 {sy} Z", PAPER, D)
        with T(0, -h):
            for i in range(14):
                with T(0, 0, 1, i * 360 / 14):
                    P("M0 -30 C-10 -46 -6 -62 0 -66 C6 -62 10 -46 0 -30 Z", PAPER, D)
            C(0, 0, 32)
            for px, py in ring(0, 0, 18, 18, 8):
                dot(px, py, 2.6)
            dot(0, 0, 2.6)


def grass(x, y, s=1.0):
    with T(x, y, s):
        S("M-14 0 Q-14 -14 -22 -24 M0 0 Q0 -18 -2 -30 M14 0 Q14 -14 22 -24", D)


def bush(x, y, w_=160, h=90, s=1.0, berries=False):
    with T(x, y, s):
        pts = ring(0, 0, w_ / 2, h, 7, 180, 360)
        P(scallop(pts, 0.62, closed=False) + " Z")
        if berries:
            for bx, by in ((-30, -40), (10, -56), (40, -30), (-50, -20), (0, -24)):
                C(bx, by, 6, PAPER, F)


def tree(x, y, s=1.0, apples=False, h=200):
    """round tree, origin trunk bottom"""
    with T(x, y, s):
        P(f"M-22 0 C-16 -40 -18 {-h * 0.6} -14 {-h} L14 {-h} C18 {-h * 0.6} 16 -40 22 0 Z")
        S(f"M-4 {-h * 0.5} Q-10 {-h * 0.62} -26 {-h * 0.7}", D)
        P(scallop(ring(0, -h - 40, 120, 100, 11), 0.62))
        S(f"M-70 {-h - 30} Q-60 {-h - 54} -40 {-h - 60}", F)
        S(f"M30 {-h - 90} Q50 {-h - 86} 60 {-h - 70}", F)
        if apples:
            for ax, ay in ((-50, -h - 40), (40, -h - 20), (0, -h - 90), (70, -h - 70), (-80, -h - 90), (-10, -h + 10)):
                apple(ax, ay, 0.38)


def pine(x, y, s=1.0, h=260):
    with T(x, y, s):
        R(-14, -30, 28, 34, 4)
        for i, (wy, ww) in enumerate(((-30, 90), (-30 - h * 0.3, 74), (-30 - h * 0.58, 56))):
            top = wy - h * 0.42
            P(f"M{-ww} {wy} Q0 {wy + 14} {ww} {wy} L{ww * 0.25} {top + 20} Q0 {top} {-ww * 0.25} {top + 20} Z")


def mushroom(x, y, s=1.0, r=0):
    with T(x, y, s, r):
        P("M-16 0 C-18 -20 -14 -36 -12 -40 L12 -40 C14 -36 18 -20 16 0 Q0 6 -16 0 Z")
        P("M-50 -36 C-54 -90 54 -90 50 -36 Q0 -26 -50 -36 Z")
        for sx, sy, rr in ((-24, -60, 8), (10, -70, 7), (30, -50, 6), (-4, -48, 5)):
            C(sx, sy, rr, PAPER, F)


# ================================================================ home
def window(x, y, w_=220, h=240, curtains=True, rain=False, night=False, sill=True, inside=None):
    """origin: top-left of the glass"""
    with T(x, y):
        R(-12, -12, w_ + 24, h + 24, 10)
        R(0, 0, w_, h, 4)
        if inside:
            with Clip(f"M0 0 H{w_} V{h} H0 Z"):
                inside()
        if night:
            moon(w_ * 0.7, h * 0.32, 0.45, face=False)
            for sx, sy in ((w_ * 0.22, h * 0.22), (w_ * 0.36, h * 0.6), (w_ * 0.8, h * 0.75)):
                star(sx, sy, 0.45, 15, D)
        if rain:
            for i, (rx, ry) in enumerate(((0.15, 0.15), (0.38, 0.32), (0.62, 0.12), (0.84, 0.3), (0.22, 0.62),
                                          (0.5, 0.72), (0.76, 0.58), (0.14, 0.88), (0.86, 0.88), (0.42, 0.95))):
                raindrop(w_ * rx, h * ry, 0.85)
        L(w_ / 2, 0, w_ / 2, h, D)
        L(0, h / 2, w_, h / 2, D)
        if curtains:
            P(f"M-30 -24 L{w_ * 0.28} -24 C{w_ * 0.16} {h * 0.3} {w_ * 0.05} {h * 0.55} 0 {h * 0.6} "
              f"C-10 {h * 0.8} -20 {h + 10} -30 {h + 20} Z")
            P(f"M{w_ + 30} -24 L{w_ * 0.72} -24 C{w_ * 0.84} {h * 0.3} {w_ * 0.95} {h * 0.55} {w_} {h * 0.6} "
              f"C{w_ + 10} {h * 0.8} {w_ + 20} {h + 10} {w_ + 30} {h + 20} Z")
            R(-40, -36, w_ + 80, 16, 8)
            C(-40, -28, 11); C(w_ + 40, -28, 11)
        if sill:
            R(-26, h + 6, w_ + 52, 18, 6)


def wall_frame(x, y, w_=110, h=90, art="heart"):
    with T(x, y):
        R(-w_ / 2, -h / 2, w_, h, 6)
        R(-w_ / 2 + 12, -h / 2 + 12, w_ - 24, h - 24, 3, PAPER, F)
        if art == "heart":
            heart(0, 2, 0.9, 0, D)
        elif art == "mountain":
            S(f"M{-w_ / 2 + 14} {h / 2 - 16} L-10 -8 L6 6 L18 -6 L{w_ / 2 - 14} {h / 2 - 16}", D)
            C(-20, -16, 7, PAPER, F)
        elif art == "flower":
            flower(0, 0, 18, 6, F)
        elif art == "cat":
            P("M-18 18 C-20 -6 -16 -10 -14 -20 L-6 -10 L6 -10 L14 -20 C16 -10 20 -6 18 18 Z", PAPER, D)


def lamp(x, y, s=1.0):
    """table lamp, origin bottom"""
    with T(x, y, s):
        E(0, -4, 34, 8)
        S("M0 -10 L0 -80", W + 2)
        P("M-44 -76 L44 -76 L28 -140 L-28 -140 Z")
        S("M-38 -98 L38 -98", F)


def floor_lamp(x, y, s=1.0):
    with T(x, y, s):
        E(0, -4, 44, 10)
        S("M0 -10 L0 -330", W + 2)
        P("M-58 -320 L58 -320 L36 -410 L-36 -410 Z")
        L(-48, -350, 48, -350, F)


def rug(x, y, rx=260, ry=50):
    with T(x, y):
        E(0, 0, rx, ry)
        E(0, 0, rx - 26, ry - 14, PAPER, D)
        E(0, 0, rx - 54, ry - 26, PAPER, F)


def armchair(x, y, s=1.0):
    """front view, origin bottom centre. Draw a sitter after the back+seat
    with armchair_arms() on top."""
    with T(x, y, s):
        P("M-130 -150 C-130 -270 130 -270 130 -150 L130 -60 L-130 -60 Z")
        for sx in (-50, 50):
            dot(sx, -190, 5)
        dot(0, -220, 5)
        R(-112, -86, 224, 54, 18)
        R(-120, -36, 18, 36, 4); R(102, -36, 18, 36, 4)


def armchair_arms(x, y, s=1.0):
    with T(x, y, s):
        for sx in (-1, 1):
            P(f"M{sx * 106} -24 L{sx * 106} -120 C{sx * 106} -150 {sx * 160} -150 {sx * 160} -120 "
              f"L{sx * 160} -24 Q{sx * 133} -16 {sx * 106} -24 Z")
            E(sx * 133, -130, 26, 14, PAPER, D)
        P("M-160 -34 L160 -34 L156 -10 Q0 -2 -156 -10 Z")


def round_table(x, y, s=1.0, top=True, w_=200):
    """café table; origin = floor under the stand"""
    with T(x, y, s):
        P("M-50 0 Q0 -16 50 0 Q0 10 -50 0 Z")
        R(-9, -150, 18, 146, 4)
        if top:
            E(0, -158, w_ / 2, 22)
            S(f"M{-w_ / 2} -158 L{-w_ / 2} -148 Q0 -120 {w_ / 2} -148 L{w_ / 2} -158", W)


def counter(x1, x2, ytop, ybot, tiles=True):
    R(x1, ytop, x2 - x1, ybot - ytop, 0)
    R(x1 - 10, ytop - 18, x2 - x1 + 20, 24, 8)
    if tiles:
        n = int((x2 - x1) / 90)
        for i in range(1, n + 1):
            L(x1 + i * (x2 - x1) / (n + 1), ytop + 6, x1 + i * (x2 - x1) / (n + 1), ybot, D)
        L(x1, (ytop + ybot) / 2 + 3, x2, (ytop + ybot) / 2 + 3, D)


def awning(x1, x2, y, h=70, n=7):
    w_ = (x2 - x1) / n
    for i in range(n):
        xa = x1 + i * w_
        P(f"M{xa} {y} L{xa + w_} {y} L{xa + w_} {y + h} A{w_ / 2} {w_ / 2} 0 0 1 {xa} {y + h} Z",
          PAPER, W if True else D)
        if i % 2 == 0:
            for k in (0.33, 0.66):
                L(xa + w_ * k, y + 8, xa + w_ * k, y + h + 10, F)


def bed(x, y, s=1.0):
    """bed seen from the foot end, sitter tucked in; origin = floor centre.
    Draw: bed_back -> character -> bed_blanket"""
    with T(x, y, s):
        P("M-230 -150 L-230 -330 C-230 -400 230 -400 230 -330 L230 -150 Z")
        R(-200, -330, 400, 40, 18, PAPER, D)
        E(-80, -232, 90, 46)
        E(90, -232, 90, 46)


def bed_blanket(x, y, s=1.0, top=-180):
    with T(x, y, s):
        P(f"M-250 {top + 10} C-200 {top - 16} 200 {top - 16} 250 {top + 10} L250 -40 L-250 -40 Z")
        S(f"M-250 {top + 50} C-200 {top + 30} 200 {top + 30} 250 {top + 50}", D)
        for i in range(-2, 3):
            heart(i * 92, top + 100, 0.9, 0, D)
        for i in range(-3, 3):
            star(i * 92 + 46, top + 150 - 10, 0.55, 15, D)
        R(-260, -44, 520, 44, 10)
        R(-250, 0, 26, 30, 4); R(224, 0, 26, 30, 4)


def nightstand(x, y, s=1.0):
    with T(x, y, s):
        R(-60, -110, 120, 110, 8)
        L(-60, -56, 60, -56, D)
        C(0, -84, 5, PAPER, F); C(0, -30, 5, PAPER, F)


def clock(x, y, r=40):
    C(x, y, r)
    C(x, y, r - 10, PAPER, F)
    L(x, y, x, y - r * 0.55, D)
    L(x, y, x + r * 0.4, y, D)
    dot(x, y, 4)


def shelf(x1, x2, y):
    R(x1, y, x2 - x1, 16, 5)
    for xx in (x1 + 20, x2 - 34):
        P(f"M{xx} {y + 16} L{xx + 14} {y + 16} L{xx + 14} {y + 40} Z", PAPER, D)


def jar(x, y, s=1.0, label="heart"):
    with T(x, y, s):
        P("M-26 -70 L26 -70 L30 -60 C34 -30 34 -10 26 0 L-26 0 C-34 -10 -34 -30 -30 -60 Z")
        R(-30, -84, 60, 16, 5)
        if label == "heart":
            heart(0, -34, 0.6, 0, F)
        elif label == "cookie":
            cookie(0, -34, 0.6)


# ================================================================ outdoors
def ground_hill(y, amp=30, x1=0, x2=850):
    P(f"M{x1 - 20} {y + 20} C{x1 + 200} {y - amp} {x2 - 300} {y + amp} {x2 + 20} {y - 10} "
      f"L{x2 + 20} 1200 L{x1 - 20} 1200 Z")


def tent(x, y, s=1.0):
    """origin bottom centre"""
    with T(x, y, s):
        P("M-170 0 L0 -230 L170 0 Z")
        P("M-60 0 C-30 -60 -6 -150 0 -230 C6 -150 30 -60 60 0 Z")
        S("M0 -230 L0 -150", D)
        S("M0 -230 L-14 -258 M0 -230 L24 -256", D)
        poly([(24, -256), (60, -250), (26, -236)], True, PAPER, D)
        S("M-170 0 L-200 -20 M170 0 L200 -20", F)


def campfire(x, y, s=1.0):
    with T(x, y, s):
        for i in range(8):
            a = math.radians(180 + i * 180 / 7)
            E(90 * math.cos(a) * 1.0, 6 + 14 * math.sin(a) + 14, 18, 13, PAPER, D)
        P("M-16 -6 C-50 -30 -50 -80 -20 -110 C-24 -80 -6 -70 0 -100 C10 -70 30 -90 26 -130 "
          "C66 -90 58 -30 16 -6 Z")
        P("M-6 -10 C-24 -26 -20 -52 -6 -62 C-4 -46 6 -42 10 -60 C26 -40 20 -20 6 -10 Z", PAPER, D)
        R(-70, -18, 140, 22, 10, PAPER, W, 14)
        R(-70, -18, 140, 22, 10, PAPER, W, -14)


def lantern(x, y, s=1.0):
    with T(x, y, s):
        S("M-16 -88 C-16 -110 16 -110 16 -88", D)
        R(-28, -88, 56, 14, 5)
        P("M-24 -74 L24 -74 L24 -14 L-24 -14 Z")
        L(-12, -74, -12, -14, F); L(12, -74, 12, -14, F)
        P("M0 -64 C10 -50 8 -30 0 -28 C-8 -30 -10 -50 0 -64 Z", PAPER, F)
        R(-30, -16, 60, 16, 5)


def umbrella(x, y, s=1.0, r=0):
    """origin = handle end"""
    with T(x, y, s, r):
        S("M0 0 L0 -190", W)
        S("M0 0 Q0 16 -14 16 Q-26 16 -26 4", W)
        P("M-130 -150 C-120 -230 120 -230 130 -150 Q108 -168 86 -150 Q65 -170 44 -150 "
          "Q22 -170 0 -150 Q-22 -170 -44 -150 Q-65 -170 -86 -150 Q-108 -168 -130 -150 Z")
        for xx in (-86, -44, 0, 44, 86):
            S(f"M0 -224 Q{xx * 0.5} -200 {xx} -150", D)
        C(0, -228, 7)


def puddle(x, y, rx=150, ry=28):
    P(smooth([(x - rx, y), (x - rx * 0.6, y - ry), (x, y - ry * 0.8), (x + rx * 0.6, y - ry * 1.1),
              (x + rx, y), (x + rx * 0.5, y + ry), (x - rx * 0.4, y + ry * 0.9)]))
    E(x, y, rx * 0.55, ry * 0.4, PAPER, F)


def boots(x, y, s=1.0):
    with T(x, y, s):
        for dx in (-34, 34):
            P(f"M{dx - 22} -74 L{dx + 14} -74 L{dx + 14} -26 L{dx + 40} -22 Q{dx + 46} 0 {dx + 30} 0 "
              f"L{dx - 22} 0 Z")
            L(dx - 22, -60, dx + 14, -60, D)


def watering_can(x, y, s=1.0, r=0):
    with T(x, y, s, r):
        tube("M-30 -64 C-30 -96 30 -96 30 -64", 9)
        P("M28 -40 L96 -84 L102 -76 L36 -20 Z")
        E(104, -84, 12, 18, PAPER, W, 40)
        R(-46, -66, 92, 66, 10)
        flower(0, -32, 14, 6, F)


def basket(x, y, s=1.0, fill=None):
    """picnic basket; origin bottom centre. fill: callable drawn peeking out"""
    with T(x, y, s):
        tube("M-60 -60 C-60 -150 60 -150 60 -60", 10)
        if fill:
            fill()
        P("M-80 -66 L80 -66 L66 0 L-66 0 Z")
        R(-86, -76, 172, 18, 6)
        for i in range(-3, 4):
            L(i * 20, -56, i * 17, -4, F)
        S("M-74 -36 L74 -36", F)


def picnic_blanket(cx, cy, w_=600, h=200, n=6):
    """trapezoid checkered blanket in gentle perspective"""
    tl, tr = (cx - w_ * 0.38, cy - h / 2), (cx + w_ * 0.38, cy - h / 2)
    bl, br = (cx - w_ / 2, cy + h / 2), (cx + w_ / 2, cy + h / 2)
    poly([tl, tr, br, bl])
    for i in range(1, n):
        t = i / n
        L(tl[0] + (tr[0] - tl[0]) * t, tl[1], bl[0] + (br[0] - bl[0]) * t, bl[1], D)
    for j in range(1, 3):
        t = j / 3
        L(tl[0] + (bl[0] - tl[0]) * t, tl[1] + h * t, tr[0] + (br[0] - tr[0]) * t, tr[1] + h * t, D)


def fence(x1, x2, y, h=110):
    n = int((x2 - x1) / 60)
    R(x1, y - h * 0.72, x2 - x1, 18, 4)
    R(x1, y - h * 0.32, x2 - x1, 18, 4)
    for i in range(n + 1):
        xx = x1 + i * (x2 - x1) / n
        P(f"M{xx - 16} {y} L{xx - 16} {y - h + 14} L{xx} {y - h} L{xx + 16} {y - h + 14} L{xx + 16} {y} Z")


def telescope(x, y, s=1.0):
    """origin = tripod top"""
    with T(x, y, s):
        L(0, 0, -60, 160, W); L(0, 0, 60, 160, W); L(0, 0, 0, 170, W)
        with T(0, 0, 1, -28):
            R(-90, -24, 150, 48, 10)
            R(56, -32, 50, 64, 8)
            R(-120, -16, 34, 32, 6)
            L(-30, -22, -30, 22, F)
        C(0, 0, 12)


def balloon(x, y, s=1.0, string=120, r=0):
    with T(x, y, s, r):
        S(f"M0 46 C-12 {46 + string * 0.4} 12 {46 + string * 0.7} 0 {46 + string}", F)
        P("M0 46 C-46 40 -46 -50 0 -50 C46 -50 46 40 0 46 Z")
        P("M-6 52 L6 52 L0 44 Z", PAPER, F)
        S("M-20 -26 Q-26 -10 -22 6", F)


def gift(x, y, s=1.0):
    with T(x, y, s):
        R(-50, -76, 100, 76, 6)
        R(-58, -96, 116, 24, 6)
        R(-10, -96, 20, 96, 2, PAPER, D)
        P("M0 -96 C-10 -120 -44 -124 -40 -104 C-38 -96 -14 -96 0 -96 Z", PAPER, D)
        P("M0 -96 C10 -120 44 -124 40 -104 C38 -96 14 -96 0 -96 Z", PAPER, D)


def yarn(x, y, s=1.0):
    with T(x, y, s):
        C(0, 0, 40)
        for k in (-20, -6, 8, 22):
            S(f"M{k - 24} {-30 + abs(k) * 0.6} Q{k + 10} 0 {k - 14} {34 - abs(k) * 0.5}", F)
        L(-56, -40, 30, 16, D); L(-46, -54, 40, 6, D)
        C(-58, -42, 5, PAPER, F); C(-48, -56, 5, PAPER, F)


def sign_board(x, y, label, w_=180, h=64, s=1.0, size=34):
    with T(x, y, s):
        R(-w_ / 2, -h / 2, w_, h, 12)
        text(0, size * 0.35, label, size, 2.2)


def stars_field(pts, s=0.5):
    for i, (x, y) in enumerate(pts):
        if i % 3 == 0:
            sparkle(x, y, s * 1.6, F + .4)
        else:
            star(x, y, s, (i * 23) % 40 - 20, D)


def butterfly(x, y, s=1.0, r=0):
    with T(x, y, s, r):
        for sd in (-1, 1):
            E(sd * 18, -12, 17, 21, PAPER, D, sd * 35)
            E(sd * 14, 12, 11, 13, PAPER, D, -sd * 25)
            C(sd * 19, -14, 5, PAPER, F)
        E(0, 0, 5, 20, PAPER, D)
        S("M-2 -18 Q-6 -30 -14 -32 M2 -18 Q6 -30 14 -32", F)


def leaf(x, y, s=1.0, r=0):
    with T(x, y, s, r):
        P("M0 30 C-26 10 -24 -20 0 -36 C24 -20 26 10 0 30 Z", PAPER, D)
        S("M0 36 L0 -26 M0 4 L-12 -8 M0 14 L12 2", F)


def bucket(x, y, s=1.0, flowers=None):
    """flower bucket; origin bottom centre; flowers(): drawn first, rising from y=-60"""
    with T(x, y, s):
        if flowers:
            flowers()
        P("M-50 -80 L50 -80 L40 0 L-40 0 Z")
        R(-56, -88, 112, 16, 5)
        L(-46, -40, 46, -40, F)


def hay_bale(x, y, s=1.0):
    with T(x, y, s):
        R(-90, -80, 180, 80, 14)
        for yy in (-58, -38, -18):
            S(wavy_line(-80, 80, yy, 3, 10), F)
        L(-50, -80, -50, 0, D); L(50, -80, 50, 0, D)


def pouf(x, y, s=1.0):
    with T(x, y, s):
        P("M-130 -40 C-140 -90 140 -90 130 -40 C140 0 -140 0 -130 -40 Z")
        E(0, -64, 120, 26, PAPER, D)
        dot(0, -64, 6)
