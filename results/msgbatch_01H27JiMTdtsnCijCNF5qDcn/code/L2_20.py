import cadquery as cq
import math

cube = cq.Workplane("XY").box(50, 50, 50, centered=False)

c = cq.Vector(25, 25, 25)
d = cq.Vector(1, 1, 1).normalized()
L = 200
base = c - d * (L / 2)

cyl = cq.Solid.makeCylinder(5, L, base, d)

result = cube.cut(cq.Workplane("XY").add(cyl))
