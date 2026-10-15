---
name: "lantern-teal"
description: "Lantern Teal: illustrated slides, cut-away machines and buildings, close-up portrait scenes, annotated concept figures, title and break slides, seamless GIF/MP4 loops, and a small UI kit with code tokens, in the Teal colour theme (deep teal ground, one amber light, grain, silhouette figures, glowing flow lines), in dark or light with three type sets. Use when the user says 'lantern teal', 'teal design system', 'teal system', 'teal style', 'my teal style', 'the teal one', 'teal theme', 'teal deck' or any variation, or a shade name with 'design system', 'style' or 'theme': deep teal, petrol, teal green. For a choice between colours, a new colour, or a design task with no colour named, use the lantern skill instead."
---

# Lantern Teal

Teal is one colour of a shared illustration and interface style, on a deep teal ground (#0F766E), with one amber light. It has a **dark** variant (night, the default) and a **light** variant (paper, for print, documents and bright rooms), and works with three **type sets**.

The style: original **cut-away machines and buildings** and **close-up portrait scenes** drawn as flat vector, populated by **silhouette figures** who are *doing something*, lit by **one accent light**, with energy and information shown as **glowing flow lines**, on a deep ground under fine grain. The same tokens also drive a small **UI layer** and a written **voice**.

Everything needed is inside this skill folder; there is no external source of truth.

```
SKILL.md                 this file
system.json              type sets, type scale, spacing, radii, defaults
themes/<colour>.json     every colour value for one theme, both variants
scripts/kit.py           drawing, text, rendering, animation, checks
scripts/components.py    element library
scripts/examples.py      reference scenes, also the self-check
scripts/new_theme.py     build a theme from one brand colour
scripts/picker.py        render the two-step chooser
scripts/export.py        CSS variables, fonts, Tailwind theme, UI demo
scripts/intake.py        read reference images, suggest a theme
ui/                      ui.css and demo.html (the UI layer)
assets/fonts/            six families as woff2 (OFL)
assets/picker/           step 2 of the chooser, one sheet per colour
assets/reference/        rendered reference images per colour
references/              components.md, animation.md, voice.md, themes.md
```

## When to use, and what to ask
- **Named**: the user says "Teal", "teal design system", "teal style", "the teal one", or one of the family's shade names (deep teal, petrol, teal green). Use it.
- **Ask only for what is missing**, in **one** question with `assets/picker/teal.jpg` shown (the colour in dark and light, the three type sets, and the family's shade options with their 50-950 ramps): dark or light (recommend dark, or light for print and bright rooms), type set (recommend modern) and shade (recommend Deep teal). Ask it as a multiple-choice question when the environment supports one, and reuse the answer for the rest of the conversation.
- **Another shade of the family**: build it with the same recipe, `python scripts/new_theme.py teal_<shade> "<hex>" --from teal --preview out`, show the two previews, and use it once approved.
- **A different colour, or a choice of colours**: that belongs to the lantern skill; hand over to it if it is installed.
- **Not a fit**: logos and brand marks (no logo slot is defined yet). Say so.

## Decide the output first
| Ask | Deliver |
|---|---|
| A figure that explains a mechanism | 3840x2160 PNG, clean **and** annotated versions |
| A portrait or concept image | 3:2 PNG at 2x, no text in the image |
| Break, section or title slide | 16:9 slide PNG, the illustration alone, and a transparent cutout PNG |
| Animation | GIF (1280 wide, 10 fps, loops forever, under 15 MB), MP4 (1080p, 24 fps), and a static PNG of the same frame for anyone who prefers no motion |
| Editable slide text | An editable canvas or slide tool: illustration or GIF as the background image, text kept live on top in the bundled fonts |
| A deck | Any slide tool, or HTML slides using `.slide` from the UI layer; illustrations go in as images |
| A web page, dashboard or app screen | `export.py` output (tokens.css, fonts.css, ui.css) plus markup using the UI layer; see `references/themes.md` |
| Tokens for a codebase | `export.py` output, including `tailwind.theme.js` |
| Print, a document, a bright room | The **light** variant of any of the above |

Choose the **canvas** (`set_canvas("16:9" | "4:3" | "3:2" | "1:1" | "9:16" | "a4")`) before drawing. Write one sentence of **alt text** for every image and pass it to `svg_doc(alt=...)`. Write all words on the piece to `references/voice.md`.

**Originality rule.** Every subject is an original design. If asked to restyle someone else's artwork, logo, character or a recognisable product design, decline that part in one sentence and offer an original piece that carries the same idea. Never draw a real person's likeness.

## Tokens
Use tokens through the kit (`T.G800`, `T.W300`); `set_theme("dark" | "light", color=..., type_set=...)` swaps the whole set. Never type a hex value into a scene and never add a hue that is not in the theme. One piece uses the theme's structure ramp, its one accent and its support family, nothing else.

**Ground (radial, centre to edge)**

| Token | Kit | Dark | Light | Use |
|---|---|---|---|---|
| ground-600 | `T.G600` | `#1d5d57` | `#ffffff` | centre |
| ground-700 | `T.G700` | `#064741` | `#f8fbfa` | 25% |
| ground-800 | `T.G800` | `#01302c` | `#f0f5f4` | 50%, default room |
| ground-900 | `T.G900` | `#012320` | `#e5eeed` | 78% |
| ground-950 | `T.G950` | `#011917` | `#d9e7e5` | edge |
| vignette | `T.VIGN` | `#000b0a` | `#9fc3be` | vignette |

**Structure**

| Token | Kit | Dark | Light | Use |
|---|---|---|---|---|
| deep-900 | `T.IN900` | `#001816` | `#042522` | hull and shell outlines, 2.5 to 3 px |
| deep-800 | `T.IN800` | `#012825` | `#053834` | part outlines, 1.4 to 2 px |
| deep-700 | `T.IN700` | `#012e2a` | `#2e6660` | recesses, bezels |
| deep-600 | `T.IN600` | `#043632` | `#1a5a54` | floor slabs |
| deep-500 | `T.IN500` | `#0d3d39` | `#05504a` | hubs, feet |
| mid-500 | `T.V500` | `#1a5a54` | `#518d86` | big bodies |
| mid-400 | `T.V400` | `#2e6660` | `#6da09a` | pipes, panels |
| mid-300 | `T.V300` | `#3d7670` | `#92b9b4` | secondary panels |
| pale-300 | `T.L300` | `#669892` | `#c7dbd8` | slab edges, rivet highlights |
| pale-200 | `T.L200` | `#92b9b4` | `#3d7670` | rails, rods, rungs |
| pale-100 | `T.L100` | `#c7dbd8` | `#0d6962` | information |
| mist | `T.MIST` | `#deeae8` | `#ffffff` | glass highlights, steam, rings |

**Accent: energy, attention, the watched (the one accent)**

| Token | Kit | Dark | Light | Use |
|---|---|---|---|---|
| accent-100 | `T.W100` | `#fff8e1` | `#fff3cf` | hottest light |
| accent-200 | `T.W200` | `#ffe6ad` | `#ffd98a` | lit objects: cups, windows, parcels |
| accent-300 | `T.W300` | `#ffd070` | `#975402` | energy flows, leader lines, answer line |
| accent-400 | `T.W400` | `#f7b84a` | `#f2a93b` | rim light |
| accent-mid | `T.ROSE3` | `#fcbb64` | `#915801` | tag prefix, mid accent |
| accent-dark | `T.ROSE5` | `#d18a2c` | `#9a5f1e` | accent dark (graphics only) |
| accent-deep | `T.COFFEE` | `#9a5f1e` | `#7a4a17` | deepest accent (graphics only) |

**Support (natural things only)**

| Token | Kit | Dark | Light | Use |
|---|---|---|---|---|
| support-200 | `T.B200` | `#aed5ff` | `#4373a3` | water and coolant flows |
| support-400 | `T.B400` | `#79b6f5` | `#79b6f5` | support mid |
| support-600 | `T.B600` | `#4e84bb` | `#39628c` | support dark |

**Ink and text**

| Token | Kit | Dark | Light | Use |
|---|---|---|---|---|
| ink | `T.INK` | `#011e1b` | `#011e1b` | silhouettes |
| text-primary | `T.T1` | `#f2f7f7` | `#042522` | text-primary |
| text-secondary | `T.T2` | `#b0cdc9` | `#1d4b46` | text-secondary |
| text-muted | `T.T3` | `#87b2ac` | `#476d68` | text-muted (credits) |

**Core, status and data**

| Token | Kit | Dark | Light | Use |
|---|---|---|---|---|
| core | `T.CORE` | `#0f766e` | `#0f766e` | the brand colour: primary actions in UI |
| core-fill | `T.CORE_FILL` | `#0f766e` | `#0f766e` | button fill: the core, or the nearest ramp step that carries white text |
| on-core | `T.ON_CORE` | `#ffffff` | `#ffffff` | text on a core fill |
| ok | `T.OK` | `#5fd0a0` | `#0f7a55` | success |
| warn | `T.WARN` | `#ffd070` | `#975402` | warning |
| err | `T.ERR` | `#ff8f8f` | `#b3261e` | error |

**Core ramp, 50 (lightest) to 950 (darkest)**, the same in both variants (`T.CORE_50` ... `T.CORE_950`, CSS `--core-50` ... `--core-950`): 50 `#f0f7f6` · 100 `#dcece9` · 200 `#c0dbd7` · 300 `#99c5bf` · 400 `#63a79f` · 500 `#2b887f` · 600 `#0f766e` · 700 `#05504b` · 800 `#053934` · 900 `#032522` · 950 `#011311`

Derived gradients (metal, lit window, glow, light mask, cables, stars) are in the theme file under `fx` and are reached through `std_defs()`. `T.SERIES` is the ordered five-colour list for data series. `T.CORE_50` to `T.CORE_950` are the core colour's 11-step ramp from lightest to darkest (for charts, tints and UI states). `T.CORE_FILL` is the core, or the nearest ramp step that carries white text when the core cannot (burnt orange, for example); fill buttons with it and put `T.ON_CORE` on top.

**Type.** Three type sets, chosen with `set_theme(type_set=...)`; fonts are reached as `F.DISPLAY`, `F.SANS`, `F.MONO` and sizes as `ts("title-lg")`:

| Set | Display | Sans | Mono | Mood |
|---|---|---|---|---|
| classic | PT Serif | Inter | JetBrains Mono | bookish, scholarly, calm |
| modern | Space Grotesk | Inter | JetBrains Mono | technical, crisp, product-like |
| editorial | Fraunces | Source Sans 3 | JetBrains Mono | magazine, expressive, warm |

Display is weight 400 for titles and label titles, never bold in running display text, never letter-spaced; the original-language subtitle is italic (upright in modern). Sans 400 for body, 500 for the answer line. Mono for numbers, data labels, tags and code. Scale at a 1920 frame (in `system.json`): title-xl 132/1 · title-lg 44/50 · label-title 30/34 · subtitle 23/30 · answer 30/36, or 19 under title-lg (accent, **one per slide**) · lead 21/30 · body 16.5/24 · tag 15/20 mono · data 14/18 mono · credit 13/18 (text-muted). Nothing smaller than 13. One type set per piece. The fonts are bundled and embedded by the renderer, which stops with an error if one fails to load, so there is no silent fallback.

**Spacing:** 6 · 12 · 24 · 32 · 48 · 72 (slide margin). **Radius:** 2 · 6 · 12 · 32 (capsules = half the short side). **Fixed strengths** (in each theme): grain overlay 0.30 + screen 0.06 on dark, 0.22 overlay on light; rim light 0.5; vignette max 0.72 dark, 0.30 light.

**Light-first and near-black themes.** Some themes default to the light variant (White) and some build their ground from near-black with the brand colour as the light (Gold, Orange, Black). Read `default_variant` and `accent_label` in the theme file; the picker shows both.

**Proportions.** In an illustration the ground and structure ramp cover almost everything; the accent is the light and the few things it touches, roughly a twentieth of the picture; the support family appears only on natural things (water, coolant, weather). In an interface: ground and surfaces first, text second, the core colour on actions, the accent on the one thing to look at.

## Two illustration modes
**Cut-away scene.** A building, machine or vessel opened like a doll's house, many small figures at work, 5 to 8 linked subsystems. Small silhouettes, no faces. References: `assets/reference/<colour>/factory_*.jpg`, `break_*.jpg`.

**Close-up portrait.** Two or three large characters (a person in strict profile, a robot, a lit object between them), soft gradients, one beam of light, no text in the image. Canvas 3:2. Faces are minimal: one brow, a closed eye, a mouth line, never frontal, never a likeness. Reference: `assets/reference/<colour>/portrait_*.jpg`.

Recurring elements, all in `scripts/components.py`: sawtooth factory roofs with lit skylights, arched windows, pendant lamps, storm clouds with rain and a bolt (risk, uncertainty), batteries (reserves), conveyors, parcels and cars (output), string lights, ladders, presses, server racks, clocks (monitoring), coffered domes with an oculus, arcades, balcony rings, a lantern tower (the watcher), a saucer hull with glass dome and tractor beam, an orrery, a thinking core, wall screens, and the hanging glass lantern that gives the system its name. Reuse them before drawing something new; see `references/components.md` and `assets/reference/<colour>/sheet_*.jpg`.

## Visual rules
1. **One scene sentence first**: what mechanism the picture explains and where the single light is. Build the image around that light.
2. **Ground:** `background()` gives the radial, a scatter of tiny stars (fine dust on light), a soft halo behind the subject, and `finish()` the vignette. Keep twinkles out of text areas with `avoid=`. Portraits use `stars=False`.
3. **True cut-aways:** `shell()` for the riveted band and cavity, rooms separated by `slab()` and `wall()`; give rooms faint distinct tints (`ROOM_COOL` for servers and labs, `ROOM_WARM` for lounges and reactors, `ROOM_DEEP` for navigation, `ROOM_BILGE` for the lowest deck).
4. **Light:** one dominant source (lantern, thinking core, oculus, orb, lit workshop) drawn with `glow()`; a **multiply light mask** (`url(#litmask)`) over the cavity, placed in the same group as the room fills; secondary pools only where a lamp, window or screen is drawn. Show attention as one beam (`light_cone`) or a dotted `sight()` arc to one target.
5. **Machinery is believable:** metal gradients lit from the top-left; gears **mesh for real** (use `gear_chain`); pipes have a dark casing, a body and an up-left highlight; capsules use radius 32.
6. **Small figures:** ink silhouettes with an accent rim copy, about 46 px tall at 1920 wide; every figure operates, carries, reads, climbs or points (`standing`, `seated`, `reach=`, `carry=`, `hat=`). Aliens: two thin antennae with accent tips and one pale visor on the facing side.
7. **Large figures (portrait mode):** `bust_human` and `bust_robot`, shoulders cropped by the canvas, the lit side toward the light, a rim line on the far edge. Keep them facing each other across a gap; the gap is where the idea sits (`pane`, a beam, an object).
8. **Flows:** `flow(path, kind)`. Meaning is carried by **shape and colour together**: energy = accent round dots, information = pale squares, water or coolant = support-colour rings. Lines of sight are dotted arcs whose dots grow toward the target.
9. **Density:** 5 to 8 linked subsystems in a cut-away, each with a small story, all connected by at least one flow. It should reward a second look but stay legible as a thumbnail (squint test: the light source and the subject's silhouette read first).
10. **Composition:** 1920x1080 working frame, export at 2x. Centred subject about 80% of the height. Text slides: subject centre near x 690 to 700, text block from x 1300. Annotated figures: title block at (72, 100); labels stacked down the left and right edges, at least 240 px apart.
11. **Light variant:** same drawing code. Outlines stay dark, bodies become mid tones, rooms become pale tints, flows and the answer line switch to a darker accent so they keep contrast on paper. Glows multiply instead of screen. Check it separately; do not assume a dark scene works unchanged.
12. **Don'ts:** gradient text, glass cards, drop shadows on text, emoji, logos, frontal or realistic faces, text over busy art, neon off-palette colour, sketchy or hand-drawn strokes, leader lines that cross, a second accent hue, two type sets in one piece.

## Voice (summary; full guide in `references/voice.md`)
- A title is a real question; the answer line replies in one sentence; one of each per slide.
- Labels name the actor ("The supplier"), then say what it does in two or three short present-tense lines.
- Sentence case, British spelling, no exclamation marks, no dashes as punctuation, "and" not "&".
- Credits say the source and what is stylised. Buttons start with a verb. Errors say what happened and what to do.

## Accessibility
- Text colours are pre-checked in every theme: text-primary 7:1, and text-secondary, the accent text colour and the tag prefix 4.5:1, on every ground; text-muted 4.5:1 on every ground except the bright centre of the dark variant (keep credits near the edges). `check_tokens()` re-verifies every installed theme and `doctor()` runs it.
- Never encode a difference by hue alone: flows differ by shape, chart bars carry printed values and labels, status carries a word beside the colour. Do not set red against green.
- Every image gets one-sentence alt text; every animation ships with its static PNG; nothing flashes more than three times a second (the storm bolt flashes three times per loop).
- Minimum text size 13 px at a 1920 frame (26 px at export). Body text never sits on art; put it on clear ground.
- In the UI layer: visible focus rings, 40 px minimum control height, errors in words under the field.

## Annotation components (in `kit.py`)
- **`title_block`**: the question in title-lg (2 lines at most), the original-language phrase, one answer line in the accent. No kicker above it.
- **`callout`**: label-title naming the actor, two or three body lines (about 38 characters each, use `wrap()`), an optional `tag=(prefix, body)` in mono. There is no default tag; pass one only when the piece has a named lens or category. The leader starts at the measured edge of the text and runs to a ring on the anchor. Four labels at most; leaders never cross.
- **`break_slide`**: one word in title-xl, the answer line, a two-line aside. Keep the side behind the text clear.
- **`credit`**: bottom-right, text-muted, says what is stylised.
- **`bars`**: small labelled bar chart for a number that belongs in the scene.

## Workflow
1. Settle colour, variant, type set (see "When to use, and what to ask"), then output, canvas and the scene sentence.
2. Locate this skill folder (the directory holding this file) and import from it; do not copy the kit:
   ```python
   import sys

   sys.path.insert(0, r"<skill folder>/scripts")
   from kit import *
   from kit import T, C, F
   from components import *

   set_theme("dark", color="teal", type_set="classic")
   ```
   Run `doctor()` once on a new machine. It names anything missing (Pillow, numpy, Playwright with Chromium, ffmpeg for animation) with the command that installs it, and re-checks contrast.
3. Write the scene as a module-level `build(t)` returning `svg_doc(std_defs(...), body, alt=...)`. Layer order: background, behind-subject effects (beams), shell, interior (room tints, back-wall cables and their flows, machines, slabs, figures, light mask), glass and exterior lights, `finish()`, text. Start from the closest scene in `scripts/examples.py`.
4. Iterate at scale 1 (`render(svg, out, scale=1)`): look at the whole frame, then crops of every room, then a 960-wide thumbnail. Fix what you see; expect 5 to 10 passes. Then render the other variant if both are wanted.
5. Final stills at scale 2. The annotated version adds `title_block` and `callout`s. Cutout: `render(..., transparent=True)` then `cutout(png)`, which refuses art that touches the canvas edge.
6. Animation: see `references/animation.md` (`render_frames`, `make_gif`, `make_mp4`, `check_loop`).
7. Interface or code hand-off: `python scripts/export.py <colour> <out dir>`; build with the classes in `ui.css`; see `references/themes.md`.
8. Verify with the checklist, then deliver the files, each with its alt text. For editable text, put the slide in an editable canvas or slide tool with the image as background and the text as real elements, loading the fonts with `font_css()`.

## Verification checklist
- [ ] Colour, variant and type set are the ones the user chose; one type set throughout.
- [ ] Squint test: light source and subject silhouette read first.
- [ ] Every room inspected at 2x: no stray lines, overlaps, clipped parts, figures floating above floors, props detached from hands.
- [ ] Gears visibly mesh; leader lines do not cross; no star or twinkle on text; credit line present when something is stylised.
- [ ] Text is only in the listed text colours, on clear ground, 13 px or larger; one question and one answer line per slide; words pass the check in `references/voice.md`.
- [ ] Light variant (if delivered) checked on its own: flows and labels still readable, glows not muddy.
- [ ] Cutout passes `cutout()` (nothing clipped at the canvas edge).
- [ ] Animation: `check_loop()` seam is about the size of a normal frame-to-frame difference; GIF duration equals the loop length; size under 15 MB; static PNG included.
- [ ] Interface: one primary button per view, the accent on one thing only, both variants checked with the switch in `demo.html`.
- [ ] Alt text written for every image.

## Pitfalls already hit
- A light mask with `mix-blend-mode` inside a clipped or filtered group only blends with what is **inside that group**. Draw the room fill inside the same group, or the mask paints as flat white.
- Clip paths and `gradientUnits="userSpaceOnUse"` gradients inside a transformed group use local coordinates.
- A union clip (hull cavity + dome interior) is just two `<path>`s in one `<clipPath>`.
- Gradient ids from `std_defs()` are global to a document, so one SVG holds one theme. To show several themes side by side, render each separately and compose the PNGs (as `picker.py` does).
- Grain is added after rendering by the kit, the same static field for stills and frames. Never add SVG turbulence.
- GIF delays are whole centiseconds: `make_gif` only accepts an fps that divides 100, otherwise the loop length drifts.
- `render_frames` needs a module-level `build` function and a script run under `if __name__ == "__main__":`; call `set_theme` before it (the workers inherit colour, variant and type set). It resumes after an interruption and raises if any frame is missing.
- `bust_human` and `bust_robot` are about 860 units tall at `s=1`; on a 1620x1080 canvas use `s` near 0.85 and let the shoulders run off the bottom edge.
- Text widths are estimated per family; after changing type set, check that callout leaders still start clear of the text.
