"""Build the Lantern skills from one source.

    python build/build.py                 render reference images and pickers, write every skill, plugin and zip
    python build/build.py --skip-render   reuse the existing reference images and pickers (docs and code only)
    python build/build.py --install       also copy every skill into ~/.claude/skills for local use

Reads src/ (engine, themes, fonts, UI) and build/templates/. Writes:
    plugins/<skill>/                      one plugin per skill, listed in .claude-plugin/marketplace.json
    dist/<skill>.zip                      one upload zip per skill (not committed; attach to a release)
Needs the same Python packages as the skills themselves (Pillow, numpy, Playwright with Chromium).
"""

import argparse
import ast
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC, TEMPLATES, PLUGINS, DIST = REPO / "src", REPO / "build" / "templates", REPO / "plugins", REPO / "dist"
VERSION = "1.0.1"
BRAND = "lantern"
sys.path.insert(0, str(SRC / "scripts"))
from new_theme import NAMES as GENERIC  # noqa: E402

COLORS = {
    "blue": dict(
        N="Blue",
        ground="night-navy",
        accent="amber",
        built="a deep navy ground built from shades of the core colour #3366FF, with one amber light and a teal support family",
        aliases=["cobalt", "royal blue", "azure"],
    ),
    "purple": dict(
        N="Purple",
        ground="night-violet",
        accent="warm peach",
        built="a deep violet ground, with one warm peach light and a blue support family",
        aliases=["violet", "indigo", "lavender"],
    ),
    "black": dict(
        N="Black",
        ground="jet near-black",
        accent="metallic-gold",
        built="a jet near-black ground (#1C1C1E) in neutral greys, with one metallic-gold light",
        aliases=["jet", "onyx", "ebony", "noir", "black and gold"],
    ),
    "white": dict(
        N="White",
        ground="ivory paper",
        accent="white (ink only)",
        built="ivory paper (#FAF8F2) in strict monochrome: ink on paper, the light is plain white",
        aliases=["ivory", "porcelain", "paper", "cream", "black and white"],
    ),
    "green": dict(
        N="Green",
        ground="deep forest-green",
        accent="amber",
        built="a deep forest-green ground (#1B4D3E), with one amber light",
        aliases=["forest", "emerald", "jade", "sage", "olive"],
    ),
    "red": dict(
        N="Red",
        ground="deep maroon",
        accent="champagne",
        built="a deep maroon ground (#7A1F2B), with one champagne-gold light",
        aliases=["maroon", "burgundy", "crimson", "wine", "oxblood"],
    ),
    "gray": dict(
        N="Gray",
        ground="charcoal",
        accent="amber",
        built="a charcoal ground (#36454F), with one amber light",
        aliases=["grey", "silver", "charcoal", "slate", "graphite"],
    ),
    "teal": dict(
        N="Teal",
        ground="deep teal",
        accent="amber",
        built="a deep teal ground (#0F766E), with one amber light",
        aliases=["deep teal", "petrol", "teal green"],
    ),
    "gold": dict(
        N="Gold",
        ground="warm near-black",
        accent="metallic-gold",
        built="a warm near-black ground with metallic gold (#D4AF37) as the light",
        aliases=["yellow", "mustard", "golden", "ochre"],
    ),
    "orange": dict(
        N="Orange",
        ground="warm near-black",
        accent="tangerine",
        built="a warm near-black ground with burnt orange (#CC5500) as the brand colour and tangerine as the light",
        aliases=["burnt orange", "tangerine", "persimmon", "copper"],
    ),
    "cyan": dict(
        N="Cyan",
        ground="vivid deep-cyan",
        accent="amber",
        built="a vivid deep-cyan ground built from bright cyan (#1CABE2), with one amber light",
        aliases=["aqua", "turquoise", "sky blue"],
    ),
    "rose": dict(
        N="Rose",
        ground="deep rose",
        accent="champagne",
        built="a deep rose ground (#C2185B), with one champagne-gold light",
        aliases=["pink", "raspberry", "magenta", "fuchsia"],
    ),
}
ROLES = [
    (
        "Ground (radial, centre to edge)",
        [
            ("G600", "centre"),
            ("G700", "25%"),
            ("G800", "50%, default room"),
            ("G900", "78%"),
            ("G950", "edge"),
            ("VIGN", "vignette"),
        ],
    ),
    (
        "Structure",
        [
            ("IN900", "hull and shell outlines, 2.5 to 3 px"),
            ("IN800", "part outlines, 1.4 to 2 px"),
            ("IN700", "recesses, bezels"),
            ("IN600", "floor slabs"),
            ("IN500", "hubs, feet"),
            ("V500", "big bodies"),
            ("V400", "pipes, panels"),
            ("V300", "secondary panels"),
            ("L300", "slab edges, rivet highlights"),
            ("L200", "rails, rods, rungs"),
            ("L100", "information"),
            ("MIST", "glass highlights, steam, rings"),
        ],
    ),
    (
        "Accent: energy, attention, the watched (the one accent)",
        [
            ("W100", "hottest light"),
            ("W200", "lit objects: cups, windows, parcels"),
            ("W300", "energy flows, leader lines, answer line"),
            ("W400", "rim light"),
            ("ROSE3", "tag prefix, mid accent"),
            ("ROSE5", "accent dark (graphics only)"),
            ("COFFEE", "deepest accent (graphics only)"),
        ],
    ),
    (
        "Support (natural things only)",
        [("B200", "water and coolant flows"), ("B400", "support mid"), ("B600", "support dark")],
    ),
    (
        "Ink and text",
        [("INK", "silhouettes"), ("T1", "text-primary"), ("T2", "text-secondary"), ("T3", "text-muted (credits)")],
    ),
    (
        "Core, status and data",
        [
            ("CORE", "the brand colour: primary actions in UI"),
            ("CORE_FILL", "button fill: the core, or the nearest ramp step that carries white text"),
            ("ON_CORE", "text on a core fill"),
            ("OK", "success"),
            ("WARN", "warning"),
            ("ERR", "error"),
        ],
    ),
]
STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]


def slug(color=None):
    return BRAND if color is None else f"{BRAND}-{color}"


def write(path, s):
    Path(path).write_text(s, encoding="utf-8", newline="\n")


def tokens_md(tok):
    d, l, nm = tok["variants"]["dark"]["colors"], tok["variants"]["light"]["colors"], tok["names"]
    out = []
    for title, rows in ROLES:
        out.append(f"\n**{title}**\n\n| Token | Kit | Dark | Light | Use |\n|---|---|---|---|---|")
        out += [
            f"| {nm.get(k, k.lower().replace('_', '-'))} | `T.{k}` | `{d[k]}` | `{l[k]}` | {use} |" for k, use in rows
        ]
    out.append(
        "\n**Core ramp, 50 (lightest) to 950 (darkest)**, the same in both variants (`T.CORE_50` ... `T.CORE_950`, CSS `--core-50` ... `--core-950`): "
        + " · ".join(f"{s} `{d[f'CORE_{s}']}`" for s in STEPS)
    )
    return "\n".join(out)


def roles_md():
    out = ["| Role | Kit | Use |", "|---|---|---|"]
    for _, rows in ROLES:
        out += [f"| {GENERIC.get(k, k.lower().replace('_', '-'))} | `T.{k}` | {use} |" for k, use in rows]
    return "\n".join(out)


def api_md(path, skip=()):
    rows = []
    for n in ast.parse(Path(path).read_text(encoding="utf-8")).body:
        if isinstance(n, ast.FunctionDef) and not n.name.startswith("_") and n.name not in skip:
            doc = (ast.get_docstring(n) or "").replace("\n", " ").replace("|", "/")
            rows.append(f"| `{n.name}({ast.unparse(n.args)})` | {doc} |")
    return "| Function | What it does |\n|---|---|\n" + "\n".join(rows)


def scene_md():
    import scenes

    rows = [f"| `{n}` | {' '.join(sc['title'])} | {sc['answer']} |" for n, sc in scenes.SCENES.items()]
    return (
        "`build(name, t, annotate=True, words=None)` returns the finished slide; `art(name, t)` the drawing alone. "
        "Each scene is a seamless loop.\n\n| Scene | Question | Answer line |\n|---|---|---|\n" + "\n".join(rows)
    )


def keep_mode(md, keep):
    """Drop the [[master]] or [[single]] blocks that do not belong to this skill."""
    drop = "single" if keep == "master" else "master"
    while f"[[{drop}]]" in md:
        a = md.index(f"[[{drop}]]")
        b = md.index(f"[[/{drop}]]") + len(f"[[/{drop}]]\n")
        md = md[:a] + md[b:]
    return md.replace(f"[[{keep}]]\n", "").replace(f"[[/{keep}]]\n", "")


def descriptions(themes):
    names = ", ".join(t["name"] for t in themes.values())
    master = (
        "Lantern, a design system for illustrated slides, cut-away machines and buildings, close-up portrait scenes, annotated figures, title and break slides, GIF/MP4 loops "
        f"and a small UI kit with code tokens, in one style across many colour themes ({names}, and any colour added from a brand colour), each with a 50-950 shade ramp, "
        "dark and light variants and three type sets. Use when the user says 'lantern', 'lantern design system', 'multi-color design system', 'design system', 'my design system', "
        "'house style', names a colour with no skill of its own, wants a new theme or palette from a brand colour, drops reference images to match, or wants tokens exported to "
        "CSS or Tailwind. Also use for any design task (slide, deck, figure, illustration, poster, title or break slide, animation, simple interface) with no style chosen: show "
        "the picker and ask which colour, then which variant, type set and shade, before designing."
    )
    single = {}
    for c, s in COLORS.items():
        single[c] = (
            f"Lantern {s['N']}: illustrated slides, cut-away machines and buildings, close-up portrait scenes, annotated concept figures, title and break slides, seamless "
            f"GIF/MP4 loops, and a small UI kit with code tokens, in the {s['N']} colour theme ({s['ground']} ground, one {s['accent']} light, grain, silhouette figures, "
            f"glowing flow lines), in dark or light with three type sets. Use when the user says 'lantern {c}', '{c} design system', '{c} system', '{c} style', 'my {c} style', "
            f"'the {c} one', '{c} theme', '{c} deck' or any variation, or a shade name with 'design system', 'style' or 'theme': {', '.join(s['aliases'])}. For a choice "
            "between colours, a new colour, or a design task with no colour named, use the lantern skill instead."
        )
    return master, single


def render_references(work):
    """Every scene, colour and variant through the engine's own self-check, saved as compact JPEGs."""
    from PIL import Image

    subprocess.run(
        [sys.executable, str(SRC / "scripts" / "examples.py")], cwd=work, check=True, stdout=subprocess.DEVNULL
    )
    subprocess.run([sys.executable, str(SRC / "scripts" / "picker.py"), "--all"], check=True, stdout=subprocess.DEVNULL)
    ref = Path(work) / "reference"
    for color_dir in (Path(work) / "out").iterdir():
        (ref / color_dir.name).mkdir(parents=True, exist_ok=True)
        for f in color_dir.glob("*.png"):
            im = Image.open(f).convert("RGB")
            im.thumbnail((1100, 1100))
            im.save(ref / color_dir.name / f"{f.stem}.jpg", quality=80)
    return ref


def skill_dir(color=None):
    return PLUGINS / slug(color) / "skills" / slug(color)


def write_skill(color, themes, ref, master_desc, single_desc):
    """Assemble one self-contained skill folder from the engine, its theme(s) and the generated docs."""
    sk = skill_dir(color)
    old_assets = sk / "assets"
    keep = {}
    if ref is None and old_assets.exists():  # --skip-render: carry the previous images over
        keep = {p: (old_assets / p) for p in ("reference", "picker", "picker.jpg") if (old_assets / p).exists()}
        tmp = Path(tempfile.mkdtemp())
        for p, src in keep.items():
            (shutil.copytree if src.is_dir() else shutil.copy)(src, tmp / p)
        keep = {p: tmp / p for p in keep}
    if sk.exists():
        shutil.rmtree(sk)
    sk.mkdir(parents=True)
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
    for d in ("scripts", "ui"):
        shutil.copytree(SRC / d, sk / d, ignore=ignore)
    shutil.copytree(SRC / "assets" / "fonts", sk / "assets" / "fonts")
    (sk / "themes").mkdir()
    sysj = json.loads((SRC / "system.json").read_text(encoding="utf-8"))
    for c in themes if color is None else [color]:
        shutil.copy(SRC / "themes" / f"{c}.json", sk / "themes" / f"{c}.json")
    if color:
        sysj["default_color"] = color
    write(sk / "system.json", json.dumps(sysj, indent=1) + "\n")
    if ref is not None:
        for c in themes if color is None else [color]:
            shutil.copytree(ref / c, sk / "assets" / "reference" / c)
        (sk / "assets" / "picker").mkdir()
        for c in themes if color is None else [color]:
            shutil.copy(SRC / "assets" / "picker" / f"{c}.jpg", sk / "assets" / "picker" / f"{c}.jpg")
        if color is None:
            shutil.copy(SRC / "assets" / "picker.jpg", sk / "assets" / "picker.jpg")
    else:
        for p, src in keep.items():
            (shutil.copytree if src.is_dir() else shutil.copy)(src, sk / "assets" / p)

    mode = "master" if color is None else "single"
    tpl = keep_mode((TEMPLATES / "skill.md").read_text(encoding="utf-8"), mode)
    if color is None:
        v = dict(
            slug=slug(),
            title="Lantern design system",
            description=master_desc,
            installed=", ".join(t["name"] for t in themes.values()),
            example_color="blue",
            roles_table=roles_md(),
            installed_table="| Colour | Core | Light | Default type set | Default variant |\n|---|---|---|---|---|\n"
            + "\n".join(
                f"| {t['name']} | `{t['core']}` | {t.get('accent_label', 'amber light')} | {t.get('default_type', 'classic')} | {t.get('default_variant', 'dark')} |"
                for t in themes.values()
            ),
        )
    else:
        s, tok = COLORS[color], themes[color]
        v = dict(
            s,
            slug=slug(color),
            title=f"Lantern {s['N']}",
            description=single_desc[color],
            nl=color,
            example_color=color,
            tokens=tokens_md(tok),
            default_type=tok.get("default_type", "classic"),
            default_variant=tok.get("default_variant", "dark"),
            aliases=", ".join(s["aliases"]),
            shade=next((x["name"] for x in tok.get("shades", []) if x["core"] == tok["core"].lower()), s["N"]),
        )
    for k, val in v.items():
        tpl = tpl.replace("{" + k + "}", val)
    left = [w for w in ("{N}", "{nl}", "{slug}", "{title}", "{tokens}", "{aliases}") if w in tpl]
    if left:
        raise SystemExit(f"{slug(color)}: unfilled placeholders {left}")
    if len(v["description"]) > 1024:
        raise SystemExit(f"{slug(color)}: description is {len(v['description'])} characters (limit 1024)")
    write(sk / "SKILL.md", tpl)
    (sk / "references").mkdir()
    title = v["title"]
    write(
        sk / "references" / "components.md",
        f"# {title}: component and function reference\n\nDrawing functions return SVG strings in local coordinates and read colours from the theme, "
        "so one scene renders in every colour and variant. `p` is the loop phase 0..1; `y` is the floor or base line unless stated. `assets/reference/<colour>/sheet_dark.jpg` and "
        "`sheet_light.jpg` show every element rendered.\n\n## components.py\n\n"
        + api_md(sk / "scripts" / "components.py")
        + "\n\n## kit.py\n\n"
        + api_md(sk / "scripts" / "kit.py", skip=("f2", "lerp", "frac", "poly_len", "point_at"))
        + "\n\n## scenes.py: the scene library\n\n"
        + scene_md()
        + "\n",
    )
    write(
        sk / "references" / "animation.md",
        (TEMPLATES / "animation.md")
        .read_text(encoding="utf-8")
        .replace("# {N}: seamless loops", "# Seamless loops")
        .replace("{N}", title)
        .replace("from kit import T, C\n", "from kit import T, C, F\n"),
    )
    write(
        sk / "references" / "voice.md",
        (TEMPLATES / "voice.md")
        .read_text(encoding="utf-8")
        .replace("none on titles of labels or on buttons", "none on titles, labels or buttons"),
    )
    write(sk / "references" / "themes.md", (TEMPLATES / "themes.md").read_text(encoding="utf-8"))
    plugin = {
        "name": slug(color),
        "version": VERSION,
        "description": v["description"].split(". Use when")[0] + ".",
        "license": "Apache-2.0",
        "author": {"name": "Lantern contributors"},
        "keywords": ["design-system", "slides", "illustration", "svg", "theme"]
        + ([color] + COLORS[color]["aliases"][:2] if color else ["multi-color"]),
    }
    (PLUGINS / slug(color) / ".claude-plugin").mkdir(exist_ok=True)
    write(PLUGINS / slug(color) / ".claude-plugin" / "plugin.json", json.dumps(plugin, indent=2) + "\n")
    return sk, v["description"]


def marketplace(names, descs):
    m = {
        "name": "lantern-design-system",
        "owner": {"name": "Lantern contributors"},
        "metadata": {
            "description": "Lantern: one illustration and interface style in many colours, as installable skills.",
            "version": VERSION,
        },
        "plugins": [
            {
                "name": n,
                "source": f"./plugins/{n}",
                "description": descs[n].split(". Use when")[0] + ".",
                "version": VERSION,
            }
            for n in names
        ],
    }
    (REPO / ".claude-plugin").mkdir(exist_ok=True)
    write(REPO / ".claude-plugin" / "marketplace.json", json.dumps(m, indent=2) + "\n")


def zip_skill(sk):
    DIST.mkdir(exist_ok=True)
    out = DIST / f"{sk.name}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(sk.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f, f.relative_to(sk.parent).as_posix())
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--skip-render", action="store_true")
    ap.add_argument("--install", action="store_true")
    a = ap.parse_args()
    themes = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((SRC / "themes").glob("*.json"))}
    missing = set(themes) ^ set(COLORS)
    if missing:
        raise SystemExit(f"themes and COLORS disagree: {sorted(missing)}")
    ref = None
    if not a.skip_render:
        work = Path(tempfile.mkdtemp(prefix="lantern-build-"))
        ref = render_references(work)
    if ref is not None:  # a few images for the README
        img = REPO / "docs" / "images"
        img.mkdir(parents=True, exist_ok=True)
        shutil.copy(SRC / "assets" / "picker.jpg", img / "picker.jpg")
        for c, scene in (
            ("blue", "factory_dark"),
            ("red", "factory_light"),
            ("gold", "break_dark"),
            ("purple", "portrait_dark"),
        ):
            shutil.copy(ref / c / f"{scene}.jpg", img / f"{c}_{scene}.jpg")
    master_desc, single_desc = descriptions(themes)
    built, descs = [], {}
    for color in [None] + list(COLORS):
        sk, d = write_skill(color, themes, ref, master_desc, single_desc)
        built.append(sk)
        descs[sk.name] = d
        r = subprocess.run([sys.executable, str(sk / "scripts" / "kit.py")], capture_output=True, text=True)
        for p in sk.rglob("__pycache__"):
            shutil.rmtree(p, ignore_errors=True)
        z = zip_skill(sk)
        print(f"{sk.name}: {r.stdout.strip() or r.stderr.strip()[-200:]}; zip {z.stat().st_size // 1024} KB")
    marketplace([sk.name for sk in built], descs)
    for p in (SRC / "scripts").rglob("__pycache__"):
        shutil.rmtree(p, ignore_errors=True)
    if a.install:
        home = Path.home() / ".claude" / "skills"
        for sk in built:
            dest = home / sk.name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(sk, dest)
        print(f"installed {len(built)} skills into {home}")


if __name__ == "__main__":
    main()
