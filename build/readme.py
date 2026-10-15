"""Write README.md from build/templates/README.md and the theme files, so every colour and hex value is exact.

python build/readme.py
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "build"))
from build import COLORS, VERSION  # noqa: E402

ORDER = ["black", "white", "blue", "purple", "green", "red", "gray", "teal", "gold", "orange", "cyan", "rose"]
BEST_FOR = {
    "black": "keynotes, launches and premium reports",
    "white": "print, documents and bright rooms",
    "blue": "technology, science and finance",
    "purple": "ideas, research and storytelling",
    "green": "sustainability, health and growth",
    "red": "strategy, culture and history",
    "gray": "engineering, operations and data",
    "teal": "healthcare, water and calm explainers",
    "gold": "awards, finance and luxury brands",
    "orange": "energy, product launches and bold talks",
    "cyan": "digital products, cloud and fresh decks",
    "rose": "culture, wellbeing and consumer brands",
}
STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]


def theme(c):
    return json.loads((REPO / "src" / "themes" / f"{c}.json").read_text(encoding="utf-8"))


def shade_name(t):
    return next((s["name"] for s in t.get("shades", []) if s["core"] == t["core"].lower()), t["name"])


def type_label(t):
    return t.get("default_type", "classic").capitalize()


def colour_table():
    rows = []
    for c in ORDER:
        t = theme(c)
        rows.append(
            f"| [{t['name']}](#{c}) | {shade_name(t)} `{t['core'].upper()}` | {t.get('accent_label', 'amber light')} "
            f"| {type_label(t)} | {t.get('default_variant', 'dark')} | {BEST_FOR[c]} |"
        )
    return "\n".join(rows)


def skill_table():
    return "\n".join(f"| `lantern-{c}` | {theme(c)['name']} only: {COLORS[c]['built']}. |" for c in ORDER)


def colour_guide():
    out = []
    for c in ORDER:
        t = theme(c)
        d, l = t["variants"]["dark"]["colors"], t["variants"]["light"]["colors"]
        others = [s for s in t.get("shades", []) if s["core"] != t["core"].lower()]
        alt = ", ".join(f"{s['name']} `{s['core'].upper()}`" for s in others) or "none"
        aliases = ", ".join(COLORS[c]["aliases"])
        ramp = " ".join("`" + d[f"CORE_{s}"] + "`" for s in STEPS)
        out.append(
            f"""### {t["name"]}

<p align="center"><img src="docs/images/colors/{c}.jpg" alt="{t["name"]} in dark and light, with type sets and shade options" width="100%"></p>
<p align="center"><img src="docs/images/ramps/{c}.png" alt="{t["name"]} shade ramp from 50 to 950" width="100%"></p>

{COLORS[c]["built"][0].upper() + COLORS[c]["built"][1:]}. Best for {BEST_FOR[c]}.

- **Skill:** `lantern-{c}`, or `lantern` and pick {t["name"]}. It also answers to: {aliases}.
- **Defaults:** {t.get("default_variant", "dark")} variant, {type_label(t)} type set.
- **Other shades:** {alt}.

<details>
<summary>Key tokens</summary>

| Token | Dark | Light |
|---|---|---|
| Ground (centre to edge) | `{d["G600"]}` `{d["G800"]}` `{d["G950"]}` | `{l["G600"]}` `{l["G800"]}` `{l["G950"]}` |
| Text primary / secondary | `{d["T1"]}` / `{d["T2"]}` | `{l["T1"]}` / `{l["T2"]}` |
| The light (accent text) | `{d["W300"]}` | `{l["W300"]}` |
| Information flows | `{d["L100"]}` | `{l["L100"]}` |
| Support (water) | `{d["B200"]}` | `{l["B200"]}` |
| Button fill / text | `{d["CORE_FILL"]}` / `{d["ON_CORE"]}` | `{l["CORE_FILL"]}` / `{l["ON_CORE"]}` |
| Shade ramp 50 to 950 | {ramp} | same |

</details>
"""
        )
    return "\n".join(out)


def scene_table():
    """The library as a three-column grid of thumbnails (rendered by build/site.py)."""
    sys.path.insert(0, str(REPO / "src" / "scripts"))
    import scenes

    cells = [
        f'<td width="33%" valign="top"><img src="docs/site/lib/{n}.jpg" alt="{sc["alt"]}" width="100%"><br>'
        f"<b>{' '.join(sc['title'])}</b><br><code>{n}</code></td>"
        for n, sc in scenes.SCENES.items()
    ]
    rows = ["<tr>" + "".join(cells[i : i + 3]) + "</tr>" for i in range(0, len(cells), 3)]
    return "<table>\n" + "\n".join(rows) + "\n</table>", len(cells)


def main():
    tpl = (REPO / "build" / "templates" / "README.md").read_text(encoding="utf-8")
    for key, value in (
        ("version", VERSION),
        ("colour_table", colour_table()),
        ("skill_table", skill_table()),
        ("colour_guide", colour_guide()),
        ("scene_table", scene_table()[0]),
        ("scene_count", str(scene_table()[1])),
    ):
        tpl = tpl.replace("{{" + key + "}}", value)
    left = re.findall(r"\{\{\w+\}\}", tpl)
    if left:
        sys.exit(f"unfilled: {left}")
    (REPO / "README.md").write_text(tpl, encoding="utf-8", newline="\n")
    print(f"README.md written ({len(tpl.splitlines())} lines)")


if __name__ == "__main__":
    main()
