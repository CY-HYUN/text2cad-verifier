import cadquery as cq

# Create the horizontal cylinder (along X-axis)
# Diameter 20mm, length 80mm, centered at origin
horizontal_cylinder = cq.Workplane("XY").cylinder(height=80, radius=10, centered=True)

# Create the vertical cylinder (along Z-axis)
# Diameter 20mm, length 40mm, positioned at the midpoint of horizontal cylinder
# The vertical cylinder should be positioned so its base is at z=0 and extends upward
vertical_cylinder = (cq.Workplane("XY")
                     .workplane(offset=0)
                     .cylinder(height=40, radius=10, centered=False))

# Move the vertical cylinder so it's centered at the origin in X-Y plane
# and positioned to create the T-shape (extends from z=0 to z=40)
vertical_cylinder = vertical_cylinder.translate((0, 0, 0))

# Union the two cylinders to create the T-shaped solid
result = horizontal_cylinder.union(vertical_cylinder)
