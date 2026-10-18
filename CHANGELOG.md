# Changelog

All notable changes to this project are recorded here. Versions follow [semantic versioning](https://semver.org): a new colour or component is a minor release, a change that breaks existing scenes or token names is a major one.

## 1.2.1

- `lantern-design-system.zip` on every release: the whole marketplace in one download, for installing in Claude Code without git (`claude plugin marketplace add ./lantern-design-system`).
- One install route per agent: Codex (`codex plugin marketplace add`), GitHub Copilot CLI, Gemini CLI (`gemini extensions install`), Cursor team marketplaces, OpenCode and Grok Build. The repo root is also an Agent Plugins plugin (`plugin.json`), a Gemini CLI extension and a Codex marketplace (`.agents/plugins/marketplace.json`).
- Install troubleshooting in the README: the full HTTPS address when SSH or checkout fails, and the Windows long-path setting.

## 1.2.0

- The 24 library scenes in Persian and Spanish: every title, answer, label and alt text, matched to the scene's own labels (`scenes.py bank fa`, `social.py ... es`, `build(name, lang=...)`). CI checks that every translation covers every scene.
- A Persian slide template, right to left throughout: right-to-left paragraphs, mirrored layouts, Persian digits, a chart that reads from the right, and Vazirmatn as the font. Persian templates for every colour are attached to the release.
- Right-to-left text that is centred or anchored to one side now keeps its place (social cards, credit lines).
- Polished portraits: natural hair that tapers into the nape, a notched lapel and a lit shoulder, a robot visor set into its recess, a chest panel, and bodies that run off the frame instead of floating.
- Unit tests (`python -m unittest discover -s tests`) for the colour maths, themes, brand colours, fonts, right-to-left text, scenes, translations and slide-template words, run in CI on Python 3.11 and 3.13.
- An evaluation suite in `evals/` that measures what the skill adds over plain Claude (colour first, the right scene, brand and Persian commands, the slide voice), run with `claude plugin eval skills/lantern`.
- Every SKILL.md carries the Agent Skills `license`, `compatibility` and `metadata` fields, and all skills pass the specification's validator.

## 1.1.0

- Four new type sets: **Technical** (IBM Plex), **Geometric** (DM Serif Display and DM Sans), **Garamond** (EB Garamond with Inter) and **Swiss** (Inter Tight with Inter), for seven in all.
- Many languages: accented Latin for Central and Eastern European languages, Turkish and Vietnamese; Cyrillic and Greek; and Arabic script (Persian, Arabic, Urdu) set right to left, with titles moving to the top right and every text block aligned to its right edge.
- Font packs: the master skill carries every font; colour skills carry the core fonts and add others with `python scripts/fonts.py add <pack>`, which downloads only pinned files and checks each against its recorded hash. `fonts.py verify` re-checks them, and CI checks every font in every skill.
- The renderer embeds only the script subsets a piece of text uses, so English slides render as lightly as before.
- `python scripts/examples.py languages` renders one slide in six languages and type sets.
- The picker, the playground and the README show all seven type sets; the README has a Languages section.

## 1.0.2

- Every skill folder is now a complete, self-contained plugin: it carries its own `.claude-plugin/plugin.json`, a README that says what it runs and connects to, and the `LICENSE` and `NOTICE` files, so a copied folder keeps its licence and each skill can be listed in plugin directories.
- The README opens with the playground: screenshots, what each part of the page does, and a link row under the title. The repository has a social preview image, which the playground also uses when its link is shared.
- Playground images are smaller (1280 pixels wide), which keeps the repository well under directory size limits.
- The minimum Pillow version is now 12.3.0, which carries recent security fixes.
- CI uses the current `actions/checkout` and `actions/setup-python`, still pinned to exact commits. Dependabot now raises a minimum version only when it has to.

## 1.0.1

Security and robustness.

- `brand.py` reads public web addresses only: local, private and non-web addresses are refused, every redirect is checked, and compressed pages are unpacked within the same 2 MB limit. `brand.py --selftest` checks this, and CI runs it.
- Websites that send compressed pages unasked are now read correctly.
- The master skill's description no longer trips a prompt-injection rule in skill scanners.
- CI actions are pinned to exact commits, with Dependabot keeping them current.
- Every skill now lives in its own folder under `skills/` (the Agent Skills layout), so it installs in Claude Code, Codex, Gemini CLI, GitHub Copilot, Cursor and other agents that read `SKILL.md`. Claude Code installs each skill straight from its folder. The README covers terminal installs and other agents.

## 1.0.0

First public release.

- Twelve colour themes: Black, White, Blue, Purple, Green, Red, Gray, Teal, Gold, Orange, Cyan and Rose, each with dark and light variants, an 11-step shade ramp and two alternative shades.
- The `lantern` master skill, which shows a two-step picker and asks for colour, variant, type set and shade, plus one skill per colour.
- A drawing engine and a library of about forty components for cut-away scenes and close-up portraits, including the hanging lantern.
- Three type sets (Classic, Modern, Editorial) with bundled fonts.
- Seamless GIF and MP4 loops with a seam check.
- A theme generator, a reference-image reader, token export to CSS and Tailwind, and a UI layer with eight components.
- A voice guide for words on slides and screens.
- Contrast checks for every text and flow colour in every theme.
- A scene library of 24 ready cut-aways (supply chain, data pipeline, data centre, power grid, the web, the cloud, a sales funnel and more), each with its words and each a seamless loop.
- `brand.py`: a complete theme from a website, a logo or a hex value, with previews and tokens.
- `social.py`: any scene as a square, 4:5 or 9:16 post, still or as an MP4 loop.
- `deck.py`: an editable ten-slide template for PowerPoint, Keynote and Google Slides in any colour, with a native chart; templates for every colour are attached to the release.
- Eleven new components for towns and utilities: house, road, truck, pylon, turbine, solar panel, tank, tree, shelf, bed and dish.
- A playground page for GitHub Pages where the whole page takes on the chosen colour.
