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
  <img alt="Version 1.1.0" src="https://img.shields.io/badge/version-1.1.0-7a1f2b">
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
  <img src="docs/images/teasers/spectrum.jpg" alt="Twelve lanterns, one in each colour theme" width="100%">
</p>

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
- **A library of 24 ready scenes** for the ideas people explain most often, from supply chains to the cloud, each with its question, answer and labels.
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
| The scene library | Browse all 24 scenes with their questions and names. |

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

24 cut-aways, ready to drop into a deck. Each comes in every colour and both variants, carries its own words (a question, an answer line and three labels), and moves as a seamless loop. Shown here across the twelve colours.

<table>
<tr><td width="33%" valign="top"><img src="docs/site/lib/supply_chain.webp" alt="Cut-away of a factory and a warehouse, with a van carrying a lit parcel along a road to a house." width="100%"><br><b>How does a parcel reach your door?</b><br><code>supply_chain</code></td><td width="33%" valign="top"><img src="docs/site/lib/data_pipeline.webp" alt="Homes and a shop send glowing records along pipes into a hall of servers, then a store, then a big screen." width="100%"><br><b>Where does a dashboard's number come from?</b><br><code>data_pipeline</code></td><td width="33%" valign="top"><img src="docs/site/lib/data_centre.webp" alt="Cut-away data centre with rows of server racks, coolant pipes looping to chillers on the roof and a lit control room." width="100%"><br><b>How does a data centre stay cool?</b><br><code>data_centre</code></td></tr>
<tr><td width="33%" valign="top"><img src="docs/site/lib/power_grid.webp" alt="Wind turbines and solar panels feed glowing power lines over pylons to a substation and a street of lit homes." width="100%"><br><b>How does power reach a home?</b><br><code>power_grid</code></td><td width="33%" valign="top"><img src="docs/site/lib/internet.webp" alt="A person at a lit desk at home, cables through an exchange building to a server hall, with information flowing both ways." width="100%"><br><b>What happens when you open a web page?</b><br><code>internet</code></td><td width="33%" valign="top"><img src="docs/site/lib/org_team.webp" alt="A three-storey cut-away office: leads at a board on top, makers at benches in the middle, support staff below." width="100%"><br><b>Who does what on a team?</b><br><code>org_team</code></td></tr>
<tr><td width="33%" valign="top"><img src="docs/site/lib/sales_funnel.webp" alt="A building of four floors that narrows downward like a funnel: crowds on top, one buyer carrying a lit parcel at the bottom." width="100%"><br><b>Why do most visitors never buy?</b><br><code>sales_funnel</code></td><td width="33%" valign="top"><img src="docs/site/lib/research_lab.webp" alt="A domed laboratory in cut-away: an orrery under the dome, benches and machines below, and a library on the ground floor." width="100%"><br><b>How does a lab turn questions into results?</b><br><code>research_lab</code></td><td width="33%" valign="top"><img src="docs/site/lib/model_training.webp" alt="Shelves of examples ride a conveyor into a hall of servers around a glowing core, with a falling error line on a screen." width="100%"><br><b>How does a model learn from examples?</b><br><code>model_training</code></td></tr>
<tr><td width="33%" valign="top"><img src="docs/site/lib/water_supply.webp" alt="Rain falls on a reservoir; water flows through a treatment plant, up a water tower and down to houses." width="100%"><br><b>How does clean water reach a tap?</b><br><code>water_supply</code></td><td width="33%" valign="top"><img src="docs/site/lib/hospital.webp" alt="A three-storey hospital in cut-away: a ward of beds on top, a lab in the middle, an ambulance bay and front desk below." width="100%"><br><b>What keeps a hospital running at night?</b><br><code>hospital</code></td><td width="33%" valign="top"><img src="docs/site/lib/school.webp" alt="A school in cut-away: a classroom of pupils facing a teacher, a library upstairs, and a yard with trees outside." width="100%"><br><b>What makes a school work?</b><br><code>school</code></td></tr>
<tr><td width="33%" valign="top"><img src="docs/site/lib/bank.webp" alt="A cut-away bank: money flows in from a saver's house, out to a home and a workshop, and a small reserve in the vault." width="100%"><br><b>Where does your deposit go?</b><br><code>bank</code></td><td width="33%" valign="top"><img src="docs/site/lib/support_desk.webp" alt="An office in cut-away: tickets ride a conveyor to agents at desks, and a few climb to engineers at server racks upstairs." width="100%"><br><b>How does a support ticket get solved?</b><br><code>support_desk</code></td><td width="33%" valign="top"><img src="docs/site/lib/newsroom.webp" alt="A newspaper building in cut-away: a dish brings stories to editors upstairs, a press prints below, and a van drives off." width="100%"><br><b>How does a story reach print?</b><br><code>newsroom</code></td></tr>
<tr><td width="33%" valign="top"><img src="docs/site/lib/retail_store.webp" alt="A shop in cut-away: customers at shelves in front, a stock room behind, an office upstairs and a van at the loading dock." width="100%"><br><b>What sits behind a shop shelf?</b><br><code>retail_store</code></td><td width="33%" valign="top"><img src="docs/site/lib/farm_to_table.webp" alt="An orchard, a packing barn, a van on the road and a lit restaurant kitchen with diners at a table." width="100%"><br><b>How does food get from field to plate?</b><br><code>farm_to_table</code></td><td width="33%" valign="top"><img src="docs/site/lib/knowledge_base.webp" alt="A domed reading room in cut-away: shelves on curved galleries, a shaft of light from the oculus onto a reader's desk." width="100%"><br><b>How does a knowledge base answer a question?</b><br><code>knowledge_base</code></td></tr>
<tr><td width="33%" valign="top"><img src="docs/site/lib/network_defence.webp" alt="A walled compound at night: a lit watchtower with sight lines over a server building, a guarded gate and a storm outside." width="100%"><br><b>How is a network defended?</b><br><code>network_defence</code></td><td width="33%" valign="top"><img src="docs/site/lib/cloud_computing.webp" alt="A big soft cloud with a beam of light dropping from it into a cut-away building full of server racks, linked to homes and offices." width="100%"><br><b>What is the cloud, really?</b><br><code>cloud_computing</code></td><td width="33%" valign="top"><img src="docs/site/lib/remote_team.webp" alt="Four small lit homes, each with a person at a desk, linked by flowing lines to a central hub on a hill." width="100%"><br><b>How does a team stay in step from home?</b><br><code>remote_team</code></td></tr>
<tr><td width="33%" valign="top"><img src="docs/site/lib/recycling.webp" alt="A loop of glowing dots: a house, a van, a sorting plant, a factory and a shop, then back to the house." width="100%"><br><b>Where does a bottle go after the bin?</b><br><code>recycling</code></td><td width="33%" valign="top"><img src="docs/site/lib/startup_growth.webp" alt="A garage with two people, a small office and a four-storey building in a row, growing left to right under a bar chart." width="100%"><br><b>How does a small team become a company?</b><br><code>startup_growth</code></td><td width="33%" valign="top"><img src="docs/site/lib/mission_control.webp" alt="A mission control room of consoles facing a big screen, a dish outside, and a dotted signal arcing up to a ship." width="100%"><br><b>How does mission control talk to a ship?</b><br><code>mission_control</code></td></tr>
</table>

```bash
python scripts/scenes.py                                  # list them
python scripts/scenes.py power_grid teal light modern     # one scene, any colour, variant and type set
python scripts/scenes.py power_grid clean                 # the picture without words
```

Change the words without touching the drawing: `build("bank", words={"title": ["Where does the money go?"], "answer": "Mostly back out as loans."})`.

## Quick start

### 1. Install the skills

Every skill is a plain folder in [`skills/`](skills): `skills/lantern` is the master skill with every colour, and `skills/lantern-<colour>` holds one colour each. Install the master skill, or just the colours you use.

**Claude Code, inside a session**, from this repository as a plugin marketplace:

```
/plugin marketplace add Amircode2050/lantern-design-system
/plugin install lantern@lantern-design-system
```

**Claude Code, from your terminal**, the same two steps without opening a session:

```bash
claude plugin marketplace add Amircode2050/lantern-design-system
claude plugin install lantern@lantern-design-system
claude plugin install lantern-teal@lantern-design-system
```

Update later with `claude plugin marketplace update lantern-design-system`, and remove a skill with `claude plugin uninstall lantern-teal@lantern-design-system`.

**claude.ai**: download the skill's zip from the [latest release](../../releases/latest), then upload it under **Settings, Capabilities, Skills**.

**Other coding agents.** The skills follow the open [Agent Skills](https://agentskills.io) format (a folder with a `SKILL.md`), so agents that read that format can use them unchanged, among them OpenAI Codex, Gemini CLI, GitHub Copilot and Cursor. The [`skills` installer](https://github.com/vercel-labs/skills) puts them in the right place for each agent:

```bash
npx skills add Amircode2050/lantern-design-system                          # choose skills and agents interactively
npx skills add Amircode2050/lantern-design-system --skill lantern -a codex -g # the master skill, for Codex, for all projects
```

Or copy a folder from `skills/` by hand into your agent's skills directory:

| Agent | This project only | Every project |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` |
| Gemini CLI | `.agents/skills/` | `~/.gemini/skills/` |
| GitHub Copilot | `.agents/skills/` | `~/.copilot/skills/` |
| Cursor | `.agents/skills/` | `~/.cursor/skills/` |

```bash
git clone https://github.com/Amircode2050/lantern-design-system
cp -r lantern-design-system/skills/lantern ~/.agents/skills/
```

Paths change as agents evolve, so check your agent's documentation if a skill does not appear. Whatever the agent, the skill draws with Python on your machine, so step 2 below applies to every agent. In agents that cannot show multiple-choice questions, the colour picker asks the same questions in plain text.

| Skill | What it does |
|---|---|
| `lantern` | Shows the picker, asks for colour, variant, type set and shade, can add new colours, exports tokens. |
| `lantern-black` | Black only: a jet near-black ground (#1C1C1E) in neutral greys, with one metallic-gold light. |
| `lantern-white` | White only: ivory paper (#FAF8F2) in strict monochrome: ink on paper, the light is plain white. |
| `lantern-blue` | Blue only: a deep navy ground built from shades of the core colour #3366FF, with one amber light and a teal support family. |
| `lantern-purple` | Purple only: a deep violet ground, with one warm peach light and a blue support family. |
| `lantern-green` | Green only: a deep forest-green ground (#1B4D3E), with one amber light. |
| `lantern-red` | Red only: a deep maroon ground (#7A1F2B), with one champagne-gold light. |
| `lantern-gray` | Gray only: a charcoal ground (#36454F), with one amber light. |
| `lantern-teal` | Teal only: a deep teal ground (#0F766E), with one amber light. |
| `lantern-gold` | Gold only: a warm near-black ground with metallic gold (#D4AF37) as the light. |
| `lantern-orange` | Orange only: a warm near-black ground with burnt orange (#CC5500) as the brand colour and tangerine as the light. |
| `lantern-cyan` | Cyan only: a vivid deep-cyan ground built from bright cyan (#1CABE2), with one amber light. |
| `lantern-rose` | Rose only: a deep rose ground (#C2185B), with one champagne-gold light. |

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
| [Black](#black) | Jet `#1C1C1E` | metallic-gold light | Classic | dark | keynotes, launches and premium reports |
| [White](#white) | Ivory `#FAF8F2` | white light, ink only | Editorial | light | print, documents and bright rooms |
| [Blue](#blue) | Blue `#3366FF` | amber light | Classic | dark | technology, science and finance |
| [Purple](#purple) | Purple `#6A57B8` | warm peach light | Classic | dark | ideas, research and storytelling |
| [Green](#green) | Forest `#1B4D3E` | amber light | Classic | dark | sustainability, health and growth |
| [Red](#red) | Maroon `#7A1F2B` | champagne light | Editorial | dark | strategy, culture and history |
| [Gray](#gray) | Charcoal `#36454F` | amber light | Modern | dark | engineering, operations and data |
| [Teal](#teal) | Deep teal `#0F766E` | amber light | Modern | dark | healthcare, water and calm explainers |
| [Gold](#gold) | Metallic gold `#D4AF37` | gold light on near-black | Classic | dark | awards, finance and luxury brands |
| [Orange](#orange) | Burnt orange `#CC5500` | orange light on near-black | Modern | dark | energy, product launches and bold talks |
| [Cyan](#cyan) | Bright cyan `#1CABE2` | amber light | Modern | dark | digital products, cloud and fresh decks |
| [Rose](#rose) | Rose `#C2185B` | champagne light | Editorial | dark | culture, wellbeing and consumer brands |

Every theme follows the same rules: a deep ground, a structure ramp built from the core colour, exactly one accent (the light) and a support colour reserved for natural things such as water. Text colours are fitted to WCAG contrast in both variants.

### Black

<p align="center"><img src="docs/images/colors/black.jpg" alt="Black in dark and light, with type sets and shade options" width="100%"></p>
<p align="center"><img src="docs/images/ramps/black.png" alt="Black shade ramp from 50 to 950" width="100%"></p>

A jet near-black ground (#1C1C1E) in neutral greys, with one metallic-gold light. Best for keynotes, launches and premium reports.

- **Skill:** `lantern-black`, or `lantern` and pick Black. It also answers to: jet, onyx, ebony, noir, black and gold.
- **Defaults:** dark variant, Classic type set.
- **Other shades:** Onyx `#111111`, Rich black `#0B0B0C`.

<details>
<summary>Key tokens</summary>

| Token | Dark | Light |
|---|---|---|
| Ground (centre to edge) | `#1f1f21` `#0c0c0d` `#040404` | `#ffffff` `#f4f4f4` `#e3e3e4` |
| Text primary / secondary | `#f2f2f2` / `#c1c1c2` | `#1f1f20` / `#424243` |
| The light (accent text) | `#f9d461` | `#7b6201` |
| Information flows | `#d6d6d6` | `#5b5b5d` |
| Support (water) | `#90e1e5` | `#007f84` |
| Button fill / text | `#1c1c1e` / `#ffffff` | `#1c1c1e` / `#ffffff` |
| Shade ramp 50 to 950 | `#f5f5f5` `#e8e8e8` `#d4d4d5` `#bababc` `#98989a` `#77777a` `#5a5a5d` `#454546` `#303031` `#1c1c1e` `#0f0f10` | same |

</details>

### White

<p align="center"><img src="docs/images/colors/white.jpg" alt="White in dark and light, with type sets and shade options" width="100%"></p>
<p align="center"><img src="docs/images/ramps/white.png" alt="White shade ramp from 50 to 950" width="100%"></p>

Ivory paper (#FAF8F2) in strict monochrome: ink on paper, the light is plain white. Best for print, documents and bright rooms.

- **Skill:** `lantern-white`, or `lantern` and pick White. It also answers to: ivory, porcelain, paper, cream, black and white.
- **Defaults:** light variant, Editorial type set.
- **Other shades:** Porcelain `#F7F7F5`, Pure white `#FFFFFF`.

<details>
<summary>Key tokens</summary>

| Token | Dark | Light |
|---|---|---|
| Ground (centre to edge) | `#302f2c` `#161513` `#090807` | `#fdfaf1` `#f4f4f3` `#e3e3e2` |
| Text primary / secondary | `#f2f2f1` / `#c2c1bf` | `#201f1d` / `#43423f` |
| The light (accent text) | `#d7d7d6` | `#656564` |
| Information flows | `#d6d6d4` | `#5d5b56` |
| Support (water) | `#d1d1d0` | `#6f6f6e` |
| Button fill / text | `#faf8f2` / `#191817` | `#faf8f2` / `#191817` |
| Shade ramp 50 to 950 | `#faf8f2` `#e8e8e7` `#d5d4d2` `#bbbab7` `#9a9894` `#797772` `#5c5b56` `#464541` `#31302e` `#201f1d` `#100f0e` | same |

</details>

### Blue

<p align="center"><img src="docs/images/colors/blue.jpg" alt="Blue in dark and light, with type sets and shade options" width="100%"></p>
<p align="center"><img src="docs/images/ramps/blue.png" alt="Blue shade ramp from 50 to 950" width="100%"></p>

A deep navy ground built from shades of the core colour #3366FF, with one amber light and a teal support family. Best for technology, science and finance.

- **Skill:** `lantern-blue`, or `lantern` and pick Blue. It also answers to: cobalt, royal blue, azure.
- **Defaults:** dark variant, Classic type set.
- **Other shades:** none.

<details>
<summary>Key tokens</summary>

| Token | Dark | Light |
|---|---|---|
| Ground (centre to edge) | `#2145b0` `#091e67` `#030f3b` | `#ffffff` `#eff4ff` `#d8e3ff` |
| Text primary / secondary | `#edf2fe` / `#a7c1fa` | `#071850` / `#1f3a8a` |
| The light (accent text) | `#ffd070` | `#975402` |
| Information flows | `#c3d6fe` | `#1e48d1` |
| Support (water) | `#90e1e6` | `#007f85` |
| Button fill / text | `#3366ff` / `#ffffff` | `#3366ff` / `#ffffff` |
| Shade ramp 50 to 950 | `#f1f5fe` `#dde8fe` `#c1d4fe` `#9ab9fe` `#6592ff` `#3366ff` `#1e47d1` `#1535a3` `#0d2576` `#071850` `#020b2f` | same |

</details>

### Purple

<p align="center"><img src="docs/images/colors/purple.jpg" alt="Purple in dark and light, with type sets and shade options" width="100%"></p>
<p align="center"><img src="docs/images/ramps/purple.png" alt="Purple shade ramp from 50 to 950" width="100%"></p>

A deep violet ground, with one warm peach light and a blue support family. Best for ideas, research and storytelling.

- **Skill:** `lantern-purple`, or `lantern` and pick Purple. It also answers to: violet, indigo, lavender.
- **Defaults:** dark variant, Classic type set.
- **Other shades:** none.

<details>
<summary>Key tokens</summary>

| Token | Dark | Light |
|---|---|---|
| Ground (centre to edge) | `#4c3da2` `#29185d` `#1b0832` | `#ffffff` `#f3f3fc` `#e2e0f9` |
| Text primary / secondary | `#f4efff` / `#c4b9ef` | `#201545` / `#423479` |
| The light (accent text) | `#fcd5ad` | `#a04e24` |
| Information flows | `#d7ceff` | `#5d40b5` |
| Support (water) | `#adbcf9` | `#3f51b5` |
| Button fill / text | `#6a57b8` / `#ffffff` | `#6a57b8` / `#ffffff` |
| Shade ramp 50 to 950 | `#f5f4fd` `#e7e5fa` `#d3cff4` `#b9b2ec` `#978bdd` `#6a57b8` `#5b49a1` `#45377d` `#302659` `#1f183c` `#0f0b22` | same |

</details>

### Green

<p align="center"><img src="docs/images/colors/green.jpg" alt="Green in dark and light, with type sets and shade options" width="100%"></p>
<p align="center"><img src="docs/images/ramps/green.png" alt="Green shade ramp from 50 to 950" width="100%"></p>

A deep forest-green ground (#1B4D3E), with one amber light. Best for sustainability, health and growth.

- **Skill:** `lantern-green`, or `lantern` and pick Green. It also answers to: forest, emerald, jade, sage, olive.
- **Defaults:** dark variant, Classic type set.
- **Other shades:** Emerald `#046C4E`, Jade `#00A86B`.

<details>
<summary>Key tokens</summary>

| Token | Dark | Light |
|---|---|---|
| Ground (centre to edge) | `#375a4e` `#172e26` `#0a1813` | `#ffffff` `#f1f5f3` `#dde6e2` |
| Text primary / secondary | `#f2f6f4` / `#b9cbc4` | `#12241d` / `#2f483f` |
| The light (accent text) | `#ffd070` | `#975402` |
| Information flows | `#cdd9d4` | `#396557` |
| Support (water) | `#aed5ff` | `#4373a3` |
| Button fill / text | `#1b4d3e` / `#ffffff` | `#1b4d3e` / `#ffffff` |
| Shade ramp 50 to 950 | `#f2f6f4` `#e1eae7` `#c8d9d2` `#a7c2b7` `#7ba294` `#528372` `#396556` `#1b4d3e` `#1c362e` `#11231d` `#07120e` | same |

</details>

### Red

<p align="center"><img src="docs/images/colors/red.jpg" alt="Red in dark and light, with type sets and shade options" width="100%"></p>
<p align="center"><img src="docs/images/ramps/red.png" alt="Red shade ramp from 50 to 950" width="100%"></p>

A deep maroon ground (#7A1F2B), with one champagne-gold light. Best for strategy, culture and history.

- **Skill:** `lantern-red`, or `lantern` and pick Red. It also answers to: maroon, burgundy, crimson, wine, oxblood.
- **Defaults:** dark variant, Editorial type set.
- **Other shades:** Burgundy `#800020`, Crimson `#A4161A`.

<details>
<summary>Key tokens</summary>

| Token | Dark | Light |
|---|---|---|
| Ground (centre to edge) | `#7d393e` `#45181b` `#260b0d` | `#ffffff` `#faf2f2` `#f1dede` |
| Text primary / secondary | `#f8f0f0` / `#deb6b6` | `#351315` / `#633133` |
| The light (accent text) | `#f6d196` | `#7e5f2a` |
| Information flows | `#eacece` | `#903c42` |
| Support (water) | `#90e1e5` | `#007f84` |
| Button fill / text | `#7a1f2b` / `#ffffff` | `#7a1f2b` / `#ffffff` |
| Shade ramp 50 to 950 | `#fcf3f2` `#f7e2e2` `#efcaca` `#e3a9aa` `#cf7e81` `#b5555b` `#903b42` `#7a1f2b` `#501e22` `#351215` `#1e0709` | same |

</details>

### Gray

<p align="center"><img src="docs/images/colors/gray.jpg" alt="Gray in dark and light, with type sets and shade options" width="100%"></p>
<p align="center"><img src="docs/images/ramps/gray.png" alt="Gray shade ramp from 50 to 950" width="100%"></p>

A charcoal ground (#36454F), with one amber light. Best for engineering, operations and data.

- **Skill:** `lantern-gray`, or `lantern` and pick Gray. It also answers to: grey, silver, charcoal, slate, graphite.
- **Defaults:** dark variant, Modern type set.
- **Other shades:** Slate `#475569`, Silver `#A8A9AD`.

<details>
<summary>Key tokens</summary>

| Token | Dark | Light |
|---|---|---|
| Ground (centre to edge) | `#48535b` `#222a2f` `#111619` | `#ffffff` `#f3f4f5` `#e1e4e6` |
| Text primary / secondary | `#f1f2f3` / `#bfc6ca` | `#1a2024` / `#3b4449` |
| The light (accent text) | `#ffd070` | `#975402` |
| Information flows | `#d2d6da` | `#4f5d67` |
| Support (water) | `#aed5ff` | `#4373a3` |
| Button fill / text | `#36454f` / `#ffffff` | `#36454f` / `#ffffff` |
| Shade ramp 50 to 950 | `#f4f5f6` `#e5e8eb` `#cfd5d9` `#b3bcc3` `#8d9ba4` `#6a7a85` `#4f5d67` `#36454f` `#293237` `#1a2024` `#0c1013` | same |

</details>

### Teal

<p align="center"><img src="docs/images/colors/teal.jpg" alt="Teal in dark and light, with type sets and shade options" width="100%"></p>
<p align="center"><img src="docs/images/ramps/teal.png" alt="Teal shade ramp from 50 to 950" width="100%"></p>

A deep teal ground (#0F766E), with one amber light. Best for healthcare, water and calm explainers.

- **Skill:** `lantern-teal`, or `lantern` and pick Teal. It also answers to: deep teal, petrol, teal green.
- **Defaults:** dark variant, Modern type set.
- **Other shades:** Petrol `#005F73`, Teal `#008080`.

<details>
<summary>Key tokens</summary>

| Token | Dark | Light |
|---|---|---|
| Ground (centre to edge) | `#1d5d57` `#01302c` `#011917` | `#ffffff` `#f0f5f4` `#d9e7e5` |
| Text primary / secondary | `#f2f7f7` / `#b0cdc9` | `#042522` / `#1d4b46` |
| The light (accent text) | `#ffd070` | `#975402` |
| Information flows | `#c7dbd8` | `#0d6962` |
| Support (water) | `#aed5ff` | `#4373a3` |
| Button fill / text | `#0f766e` / `#ffffff` | `#0f766e` / `#ffffff` |
| Shade ramp 50 to 950 | `#f0f7f6` `#dcece9` `#c0dbd7` `#99c5bf` `#63a79f` `#2b887f` `#0f766e` `#05504b` `#053934` `#032522` `#011311` | same |

</details>

### Gold

<p align="center"><img src="docs/images/colors/gold.jpg" alt="Gold in dark and light, with type sets and shade options" width="100%"></p>
<p align="center"><img src="docs/images/ramps/gold.png" alt="Gold shade ramp from 50 to 950" width="100%"></p>

A warm near-black ground with metallic gold (#D4AF37) as the light. Best for awards, finance and luxury brands.

- **Skill:** `lantern-gold`, or `lantern` and pick Gold. It also answers to: yellow, mustard, golden, ochre.
- **Defaults:** dark variant, Classic type set.
- **Other shades:** Antique gold `#C9A227`, Mustard `#E1AD01`.

<details>
<summary>Key tokens</summary>

| Token | Dark | Light |
|---|---|---|
| Ground (centre to edge) | `#282418` `#120f07` `#060502` | `#ffffff` `#f4f4f2` `#e4e3df` |
| Text primary / secondary | `#f2f2f0` / `#c4c1ba` | `#221f18` / `#464238` |
| The light (accent text) | `#f9d461` | `#7b6201` |
| Information flows | `#d8d6d0` | `#615b49` |
| Support (water) | `#90e1e5` | `#007f84` |
| Button fill / text | `#d4af37` / `#1b1812` | `#d4af37` / `#1b1812` |
| Shade ramp 50 to 950 | `#f8f5ed` `#eee8d5` `#e0d4b2` `#d4af37` `#b2953c` `#917407` `#6f5801` `#554302` `#3c2f00` `#281e00` `#150f00` | same |

</details>

### Orange

<p align="center"><img src="docs/images/colors/orange.jpg" alt="Orange in dark and light, with type sets and shade options" width="100%"></p>
<p align="center"><img src="docs/images/ramps/orange.png" alt="Orange shade ramp from 50 to 950" width="100%"></p>

A warm near-black ground with burnt orange (#CC5500) as the brand colour and tangerine as the light. Best for energy, product launches and bold talks.

- **Skill:** `lantern-orange`, or `lantern` and pick Orange. It also answers to: burnt orange, tangerine, persimmon, copper.
- **Defaults:** dark variant, Modern type set.
- **Other shades:** Persimmon `#E4572E`, Tangerine `#F28C28`.

<details>
<summary>Key tokens</summary>

| Token | Dark | Light |
|---|---|---|
| Ground (centre to edge) | `#302019` `#160c07` `#090403` | `#ffffff` `#f5f3f2` `#e7e2e0` |
| Text primary / secondary | `#f4f1f0` / `#cabfba` | `#261d19` / `#4d3f39` |
| The light (accent text) | `#ffcca5` | `#995304` |
| Information flows | `#dbd4d1` | `#6c554b` |
| Support (water) | `#90e1e5` | `#007f84` |
| Button fill / text | `#943c00` / `#ffffff` | `#943c00` / `#ffffff` |
| Shade ramp 50 to 950 | `#fdf3ee` `#fbe2d7` `#f6c9b5` `#eda888` `#dc7a4b` `#cc5500` `#943c00` `#722d01` `#521e01` `#381200` `#1f0700` | same |

</details>

### Cyan

<p align="center"><img src="docs/images/colors/cyan.jpg" alt="Cyan in dark and light, with type sets and shade options" width="100%"></p>
<p align="center"><img src="docs/images/ramps/cyan.png" alt="Cyan shade ramp from 50 to 950" width="100%"></p>

A vivid deep-cyan ground built from bright cyan (#1CABE2), with one amber light. Best for digital products, cloud and fresh decks.

- **Skill:** `lantern-cyan`, or `lantern` and pick Cyan. It also answers to: aqua, turquoise, sky blue.
- **Defaults:** dark variant, Modern type set.
- **Other shades:** Cyan `#0891B2`, Aqua `#00B4D8`.

<details>
<summary>Key tokens</summary>

| Token | Dark | Light |
|---|---|---|
| Ground (centre to edge) | `#066081` `#013144` `#011a26` | `#ffffff` `#ebf6fc` `#cce8f8` |
| Text primary / secondary | `#ffffff` / `#99d8f9` | `#012332` / `#034963` |
| The light (accent text) | `#ffd070` | `#975402` |
| Information flows | `#b2ddf4` | `#066486` |
| Support (water) | `#aed5ff` | `#4373a3` |
| Button fill / text | `#1cabe2` / `#001b28` | `#1cabe2` / `#001b28` |
| Shade ramp 50 to 950 | `#eef7fb` `#d8ebf6` `#b7daee` `#89c4e2` `#1cabe2` `#0882ae` `#016386` `#014c67` `#02354a` `#012331` `#00121b` | same |

</details>

### Rose

<p align="center"><img src="docs/images/colors/rose.jpg" alt="Rose in dark and light, with type sets and shade options" width="100%"></p>
<p align="center"><img src="docs/images/ramps/rose.png" alt="Rose shade ramp from 50 to 950" width="100%"></p>

A deep rose ground (#C2185B), with one champagne-gold light. Best for culture, wellbeing and consumer brands.

- **Skill:** `lantern-rose`, or `lantern` and pick Rose. It also answers to: pink, raspberry, magenta, fuchsia.
- **Defaults:** dark variant, Editorial type set.
- **Other shades:** Deep rose `#9E1450`, Blush rose `#D4708F`.

<details>
<summary>Key tokens</summary>

| Token | Dark | Light |
|---|---|---|
| Ground (centre to edge) | `#901d45` `#510020` `#2e0110` | `#ffffff` `#fdf0f2` `#f9dae0` |
| Text primary / secondary | `#fbeef0` / `#ecaeba` | `#3f0319` / `#721e39` |
| The light (accent text) | `#f6d196` | `#7e5f2a` |
| Information flows | `#f5c9d1` | `#a7084c` |
| Support (water) | `#90e1e5` | `#007f84` |
| Button fill / text | `#c2185b` / `#ffffff` | `#c2185b` / `#ffffff` |
| Shade ramp 50 to 950 | `#fef1f4` `#ffdee4` `#fdc2ce` `#f79cb0` `#e86789` `#c2185b` `#a7074b` `#820239` `#5d0327` `#3f0319` `#24010b` | same |

</details>


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
python build/check.py                 # contrast, names, interface contrast, engine copies
python build/readme_images.py         # the images on this page
python build/site.py                  # the playground in docs/ (GitHub Pages, deploy from /docs)
python src/scripts/deck.py all --out dist   # slide templates for a release
```

## Contributing, security and licence

Contributions are welcome, especially new colours and components: see [CONTRIBUTING.md](CONTRIBUTING.md). To report a vulnerability, see [SECURITY.md](SECURITY.md). Changes are listed in [CHANGELOG.md](CHANGELOG.md).

Lantern is licensed under the [Apache License 2.0](LICENSE). The bundled fonts (PT Serif, Inter, JetBrains Mono, Space Grotesk, Fraunces and Source Sans 3) keep their own SIL Open Font Licence; see [NOTICE](NOTICE).
