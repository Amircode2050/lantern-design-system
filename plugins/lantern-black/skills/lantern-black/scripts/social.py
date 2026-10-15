"""social: turn any library scene into a post, as a still or a seamless loop.

    python social.py supply_chain                          square still (1080x1080) in the default colour
    python social.py supply_chain story teal light         story (1080x1920), any colour and variant
    python social.py supply_chain portrait --loop 8        4:5 feed post as an 8 s MP4 loop (and its still)
    python social.py all square gold                       every scene as a square still
    options: --handle "@you"  a small line at the foot; --out DIR (default ./out/social)

Formats: square 1080x1080 (LinkedIn, X, Instagram), portrait 1080x1350 (feed posts), story 1080x1920 (Stories,
Reels, Shorts). The card carries the scene's question and answer line; the labels stay on the slide version.
"""

import argparse
import functools
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scenes
from components import *
from kit import C, F, T

FORMATS = {"square": (1080, 1080), "portrait": (1080, 1350), "story": (1080, 1920)}


def _nest(svg, x, y, w, h, view):
    """Place a finished scene SVG inside the card, cropped to `view`, its ids renamed so they cannot clash."""
    inner = re.sub(r"^<svg[^>]*>", "", svg).removesuffix("</svg>")
    inner = re.sub(r"<title>.*?</title>", "", inner)
    inner = re.sub(r'id="([^"]+)"', r'id="s-\1"', inner)
    inner = re.sub(r"url\(#([^)]+)\)", r"url(#s-\1)", inner)
    vx, vy, vw, vh = view
    return (  # the mask sits on an outer group: on the nested svg it would be read in the scene's coordinates
        f'<g mask="url(#fade)"><svg x="{f2(x)}" y="{f2(y)}" width="{f2(w)}" height="{f2(h)}" viewBox="{f2(vx)} {f2(vy)} {f2(vw)} {f2(vh)}" '
        f'preserveAspectRatio="xMidYMid meet">{inner}</svg></g>'
    )


def card(name, fmt="square", t=0.0, handle=None, words=None):
    """One social card as an SVG: question and answer on clear ground, the scene's drawing below."""
    sc = dict(scenes.SCENES[name], **(words or {}))
    W, H = FORMATS[fmt]
    set_canvas(W, H)
    art = scenes.art(name, t)
    set_canvas(W, H)
    zt = scenes.zoomer(sc["zoom"])
    x0, y0 = zt(sc["focus"][:2])
    x1, y1 = zt(sc["focus"][2:])
    pad = 40
    keep = {"square": 1.0, "portrait": 0.96, "story": 0.92}[fmt]  # tall formats trim the sides a little
    vw = (x1 - x0 + 2 * pad) * keep
    view = ((x0 + x1) / 2 - vw / 2, y0 - pad, vw, y1 - y0 + 2 * pad)
    aw = W
    ah = aw * view[3] / view[2]
    title_size = {"square": 62, "portrait": 66, "story": 76}[fmt]
    widest = max(text_width(ln, title_size, F.DISPLAY) for ln in sc["title"])
    title_size = round(min(title_size, title_size * (W - 140) / widest))
    lead = title_size * 1.12
    ty = {"square": 120, "portrait": 170, "story": 330}[fmt]
    ay = ty + lead * (len(sc["title"]) - 1) + title_size * 0.95
    ans = wrap(sc["answer"], 34 if fmt != "story" else 32)
    asz = 36 if fmt == "story" else 30
    text_end = ay + 8 + len(ans) * asz * 1.33
    if fmt == "story":  # centre the drawing in the space under the words; its upper part is mostly sky
        top = text_end + (H - 140 - text_end - ah) / 2 - ah * 0.08
    else:
        top = H - ah - {"square": 40, "portrait": 110}[fmt]
    fade = (
        f'<linearGradient id="fadeg" x1="0" y1="{f2(top)}" x2="0" y2="{f2(top + ah)}" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.14" stop-color="#fff"/>'
        '<stop offset="0.9" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<mask id="fade" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
        f'<rect x="0" y="{f2(top)}" width="{W}" height="{f2(ah)}" fill="url(#fadeg)"/></mask>'
    )
    cx, cy = W / 2, top + ah * 0.55
    body = [
        background(cx, cy, seed=5, p=(t % C.LOOP) / C.LOOP, avoid=[(0, 0, W, ay + 60)]),
        _nest(art, 0, top, aw, ah, view),
        finish(),
    ]
    body += [
        text(W / 2, ty + i * lead, ln, title_size, T.T1, F.DISPLAY, 'text-anchor="middle"')
        for i, ln in enumerate(sc["title"])
    ]
    body += [
        text(W / 2, ay + 8 + i * asz * 1.33, ln, asz, T.W300, F.SANS, 'text-anchor="middle" font-weight="500"')
        for i, ln in enumerate(ans)
    ]
    if handle:
        body.append(text(W / 2, H - 44, handle, 20, T.T3, F.MONO, 'text-anchor="middle"'))
    return svg_doc(std_defs(cx, cy) + fade, "".join(body), alt=sc["alt"])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render library scenes as social posts.")
    ap.add_argument("scene", help="a scene name from scenes.py, or 'all'")
    ap.add_argument("rest", nargs="*", help="format (square, portrait, story), colour, variant, type set")
    ap.add_argument("--loop", type=float, default=0, help="also render a seamless MP4 of this many seconds")
    ap.add_argument("--handle", default=None)
    ap.add_argument("--out", default="out/social")
    a = ap.parse_args(argv)
    names = list(scenes.SCENES) if a.scene == "all" else [a.scene]
    if any(n not in scenes.SCENES for n in names):
        sys.exit(f"unknown scene; choose from: {', '.join(scenes.SCENES)}")
    pick = lambda opts, default: ([x for x in a.rest if x in opts] or [default])[0]
    fmt = pick(FORMATS, "square")
    set_theme(pick(("dark", "light"), "dark"), pick(colors(), None), pick(SYS["type_sets"], None))
    os.makedirs(a.out, exist_ok=True)
    for n in names:
        stem = os.path.join(a.out, f"{n}_{fmt}_{T.color}_{T.variant}")
        print(render(card(n, fmt, 3.0, a.handle), stem + ".png", scale=1))
        if a.loop:
            W, H = FORMATS[fmt]
            set_canvas(W, H, loop=a.loop)
            frames = stem + "_frames"
            render_frames(functools.partial(card, n, fmt, handle=a.handle), 24, frames, fresh=True)
            mb = make_mp4(frames, stem + ".mp4", fps=24)
            seam, typical = check_loop(frames)
            print(f"{stem}.mp4  {mb:.1f} MB, seam {seam:.2f} vs typical {typical:.2f}")


if __name__ == "__main__":
    main()
