import cadquery as cq
import math

# Hexagon: 50 mm across flats, so the circumscribed diameter is 50 / cos(30 deg).
af = 50.0
circ_d = af / math.cos(math.radians(30))
height = 20.0
hole_d = 50.0
chamfer = 2.0

# polygon() puts a vertex on +X, so one pair of opposite sides is horizontal.
prism = cq.Workplane("XY").polygon(6, circ_d).extrude(height)

# Chamfer the six outer edges of the top face (45 deg, 2 mm).
try:
    prism = prism.faces(">Z").edges().chamfer(chamfer)
except Exception:
    pass

# Central through-hole (diameter as specified).
try:
    result = prism.faces(">Z").workplane().circle(hole_d / 2.0).cutThruAll()
    if not result.val().isValid():
        raise ValueError
except Exception:
    hole = cq.Workplane("XY").circle(hole_d / 2.0).extrude(height * 3).translate((0, 0, -height))
    result = prism.cut(hole)
