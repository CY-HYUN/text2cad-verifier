import cadquery as cq
import math

H = 40.0
R_out = 60.0
R_in = 50.0
R_hub = 22.5

# Rim with 1.5 x 45 deg chamfers on both ends
rim = (cq.Workplane("XY").circle(R_out).circle(R_in).extrude(H))
rim = rim.edges("%CIRCLE").chamfer(1.5)

# Hub
hub = cq.Workplane("XY").circle(R_hub).extrude(H)

# Spokes: elliptical loft with 90 deg twist
def make_spoke():
    pl = cq.Plane(origin=(R_hub - 1.5, 0, H / 2), xDir=(0, 0, 1), normal=(1, 0, 0))
    s = (cq.Workplane(pl).ellipse(6, 3)
         .workplane(offset=(R_in + 1.5) - (R_hub - 1.5))
         .transformed(rotate=(0, 0, 90))
         .ellipse(6, 3)
         .loft(combine=True))
    return s.val()

spoke0 = make_spoke()
body = rim.union(hub)
for i in range(5):
    sp = spoke0.rotate((0, 0, 0), (0, 0, 1), i * 72.0)
    body = body.union(cq.Workplane("XY").add(sp))

# Fillet at spoke roots (hub and rim junctions)
def is_root_edge(e):
    try:
        pts = [e.positionAt(t) for t in (0.0, 0.5, 1.0)]
    except Exception:
        return False
    for target in (R_hub, R_in):
        if all(abs(math.hypot(p.x, p.y) - target) < 0.2 for p in pts):
            if 1.0 < pts[1].z < H - 1.0:
                return True
    return False

try:
    root_edges = [e for e in body.edges().vals() if is_root_edge(e)]
    filleted = body.newObject(root_edges).fillet(4.0)
    if filleted.val().isValid():
        body = filleted
except Exception:
    pass

# Helical teeth grooves (HTD 8M style arc profile, 15 deg helix at pitch radius)
twist = math.degrees(H * math.tan(math.radians(15.0)) / R_out)
groove_r = 2.6
groove_cx = R_out - 3.4 + groove_r
groove0 = (cq.Workplane("XY").pushPoints([(groove_cx, 0)]).circle(groove_r)
           .twistExtrude(H, twist)).val()
N = 47
grooves = [groove0.rotate((0, 0, 0), (0, 0, 1), i * 360.0 / N) for i in range(N)]
groove_comp = cq.Compound.makeCompound(grooves)
body = body.cut(cq.Workplane("XY").add(groove_comp))

# Shaft hole 25 mm with 6 mm keyway
bore = cq.Workplane("XY").circle(12.5).extrude(H)
key = cq.Workplane("XY").box(15.3, 6, H, centered=(False, True, False))
body = body.cut(bore).cut(key)

result = body
