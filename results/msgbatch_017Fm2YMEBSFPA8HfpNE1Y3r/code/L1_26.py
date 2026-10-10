import cadquery as cq
import math

# Create a sphere with radius 30 mm centered at the origin
sphere = cq.Workplane("XY").sphere(30.0)

# Create a box that extends above the sphere to use as a cutting tool
# Position it so it cuts at Z = 15.0 mm, removing everything above
# Box needs to be larger and positioned correctly
cutting_box = cq.Workplane("XY").box(200, 200, 60).translate((0, 0, 45))

# Cut the sphere with the box to remove the upper portion above Z = 15.0
result = sphere.cut(cutting_box)
