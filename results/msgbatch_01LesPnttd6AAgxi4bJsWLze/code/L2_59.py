import cadquery as cq
import math

# Create a 50mm cube
cube = cq.Workplane("XY").box(50, 50, 50)

# Create a blind hole along the X-axis (15mm diameter, 30mm deep)
# This hole goes into the cube from one face along the X direction
# We'll drill from the left face (at x = -25) going towards positive X
hole_x = (
    cq.Workplane("YZ")
    .workplane(offset=-25)  # Position at the left face of the cube
    .circle(15/2)  # 15mm diameter = 7.5mm radius
    .extrude(30, taper=None)  # 30mm deep into the cube
)

# Create a blind hole along the Z-axis (15mm diameter, 30mm deep)
# This hole goes into the cube from the top face along the Z direction
hole_z = (
    cq.Workplane("XY")
    .workplane(offset=25)  # Position at the top face of the cube
    .circle(15/2)  # 15mm diameter = 7.5mm radius
    .extrude(-30, taper=None)  # 30mm deep into the cube (negative Z direction)
)

# Combine the holes with the cube using cut operations
result = cube.cut(hole_x).cut(hole_z)
