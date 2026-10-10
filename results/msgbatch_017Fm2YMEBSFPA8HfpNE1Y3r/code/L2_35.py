import cadquery as cq
import math

# Start with a 60mm cube centered at origin
cube = cq.Workplane("XY").box(60, 60, 60)

# First hole: Right view plane (YZ plane), circle at Z=5mm, cut along X-axis
# Create a workplane on the right face and drill
hole1 = (cq.Workplane("YZ")
         .move(0, 5)  # Move to Z=5mm
         .circle(10)  # 20mm diameter = 10mm radius
         .cutThruAll())

# Apply first hole cut
cube = cube.cut(hole1)

# Second hole: Front view plane (XZ plane), circle at Z=-5mm, cut along Y-axis
# Create a workplane on the front face and drill
hole2 = (cq.Workplane("XZ")
         .move(0, -5)  # Move to Z=-5mm
         .circle(10)   # 20mm diameter = 10mm radius
         .cutThruAll())

# Apply second hole cut
result = cube.cut(hole2)
