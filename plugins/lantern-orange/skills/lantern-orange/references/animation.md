# Seamless loops

The default loop is 25 s (`set_canvas("16:9", loop=25)`); any length works as long as every motion completes whole cycles.

- Let `p = (t % C.LOOP) / C.LOOP`. Every periodic motion uses **whole cycles per loop**: `sin(TAU * n * p)`, `frac(n * p)` with integer n. All library components already do this through their `p` argument.
- Gears: choose m teeth passing per loop (for example 40); the driver speed is `TAU * (m / T0) / C.LOOP`; `gear_chain` returns each gear's start angle and speed. The per-loop rotation of m/T turns must be a symmetry of the drawing: pick the hole count `nh` so that nh*m/T is an integer (for m = 40: T=24 gives 6, 16 gives 4, 20 gives 5, 15 gives 3).
- Flows: `flow(pts, kind, p, cycles)` with integer cycles.
- Keep motion slow and mechanical: gears 1 to 2 turns per loop, pulses 30 to 60 px/s, pistons 2.5 s, status lights 0.5 to 5 s. Animate small things; keep large glows **steady** (pulsing big glows bloats GIFs and tires the eye). Nothing flashes more than three times a second.
- Grain is static: the kit adds the same noise field to every frame after rendering.

```python
def build_frame(t): return build(t)          # module level, no text

if __name__ == "__main__":
    set_theme("dark"); set_canvas("16:9", loop=25)
    render(build(3.0), "still.png", scale=2)        # the static alternative
    render_frames(build_frame, 10, "frames10")     # 250 frames, resumable
    render_frames(build_frame, 24, "frames24")
    print(check_loop("frames10"))                  # (seam, typical): should be close
    make_gif("frames10", "loop.gif")               # 1280 wide, exact length; the palette shrinks if over 15 MB
    make_mp4("frames24", "loop.mp4")
```

Render the text once as a transparent PNG (`render(text_only_svg, "text.png", scale=1, transparent=True, grain=False)`) and pass `text_png="text.png"` to `make_gif` and `make_mp4`; the no-text version then comes free.

Cost: about 0.4 s per frame per worker; a 25 s loop at 10 and 24 fps is roughly 6 minutes with 2 workers. If the seam value from `check_loop` is several times the typical value, one motion is not on a whole cycle: usually a gear hole count or a non-integer `cycles`.
