"""Teaser images for the README and the launch, drawn with the engine itself.

    python build/teasers.py [out_dir]     default: docs/images/teasers

Writes hero.jpg (16:9), spectrum.jpg (16:9, all twelve colours), portrait.jpg (3:2), square.jpg (1:1), story.jpg (9:16)
and social-preview.jpg (1280x640, the repository's link preview).
"""

import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src" / "scripts"))
from components import *  # noqa: E402,F403
from kit import F, T  # noqa: E402

ORDER = ["black", "white", "blue", "purple", "green", "red", "gray", "teal", "gold", "orange", "cyan", "rose"]


def cores():
    return [load_theme(c)["core"] for c in ORDER]


def dots(x, y, gap=34, r=11):
    return "".join(
        circ(x + i * gap, y, r, c, f'stroke="{T.T2}" stroke-width="1" stroke-opacity="0.4"')
        for i, c in enumerate(cores())
    )


def hero():
    set_theme("dark", "black")
    set_canvas("16:9")
    b = [
        background(620, 470, seed=11, avoid=[(1100, 260, 1900, 820)]),
        line((620, 0), (620, 170), T.IN800, 3),
        lantern(620, 170, 2.3, glow_r=3.6),
        plinth(330, 960, 580),
        sawtooth_roof(380, 820, 220, 2),
        shell(380, 820, 220, 140),
        arched_window(420, 946, 22, 70, lit=True),
        arched_window(456, 946, 22, 70),
        pendant_lamp(520, 834, 16, 40),
        standing(560, 946, -1, reach=(540, 916)),
        standing(700, 960, -1, reach=(676, 920)),
        standing(760, 960, -1, carry=True),
        flow([(600, 950), (700, 950), (760, 950)], "energy", gap=12, r=2),
        finish(),
        text(1180, 470, "Lantern", ts("title-xl"), T.T1, F.DISPLAY),
        text(1186, 532, "One light. Twelve colours.", ts("answer"), T.W300, F.SANS, 'font-weight="500"'),
        text(1186, 590, "Illustrated slides, diagrams and loops,", ts("lead"), T.T2),
        text(1186, 622, "as skills for Claude Code and claude.ai.", ts("lead"), T.T2),
        dots(1196, 690),
    ]
    return svg_doc(
        std_defs(620, 470), "".join(b), alt="A glowing lantern above a small lit workshop, beside the word Lantern."
    )


def spectrum_tile(name):
    t = load_theme(name)
    set_theme(t.get("default_variant", "dark"), name)
    set_canvas(320, 540)
    b = [
        background(160, 230, seed=4, avoid=[(0, 390, 320, 540)]),
        line((160, 0), (160, 90), T.IN800, 2),
        lantern(160, 90, 1.0, glow_r=2.6),
        finish(),
        text(160, 452, t["name"], 40, T.T1, F.DISPLAY, 'text-anchor="middle"'),
        text(160, 486, t["core"].upper(), 15, T.T2, F.MONO, 'text-anchor="middle"'),
    ]
    return svg_doc(std_defs(160, 230), "".join(b), alt=f"{t['name']} lantern")


def portrait():
    set_theme("dark", "purple")
    set_canvas("3:2")
    b = [
        background(810, 520, stars=False),
        light_cone(508, 434, 1160, 300, 610, 18, 0.5),
        bust_human(300, 790, 0.82, 1),
        line((470, 250), (470, 330), T.IN900, 3),
        lantern(470, 330, 0.75, glow_r=3.4),
        bust_robot(1290, 770, 0.8, -1),
        finish(),
    ]
    return svg_doc(
        std_defs(810, 520), "".join(b), alt="A person in profile holds up a lantern whose beam reaches a robot."
    )


def square():
    set_theme("dark", "blue")
    set_canvas("1:1")
    b = [
        background(540, 420, seed=8, avoid=[(120, 700, 960, 1000)]),
        line((540, 0), (540, 120), T.IN800, 3),
        lantern(540, 120, 2.0, glow_r=3.4),
        finish(),
        text(540, 760, "Lantern", 120, T.T1, F.DISPLAY, 'text-anchor="middle"'),
        text(540, 822, "One light. Twelve colours.", 30, T.W300, F.SANS, 'text-anchor="middle" font-weight="500"'),
        dots(540 - 34 * 5.5, 900),
    ]
    return svg_doc(
        std_defs(540, 420), "".join(b), alt="A glowing lantern above the word Lantern and twelve colour dots."
    )


def story():
    set_theme("dark", "gold")
    set_canvas("9:16")
    b = [
        background(540, 760, seed=12, avoid=[(80, 1180, 1000, 1700)]),
        line((540, 0), (540, 360), T.IN800, 3),
        lantern(540, 360, 2.6, glow_r=3.4),
        finish(),
        text(540, 1340, "Lantern", 150, T.T1, F.DISPLAY, 'text-anchor="middle"'),
        text(540, 1414, "One light. Twelve colours.", 38, T.W300, F.SANS, 'text-anchor="middle" font-weight="500"'),
        text(540, 1480, "Illustrated slides, diagrams and loops.", 26, T.T2, F.SANS, 'text-anchor="middle"'),
        dots(540 - 34 * 5.5, 1580),
    ]
    return svg_doc(std_defs(540, 760), "".join(b), alt="A gold lantern above the word Lantern.")


def preview():
    """1280x640 social preview for the repository (Settings, General, Social preview) and the playground's og:image."""
    set_theme("dark", "black")
    set_canvas(1280, 640)
    b = [
        background(330, 300, seed=21, avoid=[(560, 120, 1260, 560)]),
        line((330, 0), (330, 120), T.IN800, 3),
        lantern(330, 120, 1.75, glow_r=3.4),
        finish(),
        text(600, 290, "Lantern", 104, T.T1, F.DISPLAY),
        text(604, 346, "One light. Twelve colours.", 30, T.W300, F.SANS, 'font-weight="500"'),
        text(604, 396, "Illustrated slides, scenes and templates,", 21, T.T2),
        text(604, 426, "as skills for Claude Code and other agents.", 21, T.T2),
        dots(612, 490, gap=32, r=10),
    ]
    return svg_doc(
        std_defs(330, 300), "".join(b), alt="A glowing lantern beside the word Lantern and twelve colour dots."
    )


def main(out):
    from PIL import Image

    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp())

    def save(svg, name, scale=1):
        png = render(svg, str(tmp / f"{name}.png"), scale=scale)
        Image.open(png).convert("RGB").save(out / f"{name}.jpg", quality=90)
        print(out / f"{name}.jpg")

    save(hero(), "hero")
    save(portrait(), "portrait")
    save(square(), "square")
    save(story(), "story")
    save(preview(), "social-preview")
    sheet = Image.new("RGB", (1920, 1080))
    for i, name in enumerate(ORDER):
        png = render(spectrum_tile(name), str(tmp / f"tile_{name}.png"), scale=1)
        sheet.paste(Image.open(png).convert("RGB"), ((i % 6) * 320, (i // 6) * 540))
    sheet.save(out / "spectrum.jpg", quality=90)
    print(out / "spectrum.jpg")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else REPO / "docs" / "images" / "teasers")
