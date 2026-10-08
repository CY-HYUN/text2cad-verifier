import cadquery as cq
import math

# ---------------- Parameters ----------------
base_od = 60.0
base_id = 44.0
base_t = 5.0
lug_r = 34.0          # bolt circle radius for lugs
lug_w = 10.0
m4_hole = 4.5

top_z = 40.0          # offset plane height
top_d = 40.0
top_t = 5.0
bearing_d = 10.0
motor_hole_d = 3.0
motor_hole_r = 12.0

n_pillars = 8
pillar_d = 5.0
r_bot = 26.0          # pillar centre radius on base
r_top = 16.5          # pillar centre radius on top mount

# ---------------- Base ring with lugs ----------------
base = cq.Workplane("XY").circle(base_od / 2).extrude(base_t)
for i in range(4):
    a = i * 90.0
    lug = (cq.Workplane("XY")
           .center(lug_r / 2 * math.cos(math.radians(a)), lug_r / 2 * math.sin(math.radians(a)))
           .rect(lug_r, lug_w).extrude(base_t)
           .rotate((0, 0, 0), (0, 0, 1), 0))
    # rect is axis aligned; build rotated lug instead
    lug = (cq.Workplane("XY").center(lug_r / 2, 0).rect(lug_r, lug_w).extrude(base_t)
           .union(cq.Workplane("XY").center(lug_r, 0).circle(lug_w / 2).extrude(base_t))
           .rotate((0, 0, 0), (0, 0, 1), a))
    base = base.union(lug)
base = base.cut(cq.Workplane("XY").circle(base_id / 2).extrude(base_t))
for i in range(4):
    a = math.radians(i * 90.0)
    base = base.cut(cq.Workplane("XY")
                    .center(lug_r * math.cos(a), lug_r * math.sin(a))
                    .circle(m4_hole / 2).extrude(base_t))

# ---------------- Top motor mount ----------------
top = (cq.Workplane("XY", origin=(0, 0, top_z))
       .circle(top_d / 2).extrude(top_t))
top = top.cut(cq.Workplane("XY", origin=(0, 0, top_z)).circle(bearing_d / 2).extrude(top_t))
for i in range(4):
    a = math.radians(45 + i * 90.0)
    top = top.cut(cq.Workplane("XY", origin=(0, 0, top_z))
                  .center(motor_hole_r * math.cos(a), motor_hole_r * math.sin(a))
                  .circle(motor_hole_d / 2).extrude(top_t))

result = base.union(top)

# ---------------- Inclined pillars ----------------
z0 = base_t / 2.0
z1 = top_z + top_t / 2.0
for i in range(n_pillars):
    a = math.radians(22.5 + i * 360.0 / n_pillars)
    p0 = cq.Vector(r_bot * math.cos(a), r_bot * math.sin(a), z0)
    p1 = cq.Vector(r_top * math.cos(a), r_top * math.sin(a), z1)
    d = p1 - p0
    L = d.Length
    u = d.normalized()
    cyl = cq.Solid.makeCylinder(pillar_d / 2, L, p0, u)
    result = result.union(cq.Workplane("XY").add(cyl))

# ---------------- Mid reinforcing ring ----------------
z_mid = (z0 + z1) / 2.0
r_mid = (r_bot + r_top) / 2.0
ring_t = 4.0
ring_w = 7.0
ring = (cq.Workplane("XY", origin=(0, 0, z_mid - ring_t / 2))
        .circle(r_mid + ring_w / 2).circle(r_mid - ring_w / 2).extrude(ring_t))
result = result.union(ring)

# ---------------- Fillets at intersections ----------------
def try_fillet(wp, r):
    try:
        sel = [e for e in wp.edges().vals() if e.geomType() not in ("LINE", "CIRCLE")]
        if not sel:
            return wp
        out = wp.newObject(sel).fillet(r)
        if out.val().isValid():
            return out
    except Exception:
        pass
    return None

for r in (1.5, 1.0, 0.6):
    f = try_fillet(result, r)
    if f is not None:
        result = f
        break
