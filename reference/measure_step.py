"""Re-measure the official 5" Touch Display 2 STEP.   python3 reference/measure_step.py

Prints the numbers that acrylic_panels.py hard-codes, so they can be checked
against a freshly downloaded model.
"""
import collections, os, sys
import cadquery as cq

STEP = os.path.join(os.path.dirname(__file__), "td2_5in.step")
if not os.path.exists(STEP):
    sys.exit("download td2_5in.step first — see reference/README.md")

solids = cq.importers.importStep(STEP).solids().vals()
rows = sorted(((s.Volume(), s.BoundingBox()) for s in solids), key=lambda r: -r[0])
print(f"{len(solids)} solids")
for vol, b in rows:
    print(f"  vol={vol:8.0f}  {b.xlen:7.2f} x {b.ylen:7.2f} x {b.zlen:5.2f}  centre ({b.center.x:6.2f},{b.center.y:6.2f})  z[{b.zmin:6.2f},{b.zmax:6.2f}]")

glass = next(b for v, b in rows if abs(b.zlen - 0.70) < 0.05 and b.xlen > 90)
frame = next(b for v, b in rows if abs(b.zlen - 7.00) < 0.05)
panel = rows[0][1]
rear = min(b.zmin for _, b in rows)
print(f"\nglass  {glass.xlen:.2f} x {glass.ylen:.2f} x {glass.zlen:.2f}  centre ({glass.center.x:.2f},{glass.center.y:.2f})")
print(f"frame  {frame.xlen:.2f} x {frame.ylen:.2f}  centre offset vs glass: {frame.center.y - glass.center.y:+.2f}")
print(f"panel  centre offset vs glass: {panel.center.y - glass.center.y:+.2f}")
print(f"depth  glass front {glass.zmax:.2f} -> rearmost {rear:.2f} = {glass.zmax - rear:.2f}")
gs = next(s for s in solids if abs(s.BoundingBox().zlen - 0.70) < 0.05 and s.BoundingBox().xlen > 90)
print("glass corner radii:", dict(collections.Counter(round(e.radius(), 2) for e in gs.Edges() if e.geomType() == "CIRCLE")))

posts = set()
for s in solids:
    for f in s.Faces():
        if f.geomType() != "CYLINDER":
            continue
        try:
            cyl = f._geomAdaptor().Cylinder()
            fb = f.BoundingBox()
            if 1.2 <= cyl.Radius() <= 2.0 and abs(cyl.Axis().Direction().Z()) > 0.99 and fb.zmin < rear + 0.1:
                posts.add((round(cyl.Axis().Location().X(), 2), round(cyl.Axis().Location().Y(), 2)))
        except Exception:
            pass
xs = sorted({p[0] for p in posts}); ys = sorted({p[1] for p in posts})
print(f"rear M2.5 points: {sorted(posts)}")
if len(xs) == 2 and len(ys) == 2:
    print(f"  pitch {xs[1]-xs[0]:.2f} x {ys[1]-ys[0]:.2f}   (Raspberry Pi 5 pattern is 58 x 49)")
