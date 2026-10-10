import cadquery as cq

# Create the cylinder base
cylinder = cq.Workplane("XY").cylinder(height=20, radius=25, centered=False)

# Create the cone on top
# The cone's base should be at z=20 (top of cylinder) and extend to z=60
cone = cq.Workplane("XY").cone(height=40, radius1=25, radius2=0, centered=False).translate((0, 0, 20))

# Combine the cylinder and cone
result = cylinder.union(cone)
