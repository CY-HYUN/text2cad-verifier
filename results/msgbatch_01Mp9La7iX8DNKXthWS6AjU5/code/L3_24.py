import cadquery as cq
import math

H = 40.0
R_out = 60.0
R_in = 55.0
R_hub = 22.5

# Rim with 1.5x45deg chamfers on both outer edges (revolved profile)
rim_pts = [(R_in, 0), (R_out - 1.5, 0), (R_out, 1.5), (R_out, H - 1.5),
           (R_out - 1.5, H), (R_in, H)]
rim = (cq.Workplane("XZ").polyline(rim_pts).close()
       .revolve(360, (0, 0, 0), (0, 1, 0)))

# Hub
hub = cq.Workplane("XY").circle(R_hub).extrude(H)

# Spokes: lofted ellipses, axial major axis at hub -> circumferential at rim
def make_spoke():
    w = (cq.Workplane("YZ").workplane(offset=R_hub - 2.5).center(0, H / 2)
         .ellipse(3, 6)
         .workplane(offset=(R_in + 2.0) - (R_hub - 2.5))
         .ellipse(6, 3)
         .loft(combine=True, ruled=False))
    return w

spoke0 = make_spoke()
body = rim.union(hub)
for i in range(5):
    body = body.union(spoke0.rotate((0, 0, 0), (0, 0, 1), i * 72))

# Fillet at spoke roots (best effort)
try:
    sol = body.val()
    sel = []
    for e in sol.Edges():
        if e.geomType() in ("LINE", "CIRCLE"):
            continue
        c = e.Center()
        r = math.hypot(c.x, c.y)
        if (abs(r - R_hub) < 2.0) or (abs(r - R_in) < 2.0):
            sel.append(e)
    if sel:
        filleted = sol.fillet(4.0, sel)
        if filleted.isValid():
            body = cq.Workplane("XY").newObject([filleted])
except Exception:
    pass

# Shaft hole and keyway
body = body.cut(cq.Workplane("XY").circle(12.5).extrude(H))
key = cq.Workplane("XY").center(0, 7.15).rect(6, 14.3).extrude(H)
body = body.cut(key)

# Helical HTD-8M-like grooves: 47 teeth, 15 deg helix over 40 mm
twist = math.degrees(H * math.tan(math.radians(15)) / R_out)
groove = (cq.Workplane("XY").pushPoints([(R_out, 0)]).circle(2.8)
          .twistExtrude(H, twist))
grooves = []
for i in range(47):
    g = groove.rotate((0, 0, 0), (0, 0, 1), i * 360.0 / 47)
    grooves.append(g.val())
groove_comp = cq.Compound.makeCompound(grooves)
body = body.cut(cq.Workplane("XY").newObject([groove_comp]))

result = body
