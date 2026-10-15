"""components: the element library for cut-away scenes and close-up portraits.

Every function returns an SVG string in local coordinates and reads colours from the theme (`T`), so the
same scene renders in the dark and the light variant. Animated parts take p = loop phase 0..1 and move in
whole cycles per loop, so they are seamless by construction. `y` is the floor/base line unless stated.
"""

import math
import random
from kit import *
from kit import T, F


# =====================================================================================================
# structure
# =====================================================================================================
def shell(x, y, w, h, r=0, t=14, tint="ROOM"):
    """Building or hull frame: riveted metal band + cavity. Rooms go inside (x+t, y+t, w-2t, h-2t)."""
    s = [
        rrect(x, y, w, h, r, "url(#metalh)", f'stroke="{T.IN900}" stroke-width="3"'),
        rrect(
            x + t,
            y + t,
            w - 2 * t,
            h - 2 * t,
            max(0, r - t),
            getattr(T, tint),
            f'stroke="{T.IN800}" stroke-width="1.5"',
        ),
    ]
    n = max(2, int((w - 2 * t) / 30))
    m = max(2, int((h - 2 * t) / 30))
    for i in range(n + 1):
        xx = x + t + (w - 2 * t) * i / n
        s += [circ(xx, y + t / 2, 1.6, T.L300, 'opacity="0.8"'), circ(xx, y + h - t / 2, 1.6, T.L300, 'opacity="0.5"')]
    for i in range(1, m):
        yy = y + t + (h - 2 * t) * i / m
        s += [circ(x + t / 2, yy, 1.6, T.L300, 'opacity="0.8"'), circ(x + w - t / 2, yy, 1.6, T.L300, 'opacity="0.5"')]
    s.append(line((x + 3, y + 2), (x + w - 3, y + 2), T.L300, 1.2, 'opacity="0.6"'))
    return "".join(s)


def room(x, y, w, h, tint="ROOM_COOL"):
    """Room tint: ROOM, ROOM_COOL (servers, labs), ROOM_WARM (lounges, reactors), ROOM_DEEP (navigation), ROOM_BILGE."""
    return rrect(x, y, w, h, 0, getattr(T, tint))


def slab(x, y, w, t=10):
    """Floor slab with a lit top edge and a soft shadow beneath."""
    return (
        rrect(x, y + t, w, 10, 0, T.IN900, 'opacity="0.35" filter="url(#blur3)"')
        + rrect(x, y, w, t, 0, T.IN600)
        + rrect(x, y, w, 2.6, 0, T.L300, 'opacity="0.85"')
    )


def wall(x, y, h, t=6):
    return rrect(x - t / 2, y, t, h, 0, T.IN600) + rrect(x - t / 2, y, 1.6, h, 0, T.L300, 'opacity="0.5"')


def truss(x, y, w, h=16):
    n = max(2, int(w / (h * 1.6)))
    pts = [(x + w * i / n, y + (h if i % 2 else 0)) for i in range(n + 1)]
    return (
        path(P(pts, False), "none", f'stroke="{T.L300}" stroke-width="1.3" opacity="0.6"')
        + line((x, y), (x + w, y), T.L300, 1.3, 'opacity="0.6"')
        + line((x, y + h), (x + w, y + h), T.L300, 1.3, 'opacity="0.6"')
    )


def plinth(x, y, w, h=18):
    """Ground slab a building stands on, with its contact shadow."""
    return (
        ell(x + w / 2, y + h + 14, w * 0.5, 12, T.VIGN, 'opacity="0.45" filter="url(#blur8)"')
        + rrect(x, y, w, h, 3, T.IN700, f'stroke="{T.IN900}" stroke-width="2"')
        + rrect(x + 3, y + 1.5, w - 6, 2, 1, T.L300, 'opacity="0.5"')
    )


def sawtooth_roof(x, y, w, n=5, h=None):
    """Row of glazed factory gables sitting on the line y; each has a warm skylight with mullions."""
    tw = w / n
    h = h or tw * 0.58
    s = []
    for i in range(n):
        cx = x + tw * (i + 0.5)
        hw = tw * 0.5
        iw = tw * 0.34
        ih = h - 16
        s.append(
            path(
                P([(cx - hw, y), (cx, y - h), (cx + hw, y)]),
                T.V500,
                f'stroke="{T.IN900}" stroke-width="2.5" stroke-linejoin="round"',
            )
        )
        s.append(
            path(
                P([(cx - iw, y - 5), (cx, y - 5 - ih), (cx + iw, y - 5)]),
                "url(#warmwin)",
                f'stroke="{T.IN900}" stroke-width="1.4" stroke-linejoin="round"',
            )
        )
        for dx in (-iw * 0.4, 0, iw * 0.4):
            s.append(line((cx + dx, y - 5), (cx + dx, y - 5 - ih * (1 - abs(dx) / iw)), T.IN800, 1.2, 'opacity="0.7"'))
    return "".join(s)


def gable(x, y, w, h=None, oculus=True):
    """Pitched roof on the line y, with a lit round window."""
    h = h or w * 0.36
    cx = x + w / 2
    s = path(
        P([(x - 10, y), (cx, y - h), (x + w + 10, y)]),
        T.V500,
        f'stroke="{T.IN900}" stroke-width="2.5" stroke-linejoin="round"',
    )
    if oculus:
        s += circ(cx, y - h * 0.38, 10, T.W100, f'stroke="{T.IN900}" stroke-width="1.6"')
        s += line((cx - 10, y - h * 0.38), (cx + 10, y - h * 0.38), T.IN900, 1.2) + line(
            (cx, y - h * 0.38 - 10), (cx, y - h * 0.38 + 10), T.IN900, 1.2
        )
    return s


def arched_window(x, y, w=26, h=78, lit=False):
    """Tall arched window standing on y. lit=True fills it with the warm gradient and a soft halo."""
    d = f"M{f2(x)},{f2(y)} L{f2(x)},{f2(y - h + w / 2)} A{f2(w / 2)},{f2(w / 2)} 0 0 1 {f2(x + w)},{f2(y - h + w / 2)} L{f2(x + w)},{f2(y)} Z"
    s = glow(x + w / 2, y - h / 2, w * 1.5, h * 0.8, op=0.55) if lit else ""
    s += path(d, "url(#warmwin)" if lit else (T.L300 if T.light else T.IN700), f'stroke="{T.IN900}" stroke-width="1.5"')
    return s + line((x + w / 2, y), (x + w / 2, y - h + 3), T.IN800, 1.2, 'opacity="0.7"')


def arcade(x, y, w, n=12, h=64, lit=True):
    """Row of arched openings (a gallery or cloister) standing on y."""
    step = w / n
    return "".join(arched_window(x + step * i + step * 0.19, y, step * 0.62, h, lit) for i in range(n))


def pendant_lamp(x, y, drop=40, r=48):
    """Hanging lamp from the ceiling point (x, y): cord, shade, bulb and its pool of light."""
    by = y + drop
    return (
        glow(x, by + 12, r)
        + line((x, y), (x, by), T.IN900, 1.2)
        + path(P([(x - 8, by + 5), (x, by - 3), (x + 8, by + 5)]), T.INK)
        + circ(x, by + 6.5, 2.7, T.W100, 'filter="url(#dotglow)"')
    )


def ladder(x, y0, y1, w=16):
    s = line((x, y0), (x, y1), T.L200, 1.7) + line((x + w, y0), (x + w, y1), T.L200, 1.7)
    return s + "".join(
        line((x, yy), (x + w, yy), T.L200, 1.4) for yy in range(int(min(y0, y1)) + 8, int(max(y0, y1)), 12)
    )


def string_lights(a, b, sag=28, n=5, p=0.0):
    """Cable of warm bulbs hung between two points; bulbs breathe in whole cycles."""
    pts = curve(a, b, sag)
    s = path(P(pts, False), "none", f'stroke="{T.IN900}" stroke-width="1.4"')
    for i in range(n):
        x, y = pts[round(len(pts) * (i + 1) / (n + 1))]
        o = 0.7 + 0.3 * math.sin(TAU * (2 * p + i / n))
        s += circ(x, y + 3, 4.2, T.W200, f'opacity="{o:.2f}" filter="url(#dotglow)" stroke="{T.W400}" stroke-width="1"')
    return s


# =====================================================================================================
# weather
# =====================================================================================================
def cloud(x, y, s=1.0, p=0.0, rain=True, bolt=True, seed=5):
    """Storm cloud centred on (x, y) with slanted rain and a lightning bolt that flashes three times per loop."""
    rnd = random.Random(seed)
    g = []
    if rain:
        for _ in range(22):
            rx, ph, n = rnd.uniform(-95, 110), rnd.random(), rnd.choice([3, 4, 5])
            yy = 30 + frac(n * p + ph) * 78
            o = 0.55 * math.sin(math.pi * frac(n * p + ph))
            g.append(line((rx, yy), (rx - 4, yy + 13), T.L200, 1.3, f'opacity="{o:.2f}" stroke-linecap="round"'))
    for cx, cy, r, k in (
        (-64, 12, 38, 0.0),
        (-28, -18, 46, 0.25),
        (20, -32, 52, 0.4),
        (64, -10, 42, 0.2),
        (98, 14, 33, 0.05),
        (-30, 24, 40, 0.0),
        (16, 22, 48, 0.1),
        (62, 26, 40, 0.0),
    ):
        g.append(
            circ(cx, cy, r, hexmix(T.V500, T.V300, k), f'stroke="{T.IN800}" stroke-width="0.8" stroke-opacity="0.5"')
        )
    if bolt and frac(3 * p) < 0.12:
        g.append(
            path(
                P([(12, 44), (0, 68), (11, 68), (1, 98)], False),
                "none",
                f'stroke="{T.W100 if not T.light else T.W400}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round" filter="url(#dotglow)"',
            )
        )
    return f'<g transform="translate({f2(x)},{f2(y)}) scale({s})">' + "".join(g) + "</g>"


# =====================================================================================================
# machines and props
# =====================================================================================================
def battery(x, y, w=58, h=250, level=1.0, cells=8):
    """Reserve tank drawn as a battery; (x, y) is the top-left. level 0..1 = how many cells are lit."""
    s = rrect(x + w / 2 - 9, y - 9, 18, 10, 3, T.IN800, f'stroke="{T.IN900}" stroke-width="2"')
    s += rrect(x, y, w, h, 10, T.IN800, f'stroke="{T.IN900}" stroke-width="3"') + rrect(
        x + 3, y + 3, w - 6, h - 6, 8, "none", f'stroke="{T.L300}" stroke-width="1.2" opacity="0.7"'
    )
    ch = (h - 14 - 4 * (cells - 1)) / cells
    on = round(level * cells)
    for i in range(cells):
        yy = y + h - 7 - ch - i * (ch + 4)
        s += rrect(
            x + 7, yy, w - 14, ch, 2.5, "url(#warmwin)" if i < on else T.IN700, f'stroke="{T.IN900}" stroke-width="1"'
        )
    return s


def conveyor(x, y, w, h=12):
    """Belt whose top surface is at y, on rollers."""
    s = rrect(x, y, w, h, h / 2, T.IN600, f'stroke="{T.IN900}" stroke-width="1.5"') + rrect(
        x + 4, y + 1.5, w - 8, 2, 1, T.L300, 'opacity="0.7"'
    )
    n = max(2, int(w / 27))
    return s + "".join(
        circ(
            x + 12 + (w - 24) * i / (n - 1), y + h + 7, 5, "none", f'stroke="{T.L200}" stroke-width="1.3" opacity="0.7"'
        )
        for i in range(n)
    )


def crate(x, y, s=16):
    """Lit parcel standing on y."""
    return (
        rrect(x, y - s, s, s, 2, T.W200, f'stroke="{T.IN900}" stroke-width="1"')
        + line((x, y - s / 2), (x + s, y - s / 2), T.W400, 1.2)
        + line((x + s / 2, y - s), (x + s / 2, y), T.W400, 1.2)
    )


def car(x, y, s=1.0):
    """Small saloon on an assembly line; wheels rest on y."""
    g = path(
        "M-58,-14 L-58,-30 Q-56,-39 -44,-41 L-30,-43 Q-18,-66 6,-66 L22,-66 Q40,-64 50,-43 L60,-39 Q68,-35 68,-25 L68,-14 Z",
        "url(#metalh)",
        f'stroke="{T.IN900}" stroke-width="2" stroke-linejoin="round"',
    ) + path("M-22,-45 Q-12,-60 6,-60 L8,-45 Z M14,-60 L22,-60 Q34,-58 42,-45 L14,-45 Z", T.MIST, 'opacity="0.35"')
    for wx in (-34, 42):
        g += circ(wx, -10, 11, T.INK) + circ(wx, -10, 4, T.V300)
    return f'<g transform="translate({f2(x)},{f2(y)}) scale({s})">{g}</g>'


def machine(x, y, w=70, h=84):
    """Generic press or processor standing on y: body, hopper, slot, dial and two status lights."""
    bh = h * 0.72
    return (
        rrect(x + w * 0.3, y - h, w * 0.4, h * 0.34, 4, T.V300, f'stroke="{T.IN900}" stroke-width="1.6"')
        + rrect(x, y - bh, w, bh, 8, "url(#metalv)", f'stroke="{T.IN900}" stroke-width="1.8"')
        + rrect(x + w * 0.14, y - bh * 0.78, w * 0.5, 6, 3, T.IN900)
        + circ(
            x + w * 0.8, y - bh * 0.7, 7, T.L100 if not T.light else T.MIST, f'stroke="{T.IN900}" stroke-width="1.4"'
        )
        + line((x + w * 0.8, y - bh * 0.7), (x + w * 0.8 + 4, y - bh * 0.7 - 4), T.IN900, 1.3)
        + circ(x + w * 0.2, y - bh * 0.18, 1.9, T.W300)
        + circ(x + w * 0.3, y - bh * 0.18, 1.9, T.W300)
    )


def server_rack(x, y, w=54, h=110, rows=7, p=0.0, seed=1):
    """Rack standing on y; status lights blink in whole cycles (squares = information, dots = power)."""
    rnd = random.Random(seed)
    s = rrect(x, y - h, w, h, 4, T.IN700, f'stroke="{T.IN900}" stroke-width="1.8"')
    rh = (h - 10) / rows
    for i in range(rows):
        yy = y - h + 6 + i * rh
        s += rrect(x + 5, yy, w - 10, rh - 4, 2, T.IN800 if not T.light else T.V400)
        for k in range(3):
            n, ph = rnd.choice([1, 2, 3, 5]), rnd.random()
            o = 0.25 + 0.75 * (math.sin(TAU * (n * p + ph)) > 0)
            cx, cy = x + 11 + k * 8, yy + (rh - 4) / 2
            s += (
                circ(cx, cy, 1.6, T.W200, f'opacity="{o:.2f}"')
                if k == 2
                else rrect(cx - 1.6, cy - 1.6, 3.2, 3.2, 0.6, T.MIST if T.light else T.L100, f'opacity="{o:.2f}"')
            )
    return s


def clock(x, y, r=16, p=0.0):
    """Wall clock centred on (x, y); the minute hand makes one turn per loop."""
    a = TAU * p - TAU / 4
    return (
        circ(x, y, r, T.W100, f'stroke="{T.IN900}" stroke-width="2.2" filter="url(#dotglow)"')
        + line((x, y), (x + r * 0.7 * math.cos(a), y + r * 0.7 * math.sin(a)), T.INK, 1.8, 'stroke-linecap="round"')
        + line((x, y), (x + r * 0.42, y + r * 0.12), T.INK, 2.2, 'stroke-linecap="round"')
    )


def desk(x, y, w=64, lit=True):
    s = (
        rrect(x, y - 26, w, 4, 1.5, T.L200)
        + line((x + 5, y - 22), (x + 5, y), T.L200, 2)
        + line((x + w - 5, y - 22), (x + w - 5, y), T.L200, 2)
    )
    return s + (rrect(x + w * 0.5, y - 34, 16, 8, 1.5, T.W200, f'stroke="{T.IN900}" stroke-width="0.8"') if lit else "")


def cabinet(x, y, w=28, h=64):
    s = rrect(x, y - h, w, h, 3, T.V400, f'stroke="{T.IN900}" stroke-width="1.6"')
    return s + "".join(
        line((x + 6, y - h + (i + 0.5) * h / 3), (x + w - 6, y - h + (i + 0.5) * h / 3), T.L200, 1.4) for i in range(3)
    )


def screen(x, y, w=60, h=44, kind="bars", p=0.0):
    """Wall display with top-left (x, y). kind = 'bars' | 'line'."""
    s = rrect(x, y, w, h, 4, T.IN900, f'stroke="{T.L200}" stroke-width="1.2"')
    col = T.MIST if T.light else T.L100
    if kind == "bars":
        for i, v in enumerate((0.35, 0.6, 0.45, 0.85, 0.7)):
            v = v * (0.85 + 0.15 * math.sin(TAU * (2 * p + i / 5)))
            bw = (w - 16) / 5
            s += rrect(x + 8 + i * bw, y + h - 7 - v * (h - 16), bw - 3, v * (h - 16), 1, col, 'opacity="0.9"')
    else:
        pts = [(x + 7 + (w - 14) * i / 12, y + h / 2 + math.sin(TAU * (i / 6 + p * 3)) * (h * 0.26)) for i in range(13)]
        s += path(P(pts, False), "none", f'stroke="{col}" stroke-width="1.6" stroke-linejoin="round"')
    return s


def orrery(cx, cy, r=60, p=0.0):
    """Model solar system: tilted orbits, a lit sun, planets in whole orbits per loop."""
    s = "".join(
        ell(cx, cy, r * k, r * k * 0.36, "none", f'stroke="{T.L200}" stroke-width="1" opacity="0.5"')
        for k in (0.45, 0.72, 1.0)
    )
    s += glow(cx, cy, r * 0.5) + circ(
        cx, cy, r * 0.13, T.W200, f'stroke="{T.W400}" stroke-width="1" filter="url(#dotglow)"'
    )
    for k, n, ph, col in ((0.45, 3, 0.1, T.L100), (0.72, 2, 0.5, T.B200), (1.0, 1, 0.8, T.L200)):
        a = TAU * (n * p + ph)
        s += circ(
            cx + r * k * math.cos(a),
            cy + r * k * 0.36 * math.sin(a),
            3.4,
            col,
            f'stroke="{T.IN900}" stroke-width="0.8"',
        )
    return s


def thinking_core(cx, cy, r=44, p=0.0, seed=4):
    """The 'thinking' orb: a lit sphere holding a small network whose nodes pulse in turn."""
    rnd = random.Random(seed)
    nodes = []
    while len(nodes) < 8:
        a, d = rnd.uniform(0, TAU), rnd.uniform(0.15, 0.78) * r
        nodes.append((cx + d * math.cos(a), cy + d * math.sin(a)))
    s = glow(cx, cy, r * 2.3) + circ(cx, cy, r, "url(#warmwin)", f'stroke="{T.W400}" stroke-width="1.6"')
    for a in nodes:
        for b in sorted(nodes, key=lambda q: math.hypot(q[0] - a[0], q[1] - a[1]))[1:3]:
            s += line(a, b, T.ROSE5, 1.1, 'opacity="0.8"')
    for i, (x, y) in enumerate(nodes):
        s += circ(x, y, 2.2 + 1.0 * (0.5 + 0.5 * math.sin(TAU * (2 * p + i / 8))), T.COFFEE)
    return s


def bars(x, y, w, h, values, labels=None, highlight=None, unit=""):
    """Small bar chart on the baseline y. One series in the information colour; `highlight` index takes the accent.
    Values are printed on the bars and categories under them, so nothing depends on colour alone."""
    n = len(values)
    bw = w / n
    top = max(values) or 1
    s = line((x, y), (x + w, y), T.L200, 1.4)
    for i, v in enumerate(values):
        bh = h * v / top
        col = T.W300 if i == highlight else T.L100
        s += rrect(x + i * bw + bw * 0.16, y - bh, bw * 0.68, bh, 3, col)
        s += text(x + (i + 0.5) * bw, y - bh - 8, f"{v:g}{unit}", 14, T.T1, F.MONO, 'text-anchor="middle"')
        if labels:
            s += text(x + (i + 0.5) * bw, y + 22, labels[i], 14, T.T2, F.SANS, 'text-anchor="middle"')
    return s


# =====================================================================================================
# large architecture
# =====================================================================================================
def dome(cx, cy, rx, ry, rows=5, cols=16, oculus=True, shaft=0):
    """Coffered dome seen from inside, springing from the line cy. shaft>0 drops a light shaft that far below the oculus."""
    s = path(
        f"M{f2(cx - rx)},{f2(cy)} A{f2(rx)},{f2(ry)} 0 0 1 {f2(cx + rx)},{f2(cy)} Z",
        "url(#metalh)",
        f'stroke="{T.IN900}" stroke-width="2.5"',
    )

    def pt(phi, th):
        return (cx + rx * math.cos(phi) * math.sin(th) * 0.98, cy - ry * math.sin(phi) * 0.96)

    span = math.radians(82)
    for r in range(rows):
        p0, p1 = math.radians(9 + r * 62 / rows), math.radians(9 + (r + 0.74) * 62 / rows)
        for c in range(cols):
            t0 = -span + 2 * span * (c + 0.14) / cols
            t1 = -span + 2 * span * (c + 0.86) / cols
            s += path(
                P([pt(p0, t0), pt(p0, t1), pt(p1, t1), pt(p1, t0)]),
                T.IN700 if not T.light else T.V300,
                'opacity="0.55"',
            )
    if oculus:
        oy = cy - ry * 0.93
        if shaft:
            s += path(
                P(
                    [
                        (cx - rx * 0.13, oy),
                        (cx + rx * 0.13, oy),
                        (cx + rx * 0.24, oy + shaft),
                        (cx - rx * 0.24, oy + shaft),
                    ]
                ),
                "url(#beamv)",
                f'style="mix-blend-mode:{T.GLOW_BLEND}"',
            )
        s += glow(cx, oy, rx * 0.3, ry * 0.16) + ell(
            cx, oy, rx * 0.14, ry * 0.045, T.W100, f'stroke="{T.W400}" stroke-width="1"'
        )
    return s


def gallery_ring(cx, cy, rx, ry, t=12, posts=26):
    """Front half of a circular balcony: slab, lit edge and a railing. Stack several for tiers."""
    arc = lambda yy, a, b: f"M{f2(cx - a)},{f2(yy)} A{f2(a)},{f2(b)} 0 0 0 {f2(cx + a)},{f2(yy)}"
    s = path(
        arc(cy, rx, ry) + f" L{f2(cx + rx)},{f2(cy + t)} A{f2(rx)},{f2(ry)} 0 0 1 {f2(cx - rx)},{f2(cy + t)} Z",
        T.IN600,
        f'stroke="{T.IN900}" stroke-width="1.2"',
    )
    s += path(arc(cy, rx, ry), "none", f'stroke="{T.L300}" stroke-width="2" opacity="0.85"') + path(
        arc(cy - 15, rx, ry), "none", f'stroke="{T.L200}" stroke-width="1.3" opacity="0.8"'
    )
    for i in range(1, posts):
        a = math.pi * i / posts
        x, y = cx - rx * math.cos(a), cy + ry * math.sin(a)
        s += line((x, y), (x, y - 15), T.L200, 1, 'opacity="0.6"')
    return s


def lantern_tower(cx, base, w=170, tiers=4, tier_h=118, seed=2):
    """Central lit tower of stacked glazed drums (the single light of a watchtower scene). Stands on `base`."""
    rnd = random.Random(seed)
    s = glow(cx, base - tiers * tier_h / 2, w * 1.9, tiers * tier_h * 0.75, op=0.9)
    for i in range(tiers):
        top = base - (i + 1) * tier_h + 16
        bh = tier_h - 20
        x0 = cx - w / 2
        s += rrect(x0, top, w, bh, 2, "url(#warmwin)", f'stroke="{T.IN900}" stroke-width="2"')
        for _ in range(rnd.choice([1, 2, 2])):
            fx = cx + rnd.uniform(-w * 0.26, w * 0.26)
            fy = top + bh
            s += circ(fx, fy - 46, 11, T.ROSE5, 'opacity="0.42"') + rrect(
                fx - 17, fy - 34, 34, 34, 13, T.ROSE5, 'opacity="0.42"'
            )
        s += rrect(x0, top, w * 0.22, bh, 0, T.ROSE3, 'opacity="0.28"') + rrect(
            x0 + w * 0.78, top, w * 0.22, bh, 0, T.ROSE3, 'opacity="0.38"'
        )
        for fxr in (0.22, 0.78):
            s += line((x0 + w * fxr, top), (x0 + w * fxr, top + bh), T.IN900, 2.2)
        for fxr in (0.11, 0.36, 0.5, 0.64, 0.89):
            s += line((x0 + w * fxr, top), (x0 + w * fxr, top + bh), T.IN900, 0.9, 'opacity="0.7"')
        s += ell(cx, top + bh + 3, w / 2 + 16, 11, T.V400, f'stroke="{T.IN900}" stroke-width="2"') + ell(
            cx, top + bh + 1, w / 2 + 13, 8, "none", f'stroke="{T.L300}" stroke-width="1.2" opacity="0.7"'
        )
    ty = base - tiers * tier_h + 16
    s += path(
        P([(cx - w / 2 - 10, ty), (cx, ty - 46), (cx + w / 2 + 10, ty)]),
        T.V500,
        f'stroke="{T.IN900}" stroke-width="2" stroke-linejoin="round"',
    )
    return s + circ(cx, ty - 50, 4.5, T.W200, 'filter="url(#dotglow)"')


def saucer(cx, cy, rx=330, ry=92, rivet_gap=22):
    """Lens-shaped hull with a glass dome and an emitter underneath.
    Returns (svg, cavity_path): put cavity_path in a <clipPath> and draw decks and crew inside it."""
    lens = lambda a, top, bot: (
        f"M{f2(cx - a)},{f2(cy)} Q{f2(cx)},{f2(cy - 2 * top)} {f2(cx + a)},{f2(cy)} Q{f2(cx)},{f2(cy + 2 * bot)} {f2(cx - a)},{f2(cy)} Z"
    )
    cavity = lens(rx - 26, ry * 0.9 - 13, ry * 1.1 - 13)
    dw, dh = rx * 0.4, ry * 1.25
    dy = cy - ry * 0.84
    s = path(
        f"M{f2(cx - dw)},{f2(dy)} A{f2(dw)},{f2(dh)} 0 0 1 {f2(cx + dw)},{f2(dy)} Z",
        T.MIST,
        f'fill-opacity="{T.GLASS_OP}" stroke="{T.L200}" stroke-width="1.6"',
    )
    s += path(lens(rx, ry * 0.9, ry * 1.1), "url(#metalh)", f'stroke="{T.IN900}" stroke-width="3"') + path(
        cavity, T.ROOM, f'stroke="{T.IN800}" stroke-width="1.5"'
    )
    n = int(2 * rx / rivet_gap)
    for i in range(1, n):
        t = i / n
        x = cx - rx + 2 * rx * t
        k = 2 * t * (1 - t) * 2
        s += circ(x, cy - (ry * 0.9 - 6.5) * k, 1.6, T.L300, 'opacity="0.8"') + circ(
            x, cy + (ry * 1.1 - 6.5) * k, 1.6, T.L300, 'opacity="0.5"'
        )
    s += rrect(cx - dw - 8, dy - 5, 2 * dw + 16, 10, 5, T.V400, f'stroke="{T.IN900}" stroke-width="1.6"')
    ey = cy + ry * 1.08
    s += (
        ell(cx, ey, 62, 15, T.V400, f'stroke="{T.IN900}" stroke-width="2"')
        + glow(cx, ey + 6, 70, 26)
        + ell(cx, ey + 3, 26, 7, T.W100, 'filter="url(#dotglow)"')
    )
    return s, cavity


def tractor_beam(cx, y, h=300, w0=70, w1=270, p=0.0, seed=9):
    """Cone of light below an emitter at (cx, y) with rising rings and sparks (two cycles per loop)."""
    cone = lambda a, b: P([(cx - a / 2, y), (cx + a / 2, y), (cx + b / 2, y + h), (cx - b / 2, y + h)])
    s = path(cone(w0, w1), "url(#beamv)", f'opacity="0.75" style="mix-blend-mode:{T.GLOW_BLEND}"') + path(
        cone(w0 * 0.5, w1 * 0.42), "url(#beamv)", f'opacity="0.8" style="mix-blend-mode:{T.GLOW_BLEND}"'
    )
    ring = T.MIST if not T.light else T.W400
    for k in range(3):
        t = 1 - frac(2 * p + k / 3)
        wy = lerp(w0, w1, t) / 2
        s += ell(
            cx,
            y + h * t,
            wy,
            wy * 0.12,
            "none",
            f'stroke="{ring}" stroke-width="1.3" opacity="{0.75 * math.sin(math.pi * t):.2f}"',
        )
    rnd = random.Random(seed)
    for _ in range(26):
        u, ph, n = rnd.uniform(-0.4, 0.4), rnd.random(), rnd.choice([1, 2, 3])
        t = 1 - frac(n * p + ph)
        s += circ(
            cx + u * lerp(w0, w1, t),
            y + h * t,
            rnd.choice([1.0, 1.4, 1.9]),
            T.W100 if not T.light else T.W300,
            f'opacity="{0.9 * math.sin(math.pi * t):.2f}"',
        )
    return s + glow(cx, y + h, w1 * 0.55, 22, op=0.8)


# =====================================================================================================
# close-up portrait mode (large figures, soft gradients, one beam of light)
# =====================================================================================================
def bust_human(x, y, s=1.0, facing=1):
    """Head-and-shoulders human in strict profile. (x, y) = base of the neck; the head is about 370*s tall and the
    shoulders run about 340*s below, normally cropped by the canvas. The face stays minimal: a brow, a closed eye,
    a nostril and a mouth line, lit from the side it faces with a rim of light along the profile."""
    skin_dark = hexmix(T.V300, T.W400, 0.22)
    face = (
        "M44,-452 C86,-432 106,-388 108,-344 L114,-318 L106,-300 C120,-272 146,-238 156,-222 "
        "Q162,-210 148,-207 L122,-204 C128,-196 130,-186 124,-180 L116,-176 C126,-170 124,-158 114,-152 "
        "C108,-148 110,-140 114,-128 C118,-110 104,-96 80,-92 C30,-88 -20,-100 -50,-140 L-70,-200 "
        "C-110,-300 -120,-420 -40,-460 Z"
    )
    profile = (
        "M44,-452 C86,-432 106,-388 108,-344 L114,-318 L106,-300 C120,-272 146,-238 156,-222 "
        "Q162,-210 148,-207 L122,-204 C128,-196 130,-186 124,-180 L116,-176 C126,-170 124,-158 114,-152 "
        "C108,-148 110,-140 114,-128 C118,-110 104,-96 80,-92"
    )
    hair = (
        "M46,-452 C10,-500 -120,-512 -190,-450 C-250,-395 -262,-290 -236,-200 C-222,-150 -196,-118 -160,-104 "
        "L-112,-118 C-104,-150 -92,-185 -84,-210 C-70,-240 -60,-275 -40,-300 C-10,-330 20,-380 46,-452 Z"
    )
    g = [
        # jacket, shirt collar, tie knot, lapel
        path(
            "M-370,340 C-370,130 -262,26 -100,-6 L12,64 L66,20 C206,58 306,160 330,340 Z",
            "url(#cloth)",
            f'stroke="{T.IN900}" stroke-width="2"',
        ),
        path(
            "M-74,-30 L44,8 L60,74 L16,52 L-64,12 Z",
            T.MIST if not T.light else T.G600,
            f'stroke="{T.IN800}" stroke-width="1.2"',
        ),
        path("M16,52 L60,74 L50,122 L24,108 Z", T.IN700, 'opacity="0.9"'),
        path("M12,64 C42,150 58,250 62,340", "none", f'stroke="{T.L300}" stroke-width="1.6" opacity="0.45"'),
        path("M-260,120 C-200,60 -140,30 -100,-6", "none", f'stroke="{T.L200}" stroke-width="1.4" opacity="0.25"'),
        # neck, with the shadow the jaw throws on it
        path("M-62,-150 C-58,-90 -70,-40 -78,-20 L50,8 C46,-30 42,-70 48,-96 Z", skin_dark),
        ell(-4, -96, 66, 22, T.IN900, 'opacity="0.35" filter="url(#blur8)"'),
        # head
        path(face, "url(#skin)"),
        ell(64, -236, 40, 20, T.W200, 'opacity="0.22" filter="url(#blur8)"'),
        path(
            "M-50,-140 C-20,-104 30,-92 80,-94",
            "none",
            f'stroke="{T.IN800}" stroke-width="10" opacity="0.18" filter="url(#blur3)"',
        ),
        path(profile, "none", f'stroke="{T.W200}" stroke-width="2.2" stroke-linejoin="round" opacity="0.55"'),
        # hair, with two highlight strands
        path(hair, "url(#cloth)", f'stroke="{T.IN900}" stroke-width="1.5"'),
        path(
            "M-160,-452 C-100,-486 -30,-486 24,-460",
            "none",
            f'stroke="{T.L200}" stroke-width="3" stroke-linecap="round" opacity="0.5"',
        ),
        path(
            "M-206,-394 C-150,-436 -84,-446 -36,-432",
            "none",
            f'stroke="{T.L200}" stroke-width="2" stroke-linecap="round" opacity="0.35"',
        ),
        # ear
        ell(-56, -214, 20, 30, skin_dark, f'stroke="{T.IN800}" stroke-width="1.2" stroke-opacity="0.5"'),
        path(
            "M-60,-230 C-46,-222 -46,-204 -58,-196",
            "none",
            f'stroke="{T.IN800}" stroke-width="1.6" stroke-linecap="round" opacity="0.6"',
        ),
        # face details
        path("M70,-320 Q88,-326 106,-316", "none", f'stroke="{T.INK}" stroke-width="3.2" stroke-linecap="round"'),
        path("M74,-284 Q90,-276 104,-284", "none", f'stroke="{T.INK}" stroke-width="2.6" stroke-linecap="round"'),
        path(
            "M128,-214 Q136,-218 140,-212",
            "none",
            f'stroke="{T.INK}" stroke-width="1.8" stroke-linecap="round" opacity="0.55"',
        ),
        path("M98,-177 L118,-177", "none", f'stroke="{T.INK}" stroke-width="2.2" stroke-linecap="round" opacity="0.8"'),
    ]
    return f'<g transform="translate({f2(x)},{f2(y)}) scale({f2(s * facing)},{f2(s)})">' + "".join(g) + "</g>"


def bust_robot(x, y, s=1.0, facing=1, visor=True):
    """Head-and-shoulders robot: capsule head with a glowing visor band, an ear module, vent lines, a ribbed neck and
    broad shoulders. (x, y) = collar centre. The visor points the way it faces; the rim light sits on the back."""
    g = [
        path(
            "M-330,340 C-330,130 -230,40 -100,20 L100,20 C230,40 330,130 330,340 Z",
            "url(#chrome)",
            f'stroke="{T.IN900}" stroke-width="2"',
        ),
        path("M-210,140 Q0,104 170,116", "none", f'stroke="{T.IN800}" stroke-width="1.6" opacity="0.5"'),
        line((0, 112), (0, 340), T.IN800, 1.4, 'opacity="0.5"'),
        path(
            "M200,70 C268,110 318,190 328,330",
            "none",
            f'stroke="{T.W400}" stroke-width="2.4" stroke-linecap="round" opacity="0.55"',
        ),
        ell(0, 22, 122, 22, T.IN900),
    ]
    for i in range(4):
        g.append(
            rrect(
                -60 - (i % 2) * 5,
                -122 + i * 34,
                120 + (i % 2) * 10,
                38,
                19,
                "url(#metalv)",
                f'stroke="{T.IN900}" stroke-width="1.6"',
            )
        )
    g += [
        ell(0, -116, 74, 12, T.IN900, 'opacity="0.5" filter="url(#blur3)"'),
        rrect(-160, -520, 320, 400, 150, "url(#chrome)", f'stroke="{T.IN900}" stroke-width="2.5"'),
        path(
            "M-110,-500 C-60,-522 20,-524 70,-506",
            "none",
            f'stroke="{T.MIST}" stroke-width="3" stroke-linecap="round" opacity="0.45"',
        ),
        path("M-20,-518 C-10,-400 -30,-250 -22,-122", "none", f'stroke="{T.IN800}" stroke-width="1.6" opacity="0.6"'),
        path("M-158,-210 Q-90,-200 -22,-214", "none", f'stroke="{T.IN800}" stroke-width="1.6" opacity="0.6"'),
        path("M-150,-170 Q-60,-138 40,-150", "none", f'stroke="{T.IN800}" stroke-width="1.4" opacity="0.4"'),
        ell(0, -150, 150, 34, T.IN900, 'opacity="0.18" filter="url(#blur8)"'),
        path(
            "M150,-430 C166,-380 166,-260 150,-200",
            "none",
            f'stroke="{T.W400}" stroke-width="2.4" stroke-linecap="round" opacity="0.85"',
        ),
        circ(92, -300, 34, "url(#metalv)", f'stroke="{T.IN900}" stroke-width="2"'),
        circ(92, -300, 18, T.IN800),
        circ(92, -300, 4, T.W300, 'filter="url(#dotglow)"'),
    ]
    if visor:
        g += [
            glow(-60, -332, 170, 70, op=0.8),
            rrect(-160, -360, 200, 56, 28, T.W200, f'stroke="{T.W400}" stroke-width="1.2" filter="url(#dotglow)"'),
            rrect(-150, -352, 120, 10, 5, T.W100, 'opacity="0.7"'),
        ]
    g += [line((40, y0), (70, y0), T.IN800, 4.2, 'stroke-linecap="round" opacity="0.8"') for y0 in (-250, -231, -212)]
    g.append(circ(48, -408, 5, T.W100, 'filter="url(#dotglow)"'))
    return f'<g transform="translate({f2(x)},{f2(y)}) scale({f2(-s * facing)},{f2(s)})">' + "".join(g) + "</g>"


def lantern(x, y, s=1.0, p=0.0, lit=True, glow_r=3.2):
    """Hanging glass lantern, the system's emblem. (x, y) = top of the ring; it stands about 230*s tall.
    Glass panes, a dark metal cap and base, a hot core and a pool of light; the flame flickers four times per loop."""
    k = 0.94 + 0.06 * math.sin(TAU * 4 * p) if lit else 0
    g = []
    if lit:
        g.append(glow(0, 120, 70 * glow_r, 70 * glow_r * 0.9, op=round(0.9 * k, 3)))
    g += [
        circ(0, 0, 14, "none", f'stroke="{T.IN900}" stroke-width="5"'),
        circ(0, 0, 14, "none", f'stroke="{T.L200}" stroke-width="1.2" opacity="0.5"'),
        rrect(-6, 12, 12, 14, 3, T.IN800),
        path(
            P([(-58, 64), (-30, 26), (30, 26), (58, 64)]),
            "url(#metalh)",
            f'stroke="{T.IN900}" stroke-width="2.5" stroke-linejoin="round"',
        ),
        rrect(-64, 62, 128, 12, 4, T.IN700, f'stroke="{T.IN900}" stroke-width="2"'),
        path(
            P([(-50, 74), (50, 74), (56, 184), (-56, 184)]),
            "url(#warmwin)" if lit else T.IN700,
            f'stroke="{T.IN900}" stroke-width="2.5" stroke-linejoin="round" opacity="0.92"',
        ),
    ]
    if lit:
        g += [
            ell(0, 140, 30, 40, T.W200, f'opacity="{0.55 * k:.2f}" filter="url(#blur8)"'),
            path(
                "M0,104 C14,124 16,146 0,160 C-16,146 -14,124 0,104 Z",
                T.W100,
                f'opacity="{k:.2f}" filter="url(#dotglow)"',
            ),
            path("M0,124 C6,134 6,146 0,152 C-6,146 -6,134 0,124 Z", T.W200),
        ]
    g += [
        line((0, 74), (0, 184), T.IN900, 3, 'opacity="0.85"'),
        line((-34, 74), (-37, 184), T.IN900, 1.6, 'opacity="0.55"'),
        line((34, 74), (37, 184), T.IN900, 1.6, 'opacity="0.55"'),
        rrect(-66, 182, 132, 16, 5, T.IN700, f'stroke="{T.IN900}" stroke-width="2"'),
        path(
            P([(-44, 198), (44, 198), (30, 222), (-30, 222)]),
            "url(#metalh)",
            f'stroke="{T.IN900}" stroke-width="2" stroke-linejoin="round"',
        ),
        rrect(-60, 64, 4, 8, 2, T.L300, 'opacity="0.7"'),
        path("M-44,82 L-48,176", "none", f'stroke="{T.MIST}" stroke-width="3" stroke-linecap="round" opacity="0.35"'),
    ]
    return f'<g transform="translate({f2(x)},{f2(y)}) scale({f2(s)})">' + "".join(g) + "</g>"


def light_cone(x0, y0, x1, y_top, y_bot, spread0=8, op=0.85):
    """Beam from a source at (x0, y0) widening to the segment x1, y_top..y_bot. Brightest at the source."""
    grad = "beam" if x1 >= x0 else "beamr"
    return path(
        P([(x0, y0 - spread0), (x1, y_top), (x1, y_bot), (x0, y0 + spread0)]),
        f"url(#{grad})",
        f'opacity="{op}" style="mix-blend-mode:{T.GLOW_BLEND}" filter="url(#blur3)"',
    )


def orb(x, y, r=60):
    """Free-standing light source: the one warm light of a portrait scene."""
    return (
        glow(x, y, r * 3.2)
        + circ(x, y, r, "url(#warmwin)", f'stroke="{T.W400}" stroke-width="1.2" filter="url(#dotglow)"')
        + circ(x - r * 0.2, y - r * 0.2, r * 0.45, T.W100, 'opacity="0.7" filter="url(#blur8)"')
    )


def headlamp(x, y, r=58, facing=1):
    """Round lamp worn in front of a face (examiner's mirror): dark ring, hot lens."""
    return (
        glow(x, y, r * 2.2)
        + circ(x, y, r, T.W100, f'stroke="{T.INK}" stroke-width="{r * 0.18:.1f}" filter="url(#dotglow)"')
        + path(
            f"M{f2(x + facing * r * 0.5)},{f2(y - r * 0.6)} A{f2(r * 0.8)},{f2(r * 0.8)} 0 0 1 {f2(x + facing * r * 0.78)},{f2(y + r * 0.1)}",
            "none",
            f'stroke="{T.W400}" stroke-width="2" stroke-linecap="round" opacity="0.8"',
        )
    )


def pane(x, y, w, h, lean=46, silhouette=True):
    """Frosted screen or mirror standing between two characters: a lit panel with a bright leading edge and a
    blurred silhouette behind it. (x, y) = top-left of the near edge."""
    quad = P([(x, y), (x + w, y + lean), (x + w, y + h - lean), (x, y + h)])
    s = path(quad, "url(#warmwin)", 'opacity="0.82"') + path(quad, T.ROSE3, 'opacity="0.22"')
    if silhouette:
        fx, fy = x + w * 0.46, y + h * 0.42
        s += f'<g opacity="0.42" filter="url(#blur8)">{ell(fx, fy, w * 0.2, h * 0.11, T.INK)}{rrect(fx - w * 0.34, fy + h * 0.13, w * 0.68, h * 0.42, w * 0.3, T.INK)}</g>'
    return s + rrect(x + w - 5, y + lean, 12, h - 2 * lean, 2, T.W100, 'filter="url(#dotglow)"')


def camera_eye(x, y, s=1.0, facing=1):
    """Lens module on a machine's head, the mechanical counterpart of an eye: housing, shade, one hot lens."""
    g = (
        rrect(-34, -58, 68, 116, 22, T.INK, f'stroke="{T.IN900}" stroke-width="2"')
        + path(P([(34, -44), (112, -62), (112, 62), (34, 44)]), T.IN800, f'stroke="{T.IN900}" stroke-width="2"')
        + glow(0, 0, 70)
        + circ(0, 0, 25, T.ROSE3, f'stroke="{T.W400}" stroke-width="1.5" filter="url(#dotglow)"')
        + circ(-6, -6, 8, T.W100, 'opacity="0.8"')
    )
    return f'<g transform="translate({f2(x)},{f2(y)}) scale({f2(s * facing)},{f2(s)})">{g}</g>'
