"""Recipes for the generated colour themes. Blue and Purple are hand-tuned and are not rebuilt here.

python build/themes.py            rebuild every generated theme in src/themes/
python build/themes.py red teal   rebuild only these
"""

import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.insert(0, os.path.join(SRC, "scripts"))
import new_theme  # noqa: E402  (needs the path set above)

# name, core, options, current shade name, other shades
RECIPES = [
    (
        "black",
        "#1C1C1E",
        ["--accent", "#D4AF37", "--deep", "0.55", "--type", "classic", "--label", "metallic-gold light"],
        "Jet",
        [("Onyx", "#111111"), ("Rich black", "#0B0B0C")],
    ),
    (
        "white",
        "#FAF8F2",
        [
            "--harmony",
            "monochrome",
            "--deep",
            "0.7",
            "--type",
            "editorial",
            "--default-variant",
            "light",
            "--label",
            "white light, ink only",
        ],
        "Ivory",
        [("Porcelain", "#F7F7F5"), ("Pure white", "#FFFFFF")],
    ),
    (
        "green",
        "#1B4D3E",
        ["--type", "classic", "--label", "amber light"],
        "Forest",
        [("Emerald", "#046C4E"), ("Jade", "#00A86B")],
    ),
    (
        "red",
        "#7A1F2B",
        ["--accent", "#D8B47A", "--type", "editorial", "--label", "champagne light"],
        "Maroon",
        [("Burgundy", "#800020"), ("Crimson", "#A4161A")],
    ),
    (
        "gray",
        "#36454F",
        ["--type", "modern", "--label", "amber light"],
        "Charcoal",
        [("Slate", "#475569"), ("Silver", "#A8A9AD")],
    ),
    (
        "teal",
        "#0F766E",
        ["--type", "modern", "--label", "amber light"],
        "Deep teal",
        [("Petrol", "#005F73"), ("Teal", "#008080")],
    ),
    (
        "gold",
        "#D4AF37",
        [
            "--accent",
            "core",
            "--ground-chroma",
            "0.22",
            "--deep",
            "0.6",
            "--type",
            "classic",
            "--label",
            "gold light on near-black",
        ],
        "Metallic gold",
        [("Antique gold", "#C9A227"), ("Mustard", "#E1AD01")],
    ),
    (
        "orange",
        "#CC5500",
        [
            "--accent",
            "#F28C28",
            "--ground-chroma",
            "0.22",
            "--deep",
            "0.6",
            "--type",
            "modern",
            "--label",
            "orange light on near-black",
        ],
        "Burnt orange",
        [("Persimmon", "#E4572E"), ("Tangerine", "#F28C28")],
    ),
    (
        "cyan",
        "#1CABE2",
        ["--type", "modern", "--label", "amber light", "--deep", "1.05", "--ground-chroma", "1.6"],
        "Bright cyan",
        [("Cyan", "#0891B2"), ("Aqua", "#00B4D8")],
    ),
    (
        "rose",
        "#C2185B",
        ["--accent", "#D8B47A", "--type", "editorial", "--label", "champagne light"],
        "Rose",
        [("Deep rose", "#9E1450"), ("Blush rose", "#D4708F")],
    ),
]

if __name__ == "__main__":
    only = set(sys.argv[1:])
    fails = 0
    for name, core, opts, shade, alts in RECIPES:
        if only and name not in only:
            continue
        shades = [f"{shade}={core}"] + [f"{n}={h}" for n, h in alts]
        fails += new_theme.main([name, core, *opts, "--shades", *shades, "--force"])
    sys.exit(1 if fails else 0)
