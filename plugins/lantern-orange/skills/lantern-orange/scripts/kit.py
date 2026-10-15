"""kit: drawing + rendering helpers (SVG in, PNG/GIF/MP4 out).

Every colour comes from ../themes/<colour>.json through the theme object `T`, and every font and size from
../system.json through `F` and `ts()`; nothing here hard-codes a hue or a typeface.
    set_theme("dark" | "light", color="blue", type_set="classic")   choose before building a scene
    set_canvas(1920, 1080, loop=25)                                  choose the frame and loop length
"""

import base64
import html
import importlib.util
import json
import math
import os
import random
import shutil
import subprocess
import textwrap
from pathlib import Path

TAU = 2 * math.pi
ROOT = Path(__file__).resolve().parent.parent
SYS = json.loads((ROOT / "system.json").read_text(encoding="utf-8"))


def colors():
    """Installed colour themes (one JSON file each in themes/)."""
    return sorted(p.stem for p in (ROOT / "themes").glob("*.json"))


def load_theme(color):
    return json.loads((ROOT / "themes" / f"{color}.json").read_text(encoding="utf-8"))


class _Theme:
    """T.G800, T.W300, T.LIT ... resolve to the current colour and variant's tokens."""

    def use(self, variant=None, color=None):
        have = colors()
        color = (
            color or getattr(self, "color", None) or (SYS["default_color"] if SYS["default_color"] in have else have[0])
        )
        if color not in have:
            raise ValueError(f"no theme '{color}'; installed: {have}")
        variant = variant or getattr(self, "variant", "dark")
        tok = load_theme(color)
        v = tok["variants"][variant]
        self.__dict__.clear()
        self.__dict__.update(v["colors"])
        self.__dict__.update(v["fx"])
        self.variant, self.light, self.color, self.name, self.tok = variant, variant == "light", color, tok["name"], tok


class _Type:
    """F.DISPLAY, F.SANS, F.MONO are CSS font stacks for the current type set."""

    def use(self, name=None):
        name = name or SYS["default_type_set"]
        d = SYS["type_sets"][name]
        self.set = name
        self.SUB_STYLE = d["subtitle_style"]
        self.DISPLAY, self.SANS, self.MONO = (SYS["fonts"][d[r]]["stack"] for r in ("display", "sans", "mono"))


def ts(style):
    """Font size of a named style in the type scale (system.json), at a 1920 frame."""
    return SYS["type_scale"][style]["size"]


class _Canvas:
    W, H, LOOP = 1920, 1080, 25.0


T, C, F = _Theme(), _Canvas(), _Type()
T.use("dark")
F.use(T.tok.get("default_type"))
PRESETS = {
    "16:9": (1920, 1080),
    "4:3": (1440, 1080),
    "3:2": (1620, 1080),
    "1:1": (1080, 1080),
    "9:16": (1080, 1920),
    "a4": (1754, 1240),
}


def set_theme(variant=None, color=None, type_set=None):
    """Any argument left out keeps its current value. A new colour brings its own default type set unless one is given."""
    T.use(variant, color)
    if type_set or color:
        F.use(type_set or T.tok.get("default_type"))


def set_canvas(w=1920, h=1080, loop=None):
    """w may also be a preset name: '16:9', '4:3', '3:2', '1:1', '9:16', 'a4'."""
    if isinstance(w, str):
        w, h = PRESETS[w]
    C.W, C.H = w, h
    if loop:
        C.LOOP = float(loop)


# ---------- primitives ----------
def f2(v):
    return f"{v:.2f}"


def esc(s):
    return html.escape(str(s), quote=True)


def wrap(text, chars=40):
    return textwrap.wrap(text, chars)


def P(pts, close=True):
    s = "M" + " L".join(f"{f2(a)},{f2(b)}" for a, b in pts)
    return s + (" Z" if close else "")


def lerp(a, b, t):
    return a + (b - a) * t


def frac(x):
    return x - math.floor(x)


def hexmix(c1, c2, t):
    a = [int(c1[i : i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i : i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(lerp(a[k], b[k], t)):02x}" for k in range(3))


def to_oklch(h):
    """#rrggbb -> (lightness 0..1, chroma, hue in degrees)."""
    r, g, b = [
        (v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4)
        for v in (int(h[i : i + 2], 16) / 255 for i in (1, 3, 5))
    ]
    l, m, s = (
        (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3),
        (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3),
        (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3),
    )
    A, B = (
        1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
        0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s,
    )
    return (
        0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
        math.hypot(A, B),
        math.degrees(math.atan2(B, A)) % 360,
    )


def from_oklch(L, Cc, H):
    """(lightness, chroma, hue) -> #rrggbb, lowering chroma until the colour fits sRGB."""

    def lin(c):
        a, b = c * math.cos(math.radians(H)), c * math.sin(math.radians(H))
        l, m, s = (
            (L + 0.3963377774 * a + 0.2158037573 * b) ** 3,
            (L - 0.1055613458 * a - 0.0638541728 * b) ** 3,
            (L - 0.0894841775 * a - 1.2914855480 * b) ** 3,
        )
        return (
            4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
        )

    L = max(0.0, min(1.0, L))
    while Cc > 0 and any(v < -1e-4 or v > 1 + 1e-4 for v in lin(Cc)):
        Cc -= 0.002
    enc = lambda v: round(255 * (12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055))
    return "#" + "".join(f"{enc(max(0.0, min(1.0, v))):02x}" for v in lin(max(Cc, 0)))


def rrect(x, y, w, h, r, fill, extra=""):
    return f'<rect x="{f2(x)}" y="{f2(y)}" width="{f2(w)}" height="{f2(h)}" rx="{f2(r)}" fill="{fill}" {extra}/>'


def circ(cx, cy, r, fill, extra=""):
    return f'<circle cx="{f2(cx)}" cy="{f2(cy)}" r="{f2(r)}" fill="{fill}" {extra}/>'


def ell(cx, cy, rx, ry, fill, extra=""):
    return f'<ellipse cx="{f2(cx)}" cy="{f2(cy)}" rx="{f2(rx)}" ry="{f2(ry)}" fill="{fill}" {extra}/>'


def line(a, b, col, w, extra=""):
    return f'<path d="M{f2(a[0])},{f2(a[1])} L{f2(b[0])},{f2(b[1])}" stroke="{col}" stroke-width="{f2(w)}" {extra}/>'


def path(d, fill="none", extra=""):
    return f'<path d="{d}" fill="{fill}" {extra}/>'


def glow(cx, cy, rx, ry=None, grad="warmglow", op=1.0):
    """Soft pool of light. Blend mode follows the theme (screen on dark, multiply on light)."""
    return ell(cx, cy, rx, ry or rx, f"url(#{grad})", f'opacity="{op}" style="mix-blend-mode:{T.GLOW_BLEND}"')


def pipe(pts, w=10, col=None, hi=None, dark=None, elbows=True):
    col, hi, dark = col or T.V400, hi or T.L200, dark or T.IN800
    d = P(pts, False)
    s = [
        f'<path d="{d}" stroke="{dark}" stroke-width="{w + 3}" fill="none" stroke-linejoin="round"/>',
        f'<path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linejoin="round"/>',
        f'<path d="{d}" stroke="{hi}" stroke-width="{w * 0.24:.2f}" fill="none" opacity="0.5" transform="translate({-w * 0.2:.2f},{-w * 0.2:.2f})"/>',
    ]
    if elbows:
        s += [circ(p[0], p[1], w * 0.66, col, f'stroke="{dark}" stroke-width="1.8"') for p in pts[1:-1]]
    return "".join(s)


def cable(pts, w=4, col=None):
    d = P(pts, False)
    return (
        f'<path d="{d}" stroke="{T.CABLE_DARK}" stroke-width="{w + 2}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
        f'<path d="{d}" stroke="{col or T.CABLE}" stroke-width="{w}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
    )


def poly_len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def point_at(pts, s):
    for a, b in zip(pts, pts[1:]):
        l = math.hypot(b[0] - a[0], b[1] - a[1])
        if s <= l and l > 0:
            return (lerp(a[0], b[0], s / l), lerp(a[1], b[1], s / l))
        s -= l
    return pts[-1]


def flow(pts, kind="energy", p=0.0, cycles=0, gap=16, r=2.2, op=0.95, col=None):
    """Glowing marks along a polyline; they advance `cycles` gaps per loop (integer = seamless).
    kind sets BOTH colour and shape so meaning never rests on hue alone:
    'energy' = warm round dots, 'info' = cool squares, 'water' = support-colour rings."""
    col = col or {"energy": T.W300, "info": T.L100, "water": T.WATER}[kind]
    L = poly_len(pts)
    s = frac(cycles * p) * gap
    out = []
    while s < L:
        x, y = point_at(pts, s)
        o = f'opacity="{op * max(0.0, min(1.0, min(s, L - s) / 12.0)):.2f}"'
        if kind == "info":
            out.append(rrect(x - r * 1.1, y - r * 1.1, r * 2.2, r * 2.2, 1, col, o))
        elif kind == "water":
            out.append(circ(x, y, r * 1.15, "none", f'stroke="{col}" stroke-width="{r * 0.6:.2f}" {o}'))
        else:
            out.append(circ(x, y, r, col, o))
        s += gap
    return '<g filter="url(#dotglow)">' + "".join(out) + "</g>"


def curve(a, b, sag, n=24):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + sag
    return [
        (
            (1 - t) ** 2 * a[0] + 2 * (1 - t) * t * mx + t * t * b[0],
            (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * my + t * t * b[1],
        )
        for t in [i / n for i in range(n + 1)]
    ]


def sight(a, b, bulge=0.2, n=None):
    """Line of sight: dotted arc whose dots grow and brighten toward b."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    dist = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / dist, dx / dist
    if ny > 0:
        nx, ny = -nx, -ny
    cx, cy = (a[0] + b[0]) / 2 + nx * dist * bulge, (a[1] + b[1]) / 2 + ny * dist * bulge
    n = max(2, n or int(dist / 26))
    out = []
    for i in range(n):
        t = 0.05 + 0.95 * i / (n - 1)
        x = (1 - t) ** 2 * a[0] + 2 * (1 - t) * t * cx + t * t * b[0]
        y = (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * cy + t * t * b[1]
        out.append(circ(x, y, lerp(1.4, 4.4, t), T.SIGHT, f'opacity="{lerp(0.3, 1, t):.2f}"'))
    return '<g filter="url(#dotglow)">' + "".join(out) + "</g>"


PITCH = 8.0


def gear(cx, cy, teeth, rot=0.0, fill=None, hub=None, nh=None):
    """Gear with pitch radius teeth*PITCH/TAU. nh = number of lightening holes (choose so the loop rotation is a symmetry)."""
    fill, hub = fill or T.V300, hub or T.IN500
    rp = teeth * PITCH / TAU
    ro, rr = rp + 3.4, rp - 3.4
    step = TAU / teeth
    pts = []
    for i in range(teeth):
        a = rot + step * i
        for da, r in ((0, rr), (step * 0.2, ro), (step * 0.45, ro), (step * 0.65, rr)):
            pts.append((cx + r * math.cos(a + da), cy + r * math.sin(a + da)))
    s = [
        f'<path d="{P(pts)}" fill="{fill}" stroke="{T.IN800}" stroke-width="1.5" stroke-linejoin="round"/>',
        circ(cx, cy, rp * 0.76, "none", f'stroke="{hexmix(fill, T.INK, 0.3)}" stroke-width="{rp * 0.07:.2f}"'),
    ]
    nh = nh or (4 if rp < 24 else 6)
    s += [
        circ(
            cx + rp * 0.5 * math.cos(rot + TAU * i / nh),
            cy + rp * 0.5 * math.sin(rot + TAU * i / nh),
            rp * 0.15,
            hexmix(fill, T.INK, 0.45),
        )
        for i in range(nh)
    ]
    return "".join(s) + circ(cx, cy, rp * 0.26, hub) + circ(cx, cy, rp * 0.1, T.L300)


def gear_radius(teeth):
    return teeth * PITCH / TAU


def place_next(c, t_from, t_to, angle_deg):
    d = gear_radius(t_from) + gear_radius(t_to)
    a = math.radians(angle_deg)
    return (c[0] + d * math.cos(a), c[1] + d * math.sin(a))


def gear_chain(chain, theta0, omega0):
    """chain = [(teeth, centre), ...] meshing in order -> [(teeth, centre, theta0, omega)] with teeth interlocking."""
    out = [(chain[0][0], chain[0][1], theta0, omega0)]
    for Tn, c in chain[1:]:
        TA, cA, thA, omA = out[-1]
        sA, sB = TAU / TA, TAU / Tn
        psi = math.atan2(c[1] - cA[1], c[0] - cA[0])
        xA = frac((psi - thA) / sA - 0.325)
        out.append((Tn, c, psi + math.pi - sB * (frac(-xA) + 0.825), -omA * TA / Tn))
    return out


def figure(j, alien=False, facing=1, props=""):
    """Silhouette in ink with a warm rim copy. j: head, neck, hip, arms=[[pts]], legs=[[pts]] (feet last)."""

    def draw(col, dx, dy, op):
        s = []
        for leg in j.get("legs", []):
            s.append(
                f'<path d="{P([(x + dx, y + dy) for x, y in leg], False)}" stroke="{col}" stroke-width="{5 if alien else 5.9}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            )
        (nx, ny), (hx, hy) = j["neck"], j["hip"]
        s.append(
            f'<path d="M{f2(nx + dx)},{f2(ny + dy)} L{f2(hx + dx)},{f2(hy + dy)}" stroke="{col}" stroke-width="{11 if alien else 12.5}" stroke-linecap="round"/>'
        )
        for arm in j.get("arms", []):
            s.append(
                f'<path d="{P([(x + dx, y + dy) for x, y in arm], False)}" stroke="{col}" stroke-width="{4.2 if alien else 5}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            )
        ex, ey = j["head"]
        if alien:
            s.append(ell(ex + dx, ey + dy, 8.6, 7.8, col))
            for sx in (-1, 1):
                s.append(
                    f'<path d="M{f2(ex + 3 * sx + dx)},{f2(ey - 6 + dy)} L{f2(ex + 7 * sx + dx)},{f2(ey - 15 + dy)}" stroke="{col}" stroke-width="1.6" stroke-linecap="round"/>'
                )
        else:
            s.append(circ(ex + dx, ey + dy, 6.8, col))
        return f'<g opacity="{op}">' + "".join(s) + "</g>"

    out = draw(T.W400, -1.2, -1.0, T.RIM_OP) + draw(T.INK, 0, 0, 1)
    if alien:
        ex, ey = j["head"]
        out += "".join(circ(ex + 7 * sx, ey - 15, 2.1, T.W300, 'filter="url(#dotglow)"') for sx in (-1, 1))
        out += ell(ex + 4 * facing, ey - 0.5, 2.6, 1.5, T.MIST if T.light else T.L100, 'opacity="0.9"')
    return out + props


def standing(x, floor, facing=1, reach=None, alien=False, hat=None, carry=False):
    """Standing pose, ~46px tall, feet on `floor`. reach=(x,y) puts the front hand there.
    hat='top' | 'bun' varies the silhouette; carry=True adds a lit box in the front hand."""
    hy = floor - 17
    ny = floor - 34
    head = (x + facing, floor - 42)
    hand = reach or (x + 14 * facing, ny + 18)
    front = [(x + facing, ny + 2), (x + 10 * facing, ny + 9), hand]
    back = [(x - facing, ny + 3), (x - 4 * facing, ny + 12), (x - 3 * facing, ny + 20)]
    props = ""
    if hat == "top":
        props += rrect(head[0] - 5, head[1] - 17, 10, 11, 1, T.INK) + rrect(
            head[0] - 8, head[1] - 7.5, 16, 2.4, 1, T.INK
        )
    if hat == "bun":
        props += circ(head[0] - 5 * facing, head[1] - 6, 3.4, T.INK)
    if carry:
        props += rrect(hand[0] - 5, hand[1] - 9, 10, 9, 1.5, T.W200, f'stroke="{T.IN900}" stroke-width="1"')
    return figure(
        dict(
            head=head,
            neck=(x, ny),
            hip=(x, hy),
            arms=[back, front],
            legs=[[(x, hy), (x - 3, floor - 8), (x - 5, floor)], [(x, hy), (x + 4, floor - 8), (x + 6, floor)]],
        ),
        alien=alien,
        facing=facing,
        props=props,
    )


def seated(x, seat, facing=1, alien=False):
    """Seated pose (at a desk or console); `seat` is the y of the chair seat."""
    ny = seat - 19
    head = (x + facing, seat - 27)
    return figure(
        dict(
            head=head,
            neck=(x, ny),
            hip=(x, seat - 2),
            arms=[[(x + facing, ny + 2), (x + 8 * facing, ny + 9), (x + 15 * facing, ny + 8)]],
            legs=[[(x, seat - 2), (x + 10 * facing, seat - 1), (x + 11 * facing, seat + 14)]],
        ),
        alien=alien,
        facing=facing,
    )


# ---------- standard <defs> ----------
def _stops(cols, offs, ops=None):
    ops = ops or [1] * len(cols)
    return "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for c, o, a in zip(cols, offs, ops))


def std_defs(cx=None, cy=None, lit=(0, -40), lit_r=460):
    """Gradients and filters every scene uses. `lit` is the light source in the local (subject) frame."""
    cx = C.W / 2 if cx is None else cx
    cy = C.H * 0.48 if cy is None else cy
    R = 0.625 * max(C.W, C.H * 16 / 9)
    g_ops = [0.9, 0.5, 0.2, 0] if T.light else [0.85, 0.4, 0.1, 0]
    return f"""
<radialGradient id="bg" cx="{cx}" cy="{cy}" r="{R:.0f}" gradientUnits="userSpaceOnUse">{_stops([T.G600, T.G700, T.G800, T.G900, T.G950], [0, 0.25, 0.5, 0.78, 1])}</radialGradient>
<radialGradient id="vign" cx="{cx}" cy="{cy}" r="{R * 0.98:.0f}" gradientUnits="userSpaceOnUse">{_stops([T.VIGN, T.VIGN], [0.45, 1], [0, T.VIGN_MAX])}</radialGradient>
<radialGradient id="litmask" cx="{lit[0]}" cy="{lit[1]}" r="{lit_r}" gradientUnits="userSpaceOnUse">{_stops(T.LIT, [0, 0.5, 0.82, 1])}</radialGradient>
<radialGradient id="warmglow" cx="0.5" cy="0.5" r="0.5">{_stops(T.GLOW, [0, 0.3, 0.65, 1], g_ops)}</radialGradient>
<radialGradient id="cool" cx="0.5" cy="0.5" r="0.5">{_stops(T.COOL, [0, 0.5, 1], [0.5, 0.15, 0])}</radialGradient>
<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">{_stops([T.HALO, T.HALO, T.HALO], [0, 0.55, 1], [T.HALO_OP, T.HALO_OP * 0.45, 0])}</radialGradient>
<linearGradient id="metalv" x1="0" y1="0" x2="1" y2="0">{_stops(T.METALV, [0, 0.3, 0.55, 1])}</linearGradient>
<linearGradient id="metalh" x1="0" y1="0" x2="0" y2="1">{_stops(T.METALH, [0, 0.35, 1])}</linearGradient>
<linearGradient id="warmwin" x1="0" y1="0" x2="0" y2="1">{_stops(T.WARMWIN, [0, 0.55, 1])}</linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0">{_stops([T.W100, T.W200, T.W200], [0, 0.45, 1], [0.95, 0.5, 0.0] if not T.light else [0.95, 0.6, 0.0])}</linearGradient>
<linearGradient id="beamr" x1="1" y1="0" x2="0" y2="0">{_stops([T.W100, T.W200, T.W200], [0, 0.45, 1], [0.95, 0.5, 0.0] if not T.light else [0.95, 0.6, 0.0])}</linearGradient>
<linearGradient id="beamv" x1="0" y1="0" x2="0" y2="1">{_stops([T.W100, T.W200, T.W200], [0, 0.45, 1], [0.8, 0.35, 0.0])}</linearGradient>
<linearGradient id="skin" x1="1" y1="0" x2="0" y2="0.3">{_stops([hexmix(T.W200, T.W400, 0.5), hexmix(T.W400, T.L300, 0.55), T.V300], [0, 0.45, 1])}</linearGradient>
<linearGradient id="cloth" x1="0" y1="0" x2="1" y2="1">{_stops([T.IN700, T.IN800 if not T.light else T.IN600, T.IN900], [0, 0.5, 1])}</linearGradient>
<linearGradient id="chrome" x1="0" y1="0" x2="1" y2="0.25">{_stops([T.V400, T.V300, T.L300, hexmix(T.L200 if not T.light else T.L300, T.W200, 0.45)], [0, 0.45, 0.82, 1])}</linearGradient>
<filter id="blur3" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="blur8" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="blur18" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
<filter id="dotglow" x="-200%" y="-200%" width="500%" height="500%">
  <feGaussianBlur stdDeviation="1.7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
"""


def background(cx=None, cy=None, seed=3, p=0.0, avoid=(), stars=True):
    """Ground radial + stars (dust on light) + halo. avoid = [(x0,y0,x1,y1)] boxes kept free of twinkles (text areas)."""
    W, H = C.W, C.H
    cx = W / 2 if cx is None else cx
    cy = H * 0.48 if cy is None else cy
    rnd = random.Random(seed)
    out = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']
    if stars:
        for _ in range(int(460 * W * H / (1920 * 1080))):
            x, y = rnd.uniform(0, W), rnd.uniform(0, H)
            d = math.hypot((x - cx) / 1.4, y - cy) / 900
            if rnd.random() < d * 0.55:
                continue
            out.append(
                circ(
                    x,
                    y,
                    rnd.choice([0.6, 0.7, 0.8, 1.0, 1.3]),
                    T.STAR,
                    f'opacity="{rnd.uniform(0.15, 0.7) * (1.1 - min(d, 1)) * T.STAR_OP:.2f}"',
                )
            )
        for _ in range(26):
            x, y = rnd.uniform(40, W - 40), rnd.uniform(30, H - 30)
            n = rnd.choice([1, 2, 3, 5])
            ph = rnd.random()
            r = rnd.choice([1.4, 1.7, 2.0])
            if any(x0 < x < x1 and y0 < y < y1 for x0, y0, x1, y1 in avoid):
                continue
            o = (0.25 + 0.6 * (0.5 + 0.5 * math.sin(TAU * (n * p + ph)))) * T.STAR_OP
            out.append(circ(x, y, r, T.TWINKLE, f'opacity="{o:.2f}" filter="url(#dotglow)"'))
            out.append(
                f'<path d="M{f2(x - 5 * r)},{f2(y)} L{f2(x + 5 * r)},{f2(y)} M{f2(x)},{f2(y - 5 * r)} L{f2(x)},{f2(y + 5 * r)}" stroke="{T.TWINKLE}" stroke-width="0.7" opacity="{o * 0.55:.2f}"/>'
            )
    out.append(ell(cx, cy, 820, 600, "url(#halo)"))
    return "".join(out)


def finish():
    """Vignette. Grain is NOT drawn in SVG: render()/make_gif()/make_mp4() add the same static grain to stills and frames."""
    return f'<rect width="{C.W}" height="{C.H}" fill="url(#vign)"/>'


def svg_doc(defs, body, alt=""):
    """alt = one-sentence description; it becomes the SVG <title> and should be reused as the image's alt text."""
    t = f"<title>{esc(alt)}</title>" if alt else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" role="img" viewBox="0 0 {C.W} {C.H}" width="{C.W}" height="{C.H}">{t}<defs>{defs}</defs>{body}</svg>'


# ---------- text (annotated figures & slides) ----------
_ADV = {
    v["stack"]: v["adv"] for v in SYS["fonts"].values()
}  # average advance per em: good to about 5%; measure in the browser if a layout needs exact widths


def text_width(s, size, family=None):
    return len(s) * size * _ADV[family or F.SANS]


def text(x, y, s, size=None, fill=None, family=None, extra=""):
    return f'<text x="{f2(x)}" y="{f2(y)}" font-family="{family or F.SANS}" font-size="{size or ts("body")}" fill="{fill or T.T2}" {extra}>{esc(s)}</text>'


def title_block(title_lines, subtitle=None, answer=None, x=72, y=100):
    """Question in display serif (<=2 lines), an optional subtitle in italic, one answer line in the accent."""
    s = "".join(text(x, y + i * 50, t, ts("title-lg"), T.T1, F.DISPLAY) for i, t in enumerate(title_lines))
    yy = y + (len(title_lines) - 1) * 50
    if subtitle:
        yy += 40
        s += text(x + 1, yy, subtitle, ts("subtitle"), T.T2, F.DISPLAY, f'font-style="{F.SUB_STYLE}"')
    if answer:
        yy += 38
        s += text(x + 2, yy, answer, ts("answer-sm"), T.W300, F.SANS, 'font-weight="500"')
    return s


def callout(x, y, title, lines, anchor, side="left", tag=None):
    """Label + leader. side='left' = label in the left column (leader leaves from its right edge, measured from the text).
    tag = (prefix, body) or None; e.g. ("Step", "final check")."""
    s = [text(x, y, title, ts("label-title"), T.T1, F.DISPLAY)]
    s += [text(x, y + 32 + i * 24, ln, ts("body"), T.T2) for i, ln in enumerate(lines)]
    wid = max([text_width(title, ts("label-title"), F.DISPLAY)] + [text_width(ln, ts("body")) for ln in lines])
    if tag:
        pre, body = tag
        tag_size = ts("tag")
        wid = max(wid, text_width(f"{pre} · {body}", ts("tag"), F.MONO))
        s.append(
            f'<text x="{f2(x)}" y="{f2(y + 38 + len(lines) * 24)}" font-family="{F.MONO}" font-size="{tag_size}" fill="{T.W300}"><tspan fill="{T.ROSE3}">{esc(pre)} · </tspan>{esc(body)}</text>'
        )
    sx, sy = (x + wid + 24, y - 10) if side == "left" else (x - 20, y - 10)
    ex = sx + 22 if side == "left" else sx - 22
    ax, ay = anchor
    s.append(
        f'<path d="M{f2(sx)},{f2(sy)} L{f2(ex)},{f2(sy)} L{f2(ax)},{f2(ay)}" stroke="{T.W300}" stroke-opacity="0.7" stroke-width="1.3" fill="none"/>'
    )
    s.append(circ(sx, sy, 2.6, T.W300))
    s.append(
        circ(ax, ay, 9, "none", f'stroke="{T.VIGN if not T.light else T.G600}" stroke-opacity="0.6" stroke-width="3.4"')
    )
    s.append(circ(ax, ay, 9, "none", f'stroke="{T.W300}" stroke-opacity="0.9" stroke-width="1.4"'))
    s.append(circ(ax, ay, 2.8, T.W100 if not T.light else T.W300))
    return "".join(s)


def break_slide(word="Break", answer="Back in 15 minutes", aside=(), x=1300, y=440):
    s = text(x, y, word, ts("title-xl"), T.T1, F.DISPLAY) + text(
        x + 4, y + 58, answer, ts("answer"), T.W300, F.SANS, 'font-weight="500"'
    )
    return s + "".join(text(x + 4, y + 110 + i * 30, ln, ts("lead"), T.T2) for i, ln in enumerate(aside))


def credit(s, margin=72):
    return text(C.W - margin, C.H - 36, s, ts("credit"), T.T3, F.SANS, 'text-anchor="end"')


# ---------- rendering ----------
_FONT_FILES = {fam: v["files"] for fam, v in SYS["fonts"].items()}
_font_css_cache = {}


def font_css(families=None):
    """@font-face rules with the bundled woff2 files embedded (works in a blank page and in any HTML editor)."""
    out = []
    for fam in families or _FONT_FILES:
        if fam not in _font_css_cache:
            _font_css_cache[fam] = "".join(
                f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};src:url(data:font/woff2;base64,"
                f"{base64.b64encode((ROOT / 'assets' / 'fonts' / (fn + '.woff2')).read_bytes()).decode()}) format('woff2');}}"
                for w, st, fn in _FONT_FILES[fam]
            )
        out.append(_font_css_cache[fam])
    return "".join(out)


def _offline(pg):
    """Block every request that is not inline data, so rendering never touches the network."""
    pg.route(
        "**/*",
        lambda route: route.abort() if not route.request.url.startswith(("data:", "about:")) else route.continue_(),
    )
    return pg


def _shoot(pg, svg, path, transparent=False):
    used = [f for f in _FONT_FILES if f in svg] if "<text" in svg else []
    bg = "transparent" if transparent else T.G950
    pg.set_content(
        f"<!doctype html><html><head><style>{font_css(used)}html,body{{margin:0;background:{bg}}}svg{{display:block}}</style></head><body>{svg}</body></html>"
    )
    if used:
        bad = pg.evaluate(
            'async fams => { const r = await Promise.all(fams.map(f => document.fonts.load(`400 20px "${f}"`))); await document.fonts.ready; return fams.filter((f, i) => !r[i].length) }',
            used,
        )
        if bad:
            raise RuntimeError(f"fonts failed to load: {bad} (check assets/fonts)")
    pg.screenshot(path=path, clip={"x": 0, "y": 0, "width": C.W, "height": C.H}, omit_background=transparent)


def render(svg, out, scale=2, transparent=False, grain=True):
    """SVG string -> PNG via Playwright's Chromium, fonts verified, then the theme's static grain."""
    from playwright.sync_api import sync_playwright
    from PIL import Image

    with sync_playwright() as p:
        b = p.chromium.launch()
        try:
            _shoot(
                _offline(b.new_page(viewport={"width": C.W, "height": C.H}, device_scale_factor=scale)),
                svg,
                out,
                transparent,
            )
        finally:
            b.close()
    if grain:
        im = Image.open(out)
        apply_grain(im, grain_field(im.width, im.height, grain_amp(C.W), scale=scale)).save(out)
    return out


def cutout(png, out=None, pad=24):
    """Crop a transparent render to its content + padding; fails if the art touches the canvas edge."""
    from PIL import Image

    im = Image.open(png)
    box = im.getbbox()
    if box is None:
        raise ValueError("cutout is empty")
    if box[0] == 0 or box[1] == 0 or box[2] == im.width or box[3] == im.height:
        raise ValueError(f"art is clipped at the canvas edge (bbox {box}); move or shrink the subject")
    im.crop(
        (max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))
    ).save(out or png)
    return out or png


# ---------- animation ----------
def _worker(k, nw, build, fps, out_dir, state):
    from playwright.sync_api import sync_playwright

    variant, color, type_set, C.W, C.H, C.LOOP = state
    T.use(variant, color)
    F.use(type_set)
    n = int(round(C.LOOP * fps))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = _offline(b.new_page(viewport={"width": C.W, "height": C.H}))
        for i in range(k, n, nw):
            fp = f"{out_dir}/raw_{i:04d}.png"
            if os.path.exists(fp):
                continue
            _shoot(pg, build(i / fps), fp + ".tmp.png")
            os.replace(fp + ".tmp.png", fp)
        b.close()


def render_frames(build, fps, out_dir, workers=2, fresh=False):
    """build(t) -> SVG string (grain is added later, static). Parallel; raises if any frame is missing.
    Resumable: frames already in out_dir are kept, so pass fresh=True after changing the scene.
    `build` must be a module-level function and the script must run under `if __name__ == "__main__":`."""
    from multiprocessing import Process

    if fresh and os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    n = int(round(C.LOOP * fps))
    state = (T.variant, T.color, F.set, C.W, C.H, C.LOOP)
    ps = [Process(target=_worker, args=(k, workers, build, fps, out_dir, state)) for k in range(workers)]
    for q in ps:
        q.start()
    for q in ps:
        q.join()
    have = len([f for f in os.listdir(out_dir) if f.startswith("raw_") and f.endswith(".png") and ".tmp" not in f])
    if have != n or any(q.exitcode for q in ps):
        raise RuntimeError(
            f"{have}/{n} frames rendered (worker exit codes {[q.exitcode for q in ps]}); re-run render_frames to resume"
        )
    return n


def grain_amp(width):
    return 0.09 if width <= 1280 else 0.12


def grain_field(w, h, amp, seed=7, scale=1):
    """Static noise field. scale>1 generates at w/scale and enlarges, so 2x stills carry the same grain size as 1x frames."""
    import numpy as np
    from PIL import Image, ImageFilter

    bw, bh = max(1, round(w / scale)), max(1, round(h / scale))
    n = np.random.default_rng(seed).normal(0.5, 0.2, (bh, bw)).astype("float32")
    im = Image.fromarray((n.clip(0, 1) * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.6))
    if (bw, bh) != (w, h):
        im = im.resize((w, h), Image.BICUBIC)
    n = np.asarray(im).astype("float32") / 255
    return ((n - n.mean()) / (n.std() + 1e-6) * amp + 0.5).clip(0, 1)[..., None]


def apply_grain(img, n):
    """Overlay + screen grain at the theme's strengths; alpha (cutouts) is preserved."""
    import numpy as np
    from PIL import Image

    alpha = img.getchannel("A") if img.mode == "RGBA" else None
    b = np.asarray(img.convert("RGB")).astype("float32") / 255
    ov = np.where(b < 0.5, 2 * b * n, 1 - 2 * (1 - b) * (1 - n))
    o = b + (ov - b) * T.GRAIN_OVERLAY
    o = o + ((1 - (1 - o) * (1 - n)) - o) * T.GRAIN_SCREEN
    res = Image.fromarray((o * 255 + 0.5).clip(0, 255).astype("uint8"))
    if alpha is not None:
        res.putalpha(alpha)
    return res


def _raw_frames(raw_dir):
    return sorted(f for f in os.listdir(raw_dir) if f.startswith("raw_") and f.endswith(".png") and ".tmp" not in f)


def make_gif(raw_dir, out, size=None, fps=10, text_png=None, limit_mb=15.0):
    """Exact-length GIF. GIF delays are whole centiseconds, so fps must divide 100 (10, 20, 25, 50).
    If the file exceeds limit_mb the palette is reduced and it is encoded again."""
    from PIL import Image

    if 100 % fps:
        raise ValueError("GIF fps must divide 100 (use 10, 20 or 25) or the loop length drifts")
    size = size or (1280, round(1280 * C.H / C.W / 2) * 2)
    frames = _raw_frames(raw_dir)
    want = int(round(C.LOOP * fps))
    if len(frames) != want:
        raise RuntimeError(f"{len(frames)} frames in {raw_dir}, expected {want}")
    tmp = raw_dir.rstrip("/\\") + f"_gif{size[0]}"
    os.makedirs(tmp, exist_ok=True)
    n = grain_field(*size, amp=grain_amp(size[0]))
    txt = Image.open(text_png).convert("RGBA") if text_png else None
    for k, f in enumerate(frames):
        im = Image.open(f"{raw_dir}/{f}").convert("RGBA")
        if txt:
            im.alpha_composite(txt)
        apply_grain(im.convert("RGB").resize(size, Image.LANCZOS), n).save(f"{tmp}/{k:04d}.png", compress_level=1)
    for colors in (208, 160, 128, 96):
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-framerate",
                str(fps),
                "-i",
                f"{tmp}/%04d.png",
                "-vf",
                f"palettegen=max_colors={colors}:stats_mode=full",
                f"{tmp}/pal.png",
            ],
            check=True,
        )
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-framerate",
                str(fps),
                "-i",
                f"{tmp}/%04d.png",
                "-i",
                f"{tmp}/pal.png",
                "-lavfi",
                "paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
                "-loop",
                "0",
                out,
            ],
            check=True,
        )
        mb = os.path.getsize(out) / 1e6
        if mb <= limit_mb:
            break
    return mb


def make_mp4(raw_dir, out, fps=24, text_png=None):
    """1080p H.264 MP4 of the frames with the same static grain as the GIF."""
    from PIL import Image

    n = grain_field(C.W, C.H, amp=grain_amp(C.W))
    txt = Image.open(text_png).convert("RGBA") if text_png else None
    p = subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{C.W}x{C.H}",
            "-r",
            str(fps),
            "-i",
            "-",
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "17",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            out,
        ],
        stdin=subprocess.PIPE,
    )
    for f in _raw_frames(raw_dir):
        im = Image.open(f"{raw_dir}/{f}").convert("RGBA")
        if txt:
            im.alpha_composite(txt)
        p.stdin.write(apply_grain(im.convert("RGB"), n).tobytes())
    p.stdin.close()
    if p.wait():
        raise RuntimeError("ffmpeg failed while encoding the MP4")
    return os.path.getsize(out) / 1e6


def check_loop(raw_dir):
    """Seam test: the last->first frame difference should look like any consecutive difference. Returns (seam, typical)."""
    import numpy as np
    from PIL import Image

    fr = _raw_frames(raw_dir)
    if len(fr) < 3:
        raise ValueError(f"need at least 3 frames in {raw_dir} to test the loop")

    def d(a, b):
        A, B = (
            np.asarray(Image.open(f"{raw_dir}/{f}").convert("L").resize((480, 270))).astype("float32") for f in (a, b)
        )
        return float(abs(A - B).mean())

    idx = range(0, len(fr) - 1, max(1, len(fr) // 12))
    typical = sum(d(fr[i], fr[i + 1]) for i in idx) / len(idx)
    return d(fr[-1], fr[0]), typical


def _lum(h):
    c = [int(h[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    x, y = sorted((_lum(a), _lum(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)


def check_tokens(only=None):
    """WCAG contrast of every text and flow colour on the grounds it is allowed on, for every installed colour
    (or just `only`) in both variants. Returns the list of failures."""
    bad = []
    for color in [only] if only else colors():
        for name, v in load_theme(color)["variants"].items():
            c = v["colors"]
            g = [c[k] for k in ("G600", "G700", "G800", "G900", "G950")]
            rules = [
                ("T1", g, 7),
                ("T2", g, 4.5),
                ("T3", g if name == "light" else g[1:], 4.5),
                ("W300", g, 4.5),
                ("ROSE3", g, 4.5),
                ("L100", g, 3),
                ("B200", g, 3),
                ("ON_CORE", [c.get("CORE_FILL", c["CORE"])], 4.5),
            ]
            bad += [
                f"{color} {name}: {k} {c[k]} on {b} = {contrast(c[k], b):.2f} < {need}"
                for k, gs, need in rules
                for b in gs
                if contrast(c[k], b) < need
            ]
    return bad


def doctor():
    """Report what the toolchain is missing, with the command that fixes it. Run this first on a new machine."""
    need = []
    for mod, pipname in (("PIL", "pillow"), ("numpy", "numpy"), ("playwright", "playwright")):
        if importlib.util.find_spec(mod) is None:
            need.append(f"pip install {pipname}")
    if "pip install playwright" not in need:
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                p.chromium.launch().close()
        except Exception:
            need.append("python -m playwright install chromium")
    if not shutil.which("ffmpeg"):
        need.append("install ffmpeg (only needed for GIF/MP4)")
    if importlib.util.find_spec("pptx") is None:
        need.append("pip install python-pptx (only needed for slide templates)")
    missing_fonts = [
        fn
        for fam in _FONT_FILES.values()
        for _, _, fn in fam
        if not (ROOT / "assets" / "fonts" / (fn + ".woff2")).exists()
    ]
    if missing_fonts:
        need.append(f"restore font files in assets/fonts: {missing_fonts}")
    need += check_tokens()
    print(f"kit ({', '.join(colors())}): " + ("ready" if not need else "missing -> " + "; ".join(need)))
    return not need


if __name__ == "__main__":
    doctor()
