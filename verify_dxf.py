"""Cross-check the exported DXFs against acrylic_panels.py, and check the as-ordered
version against dimensions measured from the fabrication drawing.   python3 verify_dxf.py"""
import ezdxf, glob, os, sys
from ezdxf import bbox
import acrylic_panels as ap

# Measured from KETI_Acrylic_Order_REV4_StraightGuide_Transparent_2T_3T.dxf, converted
# to each part's own outline centre. This is the geometry that was actually ordered.
REV4 = dict(outline=(164.40, 108.46), hole=(76.20, 50.23, 2.8), window=(112.00, 63.50, -2.47),
            glass_hw=72.20, ledge=(126.24, 74.46, -3.47), groove_floor=78.80,
            groove_bottom=-43.27, recess_inner=72.00, recess_h=3.20, recess_cy=-40.27)

ok = True
def chk(c, msg):
    global ok; print(("  OK   " if c else "  FAIL ") + msg); ok = ok and c
def ents(f): return list(ezdxf.readfile(f).modelspace())
def circles(f): return [e for e in ents(f) if e.dxftype() == "CIRCLE"]
def vx(f): return sorted({round(l.dxf.start.x, 3) for l in ents(f) if l.dxftype() == "LINE"
                          and abs(l.dxf.start.x - l.dxf.end.x) < 1e-6})
def hy(f): return sorted({round(l.dxf.start.y, 3) for l in ents(f) if l.dxftype() == "LINE"
                          and abs(l.dxf.start.y - l.dxf.end.y) < 1e-6})
def near(vals, t, tol=0.05): return any(abs(v - t) < tol for v in vals)

for name, v in ap.VERSIONS.items():
    d = f"out/acrylic/{name}/"; straight = v.get("guide") == "straight"
    print(f"== {name}" + ("  [as ordered]" if straight else ""))
    fr = d + "front_2T.dxf" if os.path.exists(d + "front_2T.dxf") else d + "front_3T.dxf"
    e = bbox.extents(ents(fr)).size
    chk(len(circles(fr)) == 4 and all(abs(c.dxf.radius*2 - ap.BOLT_CLEAR) < 1e-3 for c in circles(fr)),
        f"front: 4 x d{ap.BOLT_CLEAR}")
    chk(abs(e.x - ap.W) < 0.05 and abs(e.y - ap.H) < 0.05, f"front outline {e.x:.2f} x {e.y:.2f}")
    inner = [l for l in ents(fr) if l.dxftype() == "LINE" and abs(l.dxf.start.x) < ap.W/2 - 3
             and abs(l.dxf.start.y) < ap.H/2 - 3]
    xs = [p for l in inner for p in (l.dxf.start.x, l.dxf.end.x)]
    ys = [p for l in inner for p in (l.dxf.start.y, l.dxf.end.y)]
    chk(abs((max(xs)-min(xs)) - ap.WIN_W) < 0.05 and abs((max(ys)-min(ys)) - ap.WIN_H) < 0.05
        and abs((max(xs)+min(xs))/2 - ap.ACT_DX) < 0.05,
        f"window {max(xs)-min(xs):.2f} x {max(ys)-min(ys):.2f} at x{(max(xs)+min(xs))/2:+.2f}")
    for f in sorted(glob.glob(d + "L*_*.dxf")):
        chk(len(circles(f)) == 4, f"{os.path.basename(f)}: 4 bolt holes")
    g = glob.glob(d + "L1_gpocket_*.dxf")[0]
    chk(near([abs(x) for x in vx(g)], ap.GCAV_W/2), f"L1 glass pocket half-width {ap.GCAV_W/2:.2f}")
    if straight:
        for f in sorted(glob.glob(d + "L*_*.dxf")):
            chk(near([abs(x) for x in vx(f)], ap.W/2 - ap.GUIDE_D),
                f"{os.path.basename(f)}: groove floor |x| {ap.W/2-ap.GUIDE_D:.2f}")
            chk(near(hy(f), ap.SLOT_Y0), f"{os.path.basename(f)}: groove bottom y {ap.SLOT_Y0:+.2f}")
        l2 = glob.glob(d + "L2_guide_3T.dxf")[0]
        ri = ap.W/2 - ap.GUIDE_D - ap.WIRE_RECESS_D
        chk(near([abs(x) for x in vx(l2)], ri), f"L2 wire recess inner |x| {ri:.2f} (blind, {ap.WIRE_RECESS_D} deep)")
        chk(near(hy(l2), ap.SLOT_Y0 + ap.POCKET_H/2 - ap.WIRE_W/2)
            and near(hy(l2), ap.SLOT_Y0 + ap.POCKET_H/2 + ap.WIRE_W/2),
            f"L2 wire recess {ap.WIRE_W} tall at y{ap.SLOT_Y0+ap.POCKET_H/2:+.2f}")
        for f in sorted(glob.glob(d + "L[1345]_*.dxf")):
            chk(not near([abs(x) for x in vx(f)], ri), f"{os.path.basename(f)}: no wire recess")
        chk(not near([abs(x) for x in vx(fr)], ap.W/2 - ap.GUIDE_D), "front: no groove")
        print("  -- against the ordered REV4 drawing --")
        chk(abs(ap.W - REV4["outline"][0]) < 0.02 and abs(ap.H - REV4["outline"][1]) < 0.02, "outline")
        chk(abs(ap.BX - REV4["hole"][0]) < 0.02 and abs(ap.BY - REV4["hole"][1]) < 0.02
            and abs(ap.BOLT_CLEAR - REV4["hole"][2]) < 1e-6, "bolt pattern + diameter")
        chk(abs(ap.WIN_W - REV4["window"][0]) < 0.02 and abs(ap.WIN_H - REV4["window"][1]) < 0.02
            and abs(ap.ACT_DX - REV4["window"][2]) < 0.02, "front window size + offset")
        chk(abs(ap.GCAV_W/2 - REV4["glass_hw"]) < 0.02, "glass pocket")
        chk(abs(ap.FCAV_W - REV4["ledge"][0]) < 0.02 and abs(ap.FCAV_H - REV4["ledge"][1]) < 0.02
            and abs(ap.FRAME_DX - REV4["ledge"][2]) < 0.02, "ledge cavity + offset")
        chk(abs((ap.W/2 - ap.GUIDE_D) - REV4["groove_floor"]) < 0.02
            and abs(ap.SLOT_Y0 - REV4["groove_bottom"]) < 0.02, "groove floor + bottom")
        chk(abs(ri - REV4["recess_inner"]) < 0.02 and abs(ap.WIRE_W - REV4["recess_h"]) < 0.02
            and abs((ap.SLOT_Y0 + ap.POCKET_H/2) - REV4["recess_cy"]) < 0.02, "wire recess")
        chk([t for _, t in v["stack"]] == [2.0, 3.0, 2.0, 2.0, 2.0] and v["front_t"] == 2.0,
            "layer thicknesses 2/2/3/2/2/2 = 13.0 mm")
    else:
        pl = sorted(glob.glob(d + "L2_mouth_5T.dxf"))[0]
        chk(near(vx(pl), ap.FRAME_DX + ap.FCAV_W/2) and near(vx(pl), ap.FRAME_DX - ap.FCAV_W/2),
            f"L2 ledge cavity edges at {ap.FRAME_DX-ap.FCAV_W/2:+.2f} / {ap.FRAME_DX+ap.FCAV_W/2:+.2f}")
        chk(near([abs(x) for x in vx(pl)], ap.W/2 - ap.SLOT_D), f"L2 mouth floor {ap.W/2-ap.SLOT_D:.2f}")
        pk = glob.glob(d + "L4_pocket_*.dxf")[0]
        chk(near([abs(x) for x in vx(pk)], ap.W/2 - ap.LIP) and near([abs(x) for x in vx(pk)], ap.W/2 - ap.SLOT_D),
            "L4 pocket lip + floor")
    print("  sheets:", sorted(os.path.basename(x) for x in glob.glob(d + "sheet_*.dxf")))

for name, v in ap.VERSIONS.items():
    tag = name.split("_")[-1]
    d = f"out/acrylic/test_coupon_{tag}/"; fs = sorted(glob.glob(d + "C*_*.dxf"))
    chk(len(fs) == len(v["stack"]) and all(len(circles(f)) == 2 for f in fs),
        f"coupon {tag}: {len(fs)} pieces x 2 clamp holes")
    import re
    thick = lambda f: float(re.search(r"_([0-9.]+)T\.dxf$", f).group(1))
    kind = "guide" if v.get("guide") == "straight" else "mouth"
    m = max((f for f in fs if kind in os.path.basename(f)), key=thick)
    outer = max(vx(m))
    want = ap.GUIDE_D if v.get("guide") == "straight" else ap.SLOT_D
    chk(near([outer - x for x in vx(m)], want), f"coupon {tag} groove/mouth floor at outer-{want}")

print("ALL OK" if ok else "SOME CHECKS FAILED"); sys.exit(0 if ok else 1)
