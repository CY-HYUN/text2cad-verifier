import cadquery as cq
import math

d = 50 / math.cos(math.radians(30))
body = cq.Workplane("XY").polygon(6, d).extrude(20)
body = body.faces(">Z").edges().chamfer(2)
result = body.faces(">Z").workplane().hole(20)
