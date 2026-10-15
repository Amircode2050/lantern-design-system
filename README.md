# Lantern design system

One illustration and interface style in twelve colours, packaged as skills for Claude Code and claude.ai.

Lantern draws explanatory pictures the way a stage designer lights a set: original cut-away machines and buildings, small silhouette figures at work, one warm light, glowing flow lines and a fine grain on a deep ground. The same tokens drive slides, annotated figures, looping animations and a small web interface kit.

![The colour picker: twelve themes with their shade ramps](docs/images/picker.jpg)

| | |
|---|---|
| ![Blue, dark: an annotated factory cut-away](docs/images/blue_factory_dark.jpg) | ![Red, light: the same scene on paper](docs/images/red_factory_light.jpg) |
| ![Gold, dark: a break slide with a saucer](docs/images/gold_break_dark.jpg) | ![Purple, dark: a portrait scene](docs/images/purple_portrait_dark.jpg) |

## What you get

- **Twelve colour themes**, each in a dark and a light variant, with an 11-step shade ramp (50 to 950) and alternative shades: Black, White, Blue, Purple, Green, Red, Gray, Teal, Gold, Orange, Cyan, Rose.
- **Two illustration modes**: cut-away scenes with many small figures, and close-up portraits with large characters and one beam of light.
- **A component library** of about forty parts: factory roofs, storm clouds, batteries, conveyors, server racks, domes, a lantern tower, a saucer with a tractor beam, profile busts, robots, light cones and more.
- **Three type sets**: Classic (PT Serif, Inter), Modern (Space Grotesk, Inter) and Editorial (Fraunces, Source Sans 3), all with JetBrains Mono.
- **Seamless GIF and MP4 loops**, with a seam check.
- **A UI layer**: CSS variables, a Tailwind theme and eight components (button, card, field, table, tag, callout, stat, slide frame) for any theme.
- **A theme generator**: give it one brand colour and it builds a complete theme, with every text colour checked for contrast.
- **A voice guide** for the words on slides and screens.

| Colour | Core | Light | Type set | Starts in |
|---|---|---|---|---|
| Black | Jet `#1C1C1E` | metallic gold | Classic | dark |
| White | Ivory `#FAF8F2` | white, ink only | Editorial | light |
| Blue | Blue `#3366FF` | amber | Classic | dark |
| Purple | Purple `#6A57B8` | warm peach | Classic | dark |
| Green | Forest `#1B4D3E` | amber | Classic | dark |
| Red | Maroon `#7A1F2B` | champagne | Editorial | dark |
| Gray | Charcoal `#36454F` | amber | Modern | dark |
| Teal | Deep teal `#0F766E` | amber | Modern | dark |
| Gold | Metallic gold `#D4AF37` | gold on near-black | Classic | dark |
| Orange | Burnt orange `#CC5500` | tangerine on near-black | Modern | dark |
| Cyan | Bright cyan `#1CABE2` | amber | Modern | dark |
| Rose | Rose `#C2185B` | champagne | Editorial | dark |

## The skills

| Skill | Use it for |
|---|---|
| `lantern` | Everything: shows the picker, asks which colour, variant, type set and shade, and can add new colours. |
| `lantern-black` ... `lantern-rose` | One colour each, for when you always want the same look. |

Install the master skill, a single colour, or both. Every skill is self-contained.

## Install

**Claude Code** (plugin marketplace):

```
/plugin marketplace add Amircode2050/lantern-design-system
/plugin install lantern@lantern-design-system
```

Replace `lantern` with `lantern-red`, `lantern-gold` and so on for a single colour.

**claude.ai**: download the skill's zip from the latest release and upload it under Settings, Capabilities, Skills.

**By hand**: copy `plugins/<skill>/skills/<skill>/` into `~/.claude/skills/`.

## Requirements

The skills render with a headless browser, so the machine that runs them needs:

- Python 3.11 or newer
- `pip install -r requirements.txt` (Pillow, numpy, Playwright)
- `python -m playwright install chromium`
- ffmpeg, only for GIF and MP4 output

Each skill can check its own setup: `python scripts/kit.py` prints what is missing and how to install it, and re-checks colour contrast.

## Using it

Ask for what you want and name the style, or let the master skill ask you:

- "A break slide in the Lantern gold style."
- "An annotated cut-away explaining how a data centre is cooled, red, light variant."
- "A 25-second looping animation of the saucer for my title slide."
- "Export the teal theme as CSS variables and Tailwind tokens."

The scripts also work on their own:

```bash
python scripts/examples.py factory dark red        # a reference scene
python scripts/export.py teal out/teal             # tokens.css, fonts.css, tailwind.theme.js, ui.css, demo.html
python scripts/new_theme.py lilac "#8E7CC3" --preview out
python scripts/intake.py my-reference.png          # nearest theme for an image
```

## Building from source

Every skill is generated from one source:

```
src/            engine (scripts, UI, fonts, system.json) and the twelve themes
docs/           templates for SKILL.md and the reference guides
build/          build.py (assembles every skill) and themes.py (theme recipes)
plugins/        the generated skills, one plugin each
```

```bash
pip install -r requirements.txt
python -m playwright install chromium
python build/themes.py        # only after changing a theme recipe
python build/build.py         # renders reference images, writes plugins/ and dist/*.zip
```

`python build/build.py --skip-render` rebuilds the docs and code without re-rendering the images.

## Licence

The code, themes, documentation and images are licensed under the [Apache License 2.0](LICENSE). The bundled fonts keep their own SIL Open Font License; see [NOTICE](NOTICE) and `src/assets/fonts/`.
