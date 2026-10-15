# Lantern Green: component and function reference

Drawing functions return SVG strings in local coordinates and read colours from the theme, so one scene renders in every colour and variant. `p` is the loop phase 0..1; `y` is the floor or base line unless stated. `assets/reference/<colour>/sheet_dark.jpg` and `sheet_light.jpg` show every element rendered.

## components.py

| Function | What it does |
|---|---|
| `shell(x, y, w, h, r=0, t=14, tint='ROOM')` | Building or hull frame: riveted metal band + cavity. Rooms go inside (x+t, y+t, w-2t, h-2t). |
| `room(x, y, w, h, tint='ROOM_COOL')` | Room tint: ROOM, ROOM_COOL (servers, labs), ROOM_WARM (lounges, reactors), ROOM_DEEP (navigation), ROOM_BILGE. |
| `slab(x, y, w, t=10)` | Floor slab with a lit top edge and a soft shadow beneath. |
| `wall(x, y, h, t=6)` |  |
| `truss(x, y, w, h=16)` |  |
| `plinth(x, y, w, h=18)` | Ground slab a building stands on, with its contact shadow. |
| `sawtooth_roof(x, y, w, n=5, h=None)` | Row of glazed factory gables sitting on the line y; each has a warm skylight with mullions. |
| `gable(x, y, w, h=None, oculus=True)` | Pitched roof on the line y, with a lit round window. |
| `arched_window(x, y, w=26, h=78, lit=False)` | Tall arched window standing on y. lit=True fills it with the warm gradient and a soft halo. |
| `arcade(x, y, w, n=12, h=64, lit=True)` | Row of arched openings (a gallery or cloister) standing on y. |
| `pendant_lamp(x, y, drop=40, r=48)` | Hanging lamp from the ceiling point (x, y): cord, shade, bulb and its pool of light. |
| `ladder(x, y0, y1, w=16)` |  |
| `string_lights(a, b, sag=28, n=5, p=0.0)` | Cable of warm bulbs hung between two points; bulbs breathe in whole cycles. |
| `cloud(x, y, s=1.0, p=0.0, rain=True, bolt=True, seed=5)` | Storm cloud centred on (x, y) with slanted rain and a lightning bolt that flashes three times per loop. |
| `battery(x, y, w=58, h=250, level=1.0, cells=8)` | Reserve tank drawn as a battery; (x, y) is the top-left. level 0..1 = how many cells are lit. |
| `conveyor(x, y, w, h=12)` | Belt whose top surface is at y, on rollers. |
| `crate(x, y, s=16)` | Lit parcel standing on y. |
| `car(x, y, s=1.0)` | Small saloon on an assembly line; wheels rest on y. |
| `machine(x, y, w=70, h=84)` | Generic press or processor standing on y: body, hopper, slot, dial and two status lights. |
| `server_rack(x, y, w=54, h=110, rows=7, p=0.0, seed=1)` | Rack standing on y; status lights blink in whole cycles (squares = information, dots = power). |
| `clock(x, y, r=16, p=0.0)` | Wall clock centred on (x, y); the minute hand makes one turn per loop. |
| `desk(x, y, w=64, lit=True)` |  |
| `cabinet(x, y, w=28, h=64)` |  |
| `screen(x, y, w=60, h=44, kind='bars', p=0.0)` | Wall display with top-left (x, y). kind = 'bars' / 'line'. |
| `orrery(cx, cy, r=60, p=0.0)` | Model solar system: tilted orbits, a lit sun, planets in whole orbits per loop. |
| `thinking_core(cx, cy, r=44, p=0.0, seed=4)` | The 'thinking' orb: a lit sphere holding a small network whose nodes pulse in turn. |
| `bars(x, y, w, h, values, labels=None, highlight=None, unit='')` | Small bar chart on the baseline y. One series in the information colour; `highlight` index takes the accent. Values are printed on the bars and categories under them, so nothing depends on colour alone. |
| `house(x, y, w=96, h=64, lit=True)` | Small home standing on y with its left wall at x: pitched roof, door, and a window that glows when lit. |
| `road(x, y, w, h=14)` | Road surface whose top is at y, with a dashed centre line. |
| `truck(x, y, s=1.0, facing=1)` | Delivery van; wheels rest on y, x is the middle. facing=-1 drives left. |
| `pylon(x, y, h=200)` | Lattice power pylon standing on y. Its cables hang from (x - 0.3h, y - 0.86h) and (x + 0.3h, y - 0.86h). |
| `turbine(x, y, h=220, p=0.0, turns=1)` | Wind turbine standing on y; the rotor makes `turns` whole turns per loop. |
| `solar_panel(x, y, w=90)` | Tilted solar panel on a post standing on y; x is the left edge. |
| `tank(x, y, w=80, h=90, level=0.7)` | Upright storage tank standing on y, x the left edge, with a sight glass whose water level is `level`. |
| `tree(x, y, s=1.0, seed=1)` | Rounded tree standing on y. |
| `shelf(x, y, w=80, h=96, rows=4, kind='boxes', seed=1, lit=0.15)` | Open shelving standing on y, x the left edge. kind 'boxes' (stock, archives) or 'books'; a share `lit` glows. |
| `bed(x, y, w=74, occupied=True)` | Bed standing on y, x the left edge; a resting figure when occupied. |
| `dish(x, y, s=1.0, facing=1)` | Radio dish on a stand standing on y, aimed up and forward. Its feed sits at (x + 44*s*facing, y - 108*s). |
| `dome(cx, cy, rx, ry, rows=5, cols=16, oculus=True, shaft=0)` | Coffered dome seen from inside, springing from the line cy. shaft>0 drops a light shaft that far below the oculus. |
| `gallery_ring(cx, cy, rx, ry, t=12, posts=26)` | Front half of a circular balcony: slab, lit edge and a railing. Stack several for tiers. |
| `lantern_tower(cx, base, w=170, tiers=4, tier_h=118, seed=2)` | Central lit tower of stacked glazed drums (the single light of a watchtower scene). Stands on `base`. |
| `saucer(cx, cy, rx=330, ry=92, rivet_gap=22)` | Lens-shaped hull with a glass dome and an emitter underneath. Returns (svg, cavity_path): put cavity_path in a <clipPath> and draw decks and crew inside it. |
| `tractor_beam(cx, y, h=300, w0=70, w1=270, p=0.0, seed=9)` | Cone of light below an emitter at (cx, y) with rising rings and sparks (two cycles per loop). |
| `bust_human(x, y, s=1.0, facing=1)` | Head-and-shoulders human in strict profile. (x, y) = base of the neck; the head is about 370*s tall and the shoulders run about 340*s below, normally cropped by the canvas. The face stays minimal: a brow, a closed eye, a nostril and a mouth line, lit from the side it faces with a rim of light along the profile. |
| `bust_robot(x, y, s=1.0, facing=1, visor=True)` | Head-and-shoulders robot: capsule head with a glowing visor band, an ear module, vent lines, a ribbed neck and broad shoulders. (x, y) = collar centre. The visor points the way it faces; the rim light sits on the back. |
| `lantern(x, y, s=1.0, p=0.0, lit=True, glow_r=3.2)` | Hanging glass lantern, the system's emblem. (x, y) = top of the ring; it stands about 230*s tall. Glass panes, a dark metal cap and base, a hot core and a pool of light; the flame flickers four times per loop. |
| `light_cone(x0, y0, x1, y_top, y_bot, spread0=8, op=0.85)` | Beam from a source at (x0, y0) widening to the segment x1, y_top..y_bot. Brightest at the source. |
| `orb(x, y, r=60)` | Free-standing light source: the one warm light of a portrait scene. |
| `headlamp(x, y, r=58, facing=1)` | Round lamp worn in front of a face (examiner's mirror): dark ring, hot lens. |
| `pane(x, y, w, h, lean=46, silhouette=True)` | Frosted screen or mirror standing between two characters: a lit panel with a bright leading edge and a blurred silhouette behind it. (x, y) = top-left of the near edge. |
| `camera_eye(x, y, s=1.0, facing=1)` | Lens module on a machine's head, the mechanical counterpart of an eye: housing, shade, one hot lens. |

## kit.py

| Function | What it does |
|---|---|
| `colors()` | Installed colour themes (one JSON file each in themes/). |
| `load_theme(color)` |  |
| `ts(style)` | Font size of a named style in the type scale (system.json), at a 1920 frame. |
| `set_theme(variant=None, color=None, type_set=None)` | Any argument left out keeps its current value. A new colour brings its own default type set unless one is given. |
| `set_canvas(w=1920, h=1080, loop=None)` | w may also be a preset name: '16:9', '4:3', '3:2', '1:1', '9:16', 'a4'. |
| `esc(s)` |  |
| `wrap(text, chars=40)` |  |
| `P(pts, close=True)` |  |
| `hexmix(c1, c2, t)` |  |
| `to_oklch(h)` | #rrggbb -> (lightness 0..1, chroma, hue in degrees). |
| `from_oklch(L, Cc, H)` | (lightness, chroma, hue) -> #rrggbb, lowering chroma until the colour fits sRGB. |
| `rrect(x, y, w, h, r, fill, extra='')` |  |
| `circ(cx, cy, r, fill, extra='')` |  |
| `ell(cx, cy, rx, ry, fill, extra='')` |  |
| `line(a, b, col, w, extra='')` |  |
| `path(d, fill='none', extra='')` |  |
| `glow(cx, cy, rx, ry=None, grad='warmglow', op=1.0)` | Soft pool of light. Blend mode follows the theme (screen on dark, multiply on light). |
| `pipe(pts, w=10, col=None, hi=None, dark=None, elbows=True)` |  |
| `cable(pts, w=4, col=None)` |  |
| `flow(pts, kind='energy', p=0.0, cycles=0, gap=16, r=2.2, op=0.95, col=None)` | Glowing marks along a polyline; they advance `cycles` gaps per loop (integer = seamless). kind sets BOTH colour and shape so meaning never rests on hue alone: 'energy' = warm round dots, 'info' = cool squares, 'water' = support-colour rings. |
| `curve(a, b, sag, n=24)` |  |
| `sight(a, b, bulge=0.2, n=None)` | Line of sight: dotted arc whose dots grow and brighten toward b. |
| `gear(cx, cy, teeth, rot=0.0, fill=None, hub=None, nh=None)` | Gear with pitch radius teeth*PITCH/TAU. nh = number of lightening holes (choose so the loop rotation is a symmetry). |
| `gear_radius(teeth)` |  |
| `place_next(c, t_from, t_to, angle_deg)` |  |
| `gear_chain(chain, theta0, omega0)` | chain = [(teeth, centre), ...] meshing in order -> [(teeth, centre, theta0, omega)] with teeth interlocking. |
| `figure(j, alien=False, facing=1, props='')` | Silhouette in ink with a warm rim copy. j: head, neck, hip, arms=[[pts]], legs=[[pts]] (feet last). |
| `standing(x, floor, facing=1, reach=None, alien=False, hat=None, carry=False)` | Standing pose, ~46px tall, feet on `floor`. reach=(x,y) puts the front hand there. hat='top' / 'bun' varies the silhouette; carry=True adds a lit box in the front hand. |
| `seated(x, seat, facing=1, alien=False)` | Seated pose (at a desk or console); `seat` is the y of the chair seat. |
| `std_defs(cx=None, cy=None, lit=(0, -40), lit_r=460)` | Gradients and filters every scene uses. `lit` is the light source in the local (subject) frame. |
| `background(cx=None, cy=None, seed=3, p=0.0, avoid=(), stars=True)` | Ground radial + stars (dust on light) + halo. avoid = [(x0,y0,x1,y1)] boxes kept free of twinkles (text areas). |
| `finish()` | Vignette. Grain is NOT drawn in SVG: render()/make_gif()/make_mp4() add the same static grain to stills and frames. |
| `svg_doc(defs, body, alt='')` | alt = one-sentence description; it becomes the SVG <title> and should be reused as the image's alt text. |
| `is_rtl(s)` |  |
| `text_width(s, size, family=None)` |  |
| `text(x, y, s, size=None, fill=None, family=None, extra='', right=None)` | One line of text with its left edge at x. Right-to-left text (Arabic script) is set right to left and aligned to `right` (the right edge of its block), or to its own measured width when no block edge is given. |
| `title_block(title_lines, subtitle=None, answer=None, x=72, y=100)` | Question in display serif (<=2 lines), an optional subtitle in italic, one answer line in the accent. A right-to-left title (Arabic script) mirrors to the top right and aligns right. |
| `callout(x, y, title, lines, anchor, side='left', tag=None)` | Label + leader. side='left' = label in the left column (leader leaves from its right edge, measured from the text). tag = (prefix, body) or None; e.g. ("Step", "final check"). |
| `break_slide(word='Break', answer='Back in 15 minutes', aside=(), x=1300, y=440)` |  |
| `credit(s, margin=72)` |  |
| `font_installed(entry)` |  |
| `font_packs()` | {pack: (files present, files in the pack)}. Missing packs are added with scripts/fonts.py. |
| `stack_families(stack)` | The bundled families named in a CSS font stack, in order. |
| `font_css(families=None, text=None)` | @font-face rules with the font files embedded (works in a blank page and in any HTML editor). Each rule carries its unicode-range, so browsers use a subset only where its characters appear. With `text`, subsets whose characters do not appear in it are left out entirely, which keeps renders light. |
| `render(svg, out, scale=2, transparent=False, grain=True)` | SVG string -> PNG via Playwright's Chromium, fonts verified, then the theme's static grain. |
| `cutout(png, out=None, pad=24)` | Crop a transparent render to its content + padding; fails if the art touches the canvas edge. |
| `render_frames(build, fps, out_dir, workers=2, fresh=False)` | build(t) -> SVG string (grain is added later, static). Parallel; raises if any frame is missing. Resumable: frames already in out_dir are kept, so pass fresh=True after changing the scene. `build` must be a module-level function and the script must run under `if __name__ == "__main__":`. |
| `grain_amp(width)` |  |
| `grain_field(w, h, amp, seed=7, scale=1)` | Static noise field. scale>1 generates at w/scale and enlarges, so 2x stills carry the same grain size as 1x frames. |
| `apply_grain(img, n)` | Overlay + screen grain at the theme's strengths; alpha (cutouts) is preserved. |
| `make_gif(raw_dir, out, size=None, fps=10, text_png=None, limit_mb=15.0)` | Exact-length GIF. GIF delays are whole centiseconds, so fps must divide 100 (10, 20, 25, 50). If the file exceeds limit_mb the palette is reduced and it is encoded again. |
| `make_mp4(raw_dir, out, fps=24, text_png=None)` | 1080p H.264 MP4 of the frames with the same static grain as the GIF. |
| `check_loop(raw_dir)` | Seam test: the last->first frame difference should look like any consecutive difference. Returns (seam, typical). |
| `contrast(a, b)` |  |
| `check_tokens(only=None)` | WCAG contrast of every text and flow colour on the grounds it is allowed on, for every installed colour (or just `only`) in both variants. Returns the list of failures. |
| `doctor()` | Report what the toolchain is missing, with the command that fixes it. Run this first on a new machine. |

## scenes.py: the scene library

`build(name, t, annotate=True, words=None)` returns the finished slide; `art(name, t)` the drawing alone. Each scene is a seamless loop.

| Scene | Question | Answer line |
|---|---|---|
| `supply_chain` | How does a parcel reach your door? | Made, stored, then driven: every hand-off is a lit link. |
| `data_pipeline` | Where does a dashboard's number come from? | Records flow in, get cleaned, stored and counted, then shown. |
| `data_centre` | How does a data centre stay cool? | Cold water carries the servers' heat up and out through the roof. |
| `power_grid` | How does power reach a home? | Made far away, stepped down, then shared street by street. |
| `internet` | What happens when you open a web page? | Your request crosses the network to a server, and the page comes back. |
| `org_team` | Who does what on a team? | Leads set direction, makers build, and support keeps it running. |
| `sales_funnel` | Why do most visitors never buy? | Each step asks a little more, and only a few go all the way. |
| `research_lab` | How does a lab turn questions into results? | Observe, test and write it down, then check it all again. |
| `model_training` | How does a model learn from examples? | It guesses, measures the miss and adjusts, millions of times. |
| `water_supply` | How does clean water reach a tap? | Rain fills the reservoir; it is cleaned, stored high, then piped home. |
| `hospital` | What keeps a hospital running at night? | Wards rest while the lab, the desk and the ambulance bay stay awake. |
| `school` | What makes a school work? | Teachers, books and time together, every single day. |
| `bank` | Where does your deposit go? | Most is lent to homes and firms; a little stays in the vault. |
| `support_desk` | How does a support ticket get solved? | Logged at the front, answered by an agent, escalated only when needed. |
| `newsroom` | How does a story reach print? | Reported, edited, printed and delivered before breakfast. |
| `retail_store` | What sits behind a shop shelf? | A stock room, a loading dock and a count at closing time. |
| `farm_to_table` | How does food get from field to plate? | Grown, packed, driven and cooked, often within a week. |
| `knowledge_base` | How does a knowledge base answer a question? | Everything is filed once, so anyone can find it fast. |
| `network_defence` | How is a network defended? | Watch every gate, check every visitor, and keep the vault apart. |
| `cloud_computing` | What is the cloud, really? | Someone else's computers, rented by the minute. |
| `remote_team` | How does a team stay in step from home? | Shared tools carry the work, and a short daily call carries the rest. |
| `recycling` | Where does a bottle go after the bin? | Collected, sorted, melted and made again: a loop, not a line. |
| `startup_growth` | How does a small team become a company? | One room, then one floor, then a building, each lit by the last. |
| `mission_control` | How does mission control talk to a ship? | A dish sends the signal; the ship answers minutes later. |
