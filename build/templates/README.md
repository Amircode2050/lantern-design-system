<p align="center">
  <img src="docs/images/teasers/hero.jpg" alt="A glowing lantern above a small lit workshop, beside the word Lantern" width="100%">
</p>

<h1 align="center">Lantern</h1>

<p align="center">
  <b>One light. Twelve colours.</b><br>
  An illustration and interface design system, packaged as skills for Claude Code and claude.ai.
</p>

<p align="center">
  <a href="../../actions/workflows/check.yml"><img alt="Checks" src="https://github.com/Amircode2050/lantern-design-system/actions/workflows/check.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="Licence: Apache 2.0" src="https://img.shields.io/badge/licence-Apache%202.0-3366ff"></a>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-1b4d3e">
  <img alt="Twelve colours" src="https://img.shields.io/badge/colours-12-d4af37">
  <img alt="Version {{version}}" src="https://img.shields.io/badge/version-{{version}}-7a1f2b">
</p>

---

Most slide decks explain with bullet points. Lantern explains with pictures: cut-away machines and buildings full of small figures at work, one warm light in the dark, glowing lines that show where energy and information flow. Ask for "a slide that explains how a data centre stays cool" and you get an original illustration, a title that asks the question, one line that answers it, and labels that point to the parts that matter.

It comes in twelve colours, each with a dark and a light version, seven type sets, many languages and a full shade ramp. The same colours drive a small web interface kit, so a deck, a report and a dashboard can look like one family.

<p align="center">
  <a href="https://amircode2050.github.io/lantern-design-system/"><b>Open the playground</b></a> ·
  <a href="#quick-start">Install</a> ·
  <a href="#the-scene-library">Scene library</a> ·
  <a href="../../releases/latest">Downloads</a>
</p>

<p align="center">
  <a href="https://amircode2050.github.io/lantern-design-system/video/lantern-teaser.mp4"><img src="docs/images/teaser-poster.jpg" alt="Play the 26-second tour of the Lantern playground" width="100%"></a><br>
  <i>A 26-second tour: pick a colour, watch the page follow, download a slide template.</i>
</p>

<p align="center">
  <img src="docs/images/teasers/spectrum.jpg" alt="Twelve lanterns, one in each colour theme" width="100%">
</p>

Lantern is free and open source. If it saves you a deck or two, a star on GitHub helps other people find it.

## Contents

- [What you get](#what-you-get)
- [Try it in your browser](#try-it-in-your-browser)
- [Gallery](#gallery)
- [The scene library](#the-scene-library)
- [Quick start](#quick-start)
- [Choosing a look](#choosing-a-look)
- [The colours](#the-colours)
- [Type sets](#type-sets)
- [Languages](#languages)
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
- **Seven type sets** and **many languages** (accented Latin, Vietnamese, Cyrillic, Greek, and right-to-left Persian and Arabic), every font bundled or one command away, so nothing falls back to Arial on someone else's machine.
- **Seamless looping animation** as GIF and MP4, with an automatic seam check.
- **An interface kit**: CSS variables, a Tailwind theme and eight components, in any colour.
- **A theme generator** that turns one brand colour into a complete theme and checks every text colour for contrast.
- **A voice guide**, so the words on a slide are as considered as the picture.
- **A library of {{scene_count}} ready scenes** for the ideas people explain most often, from supply chains to the cloud, each with its question, answer and labels.
- **Your brand in one step**: point it at a logo, a website or a hex value and get a full theme with previews.
- **Social posts** in square, 4:5 and 9:16, as stills or seamless MP4 loops.
- **Slide templates** for PowerPoint, Keynote and Google Slides in every colour, every word and the chart editable.
- **A playground** on the web, where the whole page changes colour as you choose.

## Try it in your browser

The **[Lantern playground](https://amircode2050.github.io/lantern-design-system/)** shows the whole system without installing anything. Pick a colour and the entire page, its scenes, its shade ramp and its buttons take it on.

<p align="center">
  <a href="https://amircode2050.github.io/lantern-design-system/"><img src="docs/images/playground-dark.jpg" alt="The playground in Blue, dark" width="49%"></a>
  <a href="https://amircode2050.github.io/lantern-design-system/"><img src="docs/images/playground-light.jpg" alt="The playground in Gold, light" width="49%"></a>
</p>

| On the page | What you can do |
|---|---|
| Pick a colour | Switch between the twelve colours, dark or light, and the seven type sets. |
| Six scenes | See the supply chain, the cloud, a data centre, a power grid, a knowledge base and a sales funnel in the chosen colour. |
| The shade ramp | Copy any of the eleven shades, 50 to 950, with one click. |
| The interface kit | See buttons, cards, a form and a stat in that colour. |
| Take it with you | Copy the install commands, or download the skill, the slide templates in dark and light, and `tokens.css`. |
| Your colour | Pick any brand colour to see its ramp, the nearest Lantern colour and the command that builds a theme from it. |
| The scene library | Browse all {{scene_count}} scenes with their questions and names. |

The page remembers your last choice in your own browser and sends nothing anywhere.

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

Every skill is a plain folder in [`skills/`](skills): `skills/lantern` is the master skill with every colour, and `skills/lantern-<colour>` holds one colour each. Install the master skill, or just the colours you use.

| Agent | Quickest install | What you get |
|---|---|---|
| [Claude Code](#claude-code) (terminal, desktop, IDE) | `/plugin marketplace add Amircode2050/lantern-design-system` | any skill, one at a time |
| [Claude.ai and the Claude app](#claudeai-and-the-claude-app) | upload a zip from the latest release | one skill per zip |
| [OpenAI Codex](#openai-codex) | `codex plugin marketplace add Amircode2050/lantern-design-system` | all 13 skills |
| [GitHub Copilot CLI](#github-copilot-cli) | `copilot plugin marketplace add Amircode2050/lantern-design-system` | any skill, one at a time |
| [Antigravity CLI](#antigravity-cli) | `npx skills add Amircode2050/lantern-design-system -a antigravity-cli` | the skills you pick |
| [Cursor](#cursor) | `npx skills add Amircode2050/lantern-design-system -a cursor` | the skills you pick |
| [OpenCode](#opencode) | `npx skills add Amircode2050/lantern-design-system -a opencode` | the skills you pick |
| [Grok Build](#grok-build) | `npx skills add Amircode2050/lantern-design-system -a grok` | the skills you pick |
| [Any other agent](#any-other-agent) | copy a folder from `skills/` | the skills you copy |

#### Claude Code

Inside a session (the terminal, the desktop app or an IDE extension):

```
/plugin marketplace add Amircode2050/lantern-design-system
/plugin install lantern@lantern-design-system
```

Or from your terminal, without opening a session:

```bash
claude plugin marketplace add Amircode2050/lantern-design-system
claude plugin install lantern@lantern-design-system
claude plugin install lantern-teal@lantern-design-system
```

Update later with `claude plugin marketplace update lantern-design-system`, and remove a skill with `claude plugin uninstall lantern-teal@lantern-design-system`.

**If adding the marketplace fails** (an SSH `Permission denied (publickey)`, a checkout error, or a message that the repo has no release to download), add it by its full HTTPS address instead:

```bash
claude plugin marketplace add https://github.com/Amircode2050/lantern-design-system.git
```

or install from the release download, which needs no git at all: download `lantern-design-system.zip` from the [latest release](../../releases/latest), unzip it, and from the folder that holds it run

```bash
claude plugin marketplace add ./lantern-design-system
claude plugin install lantern@lantern-design-system
```

On Windows, a checkout error usually means a path over 260 characters; `git config --global core.longpaths true` fixes it.

#### Claude.ai and the Claude app

Download the skill's zip (for example `lantern.zip` or `lantern-teal.zip`) from the [latest release](../../releases/latest), then upload it under **Settings, Capabilities, Skills**. Skills you upload there also work in the Claude desktop and mobile apps.

#### OpenAI Codex

```bash
codex plugin marketplace add Amircode2050/lantern-design-system
codex plugin add lantern-design-system@lantern-design-system
```

The plugin carries all thirteen skills; Codex picks the colour you name. In the ChatGPT desktop app, the same marketplace appears in the Plugins directory once added. To install a single skill instead, use `npx skills add Amircode2050/lantern-design-system --skill lantern -a codex`.

#### GitHub Copilot CLI

```bash
copilot plugin marketplace add Amircode2050/lantern-design-system
copilot plugin install lantern@lantern-design-system
copilot plugin install lantern-teal@lantern-design-system
```

For Copilot in VS Code, use `npx skills add Amircode2050/lantern-design-system -a github-copilot`.

#### Antigravity CLI

```bash
npx skills add Amircode2050/lantern-design-system --skill lantern -a antigravity-cli -g
```

Antigravity CLI (`agy`), which replaced Gemini CLI, reads skills from `.agents/skills/` (this project) or `~/.gemini/antigravity-cli/skills/` (every project), so a copied folder works too.

#### Cursor

```bash
npx skills add Amircode2050/lantern-design-system --skill lantern -a cursor -g
```

A Cursor team can also add the skills as plugins: import this repository under **Dashboard, Settings, Plugins, Import** (it reads `.cursor-plugin/marketplace.json`).

#### OpenCode

```bash
npx skills add Amircode2050/lantern-design-system --skill lantern -a opencode -g
```

OpenCode also reads skills from `.opencode/skills/`, `~/.config/opencode/skills/`, `.agents/skills/` and `.claude/skills/`, so a copied folder works too.

#### Grok Build

```bash
npx skills add Amircode2050/lantern-design-system --skill lantern -a grok -g
```

Grok Build also reads Claude Code plugins and skills, so if Lantern is installed in Claude Code, Grok Build finds it without another step. Skills live in `.grok/skills/` (this project) or `~/.grok/skills/` (every project).

#### Any other agent

The skills follow the open [Agent Skills](https://agentskills.io) format (a folder with a `SKILL.md`), so any agent that reads that format can use them unchanged. The [`skills` installer](https://github.com/vercel-labs/skills) knows where each agent looks (`npx skills add Amircode2050/lantern-design-system` asks which skills and agents), or copy a folder by hand:

| Agent | This project only | Every project |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` |
| Antigravity CLI | `.agents/skills/` | `~/.gemini/antigravity-cli/skills/` |
| GitHub Copilot | `.agents/skills/` | `~/.copilot/skills/` |
| Cursor | `.agents/skills/` | `~/.cursor/skills/` |
| OpenCode | `.opencode/skills/` | `~/.config/opencode/skills/` |
| Grok Build | `.grok/skills/` | `~/.grok/skills/` |

```bash
git clone https://github.com/Amircode2050/lantern-design-system
cp -r lantern-design-system/skills/lantern ~/.agents/skills/
```

Paths change as agents evolve, so check your agent's documentation if a skill does not appear. Whatever the agent, the skill draws with Python on your machine, so step 2 below applies to every agent. In agents that cannot show multiple-choice questions, the colour picker asks the same questions in plain text.

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

**Step two, the details.** That colour in dark and light, the seven type sets, and the family's shade options. Pick a different shade (Burgundy instead of Maroon, say) and the skill builds it on the spot with the same recipe.

<p align="center"><img src="docs/images/colors/red.jpg" alt="Step two for Red: dark and light, type sets and shade options" width="100%"></p>

Name what you want in the request ("lantern teal, light, modern") and it skips the questions.

## The colours

| Colour | Core | The light | Type set | Starts in | Best for |
|---|---|---|---|---|---|
{{colour_table}}

Every theme follows the same rules: a deep ground, a structure ramp built from the core colour, exactly one accent (the light) and a support colour reserved for natural things such as water. Text colours are fitted to WCAG contrast in both variants.

{{colour_guide}}

## Type sets

<p align="center"><img src="docs/images/type-sets.jpg" alt="The seven type sets: Classic, Modern, Editorial, Technical, Geometric, Garamond and Swiss" width="100%"></p>

| Set | Display | Text | Numbers and code | Mood |
|---|---|---|---|---|
| Classic | PT Serif | Inter | JetBrains Mono | bookish, scholarly, calm |
| Modern | Space Grotesk | Inter | JetBrains Mono | technical, crisp, product-like |
| Editorial | Fraunces | Source Sans 3 | JetBrains Mono | magazine, expressive, warm |
| Technical | IBM Plex Serif | IBM Plex Sans | IBM Plex Mono | corporate, precise, engineered |
| Geometric | DM Serif Display | DM Sans | JetBrains Mono | clean, round, contemporary |
| Garamond | EB Garamond | Inter | JetBrains Mono | old-style, literary, humane |
| Swiss | Inter Tight | Inter | JetBrains Mono | neutral, dense, poster-like |

Any type set works with any colour. The scale is fixed so pieces stay consistent: a 132-point word for break slides, 44 for titles, 30 for labels, 16.5 for body text, and nothing smaller than 13.

## Languages

<p align="center"><img src="docs/images/languages.jpg" alt="The same slide in Polish, Vietnamese, Russian, Greek, Persian and Arabic" width="100%"></p>

Write the words in your language and Lantern picks the right letters. Persian, Arabic and Urdu are set right to left: titles move to the top right and every text block aligns to its right edge, while the picture and its labels keep their places.

All 24 library scenes also come translated into **Persian** and **Spanish**, and the slide template comes in **Persian**, right to left throughout (mirrored layouts, Persian digits, the chart reading from the right):

```bash
python scripts/scenes.py bank fa                    # a scene in Persian; es for Spanish
python scripts/social.py bank story rose fa         # a social post in Persian
python scripts/deck.py purple --lang fa             # a Persian slide template (font: Vazirmatn)
```

Persian slide templates for every colour are attached to each [release](../../releases/latest).

| Font pack | Covers | Size |
|---|---|---|
| `core` | English and other plain-Latin languages, for Classic, Modern and Editorial | 0.35 MB |
| `sets` | the Technical, Geometric, Garamond and Swiss type sets | 0.40 MB |
| `europe` | Polish, Czech, Slovak, Hungarian, Romanian, Turkish, the Baltic languages, Vietnamese and more | 0.97 MB |
| `cyrillic-greek` | Russian, Ukrainian, Bulgarian, Serbian, Kazakh, Greek and more | 0.82 MB |
| `arabic` | Persian, Arabic, Urdu (Vazirmatn) | 0.06 MB |

The master `lantern` skill includes every pack. A colour skill includes `core`; add the others when you need them:

```bash
python scripts/fonts.py list              # what is installed
python scripts/fonts.py add sets europe   # or: add all
python scripts/fonts.py verify            # check every file against its recorded hash
```

`fonts.py` downloads only the files pinned in `assets/fonts/manifest.json`, from jsDelivr's mirror of the [Fontsource](https://fontsource.org) packages, and keeps a file only if its SHA-256 hash matches. Chinese, Japanese and Korean are not bundled yet; they render in your system's font if it has one.

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

Every colour has a ten-slide template in dark and light, attached to each [release](../../releases/latest), in a calm editorial layout: thin rules, small labels and page numbers, and plenty of room. It has a title, agenda, section break, three illustrated explainers (the drawing framed, its three parts numbered and described beside it), a text slide, two columns, a native chart with the key number set large, and a closing slide. The pictures are images; every title, label and number is editable, and the file's own theme colours and fonts are set, so a new shape or chart matches without effort. It opens in PowerPoint, Keynote and Google Slides (File, Import slides).

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

sys.path.insert(0, "skills/lantern/scripts")
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

Every skill in `skills/` is generated from one source, so a fix lands everywhere at once.

```
src/            the engine (scripts, interface kit, fonts, system.json) and the twelve themes
build/          build.py, themes.py (colour recipes), check.py, release.py, teasers.py, templates/
skills/         the generated skills, one folder each; .claude-plugin/marketplace.json lists each as a plugin
docs/images/    everything on this page
docs/index.html the playground, served by GitHub Pages
```

```bash
pip install -r requirements.txt ruff
python -m playwright install chromium
python build/build.py                 # renders reference images and writes every skill (about ten minutes)
python build/build.py --skip-render   # code and docs only
python build/check.py                 # contrast, names, interface contrast, fonts, translations, engine copies
python -m unittest discover -s tests  # unit tests, no browser needed
python build/readme_images.py         # the images on this page
python build/site.py                  # the playground in docs/ (GitHub Pages, deploy from /docs)
python src/scripts/deck.py all --out dist   # slide templates for a release
```

## Contributing, security and licence

Contributions are welcome, especially new colours and components: see [CONTRIBUTING.md](CONTRIBUTING.md). To report a vulnerability, see [SECURITY.md](SECURITY.md). Changes are listed in [CHANGELOG.md](CHANGELOG.md).

Lantern is licensed under the [Apache License 2.0](LICENSE). The bundled fonts (PT Serif, Inter, JetBrains Mono, Space Grotesk, Fraunces and Source Sans 3) keep their own SIL Open Font Licence; see [NOTICE](NOTICE).
