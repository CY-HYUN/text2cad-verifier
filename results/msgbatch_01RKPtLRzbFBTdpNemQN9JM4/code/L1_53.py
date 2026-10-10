import cadquery as cq
import math

base = cq.Workplane("XY").ellipse(40, 25).extrude(25)
base = base.faces(">Z").edges().chamfer(0.8)
hole = cq.Workplane("XY").center(10, 0).circle(8).extrude(25)
result = base.cut(hole)
