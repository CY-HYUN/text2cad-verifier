import cadquery as cq
import math

L = 50.0
d = 10.0

cube = cq.Workplane("XY").box(L, L, L)

n = 1.0 / math.sqrt(3.0)
direction = cq.Vector(n, n, n)
length = 200.0
start = cq.Vector(-n * length / 2, -n * length / 2, -n * length / 2)

cyl = cq.Solid.makeCylinder(d / 2.0, length, start, direction)

result = cube.cut(cq.Workplane("XY").add(cyl))
