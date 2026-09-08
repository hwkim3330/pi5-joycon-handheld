"""DIY "Switch" handheld shell: Raspberry Pi 5 + 5" screen + Joy-Con rails.

    python3 switch_handheld.py         # -> out/switch_handheld.stl (+ preview.png)

A front shell that holds a 5" HDMI screen in the face and a Pi 5 in the back
cavity, with a Joy-Con slide rail on each side so REAL Switch Joy-Cons attach.

IMPORTANT: the Joy-Con rail here is an APPROXIMATION of Nintendo's dovetail.
The real rail has a tight locking tolerance; this profile is a tunable starting
point (RAIL_* params) and will need calibrating against an actual Joy-Con --
print just a short rail stub first and file/adjust before the full case.
"""

import os
import cadquery as cq

# ---------- parameters (mm) ----------
# Brain: Raspberry Pi 5 (85 x 56, ~16-20mm with active cooler). Screen 5" HDMI.
# Joy-Con 1 dovetail rails on both sides (screw-on printed modules, see joycon_rail.py).
W, H, DEPTH = 161.0, 109.0, 36.0    # console body (excl. rails) — matches acrylic_panels.py
WALL = 3.0
FILLET = 6.0

SCR_W, SCR_H = 143.5, 91.5          # official Pi Touch Display 2 (5") outline
SCR_ACT_W, SCR_ACT_H = 110.4, 62.1  # its active area
SCR_RECESS = 2.0                    # front bezel inset
SCR_Y = 0.0                         # active-area offset — CONFIRM on the module

PI_W, PI_H = 85.0, 56.0             # Raspberry Pi 5 board footprint
PI_HDX, PI_HDY = 58.0, 49.0         # Pi 5 mounting-hole pattern
PI_STAND = 6.0                      # standoff height
PI_TAP = 2.7                        # M2.5 self-tap

# Joy-Con CHARGING connector pocket (at each rail base). Holds a real Joy-Con
# charging-rail part (iFixit / AliExpress). Wire pin4=5V, pins1,2=GND.
CONN_W = 12.0                       # pocket width (across the rail)
CONN_H = 6.0                        # pocket height (along the slide)
CONN_D = 3.5                        # pocket depth into the rail

# ---- Joy-Con MALE rail (case side) — MEASURE THESE ON YOUR JOY-CON ----
# The console has the MALE dovetail; the Joy-Con's female channel slides down
# over it. Values below are reasonable defaults; replace with caliper readings
# of your own Joy-Con for a real locking fit (see measurement guide / notes).
RAIL_LEN = 67.0        # [A] vertical slide/engagement length
RAIL_OUT = 4.0         # [B] how far the rail stands off the side
RAIL_BASE = 3.4        # [C] front-back width at the base (the neck at the body)
RAIL_HEAD = 6.8        # [D] front-back width at the outer tip (undercut > base)
RAIL_LEADIN = 3.5      # [E] bottom lead-in taper so the Joy-Con starts sliding
NOTCH_FROM_TOP = 6.0   # [F] latch notch center, distance down from rail top
NOTCH_W = 4.0          # [G] latch notch width (along slide)
NOTCH_D = 1.4          # [H] latch notch depth (into the outer face)


def build():
    # ---- body shell, open at back ----
    body = (cq.Workplane("XY").rect(W, H).extrude(DEPTH)
            .edges("|Z").fillet(FILLET))
    # hollow: keep front wall of WALL, open the back
    cav = (cq.Workplane("XY").workplane(offset=WALL)
           .rect(W - 2 * WALL, H - 2 * WALL).extrude(DEPTH - WALL + 1))
    body = body.cut(cav)

    # ---- screen: bezel recess + active-area through hole (front at z=0) ----
    recess = (cq.Workplane("XY").center(0, SCR_Y)
              .rect(SCR_W, SCR_H).extrude(SCR_RECESS))
    through = (cq.Workplane("XY").center(0, SCR_Y)
               .rect(SCR_ACT_W, SCR_ACT_H).extrude(WALL + 1))
    body = body.cut(recess).cut(through)

    # ---- Pi 5 standoffs in the back cavity ----
    pts = [(dx, dy) for dx in (-PI_HDX / 2, PI_HDX / 2)
           for dy in (-PI_HDY / 2, PI_HDY / 2)]
    posts = (cq.Workplane("XY").workplane(offset=WALL)
             .pushPoints(pts).circle(3.2).extrude(PI_STAND))
    taps = (cq.Workplane("XY").workplane(offset=WALL)
            .pushPoints(pts).circle(PI_TAP / 2).extrude(PI_STAND + 0.1))
    body = body.union(posts).cut(taps)

    # ---- I/O opening along the bottom edge for the Nano's port bank ----
    io = (cq.Workplane("XY").center(0, -H / 2 + WALL / 2).workplane(offset=DEPTH * 0.55)
          .rect(96, DEPTH * 0.7).extrude(DEPTH, both=True))
    body = body.cut(io)

    # ---- back-cover screw bosses in the four corners ----
    bx, by = W / 2 - 6, H / 2 - 6
    bpts = [(sx * bx, sy * by) for sx in (-1, 1) for sy in (-1, 1)]
    bosses = (cq.Workplane("XY").pushPoints(bpts).circle(4).extrude(DEPTH - WALL))
    bholes = (cq.Workplane("XY").pushPoints(bpts).circle(1.4).extrude(DEPTH - WALL))
    body = body.union(bosses).cut(bholes)

    # ---- Joy-Con MALE dovetail rails, one per side ----
    body = body.union(_rail(+1)).union(_rail(-1))
    return body


def build_backcover():
    """Vented back panel. Slots sit over the Jetson heatsink so it can breathe;
    4 corner screws into the body bosses."""
    t = 2.5
    cover = (cq.Workplane("XY").rect(W - 2 * WALL - 0.6, H - 2 * WALL - 0.6)
             .extrude(t).edges("|Z").fillet(4))
    # vent slots grid over the heatsink area (center)
    slots = cq.Workplane("XY")
    for i in range(-3, 4):
        slots = slots.pushPoints([(i * 9, 0)]).slot2D(46, 3.2, 90)
    cover = cover.cut(slots.extrude(t))
    # corner screw holes matching the bosses
    bx, by = W / 2 - 6, H / 2 - 6
    bpts = [(sx * bx, sy * by) for sx in (-1, 1) for sy in (-1, 1)]
    ch = cq.Workplane("XY").pushPoints(bpts).circle(1.6).extrude(t)
    cover = cover.cut(ch)
    return cover


def _rail(side):
    """One Joy-Con dovetail rail. side=+1 right, -1 left.

    Cross-section (top view) is a trapezoid, wider at the outer tip than at the
    base -> undercut, so the Joy-Con female channel captures it and can only be
    removed by sliding vertically. A bottom lead-in taper eases the start of the
    slide, and a latch notch near the top receives the Joy-Con's spring lock.
    """
    x0 = (W / 2 - 0.6) * side          # base sits just inside the body side
    xt = x0 + RAIL_OUT * side          # outer tip
    prof = (cq.Workplane("XZ").polyline([
        (x0, -RAIL_BASE / 2), (x0, RAIL_BASE / 2),
        (xt, RAIL_HEAD / 2), (xt, -RAIL_HEAD / 2)]).close())
    rail = prof.extrude(RAIL_LEN / 2, both=True).translate((0, 0, DEPTH / 2))

    # bottom lead-in: chamfer the lower outer edges so it starts sliding
    try:
        rail = rail.edges("<Y").chamfer(RAIL_LEADIN * 0.7)
    except Exception:
        pass

    # latch notch near the top, cut into the outer face
    ny = RAIL_LEN / 2 - NOTCH_FROM_TOP
    notch = (cq.Workplane("XY").center(xt, ny).workplane(offset=DEPTH / 2)
             .rect(2 * NOTCH_D, NOTCH_W).extrude(2 * NOTCH_D, both=True))
    # (the box straddles the tip; cutting it leaves a shallow detent)
    rail = rail.cut(notch.translate((NOTCH_D * side, 0, 0)))

    # charging-connector pocket at the rail BASE (bottom of the slide), so a real
    # Joy-Con charge rail can be embedded and the Joy-Con's pins mate at the end
    cy = -RAIL_LEN / 2 + CONN_H / 2
    pocket = (cq.Workplane("XY").center(xt - CONN_D / 2 * side, cy)
              .workplane(offset=DEPTH / 2)
              .rect(CONN_D, CONN_W).extrude(CONN_W / 2, both=True))
    rail = rail.cut(pocket)
    return rail


def build_stub(L=35.0):
    """A short standing dovetail rail on a foot — print this (~10 min), slide a
    real Joy-Con onto it, and report the fit. Tune RAIL_BASE/RAIL_HEAD/RAIL_OUT
    from that, no calipers needed."""
    # dovetail fin: base (narrow) at y=0, tip (wide) at y=RAIL_OUT, extruded up Z
    prof = (cq.Workplane("XY").polyline([
        (-RAIL_BASE / 2, 0), (RAIL_BASE / 2, 0),
        (RAIL_HEAD / 2, RAIL_OUT), (-RAIL_HEAD / 2, RAIL_OUT)]).close())
    rail = prof.extrude(L)
    # backing wall + foot so it stands and prints
    wall = cq.Workplane("XY").center(0, -1.5).rect(24, 3).extrude(L)
    foot = cq.Workplane("XY").center(0, 2).rect(34, 16).extrude(3)
    stub = rail.union(wall).union(foot)
    # top lead-in so the Joy-Con starts sliding
    try:
        stub = stub.edges(">Z").chamfer(RAIL_LEADIN * 0.7)
    except Exception:
        pass
    # latch notch
    ny = L - NOTCH_FROM_TOP
    notch = (cq.Workplane("XZ").workplane(offset=-RAIL_OUT)
             .center(0, ny).rect(NOTCH_W, 2 * NOTCH_D).extrude(2 * NOTCH_D, both=True))
    try:
        stub = stub.cut(notch)
    except Exception:
        pass
    return stub


def main():
    os.makedirs("out", exist_ok=True)
    model = build()
    stl = "out/switch_handheld.stl"
    cq.exporters.export(model, stl, tolerance=0.1, angularTolerance=0.2)
    bb = model.val().BoundingBox()
    print(f"exported {stl}")
    print(f"size: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm "
          f"(rails add ~{2*RAIL_OUT:.0f}mm width)")

    stub = build_stub()
    cq.exporters.export(stub, "out/rail_stub.stl", tolerance=0.1, angularTolerance=0.2)
    print("exported out/rail_stub.stl  (print this first to test Joy-Con fit)")

    cover = build_backcover()
    cq.exporters.export(cover, "out/back_cover.stl", tolerance=0.1, angularTolerance=0.2)
    print("exported out/back_cover.stl  (vented, 4 corner screws)")
    return stl


if __name__ == "__main__":
    main()
