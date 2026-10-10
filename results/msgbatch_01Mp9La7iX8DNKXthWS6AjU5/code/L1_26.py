import cadquery as cq
import math

sphere = cq.Workplane("XY").sphere(30.0)

# Keep the portion below z = 15: intersect with a box spanning z from -30 to 15
keep = cq.Workplane("XY").box(100, 100, 45, centered=(True, True, False)).translate((0, 0, -30))

result = sphere.intersect(keep)
