"""Build the playground: a static page for GitHub Pages (Settings, Pages, deploy from the docs/ folder).

    python build/site.py                 render the scene images and write the page
    python build/site.py --skip-render   rewrite the page, styles and tokens only

Writes docs/index.html and docs/site/ (styles, fonts, per-colour tokens, scene images). The page needs no build
step or server code; it links to release downloads for the skill zips and slide templates.
"""

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src" / "scripts"))
sys.path.insert(0, str(REPO / "build"))
import scenes  # noqa: E402
from build import COLORS, VERSION  # noqa: E402
from export import tokens_css, variant_css  # noqa: E402
from kit import FONT_MANIFEST, ROOT, SYS, load_theme, render, set_theme  # noqa: E402
from new_theme import STEPS  # noqa: E402
from readme import BEST_FOR, ORDER  # noqa: E402

OWNER = "Amircode2050"
REPO_URL = f"https://github.com/{OWNER}/lantern-design-system"
DOCS, SITE = REPO / "docs", REPO / "docs" / "site"
FEATURED = ["supply_chain", "cloud_computing", "data_centre", "power_grid", "knowledge_base", "sales_funnel"]
SHORT = {
    "supply_chain": "Supply chain",
    "cloud_computing": "The cloud",
    "data_centre": "Data centre",
    "power_grid": "Power grid",
    "knowledge_base": "Knowledge base",
    "sales_funnel": "Sales funnel",
}


def styles():
    """lantern.css: the type scale once, each type set, then every colour and variant as attribute blocks."""
    out = [":root {"]
    for name, s in SYS["type_scale"].items():
        out += [f"  --fs-{name}: {s['size']}px;", f"  --lh-{name}: {s['line']}px;"]
    out += [f"  --space-{i + 1}: {v}px;" for i, v in enumerate(SYS["spacing"])]
    out += [f"  --radius-{i + 1}: {v}px;" for i, v in enumerate(SYS["radius"])] + ["}"]
    for key, d in SYS["type_sets"].items():
        fonts = " ".join(f"--font-{r}: {SYS['fonts'][d[r]]['stack']};" for r in ("display", "sans", "mono"))
        out.append(f'[data-type="{key}"] {{ {fonts} --subtitle-style: {d["subtitle_style"]}; }}')
    for c in ORDER:
        tok = load_theme(c)
        for v in ("dark", "light"):
            body = variant_css(tok["variants"][v]["colors"], v == "light")
            out.append(f'[data-color="{c}"][data-theme="{v}"] {{\n  color-scheme: {v};\n  {body}\n}}')
    (SITE / "lantern.css").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")


def fonts():
    """The page is in English, so it serves the Latin files of every family (with their unicode ranges)."""
    out = SITE / "fonts"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    rules = []
    for f in FONT_MANIFEST["files"]:
        if f["subset"] != "latin":
            continue
        shutil.copy(ROOT / "assets" / "fonts" / f"{f['file']}.woff2", out / f"{f['file']}.woff2")
        rules.append(
            f"@font-face {{ font-family: '{f['family']}'; font-weight: {f['weight']}; font-style: {f['style']}; "
            f"font-display: swap; unicode-range: {f['range']}; src: url(fonts/{f['file']}.woff2) format('woff2'); }}"
        )
    shutil.copy(ROOT / "assets" / "fonts" / "LICENSES.txt", out / "LICENSES.txt")
    (SITE / "fonts.css").write_text("\n".join(rules) + "\n", encoding="utf-8", newline="\n")


def images():
    """Six featured scenes in every colour and variant, and the whole library spread across the colours."""
    from PIL import Image

    tmp = Path(tempfile.mkdtemp(prefix="lantern-site-"))
    (SITE / "img").mkdir(parents=True, exist_ok=True)
    (SITE / "lib").mkdir(parents=True, exist_ok=True)

    def save(svg, out, width):
        png = render(svg, str(tmp / "frame.png"), scale=1)
        im = Image.open(png).convert("RGB")
        im.thumbnail((width, width))
        im.save(out, "WEBP", quality=80, method=6)

    for c in ORDER:
        for v in ("dark", "light"):
            set_theme(v, c)
            for s in FEATURED:
                save(scenes.build(s, 3.0), SITE / "img" / f"{c}_{s}_{v}.webp", 1280)
        print(c, flush=True)
    for i, s in enumerate(scenes.SCENES):
        c = ORDER[i % len(ORDER)]
        set_theme(load_theme(c).get("default_variant", "dark"), c)
        save(scenes.build(s, 3.0), SITE / "lib" / f"{s}.webp", 800)


def library():
    return [[s, f"{s}.webp"] for s in scenes.SCENES]


def page():
    data = {
        "owner": OWNER,
        "steps": STEPS,
        "featured": FEATURED,
        "types": [[k, v["label"]] for k, v in SYS["type_sets"].items()],
        "library": library(),
        "colors": {},
        "scenes": {
            n: {
                "title": " ".join(sc["title"]),
                "answer": sc["answer"],
                "alt": sc["alt"],
                "short": SHORT.get(n, n.replace("_", " ").capitalize()),
            }
            for n, sc in scenes.SCENES.items()
        },
    }
    for c in ORDER:
        t = load_theme(c)
        d = t["variants"]["dark"]["colors"]
        data["colors"][c] = {
            "name": t["name"],
            "core": t["core"].lower(),
            "ramp": [d[f"CORE_{s}"] for s in STEPS],
            "built": COLORS[c]["built"],
            "best": BEST_FOR[c],
            "variant": t.get("default_variant", "dark"),
            "type": t.get("default_type", "classic"),
        }
    html = (REPO / "build" / "templates" / "site.html").read_text(encoding="utf-8")
    for k, v in (
        ("data", json.dumps(data, separators=(",", ":"))),
        ("repo", REPO_URL),
        ("version", VERSION),
        ("scene_count", str(len(scenes.SCENES))),
    ):
        html = html.replace("{{" + k + "}}", v)
    (DOCS / "index.html").write_text(html, encoding="utf-8", newline="\n")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--skip-render", action="store_true")
    a = ap.parse_args()
    SITE.mkdir(parents=True, exist_ok=True)
    (SITE / "tokens").mkdir(exist_ok=True)
    styles()
    fonts()
    shutil.copy(ROOT / "ui" / "ui.css", SITE / "ui.css")
    for c in ORDER:
        t = load_theme(c)
        css = tokens_css(c, t.get("default_type", "classic"), t.get("default_variant", "dark"))
        (SITE / "tokens" / f"{c}.css").write_text(css, encoding="utf-8", newline="\n")
    (SITE / "icon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="3.5" r="2" fill="none" '
        'stroke="#1c1c1e" stroke-width="1.4"/><path d="M7 9l2-3h6l2 3z" fill="#1c1c1e"/><rect x="7.5" y="9" width="9" '
        'height="9" rx="1" fill="#f4b740"/><path d="M8 18h8l-1.5 3h-5z" fill="#1c1c1e"/></svg>\n',
        encoding="utf-8",
        newline="\n",
    )
    if not a.skip_render:
        images()
    page()
    print(f"wrote {DOCS / 'index.html'} and {SITE}")


if __name__ == "__main__":
    main()
