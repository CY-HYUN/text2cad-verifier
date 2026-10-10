import cadquery as cq
import math

# Create the large cylinder with diameter 50mm (radius 25mm) and length 50mm along Z-axis
large_cylinder = cq.Workplane("XY").cylinder(height=50, radius=25, centered=False)

# Create the small cylinder with diameter 30mm (radius 15mm) and length 50mm along Z-axis
# Center-to-center distance is 40mm along X-axis
small_cylinder = cq.Workplane("XY").cylinder(height=50, radius=15, centered=False).translate((40, 0, 0))

# Combine both cylinders
result = large_cylinder.union(small_cylinder)
