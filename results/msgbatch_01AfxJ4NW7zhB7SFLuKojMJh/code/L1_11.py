import cadquery as cq
import math

# Main cylinder: diameter 60, height 40, axis along Z (base at z=0)
body = cq.Workplane("XY").circle(30).extrude(40)

# Off-center through-hole: diameter 10, offset 15 mm along X
hole = cq.Workplane("XY").center(15, 0).circle(5).extrude(40)

result = body.cut(hole)
