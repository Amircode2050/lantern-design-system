"""new_theme: build a complete colour theme (dark + light) from one brand colour.

    python new_theme.py green "#1B4D3E" --preview out                  amber light (default)
    python new_theme.py red "#7A1F2B" --accent "#D8B47A"                a champagne light
    python new_theme.py gold "#D4AF37" --accent core --ground-chroma 0.22 --deep 0.6
                                                                        near-black ground, the gold is the light
    python new_theme.py white "#FAF8F2" --harmony monochrome --default-variant light
    python new_theme.py red_crimson "#A4161A" --from red                same recipe, another shade

The lightness and chroma structure comes from the reference theme (scripts/reference_theme.json), moved to the
new hue; then every text and flow colour is nudged until it passes the contrast rules. The recipe is stored in the
theme, so `--from` can rebuild any shade the same way.

--harmony          warm (amber, default) | complementary | analogous | monochrome (a pale tint of the core: black, white, grey)
--accent HEX|core  the colour of the one light; overrides --harmony. `core` makes the brand colour itself the light
--ground-chroma K  multiplies the colour of ground and structure (0.2 = nearly neutral, for gold, orange, yellow)
--deep K           multiplies the lightness of the dark grounds (below 1 = darker; about 0.55 for near-black)
--shades           alternative cores offered for this family, as name=#hex pairs
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import ROOT, SYS, colors, contrast, from_oklch, hexmix, to_oklch

REF = json.loads((ROOT / "scripts" / "reference_theme.json").read_text(encoding="utf-8"))
STRUCT = [
    "G600",
    "G700",
    "G800",
    "G900",
    "G950",
    "VIGN",
    "IN900",
    "IN800",
    "IN700",
    "IN600",
    "IN500",
    "V500",
    "V400",
    "V300",
    "L300",
    "L200",
    "L100",
    "MIST",
    "INK",
    "T1",
    "T2",
    "T3",
]
ACCENT = ["W100", "W200", "W300", "W400", "ROSE3", "ROSE5", "COFFEE"]
SUPPORT = ["B200", "B400", "B600"]
FX_STRUCT = ["LIT", "METALV", "METALH", "COOL", "STAR", "TWINKLE", "HALO", "CABLE", "CABLE_DARK"]
FX_ACCENT = ["WARMWIN", "GLOW", "SIGHT"]
STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]
NAMES = {
    "G600": "ground-600",
    "G700": "ground-700",
    "G800": "ground-800",
    "G900": "ground-900",
    "G950": "ground-950",
    "VIGN": "vignette",
    "IN900": "deep-900",
    "IN800": "deep-800",
    "IN700": "deep-700",
    "IN600": "deep-600",
    "IN500": "deep-500",
    "V500": "mid-500",
    "V400": "mid-400",
    "V300": "mid-300",
    "L300": "pale-300",
    "L200": "pale-200",
    "L100": "pale-100",
    "MIST": "mist",
    "INK": "ink",
    "T1": "text-primary",
    "T2": "text-secondary",
    "T3": "text-muted",
    "W100": "accent-100",
    "W200": "accent-200",
    "W300": "accent-300",
    "W400": "accent-400",
    "ROSE3": "accent-mid",
    "ROSE5": "accent-dark",
    "COFFEE": "accent-deep",
    "B200": "support-200",
    "B400": "support-400",
    "B600": "support-600",
    "WATER": "water",
    "CORE": "core",
    **{f"CORE_{s}": f"core-{s}" for s in STEPS},
}


def rehue(h, hue, cscale=1.0, lscale=1.0):
    L, Cc, _ = to_oklch(h)
    return from_oklch(L * lscale, Cc * cscale, hue)


def ramp(core):
    """11 shades of the core, 50 (lightest) to 950 (darkest); the core itself sits at the step nearest its own lightness."""
    Ls = [0.97, 0.93, 0.87, 0.79, 0.68, 0.57, 0.47, 0.39, 0.31, 0.24, 0.17]
    Cp = [0.08, 0.19, 0.34, 0.55, 0.81, 1, 0.92, 0.77, 0.6, 0.45, 0.32]
    L, Cc, H = to_oklch(core)
    out = [from_oklch(l, Cc * k, H) for l, k in zip(Ls, Cp)]
    out[min(range(11), key=lambda j: abs(Ls[j] - L))] = core.lower()
    return {f"CORE_{s}": c for s, c in zip(STEPS, out)}


def fit(fg, grounds, target, lighter):
    """Nudge the lightness of fg until it reaches `target` contrast on every ground."""
    L, Cc, H = to_oklch(fg)
    for _ in range(400):
        c = from_oklch(L, Cc, H)
        if all(contrast(c, g) >= target for g in grounds):
            return c
        L += 0.004 if lighter else -0.004
    return c


def build(
    name,
    core,
    harmony="warm",
    accent=None,
    ground_chroma=1.0,
    deep=1.0,
    type_set=None,
    default_variant="dark",
    shades=None,
    label=None,
):
    core = core.lower()
    cL, cC, cH = to_oklch(core)
    rC = to_oklch(REF["core"])[1]
    ref_w = to_oklch(REF["variants"]["dark"]["colors"]["W300"])
    k_struct = min(1.15, cC / rC) * ground_chroma
    if accent:
        aL, aC, aH = to_oklch(core if accent == "core" else accent)
        a_hue, a_c = aH, min(1.25, aC / ref_w[1])
        harmony = "custom"
    else:
        a_hue, a_c = {
            "warm": (ref_w[2], 1.0),
            "complementary": ((cH + 180) % 360, 1.0),
            "analogous": ((cH + 40) % 360, 1.0),
            "monochrome": (cH, 0.3 * min(1.0, cC / rC)),
        }[harmony]
    near = lambda a, b: min(abs(a - b), 360 - abs(a - b)) < 40
    s_hue = 250 if near(cH, 200) else 200
    s_c = 1.0
    if harmony == "monochrome":
        s_hue, s_c = cH, 0.35 * min(1.0, cC / rC)
    verbatim = harmony == "warm"
    out = {
        "name": name.replace("_", " ").title(),
        "core": core,
        "harmony": harmony,
        "accent_label": label
        or {
            "warm": "amber light",
            "monochrome": "white light, ink only",
            "complementary": "complementary light",
            "analogous": "analogous light",
        }.get(harmony, "custom light"),
        "default_type": type_set or SYS["default_type_set"],
        "default_variant": default_variant,
        "shades": shades or [],
        "recipe": {
            "harmony": None if accent else harmony,
            "accent": accent,
            "ground_chroma": ground_chroma,
            "deep": deep,
            "type": type_set,
            "default_variant": default_variant,
            "label": label,
        },
        "names": NAMES,
        "variants": {},
    }
    for variant in ("dark", "light"):
        rc, rf = REF["variants"][variant]["colors"], REF["variants"][variant]["fx"]
        light = variant == "light"
        c = {k: rehue(rc[k], cH, k_struct, deep if (not light and k in STRUCT[:11]) else 1.0) for k in STRUCT}
        c.update({k: rc[k] if verbatim else rehue(rc[k], a_hue, a_c) for k in ACCENT})
        c.update({k: rehue(rc[k], s_hue, s_c) for k in SUPPORT})
        if light:
            c["MIST"] = "#ffffff"
            c["G600"] = "#ffffff" if cC > 0.02 or cL < 0.5 else from_oklch(0.985, cC * 1.5, cH)
        c["CORE"] = core
        c.update(ramp(core))
        g = [c[k] for k in ("G600", "G700", "G800", "G900", "G950")]
        if light:
            for k, t in (
                ("T1", 7),
                ("T2", 7),
                ("T3", 4.5),
                ("W300", 4.5),
                ("ROSE3", 4.5),
                ("L100", 3),
                ("B200", 3),
                ("L200", 3),
            ):
                c[k] = fit(c[k], g, t, lighter=False)
        else:
            c["T1"] = fit(c["T1"], g, 7, True)
            c["T2"] = fit(c["T2"], g, 4.5, True)
            c["T3"] = fit(c["T3"], g[1:], 4.5, True)
            for k in ("ROSE3", "L100", "B200", "W300"):
                c[k] = fit(c[k], g, 4.5, True)
        c["WATER"] = c["B200"]
        room = c["G800"]
        c.update(
            ROOM=room,
            ROOM_COOL=hexmix(room, c["B400"], 0.14),
            ROOM_WARM=hexmix(room, c["W200"] if light else c["ROSE5"], 0.3 if light else 0.16),
            ROOM_DEEP=c["G950"] if light else c["IN700"],
            ROOM_BILGE=c["L300"] if light else c["IN900"],
            OK=rc["OK"],
            WARN=c["W300"],
            ERR=rc["ERR"],
        )
        c["SERIES"] = [c["L100"], c["W300"], c["B200"], c["ROSE3"], c["T2"]]
        c["ON_CORE"] = max(("#ffffff", c["INK"]), key=lambda x: contrast(x, core))
        c["CORE_FILL"] = core
        if (
            contrast(c["ON_CORE"], core) < 4.5
        ):  # e.g. burnt orange: buttons use the nearest ramp step that carries white text
            c["CORE_FILL"] = next(
                (c[f"CORE_{s}"] for s in STEPS if contrast("#ffffff", c[f"CORE_{s}"]) >= 4.5), c["CORE_950"]
            )
            c["ON_CORE"] = "#ffffff"
        fx = {k: v for k, v in rf.items() if not isinstance(v, (list, str)) or k == "GLOW_BLEND"}
        for k in FX_STRUCT:
            fx[k] = [rehue(x, cH, k_struct) for x in rf[k]] if isinstance(rf[k], list) else rehue(rf[k], cH, k_struct)
        for k in FX_ACCENT:
            fx[k] = (
                rf[k]
                if verbatim
                else ([rehue(x, a_hue, a_c) for x in rf[k]] if isinstance(rf[k], list) else rehue(rf[k], a_hue, a_c))
            )
        fx["GLOW"] = list(fx["GLOW"])
        fx["LIT"] = list(fx["LIT"])
        fx["LIT"][0] = "#ffffff"
        if light:
            fx["LIT"][1] = fx["GLOW"][3] = "#ffffff"
            fx["SIGHT"] = c["W300"]
        else:
            fx["GLOW"][3] = c["L300"]
        out["variants"][variant] = {"colors": c, "fx": fx}
    return out


HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
NAME = re.compile(r"^[a-z][a-z0-9_]{0,40}$")


def _hex(v, what):
    v = v if v.startswith("#") else "#" + v
    if not HEX.match(v):
        sys.exit(f"{what} must be a 6-digit hex colour such as #3366FF (got {v!r})")
    return v.lower()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build a colour theme from one brand colour.")
    ap.add_argument("name")
    ap.add_argument("core", help="brand colour as #rrggbb")
    ap.add_argument(
        "--from", dest="src", help="copy the recipe (accent, ground, depth, type, shades) of an installed theme"
    )
    ap.add_argument("--harmony", default=None, choices=["warm", "complementary", "analogous", "monochrome"])
    ap.add_argument("--accent", default=None, help="#rrggbb or 'core'")
    ap.add_argument("--ground-chroma", type=float, default=None)
    ap.add_argument("--deep", type=float, default=None)
    ap.add_argument("--type", default=None, choices=list(SYS["type_sets"]))
    ap.add_argument("--default-variant", default=None, choices=["dark", "light"])
    ap.add_argument("--label", default=None, help="how the light is described in the picker, e.g. 'champagne light'")
    ap.add_argument("--shades", nargs="*", default=None, metavar="NAME=#HEX")
    ap.add_argument("--preview", metavar="DIR", help="render the component sheet for both variants into DIR")
    ap.add_argument("--force", action="store_true", help="overwrite an existing theme")
    a = ap.parse_args(argv)
    name = a.name.lower()
    core = _hex(a.core, "core")
    if not NAME.match(name):
        sys.exit("name must start with a letter and use only a-z, 0-9 and _ (for example red_crimson)")
    if a.accent and a.accent != "core":
        a.accent = _hex(a.accent, "--accent")
    r = dict(harmony="warm", accent=None, ground_chroma=1.0, deep=1.0, type=None, default_variant="dark", label=None)
    shades = []
    if a.src:
        if a.src not in colors():
            sys.exit(f"--from: no installed theme '{a.src}'; installed: {', '.join(colors())}")
        src = json.loads((ROOT / "themes" / f"{a.src}.json").read_text(encoding="utf-8"))
        r.update({k: v for k, v in (src.get("recipe") or {}).items() if v is not None})
        shades = src.get("shades", [])
    for k, v in (
        ("harmony", a.harmony),
        ("accent", a.accent),
        ("ground_chroma", a.ground_chroma),
        ("deep", a.deep),
        ("type", a.type),
        ("default_variant", a.default_variant),
        ("label", a.label),
    ):
        if v is not None:
            r[k] = v
    if a.shades is not None:
        if any("=" not in s for s in a.shades):
            sys.exit("--shades takes Name=#hex pairs, for example Burgundy=#800020")
        shades = [
            {"name": s.split("=", 1)[0].strip(), "core": _hex(s.split("=", 1)[1].strip(), "--shades")} for s in a.shades
        ]
    dest = ROOT / "themes" / f"{name}.json"
    if dest.exists() and not a.force:
        sys.exit(f"theme '{name}' already exists; pass --force to overwrite it")
    dest.write_text(
        json.dumps(
            build(
                name,
                core,
                r["harmony"],
                r["accent"],
                r["ground_chroma"],
                r["deep"],
                r["type"],
                r["default_variant"],
                shades,
                r["label"],
            ),
            indent=1,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    from kit import check_tokens

    bad = check_tokens(name)
    print(f"wrote {dest}" + ("" if not bad else "\ncontrast failures:\n  " + "\n  ".join(bad)))
    if a.preview:
        import examples
        from kit import render, set_theme

        os.makedirs(a.preview, exist_ok=True)
        for v in ("dark", "light"):
            set_theme(v, name)
            print(render(examples.sheet(), os.path.join(a.preview, f"{name}_sheet_{v}.png"), scale=1))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
