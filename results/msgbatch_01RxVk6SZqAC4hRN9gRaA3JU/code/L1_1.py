import cadquery as cq
import math

af = 50.0                      # across flats
h = 20.0
circ_d = af / math.cos(math.radians(30))   # circumscribed diameter

# Hexagon with vertices on X axis -> top/bottom sides horizontal
prism = cq.Workplane("XY").polygon(6, circ_d).extrude(h)

# 45° chamfer, 2 mm, on the outer edges of the top face
try:
    prism = prism.edges(">Z").chamfer(2.0)
except Exception:
    pass

# Central through-hole, diameter 50 mm
hole = cq.Workplane("XY").circle(50.0 / 2).extrude(h * 3).translate((0, 0, -h))
result = prism.cut(hole)
