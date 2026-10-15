# Security

## What the skills do on your machine

- **Render locally.** Scenes are SVG strings drawn by a headless Chromium (Playwright). Every network request from that page is blocked, so rendering never fetches anything.
- **Write only where you ask.** Scripts write images, frames, slide files and exports to the paths you pass them. Theme names are restricted to `a-z`, `0-9` and `_` (a name such as `../x` is refused), so a theme cannot be written outside the `themes/` folder.
- **Check every input.** Colours must be six-digit hex values; scene, colour, format and type-set names must be ones that exist. Anything else stops with a message before a file is written.
- **Run one external program.** GIF and MP4 output calls `ffmpeg` with an argument list (no shell).
- **Need no accounts or keys.** There is no telemetry and there are no credentials or environment variables. The only download is the browser you install yourself with `python -m playwright install chromium`.
- **Use the network in two places only, both on your request.** `brand.py`, given a web address, reads that page and up to five of its stylesheets to find the brand's colours. It:
  - accepts `http` and `https` only, and only addresses that resolve to the public internet, so a page cannot point it at your local network or at files on disk;
  - checks every redirect the same way;
  - waits at most 10 seconds and reads at most 2 MB per file, a limit that also applies after unpacking compressed responses;
  - sends nothing but the requests, and never runs what it downloads.

  `python scripts/brand.py --selftest` confirms that local, private and non-web addresses are refused.
- **Download fonts only on request, and only known files.** `scripts/fonts.py add <pack>` fetches font files listed in `assets/fonts/manifest.json`, from `https://cdn.jsdelivr.net` only, and writes a file only if its SHA-256 hash matches the manifest. `fonts.py verify` re-checks every installed font. The master skill ships with every pack, so it never needs this.

Every other script works offline.

## What the repository does

- Continuous integration runs with read-only permissions, and every third-party action is pinned to an exact commit. Dependabot proposes updates to those pins and to the Python requirements.
- The playground page in `docs/` is static: no cookies, no analytics, no external scripts or fonts. It remembers your last colour choice in your own browser's local storage only.

## Expected scanner findings

Static skill scanners may flag:

| Finding | Why it appears |
|---|---|
| Referenced file not fully inspected | `SKILL.md` points to bundled images and scripts that a text scanner cannot read. |
| Subprocess use | The `ffmpeg` calls described above. |
| Network access | `brand.py` reading a website's colours, and `fonts.py` adding a font pack, as described above. |
| Long expressions | Colour maths in `scripts/kit.py`. |
| Broad capability ("excessive agency") | The skills write image and slide files where you ask them to. |

None of these involve credentials or hidden instructions. Read `src/scripts/` to confirm; it is plain Python.

## Reporting a vulnerability

Please report privately through the repository's **Security** tab ("Report a vulnerability") rather than in a public issue. Include the file, the steps to reproduce and the impact you see. You will get a reply within a week, and a fix in the next release.

## Supported versions

Only the latest release receives fixes.
