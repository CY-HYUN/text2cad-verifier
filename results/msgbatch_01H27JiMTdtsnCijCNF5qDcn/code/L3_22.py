import cadquery as cq
import math

# ---------- base ring with lugs ----------
base_t = 4.0
base = (cq.Workplane("XY").circle(30.0).circle(22.0).extrude(base_t))
for k in range(4):
    a = math.radians(45 + 90 * k)
    x, y = 32.0 * math.cos(a), 32.0 * math.sin(a)
    lug = cq.Workplane("XY").center(x, y).circle(5.5).extrude(base_t)
    # blend lug toward ring
    neck = (cq.Workplane("XY").center(27.0 * math.cos(a), 27.0 * math.sin(a))
            .circle(5.5).extrude(base_t))
    base = base.union(lug).union(neck)
for k in range(4):
    a = math.radians(45 + 90 * k)
    x, y = 33.0 * math.cos(a), 33.0 * math.sin(a)
    hole = cq.Workplane("XY").center(x, y).circle(2.2).extrude(base_t)
    base = base.cut(hole)

# ---------- top motor mount ----------
z_top = 50.0
top_t = 4.0
top = (cq.Workplane("XY").workplane(offset=z_top).circle(20.0).extrude(top_t))
top = top.cut(cq.Workplane("XY").workplane(offset=z_top).circle(5.0).extrude(top_t))
for k in range(4):
    a = math.radians(45 + 90 * k)
    x, y = 8.0 * math.cos(a), 8.0 * math.sin(a)
    top = top.cut(cq.Workplane("XY").workplane(offset=z_top).center(x, y)
                  .circle(1.5).extrude(top_t))

result = base.union(top)

# ---------- inclined pillars ----------
z0, z1 = 2.0, 52.0
r0, r1 = 26.0, 16.0
pr = 2.0
for k in range(8):
    a = math.radians(45 * k)
    p0 = cq.Vector(r0 * math.cos(a), r0 * math.sin(a), z0)
    p1 = cq.Vector(r1 * math.cos(a), r1 * math.sin(a), z1)
    d = p1 - p0
    cyl = cq.Solid.makeCylinder(pr, d.Length, p0, d)
    result = result.union(cq.Workplane("XY").add(cyl))

# ---------- mid reinforcing ring ----------
z_mid = 27.0
ring = (cq.Workplane("XY").workplane(offset=z_mid - 2.0)
        .circle(24.0).circle(18.0).extrude(4.0))
result = result.union(ring)

# ---------- fillets at junctions ----------
try:
    sel = []
    for e in result.val().Edges():
        c = e.Center()
        rr = math.hypot(c.x, c.y)
        if (abs(c.z - base_t) < 0.6 and 20 < rr < 31) or \
           (abs(c.z - z_top) < 0.6 and 10 < rr < 21) or \
           (abs(c.z - 25.0) < 0.3 and 15 < rr < 25) or \
           (abs(c.z - 29.0) < 0.3 and 15 < rr < 25):
            sel.append(e)
    filleted = result.newObject(sel).fillet(0.8)
    if filleted.val().isValid():
        result = filleted
except Exception:
    pass
