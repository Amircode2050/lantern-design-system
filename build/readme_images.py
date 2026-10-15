"""Images for the README and the colour guide. Run after build/build.py (it reuses the picker sheets).

    python build/readme_images.py            everything
    python build/readme_images.py --no-gif   skip the animation (the slowest part)

Writes into docs/images/: colors/<colour>.jpg, ramps/<colour>.png, type-sets.jpg, ui-dark.jpg, ui-light.jpg,
components-dark.jpg, components-light.jpg, social/<format>.jpg and loop.gif. The scene library thumbnails come
from build/site.py.
"""

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src" / "scripts"))
import examples  # noqa: E402
import social  # noqa: E402
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


def languages_tile():
    """Companion tile for the type-set grid: the same words in the languages the font packs cover."""
    b = [background(320, 180, stars=False), finish(), text(32, 54, "Every set, many languages", 15, T.W300, F.MONO)]
    for i, w in enumerate(["Polski · Čeština · Türkçe", "Tiếng Việt · Ελληνικά", "Русский · Українська"]):
        b.append(text(32, 112 + i * 44, w, 30, T.T1, F.DISPLAY))
    b.append(text(32, 282, "فارسی · العربية · اردو", 30, T.T1, F.DISPLAY, right=320))
    b.append(text(33, 330, "core, sets, europe, cyrillic-greek and arabic font packs", 13, T.T2, F.SANS))
    return svg_doc(std_defs(320, 180), "".join(b), alt="The same type set in many languages")


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


def deck_preview(tmp):
    """Six slides of the Blue template, drawn from the .pptx itself: its background pictures and its text boxes,
    set in the bundled fonts (a slide tool would substitute fonts that are not installed)."""
    import base64

    import deck
    from PIL import Image
    from pptx import Presentation

    set_theme("dark", "blue", None)
    path = deck.build_deck(str(tmp / "blue.pptx"))
    prs = Presentation(path)
    px = lambda emu: emu / deck.EMU
    tiles = []
    for k in (0, 2, 3, 4, 5, 9):
        sl = prs.slides[k]
        set_canvas("16:9")
        b = []
        for sh in sl.shapes:
            if sh.shape_type == 13:  # picture
                data = base64.b64encode(sh.image.blob).decode()
                b.append(f'<image href="data:image/jpeg;base64,{data}" width="1920" height="1080"/>')
            elif sh.has_text_frame:
                y = px(sh.top)
                for para in sh.text_frame.paragraphs:
                    if not para.runs:
                        continue
                    r = para.runs[0]
                    size = r.font.size.pt * 2  # 1 pt = 2 px on the 1920 frame
                    fam = next(f["stack"] for n, f in SYS["fonts"].items() if n == r.font.name)
                    y += (para.space_before.pt * 2 if para.space_before else 0) + size * 0.95
                    for ln in wrap(para.text, max(8, int(px(sh.width) / (size * 0.5)))):
                        weight = 'font-weight="500"' if r.font.bold else ""
                        b.append(text(px(sh.left), y, ln, size, "#" + str(r.font.color.rgb), fam, weight))
                        y += size * 1.12
        png = render(svg_doc("", "".join(b), alt="slide"), str(tmp / f"slide{k}.png"), scale=1, grain=False)
        tiles.append(Image.open(png).convert("RGB").resize((640, 360), Image.LANCZOS))
    sheet = Image.new("RGB", (1940, 750), T.G950)
    for i, im in enumerate(tiles):
        sheet.paste(im, (10 + (i % 3) * 645, 10 + (i // 3) * 370))
    sheet.save(IMG / "deck.jpg", quality=86)


def playground_shots():
    """The playground page (docs/index.html, built by build/site.py) in Blue dark and Gold light, as on GitHub Pages."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 1500})
        pg.goto((REPO / "docs" / "index.html").resolve().as_uri())
        pg.wait_for_load_state("networkidle")
        for color, variant, name in (("blue", "dark", "playground-dark"), ("gold", "light", "playground-light")):
            pg.click(f"button.sw[data-c='{color}']")
            pg.click(f"#variant button[data-v='{variant}']")
            pg.wait_for_timeout(900)
            pg.screenshot(path=str(IMG / f"{name}.png"))
            jpg(IMG / f"{name}.png", IMG / f"{name}.jpg", width=1000)
            (IMG / f"{name}.png").unlink()
        b.close()


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
    sets = list(SYS["type_sets"])
    sheet = Image.new("RGB", (1920, 270 * ((len(sets) + 3) // 4)), "#0b0f1e")
    for i, s in enumerate(sets):
        set_theme("dark", "blue", s)
        tile = Image.open(render(picker.type_tile(), str(tmp / f"type_{s}.png"), scale=1)).convert("RGB")
        sheet.paste(tile.resize((480, 270), Image.LANCZOS), ((i % 4) * 480, (i // 4) * 270))
    if len(sets) % 4:  # the empty slot lists the languages every set can carry
        set_theme("dark", "blue", "classic")
        tile = Image.open(render(languages_tile(), str(tmp / "type_languages.png"), scale=1)).convert("RGB")
        sheet.paste(tile.resize((480, 270), Image.LANCZOS), ((len(sets) % 4) * 480, (len(sets) // 4) * 270))
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

    (IMG / "social").mkdir(exist_ok=True)
    for fmt, scene, color in (
        ("square", "cloud_computing", "blue"),
        ("portrait", "supply_chain", "teal"),
        ("story", "knowledge_base", "gold"),
    ):
        set_theme("dark", color, None)
        jpg(render(social.card(scene, fmt, 3.0), str(tmp / f"{fmt}.png"), scale=1), IMG / "social" / f"{fmt}.jpg", 720)
    print("social cards")

    deck_preview(tmp)
    print("slide template preview")

    playground_shots()
    print("playground screenshots")

    sheet = Image.new("RGB", (1920, 720))
    for i, (code, *_) in enumerate(examples.LANGUAGES):
        png = render(examples.language_slide(code), str(tmp / f"lang_{code}.png"), scale=1)
        sheet.paste(Image.open(png).convert("RGB").resize((640, 360), Image.LANCZOS), ((i % 3) * 640, (i // 3) * 360))
    sheet.save(IMG / "languages.jpg", quality=86)
    print("languages")

    if not a.no_gif:
        set_theme("dark", "gold", None)
        set_canvas("16:9", loop=6)
        render_frames(examples.loop_frame, 10, str(tmp / "frames"), fresh=True)
        mb = make_gif(str(tmp / "frames"), str(IMG / "loop.gif"), size=(720, 406), limit_mb=4)
        seam, typical = check_loop(str(tmp / "frames"))
        print(f"loop.gif {mb:.1f} MB, seam {seam:.2f} vs typical {typical:.2f}")


if __name__ == "__main__":
    main()
