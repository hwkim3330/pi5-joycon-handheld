"""Laser-cut acrylic sandwich case: Raspberry Pi 5 + official 5" Touch Display 2
+ Switch (1st-gen) Joy-Con rails — rails in ACRYLIC too.

    python3 acrylic_panels.py            # -> out/acrylic/<version>/...

Headline version (v6): the acrylic only spans the LCD (16 mm). The Pi 5
(85 x 56) bolts to the display's back and hangs out the OPEN back with its
Active Cooler / NVMe HAT exposed. Front 2T dark plate covers the wide bezel and
shows only the 110.4 x 62.1 active area. Total 18 mm of acrylic.

ACRYLIC DOVETAIL RAIL (no 3D printing):
  A laser can't cut an undercut, but a T-dovetail can be BUILT from flat parts:
    - the 3T "rail" layer has a 4 mm side tab running 61 mm = the NECK
    - two 2T head strips (2.5 x 61) are solvent-glued onto the tab's faces at
      the tip = the HEAD, 7 mm wide, 1.5 mm undercut each side
  The Joy-Con's channel lips ride on smooth sheet faces, not laser edges.
  A latch notch near the top and a charge pocket (bottom 6 mm, tab removed) are
  just 2-D features of the rail layer. A 3.2 mm wire slot runs from the cavity
  through the side wall into the pocket for a stripped-USB 5 V/GND lead.

Fasteners: laser holes are perpendicular to the sheet, so 4 corner M2.5
through-bolts along the stack; v6 hides them (nuts trapped in layer 1, front
plate glued with VHB).
"""

import os, math
import cadquery as cq

# ---------- display (official Raspberry Pi Touch Display 2, 5") ----------
DISP_W, DISP_H = 143.5, 91.5        # module outline, landscape
ACT_W, ACT_H   = 110.4, 62.1        # visible active area
ACT_DX, ACT_DY = 0.0, 0.0           # active-area offset in module — CONFIRM
DISP_D         = 16.0               # module depth (Pi 5 hangs behind it)

# ---------- case geometry ----------
CLR        = 0.75
SIDE_WALL  = 8.0
TOP_WALL   = 8.0
CAV_W, CAV_H = DISP_W + 2*CLR, DISP_H + 2*CLR
W, H       = CAV_W + 2*SIDE_WALL, CAV_H + 2*TOP_WALL       # 161 x 109
R_OUT, R_CAV, R_WIN = 6.0, 3.0, 2.0
WIN_W, WIN_H = ACT_W + 1.0, ACT_H + 1.0

BOLT_D     = 2.8                    # M2.5 clearance
NUT_AF     = 5.0                    # M2.5 nut across-flats (hex trap)
BX         = W/2 - SIDE_WALL/2      # 76.5
BY_CORNER  = H/2 - TOP_WALL/2       # 50.5
BY_RAIL    = 8.0                    # printed-rail flange bolts (rail=True only)
FL_L       = 24.0

# ---------- Joy-Con rail (MEASURE-TO-CONFIRM against a real Switch rail) ----------
RAIL_LEN   = 67.0                   # total engagement incl. the pocket
RAIL_OUT   = 4.0                    # tab protrusion from the case side
POCKET_H   = 6.0                    # bottom pocket: tab removed for the charge part
TAB_LEN    = RAIL_LEN - POCKET_H    # 61 — neck tab & head strips
HEAD_W     = 2.5                    # head strip width (X): 1.5 mm undercut
HEAD_T     = 2.0                    # head strip thickness = 2T sheet
LATCH_FROM_TOP, LATCH_L, LATCH_D = 7.0, 4.5, 1.6
WIRE_W     = 3.2
IO_W       = 80.0                   # bottom I/O notch (closed-back versions only)

LAYER_T = 5.0

# ---------- versions ----------
# rail: "acrylic" | True (printed flange module) | False.  stack items: role or (role, t)
VERSIONS = {
    "v6_open_acrylic_rail": dict(
        front_t=2.0, front_holes=False, back_t=0.0, rail="acrylic",
        stack=[("nuttrap", 5.0), ("rail", 3.0), ("display", 5.0), ("display", 3.0)],  # = 16 = LCD
        note="Acrylic only around the LCD (16 mm). Pi 5 + cooler/SSD hang out the open back. "
             "Acrylic T-dovetail rails: 3T neck tab + glued 2T head strips. Nuts trapped in L1, front glued."),
    "v1_slim_black": dict(
        front_t=2.0, front_holes=False, back_t=2.0, rail=True,
        stack=["nuttrap", "display", "display", "rail", "pi", "pi", "pi"],
        note="Closed slim box, printed rail modules, hidden hardware."),
    "v2_standard": dict(
        front_t=3.0, front_holes=True, back_t=3.0, rail=True,
        stack=["plain", "display", "display", "rail", "pi", "pi", "pi"],
        note="Closed box, visible black button-heads, easiest to open."),
    "v3_tablet_norail": dict(
        front_t=3.0, front_holes=True, back_t=3.0, rail=False,
        stack=["plain", "display", "display", "pi", "pi", "pi", "pi"],
        note="No rails — a plain Pi tablet."),
    "v5_cooler_ssd": dict(
        front_t=3.0, front_holes=True, back_t=3.0, rail=True, back_fan_window=True,
        stack=["plain", "display", "display", "rail", "pi", "pi", "pi", "pi", "pi"],
        note="Closed box with room for Active Cooler + M.2 HAT; 48 mm fan window in the back."),
}


def _norm_stack(stack):
    return [(s, LAYER_T) if isinstance(s, str) else s for s in stack]


def _rrect(w, h, r, t=1.0):
    return cq.Workplane("XY").rect(w, h).extrude(t).edges("|Z").fillet(r)


def _bolt_pts(rail):
    pts = [(sx*BX, sy*BY_CORNER) for sx in (-1, 1) for sy in (-1, 1)]
    if rail is True:
        pts += [(sx*BX, sy*BY_RAIL) for sx in (-1, 1) for sy in (-1, 1)]
    return pts


def _holes(solid, pts, d):
    if not pts:
        return solid
    return solid.cut(cq.Workplane("XY").pushPoints(pts).circle(d/2).extrude(1.0))


def _hex_traps(solid, pts):
    dia = NUT_AF / math.cos(math.radians(30))
    return solid.cut(cq.Workplane("XY").pushPoints(pts).polygon(6, dia).extrude(1.0))


def panel_front(v):
    p = _rrect(W, H, R_OUT)
    p = p.cut(_rrect(WIN_W, WIN_H, R_WIN).translate((ACT_DX, ACT_DY, 0)))
    if v["front_holes"]:
        p = _holes(p, _bolt_pts(v["rail"]), BOLT_D)
    return p


def panel_back(v):
    p = _rrect(W, H, R_OUT)
    p = _holes(p, _bolt_pts(v["rail"]), BOLT_D)
    if v.get("back_fan_window"):
        p = p.cut(_rrect(48.0, 48.0, 6.0))
        for sx in (-1, 1):
            s = cq.Workplane("XY")
            for i in range(3):
                s = s.pushPoints([(sx*(34.0 + i*7.0), 0)]).slot2D(40, 3.0, 90)
            p = p.cut(s.extrude(1.0))
        return p
    s = cq.Workplane("XY")
    for i in range(-3, 4):
        s = s.pushPoints([(i*9.0, 0)]).slot2D(46, 3.2, 90)
    return p.cut(s.extrude(1.0))


def _acrylic_rail_tabs(p):
    """Add the neck tabs (+ latch notch, pocket, wire slot) to the rail layer."""
    tab_y0 = -RAIL_LEN/2 + POCKET_H                # tab spans [tab_y0, +RAIL_LEN/2]
    for sx in (-1, 1):
        xc = sx*(W/2 + RAIL_OUT/2)
        tab = (cq.Workplane("XY").center(xc, (tab_y0 + RAIL_LEN/2)/2)
               .rect(RAIL_OUT + 0.2, TAB_LEN).extrude(1.0))
        p = p.union(tab)
        # latch notch into the tab tip, near the top
        ly = RAIL_LEN/2 - LATCH_FROM_TOP
        notch = (cq.Workplane("XY").center(sx*(W/2 + RAIL_OUT - LATCH_D/2), ly)
                 .rect(LATCH_D + 0.2, LATCH_L).extrude(1.0))
        p = p.cut(notch)
        # wire slot: cavity -> through the side wall -> the pocket zone
        wy = -RAIL_LEN/2 + POCKET_H/2
        slot = (cq.Workplane("XY").center(sx*(W/2 - SIDE_WALL/2), wy)
                .rect(SIDE_WALL + 0.2, WIRE_W).extrude(1.0))
        p = p.cut(slot)
    return p


def panel_spacer(v, role):
    p = _rrect(W, H, R_OUT).cut(_rrect(CAV_W, CAV_H, R_CAV))
    pts = _bolt_pts(v["rail"])
    p = _hex_traps(p, pts) if role == "nuttrap" else _holes(p, pts, BOLT_D)
    if role == "rail":
        if v["rail"] == "acrylic":
            p = _acrylic_rail_tabs(p)
        elif v["rail"] is True:
            for sx in (-1, 1):
                p = p.cut(cq.Workplane("XY").center(sx*(W/2 - SIDE_WALL/2), 0)
                          .rect(SIDE_WALL + 0.2, FL_L).extrude(1.0))
                p = p.cut(cq.Workplane("XY").center(sx*(W/2 - SIDE_WALL/2), -RAIL_LEN/2 + 3.0)
                          .rect(SIDE_WALL + 0.2, WIRE_W).extrude(1.0))
    if role == "pi" and v["back_t"] > 0:
        p = p.cut(cq.Workplane("XY").center(0, -H/2 + TOP_WALL/2)
                  .rect(IO_W, TOP_WALL + 0.2).extrude(1.0))
    return p


def head_strip():
    return cq.Workplane("XY").rect(HEAD_W, TAB_LEN).extrude(1.0)


def build_version(v):
    parts = [("front", v["front_t"], panel_front(v))]
    for i, (role, t) in enumerate(_norm_stack(v["stack"]), 1):
        parts.append((f"L{i}_{role}", t, panel_spacer(v, role)))
    if v["rail"] == "acrylic":
        for k in range(4):
            parts.append((f"rail_head_strip_{k+1}", HEAD_T, head_strip()))
    if v["back_t"] > 0:
        parts.append(("back", v["back_t"], panel_back(v)))
    return parts


def export_version(name, v):
    outdir = f"out/acrylic/{name}"
    os.makedirs(outdir, exist_ok=True)
    parts = build_version(v)

    for label, t, solid in parts:
        cq.exporters.export(solid.faces("<Z"), f"{outdir}/{label}_{t:g}T.dxf")

    by_t = {}
    for label, t, solid in parts:
        by_t.setdefault(t, []).append((label, solid))
    for t, items in by_t.items():
        sheet = cq.Workplane("XY")
        x = 0.0; y = 0.0; row_h = 0.0; cols = 0
        for label, solid in items:
            bb = solid.val().BoundingBox()
            if cols == 4:
                x = 0.0; y -= row_h + 6.0; row_h = 0.0; cols = 0
            sheet = sheet.add(solid.translate((x - bb.xmin, y - bb.ymax, 0)).faces("<Z"))
            x += bb.xlen + 6.0; row_h = max(row_h, bb.ylen); cols += 1
        cq.exporters.export(sheet, f"{outdir}/sheet_{t:g}T.dxf")

    stack_t = sum(t for label, t, _ in parts if not label.startswith("rail_head"))
    with open(f"{outdir}/manifest.txt", "w") as f:
        f.write(f"{name}\n{v['note']}\n\n")
        f.write(f"outer {W:.1f} x {H:.1f} mm; acrylic stack {stack_t:.0f} mm"
                f"{' (+8 mm with rails)' if v['rail'] else ''}\n")
        f.write(f"display cavity {CAV_W:.1f} x {CAV_H:.1f}; window {WIN_W:.1f} x {WIN_H:.1f}\n\n")
        f.write("part                   thickness  qty\n")
        for label, t, _ in parts:
            f.write(f"{label:22s} {t:g}T        1\n")
        f.write(f"\nhardware: 4x M2.5 x {int(stack_t)+4} black button-head + M2.5 nuts"
                + (" (trapped in L1); 0.5 mm VHB for the front\n" if not v["front_holes"] else "\n"))
        if v["rail"] == "acrylic":
            f.write("rails: glue the four 2T head strips onto both faces of each rail-layer tab, "
                    "flush with the tab tip, with acrylic cement (Acrifix/Weld-On). Neck 3 mm, head 7 mm.\n")
        elif v["rail"] is True:
            f.write("rails: print joycon_rail_acrylic_L/R.stl\n")
        f.write("finish: CAST acrylic; front black or smoked. kerf ~0.15 mm; 2.8 mm holes = M2.5 clearance\n")

    # 3-D preview
    z = 0.0; asm = None; rail_z = None
    for label, t, solid in parts:
        if label.startswith("rail_head"):
            continue
        layer = solid.faces("<Z").wires().toPending().extrude(t).translate((0, 0, z))
        asm = layer if asm is None else asm.union(layer)
        if "_rail" in label:
            rail_z = (z, z + t)
        z += t
    disp = (cq.Workplane("XY").rect(DISP_W, DISP_H).extrude(DISP_D)
            .edges("|Z").fillet(2.0).translate((0, 0, v["front_t"] + 0.01)))
    asm = asm.union(disp)
    if v["back_t"] == 0:   # show the Pi 5 + cooler hanging out the open back
        pi = cq.Workplane("XY").rect(85, 56).extrude(1.6).translate((0, 0, v["front_t"] + DISP_D + 4))
        cooler = cq.Workplane("XY").rect(60, 40).extrude(16).translate((-8, 4, v["front_t"] + DISP_D + 5.6))
        asm = asm.union(pi).union(cooler)
    if v["rail"] == "acrylic" and rail_z:
        yc = (-RAIL_LEN/2 + POCKET_H + RAIL_LEN/2)/2
        for sx in (-1, 1):
            xc = sx*(W/2 + RAIL_OUT - HEAD_W/2)
            for zz in (rail_z[0] - HEAD_T, rail_z[1]):
                strip = (cq.Workplane("XY").center(xc, yc).rect(HEAD_W, TAB_LEN)
                         .extrude(HEAD_T).translate((0, 0, zz)))
                asm = asm.union(strip)
    elif v["rail"] is True:
        try:
            import joycon_rail as jr
            zc = v["front_t"] + sum(t for _, t in _norm_stack(v["stack"])[:[r for r, _ in _norm_stack(v["stack"])].index("rail")]) + 2.5
            for side in (+1, -1):
                r = jr.build(+1, foot=False).rotate((0, 0, 0), (0, 1, 0), -90).rotate((0, 0, 0), (0, 0, 1), -90)
                r = r.translate((W/2 + jr.WALL_T, -RAIL_LEN/2, zc))
                if side < 0:
                    r = r.mirror("YZ")
                asm = asm.union(r)
        except Exception as e:
            print("  (rail preview skipped:", e, ")")
    cq.exporters.export(asm, f"{outdir}/stack_preview.stl", tolerance=0.1, angularTolerance=0.2)
    print(f"{name}: {len(parts)} parts, acrylic {stack_t:.0f} mm -> {outdir}/")


def main():
    for name, v in VERSIONS.items():
        export_version(name, v)


if __name__ == "__main__":
    main()
