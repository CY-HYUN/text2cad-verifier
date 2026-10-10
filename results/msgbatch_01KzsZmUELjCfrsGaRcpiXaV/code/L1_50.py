import cadquery as cq
import math

# Create the first cylinder along the X-axis
# Length 50mm, diameter 20mm (radius 10mm)
cyl1 = cq.Workplane("XY").cylinder(height=50, radius=10, centered=True)
cyl1 = cyl1.rotate((0, 0, 0), (0, 1, 0), 90)  # Rotate to align with X-axis

# Create the second cylinder along the Z-axis
# Length 50mm, diameter 20mm (radius 10mm)
cyl2 = cq.Workplane("XY").cylinder(height=50, radius=10, centered=True)
# cyl2 is already along Z-axis, position it so cylinders meet at their ends
cyl2 = cyl2.translate((25, 0, 25))  # Move so end of cyl1 meets end of cyl2

# Union the two cylinders to create the elbow
result = cyl1.union(cyl2)
