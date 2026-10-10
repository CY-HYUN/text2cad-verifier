import cadquery as cq
import math

# Cube of 50 mm edge, with one corner at the origin
cube = cq.Workplane("XY").box(50, 50, 50, centered=False)

# Sphere of radius 30 mm centered on the vertex at the origin
sphere = cq.Workplane("XY").sphere(30)

# Boolean subtract the sphere from the cube
result = cube.cut(sphere)
