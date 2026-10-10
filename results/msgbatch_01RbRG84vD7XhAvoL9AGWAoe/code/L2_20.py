import cadquery as cq
import math

L = 50.0
D = 10.0

# Base cube centered at origin
cube = cq.Workplane("XY").box(L, L, L)

# Axis along the body diagonal (vertex (-25,-25,-25) to (25,25,25))
d = cq.Vector(1, 1, 1).normalized()
length = 200.0
start = cq.Vector(0, 0, 0) - d * (length / 2.0)

hole = cq.Solid.makeCylinder(D / 2.0, length, start, d)

result = cube.cut(cq.Workplane("XY").add(hole))
