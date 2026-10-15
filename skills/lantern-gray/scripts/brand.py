"""brand: turn a brand into a Lantern colour in one step, from a website, a logo or a hex value.

    python brand.py acme https://example.com          read the colours the website declares
    python brand.py acme logo.png [screenshot.png]    read a logo or screenshots
    python brand.py acme "#E4002B"                    start from a known hex value
    options: --out DIR (default ./brand-<name>), --force (replace an existing theme of that name)

Finds the brand's most characteristic colour, borrows the recipe of the nearest installed colour (a yellow gets
the near-black ground of Gold, a grey the monochrome recipe of Black or White), writes themes/<name>.json, and
renders a cover slide, a scene and the component sheet in dark and light, plus CSS and Tailwind tokens.

The website mode is the only part of Lantern that touches the network: it downloads the one page and up to five
of its stylesheets over http(s) from public addresses only (no local or private network), 10 s timeout, 2 MB each.
Nothing is sent except the requests themselves, and nothing downloaded is run.
"""

import argparse
import ipaddress
import os
import re
import socket
import sys
import zlib
from collections import Counter
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from components import *
from kit import ROOT, F, T, colors, load_theme, to_oklch

HEX6 = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-zA-Z])")
RGB = re.compile(r"rgba?\(\s*(\d{1,3})[\s,]+(\d{1,3})[\s,]+(\d{1,3})")
META = re.compile(r'<meta[^>]+name=["\'](?:theme-color|msapplication-TileColor)["\'][^>]*>', re.I)
CONTENT = re.compile(r'content=["\']([^"\']+)["\']', re.I)
SHEET = re.compile(r'<link[^>]+rel=["\'][^"\']*stylesheet[^"\']*["\'][^>]*>', re.I)
HREF = re.compile(r'href=["\']([^"\']+)["\']', re.I)
LIMIT = 2_000_000
FAMILIES = ["black", "white", "blue", "purple", "green", "red", "gray", "teal", "gold", "orange", "cyan", "rose"]


def public(url):
    """Refuse anything but http(s) to a public address, so a page cannot point the reader at the local network."""
    u = urlparse(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        raise ValueError(f"only http and https addresses are read (got {url!r})")
    try:
        addrs = {i[4][0] for i in socket.getaddrinfo(u.hostname, u.port or (443 if u.scheme == "https" else 80))}
    except socket.gaierror as e:
        raise ValueError(f"cannot resolve {u.hostname}") from e
    for a in addrs:
        if not ipaddress.ip_address(a.split("%")[0]).is_global:
            raise ValueError(f"{u.hostname} resolves to a private or local address ({a}); only public sites are read")
    return url


class _Redirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        public(newurl)  # every hop is checked, not just the first address
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = build_opener(_Redirects)


def fetch(url):
    # ponytail: the address is checked when resolved, not pinned for the connection; enough for a tool you run yourself
    req = Request(public(url), headers={"User-Agent": "Mozilla/5.0 (compatible; lantern-brand)"})
    with _OPENER.open(req, timeout=10) as r:
        body, enc = r.read(LIMIT), (r.headers.get("Content-Encoding") or "").lower()
    if enc in ("gzip", "deflate") or body[:2] == bytes([0x1F, 0x8B]):  # some servers compress unasked
        d = zlib.decompressobj(zlib.MAX_WBITS | 32)  # gzip or zlib header
        body = d.decompress(body, LIMIT)  # capped after decompression too
    return body.decode("utf-8", "replace")


def norm(h):
    h = h.lstrip("#").lower()
    return "#" + ("".join(c * 2 for c in h) if len(h) == 3 else h)


def css_colors(s):
    out = [norm(m) for m in HEX6.findall(s)]
    out += ["#{:02x}{:02x}{:02x}".format(*(min(255, int(v)) for v in m)) for m in RGB.findall(s)]
    return out


def from_site(url):
    """Colours a page declares: theme-color counts most, then every colour in its inline and linked CSS."""
    page = fetch(url)
    count = Counter()
    for tag in META.findall(page):
        for v in CONTENT.findall(tag):
            for c in css_colors(v):
                count[c] += 25
    count.update(css_colors(page))
    sheets = [urljoin(url, h) for tag in SHEET.findall(page) for h in HREF.findall(tag)][:5]
    for s in sheets:
        try:
            count.update(css_colors(fetch(s)))
        except (OSError, ValueError) as e:
            print(f"  skipped {s}: {e}")
    if not count:
        sys.exit(f"no colours found on {url}; try a logo image or a hex value instead")
    return count


def from_images(paths):
    from intake import palette

    count = Counter()
    for p in paths:
        for share, h in palette(p):
            count[h] += share * 100
    return count


def pick(count):
    """The most characteristic colour: chromatic, mid-lightness and used often. None if the brand is neutral."""
    groups = []  # merge near-identical shades into the most-used one
    for h, n in count.most_common():
        L, Cc, H = to_oklch(h)
        for g in groups:
            gL, gC, gH = to_oklch(g[0])
            if abs(L - gL) < 0.05 and abs(Cc - gC) < 0.03 and min(abs(H - gH), 360 - abs(H - gH)) < 8:
                g[1] += n
                break
        else:
            groups.append([h, n])
    chroma = [(h, n) for h, n in groups if to_oklch(h)[1] >= 0.045 and 0.2 <= to_oklch(h)[0] <= 0.93]
    if not chroma:
        return None, groups
    score = lambda g: g[1] ** 0.5 * to_oklch(g[0])[1] * (0.4 + min(to_oklch(g[0])[0], 1 - to_oklch(g[0])[0]))
    chroma.sort(key=score, reverse=True)
    return chroma[0][0], chroma


def recipe_for(core):
    """The installed colour whose recipe suits this core: nearest hue among the chromatic themes, if close."""
    L, Cc, H = to_oklch(core)
    if Cc < 0.045:
        return ("black" if L < 0.6 else "white") if {"black", "white"} <= set(colors()) else None
    gap = lambda c: min(abs(to_oklch(load_theme(c)["core"])[2] - H), 360 - abs(to_oklch(load_theme(c)["core"])[2] - H))
    chromatic = [c for c in FAMILIES if c in colors() and to_oklch(load_theme(c)["core"])[1] >= 0.045]
    near = min(chromatic, key=gap)
    return near if gap(near) <= 30 else None


def cover(name, variant):
    """Title slide in the brand colour: the lantern over a small lit workshop, the brand name and its core value."""
    set_canvas("16:9")
    b = [
        background(620, 470, seed=11, avoid=[(1100, 260, 1900, 820)]),
        line((620, 0), (620, 170), T.IN800, 3),
        lantern(620, 170, 2.3, glow_r=3.6),
        plinth(330, 960, 580),
        sawtooth_roof(380, 820, 220, 2),
        shell(380, 820, 220, 140),
        arched_window(420, 946, 22, 70, lit=True),
        arched_window(456, 946, 22, 70),
        pendant_lamp(520, 834, 16, 40),
        standing(560, 946, -1, reach=(540, 916)),
        standing(700, 960, -1, reach=(676, 920)),
        standing(760, 960, -1, carry=True),
        flow([(600, 950), (700, 950), (760, 950)], "energy", gap=12, r=2),
        finish(),
        text(1180, 470, T.name, ts("title-xl"), T.T1, F.DISPLAY),
        text(1186, 532, "Your colour, in Lantern.", ts("answer"), T.W300, F.SANS, 'font-weight="500"'),
        text(1186, 590, f"Core {T.CORE.upper()}, {variant} variant.", ts("lead"), T.T2),
    ]
    return svg_doc(std_defs(620, 470), "".join(b), alt=f"A lantern over a lit workshop beside the name {T.name}.")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Make a Lantern colour from a website, a logo or a hex value.")
    ap.add_argument("name", help="theme name, e.g. acme (a-z, 0-9 and _)")
    ap.add_argument("source", nargs="+", help="a URL, one or more image files, or a #rrggbb value")
    ap.add_argument("--out", default=None)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    name, src = a.name.lower(), a.source
    if name in colors() and not a.force:
        sys.exit(f"theme '{name}' already exists; pass --force to replace it")

    if len(src) == 1 and re.fullmatch(r"#?[0-9a-fA-F]{6}", src[0]):
        core, groups = norm(src[0]), []
    else:
        if len(src) == 1 and src[0].startswith(("http://", "https://")):
            print(f"reading {src[0]}")
            count = from_site(src[0])
        else:
            missing = [p for p in src if not os.path.isfile(p)]
            if missing:
                sys.exit(f"not a file, URL or hex value: {', '.join(missing)}")
            count = from_images(src)
        core, groups = pick(count)
        if core is None:  # a black, white or grey brand: monochrome, from its most-used colour
            core = groups[0][0]
        else:
            others = [h for h, _ in groups[1:5]]
            print("brand colours, strongest first:", ", ".join([core] + others))
            if others:
                print(f'  to use another one: python brand.py {name} "{others[0]}" --force')
    base = recipe_for(core)
    print(f"core colour: {core}" + (f", built with the {base} recipe" if base else ", built with the default recipe"))

    import new_theme

    args = [name, core, "--shades"] + (["--from", base] if base else []) + (["--force"] if a.force else [])
    bad = new_theme.main(args)

    import examples
    from export import export

    out = a.out or f"brand-{name}"
    os.makedirs(out, exist_ok=True)
    for v in ("dark", "light"):
        set_theme(v, name)
        for nm, svg in (("cover", cover(name, v)), ("scene", examples.factory()), ("sheet", examples.sheet())):
            print(render(svg, os.path.join(out, f"{nm}_{v}.png"), scale=1))
    export(name, os.path.join(out, "tokens"), default=load_theme(name).get("default_variant", "dark"))
    print(f"theme: {ROOT / 'themes' / (name + '.json')}\npreviews and tokens: {out}")
    return bad


def _selftest():
    for bad in (
        "file:///tmp/style.css",
        "ftp://example.com/x.css",
        "http://127.0.0.1/",
        "http://10.0.0.1/",
        "http://[::1]/",
    ):
        try:
            public(bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad}")
    assert pick(Counter({"#3776ab": 30, "#ffd343": 30, "#111111": 400}))[0] == "#3776ab"
    assert pick(Counter({"#111111": 10, "#eeeeee": 10}))[0] is None
    print("brand self-test passed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        _selftest()
    else:
        sys.exit(main())
