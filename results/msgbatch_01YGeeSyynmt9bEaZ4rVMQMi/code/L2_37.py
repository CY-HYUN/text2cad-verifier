import cadquery as cq
import math

R = 20.0
cyl_d = 15.0
L = 30.0
hole_d = 8.0
hole_depth = 10.0

body = cq.Workplane("XY").sphere(R)

dirs = [
    (1, 0, 0), (-1, 0, 0),
    (0, 1, 0), (0, -1, 0),
    (0, 0, 1), (0, 0, -1),
]

for d in dirs:
    cyl = cq.Solid.makeCylinder(cyl_d / 2.0, L, cq.Vector(0, 0, 0), cq.Vector(*d))
    body = body.union(cq.Workplane("XY").add(cyl))

# Blind holes from each end face inward
for d in dirs:
    v = cq.Vector(*d)
    start = v * (L - hole_depth)
    hole = cq.Solid.makeCylinder(hole_d / 2.0, hole_depth + 0.01, start, v)
    body = body.cut(cq.Workplane("XY").add(hole))

result = body
