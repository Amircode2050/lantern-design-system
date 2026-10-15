# Lantern Gray

Lantern Gray is part of [Lantern](https://github.com/Amircode2050/lantern-design-system), a design system that draws explanations: cut-away buildings full of small figures at work, one warm light, and glowing lines where energy and information flow. This skill covers the Gray colour: a charcoal ground (#36454F), with one amber light.

Ask for a slide, an annotated figure, a title or break slide, a social post, a seamless GIF or MP4 loop, an editable PowerPoint template, design tokens for a website, or a theme built from your brand colour, logo or website. Twenty-four ready scenes cover common explainers such as a supply chain, a data pipeline and the cloud.

Try every colour in the [playground](https://amircode2050.github.io/lantern-design-system/). Installation for Claude Code, claude.ai and other coding agents is in the [main README](https://github.com/Amircode2050/lantern-design-system#quick-start).

## Requirements

Python 3.11 or newer with `pip install pillow numpy playwright python-pptx` and `python -m playwright install chromium`. `ffmpeg` is needed only for GIF and MP4 output. Run `python scripts/kit.py` to check a setup.

## What it runs and connects to

- Drawings are rendered locally by a headless Chromium with every network request blocked.
- `ffmpeg` is called with an argument list, never through a shell, to encode animations.
- Files are written only to the paths you give.
- `scripts/brand.py`, when you give it a web address, downloads that one page and up to five of its stylesheets from public addresses to read their colours.
- `scripts/fonts.py add <pack>` downloads font files listed in `assets/fonts/manifest.json` from `https://cdn.jsdelivr.net` and keeps each only if its SHA-256 hash matches.
- Nothing else uses the network, nothing is sent except those requests, and there is no telemetry.

See [SECURITY.md](https://github.com/Amircode2050/lantern-design-system/blob/main/SECURITY.md) for details. Code is licensed under the Apache License 2.0 (`LICENSE`, `NOTICE`); the bundled fonts keep their SIL Open Font Licence (`assets/fonts/LICENSES.txt`).
