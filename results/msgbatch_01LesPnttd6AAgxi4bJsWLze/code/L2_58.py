import cadquery as cq
import math

# Create the main rectangular prism body
length = 80  # mm
width = 40   # mm
height = 40  # mm
hole_radius = 5  # mm radius for the circular passages

# Start with the solid rectangular prism
result = cq.Workplane("XY").box(length, width, height, centered=True)

# Define the center point of the left face
# Left face is at x = -length/2 = -40
# The hole enters from the center of the left side

# Create the horizontal hole segment (entering from left, going 40mm deep)
# This hole goes from the left face toward the center
horizontal_hole = (
    cq.Workplane("YZ")
    .circle(hole_radius)
    .extrude(40, both=False)  # 40mm deep from left
)

# Translate the horizontal hole to the left face center
# Left face center is at x=-40, y=0, z=0
horizontal_hole = horizontal_hole.translate((-40, 0, 0))

# Create the vertical hole segment (entering from top, going 20mm deep)
# This hole goes from the top surface downward
vertical_hole = (
    cq.Workplane("XY")
    .circle(hole_radius)
    .extrude(20, both=False)  # 20mm deep from top
)

# Translate the vertical hole to the top face center
# Top face center is at x=0, y=0, z=20
vertical_hole = vertical_hole.translate((0, 0, 20))

# Cut both holes from the main body
result = result.cut(horizontal_hole)
result = result.cut(vertical_hole)
