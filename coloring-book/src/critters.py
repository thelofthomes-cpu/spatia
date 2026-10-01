"""The Cozy Little World cast: original chibi animals built from simple parts.

critter(kind, x, y, s, ...) draws a full character. Local coordinates: head
centre at (0, 0), head ~130 wide, feet at y ~160. At s=1 a character is about
260 units tall (2.6 in on the page).
"""
from ink import *

KINDS = ["bunny", "bear", "cat", "fox", "frog", "panda", "duck", "penguin",
         "mouse", "hamster", "puppy", "sheep", "hedgehog", "koala", "squirrel",
         "raccoon", "axolotl", "otter"]

HEAD = {  # rx, ry
    "bunny": (64, 54), "bear": (66, 56), "cat": (64, 54), "fox": (64, 54),
    "frog": (72, 50), "panda": (66, 56), "duck": (58, 54), "penguin": (62, 56),
    "mouse": (58, 52), "hamster": (66, 58), "puppy": (64, 55), "sheep": (60, 54),
    "hedgehog": (62, 54), "koala": (64, 54), "squirrel": (60, 52),
    "raccoon": (64, 54), "axolotl": (68, 52), "otter": (62, 52),
}


# ------------------------------------------------------------------ faces
def eyes(expr="happy", dx=23, y=6, big=1.0):
    for side, e in ((-1, expr), (1, expr)):
        if expr == "wink" and side == 1:
            e = "joy"
        elif expr == "wink":
            e = "happy"
        x = side * dx
        if e in ("happy", "wink"):
            E(x, y, 7.5 * big, 9.5 * big, INK, 0)
            C(x + 2.6 * big, y - 3.6 * big, 3.0 * big, PAPER, 0)
        elif e == "joy":
            S(f"M{x - 9} {y + 4} Q{x} {y - 9} {x + 9} {y + 4}", D)
        elif e == "sleep":
            S(f"M{x - 9} {y} Q{x} {y + 9} {x + 9} {y}", D)
        elif e == "dot":
            dot(x, y, 6)


def mouth(kind="w", y=22):
    if kind == "w":
        S(f"M-9 {y} Q-4.5 {y + 7} 0 {y} Q4.5 {y + 7} 9 {y}", F + .6)
    elif kind == "smile":
        S(f"M-8 {y} Q0 {y + 9} 8 {y}", F + .6)
    elif kind == "open":
        P(f"M-9 {y - 1} Q0 {y - 3} 9 {y - 1} Q8 {y + 13} 0 {y + 13} Q-8 {y + 13} -9 {y - 1} Z", PAPER, F + .6)
        S(f"M-5 {y + 8} Q0 {y + 5} 5 {y + 8}", F - .6)
    elif kind == "o":
        E(0, y + 3, 5, 6, PAPER, F + .6)
    elif kind == "yum":
        S(f"M-9 {y} Q0 {y + 8} 9 {y}", F + .6)
        P(f"M3 {y + 3} Q8 {y + 14} 12 {y + 4}", PAPER, F)


BLUSH = "#ffaec4"


def blush(dx=41, y=24):
    from ink import _tint
    with (Tint(BLUSH) if _tint else T()):
        for s in (-1, 1):
            E(s * dx, y, 11, 6.5, PAPER, F)


def face(expr="happy", m="w", dy=0, blushy=True, spread=23):
    if blushy:
        blush(y=24 + dy)
    eyes(expr, dx=spread, y=6 + dy)
    mouth(m, y=21 + dy)


# ------------------------------------------------------------------ bodies
BODY = ("M-40 36 C-62 60 -68 128 -42 148 C-22 162 22 162 42 148 "
        "C68 128 62 60 40 36 Z")


def body(kind):
    P(BODY)
    if kind in ("bear", "fox", "penguin", "hamster", "koala", "raccoon",
                "otter", "squirrel", "panda"):
        E(0, 108, 30, 34, PAPER, F)


def feet(kind):
    if kind in ("duck", "penguin"):
        for s in (-1, 1):
            P(f"M{s * 14} 150 L{s * 46} 150 Q{s * 50} 165 {s * 40} 166 "
              f"Q{s * 30} 160 {s * 26} 166 Q{s * 14} 166 {s * 14} 150 Z")
    elif kind == "frog":
        for s in (-1, 1):
            P(f"M{s * 10} 152 Q{s * 30} 140 {s * 52} 150 Q{s * 60} 158 {s * 52} 163 "
              f"Q{s * 44} 168 {s * 38} 162 Q{s * 30} 170 {s * 22} 163 Q{s * 10} 166 {s * 10} 152 Z")
    else:
        for s in (-1, 1):
            E(s * 28, 153, 23, 13)
            if kind in ("bear", "panda", "koala", "puppy", "hamster", "mouse", "cat"):
                for k in (-8, 0, 8):
                    L(s * 28 + k, 146, s * 28 + k, 149, F)


def tail(kind):
    if kind == "fox":
        P("M38 120 C90 140 128 100 120 52 C114 20 90 24 92 50 C94 80 70 96 40 96 Z")
        S("M120 52 C106 50 98 60 104 74 C108 82 118 78 121 66", F)
    elif kind == "squirrel":
        P("M30 140 C100 150 140 90 120 30 C108 -10 60 -20 52 10 C46 34 80 40 84 64 "
          "C88 92 60 110 34 106 Z")
        S("M84 64 C96 50 104 36 102 22", F)
    elif kind == "cat":
        tube("M40 140 C90 150 110 120 100 90 C94 72 104 60 116 64", 16)
    elif kind == "raccoon":
        P("M38 128 C80 150 120 120 116 80 C112 60 96 62 96 78 C98 100 72 110 44 104 Z")
        for t in (0.35, 0.65):
            S(f"M{70 + 30 * t} {130 - 50 * t} L{90 + 26 * t} {100 - 30 * t}", F)
    elif kind == "otter":
        P("M30 140 C70 160 120 158 128 140 C120 132 80 130 40 120 Z")


def arms(kind, pose="down"):
    """pose: down | hold | up | wave | hip"""
    def arm(s, p):
        if p == "down":
            E(s * 55, 94, 13.5, 24, PAPER, W, -s * 18)
        elif p == "hold":
            E(s * 30, 84, 15, 14)
        elif p == "up":
            E(s * 64, 30, 13, 24, PAPER, W, s * 35)
        elif p == "out":
            E(s * 70, 78, 13, 24, PAPER, W, -s * 60)
    if pose == "wave":
        arm(-1, "down"); arm(1, "up")
    elif pose == "holdl":
        arm(-1, "hold"); arm(1, "down")
    else:
        for s in (-1, 1):
            arm(s, pose)


# ------------------------------------------------------------------ heads
def ears_back(kind, ear=""):
    if kind == "bunny":
        lr = -18 if ear != "flop" else -30
        E(-26, -84, 17, 48, PAPER, W, lr)
        E(-26, -84, 8, 31, PAPER, F, lr)
        if ear == "flop":
            E(46, -62, 16, 44, PAPER, W, 60)
            E(46, -62, 7.5, 29, PAPER, F, 60)
        else:
            E(26, -84, 17, 48, PAPER, W, 18)
            E(26, -84, 8, 31, PAPER, F, 18)
    elif kind in ("bear", "panda"):
        for s in (-1, 1):
            C(s * 47, -40, 21)
            C(s * 47, -40, 10, PAPER, F)
    elif kind == "hamster":
        for s in (-1, 1):
            C(s * 42, -46, 18)
            C(s * 42, -46, 8, PAPER, F)
    elif kind == "mouse":
        for s in (-1, 1):
            C(s * 50, -42, 32)
            C(s * 50, -42, 20, PAPER, F)
    elif kind == "koala":
        for s in (-1, 1):
            P(scallop(ring(s * 58, -30, 33, 31, 9, -180, 180)))
            C(s * 58, -30, 17, PAPER, F)
    elif kind in ("cat", "fox", "raccoon", "squirrel"):
        big = 1.25 if kind == "fox" else 1.0
        for s in (-1, 1):
            P(f"M{s * 58} -18 L{s * 54 * big} {-80 * big} L{s * 14} -50 Z")
            S(f"M{s * 50} -28 L{s * 49 * big} {-66 * big} L{s * 28} -46", F)
        if kind == "squirrel":
            for s in (-1, 1):
                S(f"M{s * 52} -80 l{s * -4} -12 M{s * 52} -80 l{s * 6} -10", F)
    elif kind == "frog":
        for s in (-1, 1):
            C(s * 36, -36, 25)
    elif kind == "sheep":
        for s in (-1, 1):
            E(s * 66, -4, 22, 11, PAPER, W, s * 20)
    elif kind == "hedgehog":
        pts = []
        for i in range(15):
            a = math.radians(-200 + i * 220 / 14)
            r = 92 if i % 2 == 0 else 70
            pts.append((r * math.cos(a), 6 + r * 0.9 * math.sin(a)))
        P("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z")
    elif kind == "axolotl":
        for s in (-1, 1):
            for k, a in enumerate((-40, -10, 20)):
                E(s * (70 + 8 * (k == 1)), -14 + k * 22, 26, 10, PAPER, W, s * a)
    elif kind == "otter":
        for s in (-1, 1):
            C(s * 52, -30, 13)


def head_shape(kind):
    rx, ry = HEAD[kind]
    if kind == "cat" or kind == "fox" or kind == "raccoon":
        P(smooth([(-rx, 4), (-rx * 0.8, -ry * 0.75), (0, -ry), (rx * 0.8, -ry * 0.75),
                  (rx, 4), (rx * 0.72, ry * 0.84), (0, ry), (-rx * 0.72, ry * 0.84)]))
    else:
        E(0, 0, rx, ry)


def head_details(kind, expr, m):
    rx, ry = HEAD[kind]
    if kind == "panda":
        for s in (-1, 1):
            E(s * 24, 6, 16, 20, PAPER, F, -s * 25)
        face(expr, m, blushy=True)
        E(0, 16, 7, 5, INK, 0)
        return
    if kind == "raccoon":
        P("M-56 -4 C-40 -22 -12 -10 0 -4 C12 -10 40 -22 56 -4 C46 22 20 20 0 12 "
          "C-20 20 -46 22 -56 -4 Z", PAPER, F)
        eyes(expr)
        E(0, 16, 7, 5, INK, 0)
        mouth(m, 22)
        blush(dx=42, y=30)
        return
    if kind == "fox":
        P("M-62 14 C-40 8 -16 26 0 22 C16 26 40 8 62 14 C50 46 22 54 0 54 C-22 54 -50 46 -62 14 Z",
          PAPER, F)
    if kind == "penguin":
        P("M0 -26 C20 -46 54 -36 52 -4 C50 30 26 50 0 50 C-26 50 -50 30 -52 -4 "
          "C-54 -36 -20 -46 0 -26 Z", PAPER, F)
    if kind in ("bear", "puppy", "koala", "otter"):
        E(0, 22, 21, 15, PAPER, F)
    if kind == "sheep":
        P(scallop(ring(0, -50, 62, 24, 10, 180, 360) + [(50, -34), (-50, -34)], 0.6))
    face(expr, None if kind == "duck" else m)
    if kind in ("bear", "puppy", "otter"):
        E(0, 12, 8, 5.5, INK, 0)
    elif kind == "koala":
        P("M-11 4 Q0 -2 11 4 Q12 20 0 22 Q-12 20 -11 4 Z", INK, 0)
    elif kind in ("cat", "fox", "mouse", "hamster", "squirrel", "bunny", "sheep", "hedgehog"):
        P("M-5 12 L5 12 L0 17 Z", INK, F - 1)
    if kind in ("cat",):
        for s in (-1, 1):
            L(s * 54, 16, s * 76, 12, F); L(s * 54, 24, s * 76, 28, F)
    if kind == "duck":
        P("M-20 18 Q0 8 20 18 Q22 34 0 36 Q-22 34 -20 18 Z")
        S("M-16 24 Q0 28 16 24", F)
    if kind == "penguin":
        P("M-9 14 L9 14 L0 25 Z", PAPER, F + .6)
    if kind == "duck":
        S("M-4 -52 C-6 -66 4 -70 2 -80 M6 -52 C10 -62 18 -62 18 -70", D)
    if kind == "hamster":
        for s in (-1, 1):
            E(s * 44, 30, 16, 12, PAPER, F)
    if kind == "otter":
        for s in (-1, 1):
            L(s * 20, 22, s * 40, 18, F); L(s * 20, 28, s * 40, 30, F)


def frog_eyes(expr):
    """Frog eyes sit on top of its head bumps."""
    for s in (-1, 1):
        if expr in ("joy", "sleep"):
            sweep = "-9" if expr == "joy" else "9"
            S(f"M{s * 36 - 10} -34 Q{s * 36} {-34 + int(sweep)} {s * 36 + 10} -34", D)
        else:
            E(s * 36, -36, 9, 11, INK, 0)
            C(s * 36 + 3, -40, 3.4, PAPER, 0)


def head(kind, expr="happy", m="w", ear=""):
    ears_back(kind, ear)
    head_shape(kind)
    if kind == "frog":
        for s in (-1, 1):
            C(s * 36, -36, 25)
        frog_eyes(expr)
        blush(dx=44, y=14)
        S("M-22 8 Q0 26 22 8", D)
        return
    if kind == "puppy":
        head_details(kind, expr, m)
        for s in (-1, 1):
            E(s * 62, 2, 17, 36, PAPER, W, -s * 18)
        return
    if kind == "otter":
        head_details(kind, expr, m)
        return
    head_details(kind, expr, m)


# ------------------------------------------------------------------ outfits
def scarf(stripe=True):
    P("M-46 34 C-20 52 20 52 46 34 L50 50 C20 70 -20 70 -50 50 Z")
    P("M18 56 L40 58 L44 112 L22 112 Z")
    for x in (26, 32, 38):
        L(x, 112, x, 122, F)
    if stripe:
        L(21, 76, 42, 76, F); L(22, 92, 43, 92, F)


def apron():
    P("M-34 58 L34 58 L40 146 C20 154 -20 154 -40 146 Z")
    R(-17, 98, 34, 26, 6, PAPER, F)
    S("M-34 60 C-48 52 -52 44 -46 36 M34 60 C48 52 52 44 46 36", F)


def overalls():
    P("M-48 104 L48 104 C56 126 52 146 40 152 C20 162 -20 162 -40 152 C-52 146 -56 126 -48 104 Z")
    R(-26, 74, 52, 34, 6)
    L(-22, 76, -40, 40, D); L(22, 76, 40, 40, D)
    C(-18, 84, 4, INK, 0); C(18, 84, 4, INK, 0)
    R(-12, 116, 24, 18, 4, PAPER, F)


def sweater(stripes=(96, 120)):
    with Clip(BODY):
        for y in stripes:
            R(-80, y - 7, 160, 14, 0, PAPER, F)
    S("M-28 44 Q0 62 28 44", D)


def raincoat_hood(kind):
    rx, ry = HEAD[kind]
    E(0, -6, rx + 16, ry + 18)


def raincoat_front():
    L(0, 60, 0, 156, D)
    for y in (78, 104, 130):
        C(10, y, 4.5, PAPER, F)


def chef_hat():
    P(scallop([(-44, -50), (-62, -86), (-40, -122), (0, -136), (40, -122), (62, -86), (44, -50)], 0.6, closed=False)
      + " L44 -46 L-44 -46 Z")
    R(-46, -62, 92, 22, 8)


def beanie(pom=True):
    if pom:
        P(scallop(ring(0, -84, 18, 16, 9)))
    P("M-60 -26 C-62 -80 62 -80 60 -26 Z")
    R(-66, -36, 132, 22, 10)
    for x in range(-50, 60, 16):
        L(x, -32, x, -18, F)


def nightcap():
    P("M-58 -28 C-56 -70 -10 -84 30 -80 C70 -76 96 -40 110 -6 C90 -40 60 -54 40 -50 C60 -40 60 -30 58 -28 Z")
    C(112, 0, 14)
    R(-62, -38, 124, 20, 10)


def sunhat():
    E(0, -42, 98, 22)
    P("M-50 -44 C-50 -96 50 -96 50 -44 Z")
    P("M-50 -52 C-20 -46 20 -46 50 -52 L50 -40 C20 -34 -20 -34 -50 -40 Z")
    flower(-40, -52, 12)


def party_hat(dx=0):
    with T(dx, -46, 1, 12):
        P("M-30 0 L0 -84 L30 0 Q0 10 -30 0 Z")
        S("M-16 -40 L14 -32 M-24 -18 L22 -8", F)
        P(scallop(ring(0, -88, 12, 11, 7)))


def bow(x=-40, y=-56, s=1.0, rot=-15):
    with T(x, y, s, rot):
        P("M0 0 C-10 -22 -34 -24 -32 0 C-34 24 -10 22 0 0 Z")
        P("M0 0 C10 -22 34 -24 32 0 C34 24 10 22 0 0 Z")
        E(0, 0, 8, 9)


def glasses(dx=23, y=6):
    for s in (-1, 1):
        C(s * dx, y, 17, "none", D)
    S(f"M{-dx + 17} {y} Q0 {y - 6} {dx - 17} {y}", D)


def headphones():
    tube("M-62 -6 C-64 -84 64 -84 62 -6", 8)
    for s in (-1, 1):
        R(s * 66 - 13, -16, 26, 40, 11)


def flower_crown():
    for i, (x, y) in enumerate(ring(0, 0, 60, 52, 7, 205, 335)):
        flower(x, y, 11 if i % 2 else 13)


def leaf_hat():
    P("M0 -50 C-30 -70 -40 -96 -20 -112 C0 -96 10 -70 0 -50 Z")
    S("M0 -50 C-10 -70 -16 -90 -20 -108", F)
    S("M0 -50 Q8 -60 4 -66", D)


def beret():
    E(8, -48, 64, 22)
    S("M12 -70 l4 -12", D)


def crown_of_ears_bow(kind):
    if kind == "bunny":
        bow(-30, -64, 0.8, -20)
    else:
        bow(-42, -50, 0.8, -15)


# ------------------------------------------------------------------ flower
def flower(x, y, r=14, petals=6, w=D):
    with T(x, y):
        for i in range(petals):
            a = 360 * i / petals
            E(r * 0.75 * math.cos(math.radians(a)), r * 0.75 * math.sin(math.radians(a)),
              r * 0.55, r * 0.38, PAPER, w, a)
        C(0, 0, r * 0.38, PAPER, w)


# ------------------------------------------------------------------ assembly
class _NoTint:
    def __enter__(self):
        pass

    def __exit__(self, *a):
        pass


def critter(kind, x, y, s=1.0, expr="happy", m="w", pose="down", hold=None,
            hat=None, wear=None, ear="", flip=False, rot=0, no_body=False,
            extra=None, colors=None):
    """Draw a whole character.

    hold   : callable drawing a prop at the chest (local coords), drawn before
             the paws so the paws wrap around it.
    hat    : callable or name drawn on/around the head.
    wear   : list of 'scarf' | 'apron' | 'overalls' | 'sweater' | 'raincoat'
    colors : cover only - {'body', 'detail', 'outfit', 'hat', 'prop'} fills
    """
    wear = wear or []
    if isinstance(wear, str):
        wear = [wear]
    c = colors or {}

    def tint(key, detail=None):
        if key not in c:
            return _NoTint()
        return Tint(c[key], c.get(detail, c[key]) if detail else c[key])

    with T(x, y, s, rot, flip):
        if not no_body:
            with tint("body", "detail"):
                tail(kind)
            if "raincoat" in wear:
                with tint("outfit"):
                    raincoat_hood(kind)
            with tint("body", "detail"):
                body(kind)
            with tint("outfit", "outfit2"):
                if "sweater" in wear:
                    sweater()
                if "overalls" in wear:
                    overalls()
                if "apron" in wear:
                    apron()
                if "raincoat" in wear:
                    raincoat_front()
            with tint("body", "detail"):
                feet(kind)
            if hold is not None:
                with tint("prop", "prop2"):
                    hold()
            with tint("body", "detail"):
                arms(kind, pose)
            if "scarf" in wear:
                with tint("outfit", "outfit2"):
                    scarf()
        elif "raincoat" in wear:
            with tint("outfit"):
                raincoat_hood(kind)
        with tint("body", "detail"):
            head(kind, expr, m, ear)
        with tint("hat", "hat2"):
            if callable(hat):
                hat()
            elif hat:
                {"chef": chef_hat, "beanie": beanie, "nightcap": nightcap, "sunhat": sunhat,
                 "party": party_hat, "glasses": glasses, "headphones": headphones,
                 "crown": flower_crown, "leaf": leaf_hat, "beret": beret,
                 "bow": lambda: crown_of_ears_bow(kind)}[hat]()
        if extra:
            extra()
