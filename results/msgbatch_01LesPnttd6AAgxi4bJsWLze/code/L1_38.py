import cadquery as cq
import math

# Create a rhombus with diagonals of 60mm (X-axis) and 30mm (Y-axis)
# The rhombus vertices are at:
# (30, 0, 0), (0, 15, 0), (-30, 0, 0), (0, -15, 0)
# These represent half-diagonals of 30mm and 15mm

half_diag_x = 30  # half of 60mm diagonal along X
half_diag_y = 15  # half of 30mm diagonal along Y
height = 80       # height along Z-axis

# Create the rhombus base in the XY plane
rhombus = cq.Workplane("XY").moveTo(half_diag_x, 0).lineTo(0, half_diag_y).lineTo(-half_diag_x, 0).lineTo(0, -half_diag_y).close()

# Extrude the rhombus along the Z-axis to create the column
result = rhombus.extrude(height)
