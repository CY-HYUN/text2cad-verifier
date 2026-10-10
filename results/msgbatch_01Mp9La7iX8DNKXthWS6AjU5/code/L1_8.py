import cadquery as cq
import math

# Cube 80x80x40, centered on XY, base at z=0
cube = cq.Workplane("XY").rect(80.0, 80.0).extrude(40.0)

# Sphere centered at the center of the top surface (0,0,40), radius 20
sphere = cq.Workplane("XY").sphere(20.0).translate((0, 0, 40.0))

# Cut: only the lower half of the sphere lies inside the cube, forming a hemispherical recess
result = cube.cut(sphere)
