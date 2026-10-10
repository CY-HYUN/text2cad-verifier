import cadquery as cq
import math

a = 50.0
r = 30.0

cube = cq.Workplane("XY").box(a, a, a, centered=False)  # corner at origin through (50,50,50)
sphere = cq.Workplane("XY").sphere(r)  # centered at origin vertex

result = cube.cut(sphere)
