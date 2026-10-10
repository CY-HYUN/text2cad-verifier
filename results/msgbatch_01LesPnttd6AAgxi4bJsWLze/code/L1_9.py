import cadquery as cq
import math

# Create the cylindrical handle
cylinder = cq.Workplane("XY").cylinder(height=100, radius=15, centered=False)

# Create the sphere
# Sphere has diameter 40 mm, so radius is 20 mm
# The sphere's center is 15 mm above the top of the cylinder (at z=115)
# The bottom of the sphere (at z=95) is embedded 5 mm into the cylinder (cylinder top is at z=100)
sphere = cq.Workplane("XY").sphere(radius=20).translate((0, 0, 115))

# Combine the cylinder and sphere
result = cylinder.union(sphere)
