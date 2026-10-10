import cadquery as cq
import math

# Create the large cylinder
large_cylinder = cq.Workplane("XY").cylinder(height=50, radius=25, centered=False)

# Create the small cylinder
# The center-to-center distance is 40mm
# Large cylinder center is at (0, 0)
# Small cylinder center should be at (40, 0)
small_cylinder = cq.Workplane("XY").cylinder(height=50, radius=15, centered=False).translate((40, 0, 0))

# Combine both cylinders
result = large_cylinder.union(small_cylinder)
