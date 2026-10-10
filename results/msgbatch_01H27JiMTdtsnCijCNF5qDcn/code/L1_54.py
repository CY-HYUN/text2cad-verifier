import cadquery as cq
import math

# Sphere centered at origin, radius 25
sphere = cq.Workplane("XY").sphere(25.0)

# Cutting cylinder along Z, radius 7, height 60, centered on origin so it passes through
cylinder = cq.Workplane("XY").circle(7.0).extrude(30.0, both=True)

# Boolean difference: sphere minus cylinder
result = sphere.cut(cylinder)
