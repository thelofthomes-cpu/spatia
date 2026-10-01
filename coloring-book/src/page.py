"""Page assembly + rendering helpers."""
import cairosvg
import ink

PW, PH = 850, 1100           # 8.5 x 11 in, 100 units per inch
FX, FY, FW, FH = 70, 70, 710, 880   # scene frame (inside 0.7 in margins)
FRAME = f"M{FX + 36} {FY} H{FX + FW - 36} A36 36 0 0 1 {FX + FW} {FY + 36} V{FY + FH - 36} " \
        f"A36 36 0 0 1 {FX + FW - 36} {FY + FH} H{FX + 36} A36 36 0 0 1 {FX} {FY + FH - 36} " \
        f"V{FY + 36} A36 36 0 0 1 {FX + 36} {FY} Z"


def svg_doc(body, w=PW, h=PH, bg="#ffffff"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w / 100}in" height="{h / 100}in" '
            f'viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')


def scene_page(draw, title, number=None):
    """Draw a scene clipped into the rounded frame, with an outlined title."""
    ink.reset()
    with ink.Clip(FRAME):
        draw()
    ink.P(FRAME, "none", ink.W + 1.5)
    ink.text(PW / 2, FY + FH + 78, title, size=62, w=3.4)
    if number is not None:
        ink.raw(f'<text x="{PW / 2}" y="{PH - 34}" font-family="Baloo 2" font-weight="600" '
                f'font-size="20" text-anchor="middle" fill="#777">{number}</text>')
    return svg_doc(ink.take())


def to_pdf(svg, path):
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=path)


def to_png(svg, path, width=850):
    cairosvg.svg2png(bytestring=svg.encode(), write_to=path, output_width=width)
