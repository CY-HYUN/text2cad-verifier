import cadquery as cq
import math

# Create a cube with edge length 50mm
cube = cq.Workplane("XY").box(50, 50, 50)

# Create a sphere with radius 30mm centered at one vertex of the cube
# The cube is centered at origin, so vertices are at (±25, ±25, ±25)
# We'll use the vertex at (25, 25, 25)
sphere = cq.Workplane("XY").sphere(30).translate((25, 25, 25))

# Boolean subtract (cut) the sphere from the cube
result = cube.cut(sphere)
