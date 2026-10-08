import cadquery as cq
import math

# ---------------- Parameters ----------------
base_od = 60.0
base_id = 44.0
base_t = 5.0
lug_r_out = 38.0
lug_w = 12.0
m4_hole = 4.5
lug_hole_r = 33.0

top_z = 40.0
top_d = 40.0
top_t = 5.0
bearing_d = 10.0
motor_hole_d = 3.0
motor_hole_r = 12.0

n_pillars = 8
pillar_d = 5.0
r_bot = 26.0
r_top = 17.0

# ---------------- Base ring with lugs ----------------
base = cq.Workplane("XY").circle(base_od / 2).extrude(base_t)
for i in range(4):
    a = i * 90.0
    lug = (cq.Workplane("XY")
           .center((lug_r_out + base_id / 2) / 2 * 0 + (base_od / 2 + lug_r_out) / 2 - 4, 0)
           .rect(lug_r_out - base_od / 2 + 8 + 8, lug_w)
           .extrude(base_t)
           .union(cq.Workplane("XY").center(lug_hole_r, 0).circle(lug_w / 2).extrude(base_t))
           .rotate((0, 0, 0), (0, 0, 1), a))
    base = base.union(lug)
base = base.cut(cq.Workplane("XY").circle(base_id / 2).extrude(base_t))
holes = (cq.Workplane("XY")
         .polarArray(lug_hole_r, 0, 360, 4)
         .circle(m4_hole / 2).extrude(base_t))
base = base.cut(holes)

# ---------------- Top motor mount ----------------
top = (cq.Workplane("XY").workplane(offset=top_z)
       .circle(top_d / 2).extrude(top_t))
top = top.cut(cq.Workplane("XY").workplane(offset=top_z)
              .circle(bearing_d / 2).extrude(top_t))
top = top.cut(cq.Workplane("XY").workplane(offset=top_z)
              .polarArray(motor_hole_r, 45, 360, 4)
              .circle(motor_hole_d / 2).extrude(top_t))

# ---------------- Inclined pillars ----------------
z0 = base_t / 2
z1 = top_z + top_t / 2
result = base.union(top)
for i in range(n_pillars):
    a = math.radians(22.5 + i * 360.0 / n_pillars)
    p0 = cq.Vector(r_bot * math.cos(a), r_bot * math.sin(a), z0)
    p1 = cq.Vector(r_top * math.cos(a), r_top * math.sin(a), z1)
    d = p1 - p0
    cyl = cq.Solid.makeCylinder(pillar_d / 2, d.Length, p0, d.normalized())
    result = result.union(cq.Workplane("XY").add(cyl))

# ---------------- Mid reinforcing ring ----------------
z_mid = (base_t + top_z) / 2
t_frac = (z_mid - z0) / (z1 - z0)
r_mid = r_bot + (r_top - r_bot) * t_frac
ring_t = 4.0
ring = (cq.Workplane("XY").workplane(offset=z_mid - ring_t / 2)
        .circle(r_mid + 3.0).circle(r_mid - 3.0).extrude(ring_t))
result = result.union(ring)

# ---------------- Fillets at intersections ----------------
for rad in (1.5, 1.0, 0.6, 0.3):
    try:
        f = result.edges(cq.selectors.BoxSelector((-50, -50, base_t - 0.01),
                                                  (50, 50, top_z + 0.01)))
        f = f.filter(lambda e: e.geomType() in ("ELLIPSE", "BSPLINE", "OTHER")) \
            if hasattr(f, "filter") else f
        cand = f.fillet(rad)
        if cand.val().isValid():
            result = cand
            break
    except Exception:
        continue
