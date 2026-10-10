import cadquery as cq
import math

# Main cylinder: diameter 40, height 60, centered at origin in XY, spanning z = 0..60
body = cq.Workplane("XY").circle(20).extrude(60)

# Spherical cavity: diameter 30, centered at cylinder's geometric center (z = 30)
sphere = cq.Workplane("XY").sphere(15).translate((0, 0, 30))
body = body.cut(sphere)

# Through-hole: diameter 10 from top surface down into the cavity
hole = cq.Workplane("XY").workplane(offset=30).circle(5).extrude(30)
body = body.cut(hole)

result = body
