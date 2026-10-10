import cadquery as cq
import math

body = cq.Workplane("XY").circle(30).extrude(40)
hole = cq.Workplane("XY").center(15, 0).circle(5).extrude(40)
result = body.cut(hole)
