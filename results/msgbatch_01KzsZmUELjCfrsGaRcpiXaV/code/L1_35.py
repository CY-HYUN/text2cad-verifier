import cadquery as cq
import math

# Create the main cylinder
main_cylinder = cq.Workplane("XY").cylinder(height=40, radius=20, centered=False)

# Create a cone for the pit by revolving a triangle
# The cone has base diameter 30mm (radius 15mm) and depth 15mm
# Create a 2D profile of the cone cross-section (a triangle)
cone_profile = cq.Workplane("XZ").polyline([
    (0, 40),      # tip of cone at top of cylinder
    (15, 25),     # base of cone at radius 15mm, depth 15mm down
    (0, 25)       # back to center at bottom of cone
]).close()

# Revolve the profile around the Z-axis to create a cone
cone = cone_profile.revolve(axisEnd=(0, 0, 1), axisStart=(0, 0, 0))

# Cut the cone from the cylinder
result = main_cylinder.cut(cone)
