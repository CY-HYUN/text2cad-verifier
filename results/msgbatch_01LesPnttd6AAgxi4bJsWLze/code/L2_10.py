import cadquery as cq
import math

# Create the base rectangular plate
base = cq.Workplane("XY").box(80, 40, 10)

# Create the left flange (40mm high, 40mm wide, 10mm thick)
# Positioned at the left end of the base
left_flange = cq.Workplane("XY").box(10, 40, 40).translate((-35, 0, 20))

# Create the right flange (40mm high, 40mm wide, 10mm thick)
# Positioned at the right end of the base
right_flange = cq.Workplane("XY").box(10, 40, 40).translate((35, 0, 20))

# Combine base and flanges
part = base.union(left_flange).union(right_flange)

# Add through-hole at center of left flange (10mm diameter)
# The left flange is centered at x=-35, so hole goes through it
part = part.faces(">X").workplane().center(0, 0).hole(10)

# Add through-hole at center of right flange (10mm diameter)
part = part.faces("<X").workplane().center(0, 0).hole(10)

# Add countersink on the right flange
# 20mm diameter, 2mm deep
part = part.faces("<X").workplane().center(0, 0).cboreHole(10, 20, 2)

result = part
