"""Unit tests for the parts of Lantern that need no browser: colour maths, themes, brand colours, fonts,
right-to-left text, scenes and translations, social cards and slide-template words.

    python -m unittest discover -s tests -v
"""

import json
import random
import re
import sys
import unittest
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src" / "scripts"))

import brand  # noqa: E402
import deck  # noqa: E402
import kit  # noqa: E402
import new_theme  # noqa: E402
import scenes  # noqa: E402
import social  # noqa: E402
from kit import FONT_MANIFEST, contrast, from_oklch, hexmix, is_rtl, to_oklch  # noqa: E402

HEX = re.compile(r"^#[0-9a-f]{6}$")


class ColourMaths(unittest.TestCase):
    def test_oklch_round_trip(self):
        rnd = random.Random(1)
        for _ in range(300):
            h = "#" + "".join(f"{rnd.randrange(256):02x}" for _ in range(3))
            back = from_oklch(*to_oklch(h))
            for i in (1, 3, 5):
                self.assertLessEqual(abs(int(h[i : i + 2], 16) - int(back[i : i + 2], 16)), 1, (h, back))

    def test_out_of_gamut_is_clipped_to_a_valid_hex(self):
        self.assertRegex(from_oklch(0.7, 0.9, 140), HEX)

    def test_contrast_extremes_and_symmetry(self):
        self.assertAlmostEqual(contrast("#000000", "#ffffff"), 21.0, places=2)
        self.assertAlmostEqual(contrast("#3366ff", "#ffffff"), contrast("#ffffff", "#3366ff"))
        self.assertEqual(contrast("#777777", "#777777"), 1.0)

    def test_hexmix_endpoints(self):
        self.assertEqual(hexmix("#000000", "#ffffff", 0), "#000000")
        self.assertEqual(hexmix("#000000", "#ffffff", 1), "#ffffff")


class Themes(unittest.TestCase):
    def test_ramp_has_eleven_steps_darkening_and_keeps_the_core(self):
        core = "#3366ff"
        r = new_theme.ramp(core)
        steps = [r[f"CORE_{s}"] for s in new_theme.STEPS]
        self.assertEqual(len(steps), 11)
        self.assertIn(core, steps)
        lightness = [to_oklch(c)[0] for c in steps]
        self.assertEqual(lightness, sorted(lightness, reverse=True))

    def test_every_installed_theme_passes_its_contrast_rules(self):
        self.assertEqual(kit.check_tokens(), [])

    def test_button_fill_carries_its_text(self):
        for c in kit.colors():
            for v in ("dark", "light"):
                col = kit.load_theme(c)["variants"][v]["colors"]
                self.assertGreaterEqual(contrast(col["CORE_FILL"], col["ON_CORE"]), 4.5, (c, v))

    def test_theme_names_cannot_escape_the_themes_folder(self):
        for bad in ("../evil", "Red", "a/b", "1abc", ""):
            self.assertIsNone(new_theme.NAME.match(bad), bad)
        self.assertIsNotNone(new_theme.NAME.match("red_crimson"))


class Brand(unittest.TestCase):
    def test_picks_the_characteristic_colour_over_greys_and_pale_yellow(self):
        core, _ = brand.pick(Counter({"#3776ab": 30, "#ffd343": 30, "#111111": 400, "#ffffff": 300}))
        self.assertEqual(core, "#3776ab")

    def test_neutral_brand_has_no_chromatic_core(self):
        self.assertIsNone(brand.pick(Counter({"#111111": 10, "#eeeeee": 10}))[0])

    def test_reads_css_colours(self):
        self.assertEqual(brand.css_colors("a{color:#FFF;background:rgb(51, 102, 255)}"), ["#ffffff", "#3366ff"])

    def test_refuses_local_private_and_non_web_addresses(self):
        for bad in (
            "file:///tmp/a.css",
            "ftp://example.com/a",
            "http://127.0.0.1/",
            "http://10.1.2.3/",
            "http://[::1]/",
        ):
            with self.assertRaises(ValueError, msg=bad):
                brand.public(bad)

    def test_recipe_for_a_yellow_borrows_gold(self):
        self.assertEqual(brand.recipe_for("#d4af37"), "gold")


class Fonts(unittest.TestCase):
    def test_manifest_entries_are_pinned_and_hashed(self):
        for f in FONT_MANIFEST["files"]:
            self.assertRegex(f["sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(f["url"].startswith("https://cdn.jsdelivr.net/npm/@fontsource/"), f["url"])
            self.assertIn(f["pack"], FONT_MANIFEST["packs"])
            self.assertTrue(f["spans"], f["file"])

    def test_every_type_set_names_known_families(self):
        for name, d in kit.SYS["type_sets"].items():
            for role in ("display", "sans", "mono"):
                self.assertIn(d[role], kit.SYS["fonts"], (name, role))

    def test_subsets_are_embedded_only_for_text_that_needs_them(self):
        latin = kit.font_css(["Vazirmatn", "Inter"], "Hello")
        persian = kit.font_css(["Vazirmatn", "Inter"], "سلام")
        self.assertNotIn("font-family:'Vazirmatn'", latin)
        self.assertIn("font-family:'Inter'", latin)
        self.assertIn("font-family:'Vazirmatn'", persian)


class RightToLeft(unittest.TestCase):
    def setUp(self):
        kit.set_theme("dark", "blue", "classic")

    def test_detects_scripts(self):
        self.assertTrue(is_rtl("سلام"))
        self.assertTrue(is_rtl("שלום"))
        self.assertFalse(is_rtl("Hello, Привет, Γεια"))

    def test_rtl_line_is_set_right_to_left_and_aligned_to_its_block(self):
        svg = kit.text(100, 50, "سلام", 20, right=400)
        self.assertIn('direction="rtl"', svg)
        self.assertIn('x="400', svg)

    def test_anchored_rtl_line_keeps_its_side(self):
        svg = kit.text(1800, 50, "سلام", 20, extra='text-anchor="end"')
        self.assertIn('text-anchor="start"', svg)

    def test_greek_and_cyrillic_measure_wider_than_latin(self):
        self.assertGreater(kit.text_width("Привет", 20), kit.text_width("Privet", 20))


class ScenesAndWords(unittest.TestCase):
    def setUp(self):
        kit.set_theme("dark", "teal", "classic")

    def test_every_scene_builds_in_every_language(self):
        for lang in [None] + scenes.languages():
            for name in scenes.SCENES:
                svg = scenes.build(name, 0.0, lang=lang)
                self.assertTrue(svg.startswith("<svg"), (name, lang))

    def test_translations_keep_every_label_slot(self):
        for lang in scenes.languages():
            for name, sc in scenes.SCENES.items():
                tr = scenes.scene_words(name, lang)
                self.assertEqual([lab[:2] for lab in tr["labels"]], [lab[:2] for lab in sc["labels"]], (name, lang))

    def test_persian_scene_is_set_right_to_left(self):
        svg = scenes.build("bank", lang="fa")
        self.assertIn('direction="rtl"', svg)
        self.assertIn(scenes.scene_words("bank", "fa")["credit"], svg)

    def test_unknown_language_is_refused(self):
        with self.assertRaises(ValueError):
            scenes.scene_words("bank", "xx")

    def test_social_cards_build_in_every_format(self):
        for fmt in social.FORMATS:
            self.assertTrue(social.card("cloud_computing", fmt, lang="fa").startswith("<svg"), fmt)


class SlideTemplateWords(unittest.TestCase):
    def test_persian_template_words_cover_every_english_key(self):
        fa = json.loads((REPO / "src" / "scripts" / "words" / "fa.json").read_text(encoding="utf-8"))["deck"]
        self.assertEqual(set(fa) - {"notes"}, set(deck.EN) - {"notes"})
        self.assertEqual(set(fa["notes"]), set(deck.EN["notes"]))

    def test_persian_digits(self):
        self.assertEqual(deck.digits("01", "fa"), "۰۱")
        self.assertEqual(deck.digits("01", None), "01")

    def test_languages_without_template_words_are_refused(self):
        with self.assertRaises(ValueError):
            deck.deck_words("es")


if __name__ == "__main__":
    unittest.main()
