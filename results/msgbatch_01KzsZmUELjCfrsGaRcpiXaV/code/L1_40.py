import cadquery as cq
import math

# Create the stepped shaft (dumbbell shape)
# The shaft consists of three coaxial cylinders:
# - Left end: diameter 30mm, length 20mm
# - Middle: diameter 15mm, length 20mm
# - Right end: diameter 30mm, length 20mm

# Start by creating a workplane and building along the Z-axis
workplane = cq.Workplane("XY")

# Create left end cylinder (diameter 30mm = radius 15mm, length 20mm)
# Positioned from Z = -40 to Z = -20
left_end = workplane.cylinder(height=20, radius=15, centered=False)

# Create middle cylinder (diameter 15mm = radius 7.5mm, length 20mm)
# Positioned from Z = -20 to Z = 0, centered at origin
middle = workplane.workplane(offset=-20).cylinder(height=20, radius=7.5, centered=False)

# Create right end cylinder (diameter 30mm = radius 15mm, length 20mm)
# Positioned from Z = 0 to Z = 20
right_end = workplane.cylinder(height=20, radius=15, centered=False)

# Combine all three cylinders
result = left_end.union(middle).union(right_end)
