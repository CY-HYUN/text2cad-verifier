import cadquery as cq
import math

# Create the main cylinder
# Diameter: 30mm, Height: 60mm, Z-axis is the main axis
main_cylinder = cq.Workplane("XY").cylinder(height=60, radius=15, centered=True)

# Create the side hole
# Diameter: 10mm, drilled radially at the midpoint (Z=0 when centered)
# The hole goes along the Y-axis (radially from the cylinder's axis)
side_hole = cq.Workplane("XZ").cylinder(height=10, radius=5, centered=True)

# The side hole needs to be positioned so it intersects the cylinder properly
# Since the cylinder is centered at Z=0 and has radius 15mm, the hole should go through it
# The hole axis is along Y, so we create it in the XZ plane and it extends in Y direction

# Perform the boolean operation to subtract the side hole from the main cylinder
result = main_cylinder.cut(side_hole)
