import cadquery as cq
import math

# Create a cube with edge length 50 mm
cube = cq.Workplane("XY").box(50, 50, 50, centered=False)

# Define the corner to cut off
# We'll cut the corner at (50, 50, 50) with a plane that cuts 15mm along each axis
# The plane passes through points (35, 50, 50), (50, 35, 50), and (50, 50, 35)

# Create a cutting plane using three points that form the triangular cut
# These points represent where the plane intersects each axis
point1 = (50 - 15, 50, 50)      # (35, 50, 50) - cut 15mm along X
point2 = (50, 50 - 15, 50)      # (50, 35, 50) - cut 15mm along Y
point3 = (50, 50, 50 - 15)      # (50, 50, 35) - cut 15mm along Z

# Create a workplane at one of the points and define the cutting plane
# Using the normal vector to the plane defined by the three points
# Normal = (point1 - point3) × (point2 - point3)
v1 = (point1[0] - point3[0], point1[1] - point3[1], point1[2] - point3[2])
v2 = (point2[0] - point3[0], point2[1] - point3[1], point2[2] - point3[2])

# Cross product for normal
normal = (
    v1[1] * v2[2] - v1[2] * v2[1],
    v1[2] * v2[0] - v1[0] * v2[2],
    v1[0] * v2[1] - v1[1] * v2[0]
)

# Create a box that represents the material to be cut away
# A larger box positioned at the corner to be removed
cutting_box = cq.Workplane("XY").box(20, 20, 20, centered=False).translate((30, 30, 30))

# Use a plane to cut the corner more precisely
# Create a plane through the three points and cut everything on one side
result = cube.split(cq.Workplane("XY").plane.offset(0).moveTo(0, 0))

# Alternative approach: use a half-space to cut
# Create the cut using a plane defined by the normal and a point
result = cube.cut(
    cq.Workplane("XY")
    .workplane(offset=0)
    .transformed(offset=(50, 50, 50))
    .box(30, 30, 30, centered=True)
)

# Better approach: create the corner cut as a tetrahedron
# and subtract it from the cube
# Points of the tetrahedron: (50,50,50), (35,50,50), (50,35,50), (50,50,35)
corner_cutting_box = (
    cq.Workplane("XY")
    .moveTo(35, 50)
    .lineTo(50, 35)
    .lineTo(50, 50)
    .close()
    .extrude(15)
    .translate((0, 0, 35))
)

# Actually, we need to cut using a proper plane
# Create a simple box from corner and subtract it with plane cut
result = cq.Workplane("XY").box(50, 50, 50, centered=False)

# Cut by creating a box at the corner and using boolean operations
cut_volume = (
    cq.Workplane("XY")
    .box(20, 20, 20, centered=False)
    .translate((30, 30, 30))
)

result = result.cut(cut_volume)
