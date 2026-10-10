import cadquery as cq
import math

# Create the cylindrical handle
# Diameter 30 mm means radius 15 mm
cylinder = cq.Workplane("XY").cylinder(height=100, radius=15, centered=True)
cylinder = cylinder.translate((0, 0, 50))

# Create the sphere
# Sphere has diameter 40 mm, so radius 20 mm
# The sphere's center is 15 mm above the top of the cylinder (at z=100+15=115)
sphere = cq.Workplane("XY").sphere(radius=20).translate((0, 0, 115))

# Combine the cylinder and sphere
result = cylinder.union(sphere)
