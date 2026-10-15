"""scenes: a library of ready cut-aways for the ideas people explain most often.

    python scenes.py                                      list the scenes
    python scenes.py supply_chain                         render one, annotated, in the default colour
    python scenes.py supply_chain teal light modern clean any colour, variant and type set; clean = no words
    python scenes.py all [colour] [variant]               every scene into ./out/scenes/

Each scene is a function of t (seconds into the loop), so it is also a seamless loop, and carries its own words
(a question, an answer line and three labels, written to the voice guide). Use one as it is, change the words with
build(name, words={...}), or copy its draw function as the start of a new picture.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from components import *
from kit import C, T

BASE = 960  # ground line of every scene
TEXT = [(40, 40, 760, 230), (40, 400, 440, 1000), (1520, 260, 1900, 1000)]  # kept free of twinkles
L1, L2, R1, R2 = (72, 440), (72, 720), (1580, 360), (1580, 680)
ZY = BASE + 30  # scenes are enlarged about (960, ZY)  # label slots
SCENES = {}


def scene(title, answer, labels, alt, centre=(960, 600), lit=(960, 700, 420), focus=(420, 260, 1500, 990), zoom=1.1):
    """Register a draw(p) -> (svg, anchors) function. labels = [(slot, anchor key, title, text)]."""

    def reg(fn):
        SCENES[fn.__name__] = dict(
            draw=fn, title=title, answer=answer, labels=labels, alt=alt, centre=centre, lit=lit, focus=focus, zoom=zoom
        )
        return fn

    return reg


def building(x, w, floors, roof=None, n=3, tints=None, base=BASE):
    """Cut-away building standing on `base`. floors = heights, ground floor first.
    Returns (svg, rooms, inner) with rooms[i] = (x0, floor_y, width, height) and inner = (x, y, w, h) of the cavity."""
    t = 14
    H = sum(floors) + 2 * t
    top = base - H
    s = [shell(x, top, w, H)]
    x0, w0 = x + t, w - 2 * t
    rooms, y = [], base - t
    tints = tints or ["ROOM"] * len(floors)
    for h, tint in zip(floors, tints):
        s.append(room(x0, y - h, w0, h, tint))
        rooms.append((x0, y, w0, h))
        y -= h
    s += [slab(rx, fy, rw) for rx, fy, rw, _ in rooms[1:]]
    if roof == "saw":
        s.append(sawtooth_roof(x, top, w, n))
    elif roof == "gable":
        s.append(gable(x, top, w))
    elif roof == "flat":
        s.append(rrect(x - 6, top - 10, w + 12, 12, 2, T.V400, f'stroke="{T.IN900}" stroke-width="2"'))
    return "".join(s), rooms, (x0, top + t, w0, H - 2 * t)


def zoomer(z):
    """Map a point of the drawing to the canvas after the scene's enlargement."""
    return lambda pt: (960 + (pt[0] - 960) * z, ZY + (pt[1] - ZY) * z)


def lightmask(rect, op=0.8):
    """Multiply the light mask over a cavity so rooms fall off away from the scene's one light."""
    x, y, w, h = rect
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#litmask)" style="mix-blend-mode:multiply" opacity="{op}"/>'


def ground(x0, x1, y=BASE):
    return plinth(x0, y, x1 - x0)


def stand(x, y, w=90, h=60, kind="bars", p=0.0):
    """Free-standing display on a post, its foot on y."""
    return line((x + w / 2, y), (x + w / 2, y - 40), T.L200, 2.4) + screen(x, y - 40 - h, w, h, kind, p)


def wire(pts, kind, p, cycles=20, gap=14, w=4):
    return cable(pts, w) + flow(pts, kind, p, cycles, gap=gap)


# =====================================================================================================
# the library
# =====================================================================================================
@scene(
    ["How does a parcel reach", "your door?"],
    "Made, stored, then driven: every hand-off is a lit link.",
    [
        (L1, "factory", "The factory", "Parts become products on the line, checked before they leave."),
        (R1, "store", "The warehouse", "Stock waits on the shelves until an order calls it out."),
        (R2, "van", "The last mile", "The shortest trip and the dearest: one van, many doors."),
    ],
    "Cut-away of a factory and a warehouse, with a van carrying a lit parcel along a road to a house.",
    lit=(930, 820, 380),
)
def supply_chain(p):
    s = [ground(440, 1500)]
    fac, fr, _ = building(460, 260, [150, 124], "saw", 3, ["ROOM_WARM", "ROOM"])
    wh, wr, wi = building(760, 250, [230], "gable", tints=["ROOM_COOL"])
    s += [fac, wh]
    (x0, fy, _, _), (x1, fy1, _, _) = fr
    s += [conveyor(x0 + 10, fy - 26, 200), crate(x0 + 40, fy - 26), crate(x0 + 100, fy - 26), crate(x0 + 160, fy - 26)]
    s += [machine(x0 + 150, fy - 40, 50, 60), standing(x0 + 20, fy, 1, reach=(x0 + 40, fy - 36))]
    s += [pendant_lamp(x0 + 60, fy - 150, 30), pendant_lamp(x0 + 170, fy - 150, 30)]
    s += [
        desk(x1 + 20, fy1),
        seated(x1 + 44, fy1 - 14),
        cabinet(x1 + 110, fy1),
        standing(x1 + 180, fy1, -1, reach=(x1 + 150, fy1 - 30)),
    ]
    s += [screen(x1 + 140, fy1 - 100, 60, 40, "bars", p)]
    X, F0, W, _ = wr[0]
    s += [shelf(X + 10, F0, 66, 150, 5, seed=2), shelf(X + 86, F0, 66, 150, 5, seed=5, lit=0.25)]
    s += [ladder(X + 150, F0 - 150, F0), standing(X + 196, F0, -1, carry=True), pendant_lamp(X + 110, F0 - 230, 40, 60)]
    s += [lightmask(wi)]
    s += [road(1030, BASE - 14, 330), truck(1190, BASE - 14, 0.9), house(1384, BASE, 96, 66)]
    s += [flow([(700, BASE - 30), (800, BASE - 30)], "energy", p, 12, gap=12)]
    s += [flow([(1000, BASE - 22), (1300, BASE - 22), (1400, BASE - 22)], "energy", p, 20, gap=14)]
    return "".join(s), dict(factory=(x0 + 100, fy - 60), store=(X + 90, F0 - 120), van=(1190, BASE - 60))


@scene(
    ["Where does a dashboard's", "number come from?"],
    "Records flow in, get cleaned, stored and counted, then shown.",
    [
        (L1, "src", "The sources", "Shops, homes and machines each write down what just happened."),
        (R1, "proc", "The cleaning hall", "Duplicates go, gaps are flagged, and every record gets a time."),
        (R2, "dash", "The dashboard", "One number, kept fresh, with the trail behind it."),
    ],
    "Homes and a shop send glowing records along pipes into a hall of servers, then a store, then a big screen.",
    lit=(910, 760, 380),
)
def data_pipeline(p):
    s = [ground(440, 1500)]
    s += [house(470, BASE, 90, 60), house(470, BASE - 140, 90, 60, lit=False)]
    s += [plinth(460, BASE - 140, 110, 10)]
    hall, hr, hi = building(700, 330, [140, 130], "flat", tints=["ROOM_COOL", "ROOM"])
    s += [hall]
    (x0, f0, _, _), (x1, f1, _, _) = hr
    s += [server_rack(x0 + 14 + i * 62, f0, 50, 110, 6, p, seed=i) for i in range(3)]
    s += [machine(x0 + 210, f0, 60, 70), standing(x0 + 196, f0, 1, reach=(x0 + 214, f0 - 40))]
    s += [desk(x1 + 30, f1), seated(x1 + 54, f1 - 14), desk(x1 + 140, f1), seated(x1 + 164, f1 - 14)]
    s += [screen(x1 + 200, f1 - 100, 70, 46, "line", p), pendant_lamp(x1 + 120, f1 - 130, 30)]
    s += [lightmask(hi)]
    st, sr, _ = building(1060, 160, [200], "gable", tints=["ROOM_DEEP"])
    X, F0, _, _ = sr[0]
    s += [st, shelf(X + 8, F0, 56, 130, 4, seed=7), shelf(X + 70, F0, 56, 130, 4, seed=8, lit=0.3)]
    s += [stand(1300, BASE, 150, 96, "bars", p), standing(1474, BASE, -1, reach=(1450, BASE - 100))]
    s += [wire([(560, BASE - 30), (650, BASE - 30), (650, BASE - 60), (714, BASE - 60)], "info", p)]
    s += [wire([(560, BASE - 170), (650, BASE - 170), (650, BASE - 200), (714, BASE - 200)], "info", p)]
    s += [wire([(1016, BASE - 60), (1074, BASE - 60)], "info", p, 8)]
    s += [wire([(1206, BASE - 80), (1250, BASE - 80), (1250, BASE - 140), (1300, BASE - 140)], "info", p, 10)]
    return "".join(s), dict(src=(520, BASE - 50), proc=(x0 + 100, f0 - 80), dash=(1375, BASE - 150))


@scene(
    ["How does a data centre", "stay cool?"],
    "Cold water carries the servers' heat up and out through the roof.",
    [
        (L1, "racks", "The server halls", "Rows of machines turn power into answers, and into heat."),
        (R1, "roof", "The chillers", "Warm water rises, gives its heat to the night air and falls again."),
        (R2, "ctl", "The control room", "Two people watch a thousand numbers, mostly temperature."),
    ],
    "Cut-away data centre with rows of server racks, coolant pipes looping to chillers on the roof and a lit control room.",
    lit=(1140, 860, 420),
)
def data_centre(p):
    s = [ground(440, 1500)]
    b, rr, inner = building(500, 780, [150, 150], "flat", tints=["ROOM_COOL", "ROOM_COOL"])
    s += [b]
    (x0, f0, w0, _), (x1, f1, _, _) = rr
    s += [wall(x0 + 540, f0 - 150, 150), room(x0 + 543, f0 - 150, w0 - 543, 150, "ROOM_WARM")]
    for k, (yy, nr) in enumerate(((f1, 8), (f0, 7))):
        s += [server_rack(x0 + 20 + i * 64, yy, 50, 116, 7, p, seed=i + 9 * k) for i in range(nr)]
    s += [standing(x0 + 300, f1, 1, reach=(x0 + 316, f1 - 60)), standing(x0 + 168, f0, -1, carry=True)]
    s += [desk(x0 + 600, f0, 80), seated(x0 + 630, f0 - 14), screen(x0 + 580, f0 - 110, 60, 40, "line", p)]
    s += [screen(x0 + 650, f0 - 110, 60, 40, "bars", p), clock(x0 + 700, f0 - 132, 11, p)]
    s += [pendant_lamp(x0 + 640, f0 - 150, 26)]
    top = inner[1] - 14
    s += [tank(560 + i * 130, top - 10, 70, 60, 0.6) for i in range(5)]
    s += [rrect(540, top - 12, 660, 6, 2, T.IN700)]
    pipe_pts = [(620, top - 10), (620, f1 - 130), (1150, f1 - 130), (1150, top - 10)]
    s += [
        pipe([(530, f0 - 20), (530, top - 30), (600, top - 30)], 8),
        flow([(530, f0 - 20), (530, top - 30), (600, top - 30)], "water", p, 16, gap=16),
    ]
    s += [flow(pipe_pts, "water", p, 30, gap=18)]
    s += [flow([(x0 + 45 + i * 128, f1 - 120), (x0 + 45 + i * 128, top - 6)], "energy", p, 6, gap=12) for i in range(4)]
    s += [lightmask(inner, 0.7)]
    s += [pylon(1400, BASE, 190), battery(1330, BASE - 120, 34, 110, 0.75, 5)]
    s += [cable([(1343, BASE - 160 + 3), (1300, BASE - 120), (1280, BASE - 60)], 2)]
    return "".join(s), dict(racks=(x0 + 200, f1 - 60), roof=(820, top - 50), ctl=(x0 + 640, f0 - 60))


@scene(
    ["How does power reach", "a home?"],
    "Made far away, stepped down, then shared street by street.",
    [
        (L1, "farm", "The wind and sun farm", "Free fuel, uneven hours: the output rises and falls with the weather."),
        (R1, "line", "The high-voltage line", "High voltage loses less on the long run across the country."),
        (R2, "sub", "The substation", "Steps the voltage down and keeps a battery for the evening peak."),
    ],
    "Wind turbines and solar panels feed glowing power lines over pylons to a substation and a street of lit homes.",
    lit=(1180, 860, 360),
)
def power_grid(p):
    s = [ground(440, 1500)]
    s += [turbine(480 + i * 90, BASE, 210 - i * 20, p, 1) for i in range(3)]
    s += [solar_panel(470, BASE, 70), solar_panel(560, BASE, 70)]
    a, b = 820, 1020
    for x in (a, b):
        s.append(pylon(x, BASE, 230))
    ty = BASE - 230 * 0.86
    span1 = curve((700, BASE - 120), (a - 69, ty), 30)
    span2 = curve((a + 69, ty), (b - 69, ty), 40)
    span3 = curve((b + 69, ty), (1130, BASE - 150), 30)
    for sp in (span1, span2, span3):
        s += [
            path(P(sp, False), "none", f'stroke="{T.CABLE_DARK}" stroke-width="3"'),
            flow(sp, "energy", p, 12, gap=14),
        ]
    sub, sr, si = building(1120, 160, [150], "flat", tints=["ROOM_WARM"])
    X, F0, _, _ = sr[0]
    s += [
        sub,
        machine(X + 10, F0, 60, 80),
        battery(X + 86, F0 - 110, 36, 108, 0.6, 5),
        standing(X + 76, F0, -1, reach=(X + 60, F0 - 50)),
    ]
    s += [lightmask(si, 0.7)]
    s += [house(1310 + i * 64, BASE, 54, 44, lit=i != 1) for i in range(3)]
    s += [wire([(1266, BASE - 30), (1300, BASE - 30), (1300, BASE - 6), (1500, BASE - 6)], "energy", p, 16)]
    return "".join(s), dict(farm=(560, BASE - 200), line=(920, ty + 30), sub=(X + 60, F0 - 70))


@scene(
    ["What happens when you", "open a web page?"],
    "Your request crosses the network to a server, and the page comes back.",
    [
        (L1, "you", "You", "One click sends a short request: which page, in which language."),
        (R1, "net", "The exchange", "Routers pass the request on, hop by hop, in a few thousandths of a second."),
        (R2, "srv", "The server", "Finds the page, packs it up and sends it back the same way."),
    ],
    "A person at a lit desk at home, cables through an exchange building to a server hall, with information flowing both ways.",
    lit=(560, 860, 300),
)
def internet(p):
    s = [ground(440, 1500)]
    hm, hr, hi = building(460, 200, [130], "gable", tints=["ROOM_WARM"])
    X, F0, _, _ = hr[0]
    s += [hm, desk(X + 30, F0, 70), seated(X + 56, F0 - 14), screen(X + 70, F0 - 86, 50, 34, "bars", p)]
    s += [pendant_lamp(X + 70, F0 - 130, 26), cabinet(X + 130, F0)]
    s += [lightmask(hi, 0.7)]
    ex, er, _ = building(830, 200, [170], "flat", tints=["ROOM"])
    X2, F2, _, _ = er[0]
    s += [ex, server_rack(X2 + 14, F2, 46, 120, 7, p, 3), server_rack(X2 + 70, F2, 46, 120, 7, p, 4)]
    s += [standing(X2 + 140, F2, -1, reach=(X2 + 120, F2 - 50))]
    sv, sr, _ = building(1180, 300, [120, 120], "flat", tints=["ROOM_COOL", "ROOM_COOL"])
    (X3, F3, _, _), (X4, F4, _, _) = sr
    s += [sv] + [server_rack(X3 + 10 + i * 64, F3, 50, 100, 6, p, i) for i in range(4)]
    s += [server_rack(X4 + 10 + i * 64, F4, 50, 100, 6, p, i + 4) for i in range(4)]
    out = [(660, F0 - 40), (750, F0 - 40), (750, F2 - 130), (844, F2 - 130)]
    back = [(844, F2 - 100), (770, F2 - 100), (770, F0 - 20), (660, F0 - 20)]
    out2 = [(1030, F2 - 130), (1194, F2 - 130)]
    back2 = [(1194, F2 - 100), (1030, F2 - 100)]
    for pts in (out, out2):
        s += [wire(pts, "info", p, 14)]
    for pts in (back, back2):
        s += [cable(pts, 3), flow(pts, "energy", p, 14, gap=14)]
    return "".join(s), dict(you=(X + 56, F0 - 50), net=(X2 + 60, F2 - 140), srv=(X3 + 150, F3 - 60))


@scene(
    ["Who does what on", "a team?"],
    "Leads set direction, makers build, and support keeps it running.",
    [
        (L1, "lead", "The leads", "Decide what matters this month, and what can wait."),
        (L2, "make", "The makers", "Turn the plan into finished work, one piece at a time."),
        (R2, "help", "The support crew", "Tools, supplies and answers, so nobody waits."),
    ],
    "A three-storey cut-away office: leads at a board on top, makers at benches in the middle, support staff below.",
    lit=(960, 700, 380),
)
def org_team(p):
    s = [ground(560, 1360)]
    b, rr, inner = building(600, 720, [130, 130, 130], "saw", 6, ["ROOM", "ROOM_WARM", "ROOM_DEEP"])
    s += [b]
    (x0, f0, w0, _), (x1, f1, _, _), (x2, f2, _, _) = rr
    s += [wall(x0 + 600, f0 - 390 + 10, 380)]
    s += [stand(x2 + 30, f2, 110, 64, "line", p), standing(x2 + 160, f2, -1, reach=(x2 + 136, f2 - 76))]
    s += [desk(x2 + 220, f2, 80), seated(x2 + 250, f2 - 14), desk(x2 + 340, f2, 80), seated(x2 + 370, f2 - 14, -1)]
    s += [pendant_lamp(x2 + 260, f2 - 130, 28), pendant_lamp(x2 + 470, f2 - 130, 28), clock(x2 + 530, f2 - 90, 13, p)]
    s += [machine(x1 + 20, f1, 64, 74), standing(x1 + 100, f1, -1, reach=(x1 + 80, f1 - 40))]
    s += [
        desk(x1 + 160, f1, 80),
        seated(x1 + 190, f1 - 14),
        machine(x1 + 300, f1, 60, 66),
        standing(x1 + 380, f1, -1, reach=(x1 + 360, f1 - 36)),
    ]
    s += [
        desk(x1 + 430, f1, 80),
        seated(x1 + 460, f1 - 14),
        pendant_lamp(x1 + 200, f1 - 130, 28),
        pendant_lamp(x1 + 420, f1 - 130, 28),
    ]
    s += [cabinet(x0 + 20, f0), cabinet(x0 + 54, f0), shelf(x0 + 100, f0, 90, 100, 3, seed=4)]
    s += [
        standing(x0 + 230, f0, 1, carry=True),
        standing(x0 + 300, f0, -1),
        crate(x0 + 360, f0, 18),
        crate(x0 + 382, f0, 18),
    ]
    s += [ladder(x0 + 440, f0 - 120, f0), standing(x0 + 500, f0, -1, reach=(x0 + 470, f0 - 60))]
    lift = x0 + 640
    s += [rrect(lift - 20, f2 - 120, 40, 380, 0, T.IN800, 'opacity="0.6"'), ladder(lift - 8, f2 - 120, f0)]
    s += [flow([(lift - 26, f2 - 100), (lift - 26, f0 - 10)], "info", p, 20, gap=16)]
    s += [flow([(lift + 26, f0 - 10), (lift + 26, f2 - 100)], "energy", p, 20, gap=16)]
    s += [lightmask(inner, 0.75)]
    return "".join(s), dict(lead=(x2 + 90, f2 - 90), make=(x1 + 52, f1 - 60), help=(x0 + 460, f0 - 80))


@scene(
    ["Why do most visitors", "never buy?"],
    "Each step asks a little more, and only a few go all the way.",
    [
        (L1, "look", "The visitors", "Many arrive, look around and leave. That is normal."),
        (R1, "try", "The interested", "Fewer stay to read, compare and ask a question."),
        (R2, "buy", "The buyers", "A handful say yes. Small gains here count the most."),
    ],
    "A building of four floors that narrows downward like a funnel: crowds on top, one buyer carrying a lit parcel at the bottom.",
    centre=(960, 620),
    lit=(960, 900, 260),
)
def sales_funnel(p):
    s = [ground(820, 1100)]
    tiers = [(780, 120, 9), (560, 116, 6), (360, 112, 3), (190, 120, 1)]
    y = BASE
    boxes = []
    for w, h, _ in reversed(tiers):
        boxes.insert(0, (960 - w / 2, y - h, w, h))
        y -= h
    for i, ((x, top, w, h), (_, _, n)) in enumerate(zip(boxes, tiers)):
        s.append(shell(x, top, w, h, 0, 12, ["ROOM", "ROOM", "ROOM_WARM", "ROOM_WARM"][i]))
        fy = top + h - 12
        for k in range(n):
            fx = x + 40 + (w - 80) * (k + 0.5) / n
            if i == 3:
                s += [pendant_lamp(960, top + 12, 26, 60), standing(fx, fy, 1, carry=True)]
            elif i == 2:
                s += [desk(fx - 30, fy, 56), seated(fx - 6, fy - 14, 1 if k % 2 else -1)]
            else:
                s += [standing(fx, fy, 1 if (k + i) % 2 else -1, reach=(fx + 14, fy - 30) if k % 3 == 0 else None)]
        if i < 3:
            s += [screen(x + w - 90, top + 22, 54, 36, "bars", p)] if i == 0 else []
            s += [flow([(960, fy - 6), (960, fy + 30)], "energy", p, 4, gap=12)]
    x0, top0, w0, _ = boxes[0]
    s += [standing(x0 - 30, top0 + 108, -1), standing(x0 - 80, top0 + 108, -1), standing(x0 + w0 + 40, top0 + 108, 1)]
    s += [plinth(x0 - 110, top0 + 108, 110, 8), plinth(x0 + w0, top0 + 108, 110, 8)]
    s += [glow(960, BASE - 60, 220, 120, op=0.7)]
    return "".join(s), {
        "look": (x0 + 120, top0 + 60),
        "try": (boxes[1][0] + boxes[1][2] - 60, boxes[1][1] + 60),
        "buy": (960, BASE - 50),
    }


@scene(
    ["How does a lab turn", "questions into results?"],
    "Observe, test and write it down, then check it all again.",
    [
        (L1, "dome", "The observatory", "Every result starts as something someone noticed."),
        (L2, "bench", "The bench", "Tests change one thing at a time and keep the rest still."),
        (R2, "lib", "The library", "Results are written up, filed and read by the next team."),
    ],
    "A domed laboratory in cut-away: an orrery under the dome, benches and machines below, and a library on the ground floor.",
    centre=(960, 560),
    lit=(960, 400, 420),
)
def research_lab(p):
    s = [ground(560, 1360)]
    b, rr, inner = building(620, 680, [140, 140], tints=["ROOM_DEEP", "ROOM_COOL"])
    top = inner[1] - 14
    s += [dome(960, top, 330, 230, 5, 16, True, 160), b]
    s += [orrery(960, top - 70, 90, p), standing(840, top, 1, reach=(870, top - 60)), standing(1080, top, -1)]
    (x0, f0, _, _), (x1, f1, _, _) = rr
    s += [
        machine(x1 + 20, f1, 64, 76),
        desk(x1 + 120, f1, 80),
        seated(x1 + 150, f1 - 14),
        screen(x1 + 210, f1 - 104, 60, 40, "line", p),
    ]
    s += [
        machine(x1 + 330, f1, 56, 64),
        standing(x1 + 410, f1, -1, reach=(x1 + 380, f1 - 40)),
        desk(x1 + 460, f1, 80),
        seated(x1 + 490, f1 - 14, -1),
    ]
    s += [pendant_lamp(x1 + 160, f1 - 140, 30), pendant_lamp(x1 + 470, f1 - 140, 30)]
    s += [shelf(x0 + 14 + i * 84, f0, 76, 110, 4, "books", seed=i, lit=0.08) for i in range(3)]
    s += [
        ladder(x0 + 260, f0 - 110, f0),
        desk(x0 + 330, f0, 90),
        seated(x0 + 362, f0 - 14),
        stand(x0 + 460, f0, 120, 70, "bars", p),
    ]
    s += [standing(x0 + 600, f0, -1, reach=(x0 + 570, f0 - 80))]
    s += [
        flow([(960, top - 20), (960, f1 - 110)], "info", p, 10, gap=16),
        flow([(x1 + 520, f1 - 40), (x1 + 520, f0 - 20), (x0 + 420, f0 - 20)], "info", p, 14, gap=16),
    ]
    s += [lightmask(inner, 0.7)]
    return "".join(s), dict(dome=(900, top - 120), bench=(x1 + 52, f1 - 60), lib=(x0 + 520, f0 - 90))


@scene(
    ["How does a model learn", "from examples?"],
    "It guesses, measures the miss and adjusts, millions of times.",
    [
        (L1, "data", "The examples", "Labelled cases, each one a question with its answer."),
        (R1, "core", "The model", "Guesses an answer and compares it with the right one."),
        (R2, "loss", "The score", "The miss shrinks with each pass until it stops improving."),
    ],
    "Shelves of examples ride a conveyor into a hall of servers around a glowing core, with a falling error line on a screen.",
    centre=(1000, 600),
    lit=(1000, 700, 400),
)
def model_training(p):
    s = [ground(440, 1500)]
    wh, wr, _ = building(460, 220, [210], "gable", tints=["ROOM_DEEP"])
    X, F0, _, _ = wr[0]
    s += [wh, shelf(X + 10, F0, 80, 150, 5, seed=11, lit=0.3), shelf(X + 96, F0, 80, 150, 5, seed=12, lit=0.3)]
    hall, hr, hi = building(740, 520, [300], "flat", tints=["ROOM_COOL"])
    X2, F2, W2, _ = hr[0]
    s += [hall, conveyor(680, F0 - 20, 140)] + [crate(690 + i * 34 + 34 * (p * 4 % 1), F0 - 20, 14) for i in range(3)]
    s += [server_rack(X2 + 14 + i * 58, F2, 48, 124, 7, p, i) for i in range(2)]
    s += [server_rack(X2 + W2 - 62 - i * 58, F2, 48, 124, 7, p, i + 5) for i in range(2)]
    s += [
        thinking_core(1000, F2 - 150, 70, p),
        standing(930, F2, 1, reach=(948, F2 - 90)),
        standing(1070, F2, -1, reach=(1052, F2 - 90)),
    ]
    s += [lightmask(hi, 0.65)]
    s += [stand(1300, BASE, 150, 96, "line", p), standing(1480, BASE, -1, reach=(1456, BASE - 100))]
    loop = [(1375, BASE - 140), (1375, F2 - 330), (1000, F2 - 330), (1000, F2 - 224)]
    s += [cable(loop, 2), flow(loop, "info", p, 30, gap=16)]
    return "".join(s), dict(data=(X + 90, F0 - 100), core=(1040, F2 - 180), loss=(1375, BASE - 180))


@scene(
    ["How does clean water", "reach a tap?"],
    "Rain fills the reservoir; it is cleaned, stored high, then piped home.",
    [
        (L1, "res", "The reservoir", "Rain and rivers fill it. The level is watched every hour."),
        (R1, "tower", "The water tower", "Height is pressure: the tower pushes water uphill to every tap."),
        (R2, "plant", "The treatment plant", "Settles, filters and disinfects, then tests what leaves."),
    ],
    "Rain falls on a reservoir; water flows through a treatment plant, up a water tower and down to houses.",
    lit=(900, 860, 320),
)
def water_supply(p):
    s = [ground(440, 1500)]
    s += [cloud(560, 520, 1.0, p, rain=True, bolt=False)]
    s += [
        rrect(462, BASE - 64, 200, 64, 2, T.B600, f'stroke="{T.IN900}" stroke-width="1.5" opacity="0.85"'),
        rrect(450, BASE - 80, 12, 80, 2, T.IN700, f'stroke="{T.IN900}" stroke-width="1.5"'),
        path(
            P([(662, BASE - 80), (690, BASE - 80), (706, BASE), (662, BASE)]),
            "url(#metalh)",
            f'stroke="{T.IN900}" stroke-width="2"',
        ),
    ]
    s += [
        line(
            (480 + i * 44, BASE - 50 + 14 * (i % 2)),
            (510 + i * 44, BASE - 50 + 14 * (i % 2)),
            T.B200,
            1.6,
            'opacity="0.7"',
        )
        for i in range(4)
    ]
    pl, pr, pi = building(760, 300, [170], "flat", tints=["ROOM_COOL"])
    X, F0, _, _ = pr[0]
    s += [pl, tank(X + 14, F0, 70, 110, 0.8), tank(X + 100, F0, 70, 110, 0.5), machine(X + 190, F0, 60, 70)]
    s += [standing(X + 266, F0, -1, reach=(X + 240, F0 - 50)), pendant_lamp(X + 140, F0 - 170, 30)]
    s += [lightmask(pi, 0.7)]
    tx = 1180
    s += [
        line((tx + 8, BASE), (tx + 18, BASE - 220), T.L200, 3),
        line((tx + 72, BASE), (tx + 62, BASE - 220), T.L200, 3),
    ]
    s += [
        line((tx + 12, BASE - 70), (tx + 68, BASE - 150), T.L200, 1.4),
        line((tx + 68, BASE - 70), (tx + 12, BASE - 150), T.L200, 1.4),
    ]
    s += [tank(tx, BASE - 220, 80, 100, 0.65), ladder(tx + 34, BASE - 220, BASE)]
    s += [house(1300, BASE, 70, 50), house(1400, BASE, 70, 50, lit=False)]
    w = lambda pts: pipe(pts, 7) + flow(pts, "water", p, 20, gap=16)
    s += [
        w([(706, BASE - 20), (774, BASE - 20)]),
        w([(1046, BASE - 30), (1120, BASE - 30), (1120, BASE - 300), (1200, BASE - 300), (1200, BASE - 320)]),
    ]
    s += [w([(1240, BASE - 230), (1240, BASE - 260), (1290, BASE - 260), (1290, BASE - 10), (1480, BASE - 10)])]
    return "".join(s), dict(res=(560, BASE - 40), tower=(tx + 40, BASE - 280), plant=(X + 100, F0 - 80))


@scene(
    ["What keeps a hospital", "running at night?"],
    "Wards rest while the lab, the desk and the ambulance bay stay awake.",
    [
        (L1, "ward", "The ward", "Quiet, but never unwatched: a nurse walks the beds every hour."),
        (L2, "lab", "The lab", "Samples arrive all night; results go back within the hour."),
        (R2, "bay", "The ambulance bay", "The doors that never close, with a team ready inside."),
    ],
    "A three-storey hospital in cut-away: a ward of beds on top, a lab in the middle, an ambulance bay and front desk below.",
    lit=(1000, 760, 380),
)
def hospital(p):
    s = [ground(500, 1460)]
    b, rr, inner = building(560, 760, [140, 130, 130], "flat", tints=["ROOM", "ROOM_COOL", "ROOM_WARM"])
    (x0, f0, w0, _), (x1, f1, _, _), (x2, f2, _, _) = rr
    s += [b]
    s += [bed(x2 + 30 + i * 120, f2, 84) for i in range(4)] + [standing(x2 + 520, f2, -1, reach=(x2 + 496, f2 - 34))]
    s += [
        pendant_lamp(x2 + 140, f2 - 130, 26),
        pendant_lamp(x2 + 380, f2 - 130, 26),
        screen(x2 + 600, f2 - 100, 56, 38, "line", p),
    ]
    s += [
        machine(x1 + 30, f1, 60, 70),
        desk(x1 + 130, f1, 80),
        seated(x1 + 160, f1 - 14),
        screen(x1 + 210, f1 - 100, 56, 38, "bars", p),
    ]
    s += [
        machine(x1 + 320, f1, 56, 64),
        standing(x1 + 400, f1, -1, reach=(x1 + 376, f1 - 40)),
        cabinet(x1 + 460, f1),
        cabinet(x1 + 494, f1),
    ]
    s += [pendant_lamp(x1 + 200, f1 - 120, 28), clock(x1 + 600, f1 - 80, 13, p)]
    s += [wall(x0 + 360, f0 - 130, 130), desk(x0 + 40, f0, 120), seated(x0 + 80, f0 - 14), standing(x0 + 190, f0, -1)]
    s += [
        truck(x0 + 520, f0, 1.0, -1),
        standing(x0 + 420, f0, 1, reach=(x0 + 446, f0 - 30)),
        standing(x0 + 640, f0, -1, carry=True),
    ]
    s += [pendant_lamp(x0 + 520, f0 - 130, 30, 70)]
    s += [lightmask(inner, 0.7)]
    return "".join(s), dict(ward=(x2 + 72, f2 - 30), lab=(x1 + 60, f1 - 50), bay=(x0 + 520, f0 - 60))


@scene(
    ["What makes a school", "work?"],
    "Teachers, books and time together, every single day.",
    [
        (L1, "class", "The classroom", "One teacher, thirty questions, and a board that keeps up."),
        (R1, "lib", "The library", "A quiet room where the reading happens."),
        (R2, "yard", "The yard", "Where half the learning happens, at break."),
    ],
    "A school in cut-away: a classroom of pupils facing a teacher, a library upstairs, and a yard with trees outside.",
    lit=(860, 840, 360),
)
def school(p):
    s = [ground(440, 1500)]
    b, rr, inner = building(500, 700, [150, 130], "saw", 7, ["ROOM_WARM", "ROOM_DEEP"])
    (x0, f0, w0, _), (x1, f1, _, _) = rr
    s += [b, stand(x0 + 20, f0, 120, 70, "bars", p), standing(x0 + 170, f0, -1, reach=(x0 + 140, f0 - 90))]
    for row in range(2):
        for k in range(4):
            dx = x0 + 230 + k * 100 + row * 40
            s += [desk(dx, f0, 56), seated(dx + 18, f0 - 14, -1)]
    s += [pendant_lamp(x0 + 300, f0 - 150, 30), pendant_lamp(x0 + 520, f0 - 150, 30), clock(x0 + 640, f0 - 110, 13, p)]
    s += [shelf(x1 + 14 + i * 90, f1, 82, 110, 4, "books", seed=20 + i, lit=0.08) for i in range(4)]
    s += [
        desk(x1 + 400, f1, 90),
        seated(x1 + 430, f1 - 14),
        seated(x1 + 470, f1 - 14, -1),
        ladder(x1 + 520, f1 - 110, f1),
    ]
    s += [standing(x1 + 600, f1, -1, reach=(x1 + 570, f1 - 70)), pendant_lamp(x1 + 440, f1 - 130, 28)]
    s += [lightmask(inner, 0.7)]
    s += [
        tree(1260, BASE, 1.2, 3),
        tree(1430, BASE, 1.0, 4),
        standing(1320, BASE, 1),
        standing(1356, BASE, -1, reach=(1340, BASE - 30)),
    ]
    s += [standing(1480, BASE, -1), string_lights((1220, BASE - 150), (1440, BASE - 150), 30, 6, p)]
    return "".join(s), {"class": (x0 + 90, f0 - 90), "lib": (x1 + 180, f1 - 70), "yard": (1340, BASE - 60)}


@scene(
    ["Where does your", "deposit go?"],
    "Most is lent to homes and firms; a little stays in the vault.",
    [
        (L1, "dep", "The saver", "Pays in, and can take it out again tomorrow."),
        (R2, "loan", "The borrowers", "A home and a workshop, paying it back over years."),
        (R1, "vault", "The vault", "Only a slice is kept here, enough for a normal week."),
    ],
    "A cut-away bank: money flows in from a saver's house, out to a home and a workshop, and a small reserve in the vault.",
    lit=(960, 780, 360),
)
def bank(p):
    s = [ground(440, 1500)]
    s += [house(470, BASE, 90, 60), standing(600, BASE, 1, carry=True)]
    b, rr, inner = building(720, 480, [140, 150], "gable", tints=["ROOM_DEEP", "ROOM_WARM"])
    (x0, f0, w0, _), (x1, f1, _, _) = rr
    s += [b, arcade(x1 + 10, f1, w0 - 20, 8, 100, lit=False)]
    s += [desk(x1 + 60, f1, 90), seated(x1 + 90, f1 - 14, -1), desk(x1 + 260, f1, 90), seated(x1 + 290, f1 - 14, -1)]
    s += [standing(x1 + 30, f1, 1, reach=(x1 + 56, f1 - 30)), standing(x1 + 230, f1, 1, reach=(x1 + 256, f1 - 30))]
    s += [pendant_lamp(x1 + 110, f1 - 150, 30), pendant_lamp(x1 + 310, f1 - 150, 30)]
    s += [battery(x0 + 40, f0 - 120, 50, 116, 0.25, 6), cabinet(x0 + 120, f0), cabinet(x0 + 154, f0)]
    s += [crate(x0 + 200, f0, 18), crate(x0 + 222, f0, 18), standing(x0 + 300, f0, -1, reach=(x0 + 270, f0 - 30))]
    s += [lightmask(inner, 0.7)]
    s += [house(1290, BASE, 80, 56)]
    wk, wkr, _ = building(1380, 120, [90], "saw", 2, tints=["ROOM_WARM"])
    X, F0, _, _ = wkr[0]
    s += [wk, machine(X + 10, F0, 40, 50), standing(X + 70, F0, -1, reach=(X + 50, F0 - 30))]
    s += [flow([(560, BASE - 20), (734, BASE - 20)], "energy", p, 12, gap=12)]
    s += [flow([(1186, f1 - 40), (1250, f1 - 40), (1250, BASE - 30), (1290, BASE - 30)], "energy", p, 16, gap=12)]
    s += [flow([(1186, f1 - 70), (1440, f1 - 70), (1440, F0 - 130)], "energy", p, 18, gap=12)]
    return "".join(s), dict(dep=(520, BASE - 50), loan=(1330, BASE - 70), vault=(x0 + 64, f0 - 60))


@scene(
    ["How does a support", "ticket get solved?"],
    "Logged at the front, answered by an agent, escalated only when needed.",
    [
        (L1, "in", "The customers", "Write in when something breaks, mostly at nine and at two."),
        (R2, "desk", "The front line", "Answers most tickets on the first reply."),
        (R1, "eng", "The engineers", "Take the few hard ones, and fix the cause, not the case."),
    ],
    "An office in cut-away: tickets ride a conveyor to agents at desks, and a few climb to engineers at server racks upstairs.",
    lit=(1000, 860, 380),
)
def support_desk(p):
    s = [ground(440, 1500)]
    s += [house(470, BASE, 80, 56), house(470, BASE - 150, 80, 56, lit=False), plinth(460, BASE - 150, 100, 10)]
    b, rr, inner = building(660, 760, [150, 150], "flat", tints=["ROOM_WARM", "ROOM_COOL"])
    (x0, f0, w0, _), (x1, f1, _, _) = rr
    s += [b, conveyor(x0 + 10, f0 - 30, 160)] + [
        crate(x0 + 20 + i * 40 + 40 * (p * 6 % 1), f0 - 30, 14) for i in range(3)
    ]
    for k in range(4):
        dx = x0 + 220 + k * 110
        s += [
            desk(dx, f0, 70),
            seated(dx + 24, f0 - 14),
            screen(dx + 10, f0 - 96, 46, 30, "bars" if k % 2 else "line", p),
        ]
    s += [pendant_lamp(x0 + 300, f0 - 150, 28), pendant_lamp(x0 + 520, f0 - 150, 28), clock(x0 + 680, f0 - 110, 13, p)]
    s += [ladder(x0 + 690, f0 - 150, f0)]
    s += [server_rack(x1 + 20 + i * 62, f1, 50, 116, 7, p, i) for i in range(3)]
    s += [standing(x1 + 220, f1, -1, reach=(x1 + 190, f1 - 60)), desk(x1 + 300, f1, 80), seated(x1 + 330, f1 - 14)]
    s += [desk(x1 + 440, f1, 80), seated(x1 + 470, f1 - 14, -1), pendant_lamp(x1 + 400, f1 - 140, 28)]
    s += [lightmask(inner, 0.7)]
    s += [
        flow([(560, BASE - 30), (674, BASE - 30)], "info", p, 10, gap=14),
        flow([(560, BASE - 180), (620, BASE - 180), (620, BASE - 40)], "info", p, 12, gap=14),
    ]
    s += [flow([(x0 + 676, f0 - 20), (x0 + 676, f1 - 60)], "info", p, 10, gap=14)]
    return "".join(s), {"in": (510, BASE - 50), "desk": (x0 + 250, f0 - 60), "eng": (x1 + 110, f1 - 80)}


@scene(
    ["How does a story", "reach print?"],
    "Reported, edited, printed and delivered before breakfast.",
    [
        (L1, "wire", "The reporters", "Bring the facts in by phone, wire and notebook."),
        (R1, "ed", "The newsroom", "Editors check every name and number twice."),
        (R2, "press", "The press hall", "Thousands of copies an hour, bundled for the vans."),
    ],
    "A newspaper building in cut-away: a dish brings stories to editors upstairs, a press prints below, and a van drives off.",
    lit=(940, 700, 380),
)
def newsroom(p):
    s = [ground(440, 1500)]
    s += [dish(520, BASE, 1.1, 1), standing(600, BASE, 1, reach=(620, BASE - 30))]
    b, rr, inner = building(680, 560, [150, 140], "saw", 5, ["ROOM", "ROOM_WARM"])
    (x0, f0, w0, _), (x1, f1, _, _) = rr
    s += [b]
    for k in range(4):
        dx = x1 + 20 + k * 126
        s += [
            desk(dx, f1, 74),
            seated(dx + 26, f1 - 14, 1 if k % 2 else -1),
            screen(dx + 14, f1 - 100, 46, 30, "line" if k % 2 else "bars", p),
        ]
    s += [pendant_lamp(x1 + 130, f1 - 140, 28), pendant_lamp(x1 + 380, f1 - 140, 28), clock(x1 + 500, f1 - 110, 13, p)]
    s += [machine(x0 + 20, f0, 80, 100), machine(x0 + 110, f0, 80, 100), conveyor(x0 + 200, f0 - 30, 200)]
    s += [crate(x0 + 220 + i * 50 + 50 * (p * 4 % 1), f0 - 30, 16) for i in range(3)]
    s += [standing(x0 + 440, f0, -1, carry=True), standing(x0 + 490, f0, -1, reach=(x0 + 470, f0 - 40))]
    s += [lightmask(inner, 0.7)]
    s += [road(1260, BASE - 14, 240), truck(1380, BASE - 14, 0.9)]
    s += [sight((560, BASE - 140), (x1 + 40, f1 - 80), 0.25)]
    s += [
        flow([(x1 + 520, f1 - 20), (x1 + 520, f0 - 60)], "info", p, 10, gap=14),
        flow([(1226, BASE - 30), (1320, BASE - 30)], "energy", p, 8, gap=12),
    ]
    return "".join(s), dict(wire=(560, BASE - 100), ed=(x1 + 300, f1 - 70), press=(x0 + 150, f0 - 70))


@scene(
    ["What sits behind a", "shop shelf?"],
    "A stock room, a loading dock and a count at closing time.",
    [
        (L1, "shop", "The shop floor", "Full shelves, short queues, and the bestsellers at eye level."),
        (R1, "office", "The office", "Counts what sold today and orders tomorrow's stock."),
        (R2, "dock", "The loading dock", "Deliveries arrive before opening, while the aisles are empty."),
    ],
    "A shop in cut-away: customers at shelves in front, a stock room behind, an office upstairs and a van at the loading dock.",
    lit=(800, 860, 360),
)
def retail_store(p):
    s = [ground(440, 1500)]
    b, rr, inner = building(500, 760, [160, 120], "flat", tints=["ROOM_WARM", "ROOM"])
    (x0, f0, w0, _), (x1, f1, _, _) = rr
    s += [b, wall(x0 + 440, f0 - 160, 160)]
    s += [shelf(x0 + 20 + i * 100, f0, 80, 110, 4, seed=30 + i, lit=0.2) for i in range(3)]
    s += [
        standing(x0 + 330, f0, -1, reach=(x0 + 290, f0 - 60)),
        standing(x0 + 360, f0, 1, carry=True),
        desk(x0 + 380, f0, 50),
    ]
    s += [pendant_lamp(x0 + 140, f0 - 160, 30), pendant_lamp(x0 + 340, f0 - 160, 30)]
    s += [shelf(x0 + 460 + i * 84, f0, 76, 130, 5, seed=40 + i, lit=0.1) for i in range(2)]
    s += [standing(x0 + 650, f0, -1, carry=True), crate(x0 + 680, f0, 18), crate(x0 + 700, f0, 18)]
    s += [
        desk(x1 + 160, f1, 90),
        seated(x1 + 190, f1 - 14),
        screen(x1 + 260, f1 - 96, 70, 44, "bars", p),
        cabinet(x1 + 30, f1),
        cabinet(x1 + 64, f1),
    ]
    s += [clock(x1 + 400, f1 - 70, 13, p), pendant_lamp(x1 + 230, f1 - 120, 26)]
    s += [lightmask(inner, 0.7)]
    s += [road(1280, BASE - 14, 220), truck(1350, BASE - 14, 0.9, -1), standing(1450, BASE - 14, -1, carry=True)]
    s += [flow([(1290, BASE - 30), (1250, BASE - 30)], "energy", p, 4, gap=12)]
    return "".join(s), dict(shop=(x0 + 120, f0 - 70), office=(x1 + 300, f1 - 70), dock=(1350, BASE - 70))


@scene(
    ["How does food get from", "field to plate?"],
    "Grown, packed, driven and cooked, often within a week.",
    [
        (L1, "farm", "The orchard", "Picked by hand when ripe, a few rows each day."),
        (R1, "pack", "The packing barn", "Sorted by size, boxed and chilled before noon."),
        (R2, "kitchen", "The kitchen", "Cooked tonight for people who will never see the field."),
    ],
    "An orchard, a packing barn, a van on the road and a lit restaurant kitchen with diners at a table.",
    lit=(1330, 860, 300),
)
def farm_to_table(p):
    s = [ground(440, 1500)]
    s += [tree(490 + i * 70, BASE, 1.15, i + 5) for i in range(3)] + [standing(680, BASE, -1, carry=True)]
    bn, br, _ = building(720, 260, [170], "gable", tints=["ROOM_COOL"])
    X, F0, _, _ = br[0]
    s += [bn, conveyor(X + 10, F0 - 30, 140)] + [crate(X + 20 + i * 36, F0 - 30, 16) for i in range(4)]
    s += [standing(X + 170, F0, -1, reach=(X + 150, F0 - 40)), crate(X + 190, F0, 18), crate(X + 190, F0 - 18, 18)]
    s += [pendant_lamp(X + 110, F0 - 170, 34)]
    s += [road(1000, BASE - 14, 240), truck(1110, BASE - 14, 0.9)]
    rs, rr, ri = building(1250, 240, [150], "gable", tints=["ROOM_WARM"])
    X2, F2, _, _ = rr[0]
    s += [rs, machine(X2 + 10, F2, 56, 60), standing(X2 + 80, F2, -1, reach=(X2 + 60, F2 - 40))]
    s += [
        desk(X2 + 110, F2, 80),
        seated(X2 + 104, F2 - 14, 1),
        seated(X2 + 196, F2 - 14, -1),
        pendant_lamp(X2 + 150, F2 - 150, 30, 60),
    ]
    s += [lightmask(ri, 0.7)]
    s += [
        flow([(680, BASE - 30), (734, BASE - 30)], "energy", p, 6, gap=12),
        flow([(966, BASE - 30), (1040, BASE - 30)], "energy", p, 6, gap=12),
    ]
    s += [flow([(1180, BASE - 30), (1264, BASE - 30)], "energy", p, 6, gap=12)]
    return "".join(s), dict(farm=(540, BASE - 110), pack=(X + 80, F0 - 80), kitchen=(X2 + 150, F2 - 50))


@scene(
    ["How does a knowledge base", "answer a question?"],
    "Everything is filed once, so anyone can find it fast.",
    [
        (L1, "shelves", "The stacks", "Each answer lives in one place, with a clear name."),
        (R1, "light", "The index", "A single light over the catalogue: where everything is."),
        (R2, "reader", "The reader", "Asks once, and is pointed straight to the right shelf."),
    ],
    "A domed reading room in cut-away: shelves on curved galleries, a shaft of light from the oculus onto a reader's desk.",
    centre=(960, 560),
    lit=(960, 600, 460),
    focus=(420, 190, 1500, 990),
)
def knowledge_base(p):
    s = [ground(540, 1380)]
    s += [dome(960, 520, 420, 300, 6, 18, True, 420)]
    s += [rrect(560, 520, 800, BASE - 520, 0, T.ROOM_DEEP, f'stroke="{T.IN900}" stroke-width="2.5"')]
    for k, yy in enumerate((680, 830)):
        s += [shelf(580 + i * 98, yy - 10, 88, 130, 4, "books", seed=k * 9 + i, lit=0.06) for i in range(8)]
        s += [gallery_ring(960, yy - 10, 400, 22, 10, 30)]
    s += [shelf(580 + i * 98, BASE, 88, 110, 3, "books", seed=50 + i, lit=0.06) for i in (0, 1, 6, 7)]
    s += [
        ladder(770, 680 - 10, 830 - 10),
        standing(800, 820, 1, reach=(820, 760)),
        standing(1150, 670, -1, reach=(1130, 600)),
    ]
    s += [
        desk(910, BASE, 100),
        seated(940, BASE - 14),
        seated(990, BASE - 14, -1),
        lantern(960, 600, 0.5, p, glow_r=2.4),
    ]
    s += [line((960, 520 - 290), (960, 600), T.IN900, 1.6)]
    s += [flow([(1200, 820), (1060, 870), (1000, BASE - 40)], "info", p, 12, gap=14)]
    s += [lightmask((560, 520, 800, BASE - 520), 0.7)]
    return "".join(s), dict(shelves=(640, 760), light=(960, 640), reader=(970, BASE - 40))


@scene(
    ["How is a network", "defended?"],
    "Watch every gate, check every visitor, and keep the vault apart.",
    [
        (L1, "tower", "The watchtower", "Sees every door at once and logs who comes and goes."),
        (R1, "storm", "The attack", "Most never reach the wall; the gate stops the rest."),
        (R2, "gate", "The gate", "Every visitor shows a pass, every time, even the familiar ones."),
    ],
    "A walled compound at night: a lit watchtower with sight lines over a server building, a guarded gate and a storm outside.",
    lit=(700, 640, 380),
)
def network_defence(p):
    s = [ground(440, 1500)]
    s += [rrect(500, BASE - 44, 716, 44, 2, T.IN700, f'stroke="{T.IN900}" stroke-width="1.6"')]
    s += [lantern_tower(640, BASE, 90, 3, 110)]
    b, rr, inner = building(800, 360, [130, 120], "flat", tints=["ROOM_COOL", "ROOM_DEEP"])
    (x0, f0, _, _), (x1, f1, _, _) = rr
    s += [b] + [server_rack(x1 + 14 + i * 60, f1, 48, 100, 6, p, i) for i in range(5)]
    s += [
        battery(x0 + 20, f0 - 110, 44, 104, 0.8, 5),
        cabinet(x0 + 90, f0),
        desk(x0 + 150, f0, 80),
        seated(x0 + 180, f0 - 14),
        screen(x0 + 220, f0 - 96, 54, 36, "line", p),
    ]
    s += [lightmask(inner, 0.6)]
    for x in (500, 1200):
        s += [rrect(x, BASE - 90, 16, 90, 2, T.IN700, f'stroke="{T.IN900}" stroke-width="1.6"')]
    s += [rrect(1216, BASE - 70, 60, 8, 2, T.L200), standing(1240, BASE, 1, reach=(1262, BASE - 30))]
    s += [standing(1330, BASE, -1), standing(1380, BASE, -1), standing(1430, BASE, -1, carry=True)]
    s += [cloud(1380, 470, 0.9, p, rain=True, bolt=True, seed=3)]
    s += [sight((660, BASE - 300), (1250, BASE - 60), 0.22), sight((620, BASE - 300), (1330, 560), 0.18)]
    return "".join(s), dict(tower=(640, BASE - 200), storm=(1380, 470), gate=(1240, BASE - 50))


@scene(
    ["What is the cloud,", "really?"],
    "Someone else's computers, rented by the minute.",
    [
        (L1, "users", "You and your apps", "Save a photo or run a report, and it travels up."),
        (R1, "cloud", "The cloud", "A friendly name for a long, plain building far away."),
        (R2, "dc", "The data centre", "Racks of shared machines, cooled, powered and guarded."),
    ],
    "A big soft cloud with a beam of light dropping from it into a cut-away building full of server racks, linked to homes and offices.",
    centre=(960, 560),
    lit=(1000, 800, 380),
    focus=(420, 190, 1500, 990),
)
def cloud_computing(p):
    s = [ground(440, 1500)]
    s += [cloud(1000, 400, 2.2, p, rain=False, bolt=False, seed=6)]
    s += [tractor_beam(1000, 470, 300, 160, 420, p)]
    b, rr, inner = building(780, 440, [110, 110], "flat", tints=["ROOM_COOL", "ROOM_COOL"])
    (x0, f0, _, _), (x1, f1, _, _) = rr
    s += [b] + [server_rack(x0 + 12 + i * 58, f0, 46, 96, 6, p, i) for i in range(7)]
    s += [server_rack(x1 + 12 + i * 58, f1, 46, 96, 6, p, i + 7) for i in range(7)]
    s += [standing(x1 + 200, f1, 1, reach=(x1 + 226, f1 - 50))]
    s += [lightmask(inner, 0.6)]
    s += [
        house(470, BASE, 80, 56),
        house(580, BASE, 80, 56, lit=False),
        house(1300, BASE, 80, 56),
        house(1410, BASE, 80, 56),
    ]
    s += [flow(curve((520, BASE - 90), (880, 430), -120), "info", p, 20, gap=16)]
    s += [flow(curve((1120, 430), (1450, BASE - 90), -120), "info", p, 20, gap=16)]
    return "".join(s), dict(users=(520, BASE - 50), cloud=(1100, 360), dc=(x0 + 300, f0 - 60))


@scene(
    ["How does a team stay", "in step from home?"],
    "Shared tools carry the work, and a short daily call carries the rest.",
    [
        (L1, "home", "The home desks", "Four rooms, four time zones, one shared plan."),
        (R1, "hub", "The shared hub", "Files, chat and the plan live here, not in anyone's inbox."),
        (R2, "call", "The daily call", "Fifteen minutes: done, next, and anything in the way."),
    ],
    "Four small lit homes, each with a person at a desk, linked by flowing lines to a central hub on a hill.",
    lit=(960, 680, 300),
)
def remote_team(p):
    s = [ground(440, 1500)]
    spots = [(470, BASE), (660, BASE - 200), (1140, BASE - 200), (1330, BASE)]
    for i, (hx, hy) in enumerate(spots):
        if hy != BASE:
            s.append(plinth(hx - 20, hy, 220, 10))
        hb, hr, hi = building(hx, 180, [100], "gable", tints=["ROOM_WARM"], base=hy)
        X, F0, _, _ = hr[0]
        s += [
            hb,
            desk(X + 30, F0, 60),
            seated(X + 54, F0 - 14, 1 if i < 2 else -1),
            screen(X + 92, F0 - 80, 46, 30, "line", p),
        ]
        s += [pendant_lamp(X + 60, F0 - 100, 20), clock(X + 20, F0 - 70, 9, p)]
    hub, hr, hi = building(880, 160, [120], "flat", tints=["ROOM_COOL"])
    X, F0, _, _ = hr[0]
    s += [
        hub,
        server_rack(X + 10, F0, 46, 96, 6, p, 2),
        server_rack(X + 66, F0, 46, 96, 6, p, 3),
        lantern(960, 640, 0.5, p, glow_r=3.0),
    ]
    s += [line((960, 560), (960, 640), T.IN900, 1.6)]
    for hx, hy in spots:
        a = (hx + 90, hy - 80)
        pts = curve(a, (960, F0 - 60), -40)
        s += [flow(pts, "info", p, 14, gap=16)]
    return "".join(s), dict(home=(560, BASE - 60), hub=(960, F0 - 60), call=(960, 700))


@scene(
    ["Where does a bottle go", "after the bin?"],
    "Collected, sorted, melted and made again: a loop, not a line.",
    [
        (L1, "home", "The kitchen bin", "The loop starts with one rinse and the right lid."),
        (R1, "sort", "The sorting plant", "Belts, magnets and sharp eyes split glass, metal and plastic."),
        (R2, "make", "The factory", "Melts the sorted stuff and makes the next bottle."),
    ],
    "A loop of glowing dots: a house, a van, a sorting plant, a factory and a shop, then back to the house.",
    lit=(900, 860, 340),
)
def recycling(p):
    s = [ground(440, 1500)]
    s += [house(470, BASE, 90, 60), truck(640, BASE, 0.85, 1)]
    pl, pr, pi = building(740, 320, [160], "flat", tints=["ROOM_COOL"])
    X, F0, _, _ = pr[0]
    s += [pl, conveyor(X + 10, F0 - 40, 260)] + [
        crate(X + 20 + i * 44 + 44 * (p * 6 % 1), F0 - 40, 14) for i in range(5)
    ]
    s += [
        standing(X + 60, F0 - 54, 1, reach=(X + 80, F0 - 70)),
        standing(X + 180, F0 - 54, -1, reach=(X + 160, F0 - 70)),
        machine(X + 220, F0 - 54, 50, 60),
    ]
    s += [pendant_lamp(X + 140, F0 - 160, 30)]
    s += [lightmask(pi, 0.7)]
    fc, fr, _ = building(1100, 200, [130], "saw", 3, ["ROOM_WARM"])
    X2, F2, _, _ = fr[0]
    s += [
        fc,
        machine(X2 + 20, F2, 60, 70),
        standing(X2 + 100, F2, -1, reach=(X2 + 80, F2 - 40)),
        crate(X2 + 130, F2, 18),
    ]
    s += [house(1340, BASE, 80, 60), shelf(1440, BASE, 50, 70, 3, seed=9, lit=0.4)]
    loop = (
        [(520, BASE - 30), (1460, BASE - 30), (1490, BASE - 120)]
        + curve((1490, BASE - 120), (470, BASE - 120), -260)[1:]
        + [(520, BASE - 30)]
    )
    s += [flow(loop, "energy", p, 60, gap=16)]
    return "".join(s), dict(home=(510, BASE - 50), sort=(X + 140, F0 - 80), make=(X2 + 60, F2 - 60))


@scene(
    ["How does a small team", "become a company?"],
    "One room, then one floor, then a building, each lit by the last.",
    [
        (L1, "garage", "The garage", "Two people, one idea and a borrowed lamp."),
        (R1, "chart", "The team", "Headcount by year: slow, slow, then all at once."),
        (R2, "tower", "The company", "Four floors, and the same lamp hanging in the lobby."),
    ],
    "A garage with two people, a small office and a four-storey building in a row, growing left to right under a bar chart.",
    lit=(560, 860, 320),
)
def startup_growth(p):
    s = [ground(440, 1500)]
    g, gr, gi = building(470, 180, [110], "gable", tints=["ROOM_WARM"])
    X, F0, _, _ = gr[0]
    s += [
        g,
        desk(X + 20, F0, 70),
        seated(X + 44, F0 - 14),
        standing(X + 120, F0, -1, reach=(X + 100, F0 - 30)),
        pendant_lamp(X + 76, F0 - 110, 24, 60),
    ]
    s += [lightmask(gi, 0.6)]
    o, orr, _ = building(780, 220, [110, 110], "flat")
    (X1, F1, _, _), (X2, F2, _, _) = orr
    s += [o] + [desk(X1 + 20 + i * 64, F1, 50) + seated(X1 + 40 + i * 64, F1 - 14) for i in range(3)]
    s += [desk(X2 + 20 + i * 64, F2, 50) + seated(X2 + 40 + i * 64, F2 - 14, -1) for i in range(3)]
    tw, tr, _ = building(1150, 300, [100, 100, 100, 100], "flat", tints=["ROOM_WARM", "ROOM", "ROOM", "ROOM"])
    s.append(tw)
    for k, (Xk, Fk, _, _) in enumerate(tr):
        s += [
            desk(Xk + 20 + i * 60, Fk, 46) + seated(Xk + 38 + i * 60, Fk - 14, 1 if i % 2 else -1)
            for i in range(4 if k else 2)
        ]
    s += [pendant_lamp(tr[0][0] + 200, tr[0][1] - 100, 20, 50), standing(tr[0][0] + 160, tr[0][1], 1)]
    s += [bars(820, 470, 300, 120, [2, 9, 60], ["Year 1", "Year 3", "Year 6"], highlight=2)]
    s += [
        flow([(660, BASE - 30), (790, BASE - 30)], "energy", p, 10, gap=14),
        flow([(1010, BASE - 30), (1160, BASE - 30)], "energy", p, 10, gap=14),
    ]
    return "".join(s), dict(garage=(X + 60, F0 - 60), chart=(1010, 420), tower=(1300, tr[3][1] - 60))


@scene(
    ["How does mission control", "talk to a ship?"],
    "A dish sends the signal; the ship answers minutes later.",
    [
        (L1, "room", "The control room", "Rows of consoles, one big screen, nobody talking over anyone."),
        (R1, "ship", "The ship", "Hears the call late and answers later still: light takes time."),
        (R2, "dish", "The dish", "Aims at one point in the sky and listens for a whisper."),
    ],
    "A mission control room of consoles facing a big screen, a dish outside, and a dotted signal arcing up to a ship.",
    lit=(820, 820, 380),
    focus=(420, 190, 1500, 990),
)
def mission_control(p):
    s = [ground(440, 1500)]
    b, rr, inner = building(500, 600, [180], "flat", tints=["ROOM_DEEP"])
    X, F0, W, _ = rr[0]
    s += [b, rrect(X + 20, F0 - 170, 220, 110, 6, T.IN900, f'stroke="{T.L200}" stroke-width="1.4"')]
    s += [screen(X + 30, F0 - 160, 96, 90, "line", p), screen(X + 134, F0 - 160, 96, 90, "bars", p)]
    for k in range(4):
        s += [desk(X + 270 + k * 74, F0, 56), seated(X + 300 + k * 74, F0 - 14, -1)]
    s += [
        standing(X + 250, F0, -1, reach=(X + 226, F0 - 70)),
        pendant_lamp(X + 380, F0 - 180, 30),
        clock(X + 520, F0 - 140, 14, p),
    ]
    s += [lightmask(inner, 0.7)]
    s += [dish(1200, BASE, 1.6, 1), standing(1290, BASE, -1)]
    hull, cav = saucer(1380, 380, 120, 34)
    s += [hull, standing(1360, 380, 1, alien=True), standing(1400, 380, -1, alien=True)]
    s += [sight((1270, BASE - 172), (1360, 440), 0.25)]
    s += [
        cable([(1100, BASE - 30), (1176, BASE - 30)], 3),
        flow([(1100, BASE - 30), (1176, BASE - 30)], "info", p, 8, gap=14),
    ]
    return "".join(s), dict(room=(X + 130, F0 - 110), ship=(1380, 360), dish=(1250, BASE - 120))


# =====================================================================================================
# compose
# =====================================================================================================
def build(name, t=0.0, annotate=True, words=None):
    """One scene as a finished SVG. words may override 'title' (list of lines), 'answer' and 'labels'."""
    sc = dict(SCENES[name], **(words or {}))
    set_canvas("16:9")
    p = (t % C.LOOP) / C.LOOP
    art, anchors = sc["draw"](p)
    zt = zoomer(sc["zoom"])
    z = sc["zoom"]  # the art is drawn at a 1920 frame and enlarged about the middle of the ground line
    art = f'<g transform="translate({f2(960 * (1 - z))},{f2(ZY * (1 - z))}) scale({z})">{art}</g>'
    body = [background(*zt(sc["centre"]), p=p, avoid=TEXT), art, finish()]
    if annotate:
        body.append(title_block(sc["title"], None, sc["answer"], y=96))
        for (x, y), key, title, txt in sc["labels"]:
            side = "left" if x < 960 else "right"
            body.append(callout(x, y, title, wrap(txt, 30 if side == "left" else 34), zt(anchors[key]), side))
        body.append(credit("Illustrative scene. Places, people and numbers stylised."))
    lx, ly, lr = sc["lit"]
    return svg_doc(std_defs(*zt(sc["centre"]), lit=(lx, ly), lit_r=lr), "".join(body), alt=sc["alt"])


def art(name, t=0.0):
    """The drawing alone (with its ground), for social cards and slide backgrounds."""
    return build(name, t, annotate=False)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        for n, sc in SCENES.items():
            print(f"{n:16} {' '.join(sc['title'])}")
        sys.exit()
    names = list(SCENES) if args[0] == "all" else [a for a in args if a in SCENES]
    if not names:
        sys.exit(f"unknown scene; choose from: {', '.join(SCENES)}")
    variant = ([a for a in args if a in ("dark", "light")] or [None])[0]
    tset = ([a for a in args if a in SYS["type_sets"]] or [None])[0]
    color = ([a for a in args if a in colors()] or [None])[0]
    set_theme(variant or "dark", color, tset)
    os.makedirs("out/scenes", exist_ok=True)
    for n in names:
        print(render(build(n, annotate="clean" not in args), f"out/scenes/{n}_{T.color}_{T.variant}.png", scale=1))
