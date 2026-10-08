import cadquery as cq
import math

# ---------------- Parameters ----------------
R_out = 60.0          # rim outer radius (OD 120)
R_in = 50.0           # rim inner radius
W = 40.0              # rim width (axial)
R_hub = 22.5          # hub outer radius (OD 45)
R_bore = 12.5         # shaft hole radius (D 25)
key_w = 6.0
key_depth = 3.3
N_teeth = 47
helix_angle = 15.0
groove_r = 2.6        # HTD 8M arc tooth groove radius
groove_depth = 3.38   # HTD 8M groove depth

# ---------------- Rim and hub ----------------
rim = cq.Workplane("XY").circle(R_out).circle(R_in).extrude(W)
hub = cq.Workplane("XY").circle(R_hub).extrude(W)
body = rim.union(hub)

# ---------------- Twisted elliptical spokes ----------------
def section(r, rot):
    pl = cq.Plane(origin=(r, 0, W / 2), xDir=(0, 1, 0), normal=(1, 0, 0))
    return cq.Workplane(pl).ellipse(6.0, 3.0, rotation_angle=rot).val()

r0, r1 = R_hub - 2.0, R_in + 2.0
w_start = section(r0, 90)                 # major axis axial
w_mid = section((r0 + r1) / 2, 45)
w_end = section(r1, 0)                    # major axis circumferential
spoke = cq.Solid.makeLoft([w_start, w_mid, w_end], True)

for i in range(5):
    s = spoke.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), i * 72.0)
    body = body.union(cq.Workplane("XY").add(s))

# ---------------- Root fillets ----------------
def root_edges(wp):
    edges = []
    for e in wp.edges().vals():
        if e.geomType() in ("BSPLINE", "OTHER", "BEZIER"):
            c = e.Center()
            rr = math.hypot(c.x, c.y)
            if abs(rr - R_hub) < 3.0 or abs(rr - R_in) < 3.0:
                edges.append(e)
    return edges

for fr in (4.0, 3.0, 2.0):
    try:
        es = root_edges(body)
        if es:
            body = body.newObject(es).fillet(fr)
            body = cq.Workplane("XY").add(body.val())
        break
    except Exception:
        continue

# ---------------- Rim chamfers ----------------
try:
    body = body.edges(
        cq.selectors.BoxSelector((-R_out - 1, -R_out - 1, -0.1), (R_out + 1, R_out + 1, 0.1))
    ).edges("%CIRCLE").edges(cq.selectors.RadiusNthSelector(-1)).chamfer(1.5)
    body = body.edges(
        cq.selectors.BoxSelector((-R_out - 1, -R_out - 1, W - 0.1), (R_out + 1, R_out + 1, W + 0.1))
    ).edges("%CIRCLE").edges(cq.selectors.RadiusNthSelector(-1)).chamfer(1.5)
except Exception:
    pass

# ---------------- Helical HTD 8M teeth grooves ----------------
twist_deg = math.degrees(W * math.tan(math.radians(helix_angle)) / R_out)
gc = R_out + groove_r - groove_depth
cutter_one = (
    cq.Workplane("XY")
    .workplane(offset=-1)
    .center(gc, 0)
    .circle(groove_r)
    .twistExtrude(W + 2, twist_deg * (W + 2) / W)
)
cutter_solid = cutter_one.val()
cutters = None
for i in range(N_teeth):
    c = cutter_solid.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), i * 360.0 / N_teeth)
    cutters = c if cutters is None else cutters.fuse(c)
body = body.cut(cq.Workplane("XY").add(cutters))

# ---------------- Shaft bore with keyway ----------------
bore = cq.Workplane("XY").workplane(offset=-1).circle(R_bore).extrude(W + 2)
key = (
    cq.Workplane("XY").workplane(offset=-1)
    .center((R_bore + key_depth) / 2, 0)
    .rect(R_bore + key_depth, key_w)
    .extrude(W + 2)
)
body = body.cut(bore.union(key))

result = body
