import cadquery as cq

# Create the horizontal cylinder (along X-axis)
# Diameter 20mm, length 80mm, centered at origin
horizontal_cylinder = cq.Workplane("XY").cylinder(height=80, radius=10, centered=True)

# Create the vertical cylinder (along Z-axis)
# Diameter 20mm, length 40mm, positioned to extend upward from the horizontal cylinder
# The vertical cylinder should be positioned so it extends from z=0 to z=40
vertical_cylinder = cq.Workplane("XY").cylinder(height=40, radius=10, centered=False)

# Union the two cylinders to create the T-shaped solid
result = horizontal_cylinder.union(vertical_cylinder)
