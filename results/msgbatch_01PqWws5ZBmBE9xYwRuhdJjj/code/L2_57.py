import cadquery as cq
import math

# Create the base cylinder
cylinder = cq.Workplane("XY").cylinder(height=30, radius=50)

# Create a circle with radius 10 mm on the top edge
# Center located on the edge of the cylinder (at radius 50)
hole_radius = 10
edge_radius = 50

# Create cutting tool for single hole
cutting_circle = cq.Workplane("XY").circle(hole_radius).extrude(30)

# Apply circular array to create 8 copies of the hole
# Position the hole at the edge of the cylinder
result = cylinder
for i in range(8):
    angle = (i * 360 / 8) * math.pi / 180
    x = edge_radius * math.cos(angle)
    y = edge_radius * math.sin(angle)
    
    # Create a hole at this position
    hole = cq.Workplane("XY").moveTo(x, y).circle(hole_radius).extrude(30)
    result = result.cut(hole)

# Cut the center hole with diameter 30 mm (radius 15 mm)
center_hole = cq.Workplane("XY").circle(15).extrude(30)
result = result.cut(center_hole)

# Create keyway rectangle (8x4 mm) at the center
# The keyway extends from the center
keyway_width = 8
keyway_height = 4
keyway_length = 30

# Create keyway as a rectangular box centered at origin, extending in one direction
keyway = cq.Workplane("XY").rect(keyway_width, keyway_height).extrude(keyway_length)
result = result.cut(keyway)
