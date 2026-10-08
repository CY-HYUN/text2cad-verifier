import cadquery as cq
import math

# ---------------- Parameters ----------------
base_od = 60.0
base_id = 44.0
base_t = 5.0
lug_w = 12.0
m4_hole = 4.5
lug_hole_r = 34.0

top_z = 40.0
top_d = 40.0
top_t = 5.0
bearing_d = 10.0
motor_hole_d = 3.0
motor_hole_r = 10.0

n_pillars = 8
pillar_d = 5.0
pr = pillar_d / 2
r_bot = 26.0
r_top = 15.0

# ---------------- Base ring with lugs ----------------
base = cq.Workplane("XY").circle(base_od / 2).extrude(base_t)
for i in range(4):
    a = i * 90.0
    bar = (cq.Workplane("XY").center((26.0 + lug_hole_r) / 2, 0)
           .rect(lug_hole_r - 26.0, lug_w).extrude(base_t))
    tip = cq.Workplane("XY").center(lug_hole_r, 0).circle(lug_w / 2).extrude(base_t)
    lug = bar.union(tip).rotate((0, 0, 0), (0, 0, 1), a)
    base = base.union(lug)
base = base.cut(cq.Workplane("XY").circle(base_id / 2).extrude(base_t))
base = base.cut(cq.Workplane("XY").polarArray(lug_hole_r, 0, 360, 4)
                .circle(m4_hole / 2).extrude(base_t))

# ---------------- Top motor mount ----------------
top = cq.Workplane("XY").workplane(offset=top_z).circle(top_d / 2).extrude(top_t)
top = top.cut(cq.Workplane("XY").workplane(offset=top_z)
              .circle(bearing_d / 2).extrude(top_t))
top = top.cut(cq.Workplane("XY").workplane(offset=top_z)
              .polarArray(motor_hole_r, 45, 360, 4)
              .circle(motor_hole_d / 2).extrude(top_t))

result = base.union(top)

# ---------------- Pillars ----------------
z0 = base_t / 2
z1 = top_z + top_t / 2
z_mid = (base_t + top_z) / 2
ring_t = 4.0
t_mid = (z_mid - z0) / (z1 - z0)
r_mid = r_bot + (r_top - r_bot) * t_mid


def pt_at_z(p0, d, z):
    s = (z - p0.z) / d.z
    return p0 + d * s


solids = []
for i in range(n_pillars):
    a = math.radians(22.5 + i * 360.0 / n_pillars)
    p0 = cq.Vector(r_bot * math.cos(a), r_bot * math.sin(a), z0)
    p1 = cq.Vector(r_top * math.cos(a), r_top * math.sin(a), z1)
    d = p1 - p0
    dn = d.normalized()
    solids.append(cq.Solid.makeCylinder(pr, d.Length, p0, dn))
    # flared collars (fillet substitutes)
    fl = 2.0
    h = 3.0
    pb = pt_at_z(p0, d, base_t) - dn * 0.5
    solids.append(cq.Solid.makeCone(pr + fl, pr, h, pb, dn))
    pt = pt_at_z(p0, d, top_z) + dn * 0.5
    solids.append(cq.Solid.makeCone(pr + fl, pr, h, pt, -dn))
    pr_lo = pt_at_z(p0, d, z_mid - ring_t / 2) + dn * 0.5
    solids.append(cq.Solid.makeCone(pr + 1.5, pr, 2.5, pr_lo, -dn))
    pr_hi = pt_at_z(p0, d, z_mid + ring_t / 2) - dn * 0.5
    solids.append(cq.Solid.makeCone(pr + 1.5, pr, 2.5, pr_hi, dn))

for s in solids:
    result = result.union(cq.Workplane("XY").add(s))

# ---------------- Mid reinforcing ring ----------------
ring = (cq.Workplane("XY").workplane(offset=z_mid - ring_t / 2)
        .circle(r_mid + 3.5).circle(r_mid - 3.5).extrude(ring_t))
result = result.union(ring)
