import cadquery as cq
import math

sphere = cq.Workplane("XY").sphere(25)
hole = cq.Workplane("XY").rect(20, 20).extrude(60, both=True)
result = sphere.cut(hole)
