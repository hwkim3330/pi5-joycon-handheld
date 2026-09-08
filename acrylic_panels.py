"""Laser-cut acrylic sandwich case: Raspberry Pi 5 + official 5" Touch Display 2
+ Joy-Con 1 rails (printed modules, see joycon_rail.py).

    python3 acrylic_panels.py            # -> out/acrylic/<version>/...

Design intent: slim, light, "Apple-grade" — a dark 2T front plate covers the
display's wide bezel and shows only the active area through a window; all
hardware is hidden behind (V1) or uses black button-heads (V2).

The Pi 5 bolts to the BACK of the Touch Display 2 with the display's own M2.5
posts, so the case holds one display+Pi block — no Pi standoffs in the case.

Laser rules baked in: every hole/bolt is a through-bolt along the stack axis
(a laser only cuts perpendicular to the sheet). The printed Joy-Con rail has a
5 mm flange that drops into a notch in the middle "rail" layer and is clamped by
two of the stack bolts. A 3.2 mm wire notch lets a stripped USB cable's 5V/GND
reach the Joy-Con charge pins at the rail base.

Outputs per version: individual panel DXFs, one sheet DXF per thickness (what a
shop actually cuts), manifest.txt, and a 3D stack preview PNG.
"""

import os, math
import cadquery as cq

# ---------- display (official Raspberry Pi Touch Display 2, 5") ----------
DISP_W, DISP_H = 143.5, 91.5        # module outline, landscape
ACT_W, ACT_H   = 110.4, 62.1        # visible active area
ACT_DX, ACT_DY = 0.0, 0.0           # active-area offset in module — CONFIRM
DISP_D, PI_D   = 16.0, 17.0         # module depth, Pi5 behind it — MEASURE stack

# ---------- case geometry ----------
CLR        = 0.75                   # clearance around the display in the cavity
SIDE_WALL  = 8.0                    # carries the rail bolts (= rail flange depth)
TOP_WALL   = 8.0
CAV_W, CAV_H = DISP_W + 2*CLR, DISP_H + 2*CLR
W, H       = CAV_W + 2*SIDE_WALL, CAV_H + 2*TOP_WALL       # 161 x 109
R_OUT, R_CAV, R_WIN = 6.0, 3.0, 2.0
WIN_W, WIN_H = ACT_W + 1.0, ACT_H + 1.0                     # 0.5 mm reveal

BOLT_D     = 2.8                    # M2.5 clearance (same screws as the display posts)
NUT_AF     = 5.0                    # M2.5 nut across-flats (hex trap)
BX         = W/2 - SIDE_WALL/2      # bolt column x = 76.5
BY_CORNER  = H/2 - TOP_WALL/2       # 50.5
BY_RAIL    = 8.0                    # matches FL_HOLE_PITCH/2 in joycon_rail.py
RAIL_LEN   = 67.0
FL_L       = 24.0                   # rail flange length (notch in rail layer)
WIRE_Y     = -RAIL_LEN/2 + 3.0      # charge pocket center -> wire notch
IO_W       = 80.0                   # bottom I/O notch width (Pi ports/power) — CONFIRM

LAYER_T = 5.0                       # spacer thickness (5T)

# ---------- versions ----------
# stack roles: nuttrap | plain | display | rail | pi
VERSIONS = {
    "v1_slim_black": dict(
        front_t=2.0, front_holes=False,           # glued 2T black front, no visible bolts
        back_t=2.0,  rail=True,
        stack=["nuttrap", "display", "display", "rail", "pi", "pi", "pi"],
        note="2T black/smoked front glued with VHB; bolts from the back into M3 nuts trapped in layer 1."),
    "v2_standard": dict(
        front_t=3.0, front_holes=True,
        back_t=3.0,  rail=True,
        stack=["plain", "display", "display", "rail", "pi", "pi", "pi"],
        note="3T front with black button-head M3 bolts through everything; easiest to service."),
    "v4_open_back": dict(
        front_t=3.0, front_holes=True,
        back_t=0.0,  rail=True,                    # no back plate: nuts sit on the last layer
        stack=["plain", "display", "display", "rail", "pi", "pi", "pi"],
        note="Back left open for airflow / a visible Pi. Bolts + nuts finish on layer 7."),
    "v5_cooler_ssd": dict(
        front_t=3.0, front_holes=True,
        back_t=3.0,  rail=True, back_fan_window=True,
        stack=["plain", "display", "display", "rail", "pi", "pi", "pi", "pi", "pi"],
        note="Room for the Pi 5 Active Cooler + an M.2 HAT+ / NVMe SSD (~+10 mm); "
             "back plate gets a 48 mm fan window over the cooler."),
    "v3_tablet_norail": dict(
        front_t=3.0, front_holes=True,
        back_t=3.0,  rail=False,
        stack=["plain", "display", "display", "pi", "pi", "pi", "pi"],
        note="Same as v2 with no Joy-Con rails/holes — a plain Pi tablet."),
}


def _rrect(w, h, r, t=1.0):
    return cq.Workplane("XY").rect(w, h).extrude(t).edges("|Z").fillet(r)


def _bolt_pts(rail):
    pts = [(sx*BX, sy*BY_CORNER) for sx in (-1, 1) for sy in (-1, 1)]
    if rail:
        pts += [(sx*BX, sy*BY_RAIL) for sx in (-1, 1) for sy in (-1, 1)]
    return pts


def _holes(solid, pts, d):
    if not pts:
        return solid
    cyl = cq.Workplane("XY").pushPoints(pts).circle(d/2).extrude(1.0)
    return solid.cut(cyl)


def _hex_traps(solid, pts):
    dia = NUT_AF / math.cos(math.radians(30))
    hx = cq.Workplane("XY").pushPoints(pts).polygon(6, dia).extrude(1.0)
    return solid.cut(hx)


def panel_front(v):
    p = _rrect(W, H, R_OUT)
    win = _rrect(WIN_W, WIN_H, R_WIN).translate((ACT_DX, ACT_DY, 0))
    p = p.cut(win)
    if v["front_holes"]:
        p = _holes(p, _bolt_pts(v["rail"]), BOLT_D)
    return p


def panel_back(v):
    p = _rrect(W, H, R_OUT)
    p = _holes(p, _bolt_pts(v["rail"]), BOLT_D)
    if v.get("back_fan_window"):
        # big window straight over the Active Cooler fan + flanking slots
        p = p.cut(_rrect(48.0, 48.0, 6.0))
        for sx in (-1, 1):
            slots = cq.Workplane("XY")
            for i in range(0, 3):
                slots = slots.pushPoints([(sx*(34.0 + i*7.0), 0)]).slot2D(40, 3.0, 90)
            p = p.cut(slots.extrude(1.0))
        return p
    slots = cq.Workplane("XY")
    for i in range(-3, 4):
        slots = slots.pushPoints([(i*9.0, 0)]).slot2D(46, 3.2, 90)
    return p.cut(slots.extrude(1.0))


def panel_spacer(v, role):
    p = _rrect(W, H, R_OUT)
    p = p.cut(_rrect(CAV_W, CAV_H, R_CAV))
    pts = _bolt_pts(v["rail"])
    if role == "nuttrap":
        p = _hex_traps(p, pts)
    else:
        p = _holes(p, pts, BOLT_D)
    if role == "rail" and v["rail"]:
        for sx in (-1, 1):
            # flange notch: remove the side wall over the flange length
            n = (cq.Workplane("XY").center(sx*(W/2 - SIDE_WALL/2), 0)
                 .rect(SIDE_WALL + 0.2, FL_L).extrude(1.0))
            p = p.cut(n)
            # wire notch for the 5V/GND lead to the charge pocket
            wn = (cq.Workplane("XY").center(sx*(W/2 - SIDE_WALL/2), WIRE_Y)
                  .rect(SIDE_WALL + 0.2, 3.2).extrude(1.0))
            p = p.cut(wn)
    if role in ("pi",):
        io = (cq.Workplane("XY").center(0, -H/2 + TOP_WALL/2)
              .rect(IO_W, TOP_WALL + 0.2).extrude(1.0))
        p = p.cut(io)
    return p


def build_version(name, v):
    parts = []   # (label, thickness, solid)
    parts.append(("front", v["front_t"], panel_front(v)))
    for i, role in enumerate(v["stack"], 1):
        parts.append((f"L{i}_{role}", LAYER_T, panel_spacer(v, role)))
    if v["back_t"] > 0:
        parts.append(("back", v["back_t"], panel_back(v)))
    return parts


def export_version(name, v):
    outdir = f"out/acrylic/{name}"
    os.makedirs(outdir, exist_ok=True)
    parts = build_version(name, v)

    # individual DXFs
    for label, t, solid in parts:
        cq.exporters.export(solid.faces("<Z"), f"{outdir}/{label}_{t:g}T.dxf")

    # one sheet per thickness (grid, 6 mm gaps)
    by_t = {}
    for label, t, solid in parts:
        by_t.setdefault(t, []).append((label, solid))
    for t, items in by_t.items():
        sheet = cq.Workplane("XY")
        cols = 4
        for k, (label, solid) in enumerate(items):
            dx = (k % cols) * (W + 6.0)
            dy = -(k // cols) * (H + 6.0)
            sheet = sheet.add(solid.translate((dx, dy, 0)).faces("<Z"))
        cq.exporters.export(sheet, f"{outdir}/sheet_{t:g}T.dxf")

    # manifest
    total_t = sum(t for _, t, _ in parts)
    with open(f"{outdir}/manifest.txt", "w") as f:
        f.write(f"{name}\n{v['note']}\n\n")
        f.write(f"outer {W:.1f} x {H:.1f} mm, stack total {total_t:.0f} mm "
                f"(+{7*2 if v['rail'] else 0} mm with rails)\n")
        f.write(f"display cavity {CAV_W:.1f} x {CAV_H:.1f}; window {WIN_W:.1f} x {WIN_H:.1f}\n\n")
        f.write("part                thickness  qty\n")
        for label, t, _ in parts:
            f.write(f"{label:18s}  {t:g}T        1\n")
        f.write("\nhardware: M2.5 x %d black button-head bolts + nuts (V1: nuts trapped in L1)\n"
                % (int(total_t) + 4))
        f.write("printed: joycon_rail_L.stl + joycon_rail_R.stl (only if rail=True)\n")
        f.write("finish: CAST acrylic (clean glossy laser edge); front = black or smoked\n")
        f.write("laser: kerf ~0.15 mm; 2.8 mm holes = M2.5 clearance\n")

    # 3D stack preview STL (for rendering / sanity)
    z = 0.0
    asm = None
    for label, t, solid in parts:
        layer = solid.faces("<Z").wires().toPending().extrude(t).translate((0, 0, z))
        asm = layer if asm is None else asm.union(layer)
        z += t
    if v["rail"]:
        try:
            import joycon_rail as jr
            zc = v["front_t"] + LAYER_T * (v["stack"].index("rail") + 0.5)
            for side in (+1, -1):
                r = jr.build(+1, foot=False)
                # rail axes (x=depth, y=out, z=slide) -> case (Z, X, Y)
                r = r.rotate((0, 0, 0), (0, 1, 0), -90).rotate((0, 0, 0), (0, 0, 1), -90)
                r = r.translate((W/2 + jr.WALL_T, 0.0 - RAIL_LEN/2, zc))
                if side < 0:
                    r = r.mirror("YZ")
                asm = asm.union(r)
        except Exception as e:
            print("  (rail preview skipped:", e, ")")
    cq.exporters.export(asm, f"{outdir}/stack_preview.stl", tolerance=0.1, angularTolerance=0.2)
    bb = asm.val().BoundingBox()
    print(f"{name}: {len(parts)} panels, stack {total_t:.0f} mm, preview "
          f"{bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm -> {outdir}/")
    return outdir


def main():
    for name, v in VERSIONS.items():
        export_version(name, v)


if __name__ == "__main__":
    main()
