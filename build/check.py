"""Repository checks that need no browser. Exit code 1 if anything fails.

    python build/check.py

- every theme passes the contrast rules
- every plugin, marketplace entry and SKILL.md agree on names
- every SKILL.md has a description of at most 1024 characters
- every generated skill carries the same engine as src/
- the exported UI tokens keep buttons, text and links readable in every theme and variant
"""

import filecmp
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src" / "scripts"))
import export  # noqa: E402
from kit import check_tokens, colors, contrast  # noqa: E402


def frontmatter(md):
    m = re.match(r"---\n(.*?)\n---\n", md, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip().strip('"')
    return out


def same_tree(a, b):
    cmp = filecmp.dircmp(a, b, ignore=["__pycache__"])
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False
    return all(same_tree(Path(a) / d, Path(b) / d) for d in cmp.common_dirs)


def ui_contrast():
    out = []
    for color in colors():
        css = export.tokens_css(color, "classic", "dark")
        for variant in ("dark", "light"):
            block = re.search(rf'\[data-theme="{variant}"\] \{{(.*?)\}}', css, re.S).group(1)
            v = dict(re.findall(r"--([a-z0-9-]+): (#[0-9a-f]{6});", block))
            rules = (
                ("primary", "surface", 3),
                ("on-primary", "primary", 4.5),
                ("text", "surface", 7),
                ("link", "surface", 4.5),
            )
            out += [
                f"{color} {variant} UI: {a} on {b} = {contrast(v[a], v[b]):.2f}"
                for a, b, need in rules
                if contrast(v[a], v[b]) < need
            ]
    return out


def main():
    problems = list(check_tokens()) + ui_contrast()

    market = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    listed = {p["name"]: p for p in market["plugins"]}
    on_disk = {p.name for p in (REPO / "plugins").iterdir() if p.is_dir()}
    if set(listed) != on_disk:
        problems.append(f"marketplace lists {sorted(listed)} but plugins/ holds {sorted(on_disk)}")

    for name in sorted(on_disk):
        root = REPO / "plugins" / name
        manifest = json.loads((root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        if manifest.get("name") != name:
            problems.append(f"{name}: plugin.json name is {manifest.get('name')!r}")
        if name in listed and listed[name].get("version") != manifest.get("version"):
            problems.append(f"{name}: marketplace and plugin.json versions differ")
        skill = root / "skills" / name
        fm = frontmatter((skill / "SKILL.md").read_text(encoding="utf-8"))
        if fm.get("name") != name:
            problems.append(f"{name}: SKILL.md name is {fm.get('name')!r}")
        if not 0 < len(fm.get("description", "")) <= 1024:
            problems.append(f"{name}: description length {len(fm.get('description', ''))}")
        for part in ("scripts", "ui"):
            if not same_tree(REPO / "src" / part, skill / part):
                problems.append(f"{name}: {part}/ differs from src/{part}; run python build/build.py --skip-render")

    for p in problems:
        print("FAIL", p)
    print(f"{len(on_disk)} plugins checked, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
