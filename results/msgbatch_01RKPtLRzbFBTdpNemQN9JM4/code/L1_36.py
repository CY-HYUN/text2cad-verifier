import cadquery as cq
import math

outer = cq.Workplane("XY").circle(40).extrude(20)
inner = cq.Workplane("XY").center(10, 0).circle(20).extrude(20)
result = outer.cut(inner)
