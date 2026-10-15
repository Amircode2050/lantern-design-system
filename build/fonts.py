"""Fetch the bundled fonts and write their manifest (maintainers only; users run src/scripts/fonts.py).

    python build/fonts.py            download any missing file, verify every file, rewrite the manifest
    python build/fonts.py --measure  also re-measure each family's average advance in a browser

Every font comes from its Fontsource package (the Google Fonts files, packaged per subset) at a pinned version,
through jsDelivr's npm mirror. Writes src/assets/fonts/<file>.woff2, manifest.json (file, family, weight, style,
subset, pack, url, sha256, unicode range), LICENSES.txt, and the family stacks in src/system.json.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen

REPO = Path(__file__).resolve().parent.parent
FONTS = REPO / "src" / "assets" / "fonts"
CDN = "https://cdn.jsdelivr.net/npm/@fontsource/{pkg}@{ver}/{path}"

# family: package, version, kind (serif, sans, mono), (weight, style) pairs, pack for its Latin files
FAMILIES = {
    "PT Serif": ("pt-serif", "5.3.0", "serif", [("400", "normal"), ("400", "italic"), ("700", "normal")], "core"),
    "Fraunces": ("fraunces", "5.3.0", "serif", [("400", "normal"), ("400", "italic"), ("600", "normal")], "core"),
    "Space Grotesk": ("space-grotesk", "5.3.0", "sans", [("400", "normal"), ("500", "normal")], "core"),
    "Inter": ("inter", "5.3.0", "sans", [("400", "normal"), ("500", "normal"), ("600", "normal")], "core"),
    "Source Sans 3": (
        "source-sans-3",
        "5.3.1",
        "sans",
        [("400", "normal"), ("500", "normal"), ("600", "normal")],
        "core",
    ),
    "JetBrains Mono": ("jetbrains-mono", "5.3.0", "mono", [("400", "normal"), ("500", "normal")], "core"),
    "IBM Plex Serif": (
        "ibm-plex-serif",
        "5.3.0",
        "serif",
        [("400", "normal"), ("400", "italic"), ("600", "normal")],
        "sets",
    ),
    "IBM Plex Sans": (
        "ibm-plex-sans",
        "5.3.0",
        "sans",
        [("400", "normal"), ("500", "normal"), ("600", "normal")],
        "sets",
    ),
    "IBM Plex Mono": ("ibm-plex-mono", "5.3.0", "mono", [("400", "normal"), ("500", "normal")], "sets"),
    "DM Serif Display": ("dm-serif-display", "5.3.0", "serif", [("400", "normal"), ("400", "italic")], "sets"),
    "DM Sans": ("dm-sans", "5.3.0", "sans", [("400", "normal"), ("500", "normal"), ("600", "normal")], "sets"),
    "EB Garamond": ("eb-garamond", "5.3.0", "serif", [("400", "normal"), ("400", "italic"), ("600", "normal")], "sets"),
    "Inter Tight": ("inter-tight", "5.3.0", "sans", [("400", "normal"), ("500", "normal"), ("600", "normal")], "sets"),
    "Vazirmatn": ("vazirmatn", "5.3.0", "sans", [("400", "normal"), ("500", "normal"), ("600", "normal")], "arabic"),
}
# subset: pack. Latin goes to the family's own pack; Vazirmatn contributes only its Arabic letters.
SUBSETS = {
    "latin": None,
    "latin-ext": "europe",
    "vietnamese": "europe",
    "cyrillic": "cyrillic-greek",
    "cyrillic-ext": "cyrillic-greek",
    "greek": "cyrillic-greek",
    "greek-ext": "cyrillic-greek",
    "arabic": "arabic",
}
PACKS = {
    "core": "Latin letters for the Classic, Modern and Editorial type sets (bundled in every skill)",
    "sets": "Latin letters for the Technical, Geometric, Garamond and Swiss type sets",
    "europe": "accented Latin for Central and Eastern European languages, Turkish and Vietnamese",
    "cyrillic-greek": "Cyrillic (Russian, Ukrainian, Bulgarian, Serbian and more) and Greek",
    "arabic": "Arabic script (Persian, Arabic, Urdu), set right to left",
}
FALLBACK = {  # where a family lacks a script, these fill in, in order
    "serif": ["PT Serif", "Inter", "Vazirmatn"],
    "sans": ["Inter", "Vazirmatn"],
    "mono": ["JetBrains Mono", "Inter", "Vazirmatn"],
}
GENERIC = {"serif": "Georgia, serif", "sans": "'Helvetica Neue', Arial, sans-serif", "mono": "Consolas, monospace"}


def get(url):
    with urlopen(Request(url, headers={"User-Agent": "lantern-build"}), timeout=30) as r:
        return r.read()


def quote(f):
    return f"'{f}'" if " " in f or f[0].isdigit() else f


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--measure", action="store_true")
    a = ap.parse_args()
    FONTS.mkdir(parents=True, exist_ok=True)
    sysj = json.loads((REPO / "src" / "system.json").read_text(encoding="utf-8"))
    files, licences, families = [], [], {}
    for fam, (pkg, ver, kind, styles, own_pack) in FAMILIES.items():
        meta = json.loads(get(CDN.format(pkg=pkg, ver=ver, path="metadata.json")))
        ranges = json.loads(get(CDN.format(pkg=pkg, ver=ver, path="unicode.json")))
        licences.append(f"===== fontsource-{pkg}-{ver}\n" + get(CDN.format(pkg=pkg, ver=ver, path="LICENSE")).decode())
        for subset, pack in SUBSETS.items():
            if subset not in meta["subsets"] or (fam == "Vazirmatn" and subset != "arabic"):
                continue
            for w, st in styles:
                if st not in meta["styles"]:
                    continue
                name = f"{pkg}-{subset}-{w}-{st}"
                url = CDN.format(pkg=pkg, ver=ver, path=f"files/{name}.woff2")
                path = FONTS / f"{name}.woff2"
                if not path.exists():
                    path.write_bytes(get(url))
                    print("fetched", name)
                files.append(
                    dict(
                        file=name,
                        family=fam,
                        weight=w,
                        style=st,
                        subset=subset,
                        pack=pack or own_pack,
                        url=url,
                        sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                        range=ranges[subset].replace(" ", ""),
                    )
                )
        chain = [fam] + [f for f in FALLBACK[kind] if f != fam]
        old = sysj["fonts"].get(fam, {})
        families[fam] = {
            "stack": ", ".join(quote(f) for f in chain) + ", " + GENERIC[kind],
            "adv": old.get("adv", 0.53),
            "kind": kind,
            "tuned": "adv" in old,
        }
    if a.measure:
        measure(families, files)
    keep = {f["file"] + ".woff2" for f in files} | {"manifest.json", "LICENSES.txt", "README.md"}
    stray = [p.name for p in FONTS.iterdir() if p.name not in keep]
    if stray:
        sys.exit(f"files in {FONTS} that the manifest does not list: {stray}")
    manifest = {"source": "Fontsource packages via jsDelivr; SIL Open Font License 1.1", "packs": PACKS, "files": files}
    (FONTS / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8", newline="\n")
    (FONTS / "LICENSES.txt").write_text("\n\n".join(licences), encoding="utf-8", newline="\n")
    sysj["fonts"] = families
    (REPO / "src" / "system.json").write_text(json.dumps(sysj, indent=1) + "\n", encoding="utf-8", newline="\n")
    size = sum((FONTS / (f["file"] + ".woff2")).stat().st_size for f in files)
    by_pack = {}
    for f in files:
        by_pack[f["pack"]] = by_pack.get(f["pack"], 0) + (FONTS / (f["file"] + ".woff2")).stat().st_size
    print(f"{len(files)} files, {size / 1e6:.2f} MB: " + ", ".join(f"{k} {v / 1e6:.2f} MB" for k, v in by_pack.items()))


def measure(families, files):
    """Average advance per em of each family over a pangram, measured in Chromium (used to estimate text widths)."""
    import base64

    from playwright.sync_api import sync_playwright

    sample = "The quick brown fox jumps over the lazy dog, 1234567890. How does a factory run?"
    arabic = "چطور یک کارخانه کار می‌کند؟ هر اتاق به اتاق بعدی کمک می‌کند."
    css = "".join(
        f"@font-face{{font-family:'{f['family']}';font-weight:{f['weight']};font-style:{f['style']};unicode-range:{f['range']};"
        f"src:url(data:font/woff2;base64,{base64.b64encode((FONTS / (f['file'] + '.woff2')).read_bytes()).decode()})}}"
        for f in files
        if f["weight"] == "400" and f["style"] == "normal" and f["subset"] in ("latin", "arabic")
    )
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.set_content(f'<style>{css}</style><span id=s style="white-space:nowrap"></span>')
        for fam, spec in families.items():
            text = arabic if fam == "Vazirmatn" else sample
            w = pg.evaluate(
                """async ([fam, t]) => { await document.fonts.load(`400 100px "${fam}"`, t); const s = document.getElementById('s');
                s.style.font = `400 100px "${fam}"`; s.textContent = t; return s.getBoundingClientRect().width }""",
                [fam, text],
            )
            if not spec.get("tuned"):  # tuned values keep their layouts; new ones get the same ~8% margin
                spec["adv"] = 0.6 if spec["kind"] == "mono" else round(1.08 * w / 100 / len(text), 3)
        b.close()


if __name__ == "__main__":
    main()
