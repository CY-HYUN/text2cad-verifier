import cadquery as cq
import math

# Create a cylinder with diameter 30mm and height 50mm
# Cylinder is centered at origin, extending from Z=-25 to Z=25
cylinder = cq.Workplane("XY").cylinder(height=50, radius=15, centered=True)

# Create a cutting plane at 30 degrees to the base
# The plane tilts around the Y-axis (width direction)
# We need a large box to cut the cylinder

# Create a large box for cutting
cut_height = 150
cut_length = 150
cut_width = 150

# The box will be rotated 30 degrees around the Y-axis
# Position it so it cuts from the top of the cylinder downward
cutting_box = (
    cq.Workplane("XY")
    .box(cut_length, cut_width, cut_height)
    .rotate((0, 0, 0), (0, 1, 0), 30)  # Rotate 30 degrees around Y-axis
    .translate((0, 0, 50))  # Position it to cut from above
)

# Cut the cylinder with the tilted plane
result = cylinder.cut(cutting_box)
