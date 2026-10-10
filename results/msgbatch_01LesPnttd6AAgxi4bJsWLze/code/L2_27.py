import cadquery as cq
import math

# Create the main cylindrical body
result = cq.Workplane("XY").cylinder(height=50, radius=15)

# Create the hexagonal hole (upper segment, 25mm deep)
# For a regular hexagon with inscribed circle diameter = 15mm (radius = 7.5mm)
# The circumradius of the hexagon is 15/sqrt(3) ≈ 8.66mm
hex_radius = 15 / math.sqrt(3)

# Create hexagonal hole from top, 25mm deep
hex_hole = (
    cq.Workplane("XY")
    .polygon(6, hex_radius)
    .extrude(-25)
)

# Create circular hole (lower segment, 25mm deep)
# Starting from z = -25 and going to z = -50
circular_hole = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .cylinder(height=25, radius=7.5)
    .translate((0, 0, -25))
)

# Combine the holes
combined_holes = hex_hole.union(circular_hole)

# Subtract the combined holes from the main body
result = result.cut(combined_holes)
