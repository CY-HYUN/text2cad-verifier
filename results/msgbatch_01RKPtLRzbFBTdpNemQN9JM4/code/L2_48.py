import cadquery as cq
import math

L = 50.0
R = 30.0

cube = cq.Workplane("XY").box(L, L, L, centered=False)  # corner at origin
sphere = cq.Workplane("XY").sphere(R).translate((0, 0, 0))

result = cube.cut(sphere)
