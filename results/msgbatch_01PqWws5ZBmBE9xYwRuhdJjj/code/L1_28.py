import cadquery as cq
import math

# Create a square on the XY plane (60x60 mm)
square = cq.Workplane("XY").rect(60.0, 60.0).extrude(60.0)

# Calculate the center of the cube (which is at 30, 30, 30 from origin)
center_x = 30.0
center_y = 30.0
center_z = 30.0

# Create a sphere with diameter 61.0 mm (radius 30.5 mm)
# Position it at the geometric center of the cube
sphere = cq.Workplane("XY").sphere(61.0 / 2.0).translate((center_x, center_y, center_z))

# Perform the difference operation: subtract sphere from cube
result = square.cut(sphere)
