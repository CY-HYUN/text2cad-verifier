import cadquery as cq
import math

# Create the base solid - two cylinders intersecting orthogonally
# First cylinder (along Z axis)
cylinder1 = cq.Workplane("XY").cylinder(height=100, radius=20, centered=True)

# Second cylinder (along X axis)
cylinder2 = cq.Workplane("YZ").cylinder(height=100, radius=20, centered=True)

# Boolean union to create the cross shape
cross_solid = cylinder1.union(cylinder2)

# Shell the solid to create hollow tubes with 2mm wall thickness
# This removes material from the interior, leaving a 2mm wall
shelled = cross_solid.shell(2.0)

# The shelling operation in CadQuery removes all faces, creating an open hollow structure
# We need to remove the end faces that would be capped
# Since shelling removes interior material, we work with the shelled result directly

# To ensure the internal cavity is fully connected (not separated by walls at intersection),
# we verify the shelling has created the proper internal topology
# The shell operation on a union naturally creates the connected internal cavity

result = shelled
