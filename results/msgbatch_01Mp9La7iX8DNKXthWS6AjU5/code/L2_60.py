import cadquery as cq
import math

H = 25.0
ring = cq.Workplane("XY").circle(45).circle(20).extrude(H)

# radial holes
for i in range(6):
    cyl = (cq.Workplane("YZ").workplane(offset=0)
           .center(0, 12.5).circle(5).extrude(50))
    cyl = cyl.rotate((0, 0, 0), (0, 0, 1), i * 60)
    ring = ring.cut(cyl)

# countersunk axial holes
for i in range(6):
    ang = 30 + i * 60
    x = 32.5 * math.cos(math.radians(ang))
    y = 32.5 * math.sin(math.radians(ang))
    hole = cq.Workplane("XY").center(x, y).circle(3).extrude(H)
    cone = cq.Solid.makeCone(3, 5, 2, pnt=cq.Vector(x, y, H - 2), dir=cq.Vector(0, 0, 1))
    ring = ring.cut(hole).cut(cq.Workplane("XY").add(cone))

result = ring
