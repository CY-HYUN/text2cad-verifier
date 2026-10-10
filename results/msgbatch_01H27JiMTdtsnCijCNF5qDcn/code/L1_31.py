import cadquery as cq
import math

sphere = cq.Workplane("XY").sphere(25.0)
column = cq.Workplane("XY").rect(20.0, 20.0).extrude(25.0, both=True)
result = sphere.cut(column)
