import cadquery as cq
import math

# ---------------- Parameters ----------------
R_out = 60.0        # rim outer radius (OD 120)
R_in = 50.0         # rim inner radius
H = 40.0            # rim width (axial)
R_hub = 22.5        # hub OD 45
R_bore = 12.5       # shaft hole D25
key_w = 6.0
key_depth = 3.3
N_teeth = 47
helix_angle = 15.0
N_spokes = 5

# ---------------- Rim (with edge chamfers) ----------------
rim = (cq.Workplane("XY").circle(R_out).circle(R_in).extrude(H))
try:
    rim = rim.faces(">Z or <Z").edges(
        cq.selectors.RadiusNthSelector(1)).chamfer(1.5)
except Exception:
    try:
        rim = rim.edges("%CIRCLE").edges(
            cq.selectors.BoxSelector((-70, -70, -1), (70, 70, 41))
        ).chamfer(1.5)
    except Exception:
        pass

# ---------------- Hub ----------------
hub = cq.Workplane("XY").circle(R_hub).extrude(H)

# ---------------- Twisted elliptical spokes ----------------
x0, x1 = R_hub - 1.5, R_in + 1.5
plane = cq.Plane(origin=(x0, 0, H / 2), xDir=(0, 1, 0), normal=(1, 0, 0))
spoke = (cq.Workplane(plane).ellipse(3.0, 6.0)          # major axis axial
         .workplane(offset=x1 - x0).ellipse(6.0, 3.0)   # major axis circumferential
         .loft(ruled=False))

body = rim.union(hub)
for i in range(N_spokes):
    body = body.union(spoke.rotate((0, 0, 0), (0, 0, 1), i * 360.0 / N_spokes))

# ---------------- Root fillets ----------------
def root_edges(shape):
    sel = []
    for e in shape.Edges():
        c = e.Center()
        r = math.hypot(c.x, c.y)
        if (abs(r - R_hub) < 1.5 or abs(r - R_in) < 1.5) and 5 < c.z < H - 5:
            sel.append(e)
    return sel

solid = body.val()
for rf in (4.0, 3.0, 2.0):
    try:
        edges = root_edges(solid)
        if edges:
            f = solid.fillet(rf, edges)
            if f.isValid():
                solid = f
                break
    except Exception:
        pass
body = cq.Workplane("XY").add(solid)

# ---------------- HTD 8M helical tooth grooves ----------------
groove_r = 2.6
groove_depth = 3.4
gc = R_out - groove_depth + groove_r
twist = math.degrees(math.tan(math.radians(helix_angle)) * H / R_out)
groove = (cq.Workplane("XY").moveTo(gc, 0).circle(groove_r)
          .twistExtrude(H, twist)).val()
grooves = [groove.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1),
                         i * 360.0 / N_teeth) for i in range(N_teeth)]
body = body.cut(cq.Compound.makeCompound(grooves))

# ---------------- Shaft bore and keyway ----------------
bore = cq.Workplane("XY").circle(R_bore).extrude(H)
key = (cq.Workplane("XY").center((R_bore + key_depth) / 2.0, 0)
       .rect(R_bore + key_depth, key_w).extrude(H))
body = body.cut(bore.union(key))

result = body
