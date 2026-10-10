import cadquery as cq
import math

# Create the main cylinder
main_cylinder = cq.Workplane("XY").cylinder(height=40, radius=20, centered=False)

# Create a cone for the pit (base diameter 30mm = radius 15mm, depth 15mm)
# The cone needs to be positioned at the top of the cylinder
# We'll create it pointing downward (into the cylinder)
cone = cq.Workplane("XY").cone(height=15, radius1=15, radius2=0, centered=False)

# Move the cone to the top center of the cylinder
# The cylinder is at z=0 to z=40, so the cone base should be at z=40
cone = cone.translate((0, 0, 40))

# Cut the cone from the cylinder
result = main_cylinder.cut(cone)
