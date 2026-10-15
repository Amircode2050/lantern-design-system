"""intake: read reference images and say which installed colour they are closest to, or what new theme to make.

    python intake.py ref1.png ref2.jpg

Prints the dominant colours, the most characteristic (most chromatic, well-covered) one, the nearest installed
theme by hue, and the new_theme.py command that would build a theme from it. Needs Pillow.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import colors, load_theme, to_oklch


def palette(path, n=8):
    from PIL import Image

    im = Image.open(path).convert("RGB")
    im.thumbnail((240, 240))
    q = im.quantize(n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    total = im.width * im.height
    return sorted(
        ((cnt / total, "#{:02x}{:02x}{:02x}".format(*pal[i * 3 : i * 3 + 3])) for cnt, i in q.getcolors()), reverse=True
    )


def hue_gap(a, b):
    return min(abs(a - b), 360 - abs(a - b))


def read(paths):
    pal = sorted((pc for p in paths for pc in palette(p)), reverse=True)
    main = [h for share, h in pal if share > 0.03] or [pal[0][1]]
    # the most characteristic colour: chroma, weighted toward mid-lightness so near-black and near-white lose
    L, Cc, H = max((to_oklch(h) for h in main), key=lambda o: o[1] * (0.4 + min(o[0], 1 - o[0])))
    pick = next(h for share, h in pal if to_oklch(h) == (L, Cc, H))
    if Cc < 0.03:
        return pal, pick, None, None  # neutral image: black, white or grey system
    near = min(colors(), key=lambda c: hue_gap(to_oklch(load_theme(c)["core"])[2], H))
    return pal, pick, near, hue_gap(to_oklch(load_theme(near)["core"])[2], H)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    pal, pick, near, gap = read(sys.argv[1:])
    print("dominant colours:", ", ".join(f"{h} {share:.0%}" for share, h in pal[:8]))
    print("characteristic colour:", pick)
    if near is None:
        print(
            'the references are neutral: build a monochrome theme, e.g.\n  python new_theme.py ink "#111111" --harmony monochrome --deep 0.55'
        )
    elif gap <= 18:
        print(f"closest installed theme: {near} (hue {gap:.0f} degrees away): use it")
    else:
        print(
            f'closest installed theme: {near}, but {gap:.0f} degrees away: consider a new one\n  python new_theme.py <name> "{pick}" --preview out'
        )
