"""Tiny SVG "ink" engine for bold, clean coloring-book line art.

Every shape is drawn with a white fill and a black outline, back to front, so
foreground shapes neatly hide whatever is behind them (no stray lines to
color around). Stroke widths stay constant on the printed page no matter how
much a group is scaled, so every page has the same bold, even line weight.
"""
import math

# Line weights in page units (page = 850 x 1100 units = 8.5 x 11 in).
W = 7.5   # main outlines  (~5.4 pt)
D = 5.0   # inner details  (~3.6 pt)
F = 3.6   # fine details   (~2.6 pt)

INK = "#1b1b1b"
PAPER = "#ffffff"

_out = []
_scale = [1.0]
_ids = [0]


def reset():
    _out.clear()
    _scale[:] = [1.0]


def take():
    s = "\n".join(_out)
    reset()
    return s


def raw(s):
    _out.append(s)


def uid(prefix="c"):
    _ids[0] += 1
    return f"{prefix}{_ids[0]}"


def _w(w):
    return f"{w / _scale[-1]:.2f}"


class T:
    """Transform context: translate, rotate, uniform scale, optional mirror."""

    def __init__(self, x=0, y=0, s=1.0, r=0, flip=False):
        self.x, self.y, self.s, self.r, self.flip = x, y, s, r, flip

    def __enter__(self):
        sx = -self.s if self.flip else self.s
        _out.append(
            f'<g transform="translate({self.x:.1f},{self.y:.1f}) '
            f'rotate({self.r:.1f}) scale({sx:.4f},{self.s:.4f})">')
        _scale.append(_scale[-1] * self.s)
        return self

    def __exit__(self, *a):
        _out.append("</g>")
        _scale.pop()


class Thumb:
    """Inside a scaled-down transform: let line weights shrink with the art
    (used for page thumbnails)."""

    def __enter__(self):
        _scale.append(1.0)

    def __exit__(self, *a):
        _scale.pop()


class Clip:
    """Clip everything drawn inside to a path (in the current coordinates)."""

    def __init__(self, d):
        self.d = d

    def __enter__(self):
        cid = uid("clip")
        _out.append(f'<clipPath id="{cid}"><path d="{self.d}"/></clipPath>'
                    f'<g clip-path="url(#{cid})">')

    def __exit__(self, *a):
        _out.append("</g>")


_tint = []


class Tint:
    """Colour mode (used for the cover): white fills inside become `main`,
    fine-detail fills (blush, inner ears, bellies) become `detail`."""

    def __init__(self, main, detail=None):
        self.main, self.detail = main, detail or main

    def __enter__(self):
        _tint.append((self.main, self.detail))

    def __exit__(self, *a):
        _tint.pop()


def _style(fill, w):
    if _tint and fill == PAPER and w:
        fill = _tint[-1][1] if w <= F + 0.1 else _tint[-1][0]
    if w is None or w == 0:
        return f'fill="{fill}" stroke="none"'
    return (f'fill="{fill}" stroke="{INK}" stroke-width="{_w(w)}" '
            f'stroke-linecap="round" stroke-linejoin="round"')


# ---------------------------------------------------------------- primitives
def P(d, fill=PAPER, w=W):
    _out.append(f'<path d="{d}" {_style(fill, w)}/>')


def S(d, w=D):
    """Open stroke (no fill)."""
    P(d, "none", w)


def C(cx, cy, r, fill=PAPER, w=W):
    _out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" {_style(fill, w)}/>')


def E(cx, cy, rx, ry, fill=PAPER, w=W, rot=0):
    tr = f' transform="rotate({rot:.1f} {cx:.1f} {cy:.1f})"' if rot else ""
    _out.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}"{tr} {_style(fill, w)}/>')


def R(x, y, w_, h, rx=0, fill=PAPER, w=W, rot=0):
    tr = f' transform="rotate({rot:.1f} {x + w_ / 2:.1f} {y + h / 2:.1f})"' if rot else ""
    _out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w_:.1f}" height="{h:.1f}" rx="{rx:.1f}"{tr} {_style(fill, w)}/>')


def L(x1, y1, x2, y2, w=D):
    S(f"M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}", w)


def dot(cx, cy, r):
    C(cx, cy, r, INK, 0)


def poly(pts, closed=True, fill=PAPER, w=W):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if closed else "")
    P(d, fill if closed else "none", w)


def tube(d, width, w=W):
    """An outlined 'tube' along a path: tails, straps, handles, strings."""
    _out.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{_w(width + 2 * w)}" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')
    _out.append(f'<path d="{d}" fill="none" stroke="{PAPER}" stroke-width="{_w(width)}" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')


def text(x, y, s, size=60, w=3.2, anchor="middle", weight=800, fill=PAPER, family="Baloo 2"):
    _out.append(
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-weight="{weight}" '
        f'font-size="{size / 1:.1f}" text-anchor="{anchor}" fill="{fill}" stroke="{INK}" '
        f'stroke-width="{_w(w)}" stroke-linejoin="round">{s}</text>')


# ------------------------------------------------------------- path helpers
def smooth(pts, closed=True, t=1.0):
    """Catmull-Rom spline through points -> cubic Bezier path."""
    n = len(pts)
    p = pts
    d = f"M{p[0][0]:.1f} {p[0][1]:.1f}"
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = p[(i - 1) % n] if closed or i > 0 else p[i]
        p1 = p[i]
        p2 = p[(i + 1) % n]
        p3 = p[(i + 2) % n] if closed or i + 2 < n else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * t, p1[1] + (p2[1] - p0[1]) / 6 * t)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * t, p2[1] - (p3[1] - p1[1]) / 6 * t)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d + (" Z" if closed else "")


def scallop(pts, bulge=0.62, closed=True):
    """Polygon whose edges are outward arcs (clouds, bushes, wool, frosting).
    Give points clockwise on screen (y down)."""
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    n = len(pts)
    for i in range(n if closed else n - 1):
        a, b = pts[i], pts[(i + 1) % n]
        r = math.dist(a, b) * bulge
        d += f" A{r:.1f} {r:.1f} 0 0 1 {b[0]:.1f} {b[1]:.1f}"
    return d + (" Z" if closed else "")


def ring(cx, cy, rx, ry, n, a0=0, a1=360):
    out = []
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * i / (n if a1 - a0 >= 360 else n - 1))
        out.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    return out


def star_pts(cx, cy, r1, r2, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def wavy_line(x1, x2, y, amp=6, n=8):
    d = f"M{x1:.1f} {y:.1f}"
    step = (x2 - x1) / n
    for i in range(n):
        xa = x1 + step * (i + 0.5)
        xb = x1 + step * (i + 1)
        d += f" Q{xa:.1f} {y - amp if i % 2 == 0 else y + amp:.1f} {xb:.1f} {y:.1f}"
    return d
