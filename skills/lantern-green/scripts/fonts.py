"""fonts: list, add and verify font packs (languages and type sets).

    python fonts.py list                      what each pack covers and whether it is installed
    python fonts.py add europe arabic         add packs: core, sets, europe, cyrillic-greek, arabic, or all
    python fonts.py verify                    check every installed font file against its recorded hash

The master skill ships with every pack. Colour skills ship with `core` (the Latin letters of the Classic, Modern
and Editorial type sets) and fetch the rest on request. Downloads come only from the addresses pinned in
assets/fonts/manifest.json (jsDelivr's mirror of the Fontsource packages), over https, and a file is kept only if
its SHA-256 hash matches the manifest. All fonts are under the SIL Open Font Licence (assets/fonts/LICENSES.txt).
"""

import hashlib
import os
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import FONT_DIR, FONT_MANIFEST, font_installed, font_packs

HOST = "cdn.jsdelivr.net"
LIMIT = 2_000_000  # no single font file comes near this


def sha(b):
    return hashlib.sha256(b).hexdigest()


def fetch(entry):
    u = urlparse(entry["url"])
    if u.scheme != "https" or u.hostname != HOST:
        raise ValueError(f"refusing {entry['url']}: fonts come only from https://{HOST}")
    with urlopen(Request(entry["url"], headers={"User-Agent": "lantern-fonts"}), timeout=30) as r:
        data = r.read(LIMIT + 1)
    if len(data) > LIMIT or sha(data) != entry["sha256"]:
        raise ValueError(f"{entry['file']}: the download does not match the recorded hash; nothing was written")
    tmp = FONT_DIR / (entry["file"] + ".woff2.part")
    tmp.write_bytes(data)
    os.replace(tmp, FONT_DIR / (entry["file"] + ".woff2"))


def add(packs):
    known = FONT_MANIFEST["packs"]
    packs = list(known) if packs == ["all"] else packs
    bad = [p for p in packs if p not in known]
    if bad:
        sys.exit(f"unknown pack {bad}; choose from: {', '.join(known)} or all")
    todo = [f for f in FONT_MANIFEST["files"] if f["pack"] in packs and not font_installed(f)]
    for i, f in enumerate(todo, 1):
        fetch(f)
        print(f"[{i}/{len(todo)}] {f['file']}")
    print(f"added {len(todo)} file(s); {', '.join(packs)} installed")


def verify():
    bad = [
        f["file"]
        for f in FONT_MANIFEST["files"]
        if font_installed(f) and sha((FONT_DIR / (f["file"] + ".woff2")).read_bytes()) != f["sha256"]
    ]
    for name in bad:
        print("MISMATCH", name)
    print(
        "all installed font files match the manifest"
        if not bad
        else f"{len(bad)} file(s) differ; delete them and run add again"
    )
    return 1 if bad else 0


def show():
    for pack, (have, total) in font_packs().items():
        state = "installed" if have == total else ("partly installed" if have else "not installed")
        print(f"{pack:15} {state:17} {FONT_MANIFEST['packs'][pack]}")


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:] or ["list"]
    if cmd == "list":
        show()
    elif cmd == "add" and rest:
        add(rest)
    elif cmd == "verify":
        sys.exit(verify())
    else:
        sys.exit(__doc__)
