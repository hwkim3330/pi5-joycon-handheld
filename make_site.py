"""Build the GitHub Pages assembly viewer into docs/.   python3 make_site.py

Exports each plate of the fabricated v8 build as flat polygons (outer boundary + holes)
so the page can extrude them in the browser - no STL, no loader, no CDN model files.
"""
import json, os
import cadquery as cq
import acrylic_panels as ap

TOL = 1e-4

def _sample(edge, per_mm=0.6, lo=2, hi=64):
    n = max(lo, min(hi, int(edge.Length() * per_mm) + 2))
    return [edge.positionAt(i / n) for i in range(n + 1)]

def wire_polygon(wire):
    """Stitch a wire's edges into one ordered closed polygon."""
    chains = [_sample(e) for e in wire.Edges()]
    if not chains:
        return []
    out = chains.pop(0)
    while chains:
        tail = out[-1]
        best, rev, d = None, False, 1e9
        for i, c in enumerate(chains):
            for r, end in ((False, c[0]), (True, c[-1])):
                dd = (end - tail).Length
                if dd < d:
                    best, rev, d = i, r, dd
        c = chains.pop(best)
        if rev:
            c = c[::-1]
        out.extend(c[1:])
    return [(round(p.x, 3), round(p.y, 3)) for p in out]

def plate_shape(solid):
    face = solid.faces("<Z").val()
    return dict(outer=wire_polygon(face.outerWire()),
                holes=[wire_polygon(w) for w in face.innerWires()])

# how to tell each plate apart in the hand
INFO = {
    "front": ("Front plate", "2T",
              "One big window and <b>no grooves</b> on the side edges. The only plate whose "
              "sides are perfectly straight.",
              ["window 112.0 x 63.5", "no side groove", "4 x d2.8"]),
    "L1":    ("L1 - glass pocket", "2T",
              "A <b>large</b> opening, almost the full width of the plate. This is the pocket "
              "the display glass drops into. Side grooves present.",
              ["pocket 144.4 x 92.46", "side groove 3.4 deep", "widest opening of all plates"]),
    "L2":    ("L2 - wire recess", "3T",
              "The <b>only 3 mm plate</b>. Smaller opening, and inside each side groove there "
              "is a small extra notch. If you can only find one thick plate, this is it.",
              ["3 mm thick - unique", "cavity 126.24 x 74.46", "3.2 x 6.8 notch in each groove"]),
    "L3":    ("L3", "2T", "Smaller opening, plain side grooves, no notch. <b>L3, L4 and L5 are "
              "the same part</b> - their order does not matter.", ["cavity 126.24 x 74.46", "plain groove"]),
    "L4":    ("L4", "2T", "Identical to L3 and L5.", ["cavity 126.24 x 74.46", "plain groove"]),
    "L5":    ("L5", "2T", "Identical to L3 and L4. Sits at the very back; the washers and nuts "
              "land on it.", ["cavity 126.24 x 74.46", "plain groove"]),
}
COLORS = ["#5aa9e6", "#7fd1b9", "#f7b267", "#f4845f", "#b39ddb", "#90be6d"]

def main():
    v = ap.VERSIONS["v8_clear_straightguide_ordered"]
    parts = ap.build_case(v)
    plates, z = [], 0.0
    for i, (label, t, solid) in enumerate(parts):
        key = label.split("_")[0]
        title, thick, how, bullets = INFO[key]
        sh = plate_shape(solid)
        plates.append(dict(id=key, title=title, thickness=t, z=z, color=COLORS[i % len(COLORS)],
                           how=how, bullets=bullets, **sh))
        z += t
    data = dict(
        plates=plates, total=z, W=ap.W, H=ap.H,
        display=dict(w=ap.GLASS_W, h=ap.GLASS_H, d=ap.GLASS_T, z=v["front_t"],
                     frame_w=ap.FRAME_W, frame_h=ap.FRAME_H, frame_dx=ap.FRAME_DX,
                     frame_d=ap.FRAME_BEHIND_GLASS),
        pi=dict(w=ap.PI_W, h=ap.PI_H, dx=ap.PI_OFF_X, dy=ap.PI_OFF_Y, standoff=ap.STANDOFF_H),
        guide=dict(depth=ap.GUIDE_D, channel=sum(t for _, t in v["stack"]),
                   length=ap.JC_RAIL, bay=ap.POCKET_H, mouth_target=ap.MOUTH_TARGET,
                   head=ap.INNER_TARGET, overhang=round((sum(t for _, t in v["stack"]) - ap.MOUTH_TARGET)/2, 1)),
        bolt=dict(x=ap.BX, y=ap.BY, d=ap.BOLT_CLEAR, length=ap.validate(v)["bolt_rec"]),
    )
    os.makedirs("docs", exist_ok=True)
    with open("docs/plates.json", "w") as f:
        json.dump(data, f, separators=(",", ":"))
    n = sum(len(p["outer"]) + sum(len(h) for h in p["holes"]) for p in plates)
    print(f"docs/plates.json: {len(plates)} plates, {n} points, "
          f"{os.path.getsize('docs/plates.json')/1024:.0f} kB")

if __name__ == "__main__":
    main()
