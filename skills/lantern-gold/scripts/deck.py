"""deck: a ready PowerPoint template in any Lantern colour, every word editable. Opens in Keynote and Google Slides.

    python deck.py blue                         blue_dark.pptx in the colour's default variant and type set
    python deck.py teal light modern --out x.pptx
    python deck.py all                          every installed colour, both variants, into ./out/decks/
    python deck.py purple --lang fa             a Persian template, right to left (fonts: Vazirmatn)

Ten slides: title, agenda, section break, three illustrated explainers from the scene library, a text slide,
two columns, a native (editable) chart and a closing slide. The illustrations are images; titles, labels and
the chart are live. The theme colours and fonts are set in the file, so new shapes and charts match.
The fonts are free (Google Fonts): install the type set's two families for PowerPoint and Keynote; Google
Slides has them built in. Needs python-pptx (pip install python-pptx) besides the render requirements.
"""

import argparse
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scenes
from components import *
from kit import F, T

EMU = 6350  # one pixel of the 1920 frame
SCENE_SLIDES = ["supply_chain", "data_pipeline", "power_grid"]


def cover_art():
    """Title-slide drawing: the lantern hanging over a small lit workshop, with the right half kept for words."""
    set_canvas("16:9")
    b = [
        background(620, 470, seed=11, avoid=[(1100, 200, 1900, 900)]),
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
    ]
    return svg_doc(std_defs(620, 470), "".join(b), alt="A lantern hanging over a small lit workshop at night.")


def ground_art(lamp=False):
    """Plain ground for text slides; lamp=True hangs a small lantern at the left edge (section breaks)."""
    set_canvas("16:9")
    b = [background(960 if not lamp else 420, 540, seed=4, stars=lamp, avoid=[(700, 0, 1920, 1080)])]
    if lamp:
        b += [line((420, 0), (420, 300), T.IN800, 3), lantern(420, 300, 1.8, glow_r=3.4)]
    return svg_doc(std_defs(), "".join(b + [finish()]), alt="")


def _rgb(h):
    from pptx.dml.color import RGBColor

    return RGBColor.from_string(h.lstrip("#").upper())


def _theme_xml(blob, fonts, cs_font=None):
    """Point the file's colour scheme and fonts at the current Lantern theme (cs_font: the right-to-left font)."""
    from lxml import etree

    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    root = etree.fromstring(blob)
    scheme = {
        "dk1": T.G950 if not T.light else T.T1,
        "lt1": T.T1 if not T.light else T.G600,
        "dk2": T.G800 if not T.light else T.T2,
        "lt2": T.T2 if not T.light else T.G800,
        "accent1": T.CORE_FILL,
        "accent2": T.W300,
        "accent3": T.L100,
        "accent4": T.B200,
        "accent5": T.ROSE3,
        "accent6": T.T2,
        "hlink": T.W300,
        "folHlink": T.ROSE3,
    }
    cs = root.find(".//a:clrScheme", ns)
    cs.set("name", f"Lantern {T.name} {T.variant}")
    for k, v in scheme.items():
        el = cs.find(f"a:{k}", ns)
        for c in list(el):
            el.remove(c)
        etree.SubElement(el, f"{{{ns['a']}}}srgbClr", val=v.lstrip("#").upper())
    fs = root.find(".//a:fontScheme", ns)
    fs.set("name", f"Lantern {F.set}")
    for tag, fam in (("majorFont", fonts[0]), ("minorFont", fonts[1])):
        fs.find(f"a:{tag}/a:latin", ns).set("typeface", fam)
        if cs_font:
            fs.find(f"a:{tag}/a:cs", ns).set("typeface", cs_font)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


EN = {
    "kicker": "Quarterly review",
    "labels": {
        "agenda": "Agenda",
        "section": "Part 01",
        "scene": "Explainer",
        "text": "Context",
        "columns": "Options",
        "chart": "Results",
    },
    "options": ["Option A", "Option B"],
    "chart_note": "Revenue by quarter, in millions",
    "title": "Presentation title",
    "subtitle": "One line that says why it matters.",
    "byline": "Name, team, date",
    "agenda_title": "What we will cover",
    "agenda_answer": "Four parts, about ten minutes each.",
    "agenda": ["Where we are now", "What changed this year", "What we propose", "What we need from you"],
    "section": "Part one",
    "section_answer": "Where we are now",
    "text_title": "Why does this matter now?",
    "text_answer": "Because the cost of waiting has started to grow.",
    "text_points": [
        "Demand has doubled in two years, and our capacity has not.",
        "Each month of delay adds about four weeks to the backlog.",
        "A small change now avoids a large one next spring.",
    ],
    "columns_title": "Two ways forward",
    "columns_answer": "Both work; they differ in cost and in speed.",
    "columns": [
        ["Build it in-house", ["Full control of the result", "Slower to start", "Skills stay with us"]],
        ["Buy it in", ["Ready in weeks", "Less control over changes", "Running cost every year"]],
    ],
    "chart_title": "Where did the growth come from?",
    "chart_answer": "The third quarter carried the year.",
    "chart_categories": ["Q1", "Q2", "Q3", "Q4"],
    "chart_series": "Revenue",
    "closing": "Thank you",
    "closing_answer": "Questions are welcome.",
    "contact": "name@example.com",
    "notes": {
        "title": "Title slide. Replace the title and the line under it; keep one answer line.",
        "agenda": "Agenda. Three to five items, each a short phrase.",
        "section": "Section break. One or two words, then the answer line.",
        "scene": "Illustrated slide. Edit the question and answer; the picture is an image.",
        "text": "Text slide. One question as the title, three to five points.",
        "columns": "Two columns. Compare two options, or a before and an after.",
        "chart": "Chart. Edit the numbers with right-click, Edit Data. Highlight one bar only.",
        "closing": "Closing slide. Thank the room and leave one way to reach you.",
    },
}
RTL_FONT = "Vazirmatn"  # Arabic-script text in the file (Persian); free on Google Fonts, built into Google Slides
LANG_TAG = {"fa": "fa-IR", "es": "es-ES"}


def deck_words(lang=None):
    """The template's words in `lang` (English when None); a translation must include a "deck" section."""
    if lang in (None, "en"):
        return EN
    tr = scenes._translation(lang)
    if "deck" not in tr:
        raise ValueError(f"slide-template words are not translated into '{lang}' yet; scenes are")
    return {**EN, **tr["deck"]}


def digits(s, lang):
    """Persian digits for Persian text; other languages keep their digits."""
    return s.translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")) if lang == "fa" else s


def build_deck(out, words=None, lang=None):
    """Write the template for the current theme (set_theme first) to `out`, in English or `lang` ('fa' is set
    right to left: paragraphs marked right to left and aligned right, layouts mirrored, Vazirmatn for the text)."""
    from lxml import etree
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.enum.chart import XL_CHART_TYPE
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    from pptx.util import Emu, Pt

    from PIL import Image

    D = {**deck_words(lang), **(words or {})}
    rtl = is_rtl(D["title"] + D["agenda_title"])
    ts = SYS["type_sets"][F.set]
    disp, sans, mono = (RTL_FONT,) * 2 + (ts["mono"],) if rtl else (ts["display"], ts["sans"], ts["mono"])
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(1920 * EMU), Emu(1080 * EMU)
    theme = prs.slide_master.part.part_related_by(RT.THEME)
    theme._blob = _theme_xml(theme.blob, (disp, sans), RTL_FONT if rtl else None)
    blank = prs.slide_layouts[6]
    tmp = tempfile.mkdtemp(prefix="lantern-deck-")
    count = [0]
    A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

    def mx(x, w):
        """Mirror a box across the slide for right-to-left layouts."""
        return 1920 - x - w if rtl else x

    def picture(svg, crop=None):
        count[0] += 1
        png = render(svg, os.path.join(tmp, f"bg{count[0]}.png"), scale=1)
        jpg = png[:-4] + ".jpg"
        im = Image.open(png).convert("RGB")
        (im.crop(crop) if crop else im).save(jpg, quality=88)
        return jpg

    def slide(bg_svg, note=""):
        s = prs.slides.add_slide(blank)
        s.shapes.add_picture(picture(bg_svg), 0, 0, prs.slide_width, prs.slide_height)
        if note:
            s.notes_slide.notes_text_frame.text = note
        return s

    def style(para, r, size, color, font, bold=False, italic=False):
        r.font.size, r.font.name, r.font.bold, r.font.italic = Pt(size), font, bold, italic
        r.font.color.rgb = _rgb(color)
        if lang in LANG_TAG:
            r._r.get_or_add_rPr().set("lang", LANG_TAG[lang])
        if rtl:
            para.alignment = PP_ALIGN.RIGHT
            para._p.get_or_add_pPr().set("rtl", "1")
            etree.SubElement(r._r.get_or_add_rPr(), f"{A}cs").set("typeface", RTL_FONT)

    def box(s, x, y, w, h, lines, size, color, font, bold=False, italic=False, gap=1.15, mirror=True):
        bx = mx(x, w) if mirror else x
        tb = s.shapes.add_textbox(Emu(bx * EMU), Emu(y * EMU), Emu(w * EMU), Emu(h * EMU))
        tf = tb.text_frame
        tf.word_wrap = True
        for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
            setattr(tf, m, 0)
        for i, ln in enumerate([lines] if isinstance(lines, str) else lines):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.line_spacing = gap
            r = para.add_run()
            r.text = ln
            style(para, r, size, color, font, bold, italic)
        return tb

    def text_frame_add(tb, txt, size, color, font, before=0, bold=False):
        para = tb.text_frame.add_paragraph()
        para.space_before = Pt(before)
        r = para.add_run()
        r.text = txt
        style(para, r, size, color, font, bold)

    N = D["notes"]
    LB = D["labels"]
    total = 10
    hair = T.IN700 if not T.light else T.L300  # hairline rules: the chart's gridline colour

    def rule(s, x, y, w, h=2, color=None):
        r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(mx(x, w) * EMU), Emu(y * EMU), Emu(w * EMU), Emu(h * EMU))
        r.fill.solid()
        r.fill.fore_color.rgb = _rgb(color or hair)
        r.line.fill.background()
        return r

    def chrome(s, label, n):
        """Editorial frame: a mono label and a rule at the top, the deck title and page number at the foot."""
        box(s, 120, 66, 900, 30, label.upper(), 11, T.W300, mono)
        rule(s, 120, 112, 1680)
        rule(s, 120, 986, 1680)
        box(s, 120, 1006, 1000, 30, D["title"], 11, T.T3, mono)
        tb = box(s, 1500, 1006, 300, 30, digits(f"{n:02d} / {total:02d}", lang), 11, T.T3, mono)
        tb.text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT if rtl else PP_ALIGN.RIGHT

    def head(s, x, y, w, title, answer, tsize=44, asize=18):
        """Title and its answer line in one box, so a long title pushes the answer down instead of under it."""
        tb = box(s, x, y, w, 300, title, tsize, T.T1, disp, gap=1.02)
        text_frame_add(tb, answer, asize, T.W300, sans, tsize * 0.42, bold=True)
        return tb

    def numbered(s, x, y, w, items, size=22, step=118, sub=None):
        """A list with mono numbers and a hairline above each row (sub: a second, quieter line per row)."""
        for i, it in enumerate(items):
            yy = y + i * step
            rule(s, x, yy, w)
            box(
                s,
                x if not rtl else x + w - 80,
                yy + 26,
                80,
                40,
                digits(f"{i + 1:02d}", lang),
                13,
                T.W300,
                mono,
                mirror=False,
            )
            tb = box(
                s, x + 90 if not rtl else x, yy + 20, w - 90, step - 30, it, size, T.T1, sans, gap=1.2, mirror=False
            )
            if sub:
                text_frame_add(tb, sub[i], size * 0.68, T.T2, sans, 4)

    def scene_panel(name):
        """The scene drawing with numbered markers on its three labelled parts, cropped for the framed panel."""
        sc = scenes.scene_words(name, lang)
        set_canvas("16:9")
        drawing, anchors = sc["draw"](0.0)
        zt = scenes.zoomer(sc["zoom"])
        z = sc["zoom"]
        g = f'<g transform="translate({960 * (1 - z):.2f},{scenes.ZY * (1 - z):.2f}) scale({z})">{drawing}</g>'
        marks = ""
        for i, (_, key, _, _) in enumerate(sc["labels"]):
            ax, ay = zt(anchors[key])
            marks += circ(ax, ay, 24, T.W300)
            marks += text(
                ax, ay + 9, digits(str(i + 1), lang), 24, T.G950, F.MONO, 'text-anchor="middle" font-weight="700"'
            )
        body = background(*zt(sc["centre"]), seed=5) + g + finish() + marks
        lx, ly, lr = sc["lit"]
        return svg_doc(std_defs(*zt(sc["centre"]), lit=(lx, ly), lit_r=lr), body, alt=sc["alt"]), sc

    def side_rule(s, y):
        """A short rule under the words of the title and closing slides (they sit right of the lantern either way)."""
        r = s.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Emu((1260 if rtl else 1120) * EMU), Emu(y * EMU), Emu(560 * EMU), Emu(2 * EMU)
        )
        r.fill.solid()
        r.fill.fore_color.rgb = _rgb(hair)
        r.line.fill.background()

    # 1 title (the words sit beside the lantern in either direction)
    s = slide(cover_art(), N["title"])
    box(s, 1120, 300, 700, 30, D["kicker"].upper(), 12, T.W300, mono, mirror=False)
    tb = box(s, 1120, 350, 740, 360, D["title"], 56, T.T1, disp, gap=0.98, mirror=False)
    text_frame_add(tb, D["subtitle"], 20, T.W300, sans, 26, bold=True)
    side_rule(s, 760)
    box(s, 1120, 784, 700, 40, D["byline"], 13, T.T2, mono, mirror=False)
    # 2 agenda: the question on one side, the parts as a ruled list on the other
    s = slide(ground_art(), N["agenda"])
    chrome(s, LB["agenda"], 2)
    head(s, 120, 190, 620, D["agenda_title"], D["agenda_answer"], 52)
    numbered(s, mx(860, 940), 196, 940, D["agenda"], 30, 168)
    # 3 section break (lantern on the left, words on the right in both directions)
    s = slide(ground_art(lamp=True), N["section"])
    box(s, 900, 330, 900, 40, LB["section"].upper(), 14, T.W300, mono, mirror=False)
    tb = box(s, 900, 380, 900, 300, D["section"], 104, T.T1, disp, gap=0.95, mirror=False)
    text_frame_add(tb, D["section_answer"], 24, T.T2, sans, 30)
    # 4-6 illustrated explainers: words and the three labelled parts on one side, the drawing framed on the other
    for k, name in enumerate(SCENE_SLIDES):
        svg, sc = scene_panel(name)
        s = slide(ground_art(), f"{N['scene']} ({name})")
        chrome(s, f"{LB['scene']} {digits(f'{k + 1:02d}', lang)}", 4 + k)
        head(s, 120, 170, 600, " ".join(sc["title"]), sc["answer"], 30, 16)
        numbered(
            s,
            mx(120, 600),
            556,
            600,
            [lbl for _, _, lbl, _ in sc["labels"]],
            18,
            138,
            [txt for _, _, _, txt in sc["labels"]],
        )
        pic = s.shapes.add_picture(
            picture(svg, crop=(300, 250, 1620, 1060)),
            Emu(mx(780, 1020) * EMU),
            Emu(176 * EMU),
            Emu(1020 * EMU),
            Emu(626 * EMU),
        )
        pic.line.color.rgb = _rgb(hair)
        pic.line.width = Emu(2 * EMU)
    # 7 text: the question on one side, the points as a ruled list on the other
    s = slide(ground_art(), N["text"])
    chrome(s, LB["text"], 7)
    head(s, 120, 190, 620, D["text_title"], D["text_answer"], 52)
    numbered(s, mx(860, 940), 196, 940, D["text_points"], 24, 190)
    # 8 two columns (the first column sits where the reader starts: left, or right in right-to-left)
    s = slide(ground_art(), N["columns"])
    chrome(s, LB["columns"], 8)
    head(s, 120, 170, 1500, D["columns_title"], D["columns_answer"], 52)
    for k, (heading, pts) in enumerate(D["columns"]):
        x = 120 + k * 870
        col = T.W300 if k == 0 else T.L100
        rule(s, x, 440, 810, 4, col)
        box(s, x, 472, 810, 40, D["options"][k].upper(), 12, col, mono)
        box(s, x, 516, 810, 70, heading, 36, T.T1, disp)
        for i, pt in enumerate(pts):
            rule(s, x, 620 + i * 100, 810)
            box(s, x, 646 + i * 100, 810, 60, pt, 20, T.T2, sans)
    # 9 chart: the highlighted number large on one side, the native chart on the other
    s = slide(ground_art(), N["chart"])
    chrome(s, LB["chart"], 9)
    head(s, 120, 170, 620, D["chart_title"], D["chart_answer"], 44)
    box(s, 120, 600, 600, 200, digits("8.2", lang), 110, T.W300, disp)
    box(s, 120, 850, 600, 40, D["chart_note"], 14, T.T2, mono)
    data = CategoryChartData()
    data.categories = D["chart_categories"]
    data.add_series(D["chart_series"], (3.1, 4.6, 8.2, 4.4))
    gf = s.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(mx(800, 1000) * EMU), Emu(200 * EMU), Emu(1000 * EMU), Emu(740 * EMU), data
    )
    ch = gf.chart
    ch.has_legend = False
    ch.has_title = False
    ch.font.size, ch.font.name = Pt(14), sans
    ch.font.color.rgb = _rgb(T.T2)
    plot = ch.plots[0]
    plot.gap_width = 60
    plot.has_data_labels = True
    plot.data_labels.font.size, plot.data_labels.font.name = Pt(14), mono
    plot.data_labels.font.color.rgb = _rgb(T.T1)
    ser = plot.series[0]
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = _rgb(T.L100)
    pt = ser.points[2]
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = _rgb(T.W300)
    va = ch.value_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = _rgb(hair)
    va.format.line.fill.background()
    va.visible = False
    ch.category_axis.format.line.color.rgb = _rgb(T.L200)
    ch.category_axis.reverse_order = rtl  # the first quarter reads first, from the right in right-to-left
    # 10 closing
    s = slide(cover_art(), N["closing"])
    tb = box(s, 1120, 360, 700, 300, D["closing"], 72, T.T1, disp, gap=0.98, mirror=False)
    text_frame_add(tb, D["closing_answer"], 20, T.W300, sans, 26, bold=True)
    side_rule(s, 640)
    box(s, 1120, 664, 700, 40, D["contact"], 14, T.T2, mono, mirror=False)
    for p in ("title", "subject"):
        setattr(prs.core_properties, p, f"Lantern {T.name} template")
    prs.core_properties.author = ""
    prs.core_properties.last_modified_by = ""
    if lang:
        prs.core_properties.language = LANG_TAG.get(lang, lang)
    prs.save(out)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Make an editable slide template in a Lantern colour.")
    ap.add_argument("color", help="an installed colour, or 'all'")
    ap.add_argument("rest", nargs="*", help="variant (dark, light) and type set")
    ap.add_argument("--out", default=None, help="file name (one colour) or folder (all); default ./out/decks/")
    ap.add_argument("--lang", default=None, help="fa for a Persian template, set right to left (default English)")
    a = ap.parse_args(argv)
    todo = colors() if a.color == "all" else [a.color]
    if any(c not in colors() for c in todo):
        sys.exit(f"unknown colour; installed: {', '.join(colors())}")
    variants = [v for v in a.rest if v in ("dark", "light")]
    tset = ([x for x in a.rest if x in SYS["type_sets"]] or [None])[0]
    for c in todo:
        for v in variants or (
            ["dark", "light"] if a.color == "all" else [load_theme(c).get("default_variant", "dark")]
        ):
            set_theme(v, c, tset)
            if a.color != "all" and a.out:
                out = a.out
            else:
                folder = a.out or os.path.join("out", "decks")
                os.makedirs(folder, exist_ok=True)
                out = os.path.join(folder, f"lantern-{c}-{v}" + (f"-{a.lang}" if a.lang else "") + ".pptx")
            print(build_deck(out, lang=a.lang))


if __name__ == "__main__":
    main()
