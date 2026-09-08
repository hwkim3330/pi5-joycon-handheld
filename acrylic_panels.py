"""Laser-cut acrylic case: Raspberry Pi 5 + official 5" Touch Display 2 with
FEMALE Joy-Con T-slots — the way the real Switch does it.

    python3 acrylic_panels.py            # -> out/acrylic/<version>/...

On a Switch the CONSOLE has the slot and the JOY-CON carries the male metal
rail + spring pin. So this case cuts a T-slot into each side, open at the top:
the Joy-Con slides down from the top and its pin clicks into a notch. Slot
dimensions come from the field-tested Cuttlephone project (SiloCityLabs), the
open-source phone case that takes real Joy-Cons:

    mouth (lip gap)      7.1 mm     lip thickness      0.7 mm (we use 1.0 in acrylic)
    inner cavity width  10.1 mm     cavity depth       2.4 mm ("as low as 2.3")
    lock notch           3.8 mm wide, 9.4 mm from the top, 1.5 mm deep
    Joy-Con rail length 91.5 mm

Why acrylic loves this: a T-slot is just per-layer 2-D cuts along the stack.
    [1.5T pocket][5T mouth][2T mouth][1.5T pocket]  ->  mouth 7.0, inner 10.0
  - mouth layers: full-depth notch (lip + cavity) from the outer face
  - pocket layers: hidden pocket that stops 1.0 mm short of the face = the lip
  - the lock notch is the lip removed over 3.8 mm in the pocket layers
Order the mouth TIGHT (7.0 vs 7.1) and sand the sheet faces if it binds; loose
cannot be fixed. If your shop has no 1.5T, use 2T pocket layers (inner 11.0, a
little side play).

Everything else: dark 2T front covers the display bezel (window = active area),
Pi 5 (85 x 56) bolts to the display's back and hangs out the OPEN back with its
cooler/SSD exposed, 4 corner M2.5 through-bolts into nuts trapped in layer 1.
"""

import os, math
import cadquery as cq

# ---------- display (official Raspberry Pi Touch Display 2, 5") ----------
DISP_W, DISP_H = 143.5, 91.5
ACT_W, ACT_H   = 110.4, 62.1
ACT_DX, ACT_DY = 0.0, 0.0           # CONFIRM on the module
DISP_D         = 16.0               # module depth; Pi hangs behind

# ---------- case ----------
CLR        = 0.75
SIDE_WALL  = 9.0                    # slot (3.4) + bolt + margins
TOP_WALL   = 8.0
CAV_W, CAV_H = DISP_W + 2*CLR, DISP_H + 2*CLR                 # 145 x 93
W, H       = CAV_W + 2*SIDE_WALL, CAV_H + 2*TOP_WALL         # 163 x 109
R_OUT, R_CAV, R_WIN = 6.0, 3.0, 2.0
WIN_W, WIN_H = ACT_W + 1.0, ACT_H + 1.0

BOLT_D     = 2.8                    # M2.5 clearance
NUT_AF     = 5.0                    # M2.5 nut across flats
BX         = W/2 - SIDE_WALL + 3.5  # 76.0: clears the slot (78.1) and the cavity (72.5)
BY         = H/2 - TOP_WALL/2       # 50.5

# ---------- Joy-Con T-slot (Cuttlephone-measured) ----------
LIP        = 1.0                    # acrylic lip (Nintendo 0.7); Joy-Con sits 0.3 proud
CAV_D      = 2.4                    # cavity depth behind the lip
SLOT_D     = LIP + CAV_D            # 3.4 total from the outer face
JC_RAIL    = 91.5                   # Joy-Con rail length -> seat depth from the top edge
POCKET_H   = 6.0                    # charge-connector zone below the seat
NOTCH_W    = 3.8
NOTCH_FROM_TOP = 9.4
WIRE_W     = 3.2
IO_W       = 80.0

SEAT_Y     = H/2 - JC_RAIL          # -37.0: where the Joy-Con rail bottoms out
SLOT_Y0    = SEAT_Y - POCKET_H      # -43.0: slot/pocket bottom
NOTCH_Y    = H/2 - NOTCH_FROM_TOP   # 45.1

LAYER_T = 5.0

# stack roles: nuttrap | plain | display | pi | mouth | pocket
SLOT_BAND = [("pocket", 1.5), ("mouth", 5.0), ("mouth", 2.0), ("pocket", 1.5)]   # 10.0 = inner width

VERSIONS = {
    "v6_open_slot": dict(
        front_t=2.0, front_holes=False, back_t=0.0, rail=True,
        stack=[("nuttrap", 3.0)] + SLOT_BAND + [("display", 3.0)],              # 16 = LCD depth
        note="Acrylic only around the LCD (16 mm), open back, Joy-Con T-slots cut into the layers. "
             "Nuts trapped in L1, 2T front glued. THE ONE TO BUILD."),
    "v2_closed_slot": dict(
        front_t=3.0, front_holes=True, back_t=3.0, rail=True,
        stack=[("plain", 3.0)] + SLOT_BAND + [("display", 3.0), "pi", "pi", "pi"],
        note="Closed box with the same T-slots; visible black button-heads."),
    "v3_tablet_norail": dict(
        front_t=3.0, front_holes=True, back_t=3.0, rail=False,
        stack=["plain", "display", "display", "pi", "pi", "pi", "pi"],
        note="No Joy-Con slots — a plain Pi tablet."),
    "v5_cooler_ssd_slot": dict(
        front_t=3.0, front_holes=True, back_t=3.0, rail=True, back_fan_window=True,
        stack=[("plain", 3.0)] + SLOT_BAND + [("display", 3.0), "pi", "pi", "pi", "pi", "pi"],
        note="Closed box with room for Active Cooler + M.2 HAT; 48 mm fan window in the back."),
}


def _norm(stack):
    return [(s, LAYER_T) if isinstance(s, str) else s for s in stack]


def _rrect(w, h, r, t=1.0):
    return cq.Workplane("XY").rect(w, h).extrude(t).edges("|Z").fillet(r)


def _bolt_pts():
    return [(sx*BX, sy*BY) for sx in (-1, 1) for sy in (-1, 1)]


def _cut(solid, cx, cy, w, h):
    return solid.cut(cq.Workplane("XY").center(cx, cy).rect(w, h).extrude(1.0))


def _holes(solid, pts, d):
    return solid.cut(cq.Workplane("XY").pushPoints(pts).circle(d/2).extrude(1.0))


def _hex(solid, pts):
    dia = NUT_AF / math.cos(math.radians(30))
    return solid.cut(cq.Workplane("XY").pushPoints(pts).polygon(6, dia).extrude(1.0))


def panel_front(v):
    p = _rrect(W, H, R_OUT).cut(_rrect(WIN_W, WIN_H, R_WIN).translate((ACT_DX, ACT_DY, 0)))
    return _holes(p, _bolt_pts(), BOLT_D) if v["front_holes"] else p


def panel_back(v):
    p = _holes(_rrect(W, H, R_OUT), _bolt_pts(), BOLT_D)
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


def panel_layer(v, role, wire=False):
    p = _rrect(W, H, R_OUT).cut(_rrect(CAV_W, CAV_H, R_CAV))
    p = _hex(p, _bolt_pts()) if role == "nuttrap" else _holes(p, _bolt_pts(), BOLT_D)
    y_top = H/2 + 0.2                          # open through the top edge
    span = y_top - SLOT_Y0
    yc = (y_top + SLOT_Y0) / 2
    for sx in (-1, 1):
        face = sx * W/2
        if role == "mouth":
            # full-depth slot: lip zone + cavity, open at the top
            p = _cut(p, sx*(W/2 - SLOT_D/2) , yc, SLOT_D + 0.2, span)
            if wire:   # 5 V/GND lead from the display cavity into the charge pocket
                p = _cut(p, sx*(W/2 - SIDE_WALL/2), SEAT_Y - POCKET_H/2, SIDE_WALL + 0.2, WIRE_W)
        elif role == "pocket":
            # hidden cavity behind a LIP-thick wall, open at the top
            p = _cut(p, sx*(W/2 - LIP - CAV_D/2), yc, CAV_D, span)
            # lock notch: remove the lip over NOTCH_W so the Joy-Con pin clicks out
            p = _cut(p, sx*(W/2 - LIP/2), NOTCH_Y, LIP + 0.2, NOTCH_W)
    if role == "pi" and v["back_t"] > 0:
        p = _cut(p, 0, -H/2 + TOP_WALL/2, IO_W, TOP_WALL + 0.2)
    return p


def build_version(v):
    parts = [("front", v["front_t"], panel_front(v))]
    first_mouth = True
    for i, (role, t) in enumerate(_norm(v["stack"]), 1):
        if not v["rail"] and role in ("mouth", "pocket"):
            role = "display"
        wire = role == "mouth" and first_mouth
        if wire:
            first_mouth = False
        parts.append((f"L{i}_{role}", t, panel_layer(v, role, wire)))
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
        sheet = cq.Workplane("XY"); x = 0.0; y = 0.0; row_h = 0.0; cols = 0
        for label, solid in items:
            bb = solid.val().BoundingBox()
            if cols == 4:
                x = 0.0; y -= row_h + 6.0; row_h = 0.0; cols = 0
            sheet = sheet.add(solid.translate((x - bb.xmin, y - bb.ymax, 0)).faces("<Z"))
            x += bb.xlen + 6.0; row_h = max(row_h, bb.ylen); cols += 1
        cq.exporters.export(sheet, f"{outdir}/sheet_{t:g}T.dxf")

    total = sum(t for _, t, _ in parts)
    with open(f"{outdir}/manifest.txt", "w") as f:
        f.write(f"{name}\n{v['note']}\n\n")
        f.write(f"outer {W:.1f} x {H:.1f} mm; acrylic stack {total:.1f} mm\n")
        f.write(f"display cavity {CAV_W:.1f} x {CAV_H:.1f}; window {WIN_W:.1f} x {WIN_H:.1f}\n")
        if v["rail"]:
            f.write(f"Joy-Con T-slot: mouth 7.0 (5T+2T), inner 10.0, lip {LIP}, cavity {CAV_D}, "
                    f"open top, seat {JC_RAIL} mm below the top edge, notch {NOTCH_W} @ {NOTCH_FROM_TOP} from top\n")
        f.write("\npart               thickness\n")
        for label, t, _ in parts:
            f.write(f"{label:18s} {t:g}T\n")
        f.write(f"\nhardware: 4x M2.5 x {int(total)+4} black button-head + M2.5 nuts"
                + (" (trapped in L1); 0.5 mm VHB for the front\n" if not v["front_holes"] else "\n"))
        f.write("finish: CAST acrylic; front black/smoked. Bond layers with acrylic cement or rely on the bolts.\n"
                "fit: mouth is deliberately 0.1 tight — sand the 5T/2T sheet faces if the Joy-Con binds.\n")

    # 3-D preview
    z = 0.0; asm = None
    for label, t, solid in parts:
        layer = solid.faces("<Z").wires().toPending().extrude(t).translate((0, 0, z))
        asm = layer if asm is None else asm.union(layer); z += t
    disp = (cq.Workplane("XY").rect(DISP_W, DISP_H).extrude(DISP_D)
            .edges("|Z").fillet(2.0).translate((0, 0, v["front_t"] + 0.01)))
    asm = asm.union(disp)
    if v["back_t"] == 0:
        pi = cq.Workplane("XY").rect(85, 56).extrude(1.6).translate((0, 0, v["front_t"] + DISP_D + 4))
        cooler = cq.Workplane("XY").rect(60, 40).extrude(16).translate((-8, 4, v["front_t"] + DISP_D + 5.6))
        asm = asm.union(pi).union(cooler)
    cq.exporters.export(asm, f"{outdir}/stack_preview.stl", tolerance=0.1, angularTolerance=0.2)
    print(f"{name}: {len(parts)} parts, acrylic {total:.1f} mm -> {outdir}/")


def main():
    for name, v in VERSIONS.items():
        export_version(name, v)


if __name__ == "__main__":
    main()
