"""Prepare a release locally: verify, build the zips, and tag. Nothing is pushed.

    python build/release.py            uses VERSION from build/build.py
    python build/release.py --dry-run  run every check, create no tags

Tags: v<VERSION> for the repo, and <plugin>--v<VERSION> for each plugin (the form plugin managers look for).
Afterwards push and publish yourself:
    git push origin main --tags
    gh release create v<VERSION> dist/*.zip dist/*.pptx --title "Lantern <VERSION>" --notes-file <notes>
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def run(*cmd, check=True):
    return subprocess.run(cmd, cwd=REPO, check=check, capture_output=True, text=True).stdout.strip()


def main():
    ap = argparse.ArgumentParser(description="Verify, build and tag a release locally.")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    version = re.search(r'^VERSION = "([^"]+)"', (REPO / "build" / "build.py").read_text(encoding="utf-8"), re.M).group(
        1
    )
    if f"## {version}" not in (REPO / "CHANGELOG.md").read_text(encoding="utf-8"):
        sys.exit(f"CHANGELOG.md has no '## {version}' section")
    if run("git", "status", "--porcelain"):
        sys.exit("the working tree is not clean; commit or stash first")
    if version_tag := run("git", "tag", "--list", f"v{version}"):
        sys.exit(f"tag {version_tag} already exists; bump VERSION in build/build.py")

    subprocess.run([sys.executable, "build/check.py"], cwd=REPO, check=True)
    subprocess.run([sys.executable, "build/build.py", "--skip-render"], cwd=REPO, check=True)
    if run("git", "status", "--porcelain"):
        sys.exit("the build changed tracked files; commit the result and run again")

    subprocess.run([sys.executable, "src/scripts/deck.py", "all", "--out", "dist"], cwd=REPO, check=True)
    plugins = sorted(p.name for p in (REPO / "skills").iterdir() if p.is_dir())
    tags = [f"v{version}"] + [f"{p}--v{version}" for p in plugins]
    if a.dry_run:
        print("dry run: would create", ", ".join(tags))
        return
    for t in tags:
        run("git", "tag", "-a", t, "-m", f"Lantern {version}" if t.startswith("v") else f"{t.split('--')[0]} {version}")
    print(f"tagged {len(tags)}: {tags[0]} and one per plugin; zips and slide templates are in dist/")
    print("next: git push origin main --tags, then attach dist/*.zip and dist/*.pptx to the GitHub release")


if __name__ == "__main__":
    main()
