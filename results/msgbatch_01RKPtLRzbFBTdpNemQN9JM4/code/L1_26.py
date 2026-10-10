import cadquery as cq
import math

sphere = cq.Workplane("XY").sphere(30)
cutter = cq.Workplane("XY").workplane(offset=15).rect(100, 100).extrude(50)
result = sphere.cut(cutter)
