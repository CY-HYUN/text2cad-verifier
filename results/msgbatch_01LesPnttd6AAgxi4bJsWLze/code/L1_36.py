import cadquery as cq
import math

# Create the outer cylinder (centered at origin)
outer_cylinder = cq.Workplane("XY").cylinder(height=20, radius=40, centered=True)

# Create the inner cylinder (offset 10mm to the right/positive X direction)
# We'll subtract this from the outer cylinder
inner_cylinder = cq.Workplane("XY").workplane(offset=0).moveTo(10, 0).cylinder(height=20, radius=20, centered=True)

# Create the eccentric ring by subtracting the offset inner cylinder from the outer cylinder
result = outer_cylinder.cut(inner_cylinder)
