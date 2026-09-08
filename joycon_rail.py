"""Joy-Con (Switch 1) MALE dovetail rail — screw-on printed module.

    python3 joycon_rail.py     # -> out/joycon_rail_R.stl, out/joycon_rail_L.stl

Print with the slide axis vertical (Z): the dovetail undercut comes out as
vertical walls, no supports on the sliding faces.

Features
  - dovetail with undercut (Joy-Con only leaves by sliding up)
  - bottom lead-in taper, latch recess near the top (spring lock click)
  - charge-connector pocket at the base, open through the wall, so a stripped
    USB cable's 5V/GND can be fed to the Joy-Con pins (pin4=5V, pins1,2=GND)
  - WIRE HOLE through the backing wall behind the pocket
  - MOUNT FLANGE: a 5 mm-thick tab that drops into the notched middle acrylic
    layer of the laser-cut sandwich and is clamped by two through-bolts
  - foot with 2 screw holes (stand-alone / 3D-printed-case mounting)

Axes: X = front-back (= case depth / acrylic stack axis), Y = protrusion (+out),
Z = slide. ALL rail dims are MEASURE-TO-CONFIRM against a real Joy-Con or, best,
the real Switch console's own rail (copy it 1:1).
"""

import os
import cadquery as cq

# ---- dovetail ----
RAIL_LEN   = 67.0    # [A] engagement length (slide travel)
RAIL_OUT   = 4.0     # [B] protrusion from the wall
RAIL_BASE  = 3.4     # [C] front-back width at the wall (neck)
RAIL_HEAD  = 6.8     # [D] front-back width at the outer tip (undercut, > base)
LEAD_IN    = 4.0     # [E] bottom entry taper

# ---- latch ----
LATCH_FROM_TOP = 7.0
LATCH_W, LATCH_H, LATCH_D = 4.5, 3.5, 1.6

# ---- charge pocket (base) + wire hole ----
CONN_W, CONN_H = 12.0, 6.0     # pocket across / along slide
WIRE_W, WIRE_H = 3.2, 3.0      # wire hole through the backing wall

# ---- backing wall / foot ----
WALL_T, WALL_X = 3.0, 16.0
FOOT_L, FOOT_W, FOOT_T = 30.0, 14.0, 3.0
SCREW_D = 2.7                  # M2.5 self-tap (foot)

# ---- acrylic mount flange (matches acrylic_panels.py) ----
FL_T   = 5.0     # thickness in X = one 5T acrylic layer
FL_D   = 8.0     # depth into the case in -Y = acrylic side-wall width
FL_L   = 24.0    # length along the slide
FL_HOLE_D = 2.8  # M2.5 clearance
FL_HOLE_PITCH = 16.0


def build(side=+1, foot=True):
    prof = (cq.Workplane("XY").polyline([
        (-RAIL_BASE / 2, 0), (RAIL_BASE / 2, 0),
        (RAIL_HEAD / 2, RAIL_OUT), (-RAIL_HEAD / 2, RAIL_OUT)]).close())
    rail = prof.extrude(RAIL_LEN)
    wall = cq.Workplane("XY").center(0, -WALL_T / 2).rect(WALL_X, WALL_T).extrude(RAIL_LEN)
    foot_solid = (cq.Workplane("XY").center(0, FOOT_W / 2 - WALL_T)
            .rect(FOOT_L, FOOT_W).extrude(FOOT_T))
    fh = (cq.Workplane("XY")
          .pushPoints([(-FOOT_L / 2 + 5, FOOT_W / 2 - WALL_T),
                       (FOOT_L / 2 - 5, FOOT_W / 2 - WALL_T)])
          .circle(SCREW_D / 2).extrude(FOOT_T))
    part = rail.union(wall)
    if foot:
        part = part.union(foot_solid.cut(fh))

    # mount flange: thin in X, reaches into the case (-Y), centered on the slide
    zc = RAIL_LEN / 2
    flange = (cq.Workplane("XY").center(0, -WALL_T - FL_D / 2)
              .workplane(offset=zc - FL_L / 2).rect(FL_T, FL_D).extrude(FL_L))
    part = part.union(flange)
    # two through-holes along X (the acrylic stack bolts)
    for dz in (-FL_HOLE_PITCH / 2, FL_HOLE_PITCH / 2):
        h = (cq.Workplane("YZ").center(-WALL_T - FL_D / 2, zc + dz)
             .circle(FL_HOLE_D / 2).extrude(FL_T / 2 + 1, both=True))
        part = part.cut(h)

    # bottom lead-in
    try:
        part = part.faces("<Z").edges(">Y").chamfer(LEAD_IN * 0.7)
    except Exception:
        pass

    # latch recess near the top (outer face)
    lz = RAIL_LEN - LATCH_FROM_TOP
    latch = (cq.Workplane("XY").center(0, RAIL_OUT).workplane(offset=lz - LATCH_H / 2)
             .rect(LATCH_W, 2 * LATCH_D).extrude(LATCH_H))
    part = part.cut(latch)

    # charge pocket: cut from the tip all the way down to the wall face (y=0)
    pocket = (cq.Workplane("XY").center(0, RAIL_OUT / 2)
              .workplane(offset=CONN_H / 2).rect(CONN_W, RAIL_OUT + 0.2).extrude(CONN_H, both=True))
    part = part.cut(pocket)
    # wire hole through the backing wall, aligned with the pocket
    wire = (cq.Workplane("XY").center(0, -WALL_T / 2)
            .workplane(offset=CONN_H / 2).rect(WIRE_W, WALL_T + 0.4).extrude(WIRE_H, both=True))
    part = part.cut(wire)

    if side < 0:
        part = part.mirror("YZ")
    return part


def main():
    os.makedirs("out", exist_ok=True)
    for s, tag in ((+1, "R"), (-1, "L")):
        for foot, suffix in ((True, ""), (False, "_acrylic")):
            p = build(s, foot=foot)
            f = f"out/joycon_rail{suffix}_{tag}.stl"
            cq.exporters.export(p, f, tolerance=0.08, angularTolerance=0.2)
            bb = p.val().BoundingBox()
            print(f"exported {f}  ({bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm)")


if __name__ == "__main__":
    main()
