import cadquery as cq
import math

# Create a cylinder (disc) with diameter 60mm and thickness 10mm
disc = cq.Workplane("XY").cylinder(height=10, radius=30, centered=True)

# Create a cylindrical cutout (bite) with diameter 20mm
# Position it at the edge of the disc (at x=30, which is the radius)
# The cutout cylinder should extend beyond the disc to ensure complete removal
cutout = cq.Workplane("XY").cylinder(height=20, radius=10, centered=True).translate((30, 0, 0))

# Subtract the cutout from the disc
result = disc.cut(cutout)
