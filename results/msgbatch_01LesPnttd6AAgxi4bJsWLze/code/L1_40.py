import cadquery as cq
import math

# Create the stepped shaft (dumbbell shape)
# The shaft consists of three coaxial cylinders:
# - Left end: diameter 30mm, length 20mm
# - Middle: diameter 15mm, length 20mm
# - Right end: diameter 30mm, length 20mm

# Start with the middle section (thinner cylinder)
# Place it centered at origin, extending along Z-axis
middle = cq.Workplane("XY").cylinder(height=20, radius=7.5, centered=True)

# Create left end cylinder (diameter 30mm = radius 15mm)
# Position it at Z = -20 (below the middle section)
left_end = cq.Workplane("XY").workplane(offset=-20).cylinder(height=20, radius=15, centered=False)

# Create right end cylinder (diameter 30mm = radius 15mm)
# Position it at Z = 20 (above the middle section)
right_end = cq.Workplane("XY").workplane(offset=20).cylinder(height=20, radius=15, centered=False)

# Combine all three cylinders
result = middle.union(left_end).union(right_end)
