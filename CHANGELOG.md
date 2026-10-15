# Changelog

All notable changes to this project are recorded here. Versions follow [semantic versioning](https://semver.org): a new colour or component is a minor release, a change that breaks existing scenes or token names is a major one.

## 1.0.1

Security and robustness.

- `brand.py` reads public web addresses only: local, private and non-web addresses are refused, every redirect is checked, and compressed pages are unpacked within the same 2 MB limit. `brand.py --selftest` checks this, and CI runs it.
- Websites that send compressed pages unasked are now read correctly.
- The master skill's description no longer trips a prompt-injection rule in skill scanners.
- CI actions are pinned to exact commits, with Dependabot keeping them current.

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
