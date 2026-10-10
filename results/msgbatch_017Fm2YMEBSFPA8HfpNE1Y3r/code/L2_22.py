import cadquery as cq
import math

# Create a 40mm cube
cube = cq.Workplane("XY").box(40, 40, 40)

# Cut a through-hole with diameter 30mm at the center
hole = cq.Workplane("XY").cylinder(height=40, radius=15, centered=True)
cube = cube.cut(hole)

# Select the four vertical edges and apply chamfer
# The "|Z" selector finds edges parallel to the Z-axis (vertical edges)
cube = cube.edges("|Z").chamfer(10)

result = cube
