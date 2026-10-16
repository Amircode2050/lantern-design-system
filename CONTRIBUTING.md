# Contributing

Thanks for helping. Lantern is small on purpose, so the most useful contributions are new colours, new components, fixes and better examples.

## Set up

```bash
python -m venv .venv
. .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt ruff
python -m playwright install chromium
python src/scripts/kit.py       # should print "ready"
```

ffmpeg is only needed if you touch animation.

## Where things live

Everything in `skills/` and `.claude-plugin/` is generated. Edit the source, then rebuild:

| To change | Edit |
|---|---|
| Drawing, rendering, export | `src/scripts/` |
| A colour | its recipe in `build/themes.py` (Blue and Purple are hand-tuned in `src/themes/`) |
| Fonts, type scale, spacing | `src/system.json` and `src/assets/fonts/` |
| UI components | `src/ui/` |
| The scene library | `src/scripts/scenes.py` |
| The playground | `build/templates/site.html`, then `python build/site.py` |
| What the skills say | `build/templates/` |
| This README | `build/templates/README.md`, then `python build/readme.py` |

```bash
python build/themes.py red       # after changing a recipe
python build/build.py            # re-renders reference images (about ten minutes)
python build/build.py --skip-render   # code and docs only
python build/check.py            # contrast, names, engine copies
ruff check src/scripts build && ruff format src/scripts build
```

## Adding a colour

1. Try it: `python src/scripts/new_theme.py lilac "#8E7CC3" --preview out`, then look at both previews.
2. Add the recipe to `build/themes.py` and an entry to `COLORS` in `build/build.py` (name, ground, light, one-line description, aliases).
3. Run `python build/themes.py lilac`, then `python build/build.py`.
4. Add a line to `BEST_FOR` in `build/readme.py`, run `python build/readme.py` and `python build/readme_images.py`, and add a line to `CHANGELOG.md`.

## Adding a component

Put it in `src/scripts/components.py`. Follow the existing ones: return an SVG string, read colours only from `T`, take `p` (loop phase) if anything moves and move in whole cycles, and write a one-line docstring, which becomes the reference entry. Show it on the component sheet in `examples.py`.

## Adding a scene

Add a function to `src/scripts/scenes.py` with the `@scene(...)` decorator: a question of at most two lines, one answer line, three labels and one sentence of alt text, all written to the voice guide. Draw on the ground line `BASE` with `building()` and the components, put one light where the story is (`lit=`), and return the drawing with a dictionary of label anchors. Check it in dark and light and in two or three colours (`python src/scripts/scenes.py <name> teal light`); leader lines must not cross. `python build/check.py` confirms every label has its anchor.

## Tests and evaluations

```bash
python -m unittest discover -s tests -v     # fast, no browser: colour maths, fonts, right-to-left, scenes, words
python build/check.py                       # contrast, names, fonts, translations, engine copies
claude plugin eval skills/lantern --runs 1 --trust-plugin --no-publish   # what the skill adds over plain Claude
```

The evaluation suite in `evals/` runs each case with and without the skill and reports the difference. It uses your Claude plan, needs Claude Code 2.1.269 or later, and is not part of CI. Add a case when you add a capability: a realistic request in `prompt.md` and one or two graders that check the result.

## Pull requests

- One topic per pull request.
- Run the commands above; CI runs the same ones.
- Include a before and after image for anything visual.
- Words on slides, docs and errors follow `build/templates/voice.md`: sentence case, British spelling in prose, no dashes as punctuation.

## Releasing (maintainers)

Bump `VERSION` in `build/build.py`, add a section to `CHANGELOG.md`, commit, then run `python build/release.py`. It checks, rebuilds, and creates the repo and per-plugin tags locally; pushing and publishing the release are done by hand.

## Conduct

Be kind and specific. Critique work, not people.
