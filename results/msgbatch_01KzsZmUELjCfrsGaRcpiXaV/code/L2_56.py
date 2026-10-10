import cadquery as cq
import math

# Create the base solid - two cylinders intersecting orthogonally
# First cylinder (along Z axis) - diameter 40mm, length 100mm
cylinder1 = cq.Workplane("XY").cylinder(height=100, radius=20, centered=True)

# Second cylinder (along X axis) - diameter 40mm, length 100mm
cylinder2 = cq.Workplane("YZ").cylinder(height=100, radius=20, centered=True)

# Boolean union to create the cross shape
cross_solid = cylinder1.union(cylinder2)

# Shell the solid to create hollow tubes with 2mm wall thickness
shelled = cross_solid.shell(2.0)

result = shelled
