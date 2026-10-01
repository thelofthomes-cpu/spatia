"""Build every deliverable for Cozy Little World into ../output.

    python3 build.py
"""
import os
import sys

from pypdf import PdfWriter, PdfReader

import ink
from ink import *
from critters import critter
from props import *
import page
import scenes
import cover

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "output")
TMP = os.path.join(OUT, "_pages")
TITLE = "Cozy Little World"
SUB = "24 Cute &amp; Easy Coloring Pages"


def body_text(x, y, s, size=24, weight=600, anchor="middle", fill="#333"):
    raw(f'<text x="{x}" y="{y}" font-family="Baloo 2" font-weight="{weight}" font-size="{size}" '
        f'text-anchor="{anchor}" fill="{fill}">{s}</text>')


def doc(fn):
    ink.reset()
    fn()
    return page.svg_doc(ink.take())


def title_page():
    text(425, 250, "Cozy Little", 118, 4.5)
    text(425, 380, "World", 140, 4.5)
    text(425, 470, SUB, 44, 2.6)
    critter("bear", 225, 680, 1.0, expr="joy", m="open", pose="wave")
    critter("bunny", 425, 650, 1.2, expr="happy", m="w", pose="hold",
            hold=lambda: heart(0, 90, 1.2))
    critter("cat", 625, 680, 1.0, expr="wink", m="open", pose="wave", flip=True)
    for xx, yy in ((150, 170), (720, 150), (110, 560), (750, 560)):
        sparkle(xx, yy, 1.4)
    for xx in (120, 330, 520, 730):
        flower(xx, 930, 22)


def copyright_page():
    lines = [
        ("Cozy Little World", 34, 800),
        ("24 Cute &amp; Easy Coloring Pages", 26, 700),
        ("", 20, 600),
        ("Copyright © 2026 Diamond Spade. All rights reserved.", 20, 600),
        ("No part of this book may be reproduced, distributed or transmitted", 20, 600),
        ("in any form without the prior written permission of the publisher,", 20, 600),
        ("except for personal, non-commercial coloring use.", 20, 600),
        ("", 20, 600),
        ("All characters and illustrations are original works.", 20, 600),
        ("", 20, 600),
        ("Coloring tips", 28, 800),
        ("• Each illustration is printed on one side only.", 20, 600),
        ("• Slip a sheet of card behind the page when using markers.", 20, 600),
        ("• Try colored pencils for soft blush and gradients.", 20, 600),
        ("• There are no rules – pink bears and blue bunnies are welcome!", 20, 600),
    ]
    y = 560
    for t, sz, wt in lines:
        body_text(425, y, t, sz, wt)
        y += sz + 14
    critter("hamster", 425, 330, 0.9, expr="joy", m="open", pose="hold",
            hold=lambda: open_book(0, 120, 0.6))


def belongs_page():
    P("M150 230 H700 A40 40 0 0 1 740 270 V700 A40 40 0 0 1 700 740 H150 "
      "A40 40 0 0 1 110 700 V270 A40 40 0 0 1 150 230 Z")
    text(425, 410, "This Book", 88, 3.6)
    text(425, 510, "Belongs To", 88, 3.6)
    L(200, 650, 650, 650, W)
    bunting(110, 240, 740, 240, 9, 16)
    critter("bunny", 260, 870, 0.9, expr="joy", m="open", pose="up")
    critter("frog", 590, 880, 0.9, expr="happy", m="w", pose="hold", hold=lambda: heart(0, 90, 1.0))
    for xx, yy in ((420, 820), (440, 920), (760, 790)):
        sparkle(xx, yy, 1.3)
    heart(110, 900, 1.2, -15)


def color_test_page():
    text(425, 150, "Test Your Colors", 74, 3.4)
    body_text(425, 210, "Try your pencils, markers and gel pens here first", 26, 700)
    shapes = [heart, star, lambda x, y, s: C(x, y, 30 * s), lambda x, y, s: sparkle(x, y, 2.6 * s, W)]
    for row in range(5):
        for col in range(5):
            x, y = 165 + col * 130, 330 + row * 135
            k = (row + col) % 4
            if k == 0:
                heart(x, y + 6, 2.4)
            elif k == 1:
                star(x, y, 2.0)
            elif k == 2:
                C(x, y, 42)
            else:
                R(x - 40, y - 40, 80, 80, 18)
    critter("cat", 690, 960, 0.6, expr="happy", m="w", no_body=True)
    critter("bunny", 160, 990, 0.6, expr="joy", m="w", no_body=True)


def thanks_page():
    text(425, 250, "Thank You!", 110, 4.2)
    for i, l in enumerate(["We hope your cozy little world", "brought you a calm, happy moment.",
                           "", "If you enjoyed coloring these pages,",
                           "a short review would mean the world to us!"]):
        body_text(425, 340 + i * 40, l, 30, 700)
    critter("bear", 220, 720, 1.0, expr="joy", m="open", pose="up")
    critter("duck", 425, 740, 0.95, expr="happy", m=None, pose="wave", hat="party")
    critter("fox", 630, 720, 1.0, expr="joy", m="w", pose="up", flip=True)
    for xx, yy in ((120, 160), (740, 160), (130, 980), (720, 990)):
        heart(xx, yy, 1.3, 10)


def blank():
    pass


def main():
    os.makedirs(TMP, exist_ok=True)
    prev = os.path.join(OUT, "previews")
    os.makedirs(prev, exist_ok=True)

    svgs = {}

    def emit(name, svg, png=False):
        p = os.path.join(TMP, name + ".pdf")
        svgs[p] = (name, svg)
        page.to_pdf(svg, p)
        if png:
            page.to_png(svg, os.path.join(prev, name + ".png"), 1275)
        return p

    blank_pdf = emit("blank", doc(blank))
    front_matter = [emit("00-title", doc(title_page), True),
                    emit("00-copyright", doc(copyright_page)),
                    emit("00-belongs", doc(belongs_page), True),
                    emit("00-colortest", doc(color_test_page), True)]
    scene_pdfs = []
    for i, (title, fn) in enumerate(scenes.SCENES, 1):
        print(f"  page {i:2d}  {title}")
        scene_pdfs.append(emit(f"page-{i:02d}", page.scene_page(fn, title.replace("&", "&amp;")), True))
    thanks = emit("00-thanks", doc(thanks_page), True)

    # KDP paperback interior: every illustration on a right-hand page with a blank back
    kdp = [front_matter[0], front_matter[1], front_matter[2], blank_pdf, front_matter[3], blank_pdf]
    for p in scene_pdfs:
        kdp += [p, blank_pdf]
    kdp += [thanks, blank_pdf]
    write(kdp, os.path.join(OUT, "CozyLittleWorld_KDP_Interior_8.5x11.pdf"))

    # Etsy / printable download: no blank backs
    etsy = [front_matter[0], front_matter[3]] + scene_pdfs + [thanks]
    write(etsy, os.path.join(OUT, "CozyLittleWorld_Printable_US-Letter.pdf"))

    # Covers
    svg, w, h, spine = cover.wrap_svg(len(kdp))
    page.to_pdf(svg, os.path.join(OUT, "CozyLittleWorld_KDP_Cover_Wraparound.pdf"))
    page.to_png(svg, os.path.join(prev, "cover-wraparound.png"), 2400)
    page.to_pdf(cover.front_trim_svg(), os.path.join(OUT, "CozyLittleWorld_Front_Cover.pdf"))
    page.to_png(cover.front_trim_svg(), os.path.join(OUT, "CozyLittleWorld_Front_Cover.png"), 2550)
    print(f"interior pages: {len(kdp)}  |  cover {w:.3f} x {h:.3f} in, spine {spine:.4f} in")
    contact_sheet(prev)
    full_book(kdp, svgs, blank_pdf)
    for f in os.listdir(TMP):
        os.remove(os.path.join(TMP, f))
    os.rmdir(TMP)


def full_book(kdp, svgs, blank_pdf):
    """The whole book in reading order (front cover, interior, back cover) as
    one PDF, plus a 300 dpi PNG of every page that has content."""
    d = os.path.join(OUT, "full-book")
    png_dir = os.path.join(d, "png")
    os.makedirs(png_dir, exist_ok=True)
    for f in os.listdir(png_dir):
        os.remove(os.path.join(png_dir, f))
    front_svg, back_svg = cover.front_trim_svg(), cover.back_trim_svg()
    fpdf, bpdf = os.path.join(TMP, "cover-front.pdf"), os.path.join(TMP, "cover-back.pdf")
    page.to_pdf(front_svg, fpdf)
    page.to_pdf(back_svg, bpdf)
    write([fpdf] + kdp + [bpdf], os.path.join(d, "CozyLittleWorld_Full_Book.pdf"))

    page.to_png(front_svg, os.path.join(png_dir, "000-front-cover.png"), 2550)
    n = 0
    for i, p in enumerate(kdp, 1):
        if p == blank_pdf:
            continue
        name = svgs[p][0].replace("00-", "")
        page.to_png(svgs[p][1], os.path.join(png_dir, f"{i:03d}-{name}.png"), 2550)
        n += 1
    page.to_png(back_svg, os.path.join(png_dir, f"{len(kdp) + 1:03d}-back-cover.png"), 2550)
    print(f"full book: {len(kdp) + 2} PDF pages, {n + 2} PNGs (blank backs skipped)")


def write(paths, dest):
    wr = PdfWriter()
    for p in paths:
        wr.append(PdfReader(p))
    wr.add_metadata({"/Title": f"{TITLE}: 24 Cute & Easy Coloring Pages", "/Author": "Diamond Spade"})
    with open(dest, "wb") as f:
        wr.write(f)


def contact_sheet(prev):
    from PIL import Image
    ims = [os.path.join(prev, f"page-{i:02d}.png") for i in range(1, 25)]
    w, h = 340, 440
    sheet = Image.new("RGB", (w * 6 + 70, h * 4 + 50), "#fff3e4")
    for k, p in enumerate(ims):
        im = Image.open(p).convert("RGB").resize((w - 20, h - 20))
        sheet.paste(im, (20 + (k % 6) * (w + 2), 20 + (k // 6) * (h + 2)))
    sheet.save(os.path.join(prev, "all-24-pages.png"))


if __name__ == "__main__":
    sys.exit(main())
