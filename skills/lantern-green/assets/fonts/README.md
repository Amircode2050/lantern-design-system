# Fonts

Every font here is a subset in woff2 from its [Fontsource](https://fontsource.org) package (the Google Fonts files, packaged per script), at the version pinned in `manifest.json`. All fourteen families are under the SIL Open Font License 1.1; the full licence texts are in `LICENSES.txt`. They are not covered by the project's Apache licence.

`manifest.json` lists every file with its family, weight, style, script subset, pack, download address, SHA-256 hash and Unicode range. The renderer reads it, embeds only the subsets a piece of text needs, and `scripts/fonts.py` uses it to add or verify packs.

| Pack | Families and scripts |
|---|---|
| core | PT Serif, Fraunces, Space Grotesk, Inter, Source Sans 3, JetBrains Mono: Latin |
| sets | IBM Plex Serif, IBM Plex Sans, IBM Plex Mono, DM Serif Display, DM Sans, EB Garamond, Inter Tight: Latin |
| europe | every family that has them: Latin Extended and Vietnamese |
| cyrillic-greek | every family that has them: Cyrillic, Cyrillic Extended, Greek, Greek Extended |
| arabic | Vazirmatn: Arabic script |

| Family | Weights | Copyright | Upstream |
|---|---|---|---|
| PT Serif | 400, 400 italic, 700 | ParaType Ltd. | paratype.com |
| Fraunces | 400, 400 italic, 600 | The Fraunces Project Authors | github.com/undercasetype/Fraunces |
| Space Grotesk | 400, 500 | The Space Grotesk Project Authors | github.com/floriankarsten/space-grotesk |
| Inter | 400, 500, 600 | The Inter Project Authors | github.com/rsms/inter |
| Source Sans 3 | 400, 500, 600 | Adobe | github.com/adobe-fonts/source-sans |
| JetBrains Mono | 400, 500 | The JetBrains Mono Project Authors | github.com/JetBrains/JetBrainsMono |
| IBM Plex Serif, Sans, Mono | 400, 400 italic (serif), 500, 600 | IBM Corp. | github.com/IBM/plex |
| DM Serif Display | 400, 400 italic | Colophon Foundry | github.com/googlefonts/dm-fonts |
| DM Sans | 400, 500, 600 | The DM Sans Project Authors | github.com/googlefonts/dm-fonts |
| EB Garamond | 400, 400 italic, 600 | The EB Garamond Project Authors | github.com/octaviopardo/EBGaramond12 |
| Inter Tight | 400, 500, 600 | The Inter Project Authors | github.com/rsms/inter |
| Vazirmatn | 400, 500, 600 | The Vazirmatn Project Authors | github.com/rastikerdar/vazirmatn |

Maintainers update the set with `python build/fonts.py`, which downloads any missing file, records its hash and rewrites the manifest and the font stacks in `system.json`.
