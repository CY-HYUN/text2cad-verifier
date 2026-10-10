import cadquery as cq
import math

# Create the first cylinder along the X-axis
# Centered at origin, extending 50mm in the X direction
cyl1 = cq.Workplane("XY").cylinder(height=50, radius=10, centered=True)
cyl1 = cyl1.rotate((0, 0, 0), (0, 1, 0), 90)  # Rotate to align with X-axis

# Create the second cylinder along the Z-axis
# Positioned so it connects at the end of the first cylinder
cyl2 = cq.Workplane("XY").cylinder(height=50, radius=10, centered=True)
# cyl2 is already along Z-axis, translate it to connect properly
cyl2 = cyl2.translate((25, 0, 0))  # Move to the end of first cylinder

# Union the two cylinders to create the elbow
result = cyl1.union(cyl2)
