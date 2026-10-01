"""The 24 scenes of Cozy Little World. Each draws inside the frame
(x 70..780, y 70..950)."""
from ink import *
from critters import critter, flower, bow
from props import *

X0, X1, Y0, Y1 = 70, 780, 70, 950
CX = 425


def room(floor_y, boards=True):
    R(X0 - 10, floor_y, X1 - X0 + 20, Y1 - floor_y + 20, 0)
    R(X0 - 10, floor_y - 18, X1 - X0 + 20, 18, 0, PAPER, D)
    if boards:
        for i, yy in enumerate((floor_y + 34, floor_y + 78)):
            if yy < Y1 - 6:
                L(X0, yy, X1, yy, F)
                for k in range(4):
                    xx = X0 + 90 + k * 180 + (90 if i % 2 else 0)
                    L(xx, yy - (34 if i == 0 else 44), xx, yy, F)


def sky_ground(y, amp=26):
    ground_hill(y, amp)


# ----------------------------------------------------------------- 1
def cafe_table(cx, top, half=250, drop=170):
    P(f"M{cx - half} {top} L{cx + half} {top} L{cx + half + 14} {top + drop} " +
      " ".join(f"Q{cx + half + 14 - (2 * half + 28) * (i + .5) / 8:.1f} {top + drop + 26} "
               f"{cx + half + 14 - (2 * half + 28) * (i + 1) / 8:.1f} {top + drop}" for i in range(8)) + " Z")
    for i in range(4):
        heart(cx - half * 0.66 + i * half * 0.44, top + drop * 0.58, 0.85, 0, D)
    E(cx, top, half + 8, 26)


def morning_latte():
    room(850)
    window(118, 200, 170, 170, inside=lambda: (sun(135, 45, 0.5, face=False), cloud(55, 125, 0.5)))
    wall_frame(655, 225, 120, 100, "heart")
    shelf(570, 745, 340)
    plant_small(610, 340, 0.55)
    jar(700, 340, 0.6)
    bunting(X0, 88, X1, 88, 9, 10)
    critter("bunny", CX, 482, 1.7, expr="happy", m="w", pose="hold",
            hold=lambda: mug(0, 84, 0.78, deco="heart", steamy=False), wear=["sweater"], hat="bow")
    cafe_table(CX, 700)
    with T(250, 690):
        E(0, 0, 72, 14)
        croissant(0, -20, 0.8)
    cupcake(600, 700, 0.8)
    for xx, yy in ((150, 470), (720, 470), (700, 560)):
        sparkle(xx, yy, 1.1)


# ----------------------------------------------------------------- 2
def bakery():
    room(880, boards=False)
    awning(X0, X1, Y0 - 10, 80, 8)
    shelf(95, 300, 320)
    bread(150, 320, 0.6); bread(245, 320, 0.52)
    shelf(550, 755, 320)
    jar(590, 320, 0.62, "cookie"); jar(655, 320, 0.62); jar(718, 320, 0.62, "cookie")
    shelf(95, 300, 480)
    baguette(198, 460, 0.7, -6)
    shelf(550, 755, 480)
    croissant(652, 458, 0.72)
    critter("bear", CX, 478, 1.72, expr="joy", m="open", pose="wave", wear=["apron"], hat="chef")
    counter(X0 + 10, X1 - 10, 735, Y1 + 10, tiles=False)
    for i in range(1, 8):
        L(X0 + 10 + i * 88.75, 770, X0 + 10 + i * 88.75, Y1, F)
    E(CX, 850, 150, 62)
    E(CX, 850, 134, 48, PAPER, F)
    text(CX, 868, "Bakery", 56, 2.6)
    cake(185, 735, 0.62, candles=0)
    with T(320, 735):
        E(0, -4, 54, 10)
        donut(0, -26, 0.8)
    for i, xx in enumerate((545, 640)):
        cupcake(xx, 735, 0.62, cherry=(i == 0))
    bread(730, 735, 0.45)


# ----------------------------------------------------------------- 3
def bookstore():
    room(840)
    bookshelf(X0 + 10, 840, 210, 620, rows=4, seed=3)
    bookshelf(X1 - 220, 840, 210, 620, rows=4, seed=8)
    S(f"M{CX} {Y0} L{CX} 170", D)
    P(f"M{CX - 70} 230 Q{CX} 140 {CX + 70} 230 Z")
    C(CX, 236, 12)
    armchair(CX, 930, 1.45)
    critter("cat", CX, 560, 1.45, expr="happy", m="smile", pose="hold", hat="glasses",
            hold=lambda: open_book(0, 120, 0.62), wear=["scarf"])
    armchair_arms(CX, 930, 1.45)
    book_stack(170, 935, 0.7, 3)
    mug(170, 830, 0.62, deco="stripes")
    with T(680, 940):
        plant_small(0, 0, 0.9)


# ----------------------------------------------------------------- 4
def rainy_window():
    def outside():
        cloud(80, 80, 0.9); cloud(330, 60, 0.75)
        for i in range(9):
            raindrop(40 + i * 46, 170 + (i % 3) * 60, 0.8)
        bush(120, 380, 220, 70); bush(330, 390, 200, 60)
    R(X0 - 10, Y0 - 10, X1 - X0 + 20, 120, 0)
    for i in range(6):
        L(X0 + 60 + i * 120, Y0, X0 + 60 + i * 120, Y0 + 110, F)
    window(185, 230, 480, 400, curtains=True, inside=outside, sill=False)
    R(X0 - 10, 820, X1 - X0 + 20, 150, 0)
    R(X0 - 10, 806, X1 - X0 + 20, 24, 10)
    E(160, 784, 70, 30)
    S("M115 780 Q160 790 205 780", F)
    critter("fox", CX, 548, 1.6, expr="happy", m="w", pose="hold", wear=["sweater"],
            hold=lambda: mug(0, 86, 0.75, cocoa=True, steamy=False, deco="paw"))
    plant_small(700, 806, 0.75)
    book_stack(600, 806, 0.5, 2)
    for xx in (180, 420, 660):
        heart(xx, 890, 0.9, 0, D)


# ----------------------------------------------------------------- 5
def picnic():
    sky_ground(560, 34)
    sun(690, 170, 0.75)
    cloud(220, 160, 0.9); cloud(470, 120, 0.6)
    tree(160, 590, 0.95, h=170)
    bush(700, 560, 180, 70)
    picnic_blanket(CX, 790, 720, 260, 7)
    critter("bunny", 285, 555, 1.3, expr="joy", m="open", pose="hold", hat="sunhat",
            hold=lambda: strawberry(0, 82, 0.6))
    critter("bear", 580, 575, 1.3, expr="happy", m="w", pose="hold",
            hold=lambda: cupcake(0, 116, 0.55, cherry=True))
    basket(170, 935, 0.85, fill=lambda: (baguette(30, -80, 0.6, -30), apple(-34, -70, 0.5)))
    glass(CX, 905, 0.9)
    with T(640, 900):
        E(0, 0, 80, 18)
        for i, xx in enumerate((-40, 0, 40)):
            strawberry(xx, -26, 0.5, -20 + i * 20)
    butterfly(440, 330, 0.9, 10)
    for xx, yy in ((90, 680), (770, 640), (560, 640)):
        grass(xx, yy, 0.9)


# ----------------------------------------------------------------- 6
def campfire_night():
    R(X0 - 10, Y0 - 10, X1 - X0 + 20, Y1 - Y0 + 20, 0)
    moon(640, 200, 0.75, face=True, r=-10)
    stars_field([(140, 130), (270, 210), (420, 120), (520, 250), (180, 300), (760, 330), (350, 330)], 0.6)
    ground_hill(600, 20)
    pine(110, 640, 0.7); pine(740, 630, 0.62); pine(650, 610, 0.45)
    tent(240, 690, 0.95)
    lantern(400, 690, 0.8)
    for xx in (240, 610):
        R(xx - 120, 820, 240, 50, 22)
        E(xx + 120, 845, 14, 25, PAPER, W)
        E(xx + 120, 845, 6, 12, PAPER, F)
    critter("raccoon", 215, 612, 1.2, expr="happy", m="open", pose="hold",
            hold=lambda: (tube("M20 80 L140 150", 6), E(148, 156, 15, 13, PAPER, D, 30)))
    critter("fox", 635, 612, 1.2, expr="joy", m="w", pose="hold", wear=["scarf"], flip=True,
            hold=lambda: (tube("M20 80 L140 150", 6), E(148, 156, 15, 13, PAPER, D, 30)))
    campfire(CX, 900, 0.95)


# ----------------------------------------------------------------- 7
def garden_helper():
    sky_ground(640, 18)
    sun(150, 160, 0.7)
    cloud(560, 150, 0.85)
    fence(X0, X1, 640, 130)
    butterfly(320, 260, 0.9, -15)
    butterfly(690, 330, 0.75, 20)
    for i, xx in enumerate((520, 600, 680, 750)):
        (tulip if i % 2 == 0 else daisy)(xx, 880 - (i % 2) * 20, 130 + (i % 3) * 20)
    sunflower(720, 700, 160, 0.9)
    critter("frog", 300, 575, 1.6, expr="joy", m="open", pose="hold", wear=["overalls"], hat="leaf",
            hold=lambda: watering_can(26, 120, 0.85, -14))
    for dx, dy in ((0, 0), (26, 30), (-10, 52), (34, 74), (8, 96)):
        raindrop(520 + dx, 690 + dy, 0.7)
    mushroom(130, 920, 0.7)
    for xx in (220, 420, 560):
        grass(xx, 930, 1.0)
    flower(170, 820, 16)


# ----------------------------------------------------------------- 8
def sweet_dreams():
    room(880, boards=False)
    window(560, 140, 170, 160, curtains=True, night=True)
    wall_frame(190, 220, 110, 90, "flower")
    string_lights(X0, 105, 470, 105, 6, 20)
    bed(CX, 960, 1.3)
    critter("panda", CX, 600, 1.8, expr="sleep", m="smile", no_body=True)
    bed_blanket(CX, 960, 1.3, top=-210)
    for sx in (-1, 1):
        E(CX + sx * 80, 712, 34, 22)
    for xx, yy, k in ((640, 470, 1), (700, 420, 0.8), (750, 375, 0.6)):
        with T(xx, yy, k):
            S("M-12 -12 L12 -12 L-12 12 L12 12", W)
    for xx, yy in ((140, 420), (320, 380), (110, 330)):
        star(xx, yy, 0.55, 15, D)


# ----------------------------------------------------------------- 9
def cupcake_day():
    R(X0 - 10, Y0 - 10, X1 - X0 + 20, 700, 0)
    for i in range(8):
        L(X0 + i * 90, Y0, X0 + i * 90, 760, F)
    for j in range(8):
        L(X0, Y0 + 30 + j * 90, X1, Y0 + 30 + j * 90, F)
    shelf(110, 380, 230)
    jar(160, 230, 0.7, "cookie"); jar(240, 230, 0.6); jar(315, 230, 0.7, "heart")
    bunting(430, 120, X1 + 20, 110, 6, 20)
    R(X0 - 10, 760, X1 - X0 + 20, 220, 0)
    R(X0 - 10, 748, X1 - X0 + 20, 24, 8)
    cupcake(570, 760, 3.0, cherry=True)
    critter("mouse", 250, 515, 1.35, expr="joy", m="open", pose="up", wear=["apron"], hat="chef")
    cookie(130, 850, 1.0)
    cupcake(220, 930, 0.7)
    for xx, yy in ((300, 860), (360, 900), (420, 850)):
        sparkle(xx, yy, 1.1)
    heart(760, 820, 0.8, 15, D)


# ----------------------------------------------------------------- 10
def strawberry_patch():
    sky_ground(560, 20)
    sun(640, 180, 0.8)
    cloud(200, 150, 0.8)
    fence(X0, X1, 560, 100)
    for row, yy in enumerate((660, 790, 930)):
        for k in range(5):
            xx = X0 + 30 + k * 170 + (80 if row % 2 else 0)
            if 300 < xx < 560 and row < 2:
                continue
            bush(xx, yy, 140, 60)
            strawberry(xx - 30, yy - 10, 0.45, -10)
            strawberry(xx + 26, yy - 4, 0.42, 14)
    critter("hamster", CX, 560, 1.5, expr="happy", m="open", pose="hold", hat="sunhat",
            hold=lambda: basket(0, 150, 0.55, fill=lambda: (strawberry(-30, -84, 0.6, -20),
                                                            strawberry(10, -92, 0.6), strawberry(46, -80, 0.55, 20))))
    butterfly(170, 360, 0.8, -10)


# ----------------------------------------------------------------- 11
def puddle_splash():
    cloud(190, 150, 1.05, face=True); cloud(590, 130, 1.1, face="sleep")
    for i in range(10):
        raindrop(110 + i * 70, 270 + (i % 3) * 60, 0.9)
    sky_ground(700, 10)
    for xx in (110, 170, 720, 660):
        grass(xx, 740, 1.0)
    puddle(CX, 850, 270, 50)
    def brolly():
        umbrella(64, 52, 1.0, 4)
        E(64, 30, 13, 24, PAPER, W, 35)
    critter("duck", CX, 610, 1.5, expr="joy", m="open", pose="wave", wear=["raincoat"], extra=brolly)
    for dx, dy in ((-170, -20), (-140, -70), (-200, -60), (150, -60), (180, -15), (120, -95), (-100, -100)):
        raindrop(CX + dx, 850 + dy, 1.0)
    critter("frog", 690, 850, 0.55, expr="happy", m="w", no_body=True)
    flower(130, 900, 22); flower(200, 930, 16)
    flower(740, 930, 18)


# ----------------------------------------------------------------- 12
def tea_party():
    sky_ground(560, 10)
    cloud(170, 140, 0.7); cloud(650, 120, 0.8)
    bunting(X0, 100, X1, 100, 9, 26)
    bush(150, 560, 220, 110); bush(700, 560, 220, 110)
    for xx in (110, 200, 650, 740):
        flower(xx, 500 - (xx % 3) * 6, 15)
    critter("cat", 250, 545, 1.32, expr="happy", m="w", pose="hold", hat="bow",
            hold=lambda: teacup(0, 112, 0.6))
    critter("bunny", 605, 545, 1.32, expr="joy", m="open", pose="wave", ear="flop")
    R(X0 + 20, 720, X1 - X0 - 40, 26, 8)
    P(f"M{X0 + 30} 742 L{X1 - 30} 742 L{X1 - 30} 860 " +
      " ".join(f"Q{X1 - 30 - 70 * i - 35} 890 {X1 - 30 - 70 * (i + 1)} 860" for i in range(9)) + " Z")
    for xx in range(X0 + 65, X1 - 40, 70):
        C(xx, 840, 6, PAPER, F)
    teapot(CX, 730, 0.95)
    cake(600, 732, 0.42, candles=0)
    with T(225, 732):
        E(0, -6, 70, 12)
        for i, xx in enumerate((-36, 0, 36)):
            cookie(xx, -24, 0.6)
    L(X0 + 120, 860, X0 + 120, Y1 + 10, W); L(X1 - 120, 860, X1 - 120, Y1 + 10, W)


# ----------------------------------------------------------------- 13
def pancake_sunday():
    room(860)
    window(110, 150, 200, 190, inside=lambda: sun(150, 60, 0.6, face=False))
    clock(660, 200, 50)
    shelf(580, 760, 360); jar(615, 360, 0.55); plant_small(700, 360, 0.5)
    critter("bear", CX, 470, 1.7, expr="joy", m="yum", pose="up", wear=["sweater"])
    cafe_table(CX, 700, half=300, drop=200)
    with T(235, 690):
        pancakes(0, 0, 0.85)
    mug(620, 650, 0.8, deco="stripes")
    strawberry(405, 670, 0.6, -15); strawberry(470, 676, 0.55, 15); strawberry(700, 672, 0.55, 5)


# ----------------------------------------------------------------- 14
def cozy_knitting():
    room(780)
    window(100, 150, 200, 210, inside=lambda: [sparkle(x, y, 1.0) for x, y in
                                                ((40, 40), (140, 70), (70, 140), (160, 170), (110, 110))])
    floor_lamp(700, 780, 0.9)
    wall_frame(470, 200, 120, 100, "mountain")
    rug(CX, 880, 330, 60)
    pouf(CX, 860, 1.3)
    critter("sheep", CX, 560, 1.55, expr="happy", m="w", pose="hold", ear="",
            hold=lambda: (S("M-30 70 L40 100", D), S("M30 70 L-40 100", D),
                          P("M-36 100 L36 100 L40 150 L-40 150 Z", PAPER, D),
                          S("M-30 112 L30 112 M-32 126 L32 126 M-34 140 L34 140", F)))
    basket(160, 930, 0.7, fill=lambda: (yarn(-30, -80, 0.6), yarn(26, -86, 0.55)))
    tube("M470 790 C540 860 580 880 600 860", 4)
    yarn(610, 870, 0.65)
    critter("cat", 690, 905, 0.42, expr="sleep", m="smile", no_body=True)


# ----------------------------------------------------------------- 15
def flower_shop():
    R(X0 + 30, 180, X1 - X0 - 60, 700, 0)
    awning(X0 + 10, X1 - 10, 160, 70, 8)
    sign_board(CX, 125, "Flowers", 240, 70, size=46)
    window(130, 300, 180, 200, curtains=False, sill=True,
           inside=lambda: (plant_small(60, 200, 0.7), cactus(140, 200, 0.7)))
    R(560, 300, 170, 330, 10)
    R(580, 320, 130, 120, 8, PAPER, D)
    C(690, 480, 8, PAPER, D)
    heart(645, 380, 1.0)
    R(X0 - 10, 880, X1 - X0 + 20, 100, 0)
    critter("hedgehog", CX, 585, 1.5, expr="joy", m="open", pose="hold", wear=["apron"],
            hold=lambda: (S("M-10 120 L-30 40 M0 120 L0 30 M10 120 L30 44", D),
                          tulip(-30, 40, 1, 0.6), flower(0, 18, 16), tulip(30, 46, 1, 0.6),
                          P("M-36 74 L36 74 L10 140 L-10 140 Z")))
    bucket(150, 900, 0.8, flowers=lambda: [tulip(xx, -60, 70 + (i % 2) * 20) for i, xx in enumerate((-30, 0, 30))])
    bucket(270, 905, 0.65, flowers=lambda: [daisy(xx, -60, 70 + (i % 2) * 18) for i, xx in enumerate((-26, 0, 26))])
    bucket(680, 900, 0.85, flowers=lambda: sunflower(0, -60, 110, 0.7))
    plant_small(570, 900, 0.75)


# ----------------------------------------------------------------- 16
def stargazing():
    R(X0 - 10, Y0 - 10, X1 - X0 + 20, Y1 - Y0 + 20, 0)
    moon(230, 210, 1.0, face=True)
    stars_field([(400, 120), (530, 200), (690, 140), (620, 300), (460, 300), (750, 240),
                 (130, 360), (360, 400), (720, 420)], 0.65)
    cloud(500, 330, 0.6, face="sleep")
    P(f"M{X0 - 20} 700 C200 600 520 590 {X1 + 20} 680 L{X1 + 20} 1000 L{X0 - 20} 1000 Z")
    pine(130, 760, 0.42)
    telescope(590, 540, 0.95)
    critter("penguin", 300, 600, 1.5, expr="happy", m="o", pose="wave", wear=["scarf"], hat="beanie")
    lantern(690, 880, 0.9)
    for xx, yy in ((140, 870), (500, 900), (600, 820)):
        grass(xx, yy, 1)


# ----------------------------------------------------------------- 17
def soup_day():
    room(910, boards=False)
    for i in range(7):
        L(X0, 420 + i * 70, X1, 420 + i * 70, F)
    shelf(95, 245, 240)
    jar(135, 240, 0.55); jar(205, 240, 0.55, "heart")
    for i, xx in enumerate((520, 590, 660, 730)):
        L(xx, Y0, xx, 150, F)
    with T(520, 150): C(0, 30, 28); L(0, 0, 0, 2, D)
    with T(590, 150): tube("M0 0 L0 70", 10); E(0, 90, 16, 22)
    with T(660, 150): tube("M0 0 L0 60", 8); poly([(-16, 60), (16, 60), (12, 100), (-12, 100)])
    with T(730, 150): C(0, 30, 28); L(0, 0, 0, 2, D)
    critter("bunny", 390, 452, 1.55, expr="joy", m="w", pose="hold", wear=["apron"], hat="bow",
            hold=lambda: tube("M20 84 L70 210", 9))
    R(X0 + 40, 680, X1 - X0 - 80, 250, 12)
    R(X0 + 20, 664, X1 - X0 - 40, 24, 10)
    R(X0 + 110, 740, 300, 160, 12, PAPER, D)
    R(X0 + 140, 770, 240, 100, 10, PAPER, F)
    for xx in (520, 600, 680):
        C(xx, 760, 18)
        L(xx, 748, xx, 760, F)
    soup_pot(400, 664, 1.0)
    carrot(640, 600, 0.9, 70)
    carrot(700, 620, 0.85, 80)


# ----------------------------------------------------------------- 18
def plant_parent():
    room(800)
    window(300, 140, 250, 230, curtains=False,
           inside=lambda: (cloud(70, 70, 0.6), sun(210, 50, 0.4, face=False)))
    shelf(110, 260, 300); plant_small(150, 300, 0.55); cactus(220, 300, 0.6)
    shelf(590, 750, 300); plant_small(630, 300, 0.55); jar(700, 300, 0.6)
    S("M680 70 L680 130", D)
    with T(680, 210):
        S("M-30 -60 L0 -82 L30 -60", D)
        P("M-30 -60 L30 -60 L24 -10 L-24 -10 Z")
        for i, dx in enumerate((-28, -10, 10, 28)):
            S(f"M{dx} -10 Q{dx * 1.4} 40 {dx * 1.2} {90 + (i % 2) * 40}", D)
            for k in range(3):
                leaf(dx * 1.25, 20 + k * 30 + (i % 2) * 10, 0.42, (-1) ** i * 40)
    monstera(150, 880, 0.9)
    cactus(720, 900, 1.0)
    critter("koala", CX, 575, 1.55, expr="happy", m="w", pose="hold", wear=["overalls"],
            hold=lambda: plant_small(0, 130, 0.65))
    plant_small(570, 930, 0.75)
    heart(270, 600, 0.8, -20, D)
    sparkle(590, 620, 1.1)


# ----------------------------------------------------------------- 19
def mushroom_cottage():
    sky_ground(700, 26)
    cloud(170, 140, 0.8); cloud(640, 110, 0.7)
    sun(720, 230, 0.55)
    R(560, 160, 60, 140, 8)
    for i, (xx, yy) in enumerate(((600, 140), (620, 100), (600, 66))):
        C(xx, yy, 14 + i * 4, PAPER, D)
    P("M240 720 C230 600 240 440 260 400 L560 400 C580 440 590 600 580 720 Z")
    P("M120 420 C110 200 710 200 700 420 C600 450 220 450 120 420 Z")
    for xx, yy, rr in ((240, 320, 36), (420, 270, 30), (590, 330, 34), (330, 380, 20), (520, 400, 18)):
        C(xx, yy, rr, PAPER, D)
    P("M360 720 L360 590 C360 530 460 530 460 590 L460 720 Z")
    C(440, 650, 7, PAPER, D)
    for xx in (300, 520):
        C(xx, 520, 34); L(xx - 34, 520, xx + 34, 520, D); L(xx, 486, xx, 554, D)
    for i in range(4):
        E(410 + (i % 2) * 30 - 15, 760 + i * 50, 50 - i * 2, 16)
    critter("squirrel", 190, 660, 1.15, expr="joy", m="open", pose="wave")
    mushroom(660, 760, 1.0); mushroom(730, 790, 0.6, 10)
    for xx, yy in ((140, 860), (660, 880), (560, 930)):
        flower(xx, yy, 18)
    butterfly(130, 450, 0.8)


# ----------------------------------------------------------------- 20
def lemonade_stand():
    sky_ground(640, 14)
    sun(160, 170, 0.8)
    cloud(520, 130, 0.8)
    tree(700, 640, 0.75, h=200)
    for ax, ay in ((660, 330), (740, 300), (700, 370)):
        lemon(ax, ay, 0.45)
    L(170, 360, 170, 700, W + 4); L(680, 360, 680, 700, W + 4)
    awning(150, 700, 300, 64, 7)
    critter("puppy", CX, 505, 1.45, expr="joy", m="open", pose="up")
    R(150, 680, 550, 260, 10)
    R(140, 664, 570, 26, 8)
    sign_board(CX, 790, "Lemonade", 340, 90, size=58)
    for xx in (200, 650):
        lemon(xx, 890, 0.7, 15)
    lemonade_pitcher(270, 664, 0.9)
    glass(530, 664, 0.85); glass(610, 664, 0.85, straw=False)
    for xx in (110, 760):
        grass(xx, 930, 1)


# ----------------------------------------------------------------- 21
def birthday():
    room(860, boards=True)
    bunting(X0, 96, X1, 96, 10, 20)
    for i, (bx, by) in enumerate(((130, 270), (200, 220), (720, 260), (650, 210))):
        balloon(bx, by, 0.85, 200, (-8 if i < 2 else 8))
    critter("duck", 170, 620, 1.0, expr="joy", m=None, pose="up", hat="party")
    critter("cat", 680, 620, 1.0, expr="wink", m="open", pose="wave", hat="party", flip=True)
    critter("bunny", CX, 400, 1.3, expr="joy", m="open", pose="up", hat="party")
    R(220, 700, 410, 26, 8)
    R(250, 726, 350, 200, 10)
    text(CX, 850, "Hooray!", 76, 3.2)
    cake(CX, 700, 0.72, candles=3)
    gift(150, 930, 0.8); gift(700, 935, 0.7)
    for xx, yy in ((290, 300), (570, 300)):
        sparkle(xx, yy, 1.2)


# ----------------------------------------------------------------- 22
def pumpkin_patch():
    sky_ground(600, 22)
    sun(650, 160, 0.7)
    cloud(220, 140, 0.8)
    tree(130, 610, 0.7, h=180)
    fence(330, X1, 600, 100)
    for xx, yy, rr in ((330, 240, 20), (420, 300, -30), (720, 360, 60), (560, 300, 10), (330, 400, -60)):
        leaf(xx, yy, 1.0, rr)
    hay_bale(CX, 820, 1.3)
    critter("fox", CX, 500, 1.3, expr="happy", m="w", pose="hold", wear=["scarf"], hat="beanie",
            hold=lambda: pumpkin(0, 140, 0.55))
    pumpkin(160, 900, 1.0, face=True)
    pumpkin(700, 880, 0.8)
    pumpkin(610, 930, 0.55)
    for xx, yy, rr in ((280, 900, 40), (560, 850, -20), (110, 760, 80)):
        leaf(xx, yy, 0.8, rr)


# ----------------------------------------------------------------- 23
def sleepover_fort():
    room(800)
    window(560, 130, 170, 160, curtains=False, night=True)
    wall_frame(170, 190, 110, 90, "heart")
    P("M80 820 C90 600 160 380 425 330 C690 380 760 600 770 820 Z")
    S("M425 330 C380 500 360 700 370 820", D)
    S("M425 330 C470 500 490 700 480 820", D)
    P("M300 820 C310 640 360 520 425 500 C490 520 540 640 550 820 Z")
    string_lights(140, 560, 710, 560, 9, -60)
    critter("axolotl", 350, 640, 0.98, expr="happy", m="open", pose="hold",
            hold=lambda: popcorn(0, 150, 0.55))
    critter("otter", 510, 650, 0.98, expr="joy", m="w", pose="wave")
    for xx, rr in ((150, -10), (690, 10)):
        R(xx - 70, 830, 140, 70, 26, PAPER, W, rr)
        heart(xx, 865, 0.8, rr, D)
    for xx, yy in ((300, 900), (560, 920)):
        star(xx, yy, 0.7)


# ----------------------------------------------------------------- 24
def goodnight():
    R(X0 - 10, Y0 - 10, X1 - X0 + 20, Y1 - Y0 + 20, 0)
    stars_field([(130, 140), (300, 110), (700, 150), (590, 100), (160, 330), (745, 330),
                 (110, 520), (760, 560), (450, 120), (250, 250)], 0.7)
    cloud(165, 700, 1.2, face="sleep"); cloud(680, 720, 1.1, face="sleep")
    with T(CX + 30, 540, 3.2, -30):
        P("M10 -80 A80 80 0 1 0 70 50 A64 64 0 1 1 10 -80 Z")
    critter("bunny", 505, 420, 1.15, expr="sleep", m="smile", pose="hold", hat="nightcap",
            hold=lambda: star(0, 92, 1.3), rot=12)
    cloud(CX, 890, 1.5, face="sleep")
    for xx, yy in ((300, 650), (560, 790)):
        sparkle(xx, yy, 1.2)


SCENES = [
    ("Morning Latte", morning_latte),
    ("Fresh From the Bakery", bakery),
    ("The Bookshop Nook", bookstore),
    ("Rainy Day Cocoa", rainy_window),
    ("Picnic in the Park", picnic),
    ("Campfire Marshmallows", campfire_night),
    ("Little Garden Helper", garden_helper),
    ("Sweet Dreams", sweet_dreams),
    ("Cupcake Day", cupcake_day),
    ("Strawberry Patch", strawberry_patch),
    ("Puddle Splash", puddle_splash),
    ("Garden Tea Party", tea_party),
    ("Pancake Sunday", pancake_sunday),
    ("Cozy Knitting Corner", cozy_knitting),
    ("The Little Flower Shop", flower_shop),
    ("Stargazing", stargazing),
    ("Soup Simmering", soup_day),
    ("Plant Parent", plant_parent),
    ("Mushroom Cottage", mushroom_cottage),
    ("Lemonade Stand", lemonade_stand),
    ("Birthday Surprise", birthday),
    ("Pumpkin Patch", pumpkin_patch),
    ("Blanket Fort Sleepover", sleepover_fort),
    ("Goodnight, Cozy World", goodnight),
]
