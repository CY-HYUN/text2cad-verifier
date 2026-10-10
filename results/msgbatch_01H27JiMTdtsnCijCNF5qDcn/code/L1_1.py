import cadquery as cq
import math

af = 50.0
d = af / math.cos(math.radians(30))
prism = cq.Workplane("XY").polygon(6, d).extrude(20.0)
prism = prism.faces(">Z").edges().chamfer(2.0)
hole = cq.Workplane("XY").circle(25.0).extrude(20.0)
result = prism.cut(hole)
