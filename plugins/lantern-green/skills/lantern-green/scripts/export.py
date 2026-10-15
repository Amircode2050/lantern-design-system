"""export: hand a colour theme to a codebase or a web page.

    python export.py blue out/blue                    tokens.css, fonts.css, tailwind.theme.js, ui.css, demo.html
    python export.py purple out/p --type editorial    choose the type set
    python export.py blue out/b --default light       light on :root, dark under [data-theme="dark"]

tokens.css uses the same variable names for every colour, so switching colour is swapping one file,
and switching variant is setting data-theme="dark" or "light" on <html>.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import ROOT, SYS, colors, contrast, font_css, hexmix, load_theme
from new_theme import NAMES


def variant_css(c, light):
    raw = [f"--{NAMES[k]}: {c[k]};" for k in NAMES if k in c] + [
        f"--ok: {c['OK']};",
        f"--warn: {c['WARN']};",
        f"--err: {c['ERR']};",
    ]
    on_accent = max((c["INK"], "#ffffff"), key=lambda x: contrast(x, c["W300"]))
    sem = {
        "bg": c["G700"] if light else c["G950"],
        "surface": c["G600"] if light else c["G900"],
        "surface-2": c["G800"],
        "border": c["L300"] if light else c["V500"],
        "text": c["T1"],
        "text-2": c["T2"],
        "text-3": c["T3"],
        "primary": c["CORE_FILL"],
        "on-primary": c["ON_CORE"],
        "primary-hover": hexmix(c["CORE_FILL"], c["INK"] if light or c["ON_CORE"] == "#ffffff" else "#ffffff", 0.14),
        "accent-fg": c["W300"],
        "on-accent": on_accent,
        "link": c["L100"],
        "info": c["L100"],
        "support": c["B200"],
        "ring": c["L200"],
    }
    return "\n  ".join(raw + [f"--{k}: {v};" for k, v in sem.items()])


def tokens_css(color, type_set, default):
    tok = load_theme(color)
    d = SYS["type_sets"][type_set]
    other = "light" if default == "dark" else "dark"
    shared = [f"--font-{r}: {SYS['fonts'][d[r]]['stack']};" for r in ("display", "sans", "mono")] + [
        f"--subtitle-style: {d['subtitle_style']};"
    ]
    for name, s in SYS["type_scale"].items():
        shared += [f"--fs-{name}: {s['size']}px;", f"--lh-{name}: {s['line']}px;"]
    shared += [f"--space-{i + 1}: {v}px;" for i, v in enumerate(SYS["spacing"])] + [
        f"--radius-{i + 1}: {v}px;" for i, v in enumerate(SYS["radius"])
    ]
    return (
        f'/* {tok["name"]} theme, core {tok["core"]}. Variant: set data-theme="dark" or "light" on <html>. */\n'
        f":root {{\n  " + "\n  ".join(shared) + "\n}\n"
        f':root, [data-theme="{default}"] {{\n  color-scheme: {default};\n  {variant_css(tok["variants"][default]["colors"], default == "light")}\n}}\n'
        f'[data-theme="{other}"] {{\n  color-scheme: {other};\n  {variant_css(tok["variants"][other]["colors"], other == "light")}\n}}\n'
    )


def tailwind_js():
    cols = ",\n      ".join(
        f"'{v}': 'var(--{v})'"
        for v in list(NAMES.values())
        + [
            "ok",
            "warn",
            "err",
            "bg",
            "surface",
            "surface-2",
            "border",
            "text",
            "text-2",
            "text-3",
            "primary",
            "on-primary",
            "accent-fg",
            "on-accent",
            "link",
        ]
    )
    size = ",\n      ".join(f"'{n}': ['var(--fs-{n})', 'var(--lh-{n})']" for n in SYS["type_scale"])
    return (
        "// Tailwind theme extension. Load tokens.css first; every value is a CSS variable, so themes and variants swap at runtime.\n"
        "module.exports = {\n  theme: { extend: {\n    colors: {\n      " + cols + "\n    },\n"
        "    fontFamily: { display: 'var(--font-display)', sans: 'var(--font-sans)', mono: 'var(--font-mono)' },\n"
        "    fontSize: {\n      " + size + "\n    },\n"
        "    spacing: { "
        + ", ".join(f"'ds-{i + 1}': 'var(--space-{i + 1})'" for i in range(len(SYS["spacing"])))
        + " },\n"
        "    borderRadius: { "
        + ", ".join(f"'ds-{i + 1}': 'var(--radius-{i + 1})'" for i in range(len(SYS["radius"])))
        + " },\n  } },\n};\n"
    )


def export(color, out, type_set=None, default="dark"):
    tok = load_theme(color)
    type_set = type_set or tok.get("default_type") or SYS["default_type_set"]
    d = SYS["type_sets"][type_set]
    os.makedirs(out, exist_ok=True)

    def w(name, s):
        Path(out, name).write_text(s, encoding="utf-8", newline="\n")

    w("tokens.css", tokens_css(color, type_set, default))
    w("fonts.css", font_css([d["display"], d["sans"], d["mono"]]))
    w("tailwind.theme.js", tailwind_js())
    shutil.copy(ROOT / "ui" / "ui.css", os.path.join(out, "ui.css"))
    w(
        "demo.html",
        (ROOT / "ui" / "demo.html")
        .read_text(encoding="utf-8")
        .replace("{NAME}", tok["name"])
        .replace("{DEFAULT}", default)
        .replace("{TYPE}", d["label"]),
    )
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Export a colour theme as CSS variables, fonts, a Tailwind theme and a UI demo."
    )
    ap.add_argument("color", choices=colors())
    ap.add_argument("out")
    ap.add_argument("--type", default=None, choices=list(SYS["type_sets"]))
    ap.add_argument("--default", default="dark", choices=["dark", "light"])
    a = ap.parse_args()
    print(export(a.color, a.out, a.type, a.default))
