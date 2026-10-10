import cadquery as cq
import math

# Create the outer frustum
outer_radius_bottom = 70 / 2  # 35 mm
outer_radius_top = 40 / 2     # 20 mm
height = 60                     # mm
chamfer_width = 2               # mm

# Create the solid frustum (cone truncated)
frustum = cq.Workplane("XY").circle(outer_radius_bottom).workplane(offset=height).circle(outer_radius_top).loft(ruled=True)

# Create the through-hole (cylinder through the entire height)
hole_radius = 20 / 2  # 10 mm
hole = cq.Workplane("XY").circle(hole_radius).extrude(height)

# Subtract the hole from the frustum
result = frustum.cut(hole)

# Apply 45° chamfer on the outer edge of the base
# The base edge is the circle at z=0 with radius 35
result = result.edges(">Z").chamfer(chamfer_width)

