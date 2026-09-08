"""Cross-check the exported DXFs against acrylic_panels.py.  python3 verify_dxf.py"""
import ezdxf, glob, os, sys
from ezdxf import bbox
import acrylic_panels as ap
ok = True
def chk(c, msg):
    global ok; print(("  OK   " if c else "  FAIL ") + msg); ok = ok and c
def ents(f): return list(ezdxf.readfile(f).modelspace())
def circles(f): return [e for e in ents(f) if e.dxftype() == "CIRCLE"]
def vlines_x(f, positive=True):
    return sorted({round(l.dxf.start.x, 3) for l in ents(f) if l.dxftype() == "LINE"
                   and abs(l.dxf.start.x - l.dxf.end.x) < 1e-6 and (l.dxf.start.x > 0 or not positive)})
for name in ap.VERSIONS:
    d = f"out/acrylic/{name}/"; print(f"== {name}")
    fr = d + "front_2T.dxf"; e = bbox.extents(ents(fr)).size
    chk(len(circles(fr)) == 4 and all(abs(c.dxf.radius*2 - ap.BOLT_CLEAR) < 1e-3 for c in circles(fr)), f"front: 4 x d{ap.BOLT_CLEAR}")
    chk(abs(e.x - ap.W) < 0.05 and abs(e.y - ap.H) < 0.05, f"front outline {e.x:.2f} x {e.y:.2f} == {ap.W:.2f} x {ap.H:.2f}")
    inner = [l for l in ents(fr) if l.dxftype() == "LINE" and abs(l.dxf.start.x) < ap.W/2 - 3 and abs(l.dxf.start.y) < ap.H/2 - 3]
    xs = [p for l in inner for p in (l.dxf.start.x, l.dxf.end.x)]; ys = [p for l in inner for p in (l.dxf.start.y, l.dxf.end.y)]
    chk(abs((max(xs)-min(xs)) - ap.WIN_W) < 0.05 and abs((max(ys)-min(ys)) - ap.WIN_H) < 0.05, f"window {max(xs)-min(xs):.2f} x {max(ys)-min(ys):.2f}")
    chk(abs((max(xs)+min(xs))/2 - ap.ACT_DX) < 0.05, f"window centre x = {(max(xs)+min(xs))/2:+.2f} (ACT_DX {ap.ACT_DX:+.2f})")
    for f in sorted(glob.glob(d + "L*_*.dxf")):
        chk(len(circles(f)) == 4, f"{os.path.basename(f)}: 4 bolt holes")
    g = glob.glob(d + "L1_gpocket_*.dxf")[0]; xs = vlines_x(g)
    chk(any(abs(x - ap.GCAV_W/2) < 0.05 for x in xs), f"L1 glass pocket half-width {ap.GCAV_W/2:.2f}")
    pl = sorted(glob.glob(d + "L2_mouth_5T.dxf"))[0]; xs = vlines_x(pl, positive=False)
    chk(any(abs(x - (ap.FRAME_DX + ap.FCAV_W/2)) < 0.05 for x in xs) and any(abs(x - (ap.FRAME_DX - ap.FCAV_W/2)) < 0.05 for x in xs),
        f"L2 ledge cavity edges at {ap.FRAME_DX - ap.FCAV_W/2:+.2f} / {ap.FRAME_DX + ap.FCAV_W/2:+.2f}")
    chk(any(abs(x - (ap.W/2 - ap.SLOT_D)) < 0.05 for x in vlines_x(pl)), f"L2 mouth floor at {ap.W/2 - ap.SLOT_D:.2f}")
    pk = glob.glob(d + "L4_pocket_*.dxf")[0]; xs = vlines_x(pk)
    chk(any(abs(x - (ap.W/2 - ap.LIP)) < 0.05 for x in xs) and any(abs(x - (ap.W/2 - ap.SLOT_D)) < 0.05 for x in xs), "L4 pocket lip + floor")
    print("  sheets:", sorted(os.path.basename(x) for x in glob.glob(d + "sheet_*.dxf")))
for name in ap.VERSIONS:
    d = f"out/acrylic/test_coupon_{name.split('_')[-1]}/"; fs = sorted(glob.glob(d + "C*_*.dxf"))
    chk(len(fs) == len(ap.VERSIONS[name]["stack"]) and all(len(circles(f)) == 2 for f in fs), f"coupon {name}: {len(fs)} pieces x 2 clamp holes")
    m = [f for f in fs if "mouth_5T" in f][0]; xs = vlines_x(m, positive=False); outer = max(xs)
    chk(any(abs((outer - x) - ap.SLOT_D) < 0.06 for x in xs), f"coupon mouth floor at outer-{ap.SLOT_D}")
print("ALL OK" if ok else "SOME CHECKS FAILED"); sys.exit(0 if ok else 1)
