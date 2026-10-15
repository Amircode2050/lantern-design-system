"""examples: reference scenes (factory, portrait, break slide, component sheet) that double as the kit's self-check.

python examples.py                        every scene, colour and variant into ./out/<colour>/
python examples.py factory light blue     one scene, one variant, one colour
python examples.py portrait modern        any type set name selects that set
python examples.py loop                   short animation test (frames, GIF, seam check)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *
from kit import T, C, F
from components import *


def factory(t=0.0, annotate=True):
    """Cut-away mode. Scene sentence: a big firm and a small supplier under the same storm; the light is the lit workshop."""
    set_canvas("16:9")
    p = (t % C.LOOP) / C.LOOP
    body = [background(960, 560, p=p, avoid=[(60, 40, 720, 240), (1500, 250, 1900, 460)])]
    G = [cloud(700, 350, 1.0, p), plinth(390, 1000, 600), sawtooth_roof(430, 596, 470, 5), shell(430, 596, 470, 404)]
    G += [
        room(444, 610, 150, 190, "ROOM_COOL"),
        room(594, 610, 150, 190, "ROOM"),
        room(744, 610, 142, 190, "ROOM_WARM"),
        room(444, 810, 442, 176, "ROOM_DEEP"),
    ]
    G += [wall(594, 610, 190), wall(744, 610, 190), slab(444, 800, 442), truss(444, 812, 442)]
    G += [pendant_lamp(520, 610, 34), pendant_lamp(670, 610, 34), pendant_lamp(815, 610, 34), clock(640, 690, 13, p)]
    G += [arched_window(770, 800, 24, 74, lit=True), arched_window(808, 800, 24, 74), arched_window(846, 800, 24, 74)]
    G += [
        desk(456, 800, 58),
        cabinet(532, 800),
        machine(668, 800, 62, 76),
        standing(620, 800, 1, reach=(644, 772)),
        seated(480, 786, 1),
    ]
    for i, wx in enumerate((470, 540, 610, 680, 750, 820)):
        G.append(arched_window(wx, 968, 28, 96, lit=i in (1, 4)))
    G += [
        conveyor(456, 968, 418),
        car(540, 968, 0.72),
        car(700, 968, 0.72),
        standing(620, 968, -1, carry=True),
        standing(800, 968, 1, reach=(778, 944)),
    ]
    G += [
        battery(918, 760, 48, 226, level=1.0),
        cable([(886, 770), (942, 770), (942, 752)], 3),
        flow([(886, 770), (942, 770), (942, 752)], "energy", p, 8, gap=12, r=1.9),
    ]
    G += [
        cloud(1420, 610, 0.8, p, seed=8),
        plinth(1010, 1000, 560),
        gable(1056, 912, 140),
        shell(1056, 912, 140, 88),
        pendant_lamp(1126, 926, 14, 60),
    ]
    G += [
        car(1120, 986, 0.42),
        standing(1082, 986, 1, reach=(1100, 966)),
        standing(1172, 986, -1),
        battery(1022, 946, 22, 54, level=0.25, cells=4),
    ]
    G += [
        conveyor(1206, 980, 96, 9),
        crate(1216, 980, 14),
        crate(1250, 980, 14),
        crate(1280, 980, 14),
        string_lights((1196, 934), (1310, 900), 30, 3, p),
    ]
    G += [
        sawtooth_roof(1310, 786, 244, 3),
        shell(1310, 786, 244, 214),
        slab(1430, 900, 110),
        ladder(1438, 900, 986),
        machine(1470, 900, 54, 66),
        standing(1452, 900, 1, reach=(1470, 876)),
    ]
    G += [
        arched_window(1334, 930, 22, 80),
        arched_window(1366, 930, 22, 80, lit=True),
        arched_window(1398, 930, 22, 80),
        pendant_lamp(1376, 800, 22),
        machine(1380, 986, 60, 50),
        standing(1356, 986, 1),
        standing(1500, 986, -1, carry=True),
    ]
    body.append("".join(G))
    body.append(
        '<rect x="444" y="610" width="442" height="376" fill="url(#litmask)" style="mix-blend-mode:multiply" opacity="0.8"/>'
    )
    body.append(finish())
    if annotate:
        body.append(
            title_block(["Build it or buy it?"], "Ex officina", "Big firms build in-house; small firms buy in.")
        )
        body.append(
            callout(
                72,
                448,
                "The factory",
                wrap("One part is small beside the whole firm, so a single storm barely slows it.", 38),
                (480, 584),
                "left",
                ("Role", "maker"),
            )
        )
        body.append(
            callout(
                72,
                728,
                "The assembly hall",
                wrap("Built in-house by salaried staff and checked at every station.", 36),
                (640, 690),
                "left",
                ("Role", "in-house work"),
            )
        )
        body.append(
            callout(
                1548,
                300,
                "The workshop",
                wrap("Thin reserves: one bad month and the lights go out.", 38),
                (1126, 890),
                "right",
                ("Role", "small buyer"),
            )
        )
        body.append(
            callout(
                1612,
                800,
                "The supplier",
                wrap("Paid per part delivered, it carries the risk of the storm.", 34),
                (1496, 762),
                "right",
                ("Role", "outside work"),
            )
        )
        body.append(credit("Illustrative scene. Firms, storms and reserves stylised."))
    return svg_doc(
        std_defs(960, 560, lit=(670, 700), lit_r=420),
        "".join(body),
        alt="Cut-away of a large car factory beside a small workshop and its supplier, each under a storm cloud, with batteries showing their reserves.",
    )


def portrait(t=0.0):
    """Portrait mode. Scene sentence: a person and a machine face each other across a lit pane; the light is the orb behind the machine."""
    set_canvas("3:2")
    p = (t % C.LOOP) / C.LOOP
    body = [
        background(810, 500, p=p, stars=False),
        orb(1490, 400, 52),
        light_cone(1440, 400, 840, 170, 660, 30, 0.7),
        pane(640, 150, 200, 760),
    ]
    body += [bust_human(300, 760, 0.86, 1), bust_robot(1230, 740, 0.82, -1), finish()]
    return svg_doc(
        std_defs(810, 500),
        "".join(body),
        alt="A person in profile and a robot face each other across a glowing frosted pane lit by a single orb.",
    )


def saucer_break(t=0.0):
    """Break slide. Scene sentence: a ship thinks while the audience rests; the light is the thinking core under the dome."""
    set_canvas("16:9")
    p = (t % C.LOOP) / C.LOOP
    CX, CY = 690, 430
    hull, cavity = saucer(CX, CY, 500, 136)
    body = [background(CX, CY, p=p, avoid=[(1250, 280, 1800, 700)]), tractor_beam(CX, CY + 160, 420, 90, 400, p), hull]
    G = [
        path(cavity, T.ROOM),
        glow(CX - 250, CY - 50, 230, 80, "cool"),
        glow(CX + 210, CY + 56, 200, 70, "cool"),
        glow(CX, CY - 110, 260, 90, op=0.5),
        slab(CX - 480, CY - 5, 960, 9),
        server_rack(CX - 260, CY - 5, 46, 92, 6, p),
        server_rack(CX - 204, CY - 5, 46, 92, 6, p, seed=3),
    ]
    S = (CX + 110, CY - 62)
    A = place_next(S, 24, 16, -12)
    B = place_next(A, 16, 20, 24)
    for (Tn, c, th0, om), nh in zip(gear_chain([(24, S), (16, A), (20, B)], 0.0, TAU * (40 / 24) / C.LOOP), (6, 4, 5)):
        G.append(gear(c[0], c[1], Tn, th0 + om * t, nh=nh))
    pth = [(CX - 150, CY - 60), (CX - 20, CY - 60), (CX - 20, CY + 60), (CX - 190, CY + 60)]
    G += [
        cable(pth, 4),
        flow(pth, "energy", p, 50, gap=14),
        orrery(CX + 200, CY + 56, 56, p),
        flow([(CX - 204, CY - 110), (CX + 60, CY - 110)], "info", p, 30, gap=18),
    ]
    G += [
        standing(CX - 330, CY - 5, 1, reach=(CX - 300, CY - 40), alien=True),
        standing(CX + 330, CY - 5, -1, alien=True),
        standing(CX - 250, CY + 100, 1, alien=True),
        standing(CX + 60, CY + 100, 1, reach=(CX + 96, CY + 66), alien=True),
    ]
    body.append(
        f'<clipPath id="cav"><path d="{cavity}"/></clipPath><g clip-path="url(#cav)">'
        + "".join(G)
        + f'<path d="{cavity}" fill="url(#litmask)" style="mix-blend-mode:multiply" opacity="0.4"/></g>'
    )
    body += [
        thinking_core(CX, CY - 190, 44, p),
        standing(CX - 90, CY - 120, 1, reach=(CX - 60, CY - 150), alien=True),
        standing(CX + 90, CY - 120, -1, reach=(CX + 60, CY - 150), alien=True),
        screen(CX - 170, CY - 200, 54, 40, "bars", p),
        screen(CX + 116, CY - 200, 54, 40, "line", p),
    ]
    body += [finish(), break_slide("Break", "Back in 15 minutes", ["The ship is processing.", "So should you."])]
    return svg_doc(
        std_defs(CX, CY, lit=(CX, CY - 150), lit_r=560),
        "".join(body),
        alt="A flying saucer in cut-away with a crew at work around a glowing core, beside the word Break.",
    )


def sheet():
    """Component sheet: every library element once, labelled."""
    set_canvas("16:9")
    lab = lambda x, y, s: text(x, y, s, 14, T.T2, F.MONO)
    b = [
        background(stars=False),
        finish(),
        text(72, 84, f"{T.name} components", 44, T.T1, F.DISPLAY),
        text(74, 118, f"{T.variant} variant", 19, T.W300, F.SANS, 'font-weight="500"'),
    ]
    b += [
        sawtooth_roof(80, 250, 240, 3),
        shell(80, 250, 240, 150),
        slab(94, 330, 212),
        pendant_lamp(150, 264, 20),
        arched_window(240, 330, 22, 56, True),
        arched_window(270, 330, 22, 56),
        standing(120, 330),
        standing(170, 330, -1, hat="top"),
        seated(214, 316),
        lab(80, 424, "shell slab sawtooth_roof lamp window figures"),
    ]
    b += [
        cloud(450, 200, 0.8),
        lab(380, 300, "cloud"),
        battery(580, 170, 40, 120, 0.6, 6),
        lab(566, 314, "battery"),
        conveyor(660, 250, 150),
        crate(680, 250),
        crate(720, 250),
        car(880, 262, 0.6),
        lab(660, 300, "conveyor crate car"),
    ]
    b += [
        machine(1000, 280),
        server_rack(1090, 280),
        cabinet(1160, 280),
        desk(1200, 280),
        clock(1300, 200),
        ladder(1340, 170, 280),
        screen(1390, 180),
        screen(1390, 236, kind="line"),
        lab(1000, 304, "machine server_rack cabinet desk clock ladder screen"),
    ]
    b += [
        orrery(1560, 220, 60),
        thinking_core(1740, 220, 40),
        lab(1500, 304, "orrery"),
        lab(1680, 304, "thinking_core"),
    ]
    b += [
        dome(250, 620, 180, 130, shaft=150),
        arcade(80, 700, 340, 8, 60),
        gallery_ring(250, 760, 170, 26),
        lantern_tower(500, 980, 90, 3, 96),
        lab(80, 1010, "dome arcade gallery_ring lantern_tower"),
    ]
    hull, cav = saucer(860, 620, 210, 60)
    b += [
        tractor_beam(860, 690, 220, 50, 190),
        hull,
        standing(810, 620, 1, alien=True),
        standing(910, 620, -1, alien=True),
        lab(660, 1010, "saucer tractor_beam alien crew"),
    ]
    S = (1180, 560)
    A = place_next(S, 24, 16, -15)
    b += [gear(c[0], c[1], Tn, th) for Tn, c, th, _ in gear_chain([(24, S), (16, A)], 0, 1)]
    b += [
        pipe([(1120, 660), (1180, 660), (1180, 720), (1280, 720)]),
        flow([(1120, 760), (1300, 760)], "energy"),
        flow([(1120, 790), (1300, 790)], "info"),
        flow([(1120, 820), (1300, 820)], "water"),
        sight((1120, 900), (1300, 860)),
    ]
    b += [
        text(1316, 765, "energy", 14, T.T2, F.MONO),
        text(1316, 795, "info", 14, T.T2, F.MONO),
        text(1316, 825, "water", 14, T.T2, F.MONO),
        string_lights((1120, 930), (1300, 930), 24),
        lab(1120, 1010, "gear pipe flow sight string_lights"),
    ]
    b += [
        bust_human(1500, 800, 0.34),
        bust_robot(1740, 790, 0.34, -1),
        orb(1860, 560, 16),
        light_cone(1846, 560, 1620, 560, 760, 6, 0.6),
        lab(1420, 1010, "bust_human bust_robot orb light_cone"),
    ]
    b += [bars(1440, 480, 180, 70, [3, 5, 8, 4], ["Q1", "Q2", "Q3", "Q4"], highlight=2)]
    return svg_doc(std_defs(), "".join(b), alt=f"Reference sheet of the {T.name} component library.")


def loop_frame(t):
    return saucer_break(t)


SCENES = {"factory": factory, "portrait": portrait, "break": saucer_break, "sheet": sheet}

if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["loop"]:
        os.makedirs("out", exist_ok=True)
        set_theme("dark")
        set_canvas("16:9", loop=2.0)  # 2 s loop keeps the self-check quick
        n = render_frames(loop_frame, 10, "out/frames10", fresh=True)
        mb = make_gif("out/frames10", "out/loop.gif")
        seam, typical = check_loop("out/frames10")
        print(f"{n} frames, GIF {mb:.1f} MB, seam {seam:.2f} vs typical {typical:.2f}")
        assert seam < typical * 3 + 0.5, "loop seam jumps"
    else:
        names = [a for a in args if a in SCENES] or list(SCENES)
        tset = ([a for a in args if a in SYS["type_sets"]] or [None])[0]
        for color in [a for a in args if a in colors()] or colors():
            os.makedirs(f"out/{color}", exist_ok=True)
            for variant in [a for a in args if a in ("dark", "light")] or ["dark", "light"]:
                for nm in names:
                    set_theme(variant, color, tset)
                    print(render(SCENES[nm](), f"out/{color}/{nm}_{variant}.png", scale=1))
