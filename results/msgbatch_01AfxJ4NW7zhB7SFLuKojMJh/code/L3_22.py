import cadquery as cq
import math

H = 40.0
t = 4.0

# bottom mounting ring (OD 60)
bottom = cq.Workplane("XY").circle(30).circle(26).extrude(t)

# top motor mount plate (OD 40)
top = cq.Workplane("XY").workplane(offset=H - t).circle(20).extrude(t)

result = bottom.union(top)

# bolt lugs on the bottom ring
for i in range(4):
    a = 22.5 + 90 * i
    lug = (cq.Workplane("XY").center(33, 0).circle(5).extrude(t)
           .union(cq.Workplane("XY").center(30, 0).rect(8, 10).extrude(t)))
    lug = lug.rotate((0, 0, 0), (0, 0, 1), a)
    result = result.union(lug)

# eight inclined supports with spherical blends at the joints
r_sup = 1.5
rb, rt = 28.0, 18.0
zb, zt = t / 2, H - t / 2
for i in range(8):
    a = math.radians(45 * i)
    p1 = cq.Vector(rb * math.cos(a), rb * math.sin(a), zb)
    p2 = cq.Vector(rt * math.cos(a), rt * math.sin(a), zt)
    d = p2 - p1
    cyl = cq.Solid.makeCylinder(r_sup, d.Length, p1, d.normalized())
    result = result.union(cq.Workplane("XY").add(cyl))
    pm = (p1 + p2) * 0.5
    for p, rr in ((p1, 2.3), (p2, 2.3), (pm, 2.2)):
        sph = cq.Workplane("XY").sphere(rr).translate((p.x, p.y, p.z))
        result = result.union(sph)

# horizontal mid-height reinforcement ring
mid = (cq.Workplane("XY").workplane(offset=H / 2 - 1.5)
       .circle(24.5).circle(21.5).extrude(3))
result = result.union(mid)

# bearing hole and motor fixing holes
result = result.cut(
    cq.Workplane("XY").workplane(offset=H - t - 1).circle(5).extrude(t + 2))
for i in range(4):
    a = math.radians(45 + 90 * i)
    result = result.cut(
        cq.Workplane("XY").workplane(offset=H - t - 1)
        .center(8 * math.cos(a), 8 * math.sin(a)).circle(1.5).extrude(t + 2))

# M4 holes in lugs
for i in range(4):
    a = math.radians(22.5 + 90 * i)
    result = result.cut(
        cq.Workplane("XY").workplane(offset=-1)
        .center(33 * math.cos(a), 33 * math.sin(a)).circle(2.2).extrude(t + 2))
