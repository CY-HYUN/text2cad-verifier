import cadquery as cq
import math

# Create a rhombus in the XY plane
# Long diagonal: 60 mm (along X-axis)
# Short diagonal: 30 mm (along Y-axis)
# The diagonals intersect at the origin and are perpendicular

# Calculate rhombus vertices
# Half-diagonals
half_long = 60.0 / 2  # 30 mm
half_short = 30.0 / 2  # 15 mm

# Rhombus vertices (in order, starting from right point)
vertices = [
    (half_long, 0),      # Right point (30, 0)
    (0, half_short),     # Top point (0, 15)
    (-half_long, 0),     # Left point (-30, 0)
    (0, -half_short),    # Bottom point (0, -15)
]

# Create workplane and sketch the rhombus
result = (
    cq.Workplane("XY")
    .polyline(vertices)
    .close()
    .extrude(80.0)
)
