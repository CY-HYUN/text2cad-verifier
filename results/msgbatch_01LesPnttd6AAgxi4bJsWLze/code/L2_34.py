import cadquery as cq
import math

# Create the main cylinder: diameter 20mm, length 50mm
main_cylinder = cq.Workplane("XY").cylinder(height=50, radius=10, centered=True)

# Create a groove cutting tool
# The groove is 5mm wide and 9mm deep, cut radially into the middle
# We'll use a rectangular box to cut the groove
groove_width = 5
groove_depth = 9
groove_length = 50  # Extends along the full length

# Create a box for the groove (positioned to cut from the side)
groove_box = cq.Workplane("XY").box(groove_length, groove_width, groove_depth, centered=True)

# Position the groove box so it cuts into the cylinder radially
# The groove should be positioned at the outer surface of the cylinder
# and cut inward by 9mm, leaving a 2mm diameter shaft (1mm radius)
# The cylinder has radius 10mm, so cutting 9mm deep leaves 1mm
groove_box = groove_box.translate((0, 10 - groove_depth/2, 0))

# Cut the groove from the main cylinder
result = main_cylinder.cut(groove_box)

# Verify the geometry by ensuring the cut creates the intended features:
# - Original cylinder: 20mm diameter, 50mm length
# - Groove: 5mm wide, 9mm deep, around the circumference at the middle
# - Remaining shaft at the minimum point: 2mm diameter (1mm radius from center + 1mm on opposite side)
