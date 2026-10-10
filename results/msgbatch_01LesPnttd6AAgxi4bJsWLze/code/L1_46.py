import cadquery as cq
import math

# Create a right-angled triangular base
# The two right-angle sides are 30mm (X-axis) and 40mm (Y-axis)
# The height of the prism is 60mm (Z-axis)

# Define the vertices of the right-angled triangle in the XY plane
# Point 1: Origin (0, 0)
# Point 2: Along X-axis (30, 0)
# Point 3: Along Y-axis (0, 40)
triangle_points = [
    (0, 0),      # Right angle vertex
    (30, 0),     # End of 30mm side
    (0, 40)      # End of 40mm side
]

# Create the triangular base sketch
base = cq.Workplane("XY").polygon(3, forConstruction=False)

# Actually, let's create it properly by defining the triangle vertices
# Create a workplane and draw the triangle
base = cq.Workplane("XY")

# Create the triangle by defining its vertices
triangle = cq.Workplane("XY").moveTo(0, 0).lineTo(30, 0).lineTo(0, 40).close()

# Extrude the triangle along the Z-axis by 60mm
result = triangle.extrude(60)
