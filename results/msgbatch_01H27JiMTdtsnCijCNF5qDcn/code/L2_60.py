import cadquery as cq
import math

ring = cq.Workplane("XY").circle(45).circle(20).extrude(25)

# radial holes
radial = (cq.Workplane("XZ").center(0, 12.5).circle(5).extrude(50))  # XZ normal is -Y, extrudes toward -Y
for i in range(6):
    ring = ring.cut(radial.rotate((0, 0, 0), (0, 0, 1), 60 * i))

# countersunk axial hole
px = 32.5 * math.cos(math.radians(30))
py = 32.5 * math.sin(math.radians(30))
thru = cq.Workplane("XY").circle(3).extrude(25)
cone = cq.Solid.makeCone(0, 6, 6, pnt=cq.Vector(0, 0, 19), dir=cq.Vector(0, 0, 1))
# cone: radius 0 at z=19 to radius 6 at z=25 -> make a proper countersink: radius 3 at z=22, 6 at z=25
cs = cq.Solid.makeCone(3, 6, 3, pnt=cq.Vector(0, 0, 22), dir=cq.Vector(0, 0, 1))
hole = thru.union(cq.Workplane("XY").add(cs)).translate((px, py, 0))
for i in range(6):
    ring = ring.cut(hole.rotate((0, 0, 0), (0, 0, 1), 60 * i))

result = ring
