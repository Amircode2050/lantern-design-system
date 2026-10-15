# Colours, type sets and export

## What a theme is
One file in `themes/`, named after the colour (`themes/blue.json`). It holds the name, the core brand colour, the accent harmony, a default type set, and two variants (`dark`, `light`), each with `colors` (the role tokens) and `fx` (derived gradients and strengths). The kit lists whatever is in that folder: `colors()`.

`set_theme(variant, color, type_set)` selects all three; anything left out keeps its current value.

## Add a colour
```bash
python scripts/new_theme.py lilac "#8E7CC3" --preview out
python scripts/picker.py --all
```
1. `new_theme.py` builds both variants from the one colour, fits every text and flow colour to the contrast rules, stores the 50-950 ramp and a button-safe fill, writes `themes/lilac.json`, and with `--preview` renders the component sheet in dark and light.
2. Look at both previews. If the grounds are too light or too dark, re-run with `--deep`. If the light fights the brand colour, try `--accent` or another `--harmony`.
3. `picker.py --all` refreshes the overview (`assets/picker.jpg`) and every detail sheet (`assets/picker/<colour>.jpg`).
4. Show the previews to the user and get a yes before using the theme in real work.

| Option | Values | Use |
|---|---|---|
| `--harmony` | `warm` (default) | An amber light whatever the brand hue. Safest: it always reads as lamplight. |
| | `complementary` | The light sits opposite the brand hue. Strong contrast; check it does not turn the light green or violet. |
| | `analogous` | The light sits 40 degrees from the brand hue. Quiet, low contrast. |
| | `monochrome` | The light is a pale tint of the brand hue. For black, white and grey systems, where light is simply white. |
| `--accent` | `#rrggbb` or `core` | The exact colour of the light; overrides `--harmony`. `core` makes the brand colour itself the light. |
| `--ground-chroma` | number, default 1.0 | Scales how coloured the ground and structure are. About 0.2 gives a warm near-black, for gold, orange and yellow, whose own dark shades turn muddy brown. |
| `--deep` | number, default 1.0 | Scales the lightness of the dark grounds. About 0.55 for a near-black system. |
| `--type` | `classic`, `modern`, `editorial` | The type set the theme uses unless told otherwise. |
| `--default-variant` | `dark` or `light` | The variant recommended in the picker (White uses light). |
| `--label` | text | How the light is described in the picker, for example "champagne light". |
| `--shades` | `Name=#hex ...` | The family's shade options, current shade first. Shown in the picker detail sheet. |
| `--from` | theme name | Copy another theme's recipe (all of the above), to build another shade of the same family. |
| `--force` | | Overwrite an existing theme of the same name. |

How the installed themes were built (for rebuilding or adding shades):

| Theme | Core | Recipe |
|---|---|---|
| Blue | Blue #3366FF | hand-tuned, amber light |
| Purple | Purple #6A57B8 | hand-tuned, warm peach light |
| Black | Jet #1C1C1E | `--accent "#D4AF37" --deep 0.55 --type classic` |
| White | Ivory #FAF8F2 | `--harmony monochrome --deep 0.7 --type editorial --default-variant light` |
| Green | Forest #1B4D3E | amber light, `--type classic` |
| Red | Maroon #7A1F2B | `--accent "#D8B47A" --type editorial` (champagne) |
| Gray | Charcoal #36454F | amber light, `--type modern` |
| Teal | Deep teal #0F766E | amber light, `--type modern` |
| Gold | Metallic gold #D4AF37 | `--accent core --ground-chroma 0.22 --deep 0.6 --type classic` |
| Orange | Burnt orange #CC5500 | `--accent "#F28C28" --ground-chroma 0.22 --deep 0.6 --type modern` |
| Cyan | Bright cyan #1CABE2 | amber light, `--ground-chroma 1.6 --deep 1.05 --type modern` (saturated so it stays distinct from Teal) |
| Rose | Rose #C2185B | `--accent "#D8B47A" --type editorial` (champagne) |

Hand-tuning afterwards is fine: edit the JSON, then run `python scripts/kit.py`, which re-checks contrast for every installed theme.

Black and white systems: use a near-black or near-white core with `--harmony monochrome`. A neutral core has no hue, so the whole structure becomes grey and the light becomes white.

## Start from reference images
```bash
python scripts/intake.py ref1.png ref2.jpg
```
Prints the dominant colours of the images, the most characteristic one, the nearest installed theme, and the `new_theme.py` command to build a new theme from it when nothing installed is close. Use it when the user drops images and says "like this". Then read the images yourself for elements worth adding to the scene (the script only reads colour).

## Type sets
Defined in `system.json`; any set works with any colour.

| Set | Display | Sans | Mono | Mood |
|---|---|---|---|---|
| classic | PT Serif | Inter | JetBrains Mono | bookish, scholarly, calm |
| modern | Space Grotesk | Inter | JetBrains Mono | technical, crisp, product-like |
| editorial | Fraunces | Source Sans 3 | JetBrains Mono | magazine, expressive, warm |

The subtitle is italic in classic and editorial and upright in modern (Space Grotesk has no italic). To add a set: put the woff2 files in `assets/fonts/`, add the family under `fonts` in `system.json` (stack, average advance, files) and the pairing under `type_sets`, then run `python scripts/kit.py` and `python scripts/picker.py`.

The type scale, spacing steps and radii are also in `system.json`; `ts("title-lg")` returns a size.

## Export to code
```bash
python scripts/export.py blue out/blue --type classic --default dark
```
Writes five files:

| File | Contents |
|---|---|
| `tokens.css` | Every token as a CSS variable (including `--core-50` to `--core-950`), for both variants (`data-theme="dark"` or `"light"` on `<html>`), plus semantic variables (`--bg`, `--surface`, `--text`, `--primary`, `--accent-fg`, `--link` and so on), fonts, the type scale, spacing and radii. Variable names are the same for every colour, so changing colour is swapping this one file. |
| `fonts.css` | `@font-face` rules for the chosen type set with the fonts embedded. |
| `tailwind.theme.js` | A Tailwind `theme.extend` block that points at those variables. |
| `ui.css` | The UI layer. |
| `demo.html` | One page showing every UI component, with a variant switch. Open it to check a theme. |

## UI layer
`ui/ui.css` is small on purpose: type classes (`.t-title-lg`, `.t-subtitle`, `.t-answer`, `.t-lead`, `.t-body`, `.t-credit`, `.t-data`), layout helpers (`.stack`, `.row`, `.grid`), and eight components.

| Component | Classes | Rule |
|---|---|---|
| Button | `.btn`, `.btn-primary`, `.btn-ghost` | One primary per view. Primary uses the core colour. The accent is never a button colour. |
| Card | `.card` | Surface, hairline border, radius 12. |
| Field | `.field`, `.input`, `.hint`, `.error` | Label above, hint or error below. Errors say what to do. |
| Table | `.table`, `.num` | Numbers in mono, right-aligned. |
| Tag | `.tag`, `.tag-accent`, `.tag-ok`, `.tag-err` | Status always carries a word; the error dot is square so it does not rest on colour. |
| Callout | `.callout` | The one block the accent may mark. One per view. |
| Stat | `.stat` | Label, mono value, optional accent unit, delta in words. |
| Slide | `.slide`, `.slide-foot` | A 16:9 frame with the system's radial ground, for decks built in HTML. |

The accent keeps its meaning in UI: it marks the one thing to look at (the answer line, one callout, one unit in a stat). The core colour carries actions. Everything else is ground, surface and text.

No logo slot is defined yet; leave the corner clear.
