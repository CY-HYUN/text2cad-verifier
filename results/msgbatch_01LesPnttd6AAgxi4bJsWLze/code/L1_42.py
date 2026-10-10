import cadquery as cq
import math

# Create a cylinder with diameter 30mm and height 50mm
cylinder = cq.Workplane("XY").cylinder(height=50, radius=15, centered=True)

# Create a cutting plane at 30 degrees to the base
# The plane cuts through the top of the cylinder
# We need to create a box that will cut the cylinder at an angle

# The plane is tilted 30 degrees from horizontal
# We'll create a large box and rotate it to cut the cylinder
cut_height = 100
cut_length = 100
cut_width = 100

# Create a cutting box positioned above the cylinder
# Rotate it 30 degrees around the Y-axis (tilt around the width direction)
cutting_box = (
    cq.Workplane("XY")
    .box(cut_length, cut_width, cut_height)
    .rotate((0, 0, 0), (0, 1, 0), 30)  # Rotate 30 degrees around Y-axis
    .translate((0, 0, 30))  # Position it to cut the top of the cylinder
)

# Cut the cylinder with the tilted plane
result = cylinder.cut(cutting_box)
