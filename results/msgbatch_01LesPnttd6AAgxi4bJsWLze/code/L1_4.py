import cadquery as cq
import math

# Create the bottom large cylinder
bottom_cylinder = cq.Workplane("XY").circle(80/2).extrude(20)

# Create the top small cylinder
# Position it at the top of the bottom cylinder (Z = 20)
top_cylinder = cq.Workplane("XY").workplane(offset=20).circle(40/2).extrude(30)

# Combine both cylinders
result = bottom_cylinder.union(top_cylinder)
