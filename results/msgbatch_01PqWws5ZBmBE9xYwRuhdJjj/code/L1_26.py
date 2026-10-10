import cadquery as cq
import math

# Create a sphere with radius 30 mm centered at the origin
sphere = cq.Workplane("XY").sphere(30.0)

# Create a box that extends above the sphere to use as a cutting tool
# The box will be positioned to cut at Z = 15.0 mm
cutting_box = cq.Workplane("XY").box(100, 100, 100, centered=True).translate((0, 0, 20))

# Cut the sphere with the box to remove the upper portion above Z = 15.0
result = sphere.cut(cutting_box)
