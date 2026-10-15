# Security

## What the skills do on your machine

- **Render locally.** Scenes are SVG strings drawn by a headless Chromium (Playwright). Every network request from that page is blocked, so rendering never fetches anything.
- **Write only where you ask.** Scripts write images, frames and exports to the paths you pass them. Theme names are restricted to `a-z`, `0-9` and `_`, so they cannot point outside the `themes/` folder.
- **Run one external program.** GIF and MP4 output calls `ffmpeg` with an argument list (no shell).
- **Need no accounts or keys.** There are no network calls, telemetry, credentials or environment variables. The only download is the browser you install yourself with `python -m playwright install chromium`.

## Expected scanner findings

Static skill scanners may flag:

| Finding | Why it appears |
|---|---|
| Referenced file not fully inspected | `SKILL.md` points to bundled images and scripts that a text scanner cannot read. |
| Subprocess use | The `ffmpeg` calls described above. |
| Long expressions | Colour maths in `scripts/kit.py`. |

None of these involve network access, credentials or hidden instructions. Read `src/scripts/` to confirm; it is plain Python.

## Reporting a vulnerability

Please report privately through the repository's **Security** tab ("Report a vulnerability") rather than a public issue. Include the file, the steps to reproduce and the impact you see. You will get a reply within a week.

## Supported versions

Only the latest release receives fixes.
