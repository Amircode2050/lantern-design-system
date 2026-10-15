# Security

## What the skills do on your machine

- **Render locally.** Scenes are SVG strings drawn by a headless Chromium (Playwright). Every network request from that page is blocked, so rendering never fetches anything.
- **Write only where you ask.** Scripts write images, frames and exports to the paths you pass them. Theme names are restricted to `a-z`, `0-9` and `_`, so they cannot point outside the `themes/` folder.
- **Run one external program.** GIF and MP4 output calls `ffmpeg` with an argument list (no shell).
- **Need no accounts or keys.** There is no telemetry and there are no credentials or environment variables. The only download is the browser you install yourself with `python -m playwright install chromium`.
- **Use the network in one place only.** `brand.py` with a web address downloads that page and up to five of its stylesheets (http or https only, 10-second timeout, 2 MB each) to read their colours. It sends nothing but the requests and runs nothing it downloads. Every other script works offline.

## Expected scanner findings

Static skill scanners may flag:

| Finding | Why it appears |
|---|---|
| Referenced file not fully inspected | `SKILL.md` points to bundled images and scripts that a text scanner cannot read. |
| Subprocess use | The `ffmpeg` calls described above. |
| Long expressions | Colour maths in `scripts/kit.py`. |
| Network access | `brand.py` reading a website's colours, as described above. |

None of these involve credentials or hidden instructions, and the only network access is the one you start with `brand.py`. Read `src/scripts/` to confirm; it is plain Python.

## Reporting a vulnerability

Please report privately through the repository's **Security** tab ("Report a vulnerability") rather than a public issue. Include the file, the steps to reproduce and the impact you see. You will get a reply within a week.

## Supported versions

Only the latest release receives fixes.
