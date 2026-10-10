import cadquery as cq
import math

# Main cylinder: diameter 40, height 60, base at z=0
body = cq.Workplane("XY").circle(20).extrude(60)

# Spherical cavity: diameter 30, centered at cylinder center (z=30)
sphere = cq.Workplane("XY").sphere(15).translate((0, 0, 30))
body = body.cut(sphere)

# Through-hole on top: diameter 10, from top face down to the cavity
hole = cq.Workplane("XY").workplane(offset=30).circle(5).extrude(30)
body = body.cut(hole)

result = body
