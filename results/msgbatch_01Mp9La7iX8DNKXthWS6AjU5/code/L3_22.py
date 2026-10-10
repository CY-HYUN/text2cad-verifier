import cadquery as cq
import math

# Parameters
base_t = 4.0
top_z = 56.0
top_t = 4.0
n_pill = 8
pill_r = 2.0

# Base ring with four lugs
base = cq.Workplane("XY").circle(30).circle(22).extrude(base_t)
for k in range(4):
    a = math.radians(90 * k)
    x, y = 33 * math.cos(a), 33 * math.sin(a)
    lug = cq.Workplane("XY").center(x, y).circle(5).extrude(base_t)
    base = base.union(lug)
for k in range(4):
    a = math.radians(90 * k)
    x, y = 33 * math.cos(a), 33 * math.sin(a)
    hole = cq.Workplane("XY").center(x, y).circle(2.2).extrude(base_t)
    base = base.cut(hole)
# keep the inner bore open after lug union
base = base.cut(cq.Workplane("XY").circle(22).extrude(base_t))

# Top motor mount
top = (cq.Workplane("XY").workplane(offset=top_z).circle(20).extrude(top_t)
       .faces(">Z").workplane().circle(5).cutThruAll())
for k in range(4):
    a = math.radians(22.5 + 90 * k)
    h = (cq.Workplane("XY").workplane(offset=top_z)
         .center(10 * math.cos(a), 10 * math.sin(a)).circle(1.5).extrude(top_t))
    top = top.cut(h)

result = base.union(top)

# Inclined pillars (frustum cage)
z0, z1 = 2.0, 58.0
r0, r1 = 26.0, 16.0
for k in range(n_pill):
    a = math.radians(45 * k)
    p0 = cq.Vector(r0 * math.cos(a), r0 * math.sin(a), z0)
    p1 = cq.Vector(r1 * math.cos(a), r1 * math.sin(a), z1)
    d = p1 - p0
    cyl = cq.Solid.makeCylinder(pill_r, d.Length, p0, d.normalized())
    result = result.union(cq.Workplane("XY").add(cyl))

# Mid-height reinforcing ring
zm = (z0 + z1) / 2.0
rm = r0 + (r1 - r0) * 0.5
ring = (cq.Workplane("XY").workplane(offset=zm - 1.5)
        .circle(rm + 2.5).circle(rm - 2.5).extrude(3.0))
result = result.union(ring)

# Fillets at junctions (best effort)
try:
    sel = None
    for zlo, zhi in [(base_t - 0.1, base_t + 0.1), (top_z - 0.1, top_z + 0.1),
                     (zm - 1.6, zm + 1.6)]:
        pass
    f = result.edges(cq.selectors.BoxSelector((-40, -40, top_z - 0.1), (40, 40, top_z + 0.1)))
    f = f.edges(cq.selectors.RadiusNthSelector(0, directionMax=True)) if False else f
    filleted = result.edges(cq.selectors.BoxSelector((-40, -40, base_t - 0.1), (40, 40, base_t + 0.1))).fillet(0.8)
    result = filleted
except Exception:
    pass
try:
    result = result.edges(cq.selectors.BoxSelector((-40, -40, top_z - 0.1), (40, 40, top_z + 0.1))).fillet(0.8)
except Exception:
    pass
