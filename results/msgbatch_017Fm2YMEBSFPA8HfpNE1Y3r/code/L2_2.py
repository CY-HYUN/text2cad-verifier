import cadquery as cq
import math

# Create a sphere with radius 40 mm centered at the origin
sphere = cq.Workplane("XY").sphere(40)

# Create a cylinder with radius 15 mm (diameter 30 mm) centered at X = 25 mm, Y = 0
# and extrude it through the entire sphere along Z-axis
cylinder = cq.Workplane("XY").moveTo(25, 0).circle(15).extrude(100, both=True)

# Perform the cut operation on the sphere
result = sphere.cut(cylinder)
