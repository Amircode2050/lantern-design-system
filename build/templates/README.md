<p align="center">
  <img src="docs/images/teasers/hero.jpg" alt="A glowing lantern above a small lit workshop, beside the word Lantern" width="100%">
</p>

<h1 align="center">Lantern</h1>

<p align="center">
  <b>One light. Twelve colours.</b><br>
  An illustration and interface design system, packaged as skills for Claude Code and claude.ai.
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: Apache 2.0" src="https://img.shields.io/badge/licence-Apache%202.0-3366ff"></a>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-1b4d3e">
  <img alt="Twelve colours" src="https://img.shields.io/badge/colours-12-d4af37">
  <img alt="Version {{version}}" src="https://img.shields.io/badge/version-{{version}}-7a1f2b">
</p>

---

Most slide decks explain with bullet points. Lantern explains with pictures: cut-away machines and buildings full of small figures at work, one warm light in the dark, glowing lines that show where energy and information flow. Ask for "a slide that explains how a data centre stays cool" and you get an original illustration, a title that asks the question, one line that answers it, and labels that point to the parts that matter.

It comes in twelve colours, each with a dark and a light version, three type sets and a full shade ramp. The same colours drive a small web interface kit, so a deck, a report and a dashboard can look like one family.

<p align="center"><b><a href="https://amircode2050.github.io/lantern-design-system/">Try it live in the playground</a></b>: pick a colour and watch every scene, shade and button change with it.</p>

<p align="center">
  <img src="docs/images/teasers/spectrum.jpg" alt="Twelve lanterns, one in each colour theme" width="100%">
</p>

## Contents

- [What you get](#what-you-get)
- [Gallery](#gallery)
- [The scene library](#the-scene-library)
- [Quick start](#quick-start)
- [Choosing a look](#choosing-a-look)
- [The colours](#the-colours)
- [Type sets](#type-sets)
- [Illustration modes and components](#illustration-modes-and-components)
- [Animation](#animation)
- [Interface kit and design tokens](#interface-kit-and-design-tokens)
- [Your brand in one step](#your-brand-in-one-step)
- [Social posts](#social-posts)
- [Slide templates](#slide-templates)
- [Make your own colour](#make-your-own-colour)
- [Words on the slide](#words-on-the-slide)
- [Accessibility](#accessibility)
- [Using the scripts directly](#using-the-scripts-directly)
- [Troubleshooting](#troubleshooting)
- [Building from source](#building-from-source)
- [Contributing, security and licence](#contributing-security-and-licence)

## What you get

- **Twelve colour themes**, each in a dark and a light variant, with an 11-step shade ramp (50 to 950) and two alternative shades you can switch to.
- **Two illustration modes**: cut-away scenes with many small figures, and close-up portraits with large characters and a single beam of light.
- **About forty drawing components**: factory roofs, storm clouds, batteries, conveyors, server racks, domes, a watchtower, a saucer with a tractor beam, profile busts, robots, light cones and the lantern itself.
- **Three type sets**, every font bundled, so nothing falls back to Arial on someone else's machine.
- **Seamless looping animation** as GIF and MP4, with an automatic seam check.
- **An interface kit**: CSS variables, a Tailwind theme and eight components, in any colour.
- **A theme generator** that turns one brand colour into a complete theme and checks every text colour for contrast.
- **A voice guide**, so the words on a slide are as considered as the picture.
- **A library of {{scene_count}} ready scenes** for the ideas people explain most often, from supply chains to the cloud, each with its question, answer and labels.
- **Your brand in one step**: point it at a logo, a website or a hex value and get a full theme with previews.
- **Social posts** in square, 4:5 and 9:16, as stills or seamless MP4 loops.
- **Slide templates** for PowerPoint, Keynote and Google Slides in every colour, every word and the chart editable.
- **A playground** on the web, where the whole page changes colour as you choose.

## Gallery

| | |
|---|---|
| ![Blue, dark: an annotated factory cut-away](docs/images/blue_factory_dark.jpg) | ![Red, light: the same scene on paper](docs/images/red_factory_light.jpg) |
| **Blue, dark.** An annotated cut-away: a question, an answer and four labelled parts. | **Red, light.** The same scene in the light variant, ready for print. |
| ![Gold, dark: a break slide with a saucer](docs/images/gold_break_dark.jpg) | ![Purple, dark: a portrait scene](docs/images/purple_portrait_dark.jpg) |
| **Gold, dark.** A break slide: the ship is processing, so should you. | **Purple, dark.** Portrait mode: two characters and one beam of light. |

<p align="center">
  <img src="docs/images/loop.gif" alt="A looping animation of the saucer break slide" width="720"><br>
  <i>Every moving part completes whole cycles, so loops never jump.</i>
</p>

| | |
|---|---|
| ![The component library on a dark ground](docs/images/components-dark.jpg) | ![The component library on paper](docs/images/components-light.jpg) |
| **The component library**, Blue dark. | **The same library**, White light. |

<p align="center">
  <img src="docs/images/teasers/portrait.jpg" alt="A person in profile holds up a lantern whose beam reaches a robot" width="80%">
</p>

## The scene library

{{scene_count}} cut-aways, ready to drop into a deck. Each comes in every colour and both variants, carries its own words (a question, an answer line and three labels), and moves as a seamless loop. Shown here across the twelve colours.

{{scene_table}}

```bash
python scripts/scenes.py                                  # list them
python scripts/scenes.py power_grid teal light modern     # one scene, any colour, variant and type set
python scripts/scenes.py power_grid clean                 # the picture without words
```

Change the words without touching the drawing: `build("bank", words={"title": ["Where does the money go?"], "answer": "Mostly back out as loans."})`.

## Quick start

### 1. Install the skills

**Claude Code**, from this repository as a plugin marketplace:

```
/plugin marketplace add Amircode2050/lantern-design-system
/plugin install lantern@lantern-design-system
```

`lantern` is the master skill with every colour. If you always want the same look, install a single colour instead, for example `lantern-red@lantern-design-system`.

**claude.ai**: download the skill's zip from the [latest release](../../releases/latest), then upload it under **Settings, Capabilities, Skills**.

**By hand**: copy `plugins/<skill>/skills/<skill>/` into `~/.claude/skills/`.

| Skill | What it does |
|---|---|
| `lantern` | Shows the picker, asks for colour, variant, type set and shade, can add new colours, exports tokens. |
{{skill_table}}

### 2. Install what it renders with

The skills draw SVG and photograph it with a headless browser, so the machine that runs them needs:

```bash
pip install pillow numpy playwright
python -m playwright install chromium
```

plus [ffmpeg](https://ffmpeg.org) if you want GIF or MP4 output, `pip install python-pptx` for slide templates, and Python 3.11 or newer. To check a setup, run `python scripts/kit.py` inside any skill folder: it prints what is missing and the command that fixes it.

### 3. Ask for something

- "A title slide for a talk on supply chains, Lantern gold."
- "An annotated cut-away that explains how a heat pump works. Teal, light variant, editorial type."
- "A break slide in my Lantern style." (the master skill will show you the picker)
- "A 25-second loop of the saucer for the start of my keynote."
- "Export the rose theme as CSS variables and a Tailwind theme."
- "Here is our logo. Make a Lantern colour from it."
- "Our website is example.com. Make our slides match it."
- "Turn the supply chain scene into an Instagram story, Lantern orange."
- "Give me a PowerPoint template in Lantern teal, light."

## Choosing a look

The master skill asks at most two short questions, each with a picture, and remembers your answers for the rest of the conversation.

**Step one, the colour.** Every installed theme with its mood, its light and its shade ramp:

<p align="center"><img src="docs/images/picker.jpg" alt="The colour picker" width="100%"></p>

**Step two, the details.** That colour in dark and light, the three type sets, and the family's shade options. Pick a different shade (Burgundy instead of Maroon, say) and the skill builds it on the spot with the same recipe.

<p align="center"><img src="docs/images/colors/red.jpg" alt="Step two for Red: dark and light, type sets and shade options" width="100%"></p>

Name what you want in the request ("lantern teal, light, modern") and it skips the questions.

## The colours

| Colour | Core | The light | Type set | Starts in | Best for |
|---|---|---|---|---|---|
{{colour_table}}

Every theme follows the same rules: a deep ground, a structure ramp built from the core colour, exactly one accent (the light) and a support colour reserved for natural things such as water. Text colours are fitted to WCAG contrast in both variants.

{{colour_guide}}

## Type sets

<p align="center"><img src="docs/images/type-sets.jpg" alt="Classic, Modern and Editorial type sets" width="100%"></p>

| Set | Display | Text | Numbers and code | Mood |
|---|---|---|---|---|
| Classic | PT Serif | Inter | JetBrains Mono | bookish, scholarly, calm |
| Modern | Space Grotesk | Inter | JetBrains Mono | technical, crisp, product-like |
| Editorial | Fraunces | Source Sans 3 | JetBrains Mono | magazine, expressive, warm |

Any type set works with any colour. The scale is fixed so pieces stay consistent: a 132-point word for break slides, 44 for titles, 30 for labels, 16.5 for body text, and nothing smaller than 13.

## Illustration modes and components

**Cut-away scenes** open a building, machine or vessel like a doll's house: five to eight linked rooms, small silhouette figures who are always doing something, one dominant light, and flow lines between the parts. Flows carry meaning by shape as well as colour: round dots for energy, small squares for information, rings for water.

**Portrait scenes** use two or three large characters (a person in strict profile, a robot, a lit object between them), soft gradients and a single beam of light, with no text in the picture.

The building blocks:

| Group | Components |
|---|---|
| Structure | `shell`, `room`, `slab`, `wall`, `truss`, `plinth`, `sawtooth_roof`, `gable`, `arched_window`, `arcade` |
| Light | `lantern`, `pendant_lamp`, `string_lights`, `orb`, `glow`, `light_cone`, `headlamp` |
| Weather and nature | `cloud` (with rain and a lightning bolt), `tree` |
| Town and utilities | `house`, `road`, `truck`, `pylon`, `turbine`, `solar_panel`, `tank`, `shelf`, `bed`, `dish` |
| Machines and props | `battery`, `conveyor`, `crate`, `car`, `machine`, `server_rack`, `clock`, `desk`, `cabinet`, `screen`, `ladder`, `gear`, `pipe`, `cable` |
| Large architecture | `dome`, `gallery_ring`, `lantern_tower`, `saucer`, `tractor_beam` |
| Science | `orrery`, `thinking_core` |
| People and machines | `standing`, `seated`, `bust_human`, `bust_robot`, `camera_eye`, `pane` |
| Data | `bars`, `flow`, `sight` |
| Text | `title_block`, `callout`, `break_slide`, `credit` |

Each skill's `references/components.md` lists every function with its arguments.

## Animation

Any scene becomes a seamless loop: every moving part (gears, flows, rain, blinking lights, the lantern's flame) completes whole cycles per loop, and `check_loop()` measures the seam. GIFs come out at an exact length (the frame rate must divide 100, because GIF timing is in hundredths of a second) and shrink their palette automatically to stay under 15 MB. MP4s are 1080p H.264. Every animation ships with a still frame for anyone who prefers no motion.

```python
def frame(t):
    return build(t)  # your scene as a function of time


if __name__ == "__main__":
    set_theme("dark", color="gold")
    set_canvas("16:9", loop=25)
    render_frames(frame, 10, "frames10", fresh=True)
    print(check_loop("frames10"))  # seam vs a normal frame step: should be close
    make_gif("frames10", "loop.gif")
```

## Interface kit and design tokens

<p align="center">
  <img src="docs/images/ui-dark.jpg" alt="The interface kit in Blue, dark" width="49%">
  <img src="docs/images/ui-light.jpg" alt="The interface kit in White, light" width="49%">
</p>

```bash
python scripts/export.py teal out/teal --type modern --default dark
```

| File | Contents |
|---|---|
| `tokens.css` | Every colour as a CSS variable for both variants (switch with `data-theme="dark"` or `"light"` on `<html>`), the shade ramp as `--core-50` to `--core-950`, semantic names (`--bg`, `--surface`, `--text`, `--primary`, `--accent-fg`, `--link`), fonts, type scale, spacing and radii. The names are the same in every colour, so changing colour means swapping one file. |
| `fonts.css` | The type set's fonts, embedded. |
| `tailwind.theme.js` | A Tailwind `theme.extend` block pointing at those variables. |
| `ui.css` | Type classes, layout helpers and eight components: button, card, field, table, tag, callout, stat and a 16:9 slide frame. |
| `demo.html` | Every component on one page, with a variant switch. |

The accent keeps its meaning in an interface: it marks the one thing to look at. Actions use the core colour, and a core too pale to carry white text falls back to ink.

## Your brand in one step

```bash
python scripts/brand.py acme https://example.com     # the colours a website declares
python scripts/brand.py acme logo.png                # a logo or a few screenshots
python scripts/brand.py acme "#E4002B"               # a colour you already know
```

Lantern finds the brand's most characteristic colour (chromatic, used often, not too pale), borrows the recipe of the nearest of the twelve colours (a yellow gets Gold's near-black ground, a grey gets the monochrome recipe), and writes a complete theme. It then renders a cover slide, a scene and the component sheet in dark and light, plus the CSS and Tailwind tokens, into `brand-acme/`. If it picked the wrong colour, it prints the runners-up and the command to use one of them.

The website mode is the only part of Lantern that uses the network: it downloads that one page and up to five of its stylesheets, nothing else.

## Social posts

<p align="center">
  <img src="docs/images/social/square.jpg" alt="A square post: what is the cloud, really?" width="32%">
  <img src="docs/images/social/portrait.jpg" alt="A 4:5 post: how does a parcel reach your door?" width="32%">
  <img src="docs/images/social/story.jpg" alt="A 9:16 story: how does a knowledge base answer a question?" width="27%">
</p>

```bash
python scripts/social.py cloud_computing square blue          # 1080x1080 for LinkedIn, X and Instagram
python scripts/social.py supply_chain portrait teal           # 1080x1350 feed post
python scripts/social.py knowledge_base story gold --loop 8   # 1080x1920 still plus a seamless 8 s MP4
python scripts/social.py all square rose --handle "@you"      # every scene, with your handle at the foot
```

## Slide templates

<p align="center"><img src="docs/images/deck.jpg" alt="The ten slides of the template in Lantern Blue" width="100%"></p>

Every colour has a ten-slide template in dark and light, attached to each [release](../../releases/latest): title, agenda, section break, three illustrated explainers, a text slide, two columns, a native chart and a closing slide. The pictures are images; every title, label and number is editable, and the file's own theme colours and fonts are set, so a new shape or chart matches without effort. It opens in PowerPoint, Keynote and Google Slides (File, Import slides).

```bash
python scripts/deck.py teal light modern --out teal.pptx
```

The fonts are free from Google Fonts. Google Slides already has them; for PowerPoint and Keynote install the two families of your type set (for Classic, PT Serif and Inter).

## Make your own colour

```bash
python scripts/new_theme.py lilac "#8E7CC3" --preview out
python scripts/picker.py --all
```

One colour in, a complete theme out: both variants, the shade ramp, a button-safe fill, and every text colour nudged until it passes contrast. The preview renders the component sheet in dark and light so you can judge it before using it.

| Option | What it does |
|---|---|
| `--harmony warm` | An amber light whatever the brand colour (the default, and the safest). |
| `--harmony complementary` / `analogous` | The light sits opposite, or next to, the brand colour on the colour wheel. |
| `--harmony monochrome` | The light is a pale tint of the brand colour: for black, white and gray systems. |
| `--accent "#hex"` or `core` | Set the light exactly; `core` makes the brand colour itself the light. |
| `--ground-chroma 0.2` | A near-black ground, for gold, orange and yellow, whose own dark shades turn brown. |
| `--deep 0.55` | Darker grounds in the dark variant. |
| `--from red` | Reuse another theme's recipe for a new shade. |

Starting from a picture instead? `python scripts/intake.py logo.png` reports the dominant colours, the nearest installed theme, and the command to build a new one.

## Words on the slide

Lantern has a voice as well as a look. A title is a real question; the answer line replies in one sentence; labels name the thing ("The workshop") and say what it does in a few short lines. Sentence case, British spelling, no exclamation marks, and a credit line that says what is stylised. The full guide, with limits for every slot and a list of words to avoid, is in each skill's `references/voice.md`.

## Accessibility

- Text and flow colours are checked against every ground they may sit on: 7:1 for primary text, 4.5:1 for secondary text, the answer line and tags.
- Differences never rest on colour alone: flows differ by shape, chart bars carry their values, status tags carry a word.
- Every image gets one sentence of alt text, embedded in the SVG and returned with the file.
- Animations ship with a still, and nothing flashes more than three times a second.
- The interface kit has visible focus rings, 40-pixel controls and errors written under the field.

## Using the scripts directly

The skills are plain Python, so you can script them:

```python
import sys

sys.path.insert(0, "plugins/lantern/skills/lantern/scripts")
from kit import *
from components import *

set_theme("dark", color="green", type_set="classic")
set_canvas("16:9")
body = [
    background(),
    lantern(960, 160, 2.0),
    finish(),
    title_block(["Who keeps the lights on?"], "Fiat lux", "Everybody, a little."),
]
render(svg_doc(std_defs(), "".join(body), alt="A lantern in the dark."), "slide.png", scale=2)
```

`python scripts/examples.py` renders the reference scenes in every colour and variant, and doubles as a self-test.

## Troubleshooting

| Problem | Fix |
|---|---|
| `fonts failed to load` | The `assets/fonts` folder is incomplete; reinstall the skill. |
| `Executable doesn't exist` from Playwright | Run `python -m playwright install chromium`. |
| GIF or MP4 fails | Install ffmpeg and make sure it is on your `PATH`. |
| The skill does not start | Name it ("in the Lantern style", "lantern blue"), or check it is listed under your installed skills. |
| A loop jumps at the seam | A motion is not on whole cycles; `check_loop()` shows how large the jump is. Usually a gear's hole count or a non-integer `cycles`. |
| Text overlaps a leader line | Widths are estimated per font; shorten the label or move it after changing type set. |

## Building from source

Every skill in `plugins/` is generated from one source, so a fix lands everywhere at once.

```
src/            the engine (scripts, interface kit, fonts, system.json) and the twelve themes
build/          build.py, themes.py (colour recipes), check.py, release.py, teasers.py, templates/
plugins/        the generated skills, one plugin each, listed in .claude-plugin/marketplace.json
docs/images/    everything on this page
docs/index.html the playground, served by GitHub Pages
```

```bash
pip install -r requirements.txt ruff
python -m playwright install chromium
python build/build.py                 # renders reference images and writes every skill (about ten minutes)
python build/build.py --skip-render   # code and docs only
python build/check.py                 # contrast, names, interface contrast, engine copies
python build/readme_images.py         # the images on this page
python build/site.py                  # the playground in docs/ (GitHub Pages, deploy from /docs)
python src/scripts/deck.py all --out dist   # slide templates for a release
```

## Contributing, security and licence

Contributions are welcome, especially new colours and components: see [CONTRIBUTING.md](CONTRIBUTING.md). To report a vulnerability, see [SECURITY.md](SECURITY.md). Changes are listed in [CHANGELOG.md](CHANGELOG.md).

Lantern is licensed under the [Apache License 2.0](LICENSE). The bundled fonts (PT Serif, Inter, JetBrains Mono, Space Grotesk, Fraunces and Source Sans 3) keep their own SIL Open Font Licence; see [NOTICE](NOTICE).
