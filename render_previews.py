"""Preview renders (VTK offscreen) + a 2-D slot section.   python3 render_previews.py

Display, frame and connector blocks follow the official 5" STEP
(reference/td2_5in.step). The Raspberry Pi 5 is drawn mounted DIRECTLY on four
corner stand-offs on the display rear, per Raspberry Pi's documentation ("you can
mount any SBC form-factor Raspberry Pi directly to the back of the Touch Display 2",
four supplied M2.5 screws). The STEP does not model those stand-offs, so their exact
coordinates and height are nominal here — the Pi's 58 x 49 pattern is drawn centred
on the display's rear frame. Treat the stand-off placement as illustration.
"""
import os, math, tempfile
import cadquery as cq, vtk
import acrylic_panels as ap

TMP = tempfile.mkdtemp(prefix="pi5case_")
CLEAR = (0.86, 0.93, 0.98)

def stl(solid, name):
    p = os.path.join(TMP, name + ".stl"); cq.exporters.export(solid, p, tolerance=0.08, angularTolerance=0.2); return p

def actor(path, color, opacity=1.0, spec=0.5, power=40, edges=False):
    r = vtk.vtkSTLReader(); r.SetFileName(path); r.Update()
    m = vtk.vtkPolyDataMapper(); m.SetInputConnection(r.GetOutputPort())
    a = vtk.vtkActor(); a.SetMapper(m); p = a.GetProperty()
    p.SetColor(*color); p.SetOpacity(opacity); p.SetSpecular(spec); p.SetSpecularPower(power)
    p.SetInterpolationToPhong(); p.SetAmbient(0.3)
    if edges: p.EdgeVisibilityOn(); p.SetEdgeColor(0.45, 0.6, 0.75); p.SetLineWidth(1.0)
    return a

def scene(actors, fname, pos, focal, up=(0, 1, 0), zoom=1.0):
    ren = vtk.vtkRenderer()
    for a in actors: ren.AddActor(a)
    ren.SetBackground(0.97, 0.97, 0.98); ren.SetBackground2(0.84, 0.86, 0.90); ren.GradientBackgroundOn()
    ren.SetUseDepthPeeling(1); ren.SetMaximumNumberOfPeels(60); ren.SetOcclusionRatio(0.05)
    hl = vtk.vtkLight(); hl.SetLightTypeToHeadlight(); hl.SetIntensity(0.75); ren.AddLight(hl)
    for lp in ((1, 1, 1), (-1, 0.6, 1), (0.5, -1, -0.5)):
        l = vtk.vtkLight(); l.SetPosition(*[c*1000 for c in lp]); l.SetFocalPoint(0, 0, 0); l.SetIntensity(0.35); ren.AddLight(l)
    rw = vtk.vtkRenderWindow(); rw.SetOffScreenRendering(1); rw.SetAlphaBitPlanes(1); rw.SetMultiSamples(0)
    rw.AddRenderer(ren); rw.SetSize(1400, 950)
    ren.ResetCamera()
    c = ren.GetActiveCamera(); c.SetFocalPoint(*focal); c.SetPosition(*pos); c.SetViewUp(*up); c.Zoom(zoom)
    ren.ResetCameraClippingRange()
    rw.Render(); w = vtk.vtkWindowToImageFilter(); w.SetInput(rw); w.Update()
    wr = vtk.vtkPNGWriter(); wr.SetFileName(fname); wr.SetInputConnection(w.GetOutputPort()); wr.Write(); print("saved", fname)

def hex_prism(af, h):
    return cq.Workplane("XY").polygon(6, af / math.cos(math.radians(30))).extrude(h)

def build_scene(v, gap=0.0):
    parts = ap.build_case(v); acr, oth = [], []
    z = 0.0
    for label, t, solid in parts:
        acr.append(actor(stl(solid.faces("<Z").wires().toPending().extrude(t).translate((0, 0, z)), label), CLEAR, 0.38, edges=True))
        z += t + gap
    z_rear = z - gap
    ft = v["front_t"]; zg = ft + (gap if gap else 0.01)           # glass sits right behind the front plate
    glass = cq.Workplane("XY").rect(ap.GLASS_W, ap.GLASS_H).extrude(ap.GLASS_T).edges("|Z").fillet(ap.GLASS_R).translate((0, 0, zg))
    oth.append(actor(stl(glass, "glass"), (0.05, 0.05, 0.07), 1.0, 0.9, 80))
    frame = (cq.Workplane("XY").center(ap.FRAME_DX, ap.FRAME_DY).rect(ap.FRAME_W, ap.FRAME_H).extrude(ap.FRAME_BEHIND_GLASS)
             .edges("|Z").fillet(2.0).translate((0, 0, zg + ap.GLASS_T)))
    oth.append(actor(stl(frame, "frame"), (0.12, 0.12, 0.14), 1.0, 0.4, 30))
    zpost = zg + ap.STEP_BODY_D                                   # rear plane of the glass/frame body
    # connector blocks from the STEP (landscape X = portrait Y - glass offset)
    ffc = cq.Workplane("XY").center(37.37 - 2.47, 0.03).rect(8.9, 21.0).extrude(2.7).translate((0, 0, zpost - 2.7 - 1.68))
    oth.append(actor(stl(ffc, "ffc"), (0.95, 0.75, 0.35), 1.0, 0.2, 10))
    j1 = cq.Workplane("XY").center(-30.19 - 2.47, 4.13).rect(5.2, 16.4).extrude(2.0).translate((0, 0, zpost - 2.0 - 3.0))
    oth.append(actor(stl(j1, "j1"), (0.85, 0.2, 0.2), 1.0, 0.3, 20))
    # Pi 5 mounted DIRECTLY on the display's four corner stand-offs (official method).
    # Stand-off coordinates are not published; drawn centred on the rear frame.
    zso = zpost + (gap*2 if gap else 0)
    zpi = zso + ap.STANDOFF_H
    for dx in (-ap.PI_HOLE_DX/2, ap.PI_HOLE_DX/2):
        for dy in (-ap.PI_HOLE_DY/2, ap.PI_HOLE_DY/2):
            px, py = ap.PI_OFF_X + dx, ap.PI_OFF_Y + dy
            so = cq.Workplane("XY").center(px, py).circle(2.6).circle(1.3).extrude(ap.STANDOFF_H).translate((0, 0, zso))
            oth.append(actor(stl(so, f"so{dx:.0f}{dy:.0f}"), (0.30, 0.31, 0.34), 1.0, 0.5, 40))
            sc = cq.Workplane("XY").center(px, py).circle(2.3).extrude(1.3).translate((0, 0, zpi + 1.6))
            oth.append(actor(stl(sc, f"sc{dx:.0f}{dy:.0f}"), (0.82, 0.83, 0.86), 1.0, 0.9, 90))
    pi = (cq.Workplane("XY").center(ap.PI_OFF_X, ap.PI_OFF_Y).rect(ap.PI_W, ap.PI_H).extrude(1.6)
          .edges("|Z").fillet(3).translate((0, 0, zpi)))
    oth.append(actor(stl(pi, "pi"), (0.16, 0.42, 0.28), 1.0, 0.3, 20))
    cooler = cq.Workplane("XY").center(ap.PI_OFF_X - 8, ap.PI_OFF_Y + 3).rect(52, 40).extrude(15).translate((0, 0, zpi + 1.6))
    oth.append(actor(stl(cooler, "cooler"), (0.35, 0.36, 0.40), 1.0, 0.5, 40))
    ports = cq.Workplane("XY").center(ap.PI_OFF_X + ap.PI_W/2 - 9, ap.PI_OFF_Y).rect(18, 50).extrude(16).translate((0, 0, zpi + 1.6))
    oth.append(actor(stl(ports, "ports"), (0.70, 0.72, 0.75), 1.0, 0.6, 50))
    # bolts: button head front, shank, washer + nut on the rear face
    m = ap.validate(v); L = m["bolt_rec"]
    for (bx, by) in ap.bolt_pts():
        for s_, n in ((cq.Workplane("XY").center(bx, by).circle(2.3).extrude(1.4).translate((0, 0, -1.4)), "h"),
                      (cq.Workplane("XY").center(bx, by).circle(1.25).extrude(L), "s"),
                      (cq.Workplane("XY").center(bx, by).circle(3.0).circle(1.4).extrude(ap.WASHER_T).translate((0, 0, z_rear)), "w"),
                      (hex_prism(5.0, ap.NUT_T).translate((bx, by, z_rear + ap.WASHER_T)), "n")):
            oth.append(actor(stl(s_, f"b{n}{bx:.0f}{by:.0f}"), (0.82, 0.83, 0.86), 1.0, 0.9, 90))
    return acr, oth, z_rear

def slot_diagram(v, fname):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    layers = [("front", v["front_t"], "front")] + [(f"L{i} {r}", t, r) for i, (r, t) in enumerate(v["stack"], 1)]
    WALL, LIP, CAV, SLOT = ap.SIDE_WALL, ap.LIP, ap.CAV_D, ap.SLOT_D
    fig, ax = plt.subplots(figsize=(9.5, 6.2)); z = 0.0; acr = "#cfe3f2"; edge = "#5b7fa6"
    for name, t, role in layers:
        if role == "front": ax.add_patch(Rectangle((-3, z), WALL+3, t, fc=acr, ec=edge, lw=0.9))
        elif role == "mouth": ax.add_patch(Rectangle((0, z), WALL-SLOT, t, fc=acr, ec=edge, lw=0.9))
        elif role in ("pocket", "gpocket"):
            ax.add_patch(Rectangle((0, z), WALL-SLOT, t, fc=acr, ec=edge, lw=0.9)); ax.add_patch(Rectangle((WALL-LIP, z), LIP, t, fc=acr, ec=edge, lw=0.9))
        else: ax.add_patch(Rectangle((0, z), WALL, t, fc=acr, ec=edge, lw=0.9))
        ax.text(-3.6, z+t/2, f"{name}  {t:g}T", ha="right", va="center", fontsize=9, color="#333"); z += t
    st = v["stack"]; pt = st[0][1]
    zm0 = v["front_t"] + pt; zm1 = zm0 + 7.0; zc0 = zm0 - pt; zc1 = zm1 + pt; xo = WALL
    ax.add_patch(Rectangle((xo+0.05, zc0-2), 4.0, (zc1-zc0)+4, fc="#c9ccd3", ec="#444", lw=0.8))
    ax.add_patch(Rectangle((xo-SLOT, zc0+0.05), CAV-0.05, (zc1-zc0)-0.1, fc="#8a8f99", ec="#444", lw=0.8))
    ax.add_patch(Rectangle((xo-LIP, zm0+0.05), LIP+0.05, 7.0-0.1, fc="#8a8f99", ec="#444", lw=0.8))
    ax.text(xo+2.05, (zc0+zc1)/2, "Joy-Con rail", ha="center", va="center", fontsize=9, rotation=90, color="#222")
    def dim(x0, x1, y, txt, dy=0.35):
        ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", lw=0.9, color="#c0392b")); ax.text((x0+x1)/2, y+dy, txt, ha="center", fontsize=8.5, color="#c0392b")
    def vdim(x, y0, y1, txt, dx=0.3, ha="left"):
        ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", lw=0.9, color="#1f6fb2")); ax.text(x+dx, (y0+y1)/2, txt, va="center", ha=ha, fontsize=8.5, color="#1f6fb2")
    inner = 7.0 + 2*pt
    vdim(xo-SLOT-0.6, zm0, zm1, "mouth 7.0\n(5T+2T)")
    vdim(xo-SLOT-2.9, zc0, zc1, f"inner {inner:.1f}\n(+{pt:g}T x2)" + (f"\nliners -> {inner-2*v['shim']:.2f}" if v["shim"] else ""), dx=-0.3, ha="right")
    dim(xo-SLOT, xo-LIP, z+0.9, f"cavity {CAV}"); dim(xo-LIP, xo, z+2.3, f"lip {LIP}"); dim(xo-SLOT, xo, z+3.7, f"slot {SLOT} from face")
    ax.text(WALL/2-1.5, -1.6, f"<- glass pocket / ledge        side wall {WALL:g} mm        outer face ->", ha="center", fontsize=8.5, color="#555")
    ax.set_xlim(-14, WALL+5.5); ax.set_ylim(-2.4, z+5.0); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Joy-Con T-slot section at the side wall (reference: Cuttlephone 7.1 / 10.1 / 2.4) - clear acrylic", fontsize=10.5)
    fig.tight_layout(); fig.savefig(fname, dpi=150); plt.close(fig); print("saved", fname)

def main():
    for name, v in ap.VERSIONS.items():
        d = f"out/acrylic/{name}/"
        acr, oth, zr = build_scene(v)
        scene(acr + oth, d + "preview_front.png", pos=(-150, -90, -330), focal=(0, 0, 6), zoom=1.0)
        scene(acr + oth, d + "preview_back.png",  pos=(-180, 130, 330),  focal=(0, 0, 10), zoom=1.0)
        scene(acr + oth, d + "preview_ledge.png", pos=(-ap.BX-26, ap.BY+40, 80), focal=(-ap.BX+10, ap.BY-12, 8), zoom=1.0)
        acr_e, oth_e, _ = build_scene(v, gap=12.0)
        scene(acr_e + oth_e, d + "preview_exploded.png", pos=(-330, -250, -420), focal=(0, 0, 55), zoom=1.0)
        slot_diagram(v, d + "preview_slot.png")
    for name, v in ap.VERSIONS.items():
        d = f"out/acrylic/test_coupon_{name.split('_')[-1]}/"
        parts = ap.build_coupon(v); z = 0.0; acts = []
        for label, t, solid in parts:
            acts.append(actor(stl(solid.faces("<Z").wires().toPending().extrude(t).translate((0, 0, z)), "c"+label), CLEAR, 0.42, edges=True)); z += t + 8.0
        scene(acts, d + "preview_exploded.png", pos=(ap.W/2 - 70, ap.H/2 - 100, -110), focal=(ap.W/2 - 8, ap.H/2 - 20, z/2), zoom=1.0)

if __name__ == "__main__":
    main()
