import cadquery as cq
import math

# Create the outer cylinder
outer_cylinder = cq.Workplane("XY").cylinder(height=120, radius=20, centered=True)

# Create the inner hole (subtract)
inner_hole = cq.Workplane("XY").cylinder(height=120, radius=12.5, centered=True)

# Subtract the inner hole from the outer cylinder to create the hollow cylindrical part
result = outer_cylinder.cut(inner_hole)
