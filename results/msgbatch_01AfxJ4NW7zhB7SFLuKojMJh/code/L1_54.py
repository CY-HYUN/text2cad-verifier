import cadquery as cq
import math

sphere = cq.Workplane("XY").sphere(25)
hole = cq.Workplane("XY").workplane(offset=-30).circle(7).extrude(60)
result = sphere.cut(hole)
