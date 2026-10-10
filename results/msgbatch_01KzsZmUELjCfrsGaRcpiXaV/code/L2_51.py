import cadquery as cq
import math

# Create the main vertical cylinder (stem of the T)
vertical_cyl = cq.Workplane("XY").cylinder(height=60, radius=10, centered=True)

# Create the horizontal cylinder (arm of the T) 
horizontal_cyl = cq.Workplane("XY").cylinder(height=60, radius=10, centered=True).rotateAboutCenter((0, 1, 0), 90)

# Fuse the cylinders to create the T-shape
t_shape = vertical_cyl.union(horizontal_cyl)

# Add fillets to round all edges with 8mm radius
t_shape = t_shape.edges().fillet(8)

# Drill holes at each end face
# Top hole (along Z-axis, positive direction)
result = t_shape.faces(">Z").workplane().hole(5, depth=15)

# Bottom hole (along Z-axis, negative direction)
result = result.faces("<Z").workplane().hole(5, depth=15)

# End hole (along X-axis, positive direction)
result = result.faces(">X").workplane().hole(5, depth=15)

