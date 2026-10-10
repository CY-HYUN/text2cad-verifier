import cadquery as cq
import math

# --- Parameters ---
ring_od, ring_id, ring_t = 60.0, 50.0, 4.0
top_d, top_t = 40.0, 4.0
H = 40.0                      # overall height
strut_r = 2.0
n_struts = 8
r_bot = 27.5                  # strut radius at bottom (ring mid-wall)
r_top = 16.5                  # strut radius at top plate
z_bot = ring_t / 2.0
z_top = H - top_t / 2.0
z_mid = (z_bot + z_top) / 2.0
r_mid = r_bot + (r_top - r_bot) * (z_mid - z_bot) / (z_top - z_bot)

# --- Bottom mounting ring ---
base = (cq.Workplane("XY").circle(ring_od / 2).circle(ring_id / 2).extrude(ring_t))

# Lugs with M4 holes
lug_r = 34.0
for i in range(4):
    a = math.radians(i * 90)
    cx, cy = lug_r * math.cos(a), lug_r * math.sin(a)
    lug = (cq.Workplane("XY")
           .transformed(rotate=(0, 0, i * 90))
           .center(lug_r - 4, 0).rect(10, 10).extrude(ring_t)
           .union(cq.Workplane("XY").center(cx, cy).circle(5).extrude(ring_t)))
    base = base.union(lug)
base = base.edges("|Z").fillet(0.8) if False else base

# --- Top motor plate ---
top = cq.Workplane("XY").workplane(offset=H - top_t).circle(top_d / 2).extrude(top_t)
try:
    top = top.edges().fillet(0.8)
except Exception:
    pass

frame = base.union(top)

# --- Inclined struts with joint blends ---
for i in range(n_struts):
    a = math.radians(i * 360.0 / n_struts + 22.5)
    p0 = cq.Vector(r_bot * math.cos(a), r_bot * math.sin(a), z_bot)
    p1 = cq.Vector(r_top * math.cos(a), r_top * math.sin(a), z_top)
    d = p1 - p0
    L = d.Length
    cyl = cq.Solid.makeCylinder(strut_r, L, p0, d.normalized())
    frame = frame.union(cq.Workplane("XY").add(cyl))
    # smooth blend nodes at joints
    pm = cq.Vector(r_mid * math.cos(a), r_mid * math.sin(a), z_mid)
    for p, rr in ((p0, 2.9), (p1, 2.9), (pm, 2.8)):
        frame = frame.union(cq.Workplane("XY").add(cq.Solid.makeSphere(rr, p)))

# --- Mid-height reinforcement ring ---
torus = cq.Solid.makeTorus(r_mid, 1.6, cq.Vector(0, 0, z_mid), cq.Vector(0, 0, 1))
frame = frame.union(cq.Workplane("XY").add(torus))

# --- Holes ---
# M4 lug holes
lug_holes = (cq.Workplane("XY").workplane(offset=-1)
             .pushPoints([(lug_r * math.cos(math.radians(i * 90)),
                           lug_r * math.sin(math.radians(i * 90))) for i in range(4)])
             .circle(2.15).extrude(ring_t + 2))
frame = frame.cut(lug_holes)

# Bearing hole + motor holes
top_holes = (cq.Workplane("XY").workplane(offset=H - top_t - 3)
             .circle(5.0).extrude(top_t + 6)
             .union(cq.Workplane("XY").workplane(offset=H - top_t - 3)
                    .pushPoints([(12 * math.cos(math.radians(45 + 90 * i)),
                                  12 * math.sin(math.radians(45 + 90 * i))) for i in range(4)])
                    .circle(1.5).extrude(top_t + 6)))
frame = frame.cut(top_holes)

# Trim anything below z=0 / above top
clip = cq.Workplane("XY").box(200, 200, H, centered=(True, True, False))
result = frame.intersect(clip)
