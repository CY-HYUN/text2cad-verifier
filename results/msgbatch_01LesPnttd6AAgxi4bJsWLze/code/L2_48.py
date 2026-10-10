import cadquery as cq
import math

# Create a cube with edge length 50 mm
cube = cq.Solid.makeBox(50, 50, 50)

# Create a sphere with radius 30 mm centered at one corner (0, 0, 0)
sphere = cq.Solid.makeSphere(30)

# The sphere is centered at origin, so we need to position it at a corner of the cube
# We'll use the corner at (0, 0, 0) which is already at the origin
# Perform Boolean subtraction: remove the sphere from the cube
result = cube.cut(sphere)
