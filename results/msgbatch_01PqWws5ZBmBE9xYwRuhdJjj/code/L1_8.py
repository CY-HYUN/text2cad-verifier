import cadquery as cq
import math

# Create a cube: 80mm x 80mm x 40mm tall
cube = cq.Workplane("XY").rect(80.0, 80.0).extrude(40.0)

# Create a sphere with radius 20mm centered at the top center of the cube
# The top center is at (0, 0, 40)
sphere = cq.Workplane("XY").sphere(20.0).translate((0, 0, 40.0))

# Perform a difference operation to cut the upper hemisphere from the cube
result = cube.cut(sphere)
