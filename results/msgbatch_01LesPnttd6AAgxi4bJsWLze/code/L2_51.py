import cadquery as cq
import math

# Create the main vertical cylinder (stem of the T)
vertical_cyl = cq.Workplane("XY").cylinder(height=60, radius=10, centered=True)

# Create the horizontal cylinder (arm of the T)
horizontal_cyl = cq.Workplane("XY").cylinder(height=60, radius=10, centered=False).rotateAboutCenter((0, 1, 0), 90)

# Fuse the cylinders to create the T-shape
t_shape = vertical_cyl.union(horizontal_cyl)

# Add fillets to round all edges with 8mm radius
t_shape = t_shape.edges().fillet(8)

# Create drilling positions for the three end faces
# Face 1: Top of vertical cylinder (0, 0, 30)
# Face 2: Bottom of vertical cylinder (0, 0, -30)
# Face 3: End of horizontal cylinder (30, 0, 0)

# Drill holes at each end
drill_diameter = 5
drill_radius = drill_diameter / 2
drill_depth = 15

# Create three drill holes
hole1 = cq.Workplane("XY").workplane(offset=30).circle(drill_radius).cutBlind(-drill_depth)
hole2 = cq.Workplane("XY").workplane(offset=-30).circle(drill_radius).cutBlind(drill_depth)
hole3_workplane = cq.Workplane("YZ").workplane(offset=30).circle(drill_radius).cutBlind(-drill_depth)

# Apply the holes to the T-shape
result = t_shape.cut(hole1).cut(hole2).cut(hole3_workplane)
