import cadquery as cq
import math

af = 50.0
d_circ = af / math.cos(math.radians(30))

prism = cq.Workplane("XY").polygon(6, d_circ).extrude(20.0)
prism = prism.faces(">Z").edges().chamfer(2.0)

try:
    cutter = cq.Workplane("XY").circle(25.0).extrude(20.0)
    result = prism.cut(cutter)
    if not result.val().isValid():
        raise ValueError
except Exception:
    cutter = cq.Workplane("XY").circle(24.99).extrude(20.0)
    result = prism.cut(cutter)
