import cadquery as cq
import math

# Create the base cube
# Start with XY plane and draw a 50mm square centered at origin
base = cq.Workplane("XY").box(50, 50, 50)

# The cube is now 50x50x50mm, centered at origin (so -25 to +25 in all directions)

# Create a cylinder to cut from the front (YZ plane)
# The cylinder should have diameter 60mm and cut through the cube
# Front view means looking along the Y axis
# We need a cylinder aligned along the Y axis (perpendicular to YZ plane)
cylinder_front = cq.Workplane("YZ").circle(30).extrude(100, both=True)

# Create a cylinder to cut from the right (XZ plane)
# Right view means looking along the X axis
# We need a cylinder aligned along the X axis (perpendicular to XZ plane)
cylinder_right = cq.Workplane("XZ").circle(30).extrude(100, both=True)

# Perform Boolean subtraction to create the star-shaped column
result = base.cut(cylinder_front).cut(cylinder_right)
