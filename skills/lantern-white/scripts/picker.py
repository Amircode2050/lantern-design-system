"""picker: render the two-step chooser shown to the user before a design starts.

    python picker.py              step 1, the overview: every installed colour with its 50-950 ramp -> ../assets/picker.jpg
    python picker.py red          step 2 for one colour: dark and light, the seven type sets, its shade options
                                  -> ../assets/picker/red.jpg
    python picker.py --all        both steps for every colour

Gradient ids in an SVG are global, so each tile is rendered on its own and the PNGs are composed. Re-run after adding a theme.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *
from kit import T, C, F, ROOT, SYS
from components import *
from new_theme import STEPS, ramp

TW, TH = 640, 360
BG = "#101014"


def _scene(x0=330, y0=150):
    return [
        sawtooth_roof(x0, y0, 250, 3),
        shell(x0, y0, 250, 150),
        slab(x0 + 14, y0 + 86, 222, 8),
        pendant_lamp(x0 + 70, y0 + 14, 18, 44),
        arched_window(x0 + 170, y0 + 86, 20, 52, lit=True),
        arched_window(x0 + 198, y0 + 86, 20, 52),
        standing(x0 + 50, y0 + 86, 1, reach=(x0 + 74, y0 + 60)),
        standing(x0 + 120, y0 + 86, -1, carry=True),
        machine(x0 + 20, y0 + 136, 44, 40),
        battery(x0 + 210, y0 + 98, 18, 38, 0.75, 4),
        flow([(x0 + 72, y0 + 112), (x0 + 200, y0 + 112)], "energy", gap=11, r=1.8),
        flow([(x0 + 72, y0 + 126), (x0 + 200, y0 + 126)], "info", gap=11, r=1.8),
    ]


def _ramp_strip(x, y, w, h, core):
    r = ramp(core)
    sw = w / 11
    s = ""
    for i, st in enumerate(STEPS):
        c = r[f"CORE_{st}"]
        s += rrect(x + i * sw, y, sw - 2, h, 2, c, f'stroke="{T.T2}" stroke-width="{2 if c == core.lower() else 0}"')
    return s


def overview_tile():
    shade = next((s["name"] for s in T.tok.get("shades", []) if s["core"] == T.CORE.lower()), T.name)
    b = (
        [background(410, 200, seed=5, avoid=[(0, 0, 320, 360)])]
        + _scene()
        + [
            finish(),
            text(32, 76, T.name, 46, T.T1, F.DISPLAY),
            text(34, 106, f"{shade} {T.CORE}", 15, T.T2, F.MONO),
            text(34, 134, T.tok.get("accent_label", "amber light"), 16, T.W300, F.SANS, 'font-weight="500"'),
            text(
                34,
                162,
                f"{T.variant} · {SYS['type_sets'][T.tok.get('default_type', 'classic')]['label']}",
                13,
                T.T2,
                F.MONO,
            ),
            _ramp_strip(32, 312, 576, 26, T.CORE),
        ]
    )
    return svg_doc(std_defs(410, 200, lit=(400, 190), lit_r=220), "".join(b), alt=f"{T.name} overview")


def variant_tile():
    b = (
        [background(410, 200, seed=5, avoid=[(0, 0, 320, 360)])]
        + _scene()
        + [
            finish(),
            text(32, 76, T.name, 46, T.T1, F.DISPLAY),
            text(34, 106, f"{T.variant} variant", 16, T.W300, F.SANS, 'font-weight="500"'),
        ]
    )
    for i, k in enumerate(("G800", "V500", "L200", "L100", "W300", "B200", "CORE")):
        b.append(circ(44 + i * 34, 314, 12, getattr(T, k), f'stroke="{T.T2}" stroke-width="1" stroke-opacity="0.5"'))
    return svg_doc(std_defs(410, 200, lit=(400, 190), lit_r=220), "".join(b), alt=f"{T.name} {T.variant}")


def type_tile():
    d = SYS["type_sets"][F.set]
    b = [
        background(320, 180, stars=False),
        finish(),
        text(32, 54, f"Type set: {d['label']}", 15, T.W300, F.MONO),
        text(32, 120, "Who keeps", 50, T.T1, F.DISPLAY),
        text(32, 174, "the lights on?", 50, T.T1, F.DISPLAY),
        text(33, 214, "Fiat lux", 21, T.T2, F.DISPLAY, f'font-style="{F.SUB_STYLE}"'),
        text(33, 258, "Body text sets the pace: calm, plain, exact.", 17, T.T2, F.SANS),
        text(33, 292, f"{d['display']} + {d['sans']} + {d['mono']}", 13, T.T2, F.MONO),
        text(33, 316, d["mood"], 13, T.T2, F.SANS),
    ]
    return svg_doc(std_defs(320, 180), "".join(b), alt=f"Type set {d['label']}")


def shades_tile(height):
    shades = T.tok.get("shades") or [{"name": T.name, "core": T.CORE}]
    b = [
        f'<rect width="{C.W}" height="{C.H}" fill="{T.G950}"/>',
        text(32, 50, "Shade options (each builds its own theme on request)", 16, T.T2, F.SANS),
    ]
    for i, s in enumerate(shades):
        y = 84 + i * 56
        cur = s["core"] == T.CORE.lower()
        b += [
            text(32, y + 24, s["name"] + ("  (current)" if cur else ""), 18, T.T1 if cur else T.T2, F.DISPLAY),
            text(330, y + 24, s["core"], 14, T.T2, F.MONO),
            _ramp_strip(440, y, 800, 34, s["core"]),
        ]
    return svg_doc("", "".join(b), alt=f"{T.name} shade options")


def _render(svg, tmp, name):
    from PIL import Image

    return Image.open(render(svg, os.path.join(tmp, name + ".png"), scale=1)).convert("RGB")


def overview(out):
    from PIL import Image

    cols = colors()
    tmp = tempfile.mkdtemp()
    per = 4
    tw, th = TW // 2 * 1, TH // 2 * 1
    rows = (len(cols) + per - 1) // per
    sheet = Image.new("RGB", (tw * per, th * rows), BG)
    set_canvas(TW, TH)
    for i, color in enumerate(cols):
        t = load_theme(color)
        set_theme(t.get("default_variant", "dark"), color)
        sheet.paste(
            _render(overview_tile(), tmp, color).resize((tw, th), Image.LANCZOS), ((i % per) * tw, (i // per) * th)
        )
    sheet.save(out, quality=88)
    return out


def detail(color, out):
    from PIL import Image

    tmp = tempfile.mkdtemp()
    set_canvas(TW, TH)
    sets = list(SYS["type_sets"])
    shades = load_theme(color).get("shades") or [1]
    sh_h = 100 + 56 * len(shades)
    per = 4  # type sets in rows of four, each tile keeping the 16:9 shape
    tw, th = TW * 2 // per, TH * 2 // per
    type_h = th * ((len(sets) + per - 1) // per)
    sheet = Image.new("RGB", (TW * 2, TH + type_h + sh_h), BG)
    for c, variant in enumerate(("dark", "light")):
        set_theme(variant, color)
        sheet.paste(_render(variant_tile(), tmp, variant), (c * TW, 0))
    for i, s in enumerate(sets):
        set_theme("dark", color, s)
        sheet.paste(
            _render(type_tile(), tmp, s).resize((tw, th), Image.LANCZOS), ((i % per) * tw, TH + (i // per) * th)
        )
    set_theme("dark", color)
    set_canvas(TW * 2, sh_h)
    sheet.paste(_render(shades_tile(sh_h), tmp, "shades"), (0, TH + type_h))
    set_canvas(TW, TH)
    sheet.save(out, quality=88)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    d = ROOT / "assets" / "picker"
    d.mkdir(parents=True, exist_ok=True)
    if not a or a == ["--all"]:
        print(overview(str(ROOT / "assets" / "picker.jpg")))
    for color in colors() if a == ["--all"] else [x for x in a if x != "--all"]:
        print(detail(color, str(d / f"{color}.jpg")))
