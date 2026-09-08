"""Clear laser-cut acrylic handheld: Raspberry Pi 5 + Raspberry Pi Touch Display 2 (5")
+ 1st-gen Joy-Cons in FEMALE T-slots.  Source of truth for every dimension.

    python3 acrylic_panels.py        -> out/acrylic/<version>/  (DXF, manifest, STL)
    python3 render_previews.py       -> preview PNGs in the same folders

Fabrication intent (not a render toy):
  * 100 % CLEAR CAST acrylic, silver/stainless M2.5 button-head hardware.
  * Open back: the Pi 5, its Active Cooler / NVMe HAT, cables all visible.
  * The Pi 5 is screwed to the DISPLAY's four rear stand-offs with the four M2.5
    screws shipped with the display (official install). Those screws hold the Pi to
    the LCD. They do NOT hold the LCD in the case.
  * The LCD is captive like in any bezel: layer 1 is a pocket for the 0.70 mm cover
    glass; the layers behind have a smaller, frame-sized cavity, so the glass border
    rests on a ledge (>= 4.6 mm wide). Front plate in front, ledge behind, open back.
  * Every layer and the front share four M2.5 through-bolts: silver button-head in
    front, washer + nut on the last layer's rear face. Fully serviceable, no glue.

Display geometry is measured from the official 5" STEP (reference/td2_5in.step):
glass 91.46 x 143.40 x 0.70 R5, rear frame 72.96 x 124.74 set 3.47 off the glass centre,
total depth 10.40 (the docs' "16 mm" is not the bare module), active area 2.47 off the
glass centre. Active 62.1 x 110.4 / viewing 63.0 x 111.5 from the product brief.
Official drawings are reference-only: measure a real part before a volume order.

Joy-Con slot: Nintendo puts the FEMALE slot on the console, the MALE rail on the
Joy-Con. Reference geometry is derived from the field-tested Cuttlephone project
(SiloCityLabs, phone_case.scad): mouth 7.1, inner 10.1, cavity 2.4, notch 3.8 wide
9.4 from the top, rail 91.5. Here it is built from stacked layers:
    [pocket][mouth 5T][mouth 2T][pocket]  -> mouth 7.0, inner 10.0 (1.5T pockets)
Laser kerf and real sheet thickness still need a PHYSICAL fit test (see coupons).

Kerf policy: all DXF geometry is NOMINAL finished geometry. Cutter compensation is
the shop's job. Do not add your own kerf offset on top.
"""

import os, math, sys
import cadquery as cq

# =============================== display (from the official 5" STEP) =========
# Measured in reference/td2_5in.step (RP-009152-DD-1). Landscape here: case X = display
# long axis (portrait Y), case Y = display short axis (portrait X). Origin = glass centre.
GLASS_W, GLASS_H, GLASS_T = 143.40, 91.46, 0.70   # cover glass outline / thickness
GLASS_R          = 5.0                            # corner radius (8 R5 edges in the STEP)
FRAME_W, FRAME_H = 124.74, 72.96                  # rear frame footprint (largest rear body)
FRAME_DX, FRAME_DY = -3.47, 0.0                   # frame centre vs glass centre
FRAME_BEHIND_GLASS = 9.70                         # frame rear plane behind the glass back
DISP_D           = GLASS_T + FRAME_BEHIND_GLASS   # 10.40 total (NOT the 16 mm quoted in docs)
PANEL_DX         = -2.47                          # active-area (panel) centre vs glass centre
POST_XY          = [(sx*51.85, sy*25.5) for sx in (-1, 1) for sy in (-1, 1)]   # 4x M2.5 rear points, 103.7 x 51.0
# Product brief / documentation
ACTIVE_W, ACTIVE_H = 110.4, 62.1
VIEW_W, VIEW_H   = 111.5, 63.0
ACT_DX, ACT_DY   = PANEL_DX, 0.0                  # window centre; flip the sign if you rotate the other way
WINDOW_MARGIN    = 0.25
WIN_W, WIN_H     = VIEW_W + 2*WINDOW_MARGIN, VIEW_H + 2*WINDOW_MARGIN     # 112.0 x 63.5
R_WIN            = 2.0
# legacy aliases used by the docs
DISP_W, DISP_H, DISP_R = GLASS_W, GLASS_H, GLASS_R

# Pi 5 (85 x 56). The 5" STEP has NO 58 x 49 Pi hole pattern: its four rear M2.5 points
# are 103.7 x 51.0 apart, so a bracket is involved. Modelled as a block for previews only.
PI_W, PI_H = 85.0, 56.0

# =============================== case body ====================================
CLR_GLASS  = 0.50                    # radial clearance around the glass (L1 pocket)
CLR_FRAME  = 0.75                    # radial clearance around the rear frame (ledge layers)
SIDE_WALL  = 10.0                    # L1 side wall: 3.4 slot + bolt + ligaments
TOP_WALL   = 8.0
GCAV_W, GCAV_H = GLASS_W + 2*CLR_GLASS, GLASS_H + 2*CLR_GLASS          # 144.4 x 92.46
GCAV_R     = GLASS_R + CLR_GLASS
FCAV_W, FCAV_H = FRAME_W + 2*CLR_FRAME, FRAME_H + 2*CLR_FRAME          # 126.24 x 74.46
FCAV_R     = 3.0
W, H       = GCAV_W + 2*SIDE_WALL, GCAV_H + 2*TOP_WALL                # 164.4 x 108.46
R_OUT      = 6.0
CAV_W, CAV_H = GCAV_W, GCAV_H        # aliases

# =============================== hardware =====================================
BOLT_NOM   = 2.5
BOLT_CLEAR = 2.8
WASHER_T   = 0.5
NUT_T      = 2.0
THREAD_STICKOUT = 1.5
STD_BOLT_LENGTHS = (12, 14, 16, 18, 20, 22, 25, 30)
BX         = W/2 - SIDE_WALL + 4.0
BY         = H/2 - TOP_WALL/2

# =============================== Joy-Con slot =================================
LIP        = 1.0
CAV_D      = 2.4
SLOT_D     = LIP + CAV_D
JC_RAIL    = 91.5
POCKET_H   = 6.0
NOTCH_W, NOTCH_FROM_TOP = 3.8, 9.4
WIRE_W     = 3.2
SEAT_Y     = H/2 - JC_RAIL
SLOT_Y0    = SEAT_Y - POCKET_H
NOTCH_Y    = H/2 - NOTCH_FROM_TOP
MOUTH_TARGET, INNER_TARGET = 7.1, 10.1

# =============================== glass gasket =================================
# The glass (0.70) sits in the L1 pocket; the rest of L1's thickness is taken up by a
# compressible foam/silicone gasket ring on the ledge behind the glass border.
GASKET_W   = 4.0                     # ring width on the ledge

# =============================== versions =====================================
# roles: gpocket = glass pocket + slot pocket (L1) | mouth | pocket | plain (frame-size cavity)
def _stack(pocket_t, tail):
    return [("gpocket", pocket_t), ("mouth", 5.0), ("mouth", 2.0), ("pocket", pocket_t)] + tail

VERSIONS = {
    "v7_clear_exact": dict(
        front_t=2.0, stack=_stack(1.5, [("plain", 1.5)]), shim=0.0,
        note="Closest to the reference: 1.5T pocket layers -> Joy-Con inner 10.0. Needs 1.5T clear cast "
             "(not a standard Acrylzip option). Body 11.5 = module 10.4 fully inside."),
    "v7_clear_acrylzip": dict(
        front_t=2.0, stack=_stack(2.0, []), shim=0.45,
        note="Standard 2T/3T/5T only. 2T pocket layers -> RAW Joy-Con inner 11.0 (0.9 over reference); "
             "bring to ~10.1 with 0.45 mm clear PET liners on each pocket face. Body 11.0."),
}

COUPON_LEN = 40.0
COUPON_W   = 16.0


# =============================== geometry helpers ============================
def _rrect(w, h, r, t=1.0):
    return cq.Workplane("XY").rect(w, h).extrude(t).edges("|Z").fillet(r)

def _cut(solid, cx, cy, w, h):
    return solid.cut(cq.Workplane("XY").center(cx, cy).rect(w, h).extrude(1.0))

def _holes(solid, pts, d):
    return solid.cut(cq.Workplane("XY").pushPoints(pts).circle(d/2).extrude(1.0))

def bolt_pts():
    return [(sx*BX, sy*BY) for sx in (-1, 1) for sy in (-1, 1)]


def panel_front(v):
    p = _rrect(W, H, R_OUT).cut(_rrect(WIN_W, WIN_H, R_WIN).translate((ACT_DX, ACT_DY, 0)))
    return _holes(p, bolt_pts(), BOLT_CLEAR)


def slot_features(p, role, wire=False, y_top=None, y_bot=None):
    """Cut the Joy-Con slot features for one side-wall layer."""
    y_top = H/2 + 0.2 if y_top is None else y_top
    y_bot = SLOT_Y0 if y_bot is None else y_bot
    span, yc = y_top - y_bot, (y_top + y_bot)/2
    for sx in (-1, 1):
        if role == "mouth":
            p = _cut(p, sx*(W/2 - SLOT_D/2 + 0.1), yc, SLOT_D + 0.2, span)       # floor exactly at W/2-SLOT_D; overshoot outward only
            if wire:
                p = _cut(p, sx*(W/2 - SIDE_WALL/2), SEAT_Y - POCKET_H/2, SIDE_WALL + 0.2, WIRE_W)
        elif role == "pocket":
            p = _cut(p, sx*(W/2 - LIP - CAV_D/2), yc, CAV_D, span)               # hidden cavity behind the lip
            p = _cut(p, sx*(W/2 - LIP/2 + 0.1), NOTCH_Y, LIP + 0.2, NOTCH_W)     # lock notch = lip removed (overshoot outward)
    return p


def panel_layer(role, wire=False):
    p = _rrect(W, H, R_OUT)
    if role == "gpocket":
        p = p.cut(_rrect(GCAV_W, GCAV_H, GCAV_R))                                   # glass sits here
    else:
        p = p.cut(_rrect(FCAV_W, FCAV_H, FCAV_R).translate((FRAME_DX, FRAME_DY, 0)))  # ledge for the glass border
    p = _holes(p, bolt_pts(), BOLT_CLEAR)
    return slot_features(p, "pocket" if role == "gpocket" else role, wire)


def coupon_piece(role, wire=False):
    """Section of one side-wall layer, from the top edge down COUPON_LEN, COUPON_W wide,
    with the identical slot geometry and two M2.5 clamp holes."""
    y_top, y_bot = H/2, H/2 - COUPON_LEN
    piece = (cq.Workplane("XY").center(W/2 - COUPON_W/2, (y_top + y_bot)/2)
             .rect(COUPON_W, COUPON_LEN).extrude(1.0))
    piece = _holes(piece, [(BX, y_top - 5.0), (BX, y_bot + 5.0)], BOLT_CLEAR)
    # only the +X side exists in the coupon. Slot open at the top edge, solid 6 mm stop
    # at the bottom so the Joy-Con seats like it does on the real case.
    stop = 6.0
    y_top2, y_bot2 = y_top + 0.2, y_bot + stop
    span, yc = y_top2 - y_bot2, (y_top2 + y_bot2)/2
    if role == "mouth":
        piece = _cut(piece, W/2 - SLOT_D/2 + 0.1, yc, SLOT_D + 0.2, span)
    elif role == "pocket":
        piece = _cut(piece, W/2 - LIP - CAV_D/2, yc, CAV_D, span)
        piece = _cut(piece, W/2 - LIP/2 + 0.1, NOTCH_Y, LIP + 0.2, NOTCH_W)
    return piece


# =============================== checks =======================================
class DesignError(Exception):
    pass

def _check(cond, msg):
    if not cond:
        raise DesignError(msg)

def bolt_length(total_stack):
    need = total_stack + WASHER_T + NUT_T + THREAD_STICKOUT
    rec = next((L for L in STD_BOLT_LENGTHS if L >= need), None)
    _check(rec is not None, f"no standard bolt >= {need:.1f} mm")
    return need, rec

def validate(v):
    body = sum(t for _, t in v["stack"])
    total = v["front_t"] + body
    mouth = sum(t for r, t in v["stack"] if r == "mouth")
    inner = mouth + sum(t for r, t in v["stack"] if r in ("pocket", "gpocket"))
    eff_inner = inner - 2*v["shim"]
    r = BOLT_CLEAR/2
    g_t = v["stack"][0][1]
    # display fit
    _check(v["stack"][0][0] == "gpocket", "first layer must be the glass pocket")
    _check(GCAV_W > GLASS_W and GCAV_H > GLASS_H, "glass pocket must exceed the glass outline")
    _check(FCAV_W > FRAME_W and FCAV_H > FRAME_H, "ledge cavity must exceed the rear frame")
    _check(WIN_W > VIEW_W and WIN_H > VIEW_H, "window must exceed the viewing area")
    _check(WIN_W < GLASS_W and WIN_H < GLASS_H, "window must be smaller than the glass")
    _check(abs(ACT_DX) + WIN_W/2 < GLASS_W/2 - 3.0, "window too close to the glass edge")
    # ledge: glass border resting width on every side (glass overhang past the ledge cavity)
    ledge_xp = (GLASS_W/2) - (FRAME_DX + FCAV_W/2)
    ledge_xm = (GLASS_W/2) - (-FRAME_DX + FCAV_W/2)
    ledge_y  = (GLASS_H/2) - (FCAV_H/2)
    _check(min(ledge_xp, ledge_xm, ledge_y) >= 4.0, f"glass ledge too narrow: {ledge_xp:.2f}/{ledge_xm:.2f}/{ledge_y:.2f}")
    _check(g_t > GLASS_T + 0.3, "glass pocket layer too thin for the glass + gasket")
    _check(body >= DISP_D, f"body {body} shallower than the module {DISP_D:.2f} (frame would protrude)")
    _check(body - DISP_D <= 2.0, f"body {body} recesses the module too deep")
    # bolts
    _check(BX - r - GCAV_W/2 >= 1.5, "bolt hole too close to the glass pocket (side)")
    _check(BY - r - GCAV_H/2 >= 1.2, "bolt hole too close to the glass pocket (top)")
    _check((W/2 - SLOT_D) - (BX + r) >= 1.0, "bolt hole ligament to the Joy-Con slot < 1.0 mm")
    _check(SIDE_WALL - SLOT_D >= 4.0, "side wall too thin behind the slot")
    # slot nominal
    _check(abs(mouth - 7.0) < 1e-6, f"mouth {mouth} != 7.0 (5T+2T)")
    _check(9.5 <= inner <= 11.5, f"inner {inner} out of range")
    need, rec = bolt_length(total)
    gasket = g_t - GLASS_T + 0.2          # uncompressed thickness to specify
    return dict(body=body, total=total, mouth=mouth, inner=inner, eff_inner=eff_inner,
                bolt_need=need, bolt_rec=rec, gasket=gasket,
                ledge=(ledge_xp, ledge_xm, ledge_y))


# =============================== export =======================================
def export_dxf(solid, path):
    cq.exporters.export(solid.faces("<Z"), path)

def export_sheets(parts, outdir):
    by_t = {}
    for label, t, solid in parts:
        by_t.setdefault(t, []).append((label, solid))
    for t, items in by_t.items():
        sheet = cq.Workplane("XY"); x = y = row_h = 0.0; cols = 0
        for label, solid in items:
            bb = solid.val().BoundingBox()
            if cols == 4:
                x = 0.0; y -= row_h + 6.0; row_h = 0.0; cols = 0
            sheet = sheet.add(solid.translate((x - bb.xmin, y - bb.ymax, 0)).faces("<Z"))
            x += bb.xlen + 6.0; row_h = max(row_h, bb.ylen); cols += 1
        cq.exporters.export(sheet, f"{outdir}/sheet_{t:g}T.dxf")
    return sorted(by_t)


def build_case(v):
    parts = [("front", v["front_t"], panel_front(v))]
    first_mouth = True
    for i, (role, t) in enumerate(v["stack"], 1):
        wire = role == "mouth" and first_mouth
        first_mouth = first_mouth and not wire
        parts.append((f"L{i}_{role}", t, panel_layer(role, wire)))
    return parts


def build_coupon(v):
    parts = []
    first_mouth = True
    for i, (role, t) in enumerate(v["stack"], 1):
        wire = role == "mouth" and first_mouth
        first_mouth = first_mouth and not wire
        parts.append((f"C{i}_{role}", t, coupon_piece(role)))
    return parts


def stack_stl(parts, path, front_t):
    z = 0.0; asm = None
    for label, t, solid in parts:
        layer = solid.faces("<Z").wires().toPending().extrude(t).translate((0, 0, z))
        asm = layer if asm is None else asm.union(layer); z += t
    cq.exporters.export(asm, path, tolerance=0.1, angularTolerance=0.2)
    return z


def write_manifest(name, v, parts, thick, m, outdir, coupon=False):
    with open(f"{outdir}/manifest.txt", "w") as f:
        f.write(f"{name}\n{v['note']}\n\n")
        f.write("MATERIAL: clear (transparent) CAST acrylic, all parts. Hardware: silver/stainless.\n\n")
        if not coupon:
            f.write(f"body {W:.1f} x {H:.1f} mm; acrylic stack front+body = {m['total']:.1f} mm "
                    f"(body {m['body']:.1f}, module {DISP_D:.2f} -> rear {m['body']-DISP_D:+.2f} inside)\n")
            f.write(f"glass pocket {GCAV_W:.2f} x {GCAV_H:.2f} (L1); ledge cavity {FCAV_W:.2f} x {FCAV_H:.2f} "
                    f"offset {FRAME_DX:+.2f}; window {WIN_W:.1f} x {WIN_H:.1f} at x={ACT_DX:+.2f} "
                    f"(viewing {VIEW_W} x {VIEW_H} + {WINDOW_MARGIN}/side)\n")
            f.write(f"glass gasket: ring {GASKET_W} mm wide on the ledge, {m['gasket']:.1f} mm uncompressed foam/silicone\n")
        f.write(f"Joy-Con slot: mouth {m['mouth']:.1f} (target {MOUTH_TARGET}), raw inner {m['inner']:.1f} "
                f"(target {INNER_TARGET})")
        f.write(f", with {v['shim']} mm liners -> {m['eff_inner']:.2f}\n" if v["shim"] else "\n")
        f.write(f"lip {LIP}, cavity {CAV_D}, slot {SLOT_D} from face, open top, notch {NOTCH_W} @ {NOTCH_FROM_TOP} from top\n\n")
        f.write("part                    thickness  qty\n")
        seen = {}
        for label, t, _ in parts:
            key = (label, t)
            seen[key] = seen.get(key, 0) + 1
        for (label, t), n in seen.items():
            f.write(f"{label:22s}  {t:g}T        {n}\n")
        f.write(f"\nthicknesses to order: {', '.join(f'{t:g}T' for t in thick)}\n")
        if not coupon:
            f.write(f"\nCASE BOLTS (separate from the 4 display->Pi screws shipped with the display):\n"
                    f"  4x M2.5 silver button-head, length >= {m['bolt_need']:.1f} mm "
                    f"(stack {m['total']:.1f} + washer {WASHER_T} + nut {NUT_T} + {THREAD_STICKOUT} stick-out)"
                    f" -> use M2.5 x {m['bolt_rec']} mm\n"
                    f"  4x M2.5 washer, 4x M2.5 nut (nyloc: add 1 mm to the length)\n")
        else:
            f.write(f"\nclamp with 2x M2.5 x 25 + nuts; slide a Joy-Con a few cm from the open top.\n"
                    f"tight -> sand the 5T/2T sheet faces lightly; loose -> add/adjust liners.\n")
        f.write("\nKERF: DXF is nominal finished geometry; the shop applies cutter compensation. Do not add kerf yourself.\n")


def export_version(name, v):
    m = validate(v)                                    # raises before anything is written
    outdir = f"out/acrylic/{name}"; os.makedirs(outdir, exist_ok=True)
    parts = build_case(v)
    for label, t, solid in parts:
        export_dxf(solid, f"{outdir}/{label}_{t:g}T.dxf")
    thick = export_sheets(parts, outdir)
    stack_stl(parts, f"{outdir}/stack_preview.stl", v["front_t"])
    write_manifest(name, v, parts, thick, m, outdir)
    liner = f" -> {m['eff_inner']:.2f} with liners" if v["shim"] else ""
    print(f"{name}: {len(parts)} parts, stack {m['total']:.1f} mm, inner {m['inner']:.1f}{liner}, "
          f"bolt M2.5x{m['bolt_rec']}")
    return m


def export_coupon(name, v):
    m = validate(v)
    outdir = f"out/acrylic/test_coupon_{name.split('_')[-1]}"; os.makedirs(outdir, exist_ok=True)
    parts = build_coupon(v)
    for label, t, solid in parts:
        export_dxf(solid, f"{outdir}/{label}_{t:g}T.dxf")
    thick = export_sheets(parts, outdir)
    stack_stl(parts, f"{outdir}/stack_preview.stl", 0)
    cv = dict(v, note=f"FIT COUPON for {name}: {COUPON_LEN:g} mm slot section, identical layer order and slot geometry. "
                      "Cut this first, clamp the six pieces with two M2.5 bolts, slide a Joy-Con in from the open top.")
    write_manifest(f"test_coupon_{name.split('_')[-1]}", cv, parts, thick, m, outdir, coupon=True)
    print(f"coupon {name}: {len(parts)} pieces")


def main():
    for name, v in VERSIONS.items():
        export_version(name, v)
        export_coupon(name, v)


if __name__ == "__main__":
    try:
        main()
    except DesignError as e:
        print("DESIGN CHECK FAILED:", e); sys.exit(1)
