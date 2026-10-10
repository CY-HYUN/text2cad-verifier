import cadquery as cq
import math

# Create a sphere with radius 40mm
sphere = cq.Workplane("XY").sphere(40)

# Create a cylinder with diameter 30mm (radius 15mm)
# The cylinder's axis is 25mm away from the sphere's center
# We'll position the cylinder so its axis is offset by 25mm in the X direction
cylinder = cq.Workplane("XY").cylinder(height=100, radius=15, centered=True)

# Translate the cylinder so its axis is 25mm away from the sphere center
# The cylinder axis will be along Z, offset in X by 25mm
cylinder = cylinder.translate((25, 0, 0))

# Perform the boolean subtraction: sphere minus cylinder
result = sphere.cut(cylinder)
