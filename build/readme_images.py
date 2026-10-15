"""Images for the README and the colour guide. Run after build/build.py (it reuses the picker sheets).

    python build/readme_images.py            everything
    python build/readme_images.py --no-gif   skip the animation (the slowest part)

Writes into docs/images/: colors/<colour>.jpg, ramps/<colour>.png, type-sets.jpg, ui-dark.jpg, ui-light.jpg,
components-dark.jpg, components-light.jpg and loop.gif.
"""

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src" / "scripts"))
import examples  # noqa: E402
import export  # noqa: E402
import picker  # noqa: E402
from components import *  # noqa: E402,F403
from kit import C, F, T  # noqa: E402
from new_theme import STEPS  # noqa: E402

IMG = REPO / "docs" / "images"


def ramp_svg():
    """Eleven labelled swatches of the current theme's core ramp."""
    set_canvas(1320, 150)
    b = [f'<rect width="{C.W}" height="{C.H}" fill="{T.G950 if not T.light else T.G600}"/>']
    for i, s in enumerate(STEPS):
        c = getattr(T, f"CORE_{s}")
        x = 10 + i * 118
        ink = "#ffffff" if contrast("#ffffff", c) >= contrast("#111111", c) else "#111111"
        edge = f'stroke="{T.T1}" stroke-width="3"' if c == T.CORE.lower() else ""
        b += [
            rrect(x, 10, 110, 130, 8, c, edge),
            text(x + 12, 40, str(s), 20, ink, F.MONO),
            text(x + 12, 126, c.upper(), 15, ink, F.MONO),
        ]
    return svg_doc("", "".join(b), alt=f"{T.name} shade ramp")


def jpg(png, out, width=None, quality=85):
    from PIL import Image

    im = Image.open(png).convert("RGB")
    if width and im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(out, quality=quality)


def ui_shots(tmp):
    from playwright.sync_api import sync_playwright

    for variant, color in (("dark", "blue"), ("light", "white")):
        d = tmp / f"ui-{color}"
        export.export(color, str(d), default=variant)
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1200, "height": 900})
            pg.goto((d / "demo.html").resolve().as_uri())
            pg.evaluate("document.fonts.ready")
            pg.screenshot(path=str(tmp / f"ui-{variant}.png"), full_page=True)
            b.close()
        jpg(tmp / f"ui-{variant}.png", IMG / f"ui-{variant}.jpg", width=1000)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-gif", action="store_true")
    a = ap.parse_args()
    tmp = Path(tempfile.mkdtemp(prefix="lantern-readme-"))
    for d in ("colors", "ramps"):
        (IMG / d).mkdir(parents=True, exist_ok=True)

    for color in colors():
        shutil.copy(REPO / "src" / "assets" / "picker" / f"{color}.jpg", IMG / "colors" / f"{color}.jpg")
        set_theme("dark", color)
        render(ramp_svg(), str(IMG / "ramps" / f"{color}.png"), scale=1, grain=False)
    print("colour cards and ramps")

    from PIL import Image

    set_canvas(640, 360)
    sheet = Image.new("RGB", (1920, 360))
    for i, s in enumerate(["classic", "modern", "editorial"]):
        set_theme("dark", "blue", s)
        sheet.paste(
            Image.open(render(picker.type_tile(), str(tmp / f"type_{s}.png"), scale=1)).convert("RGB"), (i * 640, 0)
        )
    sheet.save(IMG / "type-sets.jpg", quality=86)
    print("type sets")

    for variant, color in (("dark", "blue"), ("light", "white")):
        set_theme(variant, color, None)
        jpg(
            render(examples.sheet(), str(tmp / f"sheet_{variant}.png"), scale=1),
            IMG / f"components-{variant}.jpg",
            width=1600,
        )
    print("component sheets")

    ui_shots(tmp)
    print("interface screenshots")

    if not a.no_gif:
        set_theme("dark", "gold", None)
        set_canvas("16:9", loop=6)
        render_frames(examples.loop_frame, 10, str(tmp / "frames"), fresh=True)
        mb = make_gif(str(tmp / "frames"), str(IMG / "loop.gif"), size=(720, 406), limit_mb=4)
        seam, typical = check_loop(str(tmp / "frames"))
        print(f"loop.gif {mb:.1f} MB, seam {seam:.2f} vs typical {typical:.2f}")


if __name__ == "__main__":
    main()
