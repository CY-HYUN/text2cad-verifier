import cadquery as cq
import math

L = 50.0
cube = cq.Workplane("XY").box(L, L, L, centered=False)

p0 = cq.Vector(0, 0, 0)
p1 = cq.Vector(L, L, L)
d = p1 - p0
length = d.Length
dirn = d.normalized()

# Cylinder along the body diagonal, extended beyond both ends
ext = 10.0
cyl = cq.Solid.makeCylinder(5.0, length + 2 * ext, p0 - dirn * ext, dirn)

result = cube.cut(cq.Workplane("XY").add(cyl))
