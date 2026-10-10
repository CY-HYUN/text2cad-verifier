import cadquery as cq
import math

# Create a cube with edge length 50 mm
cube = cq.Workplane("XY").box(50, 50, 50, centered=False)

# Cut off the corner at (50, 50, 50) by cutting 15mm along each axis
# We need to create a cutting solid that represents the corner to remove
# The corner to cut is defined by the plane passing through (35, 50, 50), (50, 35, 50), (50, 50, 35)

# Create a pyramid/tetrahedron-like cutting volume
# We'll use a box positioned at the corner and oriented correctly
# Then subtract it to create the 45-degree cut

# Create the main cube
result = cq.Workplane("XY").box(50, 50, 50, centered=False)

# Create a cutting solid - a box at the corner that we want to remove
# Position it so it cuts the corner properly
cutting_solid = (
    cq.Workplane("XY")
    .box(15, 15, 15, centered=False)
    .translate((35, 35, 35))
)

# For a 45-degree plane cut, we need to cut diagonally
# Create a larger cutting box and rotate it to create the plane effect
# The cutting volume should be positioned at corner (50, 50, 50)
# and extend inward 15mm along each axis

cutting_plane_box = (
    cq.Workplane("XY")
    .box(30, 30, 30, centered=False)
    .translate((20, 20, 20))
)

# Cut using a box positioned at the corner - this creates the triangular cut
# We'll cut a box from (35,35,35) to (50,50,50) which creates the corner removal
result = result.cut(cutting_solid)

