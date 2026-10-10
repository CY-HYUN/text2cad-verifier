import cadquery as cq
import math

H = 40.0
# bottom ring (z 0..4)
ring = (cq.Workplane("XY").circle(30).circle(26).extrude(4))

# lugs with M4 holes
for k in range(4):
    a = math.radians(22.5 + 90 * k)
    x, y = 31 * math.cos(a), 31 * math.sin(a)
    lug = cq.Workplane("XY").center(x, y).circle(4.5).extrude(4)
    ring = ring.union(lug)

# top motor mount disc (z 37..40)
top = cq.Workplane("XY").workplane(offset=37).circle(20).extrude(3)

result = ring.union(top)

# mid reinforcement ring
mid = (cq.Workplane("XY").workplane(offset=18.5)
       .circle(24.5).circle(21.5).extrude(3))
result = result.union(mid)

# eight inclined struts + spherical blends at joints
rb, zb = 28.0, 2.0
rt, zt = 18.0, 38.5
rm, zm = 23.0, 20.0
for k in range(8):
    a = math.radians(45 * k)
    c, s = math.cos(a), math.sin(a)
    p0 = cq.Vector(rb * c, rb * s, zb)
    p1 = cq.Vector(rt * c, rt * s, zt)
    d = p1 - p0
    cyl = cq.Solid.makeCylinder(1.5, d.Length, p0, d.normalized())
    result = result.union(cq.Workplane("XY").add(cyl))
    for (r, z) in [(rb, zb), (rt, zt), (rm, zm)]:
        sph = cq.Workplane("XY").sphere(2.2).translate((r * c, r * s, z))
        result = result.union(sph)

# bearing hole and motor holes
result = result.cut(cq.Workplane("XY").workplane(offset=35).circle(5).extrude(6))
for k in range(4):
    a = math.radians(45 + 90 * k)
    result = result.cut(
        cq.Workplane("XY").workplane(offset=35).center(12 * math.cos(a), 12 * math.sin(a))
        .circle(1.5).extrude(6))

# M4 lug holes
for k in range(4):
    a = math.radians(22.5 + 90 * k)
    result = result.cut(
        cq.Workplane("XY").workplane(offset=-1).center(31 * math.cos(a), 31 * math.sin(a))
        .circle(2.2).extrude(6))
