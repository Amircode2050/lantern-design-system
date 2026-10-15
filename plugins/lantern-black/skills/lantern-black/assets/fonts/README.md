# Bundled fonts

Latin subsets in woff2, taken from the Fontsource packages (version 5.3.0). All six families are licensed under the SIL Open Font License 1.1; the full licence texts are in `LICENSES.txt`. They are not covered by the project's Apache licence.

| Family | Weights | Copyright | Upstream |
|---|---|---|---|
| PT Serif | 400, 400 italic, 700 | ParaType Ltd. | paratype.com |
| Inter | 400, 500, 600 | The Inter Project Authors | github.com/rsms/inter |
| JetBrains Mono | 400, 500 | The JetBrains Mono Project Authors | github.com/JetBrains/JetBrainsMono |
| Space Grotesk | 400, 500 | The Space Grotesk Project Authors | github.com/floriankarsten/space-grotesk |
| Fraunces | 400, 400 italic, 600 | The Fraunces Project Authors | github.com/undercasetype/Fraunces |
| Source Sans 3 | 400, 500, 600 | Adobe | github.com/adobe-fonts/source-sans |

Only Latin characters are included. Text in other scripts falls back to the system font; add the matching subsets here and to `system.json` if you need them.
